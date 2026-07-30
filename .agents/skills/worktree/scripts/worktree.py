#!/usr/bin/env python3
"""Prepare, inspect, and safely remove project-owned Git worktrees."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn, Sequence


class WorktreeError(RuntimeError):
    """A user-actionable worktree lifecycle failure."""


OWNERSHIP_FILENAME = "asher-skills-worktree.json"


@dataclass(frozen=True)
class Registration:
    path: Path
    head: str | None
    branch_ref: str | None
    bare: bool = False
    detached: bool = False
    prunable: bool = False

    @property
    def branch(self) -> str | None:
        prefix = "refs/heads/"
        if self.branch_ref and self.branch_ref.startswith(prefix):
            return self.branch_ref[len(prefix) :]
        return self.branch_ref


def run_git(
    repo: Path,
    *args: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        text=True,
        capture_output=True,
    )
    if check and result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise WorktreeError(detail)
    return result


def repository_root(repo: Path) -> Path:
    result = run_git(repo, "rev-parse", "--show-toplevel")
    supplied_checkout = Path(result.stdout.strip()).resolve()
    listing = run_git(supplied_checkout, "worktree", "list", "--porcelain", "-z")
    registered = parse_registrations(listing.stdout)
    if not registered or registered[0].bare:
        fail("the repository has no primary working checkout")
    return registered[0].path


def resolve_commit(repo: Path, ref: str) -> str:
    result = run_git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}")
    return result.stdout.strip()


def parse_registrations(raw: str) -> list[Registration]:
    records: list[Registration] = []
    fields: dict[str, str | bool] = {}

    def finish() -> None:
        nonlocal fields
        if not fields:
            return
        path = fields.get("worktree")
        if not isinstance(path, str):
            raise WorktreeError("git returned a worktree record with no path")
        records.append(
            Registration(
                path=Path(path).resolve(),
                head=fields.get("HEAD") if isinstance(fields.get("HEAD"), str) else None,
                branch_ref=fields.get("branch") if isinstance(fields.get("branch"), str) else None,
                bare=bool(fields.get("bare")),
                detached=bool(fields.get("detached")),
                prunable=bool(fields.get("prunable")),
            )
        )
        fields = {}

    separator = "\0" if "\0" in raw else "\n"
    for field in [*raw.split(separator), ""]:
        if not field:
            finish()
            continue
        key, value_separator, value = field.partition(" ")
        fields[key] = value if value_separator else True
    return records


def registrations(repo: Path) -> list[Registration]:
    result = run_git(repo, "worktree", "list", "--porcelain", "-z")
    return parse_registrations(result.stdout)


def registration_at(repo: Path, path: Path) -> Registration | None:
    resolved = path.resolve()
    return next((item for item in registrations(repo) if item.path == resolved), None)


def registration_for_branch(repo: Path, branch: str) -> Registration | None:
    return next((item for item in registrations(repo) if item.branch == branch), None)


def common_git_directory(repo: Path) -> Path:
    result = run_git(
        repo,
        "rev-parse",
        "--path-format=absolute",
        "--git-common-dir",
    )
    return Path(result.stdout.strip()).resolve()


def expected_git_directory(repo: Path, path: Path) -> Path | None:
    common = common_git_directory(repo)
    if path == repo:
        return common
    administrative_root = common / "worktrees"
    if not administrative_root.is_dir():
        return None
    matches: list[Path] = []
    for candidate in administrative_root.iterdir():
        if candidate.is_symlink() or not candidate.is_dir():
            continue
        backlink_file = candidate / "gitdir"
        try:
            backlink = Path(backlink_file.read_text().strip()).resolve()
        except OSError:
            continue
        if backlink.name == ".git" and backlink.parent == path:
            matches.append(candidate.resolve())
    return matches[0] if len(matches) == 1 else None


def ownership_path(repo: Path, path: Path) -> Path:
    administrative_directory = expected_git_directory(repo, path)
    if administrative_directory is None:
        fail(f"worktree has no unique administrative directory: {path}")
    return administrative_directory / OWNERSHIP_FILENAME


def write_ownership(
    repo: Path,
    path: Path,
    branch_ref: str,
    base_oid: str,
) -> None:
    destination = ownership_path(repo, path)
    if destination.exists() or destination.is_symlink():
        fail(f"worktree ownership record already exists: {destination}")
    payload = {
        "base_oid": base_oid,
        "branch_ref": branch_ref,
        "path": str(path),
        "repo": str(repo),
        "schema_version": 1,
    }
    temporary = destination.with_name(f".{OWNERSHIP_FILENAME}.{os.getpid()}.tmp")
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            json.dump(payload, handle, sort_keys=True)
            handle.write("\n")
        temporary.replace(destination)
    except OSError as error:
        fail(f"could not write worktree ownership record: {error}")
    finally:
        if temporary.exists():
            temporary.unlink()


def prepared_base(
    repo: Path,
    path: Path,
    branch_ref: str,
) -> str:
    source = ownership_path(repo, path)
    if source.is_symlink() or not source.is_file():
        fail(f"worktree has no valid project ownership record: {path}")
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"worktree ownership record is unreadable: {error}")
    expected_identity = {
        "branch_ref": branch_ref,
        "path": str(path),
        "repo": str(repo),
        "schema_version": 1,
    }
    if not isinstance(payload, dict) or any(
        payload.get(key) != value for key, value in expected_identity.items()
    ):
        fail(f"worktree ownership record does not match the requested identity: {path}")
    base_oid = payload.get("base_oid")
    if not isinstance(base_oid, str):
        fail(f"worktree ownership record has no prepared base: {path}")
    return base_oid


def worktree_directory_matches(
    repo: Path,
    path: Path,
    item: Registration,
) -> bool:
    if not path.is_dir() or item.prunable:
        return False
    expected_common = common_git_directory(repo)
    expected_git = expected_git_directory(repo, path)
    if expected_git is None:
        return False
    actual_common = run_git(
        path,
        "rev-parse",
        "--path-format=absolute",
        "--git-common-dir",
        check=False,
    )
    actual_git = run_git(
        path,
        "rev-parse",
        "--path-format=absolute",
        "--absolute-git-dir",
        check=False,
    )
    actual_top = run_git(path, "rev-parse", "--show-toplevel", check=False)
    actual_branch = run_git(path, "symbolic-ref", "--quiet", "HEAD", check=False)
    actual_head = run_git(path, "rev-parse", "--verify", "HEAD", check=False)
    if any(
        result.returncode
        for result in (actual_common, actual_git, actual_top, actual_head)
    ):
        return False
    identity_matches = (
        Path(actual_common.stdout.strip()).resolve()
        == expected_common
        and Path(actual_git.stdout.strip()).resolve() == expected_git
        and Path(actual_top.stdout.strip()).resolve() == path
        and actual_head.stdout.strip() == item.head
    )
    if not identity_matches:
        return False
    if item.detached:
        return actual_branch.returncode != 0
    return actual_branch.returncode == 0 and actual_branch.stdout.strip() == item.branch_ref


def dirty(path: Path) -> bool:
    if run_git(path, "status", "--porcelain", "--ignored").stdout:
        return True
    tagged_files = run_git(path, "ls-files", "-v").stdout.splitlines()
    return any(
        line[:1].islower() or line.startswith("S ")
        for line in tagged_files
    )


def emit(payload: dict[str, object]) -> None:
    print(json.dumps(payload, sort_keys=True))


def fail(message: str) -> NoReturn:
    raise WorktreeError(message)


def safe_leaf(branch: str) -> str:
    leaf = branch.replace("/", "-")
    if not leaf or leaf in {".", ".."}:
        fail(f"branch does not produce a safe worktree name: {branch!r}")
    return leaf


def has_symlink_component(path: Path) -> bool:
    absolute = path.absolute()
    return any(candidate.is_symlink() for candidate in (absolute, *absolute.parents))


def requested_path(repo: Path, branch: str, root: str | None, path: str | None) -> Path:
    if path:
        requested = Path(path).expanduser()
        if has_symlink_component(requested):
            fail(f"the requested path contains a symlink: {requested}")
        return requested.resolve()
    worktree_root = (
        Path(root).expanduser()
        if root
        else repo.parent / f"{repo.name}-worktrees"
    )
    if has_symlink_component(worktree_root):
        fail(f"the requested worktree root contains a symlink: {worktree_root}")
    candidate = worktree_root / safe_leaf(branch)
    if has_symlink_component(candidate):
        fail(f"the requested path contains a symlink: {candidate}")
    return candidate.resolve()


def prepare(args: argparse.Namespace) -> None:
    repo = repository_root(Path(args.repo).expanduser())
    path = requested_path(repo, args.branch, args.root, args.path)
    base_oid = resolve_commit(repo, args.base)
    branch_ref = f"refs/heads/{args.branch}"

    if path == repo or repo in path.parents:
        fail("the requested path is inside the primary checkout")

    registered = registrations(repo)
    containing_checkout = next(
        (item for item in registered if item.path in path.parents),
        None,
    )
    if containing_checkout:
        fail(
            f"the requested path is inside a registered checkout "
            f"at {containing_checkout.path}"
        )

    registered_path = next((item for item in registered if item.path == path), None)
    registered_branch = next(
        (item for item in registered if item.branch == args.branch),
        None,
    )
    if registered_path:
        if registered_path.prunable or not path.is_dir():
            fail(f"path has a prunable registration or missing working directory: {path}")
        if not worktree_directory_matches(repo, path, registered_path):
            fail(f"path does not match its registered worktree identity: {path}")
        if registered_path.branch_ref != branch_ref:
            fail(
                f"path is registered to {registered_path.branch or 'a detached worktree'}, "
                f"not {args.branch}: {path}"
            )
        owned_base = prepared_base(repo, path, branch_ref)
        if owned_base != base_oid:
            fail(
                f"requested base {args.base} ({base_oid}) does not match "
                f"the prepared base ({owned_base})"
            )
        emit(
            {
                "base": args.base,
                "base_oid": base_oid,
                "branch": args.branch,
                "head": registered_path.head,
                "path": str(path),
                "repo": str(repo),
                "reused": True,
            }
        )
        return

    if registered_branch:
        fail(f"branch is already registered at another worktree: {registered_branch.path}")
    if path.exists():
        fail(f"path exists but is not a registered worktree: {path}")
    if run_git(repo, "show-ref", "--verify", "--quiet", branch_ref, check=False).returncode == 0:
        fail(f"branch exists but is not registered to a worktree: {args.branch}")

    path.parent.mkdir(parents=True, exist_ok=True)
    run_git(repo, "worktree", "add", str(path), "-b", args.branch, base_oid)
    created = registration_at(repo, path)
    if not created or created.branch_ref != branch_ref:
        fail(f"git did not register the requested branch and path: {path}")
    if not worktree_directory_matches(repo, path, created):
        fail(
            f"git did not produce a valid working directory at the requested path; "
            f"branch and registration retained for recovery: {path}"
        )
    write_ownership(repo, path, branch_ref, base_oid)
    emit(
        {
            "base": args.base,
            "base_oid": base_oid,
            "branch": args.branch,
            "head": created.head,
            "path": str(path),
            "repo": str(repo),
            "reused": False,
        }
    )


def inspect(args: argparse.Namespace) -> None:
    repo = repository_root(Path(args.repo).expanduser())
    path = Path(args.path).expanduser().resolve()
    item = registration_at(repo, path)
    if not item:
        emit(
            {
                "branch": None,
                "dirty": None,
                "exists": path.exists(),
                "head": None,
                "path": str(path),
                "prunable": False,
                "registered": False,
                "repo": str(repo),
                "valid": False,
            }
        )
        return
    valid = worktree_directory_matches(repo, path, item)
    emit(
        {
            "branch": item.branch,
            "dirty": dirty(path) if valid else None,
            "exists": path.exists(),
            "head": item.head,
            "path": str(path),
            "prunable": item.prunable,
            "registered": True,
            "repo": str(repo),
            "valid": valid,
        }
    )


def remove(args: argparse.Namespace) -> None:
    repo = repository_root(Path(args.repo).expanduser())
    requested = Path(args.path).expanduser()
    if has_symlink_component(requested):
        fail(f"refusing to remove a worktree path containing a symlink: {requested}")
    path = requested.resolve()
    if path == repo or repo in path.parents:
        fail("refusing to remove a path inside the primary checkout")
    item = registration_at(repo, path)
    if not item:
        fail(f"path is not a registered worktree: {path}")
    if item.prunable or not path.is_dir():
        fail(f"path has a prunable registration or missing working directory: {path}")
    if not worktree_directory_matches(repo, path, item):
        fail(f"path does not match its registered worktree identity: {path}")
    if dirty(path):
        fail(f"worktree is dirty and will not be removed: {path}")

    run_git(repo, "worktree", "remove", str(path))
    if registration_at(repo, path):
        fail(f"git still reports the worktree after removal: {path}")
    emit(
        {
            "branch": item.branch,
            "path": str(path),
            "removed": True,
            "repo": str(repo),
        }
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Prepare, inspect, and safely remove project-owned Git worktrees."
    )
    commands = result.add_subparsers(dest="command", required=True)

    prepare_parser = commands.add_parser(
        "prepare",
        help="create or reuse an exactly matching worktree registration",
    )
    prepare_parser.add_argument("--repo", required=True, help="any path inside the repository")
    prepare_parser.add_argument("--branch", required=True, help="local work branch to create")
    prepare_parser.add_argument("--base", required=True, help="commit-ish to seed and validate")
    location = prepare_parser.add_mutually_exclusive_group()
    location.add_argument("--root", help="parent directory for the branch-named worktree")
    location.add_argument("--path", help="exact worktree path")
    prepare_parser.set_defaults(handler=prepare)

    inspect_parser = commands.add_parser(
        "inspect",
        help="report registration, branch, head, and dirty state",
    )
    inspect_parser.add_argument("--repo", required=True, help="any path inside the repository")
    inspect_parser.add_argument("--path", required=True, help="exact worktree path")
    inspect_parser.set_defaults(handler=inspect)

    remove_parser = commands.add_parser(
        "remove",
        help="remove one clean registered worktree without deleting its branch",
    )
    remove_parser.add_argument("--repo", required=True, help="any path inside the repository")
    remove_parser.add_argument("--path", required=True, help="exact worktree path")
    remove_parser.set_defaults(handler=remove)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        args.handler(args)
    except WorktreeError as error:
        print(f"worktree: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
