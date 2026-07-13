#!/usr/bin/env python3
"""Filesystem tests for installed-skill mount reconciliation."""

from __future__ import annotations

import importlib.util
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts/install.py"
SPEC = importlib.util.spec_from_file_location("skill_install", SCRIPT)
assert SPEC and SPEC.loader
install = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = install
SPEC.loader.exec_module(install)


class InstallTests(unittest.TestCase):
    def fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        primary = root / ".agents/skills/example"
        return temp, root, primary

    def test_script_is_executable(self) -> None:
        self.assertTrue(SCRIPT.stat().st_mode & stat.S_IXUSR)

    def test_inspect_classifies_primary_and_alias_states(self) -> None:
        temp, root, primary = self.fixture()
        self.addCleanup(temp.cleanup)
        alias = root / ".claude/skills/example"
        missing = install.inspect_mounts(primary, [alias])
        self.assertEqual(missing["primary"]["state"], "missing")
        self.assertEqual(missing["aliases"][0]["state"], "missing")

        primary.mkdir(parents=True)
        alias.parent.mkdir(parents=True)
        alias.symlink_to(Path("../../.agents/skills/example"))
        mounted = install.inspect_mounts(primary, [alias])
        self.assertEqual(mounted["primary"]["state"], "real-directory")
        self.assertEqual(mounted["aliases"][0]["state"], "correct-symlink")

    def test_reconcile_creates_missing_and_fixes_dangling_and_wrong_aliases(self) -> None:
        temp, root, primary = self.fixture()
        self.addCleanup(temp.cleanup)
        primary.mkdir(parents=True)
        missing = root / ".claude/skills/example"
        dangling = root / ".cursor/skills/example"
        wrong = root / ".other/skills/example"
        dangling.parent.mkdir(parents=True)
        wrong.parent.mkdir(parents=True)
        dangling.symlink_to("missing-target")
        wrong_target = root / "wrong-target"
        wrong_target.mkdir()
        wrong.symlink_to(wrong_target)

        result = install.reconcile_mounts(primary, [missing, dangling, wrong])

        self.assertEqual([alias["state"] for alias in result["aliases"]], ["correct-symlink"] * 3)
        self.assertEqual([action["action"] for action in result["actions"]], ["created", "fixed", "fixed"])
        for alias in (missing, dangling, wrong):
            target = alias.parent / os.readlink(alias)
            self.assertEqual(Path(os.path.abspath(target)), primary)

    def test_refuses_primary_symlink_without_touching_aliases(self) -> None:
        temp, root, primary = self.fixture()
        self.addCleanup(temp.cleanup)
        source = root / "source"
        source.mkdir()
        primary.parent.mkdir(parents=True)
        primary.symlink_to(source)
        alias = root / ".claude/skills/example"

        with self.assertRaisesRegex(install.MountError, "refusing primary symlink"):
            install.reconcile_mounts(primary, [alias])
        self.assertFalse(alias.exists())
        self.assertFalse(alias.is_symlink())

    def test_refuses_independent_alias_directory_before_other_changes(self) -> None:
        temp, root, primary = self.fixture()
        self.addCleanup(temp.cleanup)
        primary.mkdir(parents=True)
        missing = root / ".claude/skills/example"
        independent = root / ".cursor/skills/example"
        independent.mkdir(parents=True)

        with self.assertRaisesRegex(install.MountError, "independent-directory"):
            install.reconcile_mounts(primary, [missing, independent])
        self.assertFalse(missing.exists())
        self.assertTrue(independent.is_dir())

    def test_refuses_regular_file_alias(self) -> None:
        temp, root, primary = self.fixture()
        self.addCleanup(temp.cleanup)
        primary.mkdir(parents=True)
        alias = root / ".claude/skills/example"
        alias.parent.mkdir(parents=True)
        alias.write_text("do not replace", encoding="utf-8")

        with self.assertRaisesRegex(install.MountError, "other"):
            install.reconcile_mounts(primary, [alias])
        self.assertEqual(alias.read_text(encoding="utf-8"), "do not replace")


if __name__ == "__main__":
    unittest.main()
