#!/usr/bin/env python3
"""Golden assertions ported from the historical Until Zero TypeScript oracle."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from runway_core import add_months, expand_rule, format_minor, next_statement_close, project  # noqa: E402


def account(**values: object) -> dict[str, object]:
    return {"id": "a", "name": "Account", "kind": "cash", "currency": "AED", "balance_minor": "0", "balance_as_of": "", "archived": False, **values}


def rule(**values: object) -> dict[str, object]:
    return {"id": "r", "account_id": "", "label": "Rule", "amount_minor": "0", "currency": "AED", "category": "", "cadence": "monthly", "config": {}, "anchor_date_iso": "2026-01-01", "certainty": "committed", "active": True, **values}


def event(**values: object) -> dict[str, object]:
    return {"id": "e", "account_id": "", "date_iso": "2026-01-01", "amount_minor": "0", "currency": "AED", "label": "Event", "certainty": "committed", "active": True, **values}


def transaction(**values: object) -> dict[str, object]:
    return {"id": "t", "account_id": "", "date_iso": "2026-06-01", "amount_minor": "0", "currency": "AED", "description": "Actual", "status": "cleared", "source": "manual", **values}


class OracleTests(unittest.TestCase):
    def projection(self, *, today: str = "2026-04-28", horizon: int = 365, accounts=None, rules=None, events=None, rates=None, transactions=None, buffer="0") -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temporary:
            state = Path(temporary)
            values = {
                "accounts": accounts or [], "rules": rules or [], "events": events or [],
                "fx_rates": rates or [], "transactions": transactions or [], "pending_captures": [],
            }
            for name, items in values.items():
                (state / f"{name}.json").write_text(json.dumps({"schema_version": 1, "items": items}), encoding="utf-8")
            return project(state, {"base_currency": "AED", "buffer_minor": buffer, "horizon_days": horizon}, today)

    def test_money_dates_and_recurrence(self) -> None:
        self.assertEqual(format_minor(2943400, "AED"), "29,434.00")
        self.assertEqual(format_minor(-16900, "AED"), "-169.00")
        self.assertEqual(add_months("2026-01-31", 1), "2026-02-28")
        self.assertEqual(next_statement_close("2026-06-10", 24), "2026-06-24")
        self.assertEqual(next_statement_close("2026-06-25", 24), "2026-07-24")
        monthly = expand_rule(rule(cadence="monthly", anchor_date_iso="2026-01-28", config={"day_of_month": 28}), "2026-04-28", "2027-04-28")
        self.assertEqual(len(monthly), 13)
        self.assertEqual(monthly[0], "2026-04-28")
        quarterly = expand_rule(rule(cadence="quarterly", anchor_date_iso="2026-07-28", config={"day_of_month": 28}), "2026-04-28", "2027-04-28")
        self.assertEqual(quarterly, ["2026-07-28", "2026-10-28", "2027-01-28", "2027-04-28"])
        yearly = expand_rule(rule(cadence="yearly", anchor_date_iso="2025-08-01", config={"month": 8, "day_of_month": 1}), "2026-04-28", "2027-04-28")
        self.assertEqual(yearly, ["2026-08-01"])

    def test_credit_card_cycle_aggregation(self) -> None:
        cash = account(id="cash", balance_minor="10000000")
        card = account(id="citi", name="Citi", kind="credit_card", statement_day="24", due_day_offset="9", funding_account_id="cash")
        result = self.projection(today="2026-06-01", horizon=120, accounts=[cash, card], events=[
            event(id="e1", account_id="citi", date_iso="2026-06-10", amount_minor="-73500"),
            event(id="e2", account_id="citi", date_iso="2026-06-20", amount_minor="-73500"),
            event(id="e3", account_id="citi", date_iso="2026-06-26", amount_minor="-10000"),
        ])
        statements = [item for item in result["timeline"] if item["kind"] == "statement"]
        self.assertEqual(len(statements), 2)
        self.assertTrue(any(item["date_iso"] == "2026-07-03" and item["delta_base"] == -147000 for item in statements))
        self.assertTrue(any(item["date_iso"] == "2026-08-02" and item["delta_base"] == -10000 for item in statements))
        self.assertFalse(any(item["kind"] == "event" and item["account_id"] == "citi" for item in result["timeline"]))

    def test_certainty_zero_and_fx(self) -> None:
        cash = account(id="cash", balance_minor="1000000")
        result = self.projection(today="2026-06-01", horizon=60, accounts=[cash], events=[
            event(id="income", account_id="cash", date_iso="2026-06-10", amount_minor="500000", certainty="speculative"),
            event(id="spend", account_id="cash", date_iso="2026-06-15", amount_minor="-300000", certainty="speculative"),
        ])
        self.assertEqual(result["series"]["pessimistic"][-1]["balance"], 700000)
        self.assertEqual(result["series"]["expected"][-1]["balance"], 1000000)
        self.assertEqual(result["series"]["optimistic"][-1]["balance"], 1500000)
        zero = self.projection(today="2026-06-01", horizon=60, accounts=[account(id="cash", balance_minor="100000")], events=[event(account_id="cash", date_iso="2026-06-11", amount_minor="-200000")])
        self.assertEqual(zero["zero_dates"]["expected"], "2026-06-11")
        already_below = self.projection(today="2026-06-01", horizon=60, accounts=[account(id="cash", balance_minor="50")], buffer="100")
        self.assertEqual(already_below["zero_dates"]["expected"], "2026-06-01")
        fx = self.projection(today="2026-06-01", horizon=30, accounts=[account(id="cash")], events=[event(account_id="cash", date_iso="2026-06-10", amount_minor="-10000", currency="USD")], rates=[{"id": "f", "base": "AED", "quote": "USD", "rate": "0.27"}])
        self.assertLessEqual(abs(fx["timeline"][0]["delta_base"] - -37037), 1)

    def test_working_balance_and_history(self) -> None:
        cash = account(id="cash", balance_minor="1000000", balance_as_of="2026-06-20")
        result = self.projection(today="2026-06-29", horizon=60, accounts=[cash], transactions=[
            transaction(id="t1", account_id="cash", date_iso="2026-06-22", amount_minor="-34000", status="cleared"),
            transaction(id="t2", account_id="cash", date_iso="2026-06-15", amount_minor="-99900", status="reconciled"),
            transaction(id="t3", account_id="cash", date_iso="2026-06-25", amount_minor="-12000", status="uncleared"),
            transaction(id="t4", account_id="cash", date_iso="2026-06-26", amount_minor="-50000", status="ignored"),
        ])
        self.assertEqual(result["opening_balance"], 954000)
        self.assertEqual(result["history_start_iso"], "2026-06-20")
        self.assertEqual(result["history"][-1]["balance"], result["opening_balance"])
        self.assertEqual(len(result["past_entries"]), 2)
        self.assertEqual(result["past_entries"][-1]["balance"], 954000)

        same_day = self.projection(today="2026-06-29", horizon=30, accounts=[account(id="cash", balance_minor="100000", balance_as_of="2026-06-29")], transactions=[
            transaction(id="clear", account_id="cash", date_iso="2026-06-29", amount_minor="-10000", status="cleared"),
            transaction(id="unclear", account_id="cash", date_iso="2026-06-29", amount_minor="-5000", status="uncleared"),
            transaction(id="reconciled", account_id="cash", date_iso="2026-06-29", amount_minor="-7000", status="reconciled"),
        ])
        self.assertEqual(same_day["opening_balance"], 85000)
        self.assertNotIn("reconciled", [item["source_id"] for item in same_day["past_entries"]])

    def test_real_and_opening_card_balances(self) -> None:
        cash = account(id="cash", balance_minor="1000000", balance_as_of="2026-06-29")
        card = account(id="card", name="Card", kind="credit_card", statement_day="24", due_day_offset="9", funding_account_id="cash")
        result = self.projection(today="2026-06-29", horizon=90, accounts=[cash, card], transactions=[transaction(id="charge", account_id="card", date_iso="2026-06-24", amount_minor="-73500")])
        statement = result["timeline"][0]
        self.assertEqual((statement["date_iso"], statement["delta_base"]), ("2026-07-03", -73500))
        self.assertEqual(result["opening_balance"], 1000000)

        card.update({"statement_day": "16", "due_day_of_month": "3"})
        result = self.projection(today="2026-06-30", horizon=120, accounts=[cash, card], transactions=[
            transaction(id="a", account_id="card", date_iso="", amount_minor="-5300", status="uncleared"),
            transaction(id="b", account_id="card", date_iso="", amount_minor="-3075", status="uncleared"),
            transaction(id="c", account_id="card", date_iso="2026-06-28", amount_minor="-4250"),
        ])
        upcoming = result["card_statements"][0]
        self.assertEqual(upcoming["due_date_iso"], "2026-08-03")
        self.assertEqual(upcoming["total_base"], -12625)
        self.assertEqual(upcoming["real_base"], -12625)
        self.assertEqual(upcoming["count"], 3)
        self.assertEqual(len(result["timeline"][0]["components"]), 3)

        card["balance_minor"] = "50000"
        card["balance_as_of"] = "2026-06-30"
        opened = self.projection(today="2026-06-30", horizon=120, accounts=[account(id="cash", balance_minor="100000", balance_as_of="2026-06-29"), card], transactions=[transaction(account_id="card", date_iso="", amount_minor="-5300")])
        self.assertEqual(opened["card_statements"][0]["total_base"], -55300)
        self.assertEqual(opened["card_statements"][0]["real_base"], -55300)
        self.assertEqual(len(opened["timeline"][0]["components"]), 2)
        self.assertEqual(opened["opening_balance"], 100000)

        card["balance_as_of"] = "2026-01-01"
        stale = self.projection(today="2026-06-30", horizon=120, accounts=[account(id="cash", balance_minor="100000", balance_as_of="2026-06-29"), card])
        self.assertEqual(stale["card_statements"][0]["total_base"], -50000)
        self.assertGreaterEqual(stale["card_statements"][0]["due_date_iso"], "2026-06-30")

    def test_intraday_order_exceptions_and_unmapped_exclusion(self) -> None:
        cash = account(id="cash", balance_minor="200000", balance_as_of="2026-06-29")
        def ordered(income_order: int, spend_order: int) -> dict[str, object]:
            return self.projection(today="2026-06-29", horizon=30, accounts=[cash], events=[
                event(id="income", account_id="cash", date_iso="2026-07-10", amount_minor="100000", order_index=income_order),
                event(id="spend", account_id="cash", date_iso="2026-07-10", amount_minor="-300000", order_index=spend_order),
            ])
        income_first = ordered(0, 1)
        spend_first = ordered(1, 0)
        self.assertIsNone(income_first["zero_dates"]["expected"])
        self.assertEqual(spend_first["zero_dates"]["expected"], "2026-07-10")
        self.assertEqual(income_first["series"]["expected"][-1]["balance"], spend_first["series"]["expected"][-1]["balance"])

        occurrences = expand_rule(rule(anchor_date_iso="2026-06-01", ex_dates=["2026-07-01"], skip_ranges=[{"from": "2026-08-01", "to": "2026-09-01"}]), "2026-06-01", "2026-10-01")
        self.assertEqual(occurrences, ["2026-06-01", "2026-10-01"])
        unmapped = self.projection(today="2026-06-01", accounts=[account(id="cash", balance_minor="100000")], transactions=[transaction(id="unknown", account_id="", amount_minor="-50000")])
        self.assertEqual(unmapped["opening_balance"], 100000)
        self.assertTrue(any("Unmapped transaction unknown" in warning for warning in unmapped["warnings"]))


if __name__ == "__main__":
    unittest.main()
