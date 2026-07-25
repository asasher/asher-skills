#!/usr/bin/env python3
"""Install this repo's skills into a target repo, or into this repo itself.

Replaces `npx skills add` for Asher-authored skills. That CLI cannot install this
repo correctly: it ignores `metadata.variants` (so `staffing` lands as uncompiled
source with no roster), skips directories named `build`, and never removes a skill
dropped from the set. See asher-skills#103.

Mount layout, matching what consumers already carry:

    .agents/skills/<name>     primary mount — real directory
    .claude/skills/<name>     alias — symlink to the primary

A skill declaring `metadata.variants` is the exception: each provider gets its own
compiled tree as a real directory at its provider's mount, and the pair is recorded
in `.agents/asher-skills/variant-lock.json`.

Self-install (`--self`) mounts by symlink into `skills/<category>/<name>` instead of
copying, so this repo's mounts are live and can never go stale. Variant skills are
still compiled, because a compiled tree has no on-disk source to point at.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import catalog  # noqa: E402


PRIMARY = Path(".agents") / "skills"
ALIAS = Path(".claude") / "skills"
PROVIDER_MOUNT = {"codex": PRIMARY, "claude": ALIAS}
VARIANT_LOCK = Path(".agents") / "asher-skills" / "variant-lock.json"
SKILLS_LOCK = Path("skills-lock.json")


class InstallError(RuntimeError):
    pass


def _read_json(path: Path, default: dict) -> dict:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InstallError(f"{path}: invalid JSON") from exc


def _write_json(path: Path, data: dict, *, sort_keys: bool = False) -> None:
    """Write JSON preserving key order by default.

    `skills-lock.json` is only partly ours — third-party entries live there too —
    so sorting keys would rewrite every foreign entry's field order for no value
    change. Order is preserved and callers decide what to touch.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=sort_keys) + "\n", encoding="utf-8")


SKIPPED_DIRS = {".git", "node_modules"}


def installed_hash(mount: Path) -> str:
    """Hash an installed mount the way the vendor CLI's `computeSkillFolderHash` does.

    sha256 over every regular file in the folder, sorted by forward-slashed relative
    path, updating with the path then the bytes; bare hex, no prefix. Matching the
    vendor keeps `skills-lock.json` verifiable by existing checkers.

    This hashes what is actually on disk, so it detects a hand-edited mount — which
    a hash of the *source* tree cannot. The vendor writes this quantity for some
    skills and a download-manifest snapshot for others; the snapshot is not derivable
    from the folder, so entries carrying one have never been verifiable. Writing this
    for every skill we install makes them all verifiable.
    """
    files: list[tuple[str, bytes]] = []

    def walk(directory: Path) -> None:
        for entry in sorted(directory.iterdir()):
            if entry.is_symlink():
                continue  # Node's Dirent.isFile() is false for symlinks
            if entry.is_dir():
                if entry.name not in SKIPPED_DIRS:
                    walk(entry)
            elif entry.is_file():
                files.append((entry.relative_to(mount).as_posix(), entry.read_bytes()))

    walk(mount)
    files.sort(key=lambda item: item[0])
    digest = hashlib.sha256()
    for relative, data in files:
        digest.update(relative.encode("utf-8"))
        digest.update(data)
    return digest.hexdigest()


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


def _mount_plain(skill: catalog.Skill, source_root: Path, target: Path, *, live: bool) -> None:
    primary = target / PRIMARY / skill.name
    if live:
        _link(primary, source_root / skill.source)
    else:
        _replace_dir(source_root / skill.source, primary, skip={"variants"})
    _link(target / ALIAS / skill.name, primary)


def _mount_variant(skill: catalog.Skill, source_root: Path, target: Path) -> dict[str, dict[str, str]]:
    """Compile one provider tree per declared variant. Returns the lock providers block."""
    providers: dict[str, dict[str, str]] = {}
    source_revision = ""
    for provider, _ in skill.variants:
        mount = PROVIDER_MOUNT.get(provider)
        if mount is None:
            raise InstallError(f"{skill.name}: no mount defined for provider {provider}")
        output = target / mount / skill.name
        _clear(output)
        result = catalog.materialize_variant(skill, source_root, provider, output)
        source_revision = result["source_revision"]
        providers[provider] = {
            "effective_hash": result["effective_hash"],
            "mount": (mount / skill.name).as_posix(),
            "provider": provider,
        }
    # A provider with no declared variant still needs a mount; alias it to the primary.
    for provider, mount in PROVIDER_MOUNT.items():
        if provider not in providers:
            _link(target / mount / skill.name, target / PRIMARY / skill.name)
    return {"providers": providers, "source_revision": source_revision}


def _uninstall(name: str, target: Path) -> None:
    for mount in (PRIMARY, ALIAS):
        _clear(target / mount / name)


def install(
    source_root: Path,
    target: Path,
    selected: set[str],
    *,
    live: bool = False,
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

    skills_lock = _read_json(target / SKILLS_LOCK, {"version": 1, "skills": {}})
    entries: dict[str, dict] = skills_lock.setdefault("skills", {})
    label = source_label or "asasher/asher-skills"

    # Only ever prune skills this source owns; third-party mounts are untouchable.
    ours = {n for n, e in entries.items() if str(e.get("source", "")) == label}
    removed = sorted(ours - closure) if prune else []

    variant_lock = _read_json(target / VARIANT_LOCK, {"schema_version": 1, "skills": {}})
    variants: dict[str, dict] = variant_lock.setdefault("skills", {})

    installed: list[str] = []
    compiled: list[str] = []
    for name in sorted(closure):
        skill = graph[name]
        if skill.variants:
            block = _mount_variant(skill, source_root, target)
            variants[name] = {
                "providers": block["providers"],
                "source": skill.source,
                "source_revision": block["source_revision"],
            }
            compiled.append(name)
        else:
            _mount_plain(skill, source_root, target, live=live)
            variants.pop(name, None)
        entries[name] = {
            "source": label,
            "sourceType": "local" if live else "github",
            "skillPath": f"{skill.source}/SKILL.md",
            "computedHash": installed_hash(target / PRIMARY / name),
        }
        installed.append(name)

    for name in removed:
        _uninstall(name, target)
        entries.pop(name, None)
        variants.pop(name, None)

    skills_lock["skills"] = {name: entries[name] for name in sorted(entries)}
    _write_json(target / SKILLS_LOCK, skills_lock)
    if variants:
        _write_json(target / VARIANT_LOCK, variant_lock, sort_keys=True)

    return {
        "target": str(target),
        "installed": installed,
        "compiled": compiled,
        "removed": removed,
        "mode": "live" if live else "copy",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("install",))
    parser.add_argument("--skill", nargs="*", default=[], help="skills to install; default all public")
    parser.add_argument("--into", type=Path, help="target repo (default: current directory)")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument(
        "--self", dest="self_install", action="store_true",
        help="mount by symlink into skills/<category>/<name>; for this repo only",
    )
    parser.add_argument("--source-label", help="value written to skills-lock.json `source`")
    parser.add_argument("--no-prune", action="store_true", help="keep skills dropped from the set")
    args = parser.parse_args(argv)

    target = (args.into or Path.cwd()).resolve()
    root = args.root.resolve()
    if args.self_install and target != root:
        parser.error("--self installs this repo into itself; --into must be the repo root")

    try:
        graph = catalog.discover(root)
        selected = set(args.skill)
        if not selected:
            # Default to refreshing the set already recorded, so a bare `install`
            # never silently widens a curated selection. Only a first install has
            # to name its skills.
            label = args.source_label or (str(root) if args.self_install else "asasher/asher-skills")
            entries = _read_json(target / SKILLS_LOCK, {}).get("skills", {})
            selected = {n for n, e in entries.items() if str(e.get("source", "")) == label}
            selected &= set(graph)
            if not selected:
                parser.error(
                    "no skills recorded for this source in skills-lock.json; "
                    "name the set explicitly with --skill on a first install"
                )
        result = install(
            root, target, selected,
            live=args.self_install,
            source_label=args.source_label or (str(root) if args.self_install else None),
        )
    except (catalog.CatalogError, InstallError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
