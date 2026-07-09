# To-Tickets

Splits a decided direction into **backlog-ready tickets** with blocking edges — the consumer half of the
discussion → work bridge that `to-spec` opens. Its primary input is a **spec** (to-spec's output at
`docs/specs/<name>.md`); it also accepts a **plan** or the **raw current conversation**. It drafts vertical
slices, quizzes the user until the granularity and edges are approved, then publishes the tickets into the bound
tracker in dependency order — blockers first — with `depends on #N` edges (backlog's recorded convention) that
`backlog run` reads to skip blocked work.

## When to use

- **After `to-spec`** — turn the direction document into pickup-able tickets (a sibling invokes this by name;
  a user can run it directly).
- **From a plan or a live conversation** — when no spec was written, split a plan or the current conversation
  the same way.

Not for writing the direction itself — that's `to-spec`. To-tickets consumes a direction and cuts it into work.

## Shape

- **Draft vertical slices.** Each ticket is a tracer bullet — a narrow-but-complete path through every layer,
  demoable on its own, sized to one fresh context window. Not a horizontal layer ("all the models," "all the
  UI") that can't be demoed alone.
- **Wide-refactor exception.** A mechanical, high-blast-radius change is sequenced expand → migrate-in-batches
  → contract instead of forced into a slice.
- **Quiz the user — the human-confirmation step.** Unlike to-spec's pure synthesis, to-tickets **interviews**:
  it quizzes on granularity and blocking edges and iterates until approved. Nothing publishes before approval.
- **Publish blockers-first, in backlog's edge convention.** Tickets are created in dependency order so each
  `- [ ] depends on #N` line (verbatim per `backlog-policy.md` § Dependencies) resolves to a real earlier id.
- **Readiness left to groom.** A fresh split does not auto-apply `ready-for-agent`; the option to apply it on
  approval (Matt's posture) is noted, but the default leaves readiness to `backlog groom`.
- **Generic vocabulary; no stale content; parent untouched.** "Ticket" throughout (ticket == the tracker's
  issue role); no file paths or code in tickets (prototype-validated-snippet exception); the source spec or
  parent issue is never modified.
- **Adapted from Matt Pocock's `to-tickets`, shipped as our own.** We never install an external skill.

## Layout

`SKILL.md` is the command surface (`to-tickets [<spec path>]`) and points into `reference/`:
`slicing.md` (the split method — inputs, vertical slices, the wide-refactor exception, the quiz, dependency
ordering and backlog's edge convention, the readiness default, no-stale-content, never-modify-parent) and
`template-guide.md` (what each ticket field holds). `templates/ticket.md` is one ticket; `templates/tickets.md`
is the whole ordered split drafted before the quiz. `agents/openai.yaml` is the Codex manifest.
`evals/probes.md` is the pre-deployment probe eval.

Self-contained at the file level; composes by name. **Inputs** — consumes `to-spec`'s output, or a `plan`, or a
raw conversation — are read as documents, not imported. The **dependency convention** and **tracker binding**
come from the repo's project playbooks (`backlog-policy.md`, `platform.md`): to-tickets emits *into* backlog's
convention, it does not import the `backlog` skill.

## Install

`npx skills add <repo-url> --skill to-tickets`, then invoke it (`to-tickets <spec path>`) to split a decided
direction into pickup-able tickets.
