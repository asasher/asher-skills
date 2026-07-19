# Split: <name of the direction being split>

<!-- The whole split, drafted BEFORE publishing — the artifact the user reacts to during the quiz. Revise
     through the quiz; publish only after approval (reference/slicing.md § Quiz, § Order and wire). -->

> Source: <spec path / plan / "this conversation">. Read as direction — never modified by to-tickets.

## Ordered tickets

<!-- In dependency order, blockers first. Numbered locally (T1, T2, …) — tracker ids don't exist until publish.
     Each ticket in the single-ticket shape (see templates/ticket.md). -->

### T1 — <capability>

- **Intent** — <what it makes possible, traceable to the source>.
- **Slice** — <the narrow-but-complete path; how it's demoable alone>.
- **Done** — <what a demo shows>.
- **Depends on** — none (root).

### T2 — <capability>

- **Intent** — <…>.
- **Slice** — <…>.
- **Done** — <…>.
- **Depends on** — T1.

## Edge list

<!-- The dependency graph, compact, so the blocking structure is eyeball-able during the quiz. On publish these
     become `- [ ] depends on #N` lines in the recorded convention, in dependency order. -->

- T2 depends on T1
- T3 depends on T1

## Wide-refactor note

<!-- If any part is a mechanical, high-blast-radius change sequenced expand → migrate-in-batches → contract,
     call out the phasing here so the user confirms it. Delete this section if no wide refactor is involved. -->

- <e.g. "T4 expand, T5–T7 migrate batches (parallel after T4), T8 contract (blocked on T5–T7)."> 
