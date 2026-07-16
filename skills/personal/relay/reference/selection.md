# Selection and disclosure

## Bindings

Treat profiles as human-readable relationship policy and audience/interest JSON as hash-bound operational
derivatives. Each audience declares project IDs, message kind, section recipe, disclosure, cadence, operator-CC
override, and recipients with explicit `header: to|cc`. Each interest file declares allowed features and
sections. A missing or stale binding blocks that audience; it never falls back to prompt lore.

## Evidence

Normalize every fact to `id`, `source`, `observed_at`, `project_id`, `feature`, `status`, `disclosure`, `section`,
`title`, and `detail`. Status is one of `production_verified`, `shipped_unverified`, `in_progress`, `pending`,
or `planned`. Only `production_verified` may be called shipped or live externally. Describe
`shipped_unverified` as released pending verification; never turn progress or plans into commitments.

For an external audience include a fact only when its project, feature, section, disclosure, and watermark all
pass the bound rules. Never expose another audience's evidence or recipients. If none pass, emit an exclusion.
For an internal digest apply its broader bound disclosure and section recipe, but keep cash and growth claims
with their authoritative providers and label uncertainty.

Resolve recipients after selection. Normalize addresses to lowercase, deduplicate within and across headers,
and fail if one address appears in both To and CC. For external sends append the operator to CC unless that
audience explicitly disables the default. The sender is never inferred as a recipient.

`scripts/select_bags.py` consumes already-normalized evidence and the local binding; it never runs arbitrary
provider commands. The agent owns provider gathering, attribution, and normalization before calling it.

Completion criterion: every eligible audience produces one validated bag or explicit exclusion, every visible
item has attributable evidence, and no fact or recipient crosses an audience boundary.
