---
name: until-zero
description: Operate a review-first personal cash runway from workspace-owned state. Use for “when do I hit zero?” reports, Wallet capture refresh or assignment, reviewed model or statement changes, and Until Zero setup.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
  setup: reference/setup.md
  external: [{"name":"shortcuts-playground","kind":"codex-plugin","source":"https://github.com/viticci/shortcuts-playground-plugin","capability":"build-apple-shortcuts","version":"1.2.x"}]
---

# Until Zero

Preserve integer minor units, calendar dates, card timing, certainty bands, provenance, and review-before-apply edits.

## Route the request

- **Question / `report`:** use [operations](reference/operations.md); finish with an explicit-date projection,
  refreshed `reports/current.html`, and a sourced answer.
- **`refresh` / `assign`:** use [capture](reference/capture.md); finish with committed Queue IDs, acknowledgements
  only after local commit, and pending captures resolved or named.
- **Model edit / statement:** use [operations](reference/operations.md); finish only after showing the embedded
  before/after preview, approving its exact hash, applying it, and refreshing the report.
- **`setup`:** use [setup](reference/setup.md) and [shortcut contract](reference/shortcut-contract.md); finish
  only when observed setup gates are complete or explicitly pending/blocked.

Read [state contract](reference/state-contract.md) whenever touching financial state or interpreting model
semantics. Run `scripts/validate_instance.py` before claiming an instance is healthy.

## Invariants

1. Treat `until-zero/state/` as canonical; HTML, remote captures, and chat are projections or input.
2. Keep secrets in the private token file or provider environment. Never print, commit, or copy them into
   proposals, audit rows, reports, deployment metadata, or Shortcut source.
3. Exclude unmapped captures from every projection. Assignment creates exactly one uncleared transaction.
4. Acknowledge a remote capture only after its atomic local commit succeeds. A rerun dedupes by Queue ID.
5. Model and statement edits require a matching approval for exact proposal bytes and unchanged base state.
   Capture ingest and assignment are the audited Queue-ID operational exceptions in [capture](reference/capture.md).
6. Preserve consumer-owned instance files on setup/upgrade. Advance untouched templates; emit adjacent
   `.setup-candidate` files for consumer edits and stop for reconciliation.
7. Provider creation, deployment, Shortcut signing/import, and live phone capture are effect gates; instructions
   are not proof. `validate_instance.py` proves structure, not completion of external gates.
