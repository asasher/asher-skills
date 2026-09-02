# Template guide — what an issue carries

This file is the content contract: what a published issue must carry, and what the pre-publish split draft shows the user.

## A single issue

- **Title**: one line naming the capability the slice delivers, from the user's perspective. Not "add the model layer" (horizontal) but "a user can save a draft and see it on reload" (a demoable slice).
- **Intent**: one or two sentences, what this issue makes possible and why, at the altitude of direction, traceable back to the source spec.
- **Slice**: the tracer bullet, the one real thing this issue does end to end and how it demos alone. For a wide-refactor issue, name which phase it is (expand, migrate batch N, contract). No file paths or code (slicing § No stale content).
- **Acceptance criteria**: a numbered list with stable ids `AC-1`, `AC-2`, and so on. Each criterion is one observable outcome a checker can grade pass or fail; together they are what a demo shows. For each, whether its check is a durable guard or a throwaway verification script, carried over from the spec. The ids are the handles the builder, verifier, reviewer, and evidence key their verdicts to, so they stay stable across revisions: amend in place or append; an id, once assigned, keeps its meaning. Numbering is per issue.
- **Work-type**: `enhancement`, or `bug` when the slice is a fix.

Dependencies are wired as native `blocked_by` edges per slicing § Order and wire; the body describes the work, the edges carry the graph.

Keep every field at the altitude of direction: an issue is pickup-able work, not a design document. If a field drifts into file-by-file detail, pull it back up; the implementing agent carries that detail.

## The split draft

One scratch document, drafted before the confirmation gate and revised through it, a justified recommendation the user edits, containing:

- **Source**: what direction this split came from: the spec'd issue and the blessed spec hash the slices were cut from, a document path, or "this conversation". Recorded so a reader can trace issues back, and so a later blessing at a new hash shows the split is stale. When the source is a spec'd issue, say that on publish it becomes the `spec` parent: every issue below attaches as its sub-issue and blocker.
- **Landing**: the stacked landing in one sentence (slicing § How slices land), so the user sees children branching from the spec branch and the promotion PR at the end.
- **Ordered issues**: the issues in dependency order, blockers first, each carrying the content above plus its rationale, numbered locally (T1, T2, and so on) since ids do not exist until publish.
- **Edge list**: the dependency graph as a compact list (`T2 depends on T1: the schema T2 reads lands in T1`), each edge justified in words so the user can judge the blocking structure. On publish, local labels become issue ids and each edge is wired.
- **Wide-refactor note**: if any part is sequenced expand, migrate, contract, call it out so the user confirms the phasing, not just the granularity.
