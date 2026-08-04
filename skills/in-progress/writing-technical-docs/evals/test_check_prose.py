#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "check_prose.py"
SPEC = importlib.util.spec_from_file_location("check_prose", SCRIPT)
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECK
SPEC.loader.exec_module(CHECK)


class CheckProseTests(unittest.TestCase):
    def codes(self, text: str, max_words: int = 25) -> list[str]:
        return [finding.code for finding in CHECK.inspect_text(text, max_words)]

    def test_clean_short_prose_has_no_findings(self) -> None:
        self.assertEqual(self.codes("The server stores each response for five minutes."), [])

    def test_sentence_limit_is_configurable(self) -> None:
        text = "One two three four five six."
        self.assertIn("long-sentence", self.codes(text, max_words=5))
        self.assertNotIn("long-sentence", self.codes(text, max_words=6))

    def test_semicolon_is_an_error(self) -> None:
        findings = CHECK.inspect_text("Start the server; then open the page.", 25)
        self.assertEqual([(item.code, item.severity) for item in findings], [("semicolon", "error")])

    def test_code_fences_and_inline_code_are_ignored(self) -> None:
        text = "Use `robust; spin up` as the exact value.\n\n```sh\nrobust; spin up\n```"
        self.assertEqual(self.codes(text), [])

    def test_quoted_text_is_immutable(self) -> None:
        text = 'The UI shows "This robust; message has many words that the writer cannot change because it is an exact label."'
        self.assertEqual(self.codes(text, max_words=5), [])

    def test_frontmatter_is_ignored(self) -> None:
        text = "---\ndescription: Robust; powerful.\n---\nThe server starts."
        self.assertEqual(self.codes(text), [])

    def test_marketing_hedge_and_phrasal_verb_are_reported(self) -> None:
        text = "It is important to note that the robust tool can spin up a server."
        self.assertEqual(set(self.codes(text)), {"hedge", "phrasal-verb", "promotional-term"})

    def test_passive_contraction_and_dash_are_reported(self) -> None:
        text = "The file isn't saved — the worker was stopped."
        self.assertEqual(set(self.codes(text)), {"contraction", "passive-voice", "dash"})

    def test_possessive_is_not_a_contraction(self) -> None:
        self.assertNotIn("contraction", self.codes("The reader's task is clear."))

    def test_line_numbers_survive_code_fence_removal(self) -> None:
        text = "Clean text.\n```sh\nignored;\n```\nThe file was removed."
        findings = CHECK.inspect_text(text, 25)
        self.assertEqual([(item.code, item.line) for item in findings], [("passive-voice", 5)])

    def test_soft_wrapped_sentence_is_joined(self) -> None:
        first = "one two three four five six seven eight nine ten"
        second = "eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty."
        findings = CHECK.inspect_text(first + "\n" + second, 15)
        self.assertEqual([(item.code, item.line) for item in findings], [("long-sentence", 1)])

    def test_version_does_not_split_a_sentence(self) -> None:
        self.assertEqual(len(CHECK.split_sentences("Version 1.2.3 is current. Start the server.")), 2)

    def test_json_records_are_serializable(self) -> None:
        finding = CHECK.inspect_text("The robust tool works.", 25)[0]
        self.assertEqual(finding.code, "promotional-term")


if __name__ == "__main__":
    unittest.main()
