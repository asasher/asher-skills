#!/usr/bin/env python3
"""Structural checks for setup-owned deferred presentation policy."""

from __future__ import annotations

import unittest
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GLOBAL = ROOT / "templates" / "global"
RENDER = ROOT / "scripts" / "render-global.py"


class GlobalPresentationTemplateTests(unittest.TestCase):
    def test_provider_pointers_are_sharp_bounded_and_fail_safe(self) -> None:
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                text = (GLOBAL / f"presentation-pointer.{provider}.md").read_text()
                self.assertLessEqual(len(text), 320)
                self.assertNotIn("@", text)
                self.assertIn(f"~/.{provider}/asher-skills/presentation.md", text)
                self.assertIn("If unreadable, open locally and do not publish", text)

    def test_module_is_self_contained_and_has_no_harness_branch(self) -> None:
        text = (GLOBAL / "presentation.common.md").read_text()
        self.assertIn("# Machine presentation policy", text)
        self.assertNotIn("~/.claude", text)
        self.assertNotIn("~/.codex", text)
        self.assertIn("Funnel stays off", text)

    def test_rendered_bytes_have_a_public_check_seam(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            module = Path(raw) / "presentation.md"
            pointer = Path(raw) / "pointer.md"
            for command in ("render", "check"):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(RENDER),
                        command,
                        "--provider",
                        "codex",
                        "--module",
                        str(module),
                        "--pointer",
                        str(pointer),
                    ],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            pointer.write_text("drift\n")
            result = subprocess.run(
                [
                    sys.executable, str(RENDER), "check", "--provider", "codex",
                    "--module", str(module), "--pointer", str(pointer),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("mismatch: pointer", result.stderr)


if __name__ == "__main__":
    unittest.main()
