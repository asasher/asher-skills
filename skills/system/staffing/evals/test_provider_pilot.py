#!/usr/bin/env python3
"""Guard staffing's provider-variant pilot budget and branch isolation."""

from __future__ import annotations

import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parent.parent

# The pilot's claim is that compiling per provider ships one harness's mechanics instead of
# both. That is a ratio, so the baseline is derived from the same files rather than frozen:
# a hardcoded byte count silently stops measuring the claim the moment content moves between
# files, which is exactly what happened when the roster's doctrine moved out of the
# home-directory module and into this skill.
MAX_SHARE_OF_UNIFIED = 0.8

# Absolute ceiling, so the ratio test cannot be satisfied by both sides growing together.
# Re-derive deliberately (and say why in the commit) rather than nudging it to pass.
CEILING_BYTES = 13_000  # claude 12,150 / codex 11,935 as of the sole-authority migration


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

    def unified_bytes(self) -> int:
        """What one uncompiled skill carrying both harnesses' mechanics would load."""
        shared = (SKILL / "SKILL.md", SKILL / "reference" / "install-and-reconcile.md")
        both = (
            SKILL / "variants" / "claude" / "reference" / "harness.md",
            SKILL / "variants" / "codex" / "reference" / "harness.md",
        )
        parts = [p.read_text(encoding="utf-8") for p in (*shared, *both)]
        return len("\n".join(parts).encode("utf-8"))

    def test_each_provider_reduces_loaded_reconcile_text_by_twenty_percent(self) -> None:
        if not (SKILL / "variants").is_dir():
            self.skipTest("compiled tree carries one provider; the ratio needs both")
        unified = self.unified_bytes()
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                loaded = len(self.loaded_text(provider).encode("utf-8"))
                self.assertLessEqual(loaded, unified * MAX_SHARE_OF_UNIFIED)
                self.assertLessEqual(loaded, CEILING_BYTES)

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
