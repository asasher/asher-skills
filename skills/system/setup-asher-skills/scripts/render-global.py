#!/usr/bin/env python3
"""Render, stage, byte-check, or barrier-apply setup-owned global artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates" / "global"
REQUIRED_BARRIER = {
    "presentation:claude", "presentation:codex", "staffing:claude", "staffing:codex"
}


def payloads(provider: str) -> dict[str, bytes]:
    return {
        "module": (TEMPLATES / "presentation.common.md").read_bytes(),
        "pointer": (TEMPLATES / f"presentation-pointer.{provider}.md").read_bytes(),
    }


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}-{secrets.token_hex(8)}")
    try:
        temporary.write_bytes(data)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def read_barrier(path: Path) -> dict[str, object]:
    if path.is_symlink():
        raise ValueError(f"refusing symlink barrier: {path}")
    if not path.exists():
        raise ValueError(f"barrier has not begun: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if (
        data.get("schema_version") != 1
        or not isinstance(data.get("transaction"), str)
        or not data["transaction"]
        or not isinstance(data.get("preflight"), dict)
        or not isinstance(data.get("verified"), dict)
    ):
        raise ValueError(f"invalid barrier: {path}")
    return data


def begin_barrier(path: Path) -> None:
    if path.is_symlink():
        raise ValueError(f"refusing symlink barrier: {path}")
    state = {
        "schema_version": 1,
        "transaction": secrets.token_hex(16),
        "preflight": {},
        "verified": {},
    }
    write_atomic(path, (json.dumps(state, indent=2, sort_keys=True) + "\n").encode())


def stage(
    owner: str, provider: str, module: Path, barrier: Path, data: bytes, pointer: bytes
) -> None:
    state = read_barrier(barrier)
    if os.environ.get("ASHER_SKILLS_FAIL_MODULE") == f"{owner}:{provider}":
        raise ValueError("injected module staging failure")
    if not module.is_file() or module.read_bytes() != data:
        write_atomic(module, data)
    if module.read_bytes() != data:
        raise ValueError(f"module read-back mismatch: {module}")
    state["verified"][f"{owner}:{provider}"] = {
        "path": str(module.resolve()),
        "hash": digest(data),
        "pointer_hash": digest(pointer),
    }
    write_atomic(barrier, (json.dumps(state, indent=2, sort_keys=True) + "\n").encode())


def require_barrier(path: Path) -> dict[str, object]:
    state = read_barrier(path)
    verified = state["verified"]
    if set(verified) < REQUIRED_BARRIER:
        raise ValueError("all four deferred modules must be staged before pointer application")
    for key in sorted(REQUIRED_BARRIER):
        record = verified[key]
        module = Path(record["path"])
        if not module.is_file() or digest(module.read_bytes()) != record.get("hash"):
            raise ValueError(f"barrier module is unreadable or changed: {key}")
    return state


def section_bytes(data: bytes, heading: str) -> bytes:
    text = data.decode("utf-8")
    match = re.search(rf"(?m)^## {re.escape(heading)}\n", text)
    if not match:
        return b""
    next_heading = re.search(r"(?m)^## ", text[match.end():])
    end = match.end() + next_heading.start() if next_heading else len(text)
    return (text[match.start():end].rstrip("\n") + "\n").encode("utf-8")


def reconcile_section(original: bytes, heading: str, section: bytes, provider: str) -> bytes:
    text = original.decode("utf-8")
    match = re.search(rf"(?m)^## {re.escape(heading)}\n", text)
    section_text = section.decode("utf-8").rstrip("\n") + "\n"
    if match:
        next_heading = re.search(r"(?m)^## ", text[match.end():])
        end = match.end() + next_heading.start() if next_heading else len(text)
        suffix = text[end:]
        separator = "\n" if suffix else ""
        return (text[:match.start()] + section_text + separator + suffix).encode("utf-8")
    header = f"# Global {'AGENTS' if provider == 'codex' else 'CLAUDE'}.md\n"
    legacy = re.search(r"(?m)^## Conventions\n", text)
    if legacy:
        marker = "Seeded by `setup-asher-skills` (`templates/global-conventions.md`)"
        legacy_header = f"# Global {'AGENTS' if provider == 'codex' else 'CLAUDE'}.md — machine-level conventions\n"
        if not text.startswith(legacy_header) or marker not in text[:legacy.start()]:
            raise ValueError("unrecognized ## Conventions owner; refusing automatic migration")
        next_heading = re.search(r"(?m)^## ", text[legacy.end():])
        end = legacy.end() + next_heading.start() if next_heading else len(text)
        suffix = text[end:]
        separator = "\n" if suffix else ""
        return (header + "\n" + section_text + separator + suffix).encode("utf-8")
    staffing = re.search(r"(?m)^## Staffing\n", text)
    if staffing:
        return (text[:staffing.start()] + section_text + "\n" + text[staffing.start():]).encode("utf-8")
    base = text if text else header
    return (base.rstrip("\n") + "\n\n" + section_text).encode("utf-8")


def preflight(provider: str, global_file: Path, barrier: Path, pointer: bytes) -> None:
    state = require_barrier(barrier)
    original = global_file.read_bytes() if global_file.exists() else b""
    reconciled = reconcile_section(original, "Presentation", pointer, provider)
    state.setdefault("preflight", {})[provider] = {
        "path": str(global_file.resolve()),
        "original_hash": digest(original),
        "result_hash": digest(reconciled),
        "section_hash": digest(pointer),
    }
    write_atomic(barrier, (json.dumps(state, indent=2, sort_keys=True) + "\n").encode())


def require_preflight(
    state: dict[str, object], provider: str, global_file: Path
) -> None:
    records = state.get("preflight")
    if not isinstance(records, dict) or set(records) < {"claude", "codex"}:
        raise ValueError("both global files must pass Presentation preflight before pointer application")
    record = records[provider]
    if Path(record["path"]) != global_file.resolve():
        raise ValueError(f"preflight path mismatch: {provider}")
    current = global_file.read_bytes() if global_file.exists() else b""
    if digest(current) not in {record["original_hash"], record["result_hash"]}:
        raise ValueError(f"global file changed after preflight: {provider}")


def finalize_barrier(path: Path) -> None:
    state = require_barrier(path)
    records = state.get("preflight")
    if not isinstance(records, dict) or set(records) < {"claude", "codex"}:
        raise ValueError("both global files must pass Presentation preflight before finalize")
    for provider in ("claude", "codex"):
        global_file = Path(records[provider]["path"])
        if not global_file.is_file():
            raise ValueError(f"final global file is unreadable: {provider}")
        data = global_file.read_bytes()
        for owner, heading in (("presentation", "Presentation"), ("staffing", "Staffing")):
            expected = state["verified"][f"{owner}:{provider}"]["pointer_hash"]
            if digest(section_bytes(data, heading)) != expected:
                raise ValueError(f"final {heading} section mismatch: {provider}")
    path.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=("begin", "render", "check", "stage", "preflight", "apply", "finalize")
    )
    parser.add_argument("--provider", choices=("claude", "codex"))
    parser.add_argument("--module", type=Path)
    parser.add_argument("--pointer", type=Path)
    parser.add_argument("--barrier", type=Path)
    parser.add_argument("--global-file", type=Path)
    parser.add_argument(
        "--audited", type=Path,
        help="machine-tuned module content (placeholders filled); replaces the template seed for check/stage",
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "begin":
            if not args.barrier:
                parser.error("begin requires --barrier")
            begin_barrier(args.barrier)
            print(json.dumps({"barrier": str(args.barrier), "status": "begun"}, sort_keys=True))
            return 0
        if args.command == "finalize":
            if not args.barrier:
                parser.error("finalize requires --barrier")
            finalize_barrier(args.barrier)
            print(json.dumps({"barrier": str(args.barrier), "status": "finalized"}, sort_keys=True))
            return 0
        if not args.provider:
            parser.error(f"{args.command} requires --provider")
        expected = payloads(args.provider)
        if args.audited is not None:
            if args.command not in {"check", "stage"}:
                parser.error("--audited applies only to check and stage")
            expected["module"] = args.audited.read_bytes()
        if args.command in {"render", "check"}:
            if not args.module or not args.pointer:
                parser.error(f"{args.command} requires --module and --pointer")
            paths = {"module": args.module, "pointer": args.pointer}
            if args.command == "render":
                for name in ("module", "pointer"):
                    write_atomic(paths[name], expected[name])
            else:
                mismatches = [
                    name for name in ("module", "pointer")
                    if not paths[name].is_file() or paths[name].read_bytes() != expected[name]
                ]
                if mismatches:
                    print("mismatch: " + ", ".join(mismatches), file=sys.stderr)
                    return 1
        elif args.command == "stage":
            if not args.module or not args.barrier:
                parser.error("stage requires --module and --barrier")
            stage(
                "presentation", args.provider, args.module, args.barrier,
                expected["module"], expected["pointer"],
            )
        elif args.command == "preflight":
            if not args.global_file or not args.barrier:
                parser.error("preflight requires --global-file and --barrier")
            preflight(args.provider, args.global_file, args.barrier, expected["pointer"])
        else:
            if not args.global_file or not args.barrier:
                parser.error("apply requires --global-file and --barrier")
            state = require_barrier(args.barrier)
            require_preflight(state, args.provider, args.global_file)
            original = args.global_file.read_bytes() if args.global_file.exists() else b""
            reconciled = reconcile_section(original, "Presentation", expected["pointer"], args.provider)
            if reconciled != original:
                write_atomic(args.global_file, reconciled)
        print(json.dumps({name: digest(expected[name]) for name in expected}, sort_keys=True))
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
