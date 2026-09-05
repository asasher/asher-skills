---
name: to-slices
description: Split an approved ticket, spec, plan, or settled conversation into ready vertical child tickets and dependencies. Requires the user's explicit split approval.
disable-model-invocation: true
metadata:
  optional: [technical-writing]
---

# To slices

Split settled direction; preserve its decisions. Use `technical-writing` when available. A spec recommendation alone does not authorize publication.

Follow [slicing](reference/slicing.md) and [the content contract](reference/template-guide.md):

1. Read the complete direction and approved revision. Account for every actor, surface, and acceptance criterion.
2. Draft demoable vertical slices, each sized for one fresh context. Use expand/migrate/contract only for wide mechanical refactors. Explain each boundary and every true blocker.
3. Present the split, landing branches, and coverage map for approval. Resolve the user's edits before publishing.
4. Audit every ticket for observable acceptance, inherited context, delegated authority, UI states where applicable, and necessary dependencies. Fix thin tickets before creation.
5. Persist the approved draft and issue mapping. Create tickets in dependency order, each `shaping` with its work-type. Wire native blockers. A split ticket becomes a `spec` parent, with each child both a sub-issue and blocker; its work branch is their integration base and PR target.
6. Read back the complete graph and confirm the spec branch is pushed. Only then release children and parent as `ready-for-agent`. Partial publication stays `shaping`; resume the existing mapping and inspect uncertain creates before retrying.

Return ticket links, coverage and dependency mapping, and publication status. Capture missing decisions as blockers rather than quietly designing them during the split.
