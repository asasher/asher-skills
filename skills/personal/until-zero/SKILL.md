---
name: until-zero
description: Operate a review-first personal cash runway from workspace-owned state. Use when the user asks when they hit zero, wants a runway refresh or report, records or assigns Wallet transactions, changes accounts/rules/events/FX, reconciles a statement, sets up or migrates Until Zero, or evaluates the Lakebed-to-skill cutover.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
  setup: reference/setup.md
  external: [{"name":"shortcuts-playground","kind":"codex-plugin","source":"https://github.com/viticci/shortcuts-playground-plugin","capability":"build-apple-shortcuts","version":"1.2.x"}]
---

# Until Zero

Answer one question from canonical local state: **when does cash cross the configured buffer?** Preserve
integer minor units, explicit calendar dates, card statement timing, certainty bands, capture provenance,
and review-before-apply mutations.

## Route the request

- **No argument / question / `report`** — read [operations](reference/operations.md), run the deterministic
  projection at an explicit `--today`, regenerate `reports/current.html`, and answer from that output.
- **`setup`** — read [setup](reference/setup.md), [deployment](reference/deployment.md), and
  [shortcut contract](reference/shortcut-contract.md). Reconcile the consumer instance end to end.
- **`refresh`** — read [capture](reference/capture.md); lease captures, commit each locally, then acknowledge.
- **`assign`** — assign one pending capture to an active account through `scripts/until_zero.py assign`.
- **Model edit / `propose` / `approve` / `apply`** — read [operations](reference/operations.md). Show the
  before/after runway, approve the exact proposal hash, then apply it; never edit canonical JSON directly.
- **Statement reconciliation** — use the proposal path in [operations](reference/operations.md); imported
  matches, statuses, balances, and candidate rules remain proposed until approval.
- **`migrate` / `retire`** — read [migration](reference/migration.md). Export and select one owner, prove
  cross-engine parity, dual-run, rehearse rollback, and only then retire Lakebed.
- **Morning orchestration** — read [control-plane](reference/control-plane.md). This domain skill owns the
  runway; the `control-plane` sibling owns sequence and the final brief.

Read [state contract](reference/state-contract.md) whenever touching financial state or interpreting model
semantics. Run `scripts/validate_instance.py` before claiming an instance is healthy.

## Non-negotiable invariants

1. Treat `control-plane/runway/state/` as canonical; HTML, remote captures, and chat are projections or input.
2. Keep secrets in the private token file or provider environment. Never print, commit, or copy them into
   proposals, audit rows, reports, deployment metadata, or Shortcut source.
3. Exclude unmapped captures from every projection. Assignment creates exactly one uncleared transaction.
4. Acknowledge a remote capture only after its atomic local commit succeeds. A rerun dedupes by Queue ID.
5. Apply no financial mutation without a matching approval for the exact proposal bytes and unchanged base
   state. Record before/after hashes, actor, source IDs, proposal ID, and approval ID.
6. Preserve consumer-owned instance files on setup/upgrade. Advance untouched templates; emit adjacent
   `.setup-candidate` files for consumer edits and stop for reconciliation.
7. Treat provider creation, deployment, Shortcut signing/import, live phone capture, and retirement as
   effect gates. Instructions or upload acceptance are not proof.

## Commands

Run scripts from the installed package; pass the consumer root explicitly:

```bash
python3 scripts/setup_instance.py --project <consumer-root>
python3 scripts/drain_capture_queue.py --project <consumer-root>
python3 scripts/until_zero.py report --project <consumer-root> --today YYYY-MM-DD
python3 scripts/validate_instance.py --project <consumer-root>
```

For model changes, create a JSON change set and use `propose`, `approve`, then `apply`. For Lakebed data,
run `migrate_lakebed.py inspect` before an explicit-owner `import`; compare old/new snapshots with
`compare_oracles.py`.

## Dependency surface

- **Bundled:** deterministic Python engine and state operations, setup/validation/migration scripts, Runway
  API template, operating contracts, and evals.
- **Project:** consumer-owned `control-plane/runway/` instance, private `.env`, reports, and optional
  `docs/agents/control-plane.md` binding.
- **Sibling:** optional `control-plane`, invoked by name for morning orchestration; no file import.
- **External:** Shortcuts Playground `1.2.x` supplies `build-apple-shortcuts` during setup after explicit
  provenance disclosure and consent. Its files and generated plist do not ship here.
