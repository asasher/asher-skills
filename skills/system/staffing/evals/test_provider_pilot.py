#!/usr/bin/env python3
"""Guard staffing's provider-variant pilot budget and branch isolation."""

from __future__ import annotations

import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parent.parent
BASELINE_BYTES = 10_391  # pre-variant SKILL.md + unified install-and-reconcile.md


class StaffingProviderPilotTests(unittest.TestCase):
    def loaded_text(self, provider: str) -> str:
        author_overlay = SKILL / "variants" / provider / "reference" / "harness.md"
        compiled_overlay = SKILL / "reference" / "harness.md"
        paths = (
            SKILL / "SKILL.md",
            SKILL / "reference" / "install-and-reconcile.md",
            author_overlay if author_overlay.is_file() else compiled_overlay,
        )
        return "\n".join(path.read_text(encoding="utf-8") for path in paths)

    def test_each_provider_reduces_loaded_reconcile_text_by_twenty_percent(self) -> None:
        providers = ("claude", "codex") if (SKILL / "variants").is_dir() else ("compiled",)
        for provider in providers:
            with self.subTest(provider=provider):
                loaded = len(self.loaded_text(provider).encode("utf-8"))
                self.assertLessEqual(loaded, BASELINE_BYTES * 0.8)

    def test_loaded_provider_path_has_no_other_direction_branch(self) -> None:
        if not (SKILL / "variants").is_dir():
            self.assertNotIn("Provider mechanics placeholder", self.loaded_text("compiled"))
            return
        codex = self.loaded_text("codex")
        claude = self.loaded_text("claude")
        self.assertNotIn("Claude→Codex", codex)
        self.assertNotIn("~/.claude/", codex)
        self.assertNotIn("Codex→Claude", claude)
        self.assertNotIn("~/.codex/", claude)


if __name__ == "__main__":
    unittest.main()
