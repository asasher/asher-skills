# Template guide — what a ticket carries

This file is the content contract: what a ticket published to the tracker must carry, and what the
pre-publish split draft shows the user. The body reads the same on any tracker; the shape is the
tracker's own — the bound tracker (or the local binding's recorded file format) decides how a body,
title, and label are expressed.

## A single ticket

- **Title** — one line naming the capability the slice delivers, from the user's perspective. Not "add the
  model layer" (horizontal) but "a user can save a draft and see it on reload" (a demoable slice).
- **Intent** — one or two sentences: what this ticket makes possible and why, at the altitude of direction. The
  reason the slice exists, traceable back to the source spec.
- **Slice** — what the narrow-but-complete path is: the one real thing this ticket does end to end, and how it
  is demoable on its own. For a wide-refactor ticket, name which phase it is (expand / migrate-batch N /
  contract). No file paths or code (prototype-validated-snippet exception only).
- **Done** — the checkable outcome that means the slice is delivered: what a demo shows. Direction for
  acceptance, not a test plan.
- **Work-type (optional)** — if the tracker's routing wants it (`bug` / `enhancement` / `refactor`), name it so
  grooming has a head start. Left off when unknown — grooming sets it.

**Dependencies are tracker relations, not body prose.** Blocking edges are wired through the dependency
verb the platform binding records (`backlog-policy.md` § Dependencies): the tracker's **native blocking
relation** where it has one, else the playbook's recorded form (a local binding's `deps:` frontmatter, a
body-line marker). The body describes the work; the tracker carries the graph.

Keep every field at the altitude of **direction**: a ticket is pickup-able work, coarser than a plan (the
retired per-ticket plan stage). If a field drifts into file-by-file implementation detail, pull it
back up — the implementing agent (or the plan step) carries that detail.

## The split draft

One scratch document, drafted before the quiz and revised through it, containing:

- **Source** — what direction this split came from (the spec'd ticket, a document path, or "this
  conversation"). Recorded so a reader can trace tickets back.
- **Ordered tickets** — the tickets in **dependency order, blockers first**, each carrying the content
  above but numbered locally (T1, T2, …) since tracker ids don't exist until publish.
- **Edge list** — the dependency graph as a compact list (`T2 depends on T1`, `T3 depends on T1`), so the user
  can eyeball the blocking structure during the quiz. On publish, local Tn labels become tracker ids and
  each edge is wired per the dependency rule above.
- **Wide-refactor note** — if any part is sequenced expand→migrate→contract, call it out so the user confirms
  the phasing, not just the granularity.

## Order and altitude

The draft exists to make the quiz concrete: one artifact, ordered, with the edges
visible, that the user approves before anything reaches the tracker.
