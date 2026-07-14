#!/usr/bin/env python3
"""Public-seam checks for provider-specific skill packages."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
CATALOG = SKILL / "scripts" / "catalog.py"
INSTALL = SKILL / "scripts" / "install.py"


def run(
    *args: object, ok: bool = True, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    command = [str(arg) for arg in args]
    if command and command[0].endswith(".py"):
        command.insert(0, sys.executable)
    result = subprocess.run(
        command, capture_output=True, text=True, check=False, env=env
    )
    if ok and result.returncode:
        raise AssertionError(f"command failed: {result.stderr}\n{result.stdout}")
    return result


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class ProviderVariantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "catalog"
        self.consumer = Path(self.temp.name) / "consumer"
        self.source = self.root / "skills" / "system" / "pilot"
        self.consumer.mkdir(parents=True)
        write(
            self.source / "SKILL.md",
            """---
name: pilot
description: Pilot provider variant.
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: thread
  requires: []
  optional: []
  variants: {\"claude\":\"variants/claude\",\"codex\":\"variants/codex\"}
---

# Pilot

Read `reference/harness.md` before provider-specific work.
""",
        )
        write(self.source / "reference" / "common.md", "shared\n")
        write(
            self.source / "variants" / "codex" / "reference" / "harness.md",
            "provider: codex\n",
        )
        write(
            self.source / "variants" / "claude" / "reference" / "harness.md",
            "provider: claude\n",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_catalog_materializes_self_contained_provider_trees(self) -> None:
        compiled = json.loads(run(CATALOG, "compile", "--root", self.root).stdout)
        pilot = compiled["skills"]["pilot"]
        self.assertEqual(compiled["schema_version"], 3)
        self.assertEqual(
            pilot["variants"],
            {"claude": "variants/claude", "codex": "variants/codex"},
        )

        codex = Path(self.temp.name) / "codex"
        record = json.loads(
            run(
                CATALOG,
                "materialize",
                "pilot",
                "--root",
                self.root,
                "--provider",
                "codex",
                "--output",
                codex,
            ).stdout
        )
        self.assertEqual((codex / "reference" / "harness.md").read_text(), "provider: codex\n")
        self.assertFalse((codex / "variants").exists())
        self.assertTrue(record["effective_hash"].startswith("sha256:"))
        self.assertTrue(record["source_revision"].startswith(("git:", "sha256:")))

    def test_overlay_cannot_change_shared_contract(self) -> None:
        write(self.source / "variants" / "codex" / "SKILL.md", "not allowed\n")
        result = run(CATALOG, "compile", "--root", self.root, ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("shared contract", result.stderr)

    def test_overlay_cannot_replace_setup_owner(self) -> None:
        write(
            self.source / "variants" / "claude" / "reference" / "setup.md",
            "not allowed\n",
        )
        result = run(CATALOG, "compile", "--root", self.root, ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("shared contract path reference/setup.md", result.stderr)

    def test_publish_and_audit_provider_mounts_and_provenance(self) -> None:
        lock = self.consumer / ".agents" / "asher-skills" / "variant-lock.json"
        published = json.loads(
            run(
                INSTALL,
                "publish-variant",
                "pilot",
                "--catalog-root",
                self.root,
                "--root",
                self.consumer,
                "--provider-root",
                "codex=.agents/skills",
                "--provider-root",
                "claude=.claude/skills",
                "--lock",
                lock,
            ).stdout
        )
        self.assertEqual(published["actions"], ["published:claude", "published:codex", "lock-updated"])
        self.assertFalse((self.consumer / ".claude" / "skills" / "pilot").is_symlink())
        self.assertEqual(
            (self.consumer / ".agents" / "skills" / "pilot" / "reference" / "harness.md").read_text(),
            "provider: codex\n",
        )
        self.assertEqual(
            (self.consumer / ".claude" / "skills" / "pilot" / "reference" / "harness.md").read_text(),
            "provider: claude\n",
        )
        locked = json.loads(lock.read_text())
        self.assertEqual(set(locked["skills"]["pilot"]["providers"]), {"claude", "codex"})

        repeat = json.loads(
            run(
                INSTALL,
                "publish-variant",
                "pilot",
                "--catalog-root",
                self.root,
                "--root",
                self.consumer,
                "--provider-root",
                "codex=.agents/skills",
                "--provider-root",
                "claude=.claude/skills",
                "--lock",
                lock,
            ).stdout
        )
        self.assertEqual(repeat["actions"], [])

        audit = json.loads(
            run(
                INSTALL,
                "audit-variant",
                "pilot",
                "--catalog-root",
                self.root,
                "--root",
                self.consumer,
                "--provider-root",
                "codex=.agents/skills",
                "--provider-root",
                "claude=.claude/skills",
                "--lock",
                lock,
            ).stdout
        )
        self.assertEqual(audit["findings"], [])

        bad_lock = json.loads(lock.read_text())
        bad_lock["skills"]["pilot"]["source"] = "skills/wrong/pilot"
        bad_lock["skills"]["pilot"]["providers"]["codex"]["mount"] = "wrong"
        lock.write_text(json.dumps(bad_lock), encoding="utf-8")
        bad_audit = json.loads(
            run(
                INSTALL,
                "audit-variant",
                "pilot",
                "--catalog-root",
                self.root,
                "--root",
                self.consumer,
                "--provider-root",
                "codex=.agents/skills",
                "--provider-root",
                "claude=.claude/skills",
                "--lock",
                lock,
            ).stdout
        )
        mismatches = [
            finding for finding in bad_audit["findings"]
            if finding["kind"] == "provider-lock-mismatch"
        ]
        self.assertEqual(
            {finding["provider"] for finding in mismatches}, {"shared-source", "codex"}
        )
        lock.write_text(json.dumps(locked), encoding="utf-8")

        write(
            self.consumer / ".claude" / "skills" / "pilot" / "reference" / "harness.md",
            "provider: codex\n",
        )
        audit = json.loads(
            run(
                INSTALL,
                "audit-variant",
                "pilot",
                "--catalog-root",
                self.root,
                "--root",
                self.consumer,
                "--provider-root",
                "codex=.agents/skills",
                "--provider-root",
                "claude=.claude/skills",
                "--lock",
                lock,
            ).stdout
        )
        kinds = {finding["kind"] for finding in audit["findings"]}
        self.assertIn("wrong-provider", kinds)
        self.assertIn("altered-tree-hash", kinds)

        write(
            self.consumer / ".agents" / "skills" / "pilot" / "SKILL.md",
            (self.source / "SKILL.md").read_text() + "\nprovider edit\n",
        )
        shutil.rmtree(self.consumer / ".claude" / "skills" / "pilot")
        audit = json.loads(
            run(
                INSTALL,
                "audit-variant",
                "pilot",
                "--catalog-root",
                self.root,
                "--root",
                self.consumer,
                "--provider-root",
                "codex=.agents/skills",
                "--provider-root",
                "claude=.claude/skills",
                "--lock",
                lock,
            ).stdout
        )
        kinds = {finding["kind"] for finding in audit["findings"]}
        self.assertIn("missing-provider-mount", kinds)
        self.assertIn("shared-contract-drift", kinds)

    def test_publication_rolls_back_all_providers_on_injected_failure(self) -> None:
        lock = self.consumer / ".agents" / "asher-skills" / "variant-lock.json"
        command = (
            INSTALL,
            "publish-variant",
            "pilot",
            "--catalog-root",
            self.root,
            "--root",
            self.consumer,
            "--provider-root",
            "codex=.agents/skills",
            "--provider-root",
            "claude=.claude/skills",
            "--lock",
            lock,
        )
        run(*command)
        old_lock = lock.read_bytes()
        old_codex = (
            self.consumer / ".agents" / "skills" / "pilot" / "reference" / "harness.md"
        ).read_bytes()
        old_claude = (
            self.consumer / ".claude" / "skills" / "pilot" / "reference" / "harness.md"
        ).read_bytes()
        write(
            self.source / "variants" / "codex" / "reference" / "harness.md",
            "provider: codex v2\n",
        )
        write(
            self.source / "variants" / "claude" / "reference" / "harness.md",
            "provider: claude v2\n",
        )
        env = dict(os.environ)
        env["ASHER_SKILLS_FAIL_AFTER_PROVIDER"] = "1"
        failed = run(*command, ok=False, env=env)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("injected provider publication failure", failed.stderr)
        self.assertEqual(lock.read_bytes(), old_lock)
        self.assertEqual(
            (self.consumer / ".agents" / "skills" / "pilot" / "reference" / "harness.md").read_bytes(),
            old_codex,
        )
        self.assertEqual(
            (self.consumer / ".claude" / "skills" / "pilot" / "reference" / "harness.md").read_bytes(),
            old_claude,
        )

    def test_legacy_primary_and_alias_convert_but_independent_alias_is_refused(self) -> None:
        primary = self.consumer / ".agents" / "skills" / "pilot"
        alias = self.consumer / ".claude" / "skills" / "pilot"
        shutil.copytree(self.source, primary)
        alias.parent.mkdir(parents=True)
        alias.symlink_to(Path("../../.agents/skills/pilot"))
        lock = self.consumer / ".agents" / "asher-skills" / "variant-lock.json"
        command = (
            INSTALL,
            "publish-variant",
            "pilot",
            "--catalog-root",
            self.root,
            "--root",
            self.consumer,
            "--provider-root",
            "codex=.agents/skills",
            "--provider-root",
            "claude=.claude/skills",
            "--lock",
            lock,
        )
        run(*command)
        self.assertTrue(primary.is_dir() and not primary.is_symlink())
        self.assertTrue(alias.is_dir() and not alias.is_symlink())

        other = Path(self.temp.name) / "unsafe-consumer"
        (other / ".claude" / "skills" / "pilot").mkdir(parents=True)
        unsafe_command = list(command)
        unsafe_command[unsafe_command.index(self.consumer)] = other
        unsafe_command[-1] = other / ".agents" / "asher-skills" / "variant-lock.json"
        failed = run(*unsafe_command, ok=False)
        self.assertIn("refusing undeclared independent provider directory", failed.stderr)
        self.assertFalse((other / ".agents" / "skills" / "pilot").exists())

    def test_unvaried_legacy_symlink_shape_remains_valid(self) -> None:
        primary = self.consumer / ".agents" / "skills" / "plain"
        alias = self.consumer / ".claude" / "skills" / "plain"
        primary.mkdir(parents=True)
        alias.parent.mkdir(parents=True)
        alias.symlink_to(Path("../../.agents/skills/plain"))
        state = json.loads(
            run(INSTALL, "inspect", "plain", "--root", self.consumer).stdout
        )
        self.assertEqual(state["primary"]["state"], "real-directory")
        self.assertEqual(state["aliases"][0]["state"], "correct-symlink")


if __name__ == "__main__":
    unittest.main()
