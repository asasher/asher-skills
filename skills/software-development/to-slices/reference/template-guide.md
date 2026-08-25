# Template guide — what a ticket carries

This file is the content contract: what a ticket published to the tracker must carry, and what the pre-publish split draft shows the user. The body reads the same on any tracker; the shape is the tracker's own — the bound tracker (or the local binding's recorded file format) decides how a body, title, and label are expressed.

## A single ticket

- **Title** — one line naming the capability the slice delivers, from the user's perspective. Not "add the model layer" (horizontal) but "a user can save a draft and see it on reload" (a demoable slice).
- **Intent** — one or two sentences: what this ticket makes possible and why, at the altitude of direction. The reason the slice exists, traceable back to the source spec.
- **Slice** — the tracer bullet: the one real thing this ticket does end to end and how it demos alone. For a wide-refactor ticket, name which phase it is (expand / migrate-batch N / contract). No file paths or code (slicing § No stale content).
- **Acceptance criteria** — a numbered list with stable ids: `AC-1`, `AC-2`, … Each criterion is one observable outcome a checker could grade pass or fail; together they are what a demo shows. Direction for acceptance, not a test plan. The ids are the handles downstream roles — builder, verifier, reviewer, evidence — key their verdicts to, so they stay stable across revisions: amend a criterion in place or append new ones; an id, once assigned, keeps its meaning. Numbering is per ticket.
  <!-- Criterion-id contract adapted from skills/software-development/to-spec/SKILL.md — that statement is canonical; improvements flow back there deliberately, per AGENTS.md § Conventions (copy a technique). -->
- **Work-type (optional)** — if the tracker's routing wants it (`bug` / `enhancement` / `refactor`), name it so grooming has a head start. Left off when unknown — grooming sets it.

**Dependencies are wired per slicing § Order and wire the edges** — the body describes the work; the recorded convention carries the graph.

Keep every field at the altitude of **direction**: a ticket is pickup-able work, not a design document. If a field drifts into file-by-file implementation detail, pull it back up — the implementing agent carries that detail.

## The split draft

One scratch document, drafted before the confirmation gate and revised through it — a justified recommendation the user edits, containing:

- **Source** — what direction this split came from: the spec'd ticket **and the blessed spec hash the slices were cut from**, a document path, or "this conversation." Recorded so a reader can trace tickets back, and so a later blessing at a new hash shows the split is stale. When the source is a spec'd ticket, note that on publish it becomes the **`spec` parent**: every ticket below attaches as its child (slicing § Parent the slices).
- **Landing shape** — the recommendation with its justification: **stacked** or **direct** (slicing § The landing shape).
- **Ordered tickets** — the tickets in **dependency order, blockers first**, each carrying the content above plus its **rationale**, numbered locally (T1, T2, …) since tracker ids don't exist until publish.
- **Edge list** — the dependency graph as a compact list (`T2 depends on T1 — the schema T2 reads lands in T1`), **each edge justified in words** so the user can judge the blocking structure, not just see it. On publish, local Tn labels become tracker ids and each edge is wired per slicing § Order and wire the edges.
- **Wide-refactor note** — if any part is sequenced expand→migrate→contract, call it out so the user confirms the phasing, not just the granularity.
