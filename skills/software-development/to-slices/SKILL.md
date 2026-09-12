---
name: to-slices
description: Split a ticket's approved spec revision into ready vertical child tickets and dependencies, with approval of the concrete split.
disable-model-invocation: true
metadata:
  optional: [technical-writing]
---

# To slices

Split one ticket's approved spec revision; preserve its decisions. Use `technical-writing` when available. Publication requires approval of the concrete split; carry prior approval when it covers this exact source revision, slices, graph, and landing plan.

Follow [slicing](reference/slicing.md) and [the content contract](reference/template-guide.md):

1. Require a ticket with a published spec and recorded approval of its exact revision. Read that revision and the ticket history; later direction changes require a revised approved spec before slicing. Account for every actor, surface, and acceptance criterion.
2. Draft demoable vertical slices, each sized for one fresh context. Use expand/migrate/contract only for wide mechanical refactors. Explain each boundary and every true blocker.
3. Present the split, landing branches, and coverage map for any approval still needed. Boundary edits stay within the approved direction; requirement changes return for a revised approved spec.
4. Audit every ticket for observable acceptance, inherited context, delegated authority, UI states where applicable, and necessary dependencies. Fix thin tickets before creation.
5. Persist the approved draft and issue mapping. Create or reconcile tickets in dependency order under the ownership and recovery gates in slicing, each new ticket `shaping` with its work-type. Wire native blockers. A split ticket becomes a `spec` parent, with each child both a sub-issue and blocker; its work branch is their integration base and PR target.
6. Read back the complete graph and confirm the spec branch is pushed. Only then release held open children and parent as `ready-for-agent`, preserving advanced labels and claims. Partial publication stays `shaping`; resume the existing mapping and inspect uncertain creates before retrying.

Return ticket links, coverage and dependency mapping, and publication status. Capture missing decisions as blockers for shaping.
