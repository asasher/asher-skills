#!/usr/bin/env python3
"""Compare normalized TypeScript and Python runway projection snapshots."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"snapshot must be an object: {path}")
    return value


def pick(value: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in value:
            return value[name]
    return None


def normalize(value: dict[str, Any]) -> dict[str, Any]:
    timeline = pick(value, "timeline") or []
    statements = pick(value, "card_statements", "cardStatements") or []
    return {
        "base_currency": pick(value, "base_currency", "baseCurrency"),
        "opening_balance": pick(value, "opening_balance", "startBalanceBase", "openingBalance"),
        "zero_dates": pick(value, "zero_dates", "zeroDates"),
        "card_statements": [
            {
                "account_id": pick(item, "account_id", "accountId"),
                "due_date_iso": pick(item, "due_date_iso", "dueDateISO", "due"),
                "total_base": pick(item, "total_base", "totalBase", "total"),
                "real_base": pick(item, "real_base", "realBase"),
            }
            for item in statements
        ],
        "timeline": [
            {
                "date_iso": pick(item, "date_iso", "dateISO", "date"),
                "label": pick(item, "label"),
                "delta_base": pick(item, "delta_base", "deltaBase", "change"),
                "balance": pick(item, "balance"),
                "kind": pick(item, "kind"),
                "source_id": pick(item, "source_id", "sourceId"),
            }
            for item in timeline
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--typescript", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        left = normalize(load(arguments.typescript))
        right = normalize(load(arguments.python))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if left != right:
        print(json.dumps({"match": False, "typescript": left, "python": right}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"match": True, "normalized": right}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
