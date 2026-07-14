# Setup

Reconcile a consumer-owned instance. Local materialization is deterministic; provider, external plugin,
Shortcut, and phone work remain effect gates.

1. Disclose the exact `metadata.external` name, kind, source, version, and capability. Obtain explicit consent
   before project-local installation and record the result separately from skill provenance. Declining leaves
   that gate pending.
2. Run `python3 <skill>/scripts/setup_instance.py --project <root>`. It materializes canonical empty state,
   editable API source, config/deployment/setup metadata, private `.env`, reports, proposals, and empty
   Shortcut directory. Reconcile any exit-3 candidates; never overwrite them wholesale.
3. Gather accounts, balances, card cycles, rules, events, FX, buffer, and horizon through reviewable proposals.
4. Deploy only from materialized `until-zero/api/`. Use one replica and persistent `/data`; create distinct
   producer/drain tokens as provider secrets and in the ignored mode-0600 `.env`. Verify health reports both
   roles configured and `auth_roles_separated: true`; unauthenticated and cross-role calls fail; append/lease/ack
   removes one smoke item exactly once. Record only provider identities and verified HTTPS origin.
5. Give [shortcut contract](shortcut-contract.md) to the consented external capability. Validate, sign, import,
   wire the personal Transaction automation, and record non-secret build evidence.
6. Run one live capture, refresh, assignment if needed, projection, report generation, and
   `validate_instance.py`. Mark a gate complete only after observing its effect.

For each observed external effect, write a non-secret evidence object with `kind` and ISO `observed_at`, then run
`setup_instance.py --project <root> --set-gate <gate> --status complete --evidence <evidence.json>`. Use `blocked`
with evidence for a real failure, or `pending` without evidence when no effect was attempted.

If provider CLI/auth is absent, record the deployment gate pending and stop before mutation. On rerun, preserve
state, provider identity, API edits, reports, XML, and signed artifacts. Advance only
untouched template files; emit adjacent candidates for conflicts. Completion requires an immediate idempotent
rerun and no unresolved structural findings.
