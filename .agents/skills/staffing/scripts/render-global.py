#!/usr/bin/env python3
"""Render, stage, byte-check, or barrier-apply staffing-owned global artifacts.

Adapted from skills/system/setup-asher-skills/scripts/render-global.py.
"""

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


def provider_name() -> str:
    provider = (TEMPLATES / "provider.txt").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[a-z0-9-]+", provider):
        raise ValueError("invalid or missing compiled provider identity")
    return provider


def payloads() -> dict[str, bytes]:
    common = (TEMPLATES / "staffing.common.md").read_text(encoding="utf-8").rstrip("\n")
    overlay = (TEMPLATES / "staffing.module.md").read_text(encoding="utf-8")
    if overlay.count("{{COMMON}}") != 1:
        raise ValueError("staffing.module.md must contain one {{COMMON}} marker")
    return {
        "module": overlay.replace("{{COMMON}}", common).encode("utf-8"),
        "pointer": (TEMPLATES / "staffing-pointer.md").read_bytes(),
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


def stage(provider: str, module: Path, barrier: Path, data: bytes, pointer: bytes) -> None:
    state = read_barrier(barrier)
    if os.environ.get("ASHER_SKILLS_FAIL_MODULE") == f"staffing:{provider}":
        raise ValueError("injected module staging failure")
    if not module.is_file() or module.read_bytes() != data:
        write_atomic(module, data)
    if module.read_bytes() != data:
        raise ValueError(f"module read-back mismatch: {module}")
    state["verified"][f"staffing:{provider}"] = {
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


def require_presentation_pair(
    state: dict[str, object], provider: str, global_file: Path
) -> None:
    records = state.get("preflight")
    if not isinstance(records, dict) or set(records) < {"claude", "codex"}:
        raise ValueError("both global files must pass Presentation preflight before Staffing apply")
    if Path(records[provider]["path"]) != global_file.resolve():
        raise ValueError(f"preflight path mismatch: {provider}")
    for candidate in ("claude", "codex"):
        path = Path(records[candidate]["path"])
        if not path.is_file():
            raise ValueError(f"Presentation must apply before Staffing: {candidate}")
        if digest(section_bytes(path.read_bytes(), "Presentation")) != records[candidate]["section_hash"]:
            raise ValueError(f"Presentation must apply before Staffing: {candidate}")


def reconcile_section(original: bytes, section: bytes, provider: str) -> bytes:
    text = original.decode("utf-8")
    match = re.search(r"(?m)^## Staffing\n", text)
    section_text = section.decode("utf-8").rstrip("\n") + "\n"
    if match:
        next_heading = re.search(r"(?m)^## ", text[match.end():])
        end = match.end() + next_heading.start() if next_heading else len(text)
        suffix = text[end:]
        separator = "\n" if suffix else ""
        return (text[:match.start()] + section_text + separator + suffix).encode("utf-8")
    header = (TEMPLATES / "global-header.txt").read_text(encoding="utf-8")
    base = text if text else header
    return (base.rstrip("\n") + "\n\n" + section_text).encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("render", "check", "stage", "apply"))
    parser.add_argument("--module", type=Path)
    parser.add_argument("--pointer", type=Path)
    parser.add_argument("--barrier", type=Path)
    parser.add_argument("--global-file", type=Path)
    args = parser.parse_args(argv)
    try:
        provider = provider_name()
        expected = payloads()
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
            stage(provider, args.module, args.barrier, expected["module"], expected["pointer"])
        else:
            if not args.global_file or not args.barrier:
                parser.error("apply requires --global-file and --barrier")
            state = require_barrier(args.barrier)
            require_presentation_pair(state, provider, args.global_file)
            original = args.global_file.read_bytes() if args.global_file.exists() else b""
            reconciled = reconcile_section(original, expected["pointer"], provider)
            if reconciled != original:
                write_atomic(args.global_file, reconciled)
        print(json.dumps({name: digest(expected[name]) for name in expected}, sort_keys=True))
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
