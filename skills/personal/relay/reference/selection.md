# Selection and disclosure

## Bindings

Treat profiles as human-readable relationship policy and audience/interest JSON as hash-bound operational
derivatives. Each audience declares project IDs, message kind, section recipe, disclosure, cadence, operator-CC
override, and recipients with explicit `header: to|cc`. Each interest file declares allowed features and
sections. A missing or stale binding blocks that audience; it never falls back to prompt lore.

The repository playbook owns project-specific collection and editorial policy: which provider operations form
a complete search, what provider states mean, how source mechanics become recipient-facing language, and which
unresolved facts may carry forward. `relay/*.json` holds the structured operational derivatives of those
choices. The portable skill supplies the selection and safety mechanics; it does not name a project's trackers,
queries, audiences, status mappings, or prose rules.

## Evidence

Normalize every fact to `id`, `source`, `observed_at`, `project_id`, `feature`, `status`, `disclosure`, `section`,
`title`, and `detail`. Status is one of `production_verified`, `shipped_unverified`, `in_progress`, `pending`,
or `planned`. Only `production_verified` may be called shipped or live externally. Describe
`shipped_unverified` as released pending verification; never turn progress or plans into commitments.

Complete every collection operation declared by the repository playbook. Preserve a run-local account of the
candidates returned by each bound provider and record whether each was included, excluded, or coalesced, with a
reason. Provider mechanics and attribution remain private evidence unless the local editorial policy explicitly
allows them in recipient copy.

For an external audience include a fact only when its project, feature, section, disclosure, and watermark all
pass the bound rules. Never expose another audience's evidence or recipients. If none pass, emit an exclusion.
For an internal digest apply its broader bound disclosure and section recipe, but keep cash and growth claims
with their authoritative providers and label uncertainty.

The default watermark rule excludes facts observed at or before the audience's confirmed-send watermark. A
collector may set `carry_forward: true` only when the repository playbook expressly identifies that unresolved
class and the fact has been rechecked in the current collection. Carry-forward bypasses the time comparison; it
does not bypass project, feature, section, or disclosure boundaries.

Resolve recipients after selection. Normalize addresses to lowercase, deduplicate within and across headers,
and fail if one address appears in both To and CC. For external sends append the operator to CC unless that
audience explicitly disables the default. The sender is never inferred as a recipient.

`scripts/select_bags.py` consumes already-normalized evidence and the local binding; it never runs arbitrary
provider commands. The agent owns provider gathering, attribution, and normalization before calling it.

Completion criterion: every eligible audience produces one validated bag or explicit exclusion, every visible
item has attributable evidence, every provider collection declared by the playbook is accounted for, and no
fact or recipient crosses an audience boundary.
