#!/usr/bin/env python3
"""Inspect and import a secret-safe Lakebed dump into an Until Zero instance."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from runway_core import StateError, atomic_write_json, load_collection, load_json, sha256_file
from until_zero import ensure_no_outstanding_journals, instance_paths, now_iso, validate_targets, write_lock

TABLES = ("accounts", "rules", "events", "fxRates", "transactions", "settings", "ingestLog")
SECRET_MARKERS = ("token", "secret", "password", "credential", "authorization", "api_key", "apikey")
ALLOWED_FIELDS = {
    "accounts": {"id", "name", "kind", "currency", "balance_minor", "balance_as_of", "card_label", "statement_day", "due_day_offset", "due_day_of_month", "funding_account_id", "last4", "match_key", "match_keys", "archived"},
    "rules": {"id", "label", "account_id", "amount_minor", "currency", "cadence", "anchor_date_iso", "start_date_iso", "end_date_iso", "certainty", "order_index", "category", "active", "config", "ex_dates", "skip_ranges", "linked_event_id"},
    "events": {"id", "label", "account_id", "amount_minor", "currency", "date_iso", "certainty", "order_index", "category", "active", "linked_event_id"},
    "fxRates": {"id", "base", "quote", "rate", "as_of"},
    "transactions": {"id", "account_id", "date_iso", "amount_minor", "currency", "description", "category", "source", "status", "external_id", "queue_id", "last4", "card_label", "raw_json_sha256"},
    "settings": {"base_currency", "buffer_minor", "horizon_days"},
}


def is_secret_key(value: Any) -> bool:
    normalized = str(value).lower().replace("-", "_")
    return any(marker in normalized for marker in SECRET_MARKERS)


def strip_secrets(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: strip_secrets(child) for key, child in value.items() if not is_secret_key(key)}
    if isinstance(value, list):
        return [strip_secrets(child) for child in value]
    return value


def secret_field_paths(value: Any, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if is_secret_key(key):
                found.add(path)
            else:
                found.update(secret_field_paths(child, path))
    elif isinstance(value, list):
        for child in value:
            found.update(secret_field_paths(child, prefix))
    return found


def tables_from_dump(value: Any) -> dict[str, list[dict[str, Any]]]:
    source = value.get("tables", value) if isinstance(value, dict) else value
    output: dict[str, list[dict[str, Any]]] = {}
    if isinstance(source, dict):
        for name, rows in source.items():
            if isinstance(rows, list):
                output[str(name)] = [row for row in rows if isinstance(row, dict)]
    elif isinstance(source, list):
        for table in source:
            if isinstance(table, dict) and isinstance(table.get("name"), str) and isinstance(table.get("rows"), list):
                output[table["name"]] = [row for row in table["rows"] if isinstance(row, dict)]
    if not output:
        raise StateError("unrecognized Lakebed dump shape")
    return output


def owners(tables: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for table, rows in tables.items():
        for row in rows:
            owner = str(row.get("ownerId") or "")
            if owner:
                result.setdefault(owner, {})[table] = result.setdefault(owner, {}).get(table, 0) + 1
    return result


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def snake_row(table: str, row: dict[str, Any]) -> dict[str, Any]:
    mapping = {
        "accountId": "account_id", "amountMinor": "amount_minor", "balanceMinor": "balance_minor",
        "balanceAsOf": "balance_as_of", "cardLabel": "card_label", "dateISO": "date_iso",
        "externalId": "external_id", "fundingAccountId": "funding_account_id", "matchKey": "match_key",
        "statementDay": "statement_day", "dueDayOffset": "due_day_offset", "dueDayOfMonth": "due_day_of_month",
        "anchorDateISO": "anchor_date_iso", "startDateISO": "start_date_iso", "endDateISO": "end_date_iso",
        "linkedEventId": "linked_event_id", "orderIndex": "order_index", "baseCurrency": "base_currency",
        "bufferMinor": "buffer_minor", "horizonDays": "horizon_days", "asOf": "as_of",
    }
    output: dict[str, Any] = {}
    for key, value in row.items():
        if key in {"ownerId", "createdAt", "updatedAt"} or is_secret_key(key):
            continue
        if key == "configJson":
            try:
                parsed = json.loads(str(value or "{}"))
            except json.JSONDecodeError:
                parsed = {}
            output["config"] = strip_secrets(parsed) if isinstance(parsed, dict) else {}
        elif key == "exDatesJson":
            try:
                parsed = json.loads(str(value or "[]"))
            except json.JSONDecodeError:
                parsed = []
            output["ex_dates"] = strip_secrets(parsed) if isinstance(parsed, list) else []
        elif key == "skipRangesJson":
            try:
                parsed = json.loads(str(value or "[]"))
            except json.JSONDecodeError:
                parsed = []
            output["skip_ranges"] = strip_secrets(parsed) if isinstance(parsed, list) else []
        elif key == "rawJson":
            output["raw_json_sha256"] = hashlib.sha256(str(value or "").encode("utf-8")).hexdigest() if value else ""
        else:
            output[mapping.get(key, key)] = strip_secrets(value)
    if table == "rules":
        output.setdefault("config", {})
        output.setdefault("ex_dates", [])
        output.setdefault("skip_ranges", [])
    if table == "settings" and "horizon_days" in output:
        try:
            output["horizon_days"] = int(str(output["horizon_days"]))
        except ValueError as error:
            raise StateError("Lakebed settings horizonDays must be an integer") from error
    if table == "settings" and "buffer_minor" in output:
        output["buffer_minor"] = str(output["buffer_minor"])
    return {key: value for key, value in output.items() if key in ALLOWED_FIELDS.get(table, set())}


def selected_rows(tables: dict[str, list[dict[str, Any]]], table: str, owner: str) -> list[dict[str, Any]]:
    return [snake_row(table, row) for row in tables.get(table, []) if str(row.get("ownerId") or "") == owner]


def inspect_dump(tables: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    result = []
    for owner, counts in sorted(owners(tables).items(), key=lambda item: fingerprint(item[0])):
        settings = [row for row in tables.get("settings", []) if str(row.get("ownerId") or "") == owner]
        result.append({
            "owner_fingerprint": fingerprint(owner),
            "counts": {name: counts.get(name, 0) for name in TABLES},
            "has_ingest_token": any(bool(row.get("ingestToken")) for row in settings),
            "has_agent_token": any(bool(row.get("agentToken")) for row in settings),
            "secret_fields_detected": sorted({path for rows in tables.values() for row in rows if str(row.get("ownerId") or "") == owner for path in secret_field_paths(row)}),
        })
    return {"schema_version": 1, "owners": result, "secret_values_included": False}


def complete_import(instance: Path, state_dir: Path, journal: dict[str, Any]) -> dict[str, Any]:
    expected_hash = hashlib.sha256(json.dumps({key: value for key, value in journal.items() if key != "journal_hash"}, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n").hexdigest()
    if journal.get("journal_hash") != expected_hash:
        raise StateError("invalid migration journal hash")
    collections = journal.get("collections")
    config = journal.get("config")
    manifest = journal.get("manifest")
    if not isinstance(collections, dict) or set(collections) != {"accounts", "rules", "events", "fx_rates", "transactions"}:
        raise StateError("invalid migration journal collections")
    if not isinstance(config, dict) or not isinstance(manifest, dict):
        raise StateError("invalid migration journal metadata")
    for destination, document in collections.items():
        atomic_write_json(state_dir / f"{destination}.json", document)
    atomic_write_json(instance / "config.json", config)
    migration_dir = instance / "migration"
    migration_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(migration_dir / "lakebed-import.json", manifest)
    (state_dir / "migration-journal.json").unlink()
    return manifest


def import_owner(project: Path, instance_arg: str, dump_path: Path, tables: dict[str, list[dict[str, Any]]], owner: str) -> dict[str, Any]:
    instance, state_dir, config = instance_paths(project, instance_arg)
    available = owners(tables)
    if owner not in available:
        raise StateError("selected owner does not exist in the dump")
    collection_map = {
        "accounts": "accounts", "rules": "rules", "events": "events",
        "fxRates": "fx_rates", "transactions": "transactions",
    }
    source_hash = sha256_file(dump_path)
    owner_fingerprint = fingerprint(owner)
    journal_path = state_dir / "migration-journal.json"
    with write_lock(instance):
        ensure_no_outstanding_journals(state_dir, allow={"migration-journal.json"})
        if journal_path.exists():
            journal = load_json(journal_path)
            if not isinstance(journal, dict) or journal.get("source_sha256") != source_hash or journal.get("owner_fingerprint") != owner_fingerprint:
                raise StateError("an interrupted migration for a different source or owner requires manual recovery")
            return complete_import(instance, state_dir, journal)
        for destination in collection_map.values():
            if load_collection(state_dir, destination):
                raise StateError(f"refusing to import over non-empty {destination}.json")
        settings = selected_rows(tables, "settings", owner)
        if len(settings) != 1:
            raise StateError(f"selected owner must have exactly one settings row, found {len(settings)}")
        documents = {
            destination: {"schema_version": 1, "items": selected_rows(tables, source, owner)}
            for source, destination in collection_map.items()
        }
        imported = {destination: len(document["items"]) for destination, document in documents.items()}
        proposed_config = dict(config)
        proposed_config.update({key: settings[0][key] for key in ("base_currency", "buffer_minor", "horizon_days") if key in settings[0]})
        validate_targets(instance, state_dir, {**documents, "config": proposed_config})
        secret_fields = sorted({path for rows in tables.values() for row in rows if str(row.get("ownerId") or "") == owner for path in secret_field_paths(row)})
        manifest = {
            "schema_version": 1, "imported_at": now_iso(), "source_sha256": source_hash,
            "owner_fingerprint": owner_fingerprint, "counts": imported, "ingest_log": "not_imported",
            "secrets": "excluded", "secret_fields_excluded": secret_fields,
        }
        journal = {
            "schema_version": 1, "source_sha256": source_hash, "owner_fingerprint": owner_fingerprint,
            "collections": documents, "config": proposed_config, "manifest": manifest,
        }
        journal["journal_hash"] = hashlib.sha256(json.dumps(journal, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n").hexdigest()
        atomic_write_json(journal_path, journal, 0o600)
        return complete_import(instance, state_dir, journal)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inspect", "import"))
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--instance", default="until-zero")
    parser.add_argument("--owner")
    arguments = parser.parse_args(argv)
    try:
        dump = load_json(arguments.input)
        tables = tables_from_dump(dump)
        if arguments.command == "inspect":
            print(json.dumps(inspect_dump(tables), indent=2, sort_keys=True))
            return 0
        if not arguments.owner:
            raise StateError("import requires --owner after explicit inspection and selection")
        print(json.dumps(import_owner(arguments.project, arguments.instance, arguments.input, tables, arguments.owner), indent=2, sort_keys=True))
        return 0
    except (OSError, StateError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
