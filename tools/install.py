#!/usr/bin/env python3
"""Install this repo's skills into a target repo, or into this repo itself.

This repo installs its own skills. `npx skills add` cannot do it correctly — it
ignores `metadata.variants` (so `staffing` lands as uncompiled source with no
roster), skips directories named `build`, and never removes a skill dropped from
the set (asher-skills#103).

Mount layout, matching what consumers already carry:

    .agents/skills/<name>     primary mount — real directory
    .claude/skills/<name>     alias — symlink to the primary

A skill declaring `metadata.variants` is the exception: each provider gets its own
compiled tree as a real directory at its provider's mount.

State lives in one first-party file, `.agents/asher-skills/install.json`: the set
we installed, where each came from, and the source revision. It records no
integrity hashes. Drift is answered by `check`, which diffs each mount against the
source it was built from and names the files that differ — strictly more useful
than a hash mismatch, and with no stored quantity to keep in sync. `skills-lock.json`
belongs to a different installer; we read it once to migrate, strip our entries, and
never write it again.

Self-install (`--self`) mounts the same way — real copies, exactly what a consumer
gets. Mounts are decoupled from sources on purpose: a running session reads a
stable copy while sources change on branches, and a merged change reaches the
mounts only through a deliberate reconcile — re-running the install in the main
checkout (asher-skills#118).
"""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import catalog  # noqa: E402


PRIMARY = Path(".agents") / "skills"
ALIAS = Path(".claude") / "skills"
PROVIDER_MOUNT = {"codex": PRIMARY, "claude": ALIAS}
STATE = Path(".agents") / "asher-skills" / "install.json"
LEGACY_VARIANT_LOCK = Path(".agents") / "asher-skills" / "variant-lock.json"
FOREIGN_LOCK = Path("skills-lock.json")
DEFAULT_SOURCE = "github:asasher/asher-skills"


class InstallError(RuntimeError):
    pass


def _read_json(path: Path, default: dict) -> dict:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InstallError(f"{path}: invalid JSON") from exc


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _revision(root: Path) -> str | None:
    """Best-effort git revision of the source, for humans reading the state file."""
    try:
        done = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout.strip() or None if done.returncode == 0 else None


def _clear(path: Path) -> None:
    """Remove a mount whether it is a symlink, a directory, or absent."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _replace_dir(source: Path, destination: Path, *, skip: set[str]) -> None:
    """Copy `source` to `destination` atomically, omitting top-level `skip` names."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{destination.name}-", dir=destination.parent))
    try:
        for child in sorted(source.iterdir()):
            if child.name in skip:
                continue
            target = staging / child.name
            if child.is_dir():
                shutil.copytree(child, target, symlinks=False)
            else:
                shutil.copy2(child, target)
        _clear(destination)
        staging.replace(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def _link(destination: Path, target: Path) -> None:
    """Point `destination` at `target`, relative to the destination's parent."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    _clear(destination)
    destination.symlink_to(os.path.relpath(target, destination.parent))


def _mount_plain(skill: catalog.Skill, source_root: Path, target: Path) -> None:
    primary = target / PRIMARY / skill.name
    _replace_dir(source_root / skill.source, primary, skip={"variants"})
    _link(target / ALIAS / skill.name, primary)


def _mount_variant(skill: catalog.Skill, source_root: Path, target: Path) -> dict[str, str]:
    """Compile one tree per declared provider. Returns provider -> mount path."""
    providers: dict[str, str] = {}
    for provider, _ in skill.variants:
        mount = PROVIDER_MOUNT.get(provider)
        if mount is None:
            raise InstallError(f"{skill.name}: no mount defined for provider {provider}")
        output = target / mount / skill.name
        _clear(output)
        catalog.materialize_variant(skill, source_root, provider, output)
        providers[provider] = (mount / skill.name).as_posix()
    # A provider with no declared variant still needs a mount; alias it to the primary.
    for provider, mount in PROVIDER_MOUNT.items():
        if provider not in providers:
            _link(target / mount / skill.name, target / PRIMARY / skill.name)
    return providers


def _uninstall(name: str, target: Path) -> None:
    for mount in (PRIMARY, ALIAS):
        _clear(target / mount / name)


def _strip_foreign_lock(target: Path, names: set[str]) -> list[str]:
    """Remove our entries from the other installer's lockfile, once.

    `skills-lock.json` is npx-skills' private bookkeeping. Two installers writing
    one file is what produced the hash and ordering problems this replaces, so we
    take our entries out and leave the rest untouched — including key order.
    """
    path = target / FOREIGN_LOCK
    if not path.is_file():
        return []
    data = _read_json(path, {})
    entries = data.get("skills")
    if not isinstance(entries, dict):
        return []
    stripped = sorted(n for n in names if n in entries)
    if not stripped:
        return []
    for name in stripped:
        entries.pop(name)
    _write_json(path, data)
    return stripped


def _recorded(target: Path) -> tuple[dict, set[str]]:
    """Read our state, migrating from the pre-install.json layout when needed."""
    state = _read_json(target / STATE, {})
    if state.get("skills"):
        return state, set(state["skills"])

    # Migration: the set we own was recorded in the foreign lockfile.
    legacy = _read_json(target / FOREIGN_LOCK, {}).get("skills", {})
    owned = {
        name for name, entry in legacy.items()
        if "asher-skills" in str(entry.get("source", ""))
    }
    return state, owned


def install(
    source_root: Path,
    target: Path,
    selected: set[str],
    *,
    source_label: str | None = None,
    prune: bool = True,
) -> dict[str, object]:
    source_root = source_root.resolve()
    target = target.resolve()
    graph = catalog.discover(source_root)

    unknown = sorted(selected - set(graph))
    if unknown:
        raise InstallError(f"unknown skill(s): {', '.join(unknown)}")

    # Pull in required siblings so a mounted skill never dangles.
    closure = set(catalog.resolve(graph, selected, set())["closure"])
    _, previously = _recorded(target)
    removed = sorted(previously - closure) if prune else []

    skills: dict[str, dict] = {}
    compiled: list[str] = []
    for name in sorted(closure):
        skill = graph[name]
        record: dict[str, object] = {"source": skill.source}
        if skill.variants:
            record["providers"] = _mount_variant(skill, source_root, target)
            compiled.append(name)
        else:
            _mount_plain(skill, source_root, target)
        skills[name] = record

    for name in removed:
        _uninstall(name, target)

    _write_json(target / STATE, {
        "schema_version": 1,
        "source": source_label or DEFAULT_SOURCE,
        "source_revision": _revision(source_root),
        "skills": skills,
    })

    stripped = _strip_foreign_lock(target, set(closure) | set(removed))
    legacy_lock = target / LEGACY_VARIANT_LOCK
    if legacy_lock.is_file():
        legacy_lock.unlink()  # superseded by install.json

    return {
        "target": str(target),
        "installed": sorted(skills),
        "compiled": compiled,
        "removed": removed,
        "unlocked_from_foreign_lockfile": stripped,
    }


def _expected_tree(skill: catalog.Skill, source_root: Path, provider: str | None, into: Path) -> Path:
    """Materialize what a mount should contain, for comparison."""
    if provider is not None:
        output = into / f"{skill.name}-{provider}"
        catalog.materialize_variant(skill, source_root, provider, output)
        return output
    output = into / skill.name
    _replace_dir(source_root / skill.source, output, skip={"variants"})
    return output


def _diff_trees(expected: Path, actual: Path) -> list[str]:
    """Relative paths that differ between two trees."""
    differences: list[str] = []

    def walk(rel: Path) -> None:
        left, right = expected / rel, actual / rel
        comparison = filecmp.dircmp(left, right)
        for name in sorted(comparison.left_only):
            differences.append(f"missing: {(rel / name).as_posix()}")
        for name in sorted(comparison.right_only):
            differences.append(f"unexpected: {(rel / name).as_posix()}")
        for name in sorted(comparison.diff_files):
            differences.append(f"modified: {(rel / name).as_posix()}")
        for name in sorted(comparison.common_dirs):
            walk(rel / name)

    walk(Path())
    return differences


def check(source_root: Path, target: Path) -> dict[str, object]:
    """Diff every recorded mount against the source it was built from."""
    source_root, target = source_root.resolve(), target.resolve()
    state, names = _recorded(target)
    if not names:
        raise InstallError(f"{target / STATE}: nothing recorded; run install first")

    graph = catalog.discover(source_root)
    drift: dict[str, list[str]] = {}
    missing: list[str] = []

    with tempfile.TemporaryDirectory(prefix="skills-check-") as raw:
        scratch = Path(raw)
        for name in sorted(names):
            skill = graph.get(name)
            if skill is None:
                drift[name] = ["no longer exists in source"]
                continue
            mounts = (
                [(provider, target / path) for provider, path
                 in (state.get("skills", {}).get(name, {}).get("providers") or {}).items()]
                or [(None, target / PRIMARY / name)]
            )
            for provider, mount in mounts:
                if not mount.exists():
                    missing.append(str(mount))
                    continue
                found = _diff_trees(_expected_tree(skill, source_root, provider, scratch), mount)
                if found:
                    drift.setdefault(name, []).extend(found)

    return {
        "target": str(target),
        "checked": sorted(names),
        "missing_mounts": missing,
        "drift": drift,
        "clean": not drift and not missing,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("install", "check"))
    parser.add_argument("--skill", nargs="*", default=[], help="skills to install; default: the recorded set")
    parser.add_argument("--into", type=Path, help="target repo (default: current directory)")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument(
        "--self", dest="self_install", action="store_true",
        help="install this repo's own mounts from the local sources; --into must be the repo root",
    )
    parser.add_argument("--source-label", help="value recorded as `source` in install.json")
    parser.add_argument("--no-prune", action="store_true", help="keep skills dropped from the set")
    args = parser.parse_args(argv)

    target = (args.into or Path.cwd()).resolve()
    root = args.root.resolve()
    if args.self_install and target != root:
        parser.error("--self installs this repo into itself; --into must be the repo root")

    try:
        if args.command == "check":
            result = check(root, target)
            print(json.dumps(result, indent=2))
            return 0 if result["clean"] else 1

        selected = set(args.skill)
        if not selected:
            _, selected = _recorded(target)
            selected &= set(catalog.discover(root))
            if not selected:
                parser.error(
                    "nothing recorded for this target; name the set with --skill on a first install"
                )
        result = install(
            root, target, selected,
            source_label=args.source_label or ("self" if args.self_install else None),
            prune=not args.no_prune,
        )
    except (catalog.CatalogError, InstallError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
