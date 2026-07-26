#!/usr/bin/env python3
"""Guard staffing's provider-variant harness isolation.

The point of compiling this skill per provider is **not** to ship less prose. It is that a
session must never be handed operating instructions written for the other harness. A Codex
session that reads "spawn a watched Agent/Workflow child" has been handed a tool it does not
have; a Claude session that reads the Codex thread-cap rules is being told to manage a
surface that does not exist for it. Both are worse than verbosity — they are instructions an
executor can actually try to follow.

So the isolation test below is the real guard. The size ratio is kept as corroborating
evidence that separation happened at all — a compiled tree that still carried both harnesses'
mechanics would not shrink — but it is a symptom, never the target. There is deliberately no
absolute byte ceiling: a cap invites trading away a needed sentence to satisfy a number, and
"is this instruction addressed to this harness?" is the question that matters, not "is it
short?".
"""

from __future__ import annotations

import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parent.parent
REPO = SKILL.parents[2]

MAX_SHARE_OF_UNIFIED = 0.8

# Instructions only a session of that harness could act on. Cross-harness *dispatch
# commands* are deliberately absent from these lists: the Claude file must describe
# `codex exec` and the Codex file must describe `claude -p`, because reaching the sibling is
# each one's own job. The direction labels ("Claude→Codex" / "Codex→Claude") ARE markers and
# belong here: each names the dispatch section written for one side — the Claude file heads
# its section "Claude→Codex", so that string in the *codex* path means a Claude-addressed
# section leaked, not that dispatch itself is forbidden. What may not leak is the other
# harness's native spawn vocabulary, config surface, and addressed sections.
CLAUDE_ONLY = (
    "Agent/Workflow",
    "`Agent` tool",
    "Monitor conditions",
    "~/.claude/",
    "Claude→Codex",
)
CODEX_ONLY = (
    "native agent threads",
    "config.toml",
    "thread cap",
    "full-history fork",
    "~/.codex/",
    "Codex→Claude",
)


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

    def seed_text(self, provider: str) -> str:
        # The seed is setup-time input, not part of the reconcile load — so it stays out of
        # loaded_text and the size ratio. But it ships per provider, which makes it a leak
        # surface: the isolation guard reads it alongside the loaded path.
        seed = (
            SKILL / "variants" / provider / "templates" / "seed" / "roster-seed.md"
            if (SKILL / "variants").is_dir()
            else SKILL / "templates" / "seed" / "roster-seed.md"
        )
        return seed.read_text(encoding="utf-8")

    def assert_no_foreign_instructions(self, provider: str, text: str, where: str) -> None:
        foreign = CODEX_ONLY if provider == "claude" else CLAUDE_ONLY
        for marker in foreign:
            with self.subTest(provider=provider, marker=marker):
                # assertNotIn would dump the whole document into the failure; a guard whose
                # output is 20KB of prose is one people stop reading.
                self.assertFalse(
                    marker in text,
                    f"{where}: the {provider} path carries {marker!r} — an instruction only "
                    f"a session of the other harness could act on",
                )

    def test_loaded_provider_path_carries_no_foreign_harness_instructions(self) -> None:
        """The guard: neither path hands a session the other harness's operating rules."""
        if not (SKILL / "variants").is_dir():
            self.skipTest("authoring tree only; the compiled case is covered below")
        for provider in ("claude", "codex"):
            self.assert_no_foreign_instructions(
                provider,
                self.loaded_text(provider) + "\n" + self.seed_text(provider),
                f"variants/{provider}",
            )

    def test_installed_mounts_carry_only_their_own_provider(self) -> None:
        """The same guard against the real build products — what a session actually reads.

        Mounts ship without `evals/`, so this cannot run from inside a compiled tree; it
        reaches the mounts from the authoring tree instead. That is the point: the compiled
        output is what a harness loads, and nothing else checks it for foreign instructions.
        """
        mounts = [p for p in (REPO / ".claude" / "skills" / "staffing",
                              REPO / ".agents" / "skills" / "staffing") if p.is_dir()]
        if not mounts:
            self.skipTest("staffing is not installed into this repo")
        for mount in mounts:
            identity = mount / "templates" / "seed" / "provider.txt"
            self.assertTrue(identity.is_file(), f"{mount.name} mount has no provider identity")
            provider = identity.read_text(encoding="utf-8").strip()
            harness = (mount / "reference" / "harness.md").read_text(encoding="utf-8")
            self.assertNotIn(
                "Provider mechanics placeholder",
                harness,
                f"{mount} still carries the placeholder — provider materialization did not run",
            )
            text = "\n".join(
                (mount / name).read_text(encoding="utf-8")
                for name in (
                    "SKILL.md",
                    "reference/install-and-reconcile.md",
                    "reference/harness.md",
                    "templates/seed/roster-seed.md",
                )
            )
            self.assert_no_foreign_instructions(provider, text, str(mount.relative_to(REPO)))

    def unified_bytes(self) -> int:
        """What one uncompiled skill carrying both harnesses' mechanics would load."""
        shared = (SKILL / "SKILL.md", SKILL / "reference" / "install-and-reconcile.md")
        both = (
            SKILL / "variants" / "claude" / "reference" / "harness.md",
            SKILL / "variants" / "codex" / "reference" / "harness.md",
        )
        parts = [p.read_text(encoding="utf-8") for p in (*shared, *both)]
        return len("\n".join(parts).encode("utf-8"))

    def test_compiling_per_provider_visibly_separates_the_mechanics(self) -> None:
        """Corroboration only: separation should be visible as a smaller load.

        A tree that still shipped both harnesses' mechanics could not clear this. It is not a
        prose budget — do not trim a needed instruction to satisfy it. If this fails while the
        isolation tests pass, the question is what stopped being separated, not what to cut.
        """
        if not (SKILL / "variants").is_dir():
            self.skipTest("compiled tree carries one provider; the ratio needs both")
        unified = self.unified_bytes()
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                loaded = len(self.loaded_text(provider).encode("utf-8"))
                self.assertLessEqual(loaded, unified * MAX_SHARE_OF_UNIFIED)


if __name__ == "__main__":
    unittest.main()
