#!/usr/bin/env python3
"""Structural checks for staffing-owned pointer/module templates."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COMMON = ROOT / "templates" / "global" / "staffing.common.md"
MEASUREMENTS = Path(__file__).with_name("token-measurements.json")


def provider_templates(provider: str) -> Path:
    return ROOT / "variants" / provider / "templates" / "global"


def compiled_copy(provider: str, destination: Path) -> Path:
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns("variants"))
    shutil.copytree(ROOT / "variants" / provider, destination, dirs_exist_ok=True)
    return destination


class GlobalStaffingTemplateTests(unittest.TestCase):
    def test_render_is_deterministic_and_provider_specific(self) -> None:
        common = COMMON.read_text().rstrip("\n")
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                source = (provider_templates(provider) / "staffing.module.md").read_text()
                self.assertEqual(source.count("{{COMMON}}"), 1)
                rendered = source.replace("{{COMMON}}", common)
                self.assertNotIn("{{", rendered)
                self.assertIn(common, rendered)
                self.assertIn("## Mechanics", rendered)

    def test_pointers_meet_character_and_optional_o200k_budgets(self) -> None:
        recorded = json.loads(MEASUREMENTS.read_text())
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                text = (provider_templates(provider) / "staffing-pointer.md").read_text()
                self.assertLessEqual(len(text.encode("utf-8")), 275)
                self.assertNotIn("@", text)
                self.assertIn(f"~/.{provider}/asher-skills/staffing.md", text)
                self.assertIn("then apply project deltas", text)
                self.assertIn("If unreadable, do not dispatch", text)
                self.assertIn("Otherwise do not load it", text)
                self.assertLessEqual(recorded[provider]["o200k_base_tokens"], 65)
                try:
                    import tiktoken  # type: ignore
                except ImportError:
                    continue
                measured = len(tiktoken.get_encoding("o200k_base").encode(text))
                self.assertEqual(measured, recorded[provider]["o200k_base_tokens"])

    def test_wrapper_never_owns_judgment_or_effect_verification(self) -> None:
        common = COMMON.read_text().rstrip("\n")
        for provider in ("claude", "codex"):
            rendered = (provider_templates(provider) / "staffing.module.md").read_text().replace(
                "{{COMMON}}", common
            )
            self.assertIn("The parent owns the prompt, judgment, and effect verification", rendered)
            self.assertIn("wrapper only supervises", rendered)

    def test_compiled_renderer_has_public_render_and_check_seam(self) -> None:
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                compiled = compiled_copy(provider, root / "staffing")
                render = compiled / "scripts" / "render-global.py"
                module = root / "module.md"
                pointer = root / "pointer.md"
                for command in ("render", "check"):
                    result = subprocess.run(
                        [sys.executable, str(render), command, "--module", str(module),
                         "--pointer", str(pointer)],
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                module.write_text("drift\n")
                result = subprocess.run(
                    [sys.executable, str(render), "check", "--module", str(module),
                     "--pointer", str(pointer)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("mismatch: module", result.stderr)


if __name__ == "__main__":
    unittest.main()
