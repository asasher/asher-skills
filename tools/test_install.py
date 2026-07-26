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
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import catalog  # noqa: E402
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

    def test_primary_mount_is_a_real_copy(self) -> None:
        """Mounts are decoupled from sources — no symlink mode (asher-skills#118).

        A running session must read a stable copy while sources change on
        branches; a merged change reaches mounts only via reconcile (reinstall).
        """
        install.install(ROOT, self.target, {"handoff"})
        primary = self.target / ".agents/skills/handoff"
        self.assertTrue(primary.is_dir())
        self.assertFalse(primary.is_symlink())
        source = (ROOT / "skills/software-development/handoff/SKILL.md").read_text()
        self.assertEqual((primary / "SKILL.md").read_text(), source)

    def test_self_install_rejects_a_foreign_target(self) -> None:
        """--self means this repo into itself; any other target is an error."""
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            install.main(["install", "--self", "--into", str(self.target), "--root", str(ROOT)])

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


class SetupReportTest(unittest.TestCase):
    """What an install says about which skills changed and which setups follow.

    The installer reports; it never runs a setup. These tests run against the real
    sources and real git history, so the expectations are derived from git rather
    than pinned to shas that rot.
    """

    def setUp(self) -> None:
        self.target = Path(tempfile.mkdtemp(prefix="install-report-"))
        self.addCleanup(shutil.rmtree, self.target, ignore_errors=True)

    def state_path(self) -> Path:
        return self.target / ".agents/asher-skills/install.json"

    def rewrite_recorded_revision(self, revision: object) -> None:
        state = json.loads(self.state_path().read_text())
        state["source_revision"] = revision
        self.state_path().write_text(json.dumps(state, indent=2) + "\n")

    def seed_repo(self, files: dict[str, str]) -> tuple[Path, Callable[..., str], str]:
        """A throwaway git repo holding `files`, committed. Returns (repo, run, head).

        Every `_changed_sources` edge case needs the same repo, so the seed lives in
        one place: a machine-level git default that breaks it is fixed here once.
        """
        repo = Path(tempfile.mkdtemp(prefix="install-git-"))
        self.addCleanup(shutil.rmtree, repo, ignore_errors=True)

        def run(*args: str) -> str:
            done = subprocess.run(
                ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
            )
            return done.stdout.strip()

        run("init", "-q")
        run("config", "user.email", "test@example.invalid")
        run("config", "user.name", "test")
        run("config", "commit.gpgsign", "false")  # signing configured on the host must not fail this
        for relative, text in files.items():
            path = repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        run("add", "-A")
        run("commit", "-qm", "seed")
        return repo, run, run("rev-parse", "HEAD")

    def dirty_source(self, source: str) -> Path:
        """Leave a real skill source uncommitted for the length of one test.

        An untracked file is the reversible half of dirtiness: the tracked content
        is never touched, so a crashed test cannot leave the repo edited.
        """
        probe = ROOT / source / ".setup-report-probe"
        self.addCleanup(probe.unlink, missing_ok=True)
        probe.write_text("uncommitted work\n")
        return probe

    def git(self, *args: str) -> str:
        done = subprocess.run(
            # Same quoting setting the installer uses, so the expectation this
            # derives cannot share a blind spot with the code under test.
            ["git", "-C", str(ROOT), "-c", "core.quotePath=false", *args],
            capture_output=True, text=True, check=True,
        )
        return done.stdout.strip()

    def changed_per_git(self, since: str, sources: dict[str, str]) -> list[str]:
        """What git itself says changed since `since`, for the given skill sources.

        Deriving the expectation instead of hardcoding one keeps these tests honest
        in a working tree that has edits of its own: a source edited in place really
        has changed, and the assertion tracks that rather than skipping.
        """
        touched = self.git("diff", "--name-only", "--relative", since, "--").splitlines()
        touched += self.git("ls-files", "--others", "--exclude-standard").splitlines()
        return sorted(
            name for name, path in sources.items()
            if any(line == path or line.startswith(path + "/") for line in touched)
        )

    def recorded_sources(self) -> dict[str, str]:
        recorded = json.loads(self.state_path().read_text())["skills"]
        return {name: entry["source"] for name, entry in recorded.items()}

    def test_first_install_treats_the_whole_closure_as_changed(self) -> None:
        result = install.install(ROOT, self.target, {"backlog"})
        report = result["setup_report"]
        self.assertEqual(report["basis"], "first-install")
        self.assertIsNone(report["since_revision"])
        self.assertEqual(report["changed"], result["installed"])
        self.assertEqual(report["setup_order"], ["diagnosing-bugs"])

    def test_nothing_changed_reports_empty_fields_rather_than_omitting_them(self) -> None:
        """"Nothing to do" and "not reported" must be distinguishable by a consumer."""
        graph = catalog.discover(ROOT)
        resolution = catalog.resolve(graph, {"backlog"}, set())
        closure = set(resolution["closure"])

        report = install._setup_report(
            graph, closure, resolution["setup_order"], closure, [], "0123456", [],
        )
        self.assertEqual(
            sorted(report), ["basis", "changed", "setup_order", "since_revision"]
        )
        self.assertEqual(report["basis"], "revision-diff")
        self.assertEqual(report["changed"], [])
        self.assertEqual(report["setup_order"], [])

    def test_reinstall_at_the_same_revision_reports_only_what_git_reports(self) -> None:
        install.install(ROOT, self.target, {"handoff"})
        sources = self.recorded_sources()
        report = install.install(ROOT, self.target, {"handoff"})["setup_report"]
        head = self.git("rev-parse", "HEAD")
        self.assertEqual(report["basis"], "revision-diff")
        self.assertEqual(report["since_revision"], head)
        self.assertEqual(report["changed"], self.changed_per_git(head, sources))

    def test_a_real_source_change_since_the_recorded_revision_is_reported(self) -> None:
        """Demoable end to end: the skill whose source moved is the one named."""
        source = "skills/software-development/diagnosing-bugs"
        older = self.git("rev-parse", self.git("log", "-1", "--format=%H", "--", source) + "^")

        install.install(ROOT, self.target, {"backlog"})
        sources = self.recorded_sources()
        self.rewrite_recorded_revision(older)

        report = install.install(ROOT, self.target, {"backlog"})["setup_report"]
        self.assertEqual(report["basis"], "revision-diff")
        self.assertEqual(report["since_revision"], older)

        # Expectation from git itself, so the test cannot rot as history grows.
        self.assertEqual(report["changed"], self.changed_per_git(older, sources))
        self.assertIn("diagnosing-bugs", report["changed"])
        self.assertEqual(report["setup_order"], ["diagnosing-bugs"])

    def test_setup_order_is_the_catalogs_own_resolution_order(self) -> None:
        selected = {"backlog", "research", "capture-to-inbox"}
        graph = catalog.discover(ROOT)
        expected = [
            name for name in catalog.resolve(graph, selected, set())["setup_order"]
            if graph[name].setup
        ]

        report = install.install(ROOT, self.target, selected)["setup_report"]
        self.assertEqual(report["setup_order"], expected)
        self.assertNotEqual(expected, sorted(expected), "resolution order is being re-sorted away")
        self.assertTrue(set(expected) < set(report["changed"]), "setups must be a subset of changed")

    def test_a_newly_added_skill_is_changed_even_at_the_same_revision(self) -> None:
        """Its mounts are new here, so its setup has never run in this repo."""
        install.install(ROOT, self.target, {"backlog"})

        result = install.install(ROOT, self.target, {"backlog", "research"})
        report = result["setup_report"]
        head = self.git("rev-parse", "HEAD")
        self.assertEqual(report["basis"], "revision-diff")
        self.assertIn("research", report["changed"])
        self.assertIn("research", report["setup_order"])
        # Nothing else is changed unless git says its source moved.
        self.assertEqual(
            set(report["changed"]) - {"research"},
            set(self.changed_per_git(head, self.recorded_sources())) - {"research"},
        )

    def test_an_unresolvable_recorded_revision_falls_back_to_the_whole_closure(self) -> None:
        """An unanswerable comparison must not read as nothing-to-do."""
        result = install.install(ROOT, self.target, {"backlog"})
        self.rewrite_recorded_revision("0" * 40)

        report = install.install(ROOT, self.target, {"backlog"})["setup_report"]
        self.assertEqual(report["basis"], "unknown-revision")
        self.assertEqual(report["since_revision"], "0" * 40)
        self.assertEqual(report["changed"], result["installed"])
        self.assertEqual(report["setup_order"], ["diagnosing-bugs"])

    def test_a_missing_recorded_revision_falls_back_to_the_whole_closure(self) -> None:
        result = install.install(ROOT, self.target, {"backlog"})
        self.rewrite_recorded_revision(None)

        report = install.install(ROOT, self.target, {"backlog"})["setup_report"]
        self.assertEqual(report["basis"], "unknown-revision")
        self.assertIsNone(report["since_revision"])
        self.assertEqual(report["changed"], result["installed"])

    def test_an_install_runs_no_process_but_git(self) -> None:
        """The report names the setups; running them stays the agent's job."""
        real = install.subprocess.run
        commands: list[list[str]] = []

        def spy(command, *args, **kwargs):
            commands.append(list(command))
            return real(command, *args, **kwargs)

        install.subprocess.run = spy
        self.addCleanup(setattr, install.subprocess, "run", real)

        install.install(ROOT, self.target, {"research", "staffing"})
        install.install(ROOT, self.target, {"research", "staffing"})

        self.assertTrue(commands, "no subprocess ran at all; the spy is not wired in")
        for command in commands:
            self.assertEqual(command[0], "git", f"unexpected process: {command}")

    def test_a_reconcile_names_the_setups_the_freshly_copied_mounts_need(self) -> None:
        """The reconcile step is the moment this report exists for.

        Mounts are decoupled copies, so a merged source change reaches them only by
        reinstalling — and copying a source forward does not re-run the setup its
        playbooks came from. The refresh that moves the copy must name that setup.
        """
        source = "skills/software-development/diagnosing-bugs"
        older = self.git("rev-parse", self.git("log", "-1", "--format=%H", "--", source) + "^")

        install.install(ROOT, self.target, {"backlog"})
        self.rewrite_recorded_revision(older)

        report = install.install(ROOT, self.target, {"backlog"})["setup_report"]

        mount = self.target / ".agents/skills/diagnosing-bugs"
        self.assertFalse(mount.is_symlink(), "mount is not a decoupled copy")
        # The copy caught up to the source, and the report says the setup did not.
        self.assertEqual(
            (mount / "SKILL.md").read_bytes(),
            (ROOT / source / "SKILL.md").read_bytes(),
        )
        self.assertIn("diagnosing-bugs", report["changed"])
        self.assertEqual(report["setup_order"], ["diagnosing-bugs"])

    def test_a_recorded_revision_cannot_smuggle_a_git_option(self) -> None:
        """`install.json` is checked in, so a poisoned revision is a reachable input.

        Handed to git bare, `--output=<path>` truncates that path and exits 0 with
        empty output — the report would read as nothing-to-do while destroying a file.
        """
        victim = self.target / "victim.txt"
        victim.write_text("important data\n")
        result = install.install(ROOT, self.target, {"backlog"})
        self.rewrite_recorded_revision(f"--output={victim}")

        report = install.install(ROOT, self.target, {"backlog"})["setup_report"]
        self.assertEqual(victim.read_text(), "important data\n", "git took it as an option")
        self.assertEqual(report["basis"], "unknown-revision")
        self.assertEqual(report["changed"], result["installed"])
        # The summary must not echo the junk back as though it were a revision.
        summary = install._summarize(report)
        self.assertIn("not a usable object name", summary[0])
        self.assertNotIn("--output", summary[0])

    def test_a_source_uncommitted_at_install_time_is_changed_once_it_is_reverted(self) -> None:
        """The mounts are built from the working tree; the recorded revision is HEAD.

        So an install that followed uncommitted work installed content the recorded
        revision does not describe. Reverting that work changes the mount again, and
        a report that called this nothing-to-do would be the silent under-report the
        whole design exists to avoid.
        """
        source = "skills/software-development/diagnosing-bugs"
        probe = self.dirty_source(source)

        install.install(ROOT, self.target, {"backlog"})
        probe.unlink()

        report = install.install(ROOT, self.target, {"backlog"})["setup_report"]
        self.assertIn("diagnosing-bugs", report["changed"])
        self.assertIn("diagnosing-bugs", report["setup_order"])

    def test_the_state_file_records_which_sources_were_uncommitted(self) -> None:
        """That record is what makes the next comparison answerable."""
        self.dirty_source("skills/software-development/diagnosing-bugs")

        install.install(ROOT, self.target, {"backlog"})
        recorded = json.loads(self.state_path().read_text())
        self.assertIn("diagnosing-bugs", recorded["source_dirty"])

    def test_a_previously_uncommitted_source_is_changed_against_a_clean_tree(self) -> None:
        """Pinned on the pure reporter, so no working-tree state can mask it."""
        graph = catalog.discover(ROOT)
        resolution = catalog.resolve(graph, {"backlog"}, set())
        closure = set(resolution["closure"])

        report = install._setup_report(
            graph, closure, resolution["setup_order"], closure, [], "0123456",
            ["diagnosing-bugs"],
        )
        self.assertEqual(report["basis"], "revision-diff")
        self.assertEqual(report["changed"], ["diagnosing-bugs"])
        self.assertEqual(report["setup_order"], ["diagnosing-bugs"])

    def test_state_that_cannot_say_what_was_uncommitted_falls_back_to_the_closure(self) -> None:
        """State written before this was recorded cannot answer, so it must not claim to."""
        graph = catalog.discover(ROOT)
        resolution = catalog.resolve(graph, {"backlog"}, set())
        closure = set(resolution["closure"])

        report = install._setup_report(
            graph, closure, resolution["setup_order"], closure, [], "0123456", None,
        )
        self.assertEqual(report["basis"], "unknown-revision")
        self.assertEqual(report["changed"], sorted(closure))

    def test_a_dirty_record_holding_junk_is_as_unanswerable_as_none(self) -> None:
        """Half-trusting the record is the outcome the fallback exists to prevent.

        Dropping the unreadable members and keeping `revision-diff` would report a
        real comparison over a set that silently lost entries.
        """
        graph = catalog.discover(ROOT)
        resolution = catalog.resolve(graph, {"backlog"}, set())
        closure = set(resolution["closure"])

        for record in ([{"name": "diagnosing-bugs"}], ["diagnosing-bugs", 7], [None]):
            with self.subTest(record=record):
                report = install._setup_report(
                    graph, closure, resolution["setup_order"], closure, [], "0123456", record,
                )
                self.assertEqual(report["basis"], "unknown-revision")
                self.assertEqual(report["changed"], sorted(closure))

    def test_a_corrupt_dirty_record_does_not_read_as_a_real_comparison(self) -> None:
        """`install.json` is checked in, so a re-serialized entry is a reachable input."""
        probe = self.dirty_source("skills/software-development/diagnosing-bugs")
        result = install.install(ROOT, self.target, {"backlog"})
        probe.unlink()

        state = json.loads(self.state_path().read_text())
        self.assertEqual(state["source_dirty"], ["diagnosing-bugs"])
        state["source_dirty"] = [{"name": "diagnosing-bugs"}]
        self.state_path().write_text(json.dumps(state, indent=2) + "\n")

        report = install.install(ROOT, self.target, {"backlog"})["setup_report"]
        self.assertEqual(report["basis"], "unknown-revision")
        self.assertEqual(report["changed"], result["installed"])

    def test_a_recorded_revision_that_is_not_a_string_still_reads_as_recorded(self) -> None:
        """Absent and unusable are different states; the report must not merge them.

        An operator told the field is absent goes looking in the wrong place, and a
        consumer cannot tell "never recorded" from "recorded but corrupt" — the same
        distinction `basis` exists to keep.
        """
        install.install(ROOT, self.target, {"backlog"})
        self.rewrite_recorded_revision(12345)

        report = install.install(ROOT, self.target, {"backlog"})["setup_report"]
        self.assertEqual(report["basis"], "unknown-revision")
        self.assertEqual(report["since_revision"], 12345)

        summary = install._summarize(report)
        self.assertIn("not a usable object name", summary[0])
        self.assertNotIn("no source revision", summary[0])

    def test_a_malformed_recorded_revision_does_not_crash_the_install(self) -> None:
        for revision in (12345, ["abc"], "not a revision", ""):
            with self.subTest(revision=revision):
                target = Path(tempfile.mkdtemp(prefix="install-report-"))
                self.addCleanup(shutil.rmtree, target, ignore_errors=True)
                result = install.install(ROOT, target, {"backlog"})
                state = json.loads((target / ".agents/asher-skills/install.json").read_text())
                state["source_revision"] = revision
                (target / ".agents/asher-skills/install.json").write_text(json.dumps(state))

                report = install.install(ROOT, target, {"backlog"})["setup_report"]
                self.assertEqual(report["basis"], "unknown-revision")
                self.assertEqual(report["changed"], result["installed"])

    def test_a_source_file_git_does_not_track_yet_counts_as_changed(self) -> None:
        """A skill gaining `reference/setup.md` is exactly what the report exists to catch.

        Driven against a throwaway git repo rather than this one, so the assertion
        does not depend on writing into real skill sources.
        """
        repo, _, head = self.seed_repo({"skills/tracked.md": "one\n"})

        self.assertEqual(install._changed_sources(repo, head), [])
        (repo / "skills" / "untracked.md").write_text("two\n")
        self.assertEqual(install._changed_sources(repo, head), ["skills/untracked.md"])

    def test_a_path_git_would_quote_is_still_matched_against_its_source(self) -> None:
        """git quotes non-ASCII paths by default; a quoted path matches no source.

        The failure is silent and in the unsafe direction — the skill drops out of
        `changed`, so its setup is never named.
        """
        repo, _, head = self.seed_repo({"skills/café.md": "one\n"})

        (repo / "skills" / "café.md").write_text("two\n")
        (repo / "skills" / "référence.md").write_text("three\n")
        self.assertEqual(
            install._changed_sources(repo, head),
            ["skills/café.md", "skills/référence.md"],
        )

    def run_main(self, *extra: str) -> tuple[dict, str]:
        out, err = io.StringIO(), io.StringIO()
        argv = ["install", "--into", str(self.target), "--root", str(ROOT), *extra]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = install.main(argv)
        self.assertEqual(code, 0, err.getvalue())
        return json.loads(out.getvalue()), err.getvalue()

    def test_stdout_stays_parseable_and_the_summary_goes_to_stderr(self) -> None:
        result, summary = self.run_main("--skill", "backlog")
        self.assertEqual(result["setup_report"]["basis"], "first-install")
        self.assertNotIn("{", summary, "the JSON leaked onto stderr")
        self.assertIn("diagnosing-bugs", summary)

        # The summary and the JSON must agree — the human and the agent read the
        # same run, and a summary that drifts from the report is worse than none.
        result, summary = self.run_main()
        setups = result["setup_report"]["setup_order"]
        if setups:
            self.assertIn("setups to re-run, in order: " + ", ".join(setups), summary)
        else:
            self.assertIn("no setups to re-run", summary)


if __name__ == "__main__":
    unittest.main(verbosity=2)
