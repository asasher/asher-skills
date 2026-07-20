# Slicing — the method

To-tickets' job is to split a decided direction into backlog-ready tickets with blocking edges, quizzing the
user until the split is approved, then publishing in dependency order. This file is the method.

## Read the direction — three inputs, one treatment

To-tickets splits a direction someone already decided. The input comes in one of three forms; all are read the
same way — mine the decided direction, the actors, and the full surface:

- **A spec** (the primary input) — `to-spec`'s output at `docs/specs/<name>.html` (a self-contained HTML deliverable; an older `.md` spec reads the same way), given as the command argument.
  This is the contract path; a repo may record a different specs location in its `docs/agents/`, honor it when
  present.
- **A legacy plan document** — a per-ticket design doc from the retired plan stage. Read it as direction for
  a single slice's worth of work, or a small cluster.
- **The raw current conversation** — when no spec or plan was written, mine the conversation and the
  codebase/project understanding built up in it.

**Never modify the source.** To-tickets reads the spec, plan, or parent issue; it never edits it. The source of
truth is preserved.

## Draft vertical slices — the default shape

The default output is **tracer-bullet tickets.** A tracer bullet is a **narrow-but-complete path through every
layer**: it touches whatever layers the change spans (data, logic, interface, whatever the stack is), does one
real thing end to end, and is **demoable on its own**. Size each to **one fresh context window** — small enough
that an agent picking it up cold can finish it without running out of room.

The anti-pattern is the **horizontal layer** — "all the models," then "all the logic," then "all the UI." A
horizontal ticket can't be demoed alone and doesn't derisk the whole path; a vertical slice proves the path
end to end early and often. Prefer the thinnest slice that still demonstrates a real capability.

## The wide-refactor exception

One kind of work resists a vertical slice: a **mechanical, high-blast-radius change** — renaming a symbol used
in a hundred places, migrating a call convention, swapping a dependency threaded through the codebase. Forcing
it into a "vertical slice" is a fiction; it is inherently horizontal. Sequence it instead as three phases:

1. **Expand** — introduce the new form alongside the old, so both work at once. One ticket.
2. **Migrate in batches** — move call sites over in reviewable batches, each its own ticket, each demoable
   (the batch compiles and passes with the new form). Batches can run in parallel once expand lands.
3. **Contract** — remove the old form once nothing uses it. One ticket, blocked on all the migrate batches.

The trigger is **both** conditions: the change is *mechanical* (little per-site judgement) **and** *high blast
radius* (touches many sites). A change that is wide but not mechanical — or mechanical but small — is a normal
vertical slice, not this exception.

## Quiz the user — the human-confirmation step

Unlike `to-spec`, which is pure synthesis and never interviews, **to-tickets interviews.** After drafting the
split, present it and **quiz the user** on the two things only they can settle:

- **Granularity** — are the slices the right size? Too coarse (a ticket that won't fit one context window, or
  bundles two demoable capabilities)? Too fine (tickets that only make sense together)?
- **Blocking edges** — what truly blocks what? Which tickets are independent and can run in parallel? Is the
  wide-refactor sequencing right?

**Iterate until approved.** This quiz *is* the human confirmation for the whole operation — **nothing publishes
before it is approved.** Draft the split into [templates/tickets.md](../templates/tickets.md) so the user has one
ordered artifact to react to, revise it against their feedback, and re-present until they sign off.

## Order and wire the edges

Once the split is approved, sort the tickets into **dependency order — blockers first.** This matters because
the tracker assigns an id at creation time: a ticket can only reference its blocker once that id exists, so
every blocker must be **created before its dependents.** Topologically sort the graph; publish in that order.

Wire each dependency **exactly as the repo's dependency playbook records it** (`docs/agents/backlog-policy.md`
§ Dependencies), so `backlog run` reads it and skips blocked work. Where the playbook records the tracker's
**native blocking relation** (this repo: GitHub `blocked_by`, written via the verified verbs in
`docs/agents/platform.md`), write the native edge — it renders the frontier in the tracker's own UI. Where it
records a body-line marker (`- [ ] depends on #N`) or `deps:` frontmatter instead, copy the playbook's
literal form — don't restyle it. The convention is a **project playbook**, not a `backlog` import: to-tickets
emits *into* it, so the playbook's wording is the authority.

## Audit each ticket for readiness

Before publishing, audit every approved ticket. Each must carry:

- **Observable acceptance** — criteria a verifier can exercise, not vibes.
- **Inherited context links** — the spec, its thin tracking ticket, and the decisions the slice relies on;
  a fresh context window must reach everything it needs from the ticket alone.
- **An authority boundary** — what the executor may decide (feeding backlog's route judgment and the
  just-in-time tactical plan) vs what is settled and must not be re-decided.
- **UX context, for UI surfaces** — the register, the key states (empty / loading / error / disabled /
  responsive), and links to `PRODUCT.md`/`DESIGN.md` where they exist.
- **True blocking edges only** — an edge that merely sequences convenience is not a blocker.

A ticket failing the audit is fixed or dropped — never published thin for grooming to repair later.

## Publish in the bound tracker's format

Create the tickets through the **tracker binding** recorded in `docs/agents/platform.md`, blockers first —
**never as local ticket files while a live tracker is bound**; on-disk tickets exist only when the recorded
binding itself is local. No recorded binding at all: state the gap and ask the user how to proceed — a
backlog needs a tracker, so publishing waits on that decision. Link each ticket to the spec's tracking
ticket when one exists. On
this repo that binding is GitHub via `gh` (`gh issue create --title '...' --body '...'`), and a ticket is a
GitHub issue. Publish the body from [templates/ticket.md](../templates/ticket.md), carrying the
dependency edges in the playbook's recorded form.

## Readiness alignment — leave it to groom

Do **not** auto-apply the `ready-for-agent` readiness role on a fresh split. The default is to **leave readiness
to `backlog groom`** — a fresh split is drafted work, not yet blessed for pickup, and grooming is where a human
confirms the shortlist (`backlog-policy.md` § Readiness decision). **Note the option** to apply readiness on
approval — the quiz *is* the human confirmation, so a user who wants it may bless
the tickets on the spot — but the recommended default, and what the skill does absent a request, is to leave it
to groom.

## No stale content

A ticket carries **no file paths and no code snippets.** They rot the moment the codebase moves; a ticket is
intent and the slice, not implementation — describe the module, the contract, or the shape in prose instead.

The single exception, carried from the plan/spec rule: a **prototype-validated snippet** that encodes a decision
more precisely than prose can — a state machine, a reducer, a schema, a type shape. Inline only that
decision-rich fragment and note it came from a prototype. Absent that exception, everything is prose.

## Vocabulary

Speak generically. A **ticket** is the unit of pickup-able work — exactly the tracker's "issue" role, in a
tracker-agnostic word. Never assume GitHub's "issue" in the skill's own text; the pair is deliberately
tracker-agnostic.
