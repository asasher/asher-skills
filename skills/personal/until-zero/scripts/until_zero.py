#!/usr/bin/env python3
"""Operate a consumer-owned Until Zero runway instance."""

from __future__ import annotations

import argparse
import copy
import fcntl
import html
import json
import os
import re
import sys
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from runway_core import (
    COLLECTIONS,
    StateError,
    append_jsonl,
    atomic_write_json,
    canonical_bytes,
    find_first_driver,
    format_minor,
    load_collection,
    load_json,
    parse_minor,
    parse_iso,
    project,
    sha256_bytes,
    sha256_file,
    state_hashes,
    validate_semantics,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def instance_paths(project_root: Path, instance_argument: str) -> tuple[Path, Path, dict[str, Any]]:
    project_root = project_root.resolve()
    relative = Path(instance_argument)
    if relative.is_absolute() or ".." in relative.parts:
        raise StateError("--instance must be a project-relative path")
    instance = (project_root / relative).resolve()
    if project_root not in instance.parents:
        raise StateError("--instance resolves outside the project")
    config = load_json(instance / "config.json")
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise StateError("run until-zero setup before using this command")
    return instance, instance / "state", config


@contextmanager
def write_lock(instance: Path) -> Iterator[None]:
    lock = instance / ".write-lock"
    descriptor = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise StateError(f"another Until Zero writer holds {lock}") from error
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def load_document(state_dir: Path, collection: str) -> dict[str, Any]:
    items = load_collection(state_dir, collection)
    return {"schema_version": 1, "items": items}


def editable_path(instance: Path, state_dir: Path, name: str) -> Path:
    return instance / "config.json" if name == "config" else state_dir / f"{name}.json"


def ensure_no_outstanding_journals(state_dir: Path, *, allow: set[str] | None = None) -> None:
    allowed = allow or set()
    for name in ("apply-journal.json", "capture-journal.json"):
        if name not in allowed and (state_dir / name).exists():
            raise StateError(f"outstanding {name}; complete its documented recovery before any other operation")


def load_editable_document(instance: Path, state_dir: Path, name: str) -> dict[str, Any]:
    if name == "config":
        value = load_json(instance / "config.json")
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise StateError("config.json must be a schema_version 1 object")
        return value
    return load_document(state_dir, name)


def apply_operations(documents: dict[str, dict[str, Any]], operations: list[dict[str, Any]]) -> None:
    for operation in operations:
        collection = operation["collection"]
        identifier = str(operation["id"])
        if collection == "config":
            documents[collection].update(copy.deepcopy(operation.get("set", {})))
            continue
        items = documents[collection]["items"]
        current = next((item for item in items if str(item.get("id")) == identifier), None)
        if current is None:
            if not operation.get("create"):
                raise StateError(f"{collection} item not found: {identifier}")
            current = {"id": identifier}
            items.append(current)
        current.update(copy.deepcopy(operation.get("set", {})))


def validate_targets(instance: Path, state_dir: Path, targets: dict[str, dict[str, Any]]) -> None:
    with tempfile.TemporaryDirectory() as temporary_name:
        root = Path(temporary_name)
        temporary_state = root / "state"
        temporary_state.mkdir()
        for collection in COLLECTIONS:
            document = targets.get(collection) or load_document(state_dir, collection)
            atomic_write_json(temporary_state / f"{collection}.json", document)
        config = targets.get("config") or load_json(instance / "config.json")
        atomic_write_json(root / "config.json", config)
        validate_semantics(temporary_state, config)


def document_hashes_after(state_dir: Path, targets: dict[str, dict[str, Any]]) -> dict[str, str]:
    hashes = state_hashes(state_dir)
    for name, document in targets.items():
        hashes[name] = sha256_bytes(canonical_bytes(document))
    return hashes


def append_audit_once(state_dir: Path, entry: dict[str, Any]) -> None:
    if any(item.get("id") == entry.get("id") for item in read_jsonl(state_dir / "audit.jsonl")):
        return
    append_jsonl(state_dir / "audit.jsonl", entry)


def capture_journal_hash(journal: dict[str, Any]) -> str:
    return sha256_bytes(canonical_bytes({key: value for key, value in journal.items() if key != "journal_hash"}))


def recover_capture_journal_locked(instance: Path, state_dir: Path) -> dict[str, Any] | None:
    journal_path = state_dir / "capture-journal.json"
    if not journal_path.exists():
        return None
    journal = load_json(journal_path)
    if not isinstance(journal, dict) or journal.get("schema_version") != 1 or journal.get("journal_hash") != capture_journal_hash(journal):
        raise StateError("invalid capture journal")
    targets = journal.get("targets")
    if not isinstance(targets, dict) or not targets or not set(targets).issubset({"transactions", "pending_captures"}):
        raise StateError("capture journal has invalid targets")
    for collection, document in targets.items():
        if not isinstance(document, dict) or document.get("schema_version") != 1 or not isinstance(document.get("items"), list):
            raise StateError(f"capture journal contains an invalid {collection} document")
        atomic_write_json(editable_path(instance, state_dir, collection), document)
    audit_entry = journal.get("audit")
    if not isinstance(audit_entry, dict) or not audit_entry.get("id"):
        raise StateError("capture journal has invalid audit metadata")
    append_audit_once(state_dir, audit_entry)
    journal_path.unlink()
    return journal


def commit_capture_mutation(instance: Path, state_dir: Path, action: str, actor: str, targets: dict[str, dict[str, Any]], **extra: Any) -> None:
    validate_targets(instance, state_dir, targets)
    before = state_hashes(state_dir)
    after = document_hashes_after(state_dir, targets)
    audit_entry = {
        "schema_version": 1, "id": str(uuid.uuid4()), "timestamp": now_iso(), "actor": actor,
        "action": action, "before_hashes": before, "after_hashes": after, **extra,
    }
    journal = {"schema_version": 1, "action": action, "targets": targets, "audit": audit_entry}
    journal["journal_hash"] = capture_journal_hash(journal)
    atomic_write_json(state_dir / "capture-journal.json", journal, 0o600)
    recover_capture_journal_locked(instance, state_dir)


def normalize_digits(value: Any) -> str:
    return "".join(character for character in str(value or "") if character.isdigit())[-8:]


def normalized_words(value: Any) -> str:
    return " ".join("".join(character.lower() if character.isalnum() else " " for character in str(value or "")).split())


def match_account(accounts: list[dict[str, Any]], capture: dict[str, Any]) -> dict[str, Any] | None:
    active = [account for account in accounts if not account.get("archived")]
    card = capture.get("card") if isinstance(capture.get("card"), dict) else {}
    last4 = normalize_digits(capture.get("last4") or card.get("last4"))
    label = str(capture.get("card_label") or card.get("label") or "")
    if last4:
        found = [account for account in active if normalize_digits(account.get("last4")) == last4]
        if len(found) == 1:
            return found[0]
        if len(found) > 1:
            return None
    normalized_label = normalized_words(label)
    if normalized_label:
        matched = []
        for account in active:
            raw_keys = account.get("match_keys", account.get("match_key", []))
            keys = raw_keys if isinstance(raw_keys, list) else str(raw_keys).split(",")
            if any(normalized_words(key) and f" {normalized_words(key)} " in f" {normalized_label} " for key in keys):
                matched.append(account)
        if len(matched) == 1:
            return matched[0]
        if len(matched) > 1:
            return None
        found = [account for account in active if normalized_words(account.get("name")) == normalized_label]
        if len(found) == 1:
            return found[0]
    return None


def normalize_capture(value: dict[str, Any]) -> dict[str, Any]:
    envelope = value.get("envelope") if isinstance(value.get("envelope"), dict) else value
    transaction = envelope.get("transaction") if isinstance(envelope.get("transaction"), dict) else envelope
    card = transaction.get("card") if isinstance(transaction.get("card"), dict) else {}
    queue_id = str(value.get("queue_id") or value.get("id") or "").strip()
    if not queue_id:
        raise StateError("capture requires queue_id or id")
    amount = str(transaction.get("amount_minor") or "")
    if not amount.lstrip("-").isdigit():
        raise StateError("capture amount_minor must be an integer string")
    currency = str(transaction.get("currency") or "").upper()
    if not re.fullmatch(r"[A-Z]{3}", currency):
        raise StateError("capture currency must be a three-letter code")
    date_iso = str(transaction.get("date_iso") or "")[:10]
    parse_iso(date_iso)
    return {
        "queue_id": queue_id,
        "received_at": str(value.get("received_at") or ""),
        "captured_at": str(envelope.get("captured_at") or ""),
        "amount_minor": amount,
        "currency": currency,
        "description": str(transaction.get("description") or "")[:240],
        "date_iso": date_iso,
        "external_id": str(transaction.get("external_id") or "")[:160],
        "category": str(transaction.get("category") or "")[:120],
        "last4": normalize_digits(transaction.get("last4") or card.get("last4")),
        "card_label": str(transaction.get("card_label") or card.get("label") or "")[:80],
        "raw": value,
    }


def ingest_capture(instance: Path, state_dir: Path, capture_value: dict[str, Any], actor: str) -> dict[str, Any]:
    capture = normalize_capture(capture_value)
    with write_lock(instance):
        ensure_no_outstanding_journals(state_dir, allow={"capture-journal.json"})
        recover_capture_journal_locked(instance, state_dir)
        accounts = load_collection(state_dir, "accounts")
        transactions = load_collection(state_dir, "transactions")
        pending = load_collection(state_dir, "pending_captures")
        if any(item.get("queue_id") == capture["queue_id"] for item in pending) or any(item.get("queue_id") == capture["queue_id"] for item in transactions):
            return {"ok": True, "queue_id": capture["queue_id"], "deduped": True}
        account = match_account(accounts, capture)
        if account is None:
            pending.append({**capture, "status": "needs_account"})
            targets = {"pending_captures": {"schema_version": 1, "items": pending}}
            outcome = {"ok": True, "queue_id": capture["queue_id"], "mapped": False}
        else:
            transaction = {
                "id": f"wallet:{capture['queue_id']}",
                "queue_id": capture["queue_id"],
                "account_id": str(account.get("id") or ""),
                "date_iso": capture["date_iso"],
                "amount_minor": capture["amount_minor"],
                "currency": capture["currency"] or str(account.get("currency") or "AED"),
                "description": capture["description"],
                "category": capture["category"],
                "source": "wallet",
                "status": "uncleared",
                "external_id": capture["external_id"],
                "last4": capture["last4"],
                "card_label": capture["card_label"],
            }
            transactions.append(transaction)
            targets = {"transactions": {"schema_version": 1, "items": transactions}}
            outcome = {"ok": True, "queue_id": capture["queue_id"], "mapped": True, "transaction_id": transaction["id"]}
        commit_capture_mutation(instance, state_dir, "ingest_capture", actor, targets, source_queue_id=capture["queue_id"], mapped=outcome["mapped"])
        return outcome


def assign_capture(instance: Path, state_dir: Path, queue_id: str, account_id: str, actor: str) -> dict[str, Any]:
    with write_lock(instance):
        ensure_no_outstanding_journals(state_dir, allow={"capture-journal.json"})
        recovered = recover_capture_journal_locked(instance, state_dir)
        pending = load_collection(state_dir, "pending_captures")
        accounts = load_collection(state_dir, "accounts")
        transactions = load_collection(state_dir, "transactions")
        if recovered and recovered.get("action") == "assign_capture" and recovered.get("audit", {}).get("source_queue_id") == queue_id:
            transaction = next((item for item in transactions if item.get("queue_id") == queue_id), None)
            if transaction:
                return transaction
        account = next((item for item in accounts if item.get("id") == account_id and not item.get("archived")), None)
        if account is None:
            raise StateError(f"active account not found: {account_id}")
        capture = next((item for item in pending if item.get("queue_id") == queue_id), None)
        if capture is None:
            raise StateError(f"pending capture not found: {queue_id}")
        if any(item.get("queue_id") == queue_id for item in transactions):
            pending = [item for item in pending if item.get("queue_id") != queue_id]
            commit_capture_mutation(instance, state_dir, "repair_capture_assignment", actor, {
                "pending_captures": {"schema_version": 1, "items": pending},
            }, source_queue_id=queue_id)
            return next(item for item in transactions if item.get("queue_id") == queue_id)
        transaction = {
            "id": f"wallet:{queue_id}", "queue_id": queue_id, "account_id": account_id,
            "date_iso": capture.get("date_iso", ""), "amount_minor": capture.get("amount_minor", "0"),
            "currency": capture.get("currency") or account.get("currency", "AED"),
            "description": capture.get("description", ""), "category": capture.get("category", ""),
            "source": "wallet", "status": "uncleared", "external_id": capture.get("external_id", ""),
            "last4": capture.get("last4", ""), "card_label": capture.get("card_label", ""),
        }
        transactions.append(transaction)
        pending = [item for item in pending if item.get("queue_id") != queue_id]
        commit_capture_mutation(instance, state_dir, "assign_capture", actor, {
            "transactions": {"schema_version": 1, "items": transactions},
            "pending_captures": {"schema_version": 1, "items": pending},
        }, source_queue_id=queue_id, transaction_id=transaction["id"])
        return transaction


def proposal_payload(changes: dict[str, Any], actor: str, before_hashes: dict[str, str]) -> dict[str, Any]:
    operations = changes.get("operations")
    if not isinstance(operations, list):
        raise StateError("changes must contain an operations array")
    if not operations:
        raise StateError("changes must contain at least one operation")
    for operation in operations:
        if not isinstance(operation, dict) or operation.get("collection") not in {*COLLECTIONS[:-1], "config"}:
            raise StateError("each operation requires an editable collection")
        if not str(operation.get("id") or ""):
            raise StateError("each operation requires an id")
        if not isinstance(operation.get("set", {}), dict):
            raise StateError("operation set must be an object")
        if "id" in operation.get("set", {}) and str(operation["set"]["id"]) != str(operation["id"]):
            raise StateError("an operation cannot change item identity")
        if operation.get("collection") == "config":
            if operation.get("id") != "settings" or operation.get("create"):
                raise StateError("config operations must update the settings document")
            disallowed = set(operation.get("set", {})) - {"base_currency", "buffer_minor", "horizon_days"}
            if disallowed:
                raise StateError(f"config operation contains disallowed fields: {', '.join(sorted(disallowed))}")
            settings = operation.get("set", {})
            if "base_currency" in settings and not re.fullmatch(r"[A-Z]{3}", str(settings["base_currency"])):
                raise StateError("config base_currency must be a three-letter uppercase code")
            if "buffer_minor" in settings and not re.fullmatch(r"-?\d+", str(settings["buffer_minor"])):
                raise StateError("config buffer_minor must be an integer string")
            if "horizon_days" in settings and (isinstance(settings["horizon_days"], bool) or not isinstance(settings["horizon_days"], int) or not 1 <= settings["horizon_days"] <= 3660):
                raise StateError("config horizon_days must be an integer from 1 to 3660")
    return {
        "schema_version": 1,
        "id": str(uuid.uuid4()),
        "created_at": now_iso(),
        "actor": actor,
        "status": "proposed",
        "before_hashes": before_hashes,
        "operations": operations,
        "note": str(changes.get("note") or ""),
    }


def proposal_content_hash(proposal: dict[str, Any]) -> str:
    content = {key: value for key, value in proposal.items() if key != "content_hash"}
    return sha256_bytes(canonical_bytes(content))


def validate_proposal_source(proposal: dict[str, Any]) -> None:
    if "source" not in proposal:
        return
    source = proposal["source"]
    allowed = {"kind", "statement_id", "statement_hash", "account_id", "as_of"}
    if not isinstance(source, dict) or source.get("kind") != "statement" or set(source) != allowed:
        raise StateError("proposal source must be exact non-secret statement provenance")
    if not re.fullmatch(r"[0-9a-f]{64}", str(source.get("statement_hash") or "")):
        raise StateError("statement source requires a SHA-256 hash")


def validate_proposal_semantics(
    instance: Path,
    state_dir: Path,
    proposal: dict[str, Any],
    base_documents: dict[str, dict[str, Any]] | None = None,
) -> dict[str, dict[str, Any]]:
    validate_proposal_source(proposal)
    operations = proposal.get("operations")
    if not isinstance(operations, list) or not operations:
        raise StateError("proposal requires operations")
    proposal_payload({"operations": operations}, str(proposal.get("actor") or "validation"), proposal.get("before_hashes", {}))
    changed = sorted({operation["collection"] for operation in operations})
    bases = copy.deepcopy(base_documents) if base_documents is not None else {
        name: load_editable_document(instance, state_dir, name) for name in changed
    }
    if set(bases) != set(changed):
        raise StateError("proposal base documents do not match its operations")
    if document_hashes_after(state_dir, bases) != proposal.get("before_hashes"):
        raise StateError("canonical state changed after proposal creation; create a fresh proposal")
    targets = copy.deepcopy(bases)
    apply_operations(targets, operations)
    validate_targets(instance, state_dir, targets)
    preview = proposal.get("preview")
    if not isinstance(preview, dict) or not isinstance(preview.get("today_iso"), str):
        raise StateError("proposal requires an exact preview")
    today = parse_iso(preview["today_iso"]).isoformat()
    expected = {
        "today_iso": today,
        "before": projection_summary(project_targets(instance, state_dir, bases, today)),
        "after": projection_summary(project_targets(instance, state_dir, targets, today)),
    }
    if canonical_bytes(preview) != canonical_bytes(expected):
        raise StateError("proposal preview does not match its operations")
    return targets


def projection_summary(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "opening_balance": value["opening_balance"],
        "zero_dates": value["zero_dates"],
        "card_statements": value["card_statements"],
        "pending_capture_count": value["pending_capture_count"],
        "warnings": value["warnings"],
    }


def project_targets(instance: Path, state_dir: Path, targets: dict[str, dict[str, Any]], today: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as temporary_name:
        root = Path(temporary_name)
        temporary_state = root / "state"
        temporary_state.mkdir()
        for collection in COLLECTIONS:
            atomic_write_json(temporary_state / f"{collection}.json", targets.get(collection) or load_document(state_dir, collection))
        config = targets.get("config") or load_json(instance / "config.json")
        atomic_write_json(root / "config.json", config)
        return project(temporary_state, config, today)


def create_proposal(instance: Path, state_dir: Path, changes: dict[str, Any], actor: str, today: str) -> dict[str, Any]:
    with write_lock(instance):
        ensure_no_outstanding_journals(state_dir)
        if changes.get("unresolved"):
            raise StateError("resolve every ambiguous statement row before creating a proposal")
        proposal = proposal_payload(changes, actor, state_hashes(state_dir))
        changed = sorted({operation["collection"] for operation in proposal["operations"]})
        targets = {name: load_editable_document(instance, state_dir, name) for name in changed}
        apply_operations(targets, proposal["operations"])
        validate_targets(instance, state_dir, targets)
        proposal["preview"] = {
            "today_iso": parse_iso(today).isoformat(),
            "before": projection_summary(project(state_dir, load_json(instance / "config.json"), today)),
            "after": projection_summary(project_targets(instance, state_dir, targets, today)),
        }
        if "source" in changes:
            proposal["source"] = copy.deepcopy(changes["source"])
            validate_proposal_source(proposal)
        proposal["content_hash"] = proposal_content_hash(proposal)
        path = instance / "proposals" / f"{proposal['id']}.json"
        atomic_write_json(path, proposal)
        return {"id": proposal["id"], "content_hash": proposal["content_hash"], "path": str(path), "preview": proposal["preview"]}


def statement_changes(instance: Path, state_dir: Path, statement: dict[str, Any], tolerance_days: int) -> dict[str, Any]:
    if statement.get("schema_version") != 1:
        raise StateError("statement must be a schema_version 1 object")
    statement_id = str(statement.get("id") or "")
    account_id = str(statement.get("account_id") or "")
    if not re.fullmatch(r"[A-Za-z0-9._:-]+", statement_id):
        raise StateError("statement id must contain only letters, numbers, dot, underscore, colon, or dash")
    accounts = load_collection(state_dir, "accounts")
    account = next((item for item in accounts if str(item.get("id")) == account_id and not item.get("archived")), None)
    if account is None:
        raise StateError(f"active account not found: {account_id}")
    as_of = parse_iso(str(statement.get("as_of") or "")).isoformat()
    currency = str(statement.get("currency") or account.get("currency") or "").upper()
    if not re.fullmatch(r"[A-Z]{3}", currency):
        raise StateError("statement currency must be a three-letter uppercase code")
    if not 0 <= tolerance_days <= 31:
        raise StateError("statement tolerance must be from 0 to 31 days")
    rows = statement.get("rows")
    if not isinstance(rows, list):
        raise StateError("statement rows must be an array")
    transactions = [item for item in load_collection(state_dir, "transactions") if str(item.get("account_id")) == account_id and item.get("status") != "ignored"]
    operations: list[dict[str, Any]] = []
    matched: list[dict[str, str]] = []
    created: list[dict[str, str]] = []
    unresolved: list[dict[str, Any]] = []
    used: set[str] = set()
    row_ids: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise StateError("statement rows must be objects")
        row_id = str(row.get("id") or "")
        if not re.fullmatch(r"[A-Za-z0-9._:-]+", row_id) or row_id in row_ids:
            raise StateError("statement row ids must be unique safe identifiers")
        row_ids.add(row_id)
        row_date = parse_iso(str(row.get("date_iso") or ""))
        amount = str(parse_minor(row.get("amount_minor")))
        external_id = str(row.get("external_id") or "")[:160]
        candidates = []
        if external_id:
            candidates = [item for item in transactions if str(item.get("external_id") or "") == external_id and str(item.get("id")) not in used]
        if not candidates:
            candidates = [
                item for item in transactions
                if str(item.get("id")) not in used
                and str(parse_minor(item.get("amount_minor"))) == amount
                and abs((parse_iso(str(item.get("date_iso") or "")) - row_date).days) <= tolerance_days
            ]
        if len(candidates) > 1:
            unresolved.append({"row_id": row_id, "reason": "ambiguous", "candidate_ids": sorted(str(item.get("id")) for item in candidates)})
            continue
        if len(candidates) == 1:
            transaction_id = str(candidates[0]["id"])
            used.add(transaction_id)
            update = {"status": "reconciled"}
            if external_id:
                update["external_id"] = external_id
            operations.append({"collection": "transactions", "id": transaction_id, "set": update})
            matched.append({"row_id": row_id, "transaction_id": transaction_id})
            continue
        transaction_id = f"statement:{statement_id}:{row_id}"
        operations.append({
            "collection": "transactions", "id": transaction_id, "create": True,
            "set": {
                "account_id": account_id, "date_iso": row_date.isoformat(), "amount_minor": amount,
                "currency": currency, "description": str(row.get("description") or "")[:240],
                "source": "statement", "status": "reconciled", "external_id": external_id,
            },
        })
        created.append({"row_id": row_id, "transaction_id": transaction_id})
    if "balance_minor" in statement:
        operations.append({
            "collection": "accounts", "id": account_id,
            "set": {"balance_minor": str(parse_minor(statement["balance_minor"])), "balance_as_of": as_of},
        })
    source = {
        "kind": "statement", "statement_id": statement_id,
        "statement_hash": sha256_bytes(canonical_bytes(statement)), "account_id": account_id, "as_of": as_of,
    }
    return {
        "note": f"Reconcile statement {statement_id}", "source": source, "operations": operations,
        "matched": matched, "created": created, "unresolved": unresolved,
    }


def read_proposal(instance: Path, proposal_id: str) -> tuple[Path, dict[str, Any], str]:
    if not proposal_id or any(character not in "0123456789abcdef-" for character in proposal_id.lower()):
        raise StateError("invalid proposal id")
    path = instance / "proposals" / f"{proposal_id}.json"
    proposal = load_json(path)
    if not isinstance(proposal, dict) or proposal.get("id") != proposal_id:
        raise StateError("invalid proposal document")
    expected = proposal_content_hash(proposal)
    if proposal.get("content_hash") != expected:
        raise StateError("proposal content hash mismatch")
    return path, proposal, sha256_file(path)


def approve_proposal(instance: Path, state_dir: Path, proposal_id: str, actor: str) -> dict[str, Any]:
    with write_lock(instance):
        ensure_no_outstanding_journals(state_dir)
        path, proposal, file_hash = read_proposal(instance, proposal_id)
        validate_proposal_semantics(instance, state_dir, proposal)
        approval = {
            "schema_version": 1, "id": str(uuid.uuid4()), "proposal_id": proposal_id,
            "proposal_content_hash": proposal["content_hash"], "proposal_file_hash": file_hash,
            "actor": actor, "approved_at": now_iso(), "proposal_path": str(path),
        }
        append_jsonl(state_dir / "approvals.jsonl", approval)
        return approval


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    output = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise StateError(f"invalid JSONL at {path}:{number}") from error
        if not isinstance(value, dict):
            raise StateError(f"JSONL row at {path}:{number} must be an object")
        output.append(value)
    return output


def apply_proposal(instance: Path, state_dir: Path, proposal_id: str, actor: str) -> dict[str, Any]:
    with write_lock(instance):
        ensure_no_outstanding_journals(state_dir)
        path, proposal, file_hash = read_proposal(instance, proposal_id)
        documents = validate_proposal_semantics(instance, state_dir, proposal)
        approvals = read_jsonl(state_dir / "approvals.jsonl")
        approval = next((item for item in reversed(approvals) if item.get("proposal_id") == proposal_id and item.get("proposal_content_hash") == proposal["content_hash"] and item.get("proposal_file_hash") == file_hash), None)
        if approval is None:
            raise StateError("no matching approval for the current proposal hash")
        before = state_hashes(state_dir)
        if any(before.get(name) != digest for name, digest in proposal.get("before_hashes", {}).items()):
            raise StateError("canonical state changed after proposal creation; create a fresh proposal")
        before_documents = {name: load_editable_document(instance, state_dir, name) for name in documents}
        expected_after = document_hashes_after(state_dir, documents)
        audit_entry = {
            "schema_version": 1, "id": str(uuid.uuid4()), "timestamp": now_iso(), "actor": actor,
            "action": "apply_proposal", "before_hashes": before, "after_hashes": expected_after,
            "proposal_id": proposal_id, "approval_id": approval["id"],
        }
        if isinstance(proposal.get("source"), dict):
            audit_entry["source"] = copy.deepcopy(proposal["source"])
        journal = {
            "schema_version": 1, "proposal_id": proposal_id,
            "before_documents": before_documents,
            "targets": documents,
            "audit": audit_entry,
        }
        journal_path = state_dir / "apply-journal.json"
        atomic_write_json(journal_path, journal, 0o600)
        for collection, document in journal["targets"].items():
            atomic_write_json(editable_path(instance, state_dir, collection), document)
        after = state_hashes(state_dir)
        if after != expected_after:
            raise StateError("proposal apply did not produce the expected state hashes")
        append_audit_once(state_dir, audit_entry)
        journal_path.unlink(missing_ok=True)
        return {"ok": True, "proposal_id": proposal_id, "approval_id": approval["id"], "after_hashes": after, "proposal_path": str(path)}


def recover_proposal(instance: Path, state_dir: Path, proposal_id: str, actor: str) -> dict[str, Any]:
    journal_path = state_dir / "apply-journal.json"
    with write_lock(instance):
        ensure_no_outstanding_journals(state_dir, allow={"apply-journal.json"})
        journal = load_json(journal_path)
        if not isinstance(journal, dict) or journal.get("schema_version") != 1:
            raise StateError("invalid apply journal")
        if journal.get("proposal_id") != proposal_id:
            raise StateError("apply journal does not match the requested proposal")
        targets = journal.get("targets")
        before_documents = journal.get("before_documents")
        if not isinstance(targets, dict) or not targets or not isinstance(before_documents, dict) or set(targets) != set(before_documents):
            raise StateError("apply journal has no targets")
        for collection, document in targets.items():
            if collection not in {*COLLECTIONS[:-1], "config"}:
                raise StateError(f"apply journal contains an invalid collection: {collection}")
            if not isinstance(document, dict) or document.get("schema_version") != 1:
                raise StateError(f"apply journal contains an invalid {collection} document")
            if collection != "config" and not isinstance(document.get("items"), list):
                raise StateError(f"apply journal contains an invalid {collection} document")
        _, proposal, file_hash = read_proposal(instance, proposal_id)
        validate_proposal_semantics(instance, state_dir, proposal, before_documents)
        approvals = read_jsonl(state_dir / "approvals.jsonl")
        approval = next((item for item in reversed(approvals) if item.get("proposal_id") == proposal_id and item.get("proposal_content_hash") == proposal["content_hash"] and item.get("proposal_file_hash") == file_hash), None)
        if approval is None:
            raise StateError("no matching approval for the interrupted proposal")
        for name, document in before_documents.items():
            if sha256_bytes(canonical_bytes(document)) != proposal.get("before_hashes", {}).get(name):
                raise StateError(f"apply journal {name} base does not match the approved proposal")
        expected_targets = copy.deepcopy(before_documents)
        apply_operations(expected_targets, proposal["operations"])
        if canonical_bytes(expected_targets) != canonical_bytes(targets):
            raise StateError("apply journal targets do not result from the approved proposal")
        validate_targets(instance, state_dir, targets)
        audit_entry = journal.get("audit")
        if not isinstance(audit_entry, dict) or audit_entry.get("proposal_id") != proposal_id or audit_entry.get("approval_id") != approval.get("id"):
            raise StateError("apply journal audit metadata does not match the approved proposal")
        before = state_hashes(state_dir)
        for collection, document in targets.items():
            atomic_write_json(editable_path(instance, state_dir, collection), document)
        after = state_hashes(state_dir)
        expected_after = document_hashes_after(state_dir, targets)
        if after != expected_after or audit_entry.get("after_hashes") != after:
            raise StateError("recovered proposal state does not match journal hashes")
        recovery_entry = {
            "schema_version": 1, "id": str(uuid.uuid4()), "timestamp": now_iso(), "actor": actor,
            "action": "recover_proposal", "before_hashes": before, "after_hashes": after,
            "proposal_id": proposal_id, "approval_id": approval["id"], "recovered_audit_id": audit_entry["id"],
        }
        append_audit_once(state_dir, audit_entry)
        append_audit_once(state_dir, recovery_entry)
        journal_path.unlink()
        return {"ok": True, "recovered": True, "proposal_id": proposal_id, "approval_id": approval["id"], "after_hashes": after}


def render_report(projection: dict[str, Any], output: Path) -> None:
    base = projection["base_currency"]
    zero = projection["zero_dates"]
    driver = find_first_driver(projection)
    cards = "".join(
        f"<tr><td>{html.escape(str(item['name']))}</td><td>{html.escape(item['due_date_iso'])}</td><td>{html.escape(format_minor(item['total_base'], base))} {base}</td></tr>"
        for item in projection["card_statements"]
    ) or '<tr><td colspan="3">No projected card statements.</td></tr>'
    timeline = "".join(
        f"<tr><td>{html.escape(str(item['date_iso']))}</td><td>{html.escape(str(item['label']))}</td><td>{html.escape(format_minor(item['delta_base'], base))}</td><td>{html.escape(format_minor(item['balance'], base))}</td></tr>"
        for item in projection["timeline"][:80]
    ) or '<tr><td colspan="4">No projected movements.</td></tr>'
    warnings = "".join(f"<li>{html.escape(str(item))}</li>" for item in projection["warnings"]) or "<li>None.</li>"
    hashes = "".join(f"<li><code>{html.escape(name)}</code> <code>{digest}</code></li>" for name, digest in projection["state_hashes"].items())
    driver_text = "No material outflow in the horizon."
    if driver:
        driver_text = f"{driver['label']} on {driver['date_iso']} ({format_minor(driver['delta_base'], base)} {base})"
    document = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Until Zero — {html.escape(projection['today_iso'])}</title><style>
:root{{--bg:#f7f8f8;--surface:#fff;--ink:#203033;--muted:#647477;--line:#dce3e4;--accent:#167b78;--danger:#b6423c}}@media(prefers-color-scheme:dark){{:root{{--bg:#11191b;--surface:#182225;--ink:#edf4f3;--muted:#9aacab;--line:#2e3d40;--accent:#6bc5bd;--danger:#f08f86}}}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,sans-serif}}main{{width:min(980px,calc(100% - 28px));margin:auto;padding:42px 0 72px}}h1{{font-size:clamp(2rem,7vw,4.8rem);line-height:1;margin:.1em 0}}p{{color:var(--muted)}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:28px 0}}.card{{padding:18px;border:1px solid var(--line);border-radius:12px;background:var(--surface)}}.card b{{display:block;font-size:1.35rem;color:var(--accent)}}table{{width:100%;border-collapse:collapse;background:var(--surface);margin:12px 0 28px}}th,td{{padding:10px;border-bottom:1px solid var(--line);text-align:left}}code{{overflow-wrap:anywhere}}details{{margin-top:20px}}@media(max-width:640px){{.cards{{grid-template-columns:1fr}}th:nth-child(3),td:nth-child(3){{display:none}}}}
</style></head><body><main><p>Cash runway as of {html.escape(projection['today_iso'])}</p><h1>Until Zero</h1>
<div class="cards"><div class="card"><span>Expected</span><b>{html.escape(str(zero['expected'] or 'Holds'))}</b></div><div class="card"><span>Pessimistic</span><b>{html.escape(str(zero['pessimistic'] or 'Holds'))}</b></div><div class="card"><span>Optimistic</span><b>{html.escape(str(zero['optimistic'] or 'Holds'))}</b></div></div>
<p>Opening balance: <strong>{html.escape(format_minor(projection['opening_balance'], base))} {base}</strong>. Pending decisions: <strong>{projection['pending_capture_count']}</strong>.</p>
<h2>First material driver</h2><p>{html.escape(driver_text)}</p><h2>Upcoming card statements</h2><table><thead><tr><th>Account</th><th>Due</th><th>Total</th></tr></thead><tbody>{cards}</tbody></table>
<h2>Expected timeline</h2><table><thead><tr><th>Date</th><th>Movement</th><th>Change</th><th>Balance</th></tr></thead><tbody>{timeline}</tbody></table>
<h2>Warnings and assumptions</h2><ul>{warnings}</ul><p>Amounts use integer minor units. Unmapped captures are excluded. Actual transactions count unless ignored; credit-card charges move cash on statement due dates.</p>
<details><summary>Provenance</summary><p>Projection schema 1; horizon ends {html.escape(projection['horizon_iso'])}.</p><ul>{hashes}</ul></details>
</main></body></html>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help=argparse.SUPPRESS)
    parser.add_argument("--instance", default="until-zero", help=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(dest="command", required=True)

    project_parser = subparsers.add_parser("project", help="compute the deterministic runway")
    project_parser.add_argument("--project", type=Path, default=Path.cwd())
    project_parser.add_argument("--instance", default="until-zero")
    project_parser.add_argument("--today", required=True)
    project_parser.add_argument("--json", action="store_true")

    report_parser = subparsers.add_parser("report", help="generate the self-contained review report")
    report_parser.add_argument("--project", type=Path, default=Path.cwd())
    report_parser.add_argument("--instance", default="until-zero")
    report_parser.add_argument("--today", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="commit one leased capture locally")
    ingest_parser.add_argument("--project", type=Path, default=Path.cwd())
    ingest_parser.add_argument("--instance", default="until-zero")
    ingest_parser.add_argument("--capture", type=Path, required=True)
    ingest_parser.add_argument("--actor", default="until-zero")

    assign_parser = subparsers.add_parser("assign", help="assign a pending capture to an account")
    assign_parser.add_argument("--project", type=Path, default=Path.cwd())
    assign_parser.add_argument("--instance", default="until-zero")
    assign_parser.add_argument("--queue-id", required=True)
    assign_parser.add_argument("--account", required=True)
    assign_parser.add_argument("--actor", default="until-zero")

    propose_parser = subparsers.add_parser("propose", help="create a reviewable state change")
    propose_parser.add_argument("--project", type=Path, default=Path.cwd())
    propose_parser.add_argument("--instance", default="until-zero")
    propose_parser.add_argument("--changes", type=Path, required=True)
    propose_parser.add_argument("--actor", required=True)
    propose_parser.add_argument("--today", required=True)

    statement_parser = subparsers.add_parser("statement", help="normalize a statement into a reviewable change set")
    statement_parser.add_argument("--project", type=Path, default=Path.cwd())
    statement_parser.add_argument("--instance", default="until-zero")
    statement_parser.add_argument("--statement", type=Path, required=True)
    statement_parser.add_argument("--output", type=Path, required=True)
    statement_parser.add_argument("--tolerance-days", type=int, default=3)

    approve_parser = subparsers.add_parser("approve", help="approve the exact proposal bytes")
    approve_parser.add_argument("--project", type=Path, default=Path.cwd())
    approve_parser.add_argument("--instance", default="until-zero")
    approve_parser.add_argument("--proposal", required=True)
    approve_parser.add_argument("--actor", required=True)

    apply_parser = subparsers.add_parser("apply", help="apply a matching approved proposal")
    apply_parser.add_argument("--project", type=Path, default=Path.cwd())
    apply_parser.add_argument("--instance", default="until-zero")
    apply_parser.add_argument("--proposal", required=True)
    apply_parser.add_argument("--actor", required=True)

    recover_parser = subparsers.add_parser("recover", help="complete an interrupted approved proposal apply")
    recover_parser.add_argument("--project", type=Path, default=Path.cwd())
    recover_parser.add_argument("--instance", default="until-zero")
    recover_parser.add_argument("--proposal", required=True)
    recover_parser.add_argument("--actor", required=True)

    arguments = parser.parse_args(argv)
    try:
        instance, state_dir, config = instance_paths(arguments.project, arguments.instance)
        if arguments.command == "project":
            ensure_no_outstanding_journals(state_dir)
            projection = project(state_dir, config, arguments.today)
            if arguments.json:
                print(json.dumps(projection, indent=2, sort_keys=True))
            else:
                print(f"Expected zero: {projection['zero_dates']['expected'] or 'holds through horizon'}")
            return 0
        if arguments.command == "report":
            ensure_no_outstanding_journals(state_dir)
            projection = project(state_dir, config, arguments.today)
            output = instance / "reports" / "current.html"
            render_report(projection, output)
            print(output)
            return 0
        if arguments.command == "ingest":
            print(json.dumps(ingest_capture(instance, state_dir, load_json(arguments.capture), arguments.actor), indent=2, sort_keys=True))
            return 0
        if arguments.command == "assign":
            print(json.dumps(assign_capture(instance, state_dir, arguments.queue_id, arguments.account, arguments.actor), indent=2, sort_keys=True))
            return 0
        if arguments.command == "propose":
            print(json.dumps(create_proposal(instance, state_dir, load_json(arguments.changes), arguments.actor, arguments.today), indent=2, sort_keys=True))
            return 0
        if arguments.command == "statement":
            ensure_no_outstanding_journals(state_dir)
            changes = statement_changes(instance, state_dir, load_json(arguments.statement), arguments.tolerance_days)
            atomic_write_json(arguments.output.resolve(), changes)
            print(json.dumps({
                "output": str(arguments.output.resolve()),
                "matched": changes["matched"], "created": changes["created"], "unresolved": changes["unresolved"],
            }, indent=2, sort_keys=True))
            return 0
        if arguments.command == "approve":
            print(json.dumps(approve_proposal(instance, state_dir, arguments.proposal, arguments.actor), indent=2, sort_keys=True))
            return 0
        if arguments.command == "apply":
            print(json.dumps(apply_proposal(instance, state_dir, arguments.proposal, arguments.actor), indent=2, sort_keys=True))
            return 0
        if arguments.command == "recover":
            print(json.dumps(recover_proposal(instance, state_dir, arguments.proposal, arguments.actor), indent=2, sort_keys=True))
            return 0
    except (OSError, StateError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 4 if arguments.command in {"approve", "apply", "recover"} else 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
