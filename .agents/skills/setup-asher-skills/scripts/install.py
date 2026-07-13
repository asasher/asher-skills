#!/usr/bin/env python3
"""Inspect and safely reconcile installed-skill primary and alias mounts."""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import sys
from pathlib import Path

NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class MountError(ValueError):
    pass


def _absolute(path: Path) -> Path:
    return Path(os.path.abspath(path))


def _primary_state(primary: Path) -> str:
    if primary.is_symlink():
        return "symlink"
    if primary.is_dir():
        return "real-directory"
    if primary.exists():
        return "other"
    return "missing"


def _alias_state(alias: Path, primary: Path) -> dict[str, str]:
    result = {"path": str(alias)}
    if alias.is_symlink():
        raw_target = os.readlink(alias)
        target = Path(raw_target)
        if not target.is_absolute():
            target = alias.parent / target
        result["target"] = raw_target
        if _absolute(target) == _absolute(primary):
            result["state"] = "correct-symlink" if alias.exists() else "dangling-symlink"
        elif not alias.exists():
            result["state"] = "dangling-symlink"
        else:
            result["state"] = "wrong-symlink"
    elif alias.is_dir():
        result["state"] = "independent-directory"
    elif alias.exists():
        result["state"] = "other"
    else:
        result["state"] = "missing"
    return result


def inspect_mounts(primary: Path, aliases: list[Path]) -> dict[str, object]:
    primary = _absolute(primary)
    aliases = [_absolute(alias) for alias in aliases]
    return {
        "primary": {"path": str(primary), "state": _primary_state(primary)},
        "aliases": [_alias_state(alias, primary) for alias in aliases],
    }


def _replace_with_symlink(alias: Path, primary: Path) -> None:
    alias.parent.mkdir(parents=True, exist_ok=True)
    if not alias.parent.is_dir():
        raise MountError(f"alias parent is not a directory: {alias.parent}")
    relative_target = os.path.relpath(primary, alias.parent)
    temporary = alias.with_name(f".{alias.name}.mount-{secrets.token_hex(8)}")
    try:
        os.symlink(relative_target, temporary)
        os.replace(temporary, alias)
    finally:
        if temporary.is_symlink():
            temporary.unlink()


def reconcile_mounts(primary: Path, aliases: list[Path]) -> dict[str, object]:
    primary = _absolute(primary)
    aliases = [_absolute(alias) for alias in aliases]
    if len(aliases) != len(set(aliases)):
        raise MountError("alias paths must be unique")
    if primary in aliases:
        raise MountError("the primary path cannot also be an alias")

    before = inspect_mounts(primary, aliases)
    primary_state = before["primary"]["state"]
    if primary_state == "symlink":
        raise MountError(f"refusing primary symlink: {primary}")
    if primary_state != "real-directory":
        raise MountError(f"primary mount must be a real directory, found {primary_state}: {primary}")

    unsafe = [
        alias for alias in before["aliases"]
        if alias["state"] in {"independent-directory", "other"}
    ]
    if unsafe:
        detail = ", ".join(f"{alias['path']} ({alias['state']})" for alias in unsafe)
        raise MountError(f"refusing unsafe alias mount(s): {detail}")

    actions: list[dict[str, str]] = []
    for alias in before["aliases"]:
        if alias["state"] == "correct-symlink":
            continue
        alias_path = Path(alias["path"])
        _replace_with_symlink(alias_path, primary)
        actions.append({"path": str(alias_path), "action": "created" if alias["state"] == "missing" else "fixed"})

    after = inspect_mounts(primary, aliases)
    if any(alias["state"] != "correct-symlink" for alias in after["aliases"]):
        raise MountError("alias reconciliation did not produce the required mount state")
    after["actions"] = actions
    return after


def _mount_paths(args: argparse.Namespace) -> tuple[Path, list[Path]]:
    root = _absolute(args.root)
    primary_root = args.primary_root if args.primary_root.is_absolute() else root / args.primary_root
    alias_roots = args.alias_root or [Path(".claude/skills")]
    aliases = [
        (alias_root if alias_root.is_absolute() else root / alias_root) / args.name
        for alias_root in alias_roots
    ]
    return primary_root / args.name, aliases


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inspect", "reconcile"))
    parser.add_argument("name")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--primary-root", type=Path, default=Path(".agents/skills"))
    parser.add_argument("--alias-root", type=Path, action="append")
    args = parser.parse_args(argv)
    if not NAME.fullmatch(args.name):
        parser.error("name must be lower-kebab-case")

    primary, aliases = _mount_paths(args)
    try:
        result = (
            inspect_mounts(primary, aliases)
            if args.command == "inspect"
            else reconcile_mounts(primary, aliases)
        )
        print(json.dumps(result, indent=2, sort_keys=True))
    except (MountError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
