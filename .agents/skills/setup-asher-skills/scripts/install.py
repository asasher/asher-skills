#!/usr/bin/env python3
"""Inspect legacy mounts and safely publish/audit provider-specific skill trees."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import secrets
import shutil
import sys
import tempfile
from pathlib import Path

NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class MountError(ValueError):
    pass


def _catalog_module():
    path = Path(__file__).with_name("catalog.py")
    spec = importlib.util.spec_from_file_location("asher_skills_catalog", path)
    if spec is None or spec.loader is None:
        raise MountError(f"cannot load catalog compiler: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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
        result["finding"] = "undeclared-independent-copy"
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


def _provider_roots(values: list[str], root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise MountError("--provider-root must be PROVIDER=PATH")
        provider, raw_path = value.split("=", 1)
        if provider not in {"claude", "codex"} or provider in result or not raw_path:
            raise MountError(f"invalid or duplicate provider root: {value}")
        path = Path(raw_path)
        result[provider] = _absolute(path if path.is_absolute() else root / path)
    return dict(sorted(result.items()))


def _read_lock(path: Path) -> dict[str, object]:
    if path.is_symlink():
        raise MountError(f"refusing symlink lock: {path}")
    if not path.exists():
        return {"schema_version": 1, "skills": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MountError(f"invalid variant lock: {path}") from exc
    if data.get("schema_version") != 1 or not isinstance(data.get("skills"), dict):
        raise MountError(f"unsupported variant lock shape: {path}")
    return data


def _relative_or_absolute(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _variant_context(
    name: str, catalog_root: Path, root: Path, provider_roots: dict[str, Path]
):
    catalog = _catalog_module()
    graph = catalog.discover(catalog_root)
    if name not in graph:
        raise MountError(f"unknown skill: {name}")
    skill = graph[name]
    declared = dict(skill.variants)
    if not declared:
        raise MountError(f"{name}: skill does not declare provider variants")
    if not provider_roots or set(provider_roots) - set(declared):
        raise MountError(
            f"{name}: provider roots must be a non-empty subset of declarations "
            f"({', '.join(sorted(declared))})"
        )
    return catalog, skill


def publish_variant(
    name: str,
    catalog_root: Path,
    root: Path,
    provider_roots: dict[str, Path],
    lock_path: Path,
) -> dict[str, object]:
    """Compile and transactionally publish every declared provider tree plus its lock."""
    root = _absolute(root)
    catalog_root = _absolute(catalog_root)
    lock_path = _absolute(lock_path)
    catalog, skill = _variant_context(name, catalog_root, root, provider_roots)
    prior_lock = _read_lock(lock_path)
    prior_entry = prior_lock["skills"].get(name, {})

    with tempfile.TemporaryDirectory(prefix=f".{name}-variants-", dir=root) as temporary_raw:
        temporary = Path(temporary_raw)
        records: dict[str, dict[str, str]] = {}
        staged: dict[str, Path] = {}
        for provider in sorted(provider_roots):
            output = temporary / "compiled" / provider
            output.parent.mkdir(parents=True, exist_ok=True)
            records[provider] = catalog.materialize_variant(
                skill, catalog_root, provider, output
            )
            staged[provider] = output

        destinations = {
            provider: provider_roots[provider] / name for provider in sorted(provider_roots)
        }
        expected_codex = destinations.get("codex", root / ".agents" / "skills" / name)
        legacy_hash = catalog.tree_hash(catalog_root / skill.source)
        changes: list[str] = []

        # Preflight every destination and the lock before replacing any tree.
        for provider, destination in destinations.items():
            if destination.is_symlink():
                target = Path(os.readlink(destination))
                if not target.is_absolute():
                    target = destination.parent / target
                if provider == "codex" or _absolute(target) != expected_codex:
                    raise MountError(f"refusing unexpected provider symlink: {destination}")
                changes.append(provider)
            elif destination.is_dir():
                actual_hash = catalog.tree_hash(destination)
                if actual_hash == records[provider]["effective_hash"]:
                    continue
                locked_provider = (
                    prior_entry.get("providers", {}).get(provider, {})
                    if isinstance(prior_entry, dict)
                    else {}
                )
                if not locked_provider and not (
                    provider == "codex" and actual_hash == legacy_hash
                ):
                    raise MountError(f"refusing undeclared independent provider directory: {destination}")
                changes.append(provider)
            elif destination.exists():
                raise MountError(f"refusing non-directory provider mount: {destination}")
            else:
                changes.append(provider)

        source_revision = next(iter(records.values()))["source_revision"]
        new_entry = {
            "source": skill.source,
            "source_revision": source_revision,
            "providers": {
                provider: {
                    "provider": provider,
                    "mount": _relative_or_absolute(destinations[provider], root),
                    "effective_hash": records[provider]["effective_hash"],
                }
                for provider in sorted(destinations)
            },
        }
        next_lock = json.loads(json.dumps(prior_lock))
        next_lock["skills"][name] = new_entry
        lock_changed = prior_entry != new_entry

        backups: dict[str, Path] = {}
        published: list[str] = []
        try:
            for index, provider in enumerate(changes, start=1):
                destination = destinations[provider]
                destination.parent.mkdir(parents=True, exist_ok=True)
                backup = temporary / "backups" / provider
                backup.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists() or destination.is_symlink():
                    os.replace(destination, backup)
                    backups[provider] = backup
                os.replace(staged[provider], destination)
                published.append(provider)
                if os.environ.get("ASHER_SKILLS_FAIL_AFTER_PROVIDER") == str(index):
                    raise MountError("injected provider publication failure")

            if lock_changed:
                lock_path.parent.mkdir(parents=True, exist_ok=True)
                lock_temp = lock_path.with_name(f".{lock_path.name}-{secrets.token_hex(8)}")
                lock_temp.write_text(
                    json.dumps(next_lock, indent=2, sort_keys=True) + "\n", encoding="utf-8"
                )
                os.replace(lock_temp, lock_path)
        except Exception:
            for provider in reversed(published):
                destination = destinations[provider]
                if destination.is_dir() and not destination.is_symlink():
                    shutil.rmtree(destination)
                elif destination.exists() or destination.is_symlink():
                    destination.unlink()
                backup = backups.get(provider)
                if backup is not None and (backup.exists() or backup.is_symlink()):
                    os.replace(backup, destination)
            raise

    actions = [f"published:{provider}" for provider in sorted(changes)]
    if lock_changed:
        actions.append("lock-updated")
    return {"skill": name, "source_revision": source_revision, "actions": actions}


def audit_variant(
    name: str,
    catalog_root: Path,
    root: Path,
    provider_roots: dict[str, Path],
    lock_path: Path,
) -> dict[str, object]:
    """Classify declared provider-tree divergence without changing the consumer."""
    root = _absolute(root)
    catalog_root = _absolute(catalog_root)
    catalog, skill = _variant_context(name, catalog_root, root, provider_roots)
    lock = _read_lock(_absolute(lock_path))
    entry = lock["skills"].get(name)
    findings: list[dict[str, str]] = []

    with tempfile.TemporaryDirectory(prefix=f".{name}-audit-", dir=root) as temporary_raw:
        temporary = Path(temporary_raw)
        records: dict[str, dict[str, str]] = {}
        expected_hash_to_provider: dict[str, str] = {}
        for provider in sorted(provider_roots):
            output = temporary / provider
            records[provider] = catalog.materialize_variant(
                skill, catalog_root, provider, output
            )
            expected_hash_to_provider[records[provider]["effective_hash"]] = provider

        expected_revision = next(iter(records.values()))["source_revision"]
        if (
            not isinstance(entry, dict)
            or entry.get("source") != skill.source
            or entry.get("source_revision") != expected_revision
        ):
            findings.append({"kind": "provider-lock-mismatch", "provider": "shared-source"})

        for provider, mount_root in sorted(provider_roots.items()):
            destination = mount_root / name
            if not destination.exists() and not destination.is_symlink():
                findings.append({"kind": "missing-provider-mount", "provider": provider})
                continue
            if destination.is_symlink() or not destination.is_dir():
                findings.append({"kind": "wrong-provider", "provider": provider})
                continue
            actual_hash = catalog.tree_hash(destination)
            expected_hash = records[provider]["effective_hash"]
            if actual_hash != expected_hash:
                actual_provider = expected_hash_to_provider.get(actual_hash)
                if actual_provider and actual_provider != provider:
                    findings.append(
                        {
                            "kind": "wrong-provider",
                            "provider": provider,
                            "actual_provider": actual_provider,
                        }
                    )
                findings.append({"kind": "altered-tree-hash", "provider": provider})
            locked = (
                entry.get("providers", {}).get(provider) if isinstance(entry, dict) else None
            )
            expected_mount = _relative_or_absolute(destination, root)
            if (
                not isinstance(locked, dict)
                or locked.get("provider") != provider
                or locked.get("mount") != expected_mount
                or locked.get("effective_hash") != expected_hash
            ):
                findings.append({"kind": "provider-lock-mismatch", "provider": provider})

            source = catalog_root / skill.source
            for relative in sorted(catalog.PROTECTED_VARIANT_PATHS):
                expected = source / relative
                actual = destination / relative
                if expected.is_file() and (
                    not actual.is_file() or actual.read_bytes() != expected.read_bytes()
                ):
                    findings.append(
                        {"kind": "shared-contract-drift", "provider": provider, "path": relative}
                    )

    return {"skill": name, "findings": findings}


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
    parser.add_argument(
        "command", choices=("inspect", "reconcile", "publish-variant", "audit-variant")
    )
    parser.add_argument("name")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--primary-root", type=Path, default=Path(".agents/skills"))
    parser.add_argument("--alias-root", type=Path, action="append")
    parser.add_argument("--catalog-root", type=Path)
    parser.add_argument("--provider-root", action="append", default=[])
    parser.add_argument("--lock", type=Path)
    args = parser.parse_args(argv)
    if not NAME.fullmatch(args.name):
        parser.error("name must be lower-kebab-case")

    try:
        if args.command in {"inspect", "reconcile"}:
            primary, aliases = _mount_paths(args)
            result = (
                inspect_mounts(primary, aliases)
                if args.command == "inspect"
                else reconcile_mounts(primary, aliases)
            )
        else:
            if not args.catalog_root or not args.provider_root or not args.lock:
                parser.error(
                    f"{args.command} requires --catalog-root, --provider-root, and --lock"
                )
            root = _absolute(args.root)
            provider_roots = _provider_roots(args.provider_root, root)
            lock_path = args.lock if args.lock.is_absolute() else root / args.lock
            result = (
                publish_variant(
                    args.name, args.catalog_root, root, provider_roots, lock_path
                )
                if args.command == "publish-variant"
                else audit_variant(
                    args.name, args.catalog_root, root, provider_roots, lock_path
                )
            )
        print(json.dumps(result, indent=2, sort_keys=True))
    except (MountError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
