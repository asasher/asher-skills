#!/usr/bin/env python3
"""Render, byte-check, or apply the staffing-owned global module and pointer.

Adapted from tools/global-modules/scripts/render-global.py.

apply writes the deferred module atomically (read-back verified), then reconciles the
`## Staffing` pointer section into the global file, preserving every foreign byte.
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


def section_bytes(data: bytes, heading: str) -> bytes:
    text = data.decode("utf-8")
    match = re.search(rf"(?m)^## {re.escape(heading)}\n", text)
    if not match:
        return b""
    next_heading = re.search(r"(?m)^## ", text[match.end():])
    end = match.end() + next_heading.start() if next_heading else len(text)
    return (text[match.start():end].rstrip("\n") + "\n").encode("utf-8")


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


def apply(provider: str, module: Path, global_file: Path, data: bytes, pointer: bytes) -> None:
    if os.environ.get("ASHER_SKILLS_FAIL_MODULE") == f"staffing:{provider}":
        raise ValueError("injected module apply failure")
    original = global_file.read_bytes() if global_file.exists() else b""
    reconciled = reconcile_section(original, pointer, provider)
    if not module.is_file() or module.read_bytes() != data:
        write_atomic(module, data)
    if module.read_bytes() != data:
        raise ValueError(f"module read-back mismatch: {module}")
    if reconciled != original:
        write_atomic(global_file, reconciled)
    if digest(section_bytes(global_file.read_bytes(), "Staffing")) != digest(
        pointer.rstrip(b"\n") + b"\n"
    ):
        raise ValueError(f"global read-back mismatch: {global_file}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("render", "check", "apply"))
    parser.add_argument("--module", type=Path)
    parser.add_argument("--pointer", type=Path)
    parser.add_argument("--global-file", type=Path)
    parser.add_argument(
        "--audited", type=Path,
        help="machine-tuned module content; replaces the template seed for check/apply",
    )
    args = parser.parse_args(argv)
    try:
        provider = provider_name()
        expected = payloads()
        if args.audited is not None:
            if args.command not in {"check", "apply"}:
                parser.error("--audited applies only to check and apply")
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
        else:
            if not args.module or not args.global_file:
                parser.error("apply requires --module and --global-file")
            apply(provider, args.module, args.global_file, expected["module"], expected["pointer"])
        print(json.dumps({name: digest(expected[name]) for name in expected}, sort_keys=True))
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
