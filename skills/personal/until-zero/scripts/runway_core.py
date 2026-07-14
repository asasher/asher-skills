#!/usr/bin/env python3
"""Deterministic Until Zero state and projection primitives (stdlib only)."""

from __future__ import annotations

import calendar
import hashlib
import json
import math
import os
import re
import tempfile
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Iterable

BANDS = ("pessimistic", "expected", "optimistic")
COLLECTIONS = ("accounts", "rules", "events", "fx_rates", "transactions", "pending_captures")
CURRENCY_DECIMALS = {"AED": 2, "USD": 2, "EUR": 2, "GBP": 2, "INR": 2, "PKR": 2, "JPY": 0}
MAX_OCCURRENCES = 2000


class StateError(ValueError):
    """Raised when canonical state violates its public contract."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def atomic_write(path: Path, data: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_write_json(path: Path, value: Any, mode: int = 0o644) -> None:
    atomic_write(path, canonical_bytes(value), mode)


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n"
    descriptor = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
    try:
        os.write(descriptor, line.encode("utf-8"))
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def parse_iso(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise StateError(f"invalid ISO date: {value!r}") from error


def add_days(value: str, days: int) -> str:
    return (parse_iso(value) + timedelta(days=days)).isoformat()


def add_months(value: str, months: int) -> str:
    current = parse_iso(value)
    total = current.year * 12 + current.month - 1 + months
    year, month_index = divmod(total, 12)
    month = month_index + 1
    day = min(current.day, calendar.monthrange(year, month)[1])
    return date(year, month, day).isoformat()


def date_on_day(year: int, month: int, day: int) -> str:
    return date(year, month, min(max(1, day), calendar.monthrange(year, month)[1])).isoformat()


def parse_minor(value: Any) -> int:
    if isinstance(value, bool):
        raise StateError(f"invalid minor-unit amount: {value!r}")
    raw = str(value if value is not None else "0")
    if not re.fullmatch(r"-?\d+", raw):
        raise StateError(f"invalid minor-unit amount: {value!r}")
    return int(raw)


def decimals_for(currency: str) -> int:
    return CURRENCY_DECIMALS.get(str(currency or "").upper(), 2)


def format_minor(value: int, currency: str) -> str:
    decimals = decimals_for(currency)
    sign = "-" if value < 0 else ""
    absolute = abs(value)
    factor = 10**decimals
    whole, fraction = divmod(absolute, factor)
    suffix = f".{fraction:0{decimals}d}" if decimals else ""
    return f"{sign}{whole:,}{suffix}"


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise StateError(f"missing state file: {path}") from error
    except json.JSONDecodeError as error:
        raise StateError(f"invalid JSON in {path}: {error}") from error


def load_collection(state_dir: Path, name: str) -> list[dict[str, Any]]:
    if name not in COLLECTIONS:
        raise StateError(f"unknown collection: {name}")
    value = load_json(state_dir / f"{name}.json")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("items"), list):
        raise StateError(f"{name}.json must be a schema_version 1 object with an items array")
    if not all(isinstance(item, dict) for item in value["items"]):
        raise StateError(f"{name}.json items must be objects")
    return value["items"]


def state_hashes(state_dir: Path) -> dict[str, str]:
    hashes = {name: sha256_file(state_dir / f"{name}.json") for name in COLLECTIONS}
    config_path = state_dir.parent / "config.json"
    if config_path.exists():
        hashes["config"] = sha256_file(config_path)
    return hashes


def validate_semantics(state_dir: Path, config: dict[str, Any], *, allow_degraded_transactions: bool = False) -> None:
    def bounded_integer(value: Any, label: str, minimum: int, maximum: int) -> int:
        if isinstance(value, bool):
            raise StateError(f"{label} must be an integer from {minimum} to {maximum}")
        try:
            parsed = int(str(value))
        except (TypeError, ValueError) as error:
            raise StateError(f"{label} must be an integer from {minimum} to {maximum}") from error
        if str(parsed) != str(value) or not minimum <= parsed <= maximum:
            raise StateError(f"{label} must be an integer from {minimum} to {maximum}")
        return parsed

    base = str(config.get("base_currency") or "")
    if not re.fullmatch(r"[A-Z]{3}", base):
        raise StateError("config base_currency must be a three-letter uppercase code")
    parse_minor(config.get("buffer_minor", "0"))
    horizon = config.get("horizon_days")
    if isinstance(horizon, bool) or not isinstance(horizon, int) or not 1 <= horizon <= 3660:
        raise StateError("config horizon_days must be an integer from 1 to 3660")
    documents = {name: load_collection(state_dir, name) for name in COLLECTIONS}
    ids: dict[str, set[str]] = {}
    for name, items in documents.items():
        values = [str(item.get("id") or item.get("queue_id") or "") for item in items]
        if any(not value for value in values):
            raise StateError(f"{name} items require a non-empty id or queue_id")
        if len(values) != len(set(values)):
            raise StateError(f"{name} contains duplicate identifiers")
        ids[name] = set(values)
    account_ids = ids["accounts"]
    for account in documents["accounts"]:
        if account.get("kind") not in {"cash", "credit_card", "rail"}:
            raise StateError(f"account {account.get('id')} has invalid kind")
        currency = str(account.get("currency") or "")
        if not re.fullmatch(r"[A-Z]{3}", currency):
            raise StateError(f"account {account.get('id')} has invalid currency")
        parse_minor(account.get("balance_minor", "0"))
        if account.get("balance_as_of"):
            parse_iso(str(account["balance_as_of"]))
        funding = str(account.get("funding_account_id") or "")
        if funding and funding not in account_ids:
            raise StateError(f"account {account.get('id')} references missing funding account {funding}")
        if account.get("kind") == "credit_card":
            if account.get("statement_day") not in (None, ""):
                bounded_integer(account["statement_day"], f"account {account.get('id')} statement_day", 1, 31)
            if account.get("due_day_offset") not in (None, ""):
                bounded_integer(account["due_day_offset"], f"account {account.get('id')} due_day_offset", 0, 365)
            if account.get("due_day_of_month") not in (None, ""):
                bounded_integer(account["due_day_of_month"], f"account {account.get('id')} due_day_of_month", 1, 31)
    for collection in ("rules", "events", "transactions"):
        for item in documents[collection]:
            identifier = item.get("id")
            account = str(item.get("account_id") or "")
            if account not in account_ids:
                if collection != "transactions" or not allow_degraded_transactions:
                    raise StateError(f"{collection} item {identifier} references missing account {account}")
            currency = str(item.get("currency") or "")
            if not re.fullmatch(r"[A-Z]{3}", currency):
                raise StateError(f"{collection} item {identifier} has invalid currency")
            parse_minor(item.get("amount_minor"))
    for rule in documents["rules"]:
        if rule.get("cadence") not in {"weekly", "monthly", "quarterly", "yearly", "interval"}:
            raise StateError(f"rule {rule.get('id')} has invalid cadence")
        if rule.get("certainty", "expected") not in {"committed", "expected", "speculative"}:
            raise StateError(f"rule {rule.get('id')} has invalid certainty")
        for key in ("anchor_date_iso", "start_date_iso", "end_date_iso"):
            if rule.get(key):
                parse_iso(str(rule[key]))
        config_value = rule.get("config", {})
        if not isinstance(config_value, dict):
            raise StateError(f"rule {rule.get('id')} config must be an object")
        cadence = rule.get("cadence")
        if cadence in {"monthly", "quarterly"} and config_value.get("day_of_month") not in (None, ""):
            bounded_integer(config_value["day_of_month"], f"rule {rule.get('id')} day_of_month", 1, 31)
        if cadence == "yearly":
            if config_value.get("month") not in (None, ""):
                bounded_integer(config_value["month"], f"rule {rule.get('id')} month", 1, 12)
            if config_value.get("day_of_month") not in (None, ""):
                bounded_integer(config_value["day_of_month"], f"rule {rule.get('id')} day_of_month", 1, 31)
        if cadence in {"weekly", "interval"} and config_value.get("interval_days") not in (None, ""):
            bounded_integer(config_value["interval_days"], f"rule {rule.get('id')} interval_days", 1, 3660)
        ex_dates = rule.get("ex_dates", [])
        if not isinstance(ex_dates, list):
            raise StateError(f"rule {rule.get('id')} ex_dates must be an array")
        for excluded in ex_dates:
            parse_iso(str(excluded))
        ranges = rule.get("skip_ranges", [])
        if not isinstance(ranges, list) or not all(isinstance(window, dict) for window in ranges):
            raise StateError(f"rule {rule.get('id')} skip_ranges must be an array of objects")
        for window in ranges:
            start = str(window.get("from") or "")
            end = str(window.get("to") or "")
            parse_iso(start)
            parse_iso(end)
            if start > end:
                raise StateError(f"rule {rule.get('id')} skip range starts after it ends")
    for event in documents["events"]:
        parse_iso(str(event.get("date_iso") or ""))
        if event.get("certainty", "expected") not in {"committed", "expected", "speculative"}:
            raise StateError(f"event {event.get('id')} has invalid certainty")
    for transaction in documents["transactions"]:
        if transaction.get("date_iso"):
            parse_iso(str(transaction["date_iso"]))
        elif not allow_degraded_transactions:
            raise StateError(f"transaction {transaction.get('id')} requires date_iso")
        if transaction.get("status") not in {"uncleared", "cleared", "reconciled", "ignored"}:
            raise StateError(f"transaction {transaction.get('id')} has invalid status")
    for capture in documents["pending_captures"]:
        parse_iso(str(capture.get("date_iso") or ""))
        parse_minor(capture.get("amount_minor"))
        if not re.fullmatch(r"[A-Z]{3}", str(capture.get("currency") or "")):
            raise StateError(f"pending capture {capture.get('queue_id')} has invalid currency")
    for rate in documents["fx_rates"]:
        if not re.fullmatch(r"[A-Z]{3}", str(rate.get("base") or "")) or not re.fullmatch(r"[A-Z]{3}", str(rate.get("quote") or "")):
            raise StateError(f"FX rate {rate.get('id')} has invalid currencies")
        try:
            decimal_rate = Decimal(str(rate.get("rate")))
        except InvalidOperation as error:
            raise StateError(f"FX rate {rate.get('id')} has invalid rate") from error
        if not decimal_rate.is_finite() or decimal_rate <= 0:
            raise StateError(f"FX rate {rate.get('id')} must be positive and finite")
        if rate.get("as_of"):
            parse_iso(str(rate["as_of"]))


def _skip_date(rule: dict[str, Any], value: str) -> bool:
    if value in {str(item) for item in rule.get("ex_dates", []) if item}:
        return True
    for window in rule.get("skip_ranges", []):
        if isinstance(window, dict) and str(window.get("from", "")) <= value <= str(window.get("to", "")):
            return True
    return False


def expand_rule(rule: dict[str, Any], window_start: str, window_end: str) -> list[str]:
    anchor_raw = str(rule.get("anchor_date_iso") or "")
    if not anchor_raw:
        return []
    anchor = parse_iso(anchor_raw)
    start = max(window_start, str(rule.get("start_date_iso") or anchor_raw))
    end = min(window_end, str(rule.get("end_date_iso") or window_end))
    if start > end:
        return []
    config = rule.get("config") if isinstance(rule.get("config"), dict) else {}
    cadence = str(rule.get("cadence") or "monthly")
    output: list[str] = []

    if cadence in {"monthly", "quarterly"}:
        step = 3 if cadence == "quarterly" else 1
        day = int(config.get("day_of_month") or anchor.day)
        cursor = date(anchor.year, anchor.month, 1).isoformat()
        for _ in range(MAX_OCCURRENCES):
            current = parse_iso(cursor)
            candidate = date_on_day(current.year, current.month, day)
            if candidate > end:
                break
            if candidate >= start and not _skip_date(rule, candidate):
                output.append(candidate)
            cursor = add_months(cursor, step)
    elif cadence == "yearly":
        month = int(config.get("month") or anchor.month)
        day = int(config.get("day_of_month") or anchor.day)
        for year in range(parse_iso(start).year - 1, parse_iso(end).year + 2):
            candidate = date_on_day(year, month, day)
            if start <= candidate <= end and not _skip_date(rule, candidate):
                output.append(candidate)
    else:
        interval = int(config.get("interval_days") or (7 if cadence == "weekly" else 30))
        if interval <= 0:
            interval = 7 if cadence == "weekly" else 30
        candidate = anchor_raw
        for _ in range(MAX_OCCURRENCES):
            if candidate >= start:
                break
            candidate = add_days(candidate, interval)
        for _ in range(MAX_OCCURRENCES):
            if candidate > end:
                break
            if candidate >= start and not _skip_date(rule, candidate):
                output.append(candidate)
            candidate = add_days(candidate, interval)
    return output


def next_statement_close(value: str, statement_day: int) -> str:
    current = parse_iso(value)
    this_month = date_on_day(current.year, current.month, statement_day)
    if this_month >= value:
        return this_month
    next_month = parse_iso(add_months(date(current.year, current.month, 1).isoformat(), 1))
    return date_on_day(next_month.year, next_month.month, statement_day)


def statement_due_date(close_date: str, card: dict[str, Any]) -> str:
    day_of_month = int(str(card.get("due_day_of_month") or "0"))
    if day_of_month > 0:
        close = parse_iso(close_date)
        due = date_on_day(close.year, close.month, day_of_month)
        if due <= close_date:
            next_month = parse_iso(add_months(date(close.year, close.month, 1).isoformat(), 1))
            due = date_on_day(next_month.year, next_month.month, day_of_month)
        return due
    return add_days(close_date, int(str(card.get("due_day_offset") or "0")))


def _included(certainty: str, is_inflow: bool, band: str) -> bool:
    if band == "expected":
        return certainty != "speculative"
    if band == "pessimistic":
        return certainty == "committed" if is_inflow else True
    return True if is_inflow else certainty == "committed"


def _converter(base: str, rates: list[dict[str, Any]], warnings: list[str]):
    missing: set[str] = set()

    def convert(minor: int, source_currency: str) -> int:
        source = str(source_currency or base).upper()
        if source == base:
            return minor
        major = Decimal(minor) / (Decimal(10) ** decimals_for(source))
        direct = next((rate for rate in rates if str(rate.get("base", "")).upper() == base and str(rate.get("quote", "")).upper() == source), None)
        inverse = next((rate for rate in rates if str(rate.get("base", "")).upper() == source and str(rate.get("quote", "")).upper() == base), None)
        try:
            if direct and Decimal(str(direct.get("rate"))) != 0:
                converted = major / Decimal(str(direct["rate"]))
            elif inverse and Decimal(str(inverse.get("rate"))) != 0:
                converted = major * Decimal(str(inverse["rate"]))
            else:
                raise InvalidOperation
        except (InvalidOperation, KeyError):
            key = f"{source}->{base}"
            if key not in missing:
                missing.add(key)
                warnings.append(f"Missing FX rate {key}; treated 1:1")
            converted = major
        return int((converted * (Decimal(10) ** decimals_for(base))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    return convert


def cash_actual_counts_after_snapshot(transaction_date: str, snapshot: str, status: str) -> bool:
    return transaction_date > snapshot or (transaction_date == snapshot and status != "reconciled")


def project(state_dir: Path, config: dict[str, Any], today: str) -> dict[str, Any]:
    parse_iso(today)
    validate_semantics(state_dir, config, allow_degraded_transactions=True)
    accounts = load_collection(state_dir, "accounts")
    rules = load_collection(state_dir, "rules")
    events = load_collection(state_dir, "events")
    rates = load_collection(state_dir, "fx_rates")
    transactions = load_collection(state_dir, "transactions")
    warnings: list[str] = []
    base = str(config.get("base_currency") or "AED").upper()
    buffer_minor = parse_minor(config.get("buffer_minor", "0"))
    horizon_days = int(config.get("horizon_days") or 365)
    horizon = add_days(today, horizon_days)
    convert = _converter(base, rates, warnings)
    accounts_by_id = {str(account.get("id")): account for account in accounts}
    cards = [account for account in accounts if account.get("kind") == "credit_card" and not account.get("archived")]

    start_balance = sum(
        convert(parse_minor(account.get("balance_minor")), str(account.get("currency") or base))
        for account in accounts
        if account.get("kind") == "cash" and not account.get("archived")
    )

    def card_due(card: dict[str, Any], charge_date: str) -> str:
        statement_day = int(str(card.get("statement_day") or "0"))
        if statement_day <= 0:
            return charge_date
        return statement_due_date(next_statement_close(charge_date, statement_day), card)

    items: list[dict[str, Any]] = []
    for rule in rules:
        if not rule.get("active", True):
            continue
        for occurrence in expand_rule(rule, today, horizon):
            items.append({
                "date_iso": occurrence,
                "amount_minor": parse_minor(rule.get("amount_minor")),
                "currency": str(rule.get("currency") or base).upper(),
                "label": str(rule.get("label") or "Rule"),
                "category": str(rule.get("category") or ""),
                "certainty": str(rule.get("certainty") or "expected"),
                "account_id": str(rule.get("account_id") or ""),
                "order_index": int(rule.get("order_index") or 0),
                "source_id": str(rule.get("id") or ""),
                "kind": "rule",
            })
    for event in events:
        if not event.get("active", True):
            continue
        event_date = str(event.get("date_iso") or "")
        if not event_date or not today <= event_date <= horizon:
            continue
        items.append({
            "date_iso": event_date,
            "amount_minor": parse_minor(event.get("amount_minor")),
            "currency": str(event.get("currency") or base).upper(),
            "label": str(event.get("label") or "Event"),
            "category": str(event.get("category") or ""),
            "certainty": str(event.get("certainty") or "expected"),
            "account_id": str(event.get("account_id") or ""),
            "order_index": int(event.get("order_index") or 0),
            "source_id": str(event.get("id") or ""),
            "kind": "event",
        })

    for transaction in transactions:
        if transaction.get("status") == "ignored":
            continue
        account_id = str(transaction.get("account_id") or "")
        account = accounts_by_id.get(account_id)
        if account is None or account.get("archived"):
            warnings.append(f"Unmapped transaction {transaction.get('id', '')} excluded from projection")
            continue
        transaction_date = str(transaction.get("date_iso") or today)
        amount = parse_minor(transaction.get("amount_minor"))
        currency = str(transaction.get("currency") or base).upper()
        if account and account.get("kind") == "credit_card":
            due = card_due(account, transaction_date)
            if today <= due <= horizon:
                items.append({
                    "date_iso": transaction_date,
                    "amount_minor": amount,
                    "currency": currency,
                    "label": str(transaction.get("description") or "Card charge"),
                    "category": str(transaction.get("category") or ""),
                    "certainty": "committed",
                    "account_id": account_id,
                    "order_index": 0,
                    "source_id": str(transaction.get("id") or ""),
                    "kind": "actual",
                })
            continue
        snapshot = str(account.get("balance_as_of") or today) if account and account.get("kind") == "cash" else today
        if cash_actual_counts_after_snapshot(transaction_date, snapshot, str(transaction.get("status") or "uncleared")) and transaction_date <= today:
            start_balance += convert(amount, currency)
        elif today < transaction_date <= horizon:
            items.append({
                "date_iso": transaction_date,
                "amount_minor": amount,
                "currency": currency,
                "label": str(transaction.get("description") or "Actual"),
                "category": str(transaction.get("category") or ""),
                "certainty": "committed",
                "account_id": account_id,
                "order_index": 0,
                "source_id": str(transaction.get("id") or ""),
                "kind": "actual",
            })

    for card in cards:
        owed = parse_minor(card.get("balance_minor"))
        if not owed:
            continue
        when = str(card.get("balance_as_of") or today)
        if card_due(card, when) < today:
            when = today
        if today <= card_due(card, when) <= horizon:
            items.append({
                "date_iso": when,
                "amount_minor": -owed,
                "currency": str(card.get("currency") or base),
                "label": "Opening balance",
                "category": "Statement",
                "certainty": "committed",
                "account_id": str(card.get("id") or ""),
                "order_index": 0,
                "source_id": f"cardopen:{card.get('id')}",
                "kind": "actual",
            })

    def build_stream(band: str) -> dict[str, Any]:
        cash: list[dict[str, Any]] = []
        card_charges: dict[str, list[dict[str, Any]]] = {}
        for item in items:
            inflow = item["amount_minor"] > 0
            if not _included(item["certainty"], inflow, band):
                continue
            delta = convert(item["amount_minor"], item["currency"])
            account = accounts_by_id.get(item["account_id"])
            if account and account.get("kind") == "credit_card":
                card_charges.setdefault(item["account_id"], []).append({
                    "date_iso": item["date_iso"], "delta_base": delta, "label": item["label"],
                    "kind": item["kind"], "certainty": item["certainty"],
                })
            else:
                cash.append({**item, "delta_base": delta, "is_inflow": inflow})

        for card in cards:
            charges = card_charges.get(str(card.get("id")), [])
            buckets: dict[str, list[dict[str, Any]]] = {}
            for charge in charges:
                buckets.setdefault(card_due(card, charge["date_iso"]), []).append(charge)
            for due, components in buckets.items():
                components.sort(key=lambda component: component["date_iso"])
                total = sum(component["delta_base"] for component in components)
                cash.append({
                    "date_iso": due, "delta_base": total, "label": str(card.get("name") or "Card"),
                    "category": "Statement", "certainty": "committed", "account_id": str(card.get("id")),
                    "kind": "statement", "is_inflow": total > 0, "order_index": 0,
                    "source_id": f"stmt:{card.get('id')}:{due}", "components": components,
                })
        cash.sort(key=lambda item: (item["date_iso"], int(item.get("order_index") or 0), 0 if item["delta_base"] > 0 else 1))
        balance = start_balance
        zero_date = today if balance < buffer_minor else None
        entries = []
        points = [{"date_iso": today, "balance": balance}]
        for item in cash:
            balance += item["delta_base"]
            entry = {
                key: value for key, value in item.items()
                if key not in {"amount_minor", "currency"}
            }
            entry["balance"] = balance
            entries.append(entry)
            points.append({"date_iso": item["date_iso"], "balance": balance})
            if zero_date is None and balance < buffer_minor:
                zero_date = item["date_iso"]
        return {"entries": entries, "series": points, "zero_date": zero_date}

    streams = {band: build_stream(band) for band in BANDS}
    cash_accounts = [account for account in accounts if account.get("kind") == "cash" and not account.get("archived")]
    snapshot_balance = sum(convert(parse_minor(account.get("balance_minor")), str(account.get("currency") or base)) for account in cash_accounts)
    history_start = min((str(account.get("balance_as_of") or today) for account in cash_accounts), default=today)
    history_transactions = []
    for transaction in transactions:
        if transaction.get("status") == "ignored":
            continue
        account = accounts_by_id.get(str(transaction.get("account_id") or ""))
        if not account or account.get("kind") != "cash" or account.get("archived"):
            continue
        transaction_date = str(transaction.get("date_iso") or today)
        snapshot = str(account.get("balance_as_of") or today)
        if cash_actual_counts_after_snapshot(transaction_date, snapshot, str(transaction.get("status") or "uncleared")) and transaction_date <= today:
            history_transactions.append(transaction)
    history_transactions.sort(key=lambda transaction: (str(transaction.get("date_iso") or today), str(transaction.get("created_at") or "")))
    history = [{"date_iso": history_start, "balance": snapshot_balance}]
    past_entries = []
    history_balance = snapshot_balance
    for transaction in history_transactions:
        transaction_date = str(transaction.get("date_iso") or today)
        delta = convert(parse_minor(transaction.get("amount_minor")), str(transaction.get("currency") or base))
        history_balance += delta
        past_entries.append({
            "date_iso": transaction_date, "delta_base": delta,
            "label": str(transaction.get("description") or "Actual"),
            "category": str(transaction.get("category") or ""), "certainty": "committed",
            "account_id": str(transaction.get("account_id") or ""), "kind": "actual",
            "is_inflow": delta > 0, "balance": history_balance,
            "source_id": str(transaction.get("id") or ""), "order_index": 0,
        })
        history.append({"date_iso": transaction_date, "balance": history_balance})
    if history[-1]["date_iso"] != today:
        history.append({"date_iso": today, "balance": start_balance})

    speculative = []
    for item in items:
        if item.get("certainty") != "speculative":
            continue
        account = accounts_by_id.get(item.get("account_id"))
        if account and account.get("kind") == "credit_card":
            continue
        speculative.append({
            "date_iso": item["date_iso"], "delta_base": convert(item["amount_minor"], item["currency"]),
            "label": item["label"], "category": item["category"], "certainty": "speculative",
            "account_id": item["account_id"], "kind": item["kind"], "is_inflow": item["amount_minor"] > 0,
            "source_id": item["source_id"], "order_index": item["order_index"],
        })
    expected_statements = []
    for entry in streams["expected"]["entries"]:
        if entry["kind"] != "statement":
            continue
        real = [component for component in entry.get("components", []) if component.get("kind") == "actual"]
        expected_statements.append({
            "account_id": entry["account_id"],
            "name": str(accounts_by_id.get(entry["account_id"], {}).get("name") or entry["label"]),
            "due_date_iso": entry["date_iso"],
            "total_base": entry["delta_base"],
            "real_base": sum(component["delta_base"] for component in real),
            "count": len(real),
        })
    expected_statements.sort(key=lambda statement: (statement["due_date_iso"], statement["name"]))
    return {
        "schema_version": 1,
        "base_currency": base,
        "today_iso": today,
        "horizon_iso": horizon,
        "opening_balance": start_balance,
        "buffer_minor": buffer_minor,
        "zero_dates": {band: streams[band]["zero_date"] for band in BANDS},
        "timeline": streams["expected"]["entries"],
        "speculative": speculative,
        "history_start_iso": history_start,
        "history": history,
        "past_entries": past_entries,
        "series": {band: streams[band]["series"] for band in BANDS},
        "card_statements": expected_statements,
        "pending_capture_count": len(load_collection(state_dir, "pending_captures")),
        "warnings": warnings,
        "state_hashes": state_hashes(state_dir),
    }


def find_first_driver(projection: dict[str, Any]) -> dict[str, Any] | None:
    expected_zero = projection.get("zero_dates", {}).get("expected")
    timeline = projection.get("timeline", [])
    if expected_zero:
        candidates = [entry for entry in timeline if entry.get("date_iso") <= expected_zero and entry.get("delta_base", 0) < 0]
    else:
        candidates = [entry for entry in timeline if entry.get("delta_base", 0) < 0]
    return min(candidates, key=lambda entry: entry.get("delta_base", 0), default=None)


def ensure_no_non_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise StateError("non-finite number in output")
    if isinstance(value, dict):
        for child in value.values():
            ensure_no_non_finite(child)
    elif isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        for child in value:
            ensure_no_non_finite(child)
