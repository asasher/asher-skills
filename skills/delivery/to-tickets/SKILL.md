---
name: to-tickets
description: Split a decided direction — a spec (to-spec's output), a plan, or the current conversation — into backlog-ready tracer-bullet tickets with blocking edges, quizzing the user on granularity and edges before publishing to the bound tracker in dependency order. Use to turn direction into pickup-able tickets. Not for writing the direction itself — that's to-spec.
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
edges.** A spec captures direction but nothing pickup-able; someone still has to cut it into tracer-bullet
tickets, order them, and wire the dependencies by hand. To-tickets automates that split — the consumer half of
the discussion → work bridge that `to-spec` opens. It reads a direction, drafts vertical slices, **quizzes the
user** until the granularity and edges are approved, then publishes the tickets into the bound tracker in
dependency order. Shipped as our own — no external skill is installed for this.

The defining constraint is the pair of postures it holds at once: **draft vertical slices, but quiz before you
publish.** Each ticket is a **tracer bullet**, with a **wide-refactor** exception for mechanical,
high-blast-radius changes — both defined under § What a ticket is. And unlike `to-spec` (pure synthesis, no
interview), to-tickets **does** interview: the quiz on granularity and blocking edges is the human-confirmation
step, and nothing publishes before it is approved.

## Command surface

- **`to-tickets [<path to a spec>]`** — split the given spec into tickets. With no argument, use the current
  conversation as the direction (or a plan, if one is on the table). This is the only command; invoked bare, it
  runs the split.

Load [slicing](reference/slicing.md) for the method (what to read, the vertical-slice default, the wide-refactor
exception, the quiz, dependency ordering and backlog's edge convention, the readiness default, the
no-stale-content and never-modify-parent rules) and [template-guide](reference/template-guide.md) for what each
ticket field holds. The fillable scaffolds are [templates/ticket.md](templates/ticket.md) (one ticket) and
[templates/tickets.md](templates/tickets.md) (the whole ordered split, drafted before publishing).

## How a split happens

The full method is in [slicing](reference/slicing.md); the shape:

1. **Read the direction.** The primary input is a **spec** at `docs/specs/<name>.html` (to-spec's output). A
   **plan** or the **raw current conversation** are accepted alternates, read the same way — mine the decided
   direction, the actors, and the surface. Never modify the source.
2. **Draft vertical slices.** Cut the work into tracer-bullet tickets — or, for a wide refactor, into its
   expand→migrate-in-batches→contract sequence (§ What a ticket is).
3. **Quiz the user — the human-confirmation step.** Present the draft split and ask about granularity (too
   coarse? too fine?) and blocking edges (what truly blocks what?). Iterate until approved. Nothing publishes
   before approval.
   3b. **Audit each ticket for readiness.** Before publishing, every ticket carries: an **observable
   acceptance** block; **inherited context links** (the spec, its tracking ticket, the decisions it relies
   on); its **authority boundary** (what the executor may decide vs what is settled); for UI surfaces, the
   **UX context** (register, key states, PRODUCT.md/DESIGN.md links); and only **true blocking edges**. A
   ticket failing the audit is fixed or dropped, never published thin.
4. **Order and wire the edges.** Sort the approved tickets into dependency order — **blockers first** — so each
   dependency edge resolves to a real, earlier id. Wire each edge **exactly as the repo's recorded
   convention** (`docs/agents/backlog-policy.md` § Dependencies): the tracker's **native blocking relation**
   where one is bound (written via the `docs/agents/platform.md` verbs), a body-line marker only where the
   playbook records that instead — so `backlog run` reads it and skips blocked work.
5. **Publish in the bound tracker's format.** Create the tickets through the tracker binding recorded in
   `docs/agents/platform.md`, blockers first, in generic "ticket" vocabulary — **never as local files while
   a live tracker is bound**; on-disk tickets exist only when the recorded binding itself is local. Link
   each ticket to the spec's tracking ticket when one exists. **Readiness** (`ready-for-agent`)
   is left to `backlog groom` by default; note the option to apply it on approval (Matt's posture).
6. **Readback.** Verify against the live tracker: every approved draft maps to exactly one created ticket, and
   every emitted `depends on #N` marker points at a real, earlier ticket id. Fix any miss before reporting the
   split done.

## What a ticket is (and isn't)

- **A tracer bullet, not a task list.** A ticket is a narrow-but-complete path through every layer — demoable
  on its own, sized to one fresh context window — not a horizontal layer ("all the models," "all the UI") that
  can't be demoed alone. The one exception is a **wide refactor** — a mechanical, high-blast-radius change —
  sequenced expand→migrate-in-batches→contract instead of forced into a slice.
- **Generic vocabulary.** A **ticket** is the unit of pickup-able work; it is exactly the tracker's "issue"
  role, in a tracker-agnostic word. Say "ticket" throughout — the skill's own text never assumes GitHub's
  vocabulary.
- **No file paths or code snippets.** They rot as the codebase moves; a ticket carries intent and the slice,
  not implementation. The single exception, carried from the plan/spec rule, is a **prototype-validated
  snippet** that encodes a decision more precisely than prose can (a state machine, a schema, a type shape) —
  inline only that fragment and note it came from a prototype.
- **The parent is never touched.** To-tickets reads the spec or parent issue; it never edits it. The source of
  truth is preserved.

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory: [slicing](reference/slicing.md) (the
  split method) and [template-guide](reference/template-guide.md) (what each ticket field holds), plus the
  fillable scaffolds [templates/ticket.md](templates/ticket.md) and [templates/tickets.md](templates/tickets.md).
  These are the authority; they import no other skill's files.
- **Project playbooks** — the repo's conventions, read from `docs/agents/`: the **dependency convention**
  (`backlog-policy.md` § Dependencies — how a blocking edge is recorded, so `backlog run` can skip blocked work)
  and the **tracker binding** (`platform.md` — how tickets are created and in what format). These come from the
  repo, not from the `backlog` skill's files: to-tickets emits **into** backlog's convention, it does not import
  backlog. A repo may record a different specs location or dependency convention; honor it when present.
- **Sibling skills** — to-tickets **consumes `to-spec`'s output** (a spec) as its primary input, and can also
  take a **legacy plan document** (from the retired plan stage) or a **raw conversation**. These inputs are composed by name — to-tickets reads the spec doc
  or the conversation, it does not import another skill's files. There is no hard skill dependency: given any of
  the three inputs, to-tickets runs standalone.
