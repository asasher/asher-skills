#!/usr/bin/env python3
"""Focused tests for the Opportunity structural validator."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_opportunities.py"
SPEC = importlib.util.spec_from_file_location("validate_opportunities", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)

FIXTURES = Path(__file__).parent / "fixtures"


class OpportunityValidatorTests(unittest.TestCase):
    def fixture(self, name: str) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        shutil.copytree(FIXTURES / name, root, dirs_exist_ok=True)
        return temp, root

    def codes(self, root: Path) -> set[str]:
        return {issue.code for issue in validator.validate_workspace(root)}

    def test_valid_active_opportunity(self) -> None:
        _, root = self.fixture("valid-active")
        self.assertEqual(validator.validate_workspace(root), [])

    def test_accepts_opportunities_directory_as_input(self) -> None:
        _, root = self.fixture("valid-active")
        self.assertEqual(validator.validate_workspace(root / "Opportunities"), [])

    def test_rejects_unknown_stage(self) -> None:
        _, root = self.fixture("invalid-stage")
        self.assertIn("invalid-stage", self.codes(root))

    def test_rejects_unresolved_next_action(self) -> None:
        _, root = self.fixture("unresolved-next-action")
        self.assertIn("next-action-count", self.codes(root))

    def test_rejects_next_action_in_two_locations(self) -> None:
        _, root = self.fixture("duplicate-next-action")
        self.assertIn("next-action-count", self.codes(root))

    def test_closed_won_requires_reciprocal_project_and_path(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "Opportunities").mkdir()
        (root / "Projects").mkdir()
        delivery = root / "delivery"
        delivery.mkdir()
        (root / "Opportunities" / "Won Deal.md").write_text(
            textwrap.dedent(
                """\
                ---
                opportunity: Won Deal
                type: opportunity
                company: "[[Studio]]"
                customer: "[[Customer]]"
                owner: "[[Owner]]"
                stage: closed-won
                opened: 2026-07-01
                outcomeDate: 2026-07-12
                ---
                # Won Deal

                A won deal with delivery.

                ## Backlog

                None yet.

                ## Done

                None yet.

                ## Commercial

                Accepted.

                ## Decision Log

                - 2026-07-12 - Accepted.

                ## Events Log

                - 2026-07-12 - Client accepted.

                ## Projects

                - [[Won Delivery]] - implementation.

                ## Links

                None yet.
                """
            ),
            encoding="utf-8",
        )
        project = root / "Projects" / "Won Delivery.md"
        project.write_text(
            textwrap.dedent(
                f"""\
                ---
                project: Won Delivery
                sourceOpportunity: "[[Won Deal]]"
                localPath: {delivery}
                ---
                # Won Delivery
                """
            ),
            encoding="utf-8",
        )
        self.assertEqual(validator.validate_workspace(root), [])

        project.write_text(project.read_text().replace('sourceOpportunity: "[[Won Deal]]"\n', ""), encoding="utf-8")
        self.assertIn("missing-project-reciprocity", self.codes(root))

    def test_closed_won_without_delivery_requires_reason(self) -> None:
        _, root = self.fixture("valid-active")
        path = root / "Opportunities" / "Acme Renewal.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("stage: proposal", "stage: closed-won")
        text = text.replace("nextAction: aB3dE\n", "outcomeDate: 2026-07-13\n")
        text = text.replace("- [ ] Send client-safe renewal proposal 🆔 aB3dE", "None yet.")
        path.write_text(text, encoding="utf-8")
        self.assertIn("missing-win-delivery", self.codes(root))
        path.write_text(text.replace("outcomeDate: 2026-07-13\n", "outcomeDate: 2026-07-13\nnoDeliveryReason: Advisory only\n"), encoding="utf-8")
        self.assertEqual(validator.validate_workspace(root), [])


if __name__ == "__main__":
    unittest.main()
