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

An install ends with a `setup_report`: which installed skills' sources changed
since the recorded revision, and which of those declare a setup, ordered by the
catalog's own resolution. Setups bring repo-owned playbooks into line and sometimes
ask the user, so they are agent-run — this reports them and invokes nothing. A source
tree with no git history to compare against reports every installed skill as
changed, since an unanswerable comparison must not read as nothing-to-do.

Self-install (`--self`) mounts the same way — real copies, exactly what a consumer
gets. Mounts are decoupled from sources on purpose: a running session reads a
stable copy while sources change on branches, and a merged change reaches the
mounts only through a deliberate reconcile — re-running the install in the main
checkout. That reconcile is the moment the report speaks to: it names which of the
freshly copied skills need their setup re-run.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import re
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
OBJECT_NAME = re.compile(r"[0-9a-fA-F]{7,40}")


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
    """Best-effort git revision of the source; the baseline the next install diffs against."""
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


def _git_lines(root: Path, args: list[str]) -> list[str] | None:
    """Run a git command in `root` and split its output. None if it could not run.

    `core.quotePath=false` because the default wraps any non-ASCII path in quotes
    and octal-escapes it, which matches no skill's source prefix — the skill would
    drop out of the report silently, in the unsafe direction.
    """
    try:
        done = subprocess.run(
            ["git", "-C", str(root), "-c", "core.quotePath=false", *args],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0:
        return None
    return [line for line in done.stdout.splitlines() if line]


def _changed_sources(root: Path, since: object) -> list[str] | None:
    """Source-relative paths that differ between `since` and the source working tree.

    The comparison runs against the working tree rather than a second revision, and
    counts files git does not track yet, so a source edited or extended in place is
    changed — a skill that gains a `reference/setup.md` is exactly the case this has
    to catch. None means the question could not be answered here: no git, a revision
    this clone lacks, or a recorded revision that is not an object name.

    `since` arrives from a checked-in state file, so it is never trusted as a git
    argument: anything but an object name is refused, and `--end-of-options` keeps
    even that from being read as a flag. Handed a bare `--output=<path>`, git would
    truncate that path and exit 0 with empty output — a destructive write reported
    as nothing-to-do.
    """
    if not isinstance(since, str) or not OBJECT_NAME.fullmatch(since):
        return None
    changed = _git_lines(
        root, ["diff", "--name-only", "--relative", "--end-of-options", since, "--"]
    )
    if changed is None:
        return None
    untracked = _git_lines(root, ["ls-files", "--others", "--exclude-standard"])
    if untracked is None:
        return None  # Half an answer would under-report; fall back to the whole closure.
    return sorted(set(changed) | set(untracked))


def _skills_touched(
    graph: dict[str, catalog.Skill], closure: set[str], paths: list[str]
) -> set[str]:
    """The installed skills owning any of `paths`."""
    return {
        name for name in closure
        if any(
            path == graph[name].source or path.startswith(graph[name].source + "/")
            for path in paths
        )
    }


def _recorded_dirty(value: object) -> list[str] | None:
    """The last install's uncommitted-source record, or None if it cannot be read.

    A list holding anything but skill names is no more answerable than no list at
    all: dropping the members it cannot read would report a real comparison over a
    set that quietly lost entries.
    """
    if isinstance(value, list) and all(isinstance(name, str) for name in value):
        return value
    return None


def _setup_report(
    graph: dict[str, catalog.Skill],
    closure: set[str],
    setup_order: list[str],
    previously: set[str],
    changed_paths: list[str] | None,
    since: object,
    previously_dirty: object,
) -> dict[str, object]:
    """Say which installed skills changed, and which setups that implies.

    `setup_order` is exactly the changed skills that declare a setup, listed in the
    catalog's own resolution order — the subset and the run order in one field.

    `changed_paths` is what the source diff reported, or None when no diff was
    possible. Undeterminable is treated as everything-changed: "we cannot tell"
    must not read as "nothing to do".

    `previously_dirty` is the skills the last install recorded as uncommitted. They
    were installed at content no revision describes, so the working tree matching
    the recorded revision does not mean their mounts are unchanged — reverting the
    uncommitted work changed them. State that cannot answer this — anything
    `_recorded_dirty` refuses, including state written before it was recorded —
    makes the whole comparison unanswerable rather than silently half-true.
    """
    dirty = _recorded_dirty(previously_dirty)
    if not previously:
        basis = "first-install"
        changed = set(closure)
    elif changed_paths is None or dirty is None:
        basis = "unknown-revision"
        changed = set(closure)
    else:
        basis = "revision-diff"
        changed = _skills_touched(graph, closure, changed_paths)
        # A skill mounted here for the first time has never had its setup run.
        changed |= closure - previously
        changed |= set(dirty) & closure

    return {
        "basis": basis,
        "since_revision": since,
        "changed": sorted(changed),
        "setup_order": [name for name in setup_order if name in changed and graph[name].setup],
    }


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
    resolution = catalog.resolve(graph, selected, set())
    closure = set(resolution["closure"])
    recorded, previously = _recorded(target)
    removed = sorted(previously - closure) if prune else []

    # Read against the revision we are about to overwrite. The recorded value is
    # reported as it was found — absent and unusable are different states, and
    # `_changed_sources` refuses anything that is not an object name anyway.
    since = recorded.get("source_revision")
    changed_paths = _changed_sources(source_root, since)
    report = _setup_report(
        graph, closure, resolution["setup_order"], previously, changed_paths, since,
        recorded.get("source_dirty"),
    )

    # The mounts come from the working tree, but the revision recorded below is
    # HEAD. Note which sources that revision does not describe, so the next install
    # can still tell that reverting the uncommitted work changed their mounts.
    revision = _revision(source_root)
    uncommitted = _changed_sources(source_root, revision)
    dirty = (
        sorted(_skills_touched(graph, closure, uncommitted))
        if uncommitted is not None else None
    )

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
        "source_revision": revision,
        "source_dirty": dirty,
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
        "setup_report": report,
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


def _summarize(report: dict[str, object]) -> list[str]:
    """The same report as two lines a human can act on."""
    changed = report["changed"]
    setups = report["setup_order"]
    since = report["since_revision"]
    short = since[:7] if isinstance(since, str) and OBJECT_NAME.fullmatch(since) else None

    sources = "1 skill source" if len(changed) == 1 else f"{len(changed)} skill sources"

    if report["basis"] == "first-install":
        first = f"first install: treating {sources} as changed"
    elif report["basis"] == "unknown-revision":
        if short:
            reason = f"cannot compare against recorded revision {short}"
        elif since is not None:
            reason = "recorded source revision is not a usable object name"
        else:
            reason = "no source revision to compare against"
        first = f"{reason}; treating {sources} as changed"
    else:
        against = f" since {short}" if short else ""
        first = (
            f"{sources} changed{against}: " + ", ".join(changed) if changed
            else f"no skill sources changed{against}"
        )

    second = (
        "setups to re-run, in order: " + ", ".join(setups) if setups
        else "no setups to re-run"
    )
    return [first, second]


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
    for line in _summarize(result["setup_report"]):
        print(line, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
