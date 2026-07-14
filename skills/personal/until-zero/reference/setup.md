# Setup

Reconcile a consumer-owned instance. Local materialization is deterministic; provider, external plugin,
Shortcut, phone, and cutover work remain effect gates.

1. Inspect the consumer root, existing `until-zero/`, private token file, external lock, provider
   binding, API source, Shortcut artifacts, setup gates, and consumer edits.
2. Disclose the exact `metadata.external` Shortcuts Playground identity, version policy, capability, file
   access, and optional hook. Obtain explicit consent before project-local installation; record the verified
   result separately from Asher-authored skill provenance. Declined consent leaves only that gate pending.
3. Run `python3 <skill>/scripts/setup_instance.py --project <root>`. It materializes canonical empty state,
   editable API source, config/deployment/setup metadata, private `.env`, reports, proposals, and empty
   Shortcut directory. Reconcile any exit-3 candidates; never overwrite them wholesale.
4. If migrating, follow [migration](migration.md) before creating real state. Otherwise gather accounts,
   balances, card cycles, rules, events, FX, buffer, and horizon through reviewable proposals.
5. Follow [deployment](deployment.md). Store only non-secret provider identities after health and auth checks.
6. Give [shortcut contract](shortcut-contract.md) to the consented external capability. Validate, sign, import,
   wire the personal Transaction automation, and record non-secret build evidence.
7. Run one live capture, refresh, assignment if needed, projection, report generation, and
   `validate_instance.py`. Mark a gate complete only after observing its effect.

On rerun, preserve state, provider identity, API edits, reports, XML, and signed artifacts. Advance only
untouched template files; emit adjacent candidates for conflicts. Completion requires an immediate idempotent
rerun and no unresolved structural findings.
