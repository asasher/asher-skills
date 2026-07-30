#!/usr/bin/env python3
"""Behavior tests for the public worktree CLI."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "worktree.py"


def run(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*args],
        cwd=cwd,
        check=check,
        text=True,
        capture_output=True,
    )


class WorktreeCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sandbox = tempfile.TemporaryDirectory()
        self.root = Path(self.sandbox.name).resolve()
        self.repo = self.root / "project"
        self.repo.mkdir()
        run("git", "init", "-b", "main", cwd=self.repo)
        run("git", "config", "user.email", "probe@example.com", cwd=self.repo)
        run("git", "config", "user.name", "Probe", cwd=self.repo)
        (self.repo / "README.md").write_text("base\n")
        run("git", "add", "README.md", cwd=self.repo)
        run("git", "commit", "-m", "base", cwd=self.repo)
        (self.repo / "primary-only.txt").write_text("leave me alone\n")
        self.worktree_root = self.root / "project-worktrees"

    def tearDown(self) -> None:
        self.sandbox.cleanup()

    def cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return run(
            "python3",
            str(SCRIPT),
            *args,
            check=check,
        )

    def prepare(self, branch: str = "136-worktree") -> dict[str, object]:
        result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            branch,
            "--base",
            "main",
            "--root",
            str(self.worktree_root),
        )
        return json.loads(result.stdout)

    def test_prepare_creates_registered_worktree_without_touching_primary_checkout(self) -> None:
        before_branch = run("git", "branch", "--show-current", cwd=self.repo).stdout.strip()
        before_status = run("git", "status", "--porcelain", cwd=self.repo).stdout

        payload = self.prepare()

        worktree_path = Path(str(payload["path"]))
        self.assertFalse(payload["reused"])
        self.assertEqual("136-worktree", payload["branch"])
        self.assertEqual(worktree_path, (self.worktree_root / "136-worktree").resolve())
        self.assertTrue(worktree_path.is_dir())
        self.assertIn(str(worktree_path), run("git", "worktree", "list", "--porcelain", cwd=self.repo).stdout)
        self.assertEqual(before_branch, run("git", "branch", "--show-current", cwd=self.repo).stdout.strip())
        self.assertEqual(before_status, run("git", "status", "--porcelain", cwd=self.repo).stdout)

    def test_prepare_reuses_only_the_matching_registration(self) -> None:
        first = self.prepare()
        second = self.prepare()

        self.assertFalse(first["reused"])
        self.assertTrue(second["reused"])
        self.assertEqual(first["path"], second["path"])
        self.assertEqual(first["base_oid"], second["base_oid"])

    def test_prepare_refuses_reuse_with_a_different_ancestor_base(self) -> None:
        older_base = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
        (self.repo / "new-base.txt").write_text("new base\n")
        run("git", "add", "new-base.txt", cwd=self.repo)
        run("git", "commit", "-m", "advance base", cwd=self.repo)
        prepared = self.prepare()

        result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "136-worktree",
            "--base",
            older_base,
            "--path",
            str(prepared["path"]),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("base", result.stderr.lower())

    def test_prepare_refuses_a_prunable_registration_with_missing_directory(self) -> None:
        first = self.prepare()
        worktree_path = Path(str(first["path"]))
        shutil.rmtree(worktree_path)

        result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "136-worktree",
            "--base",
            "main",
            "--root",
            str(self.worktree_root),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("prunable", result.stderr.lower())

        inspected = self.cli(
            "inspect",
            "--repo",
            str(self.repo),
            "--path",
            str(worktree_path),
        )
        payload = json.loads(inspected.stdout)
        self.assertTrue(payload["registered"])
        self.assertTrue(payload["prunable"])
        self.assertFalse(payload["exists"])
        self.assertFalse(payload["valid"])
        self.assertIsNone(payload["dirty"])

    def test_prepare_refuses_an_ordinary_directory_at_a_registered_path(self) -> None:
        first = self.prepare()
        worktree_path = Path(str(first["path"]))
        shutil.rmtree(worktree_path)
        worktree_path.mkdir()

        result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "136-worktree",
            "--base",
            "main",
            "--root",
            str(self.worktree_root),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertTrue(
            "prunable" in result.stderr.lower()
            or "does not match" in result.stderr.lower()
        )

    def test_prepare_refuses_a_symlinked_worktree_root(self) -> None:
        actual_root = self.root / "redirected-root"
        actual_root.mkdir()
        alias_root = self.root / "alias-root"
        alias_root.symlink_to(actual_root, target_is_directory=True)

        result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "redirected",
            "--base",
            "main",
            "--root",
            str(alias_root),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("symlink", result.stderr.lower())
        self.assertFalse((actual_root / "redirected").exists())

    def test_prepare_verifies_directory_identity_after_checkout_hooks(self) -> None:
        hooks = self.root / "hooks"
        hooks.mkdir()
        post_checkout = hooks / "post-checkout"
        post_checkout.write_text(
            "#!/bin/sh\n"
            "find . -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +\n"
        )
        post_checkout.chmod(0o755)
        run("git", "config", "core.hooksPath", str(hooks), cwd=self.repo)

        result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "hook-replaced",
            "--base",
            "main",
            "--root",
            str(self.worktree_root),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("valid working directory", result.stderr.lower())
        self.assertIn("retained for recovery", result.stderr.lower())
        self.assertIn(
            "hook-replaced",
            run("git", "branch", "--list", "hook-replaced", cwd=self.repo).stdout,
        )
        self.assertIn(
            str(self.worktree_root / "hook-replaced"),
            run("git", "worktree", "list", "--porcelain", cwd=self.repo).stdout,
        )

    def test_prepare_refuses_symlinks_in_root_and_path_ancestors(self) -> None:
        redirected = self.root / "redirected-parent"
        redirected.mkdir()
        ancestor = self.root / "linked-parent"
        ancestor.symlink_to(redirected, target_is_directory=True)

        root_result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "root-ancestor",
            "--base",
            "main",
            "--root",
            str(ancestor / "nested-root"),
            check=False,
        )
        path_result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "path-ancestor",
            "--base",
            "main",
            "--path",
            str(ancestor / "explicit-worktree"),
            check=False,
        )

        self.assertNotEqual(0, root_result.returncode)
        self.assertIn("symlink", root_result.stderr.lower())
        self.assertNotEqual(0, path_result.returncode)
        self.assertIn("symlink", path_result.stderr.lower())

    def test_prepare_refuses_a_path_registered_to_another_branch(self) -> None:
        self.prepare("first-branch")

        result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "second-branch",
            "--base",
            "main",
            "--path",
            str(self.worktree_root / "first-branch"),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("registered", result.stderr.lower())
        self.assertEqual("", run("git", "branch", "--list", "second-branch", cwd=self.repo).stdout)

    def test_prepare_refuses_a_path_inside_the_primary_checkout(self) -> None:
        before_status = run("git", "status", "--porcelain", cwd=self.repo).stdout

        result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "nested-branch",
            "--base",
            "main",
            "--path",
            str(self.repo / "nested-worktree"),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("primary checkout", result.stderr.lower())
        self.assertFalse((self.repo / "nested-worktree").exists())
        self.assertEqual(before_status, run("git", "status", "--porcelain", cwd=self.repo).stdout)

    def test_inspect_reports_registration_branch_and_dirty_state(self) -> None:
        prepared = self.prepare()
        worktree_path = Path(str(prepared["path"]))
        (worktree_path / "change.txt").write_text("dirty\n")

        result = self.cli(
            "inspect",
            "--repo",
            str(self.repo),
            "--path",
            str(worktree_path),
        )
        payload = json.loads(result.stdout)

        self.assertTrue(payload["registered"])
        self.assertEqual("136-worktree", payload["branch"])
        self.assertTrue(payload["dirty"])

    def test_inspect_accepts_a_valid_detached_registration(self) -> None:
        detached = self.worktree_root / "detached"
        run("git", "worktree", "add", "--detach", str(detached), "main", cwd=self.repo)

        result = self.cli(
            "inspect",
            "--repo",
            str(self.repo),
            "--path",
            str(detached),
        )
        payload = json.loads(result.stdout)

        self.assertTrue(payload["registered"])
        self.assertTrue(payload["valid"])
        self.assertIsNone(payload["branch"])
        self.assertFalse(payload["dirty"])

    def test_nul_safe_listing_handles_a_non_ascii_worktree_path(self) -> None:
        unusual_path = self.worktree_root / "wørk tree"

        prepared = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "unicode-path",
            "--base",
            "main",
            "--path",
            str(unusual_path),
        )
        payload = json.loads(prepared.stdout)

        self.assertEqual(str(unusual_path.resolve()), payload["path"])
        self.assertTrue(unusual_path.is_dir())

    def test_remove_refuses_dirty_worktree_and_removes_clean_worktree_only(self) -> None:
        prepared = self.prepare()
        worktree_path = Path(str(prepared["path"]))
        dirty_file = worktree_path / "change.txt"
        dirty_file.write_text("dirty\n")

        refused = self.cli(
            "remove",
            "--repo",
            str(self.repo),
            "--path",
            str(worktree_path),
            check=False,
        )
        self.assertNotEqual(0, refused.returncode)
        self.assertIn("dirty", refused.stderr.lower())
        self.assertTrue(worktree_path.exists())

        dirty_file.unlink()
        removed = self.cli(
            "remove",
            "--repo",
            str(self.repo),
            "--path",
            str(worktree_path),
        )
        payload = json.loads(removed.stdout)

        self.assertTrue(payload["removed"])
        self.assertFalse(worktree_path.exists())
        self.assertNotIn(str(worktree_path), run("git", "worktree", "list", "--porcelain", cwd=self.repo).stdout)
        self.assertIn("136-worktree", run("git", "branch", "--list", "136-worktree", cwd=self.repo).stdout)

    def test_remove_preserves_ignored_files(self) -> None:
        (self.repo / ".gitignore").write_text(".env\n")
        run("git", "add", ".gitignore", cwd=self.repo)
        run("git", "commit", "-m", "ignore local env", cwd=self.repo)
        prepared = self.prepare()
        worktree_path = Path(str(prepared["path"]))
        ignored_secret = worktree_path / ".env"
        ignored_secret.write_text("do not delete\n")

        result = self.cli(
            "remove",
            "--repo",
            str(self.repo),
            "--path",
            str(worktree_path),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertTrue(ignored_secret.exists())

    def test_remove_refuses_assume_unchanged_index_entries(self) -> None:
        prepared = self.prepare()
        worktree_path = Path(str(prepared["path"]))
        run("git", "update-index", "--assume-unchanged", "README.md", cwd=worktree_path)
        (worktree_path / "README.md").write_text("hidden local change\n")

        result = self.cli(
            "remove",
            "--repo",
            str(self.repo),
            "--path",
            str(worktree_path),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("dirty", result.stderr.lower())
        self.assertTrue(worktree_path.exists())

    def test_remove_refuses_skip_worktree_index_entries(self) -> None:
        prepared = self.prepare()
        worktree_path = Path(str(prepared["path"]))
        run("git", "update-index", "--skip-worktree", "README.md", cwd=worktree_path)
        (worktree_path / "README.md").write_text("hidden sparse change\n")

        result = self.cli(
            "remove",
            "--repo",
            str(self.repo),
            "--path",
            str(worktree_path),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("dirty", result.stderr.lower())
        self.assertTrue(worktree_path.exists())

    def test_remove_refuses_a_registered_path_inside_the_primary_checkout(self) -> None:
        nested = self.repo / "legacy-nested-worktree"
        run("git", "worktree", "add", str(nested), "-b", "legacy-nested", "main", cwd=self.repo)

        result = self.cli(
            "remove",
            "--repo",
            str(self.repo),
            "--path",
            str(nested),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("primary checkout", result.stderr.lower())
        self.assertTrue(nested.exists())

    def test_remove_refuses_a_symlink_to_a_registered_worktree(self) -> None:
        prepared = self.prepare()
        worktree_path = Path(str(prepared["path"]))
        alias = self.root / "worktree-alias"
        alias.symlink_to(worktree_path, target_is_directory=True)

        prepare_result = self.cli(
            "prepare",
            "--repo",
            str(self.repo),
            "--branch",
            "136-worktree",
            "--base",
            "main",
            "--path",
            str(alias),
            check=False,
        )
        result = self.cli(
            "remove",
            "--repo",
            str(self.repo),
            "--path",
            str(alias),
            check=False,
        )

        self.assertNotEqual(0, prepare_result.returncode)
        self.assertIn("symlink", prepare_result.stderr.lower())
        self.assertNotEqual(0, result.returncode)
        self.assertIn("symlink", result.stderr.lower())
        self.assertTrue(worktree_path.exists())

    def test_remove_refuses_a_replaced_registered_directory(self) -> None:
        prepared = self.prepare()
        worktree_path = Path(str(prepared["path"]))
        shutil.rmtree(worktree_path)
        worktree_path.mkdir()

        result = self.cli(
            "remove",
            "--repo",
            str(self.repo),
            "--path",
            str(worktree_path),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertTrue(
            "prunable" in result.stderr.lower()
            or "does not match" in result.stderr.lower()
        )
        self.assertTrue(worktree_path.exists())

    def test_identity_rejects_another_linked_checkout_moved_over_the_path(self) -> None:
        prepared = self.prepare()
        worktree_path = Path(str(prepared["path"]))
        substitute = self.worktree_root / "substitute"
        run(
            "git",
            "worktree",
            "add",
            "--force",
            str(substitute),
            "136-worktree",
            cwd=self.repo,
        )
        shutil.rmtree(worktree_path)
        shutil.move(str(substitute), str(worktree_path))

        inspected = self.cli(
            "inspect",
            "--repo",
            str(self.repo),
            "--path",
            str(worktree_path),
        )
        payload = json.loads(inspected.stdout)
        removed = self.cli(
            "remove",
            "--repo",
            str(self.repo),
            "--path",
            str(worktree_path),
            check=False,
        )

        self.assertTrue(payload["registered"])
        self.assertFalse(payload["valid"])
        self.assertNotEqual(0, removed.returncode)
        self.assertIn("does not match", removed.stderr.lower())
        self.assertTrue(worktree_path.exists())

    def test_remove_refuses_a_symlink_in_a_path_ancestor(self) -> None:
        prepared = self.prepare()
        worktree_path = Path(str(prepared["path"]))
        alias_root = self.root / "alias-worktree-root"
        alias_root.symlink_to(self.worktree_root, target_is_directory=True)

        result = self.cli(
            "remove",
            "--repo",
            str(self.repo),
            "--path",
            str(alias_root / worktree_path.name),
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("symlink", result.stderr.lower())
        self.assertTrue(worktree_path.exists())

    def test_secondary_repo_argument_still_protects_the_true_primary_checkout(self) -> None:
        secondary_payload = self.prepare("secondary")
        secondary = Path(str(secondary_payload["path"]))
        nested_primary_path = self.repo / "nested-from-secondary"

        prepare_result = self.cli(
            "prepare",
            "--repo",
            str(secondary),
            "--branch",
            "nested-from-secondary",
            "--base",
            "main",
            "--path",
            str(nested_primary_path),
            check=False,
        )
        remove_result = self.cli(
            "remove",
            "--repo",
            str(secondary),
            "--path",
            str(self.repo),
            check=False,
        )

        self.assertNotEqual(0, prepare_result.returncode)
        self.assertIn("primary checkout", prepare_result.stderr.lower())
        self.assertFalse(nested_primary_path.exists())
        self.assertNotEqual(0, remove_result.returncode)
        self.assertIn("primary checkout", remove_result.stderr.lower())
        self.assertTrue(self.repo.exists())


if __name__ == "__main__":
    unittest.main()
