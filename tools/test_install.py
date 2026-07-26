#!/usr/bin/env python3
"""Regression tests for tools/install.py.

Each test pins one defect from asher-skills#103 that `npx skills add` shipped —
uncompiled variants, the `build` discovery blind spot, skills that are never
removed — plus the state model that replaced its lockfile. They run against the
real skill sources: the claim worth pinning is that this repo's actual layout
installs correctly, which a synthetic fixture would not prove.
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

    def state(self) -> dict:
        return json.loads((self.target / ".agents/asher-skills/install.json").read_text())

    # ---- mounting -------------------------------------------------------

    def test_variant_skill_compiles_both_provider_trees(self) -> None:
        """staffing must land compiled per provider, not as raw source."""
        result = install.install(ROOT, self.target, {"staffing"})
        self.assertEqual(result["compiled"], ["staffing"])

        for provider, mount in (("claude", ".claude"), ("codex", ".agents")):
            tree = self.target / mount / "skills" / "staffing"
            self.assertFalse(tree.is_symlink(), f"{provider} mount collapsed to a symlink")
            identity = (tree / "templates" / "seed" / "provider.txt").read_text().strip()
            self.assertEqual(identity, provider)
            harness = (tree / "reference" / "harness.md").read_text()
            self.assertNotIn("placeholder", harness.lower())
            seed = (tree / "templates" / "seed" / "roster-seed.md").read_text()
            self.assertIn("| model | cost | intelligence | taste | effort |", seed)
            # The seed is read whole by setup; nothing renders it, so it must ship
            # self-contained rather than carrying a marker for a retired renderer.
            self.assertNotIn("{{", seed)
            self.assertNotIn("variants", [p.name for p in tree.iterdir()])

    def test_build_skill_is_installed(self) -> None:
        """The vendor CLI skips directories named `build`; this must not."""
        install.install(ROOT, self.target, {"build"})
        self.assertTrue((self.target / ".agents/skills/build").is_dir())
        self.assertTrue((self.target / ".claude/skills/build").is_symlink())
        self.assertIn("build", self.state()["skills"])

    def test_alias_points_at_primary(self) -> None:
        install.install(ROOT, self.target, {"handoff"})
        alias = self.target / ".claude/skills/handoff"
        self.assertTrue(alias.is_symlink())
        self.assertEqual(alias.resolve(), (self.target / ".agents/skills/handoff").resolve())

    def test_required_siblings_are_pulled_in(self) -> None:
        result = install.install(ROOT, self.target, {"backlog"})
        self.assertIn("backlog", result["installed"])
        self.assertGreater(len(result["installed"]), 1, "closure did not expand")

    # ---- state ----------------------------------------------------------

    def test_state_records_sources_and_no_hashes(self) -> None:
        install.install(ROOT, self.target, {"staffing", "handoff"})
        state = self.state()
        self.assertEqual(state["schema_version"], 1)
        self.assertEqual(state["skills"]["handoff"]["source"], "skills/software-development/handoff")
        self.assertEqual(
            sorted(state["skills"]["staffing"]["providers"]), ["claude", "codex"]
        )
        # Integrity is answered by `check` against source, not by a stored quantity.
        self.assertNotIn("hash", json.dumps(state).lower())

    def test_our_entries_are_stripped_from_the_foreign_lockfile(self) -> None:
        """skills-lock.json belongs to another installer; we take our rows out."""
        lock = self.target / "skills-lock.json"
        lock.write_text(json.dumps({
            "version": 1,
            "skills": {
                "handoff": {"source": "asasher/asher-skills", "computedHash": "abc"},
                "vendor-thing": {"source": "someone/else", "zzz": 1, "computedHash": "def"},
            },
        }, indent=2))

        result = install.install(ROOT, self.target, {"handoff"})
        self.assertEqual(result["unlocked_from_foreign_lockfile"], ["handoff"])
        remaining = json.loads(lock.read_text())["skills"]
        self.assertNotIn("handoff", remaining)
        # Foreign rows survive untouched, field order included.
        self.assertEqual(list(remaining["vendor-thing"]), ["source", "zzz", "computedHash"])

    def test_legacy_variant_lock_is_superseded(self) -> None:
        legacy = self.target / ".agents/asher-skills/variant-lock.json"
        legacy.parent.mkdir(parents=True)
        legacy.write_text(json.dumps({"schema_version": 1, "skills": {}}))
        install.install(ROOT, self.target, {"staffing"})
        self.assertFalse(legacy.exists())
        self.assertTrue((self.target / ".agents/asher-skills/install.json").is_file())

    def test_recorded_set_migrates_from_the_foreign_lockfile(self) -> None:
        """A repo installed by the old CLI keeps its set on first run."""
        lock = self.target / "skills-lock.json"
        lock.write_text(json.dumps({"version": 1, "skills": {
            "handoff": {"source": "asasher/asher-skills"},
            "watch-until": {"source": "asasher/asher-skills"},
            "vendor-thing": {"source": "someone/else"},
        }}, indent=2))
        with contextlib.redirect_stdout(io.StringIO()):
            code = install.main(["install", "--into", str(self.target), "--root", str(ROOT)])
        self.assertEqual(code, 0)
        self.assertEqual(sorted(self.state()["skills"]), ["handoff", "watch-until"])

    def test_bare_install_refreshes_the_recorded_set(self) -> None:
        """A bare install must never widen a curated selection to every skill."""
        install.install(ROOT, self.target, {"handoff", "watch-until"})
        with contextlib.redirect_stdout(io.StringIO()):
            code = install.main(["install", "--into", str(self.target), "--root", str(ROOT)])
        self.assertEqual(code, 0)
        self.assertEqual(sorted(self.state()["skills"]), ["handoff", "watch-until"])

    def test_bare_install_without_state_is_an_error(self) -> None:
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            install.main(["install", "--into", str(self.target), "--root", str(ROOT)])

    # ---- removal --------------------------------------------------------

    def test_dropped_skill_is_removed(self) -> None:
        install.install(ROOT, self.target, {"handoff", "watch-until"})
        result = install.install(ROOT, self.target, {"watch-until"})
        self.assertIn("handoff", result["removed"])
        self.assertFalse((self.target / ".agents/skills/handoff").exists())
        self.assertFalse((self.target / ".claude/skills/handoff").is_symlink())
        self.assertNotIn("handoff", self.state()["skills"])

    def test_no_prune_keeps_dropped_skills(self) -> None:
        install.install(ROOT, self.target, {"handoff"})
        result = install.install(ROOT, self.target, {"watch-until"}, prune=False)
        self.assertEqual(result["removed"], [])
        self.assertTrue((self.target / ".agents/skills/handoff").exists())

    # ---- self-install ---------------------------------------------------

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
        self.assertEqual((tree / "templates/seed/provider.txt").read_text().strip(), "claude")

    # ---- check ----------------------------------------------------------

    def test_check_is_clean_after_install(self) -> None:
        install.install(ROOT, self.target, {"staffing", "handoff", "build"})
        result = install.check(ROOT, self.target)
        self.assertTrue(result["clean"], result["drift"])
        self.assertEqual(result["missing_mounts"], [])

    def test_check_names_the_drifted_file(self) -> None:
        """The point of diffing against source: say which file, not 'hash differs'."""
        install.install(ROOT, self.target, {"handoff"})
        edited = self.target / ".agents/skills/handoff/SKILL.md"
        edited.write_text(edited.read_text() + "\nhand edit\n")

        result = install.check(ROOT, self.target)
        self.assertFalse(result["clean"])
        self.assertIn("modified: SKILL.md", result["drift"]["handoff"])

    def test_check_reports_an_added_file(self) -> None:
        install.install(ROOT, self.target, {"handoff"})
        (self.target / ".agents/skills/handoff/stowaway.md").write_text("x")
        result = install.check(ROOT, self.target)
        self.assertIn("unexpected: stowaway.md", result["drift"]["handoff"])

    def test_check_reports_a_missing_mount(self) -> None:
        install.install(ROOT, self.target, {"handoff"})
        shutil.rmtree(self.target / ".agents/skills/handoff")
        result = install.check(ROOT, self.target)
        self.assertFalse(result["clean"])
        self.assertTrue(result["missing_mounts"])

    def test_check_detects_drift_in_a_compiled_provider_tree(self) -> None:
        install.install(ROOT, self.target, {"staffing"})
        edited = self.target / ".claude/skills/staffing/reference/harness.md"
        edited.write_text("tampered\n")
        result = install.check(ROOT, self.target)
        self.assertIn("modified: reference/harness.md", result["drift"]["staffing"])

    def test_check_exit_code_signals_drift(self) -> None:
        install.install(ROOT, self.target, {"handoff"})
        argv = ["check", "--into", str(self.target), "--root", str(ROOT)]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(install.main(argv), 0)
            (self.target / ".agents/skills/handoff/SKILL.md").write_text("tampered")
            self.assertEqual(install.main(argv), 1)

    # ---- misc -----------------------------------------------------------

    def test_reinstall_is_idempotent(self) -> None:
        first = install.install(ROOT, self.target, {"staffing", "handoff"})
        before = (self.target / ".agents/asher-skills/install.json").read_bytes()
        second = install.install(ROOT, self.target, {"staffing", "handoff"})
        self.assertEqual(first["installed"], second["installed"])
        self.assertEqual(second["removed"], [])
        self.assertEqual(before, (self.target / ".agents/asher-skills/install.json").read_bytes())

    def test_unknown_skill_is_rejected(self) -> None:
        with self.assertRaises(install.InstallError):
            install.install(ROOT, self.target, {"no-such-skill"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
