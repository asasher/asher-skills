# Operations

## Query and report

Run projection with an explicit date, then regenerate the report:

```bash
python3 <skill>/scripts/until_zero.py report --project <consumer-root> --today YYYY-MM-DD
```

Answer with expected/pessimistic/optimistic zero dates, opening balance, first material driver, upcoming card
statement timing, pending decisions, warnings/assumptions, and the report path. Distinguish “holds through the
horizon” from an unavailable or invalid projection.

## Capture assignment

An unmapped capture remains in `pending_captures.json` and changes no zero date. Resolve it with:

```bash
python3 <skill>/scripts/until_zero.py assign --project <root> --queue-id <id> --account <id> --actor <actor>
```

Verify one uncleared transaction exists, the pending row is gone, and the audit row names the Queue ID.

## Review-before-apply edits

Translate a requested edit into a change document without touching state:

```json
{
  "note": "Move rent and update its amount",
  "operations": [
    {"collection": "rules", "id": "rent", "set": {"anchor_date_iso": "2026-08-01", "amount_minor": "-1400000"}}
  ]
}
```

Run `until_zero.py propose`, compute a temporary before/after projection for human review, and show material
zero-date/card-statement effects. `approve` records the exact proposal content and file hashes. `apply` rejects
tampering, missing approval, or canonical-state drift; a successful apply writes through a recovery journal
and appends the audit event.

Never treat conversational assent as approval unless the user has seen the exact proposal and effects. Never
edit the proposal after approval; create a replacement.

If validation finds `state/apply-journal.json`, stop all writers and inspect the journal, proposal, and exact
approval. Complete the already-approved write with:

```bash
python3 <skill>/scripts/until_zero.py recover --project <root> --proposal <id> --actor <actor>
```

The advisory writer lock is released automatically if a process exits. Recovery refuses a mismatched journal,
changed proposal, missing approval, invalid target collection, altered base document, or any target that cannot
be derived from the exact approved operations; it rewrites every journal target atomically, records a recovery
audit row, and only then removes the journal.

## Statement reconciliation

Parse a statement into candidate matches by account, signed amount, date tolerance, and external reference.
Present matched status changes, ignored duplicates, balance snapshot changes, new transactions, and candidate
rules in one proposal. Keep ambiguous rows unresolved. Apply only after approval; then regenerate the report
and retain statement/proposal hashes in the audit trail.
