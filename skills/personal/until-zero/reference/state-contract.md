# State contract

Canonical state lives under `until-zero/state/`. JSON documents use
`{"schema_version": 1, "items": [...]}`; `approvals.jsonl` and `audit.jsonl` are append-only. All writes use
the single-writer lock and atomic replacement. Store money as signed integer minor-unit strings and calendar
dates as `YYYY-MM-DD`. `config.json` is part of the canonical approval hash: base currency, buffer, and horizon
changes use the same proposal/approval/apply path, and direct config drift invalidates approval.

## Collections

- `accounts`: `id`, `name`, `kind` (`cash`, `credit_card`, `rail`), `currency`, balance snapshot, card cycle,
  funding account, last digits/aliases, and archived flag.
- `rules`: recurring amount, account, currency, cadence, anchor/bounds, certainty, ordering, occurrence
  exclusions, pause ranges, and active flag.
- `events`: dated one-time movement, account, amount, currency, certainty, ordering, linkage, and active flag.
- `fx_rates`: base, quote, decimal rate, and as-of date.
- `transactions`: source, status, account, date, amount, currency, description/category, external ID, Queue ID,
  and non-secret card routing fields.
- `pending_captures`: valid but unmapped Wallet inputs with Queue ID and raw provenance. Exclude them from
  projection until assignment.

## Projection semantics

Start from non-archived cash balance snapshots. Fold later non-ignored cash actuals into the opening balance;
same-day reconciled rows are already included. Treat uncleared, cleared, and reconciled actuals as real;
exclude only ignored rows.

Aggregate credit-card charges and outstanding balances onto their statement due dates. Use a fixed due day
when present, otherwise a close-date offset. Apply recurring exceptions before projection. Within one day,
honor explicit ordering and then inflow-before-outflow.

Certainty bands are asymmetric: expected excludes speculative items; pessimistic keeps every outflow but only
committed inflows; optimistic keeps every inflow but only committed outflows. A band hits zero on the first
entry whose running balance is strictly below the configured buffer.

Convert currencies through direct or inverse stored rates. When a pair is missing, surface a warning and use
1:1 only as an explicit degraded assumption.
