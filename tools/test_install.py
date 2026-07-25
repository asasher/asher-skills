#!/usr/bin/env python3
"""Regression tests for tools/install.py.

Each test pins one defect from asher-skills#103 that `npx skills add` shipped:
uncompiled variants, the `build` discovery blind spot, and skills that are never
removed. They run against the real skill sources — the point is that this repo's
actual layout installs correctly, which a synthetic fixture would not prove.
"""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import install  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class InstallTest(unittest.TestCase):
    def setUp(self) -> None:
        self.target = Path(tempfile.mkdtemp(prefix="install-test-"))
        self.addCleanup(shutil.rmtree, self.target, ignore_errors=True)

    def lock(self) -> dict:
        return json.loads((self.target / "skills-lock.json").read_text())["skills"]

    def test_variant_skill_compiles_both_provider_trees(self) -> None:
        """staffing must land compiled per provider, not as raw source."""
        result = install.install(ROOT, self.target, {"staffing"})
        self.assertEqual(result["compiled"], ["staffing"])

        for provider, mount in (("claude", ".claude"), ("codex", ".agents")):
            tree = self.target / mount / "skills" / "staffing"
            self.assertFalse(tree.is_symlink(), f"{provider} mount collapsed to a symlink")
            self.assertTrue(tree.is_dir())
            identity = (tree / "templates" / "global" / "provider.txt").read_text().strip()
            self.assertEqual(identity, provider)
            # The overlay must have replaced the source stubs.
            harness = (tree / "reference" / "harness.md").read_text()
            self.assertNotIn("placeholder", harness.lower())
            module = (tree / "templates" / "global" / "staffing.module.md").read_text()
            self.assertIn("| model | cost | intelligence | taste | effort |", module)
            # The {{COMMON}} marker is resolved by render-global.py, not at install
            # time, so the compiled tree must ship the marker and its partial together.
            self.assertEqual(module.count("{{COMMON}}"), 1)
            self.assertTrue((tree / "templates" / "global" / "staffing.common.md").is_file())
            self.assertNotIn("variants", [p.name for p in tree.iterdir()])

    def test_variant_lock_records_real_hashes(self) -> None:
        install.install(ROOT, self.target, {"staffing"})
        lock = json.loads((self.target / ".agents/asher-skills/variant-lock.json").read_text())
        entry = lock["skills"]["staffing"]
        self.assertEqual(sorted(entry["providers"]), ["claude", "codex"])
        for provider, block in entry["providers"].items():
            tree = self.target / block["mount"]
            import catalog
            self.assertEqual(block["effective_hash"], catalog.tree_hash(tree))

    def test_build_skill_is_installed(self) -> None:
        """The vendor CLI skips directories named `build`; this must not."""
        install.install(ROOT, self.target, {"build"})
        self.assertTrue((self.target / ".agents/skills/build").is_dir())
        self.assertTrue((self.target / ".claude/skills/build").is_symlink())
        self.assertIn("build", self.lock())

    def test_alias_points_at_primary(self) -> None:
        install.install(ROOT, self.target, {"handoff"})
        alias = self.target / ".claude/skills/handoff"
        self.assertTrue(alias.is_symlink())
        self.assertEqual(alias.resolve(), (self.target / ".agents/skills/handoff").resolve())

    def test_required_siblings_are_pulled_in(self) -> None:
        result = install.install(ROOT, self.target, {"backlog"})
        self.assertIn("backlog", result["installed"])
        self.assertGreater(len(result["installed"]), 1, "closure did not expand")

    def test_dropped_skill_is_removed(self) -> None:
        install.install(ROOT, self.target, {"handoff", "watch-until"})
        self.assertTrue((self.target / ".agents/skills/handoff").exists())

        result = install.install(ROOT, self.target, {"watch-until"})
        self.assertIn("handoff", result["removed"])
        self.assertFalse((self.target / ".agents/skills/handoff").exists())
        self.assertFalse((self.target / ".claude/skills/handoff").is_symlink())
        self.assertNotIn("handoff", self.lock())

    def test_foreign_skills_are_never_pruned(self) -> None:
        install.install(ROOT, self.target, {"handoff"})
        foreign = self.target / ".agents/skills/vendor-thing"
        foreign.mkdir(parents=True)
        (foreign / "SKILL.md").write_text("x")
        lock_path = self.target / "skills-lock.json"
        data = json.loads(lock_path.read_text())
        data["skills"]["vendor-thing"] = {"source": "someone/else", "sourceType": "github"}
        lock_path.write_text(json.dumps(data, indent=2))

        result = install.install(ROOT, self.target, {"watch-until"})
        self.assertNotIn("vendor-thing", result["removed"])
        self.assertTrue(foreign.is_dir())
        self.assertIn("vendor-thing", self.lock())

    def test_no_prune_keeps_dropped_skills(self) -> None:
        install.install(ROOT, self.target, {"handoff"})
        result = install.install(ROOT, self.target, {"watch-until"}, prune=False)
        self.assertEqual(result["removed"], [])
        self.assertTrue((self.target / ".agents/skills/handoff").exists())

    def test_live_mode_links_to_source(self) -> None:
        """Self-install mounts point at the source, so they cannot go stale."""
        install.install(ROOT, self.target, {"handoff"}, live=True)
        primary = self.target / ".agents/skills/handoff"
        self.assertTrue(primary.is_symlink())
        self.assertEqual(primary.resolve(), (ROOT / "skills/software-development/handoff").resolve())

    def test_live_mode_still_compiles_variants(self) -> None:
        """A compiled tree has no on-disk source to link to."""
        install.install(ROOT, self.target, {"staffing"}, live=True)
        tree = self.target / ".claude/skills/staffing"
        self.assertFalse(tree.is_symlink())
        self.assertEqual((tree / "templates/global/provider.txt").read_text().strip(), "claude")

    def test_reinstall_is_idempotent(self) -> None:
        first = install.install(ROOT, self.target, {"staffing", "handoff"})
        lock_before = (self.target / "skills-lock.json").read_bytes()
        variant_before = (self.target / ".agents/asher-skills/variant-lock.json").read_bytes()

        second = install.install(ROOT, self.target, {"staffing", "handoff"})
        self.assertEqual(first["installed"], second["installed"])
        self.assertEqual(second["removed"], [])
        self.assertEqual(lock_before, (self.target / "skills-lock.json").read_bytes())
        self.assertEqual(
            variant_before, (self.target / ".agents/asher-skills/variant-lock.json").read_bytes()
        )

    def test_computed_hash_matches_the_vendor_folder_hash(self) -> None:
        """The lock must stay verifiable by the vendor's own checker.

        `build` is the anchor: metis carried b64c6e9b… for it on 2026-07-24, computed
        by the vendor CLI, and the source has not changed since. Reproducing it proves
        we implement `computeSkillFolderHash`, not merely something deterministic.
        """
        install.install(ROOT, self.target, {"build"})
        recorded = self.lock()["build"]["computedHash"]
        self.assertNotIn(":", recorded, "must be bare hex, not a prefixed digest")
        self.assertEqual(len(recorded), 64)
        self.assertEqual(
            recorded, install.installed_hash(self.target / ".agents/skills/build")
        )
        self.assertTrue(recorded.startswith("b64c6e9bec32"), recorded)

    def test_computed_hash_tracks_the_installed_tree(self) -> None:
        """A source hash cannot catch a hand-edited mount; this must."""
        install.install(ROOT, self.target, {"handoff"})
        before = self.lock()["handoff"]["computedHash"]
        edited = self.target / ".agents/skills/handoff/SKILL.md"
        edited.write_text(edited.read_text() + "\nhand edit\n")
        self.assertNotEqual(before, install.installed_hash(edited.parent))

    def test_foreign_entries_keep_their_field_order(self) -> None:
        """skills-lock.json is only partly ours — don't churn other people's entries."""
        install.install(ROOT, self.target, {"handoff"})
        lock_path = self.target / "skills-lock.json"
        data = json.loads(lock_path.read_text())
        foreign = {"computedHash": "deadbeef", "zzz": 1, "source": "someone/else"}
        data["skills"]["vendor-thing"] = dict(foreign)
        lock_path.write_text(json.dumps(data, indent=2))

        install.install(ROOT, self.target, {"handoff"})
        after = json.loads(lock_path.read_text())["skills"]["vendor-thing"]
        self.assertEqual(list(after.keys()), list(foreign.keys()))
        self.assertEqual(after, foreign)

    def test_bare_install_refreshes_the_recorded_set(self) -> None:
        """A bare `install` must never widen a curated selection to every skill."""
        install.install(ROOT, self.target, {"handoff", "watch-until"})
        with contextlib.redirect_stdout(io.StringIO()):
            code = install.main(["install", "--into", str(self.target), "--root", str(ROOT)])
        self.assertEqual(code, 0)
        self.assertEqual(sorted(self.lock()), ["handoff", "watch-until"])

    def test_bare_install_without_a_lockfile_is_an_error(self) -> None:
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            install.main(["install", "--into", str(self.target), "--root", str(ROOT)])

    def test_unknown_skill_is_rejected(self) -> None:
        with self.assertRaises(install.InstallError):
            install.install(ROOT, self.target, {"no-such-skill"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
