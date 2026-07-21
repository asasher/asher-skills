---
name: to-tickets
description: Split a decided direction — a spec, a plan document, or the current conversation — into backlog-ready tracer-bullet tickets with blocking edges, quizzing the user on granularity and edges before publishing to the bound tracker in dependency order. Not for writing the direction itself.
argument-hint: "[<path to a spec, or nothing to use the conversation>]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: thread
  requires: []
  optional: []
---

# To-Tickets

To-tickets owns one move: **take a decided direction and split it into backlog-ready tickets with blocking
edges.** It reads a direction, drafts vertical slices, **quizzes the user** until the granularity and edges
are approved, then publishes the tickets into the bound tracker in dependency order.

The defining constraint is the pair of postures it holds at once: **draft vertical slices, but quiz before you
publish.** Each ticket is a **tracer bullet**, with a **wide-refactor** exception for mechanical,
high-blast-radius changes — both defined under § What a ticket is.

## Command surface

- **`to-tickets [<path to a spec>]`** — split the given spec into tickets. With no argument, use the current
  conversation as the direction (or a plan, if one is on the table).

Load [slicing](reference/slicing.md) for the method (what to read, the vertical-slice default, the wide-refactor
exception, the quiz, dependency ordering and backlog's edge convention, the readiness default, the
no-stale-content and never-modify-parent rules) and [template-guide](reference/template-guide.md) for what each
ticket field holds. The fillable scaffolds are [templates/ticket.md](templates/ticket.md) (one ticket) and
[templates/tickets.md](templates/tickets.md) (the whole ordered split, drafted before publishing).

## How a split happens

The full method is in [slicing](reference/slicing.md); the shape:

1. **Read the direction.** The primary input is a **spec** at `docs/specs/<name>.html`. A
   **plan** or the **raw current conversation** are accepted alternates, read the same way — mine the decided
   direction, the actors, and the surface. Never modify the source.
2. **Draft vertical slices.** Cut the work into tracer-bullet tickets — or, for a wide refactor, into its
   expand→migrate-in-batches→contract sequence (§ What a ticket is).
3. **Quiz the user — the human-confirmation step.** Present the draft split and ask about granularity (too
   coarse? too fine?) and blocking edges (what truly blocks what?).
   3b. **Audit each ticket for readiness** (slicing § Audit each ticket for readiness) — a ticket failing
   the audit is fixed or dropped, never published thin.
4. **Order and wire the edges.** Sort the approved tickets into dependency order — **blockers first** — so each
   dependency edge resolves to a real, earlier id. Wire each edge exactly as the repo's recorded convention
   (slicing § Order and wire).
5. **Publish in the bound tracker's format.** Create the tickets through the tracker binding recorded in
   `docs/agents/platform.md`, blockers first, per slicing § Publish; readiness is left unset by default
   (slicing § Readiness).
6. **Readback.** Verify against the live tracker: every approved draft maps to exactly one created ticket, and
   every emitted `depends on #N` marker points at a real, earlier ticket id. Fix any miss before reporting the
   split done.

## What a ticket is (and isn't)

- **A tracer bullet, not a task list.** A ticket is a narrow-but-complete path through every layer — demoable
  on its own, sized to one fresh context window — not a horizontal layer ("all the models," "all the UI") that
  can't be demoed alone. The one exception is a **wide refactor** — a mechanical, high-blast-radius change.
- **Generic vocabulary.** A **ticket** is the unit of pickup-able work; it is exactly the tracker's "issue"
  role, in a tracker-agnostic word. Say "ticket" throughout — the skill's own text never assumes GitHub's
  vocabulary.
- **No file paths or code snippets** — sole exception the prototype-validated snippet (slicing § No stale
  content).
- **The parent is never touched** (slicing § Read the direction).

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory: [slicing](reference/slicing.md)
  and [template-guide](reference/template-guide.md), plus the fillable scaffolds under `templates/`.
  These are the authority; they import no other skill's files.
- **Project playbooks** — the repo's conventions, read from `docs/agents/`: the **dependency convention**
  (`backlog-policy.md` § Dependencies — how a blocking edge is recorded)
  and the **tracker binding** (`platform.md` — how tickets are created and in what format). Absent a
  recorded binding, state the gap and ask the user before publishing anything.
- **Sibling skills** — none. The input is a document or the conversation, never another skill: given a
  spec, a plan document, or a raw conversation, to-tickets runs standalone.
