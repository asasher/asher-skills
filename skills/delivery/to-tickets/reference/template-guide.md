# Template guide — what each ticket field holds

Two scaffolds ship with this skill: [templates/ticket.md](../templates/ticket.md) is one ticket (the shape that
gets published to the tracker), and [templates/tickets.md](../templates/tickets.md) is the whole ordered split —
the pre-publish artifact the user reacts to during the quiz. This file says what goes in each field.

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
- **Depends on** — the blocking edges, copied verbatim from the repo's recorded dependency convention (default
  `- [ ] depends on #N`, per `backlog-policy.md` § Dependencies). Omitted when the ticket is a root with no
  blockers. These are what `backlog run` reads to skip blocked work.
- **Work-type (optional)** — if the tracker's routing wants it (`bug` / `enhancement` / `refactor`), name it so
  grooming has a head start. Left off when unknown — grooming sets it.

Keep every field at the altitude of **direction**: a ticket is pickup-able work, coarser than a plan (which is
per-ticket and gated before implementation). If a field drifts into file-by-file implementation detail, pull it
back up — the implementing agent (or the plan step) carries that detail.

## The whole split (tickets.md)

The pre-publish artifact, drafted before the quiz and revised through it:

- **Source** — what direction this split came from (the spec path, the plan, or "this conversation"). Recorded
  so a reader can trace tickets back; never edited by to-tickets.
- **Ordered tickets** — the tickets in **dependency order, blockers first**, each in the single-ticket shape
  above but numbered locally (T1, T2, …) since tracker ids don't exist until publish.
- **Edge list** — the dependency graph as a compact list (`T2 depends on T1`, `T3 depends on T1`), so the user
  can eyeball the blocking structure during the quiz. On publish, local Tn labels become tracker ids and the
  edges become `- [ ] depends on #N` lines (the playbook's verbatim form) in dependency order.
- **Wide-refactor note** — if any part is sequenced expand→migrate→contract, call it out so the user confirms
  the phasing, not just the granularity.

## Order and altitude

Publish order is the topological sort of the edge list — blockers first — so each `depends on #N` resolves to a
real, earlier id. The tickets file exists to make the quiz concrete: one artifact, ordered, with the edges
visible, that the user approves before anything reaches the tracker.
