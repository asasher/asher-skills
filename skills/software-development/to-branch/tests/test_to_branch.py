"""Offline regression tests in disposable Git repositories."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/to-branch.py"


class ToBranchTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory()
        self.addCleanup(self.sandbox.cleanup)
        self.root = Path(self.sandbox.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.repo / "tracked").write_text("initial\n")
        self.git("add", ".")
        self.git("commit", "-m", "initial")
        self.original = self.git("rev-parse", "HEAD")
        (self.repo / "tracked").write_text("staged\n")
        self.git("add", "tracked")
        (self.repo / "tracked").write_text("unstaged\n")
        (self.repo / "artifact").write_text("published\n")

    def git(self, *args, cwd=None):
        return subprocess.check_output(
            ["git", *args], cwd=cwd or self.repo, stderr=subprocess.PIPE, text=True
        ).strip()

    def snapshot(self, directory):
        return (
            self.git("rev-parse", "HEAD", cwd=directory),
            self.git("status", "--porcelain", cwd=directory),
            self.git("diff", "--cached", cwd=directory),
            self.git("diff", cwd=directory),
            (directory / "tracked").read_bytes(),
            Path(self.git("rev-parse", "--path-format=absolute", "--git-path", "index", cwd=directory)).read_bytes(),
        )

    def publish(self, branch, env=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), branch, "artifact:doc", "-m", "publish"],
            cwd=self.repo, text=True, capture_output=True, timeout=10, env=env,
        )

    def test_rejects_current_branch_without_touching_worktree_or_index(self):
        before = self.snapshot(self.repo)
        result = self.publish("main")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("checked out", result.stderr)
        self.assertEqual(before, self.snapshot(self.repo))

    def test_rejects_branch_in_another_registered_worktree(self):
        other = self.root / "other\nworktree"
        self.git("worktree", "add", "-b", "artifact-branch", str(other))
        (other / "tracked").write_text("other staged\n")
        self.git("add", "tracked", cwd=other)
        (other / "tracked").write_text("other dirty\n")
        before = self.snapshot(self.repo), self.snapshot(other)
        result = self.publish("artifact-branch")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("checked out", result.stderr)
        self.assertEqual(before, (self.snapshot(self.repo), self.snapshot(other)))

    def test_publishes_new_and_existing_unchecked_branch_preserving_source(self):
        before = self.snapshot(self.repo)
        first = self.publish("artifacts")
        self.assertEqual(0, first.returncode, first.stderr)
        first_sha = first.stdout.strip()
        self.assertEqual(self.original, self.git("rev-parse", f"{first_sha}^"))
        self.assertEqual("published", self.git("show", "artifacts:doc"))
        (self.repo / "artifact").write_text("revision\n")
        second = self.publish("artifacts")
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual(first_sha, self.git("rev-parse", f"{second.stdout.strip()}^"))
        self.assertEqual(before, self.snapshot(self.repo))

    def test_rejects_symbolic_target_without_moving_checked_out_referent(self):
        self.git("symbolic-ref", "refs/heads/artifact-alias", "refs/heads/main")
        before = self.snapshot(self.repo)
        result = self.publish("artifact-alias")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("symbolic", result.stderr)
        self.assertEqual(before, self.snapshot(self.repo))

    def test_rechecks_symbolic_target_before_updating_ref(self):
        before = self.snapshot(self.repo)
        result = self.publish_with_symbolic_swap("commit-tree")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("symbolic", result.stderr)
        self.assertEqual(before, self.snapshot(self.repo))

    def test_final_symbolic_swap_cannot_redirect_update_to_main(self):
        before = self.snapshot(self.repo)
        result = self.publish_with_symbolic_swap("update-ref")
        self.assertEqual(before, self.snapshot(self.repo))
        if result.returncode == 0:
            self.assertEqual(result.stdout.strip(), self.git("rev-parse", "artifacts"))
            self.assertEqual(self.original, self.git("rev-parse", "artifacts^"))

    def publish_with_symbolic_swap(self, phase):
        self.git("branch", "artifacts")
        shim_dir = self.root / "bin"
        shim_dir.mkdir()
        shim = shim_dir / "git"
        real_git = shutil.which("git")
        shim.write_text(f'''#!{sys.executable}
import subprocess, sys
if sys.argv[1] == {phase!r}:
    subprocess.run([{real_git!r}, "symbolic-ref", "refs/heads/artifacts", "refs/heads/main"], check=True)
result = subprocess.run([{real_git!r}, *sys.argv[1:]])
raise SystemExit(result.returncode)
''')
        shim.chmod(0o755)
        return self.publish("artifacts", env=dict(os.environ, PATH=f"{shim_dir}{os.pathsep}{os.environ['PATH']}"))


if __name__ == "__main__":
    unittest.main()
