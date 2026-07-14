# Operations

## Query and report

Run projection with an explicit date, then regenerate the report:

```bash
python3 <skill>/scripts/until_zero.py report --project <consumer-root> --today YYYY-MM-DD
```

Answer with expected/pessimistic/optimistic zero dates, opening balance, first material driver, upcoming card
statement timing, pending decisions, warnings/assumptions, and the report path. Distinguish “holds through the
horizon” from an unavailable or invalid projection.

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

Run:

```bash
python3 <skill>/scripts/until_zero.py propose --project <root> --changes <changes.json> --actor <actor> --today YYYY-MM-DD
```

The proposal embeds exact before/after opening balance, zero dates, card statements, pending count, and warnings;
its content hash binds that preview. Show it, then run `until_zero.py approve --project <root> --proposal <id>
--actor <approver>` only after explicit approval, followed by `until_zero.py apply --project <root> --proposal
<id> --actor <actor>`. Apply rejects tampering, missing approval, or canonical drift, writes through a recovery
journal, and appends the audit event.

Never treat conversational assent as approval unless the user has seen the exact proposal and effects. Never
edit the proposal after approval; create a replacement.

If validation finds `state/apply-journal.json`, stop all writers and inspect the journal, proposal, and exact
approval. Complete the already-approved write with:

```bash
python3 <skill>/scripts/until_zero.py recover --project <root> --proposal <id> --actor <actor>
```

Recovery recomputes the approved operations and preview, rewrites every journal target atomically, records its
audit row, and only then removes the journal; any mismatch leaves the journal in place.

## Statement reconciliation

Normalize source material to JSON without editing canonical state:

```json
{"schema_version":1,"id":"stmt-2026-07","account_id":"card","as_of":"2026-07-14","balance_minor":"-25000","currency":"AED","rows":[{"id":"1","date_iso":"2026-07-10","amount_minor":"-2500","description":"Coffee","external_id":"optional"}]}
```

```bash
python3 <skill>/scripts/until_zero.py statement --project <root> --statement <statement.json> --output <changes.json>
```

The deterministic pass matches an unused transaction by unique external ID, otherwise exact signed amount and
date within three days. One match proposes `reconciled`; no match proposes a new statement transaction; multiple
matches remain unresolved. A supplied balance proposes the account snapshot. Resolve every ambiguous row and
regenerate the change set before the normal propose/approve/apply path. The proposal binds the normalized statement hash; regenerate the report
after apply. Recurring-rule changes are separate explicit model edits, never inferred from a statement.
