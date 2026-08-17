# Slicing — the method

## Read the direction — one treatment for every input

To-slices splits a direction someone already decided. The input comes in one of these forms; all are read the same way — mine the decided direction, the actors, and the full surface:

- **A spec'd ticket** (the primary input) — a ticket whose projection carries the spec's summary, render URL, and blessed commit hash, given by id as the command argument. Read the spec file from the artifact branch **at the blessed hash** — the canonical direction — plus the ticket's comment trail for refinements the user made after the projection.
- **A spec document** — a spec file given by path when no tracker is bound. Read it exactly as the branch file: diagram first, the document canonical.
- **A plan document** — a per-ticket design doc. Read it as direction for a single slice's worth of work, or a small cluster.
- **The raw current conversation** — when no spec or plan was written, mine the conversation and the codebase/project understanding built up in it.

**Never modify the spec text.** To-slices reads the spec, plan, or parent ticket; it never edits the direction itself. Parenting a split ticket over its slices (below) changes tracker state, not spec content.

## Draft vertical slices — the default shape

The default output is **tracer-bullet tickets.** A **slice** is a **narrow-but-complete path through every layer** the change spans (data, logic, interface, whatever the stack is): it does one real thing end to end and is **demoable on its own**. **Tracer bullet** is the sizing bar on top: **one fresh context window** — small enough that an agent picking it up cold can finish it without running out of room.

The anti-pattern is the **horizontal layer** — "all the models," then "all the logic," then "all the UI." A horizontal ticket can't be demoed alone and doesn't derisk the whole path; a vertical slice proves the path end to end early and often. Prefer the thinnest slice that still demonstrates a real capability.

The draft is complete when every requirement in the direction maps to a slice — walk the direction's acceptance criteria (the spec's list when one exists, else the requirements mined in § Read the direction) and account for each; anything unassigned is a missing slice or a named exclusion the user approves.

**Every slice carries its rationale** — one or two sentences: why this boundary, and why the slice is demoable alone.

## The wide-refactor exception

One kind of work resists a vertical slice: a **mechanical, high-blast-radius change** — renaming a symbol used in a hundred places, migrating a call convention, swapping a dependency threaded through the codebase. Forcing it into a "vertical slice" is a fiction; it is inherently horizontal. Sequence it instead as three phases:

1. **Expand** — introduce the new form alongside the old, so both work at once. One ticket.
2. **Migrate in batches** — move call sites over in reviewable batches, each its own ticket, each demoable (the batch compiles and passes with the new form). Batches can run in parallel once expand lands.
3. **Contract** — remove the old form once nothing uses it. One ticket, blocked on all the migrate batches.

The trigger is **both** conditions: the change is _mechanical_ (little per-site judgement) **and** _high blast radius_ (touches many sites). A change that is wide but not mechanical — or mechanical but small — is a normal vertical slice, not this exception.

## The landing shape — a to-slices decision

The split also chooses how the slices land, recommended with justification like every other cut:

- **Stacked** (the default for split specs) — the spec ticket gets a **feature branch** off main whose **root commit is the context delta** (the `CONTEXT.md` terms and ADR drafts, derived from the blessed spec). Slices branch off it and open change requests into it, inheriting the language from birth. The spec ticket's own change request is the feature→main merge — one ticket, one change request — and the parent's coverage check is the review of exactly that change request. Main receives the vocabulary atomically, when the whole direction becomes true. A slice's change request merging into the feature branch earns the slice the **`delivered`** role — applied in the same act as the merge — and the slices close natively at promotion via one `Closes` line per slice on the parent's change request, which targets main.
- **Direct** — independent slices open change requests straight to main. The first slice carries the context delta and is wired as a blocker of the rest. The justified exception, for slices that genuinely don't interlock — it keeps tracer-bullet continuous integration.

State the recommendation and its reasons in the draft; the user edits it like any boundary.

## Present the recommendation — the confirmation gate

**To-slices recommends; the user edits.** Present the split draft (template-guide § The split draft). The user reacts to reasons — moving a boundary, cutting an edge, overriding the landing shape — and the draft is revised and re-presented until they approve.

**Nothing publishes before approval.** One gate confirms the whole operation.

## Order and wire the edges

Once the split is approved, sort the tickets into **dependency order — blockers first.** This matters because the tracker assigns an id at creation time: a ticket can only reference its blocker once that id exists, so every blocker must be **created before its dependents.** Topologically sort the graph; publish in that order.

Wire each dependency **exactly as the dependency convention the repo's playbook records** (`docs/agents/backlog-policy.md` § Dependencies), so downstream scheduling reads it and skips blocked work. Where the playbook records the tracker's **native blocking relation** (e.g. GitHub `blocked_by`, written via the verbs in `docs/agents/platform.md`), write the native edge — it renders the blocking structure in the tracker's own UI. Where it records a body-line marker (`- [ ] depends on #N`) or `deps:` frontmatter instead, copy the playbook's literal form — don't restyle it. The convention is the **project playbook's**: to-slices emits _into_ it, so the playbook's wording is the authority.

## Audit each ticket — backlog-ready or not published

Before publishing, audit every approved ticket. Each must carry:

- **Observable acceptance** — criteria a verifier can exercise, not vibes.
- **Inherited context links** — the spec (its ticket and blessed hash) and the decisions the slice relies on; a fresh context window must reach everything it needs from the ticket alone.
- **An authority boundary** — what the executor may decide vs what is settled and must not be re-decided.
- **UX context, for UI surfaces** — the register, the key states (empty / loading / error / disabled / responsive), and links to `PRODUCT.md`/`DESIGN.md` where they exist.
- **True blocking edges only** — an edge that merely sequences convenience is not a blocker.

A ticket failing the audit is fixed or dropped — never published thin for grooming to repair later.

## Publish in the bound tracker's format

Create the tickets through the **tracker binding** recorded in `docs/agents/platform.md`, blockers first — **never as local ticket files while a live tracker is bound**; on-disk tickets exist only when the recorded binding itself is local. No recorded binding at all: state the gap and ask the user how to proceed — a backlog needs a tracker, so publishing waits on that decision. Link each ticket to the spec's ticket when one exists. Publish each body per template-guide § A single ticket.

## Parent the slices

When the input was a spec'd ticket, the slices carry the installments but the parent keeps the whole — finish by **parenting it over them**:

- **Attach every slice as a child** of the parent, through the parent/child relation the platform playbook records (`docs/agents/platform.md` — the tracker's native sub-issue relation where it has one, else the playbook's recorded form). The relation is load-bearing: the backlog policy's open-children rule reads it, keeping the parent undispatchable while any child is open and undelivered — no per-slice blocking edges are wired for this.
- **Convert the parent to the `spec` work-type** per the label roles (`docs/agents/backlog-policy.md` § Label roles), replacing its previous work-type. The parent's remaining work is the coverage check that role names: when the open-children rule clears, the dispatched session verifies the delivered slices against the spec — filing any gap as a new child (which re-blocks the parent) or, on a clean pass, landing the promotion (§ The landing shape).
- **Post a pointer comment** on the parent linking every child, so anyone landing on it sees the split. Each child links back to the parent in turn (§ Audit — inherited context links): the parent's spec remains the direction record the slices inherit from, live for as long as they build.

The parent's readiness role is left as it stands — the open-children rule, not a label change, is what keeps it out of the build sweep. A slice discovered later (a mid-build capture, a gap the coverage check finds) is attached as a child the same way and re-blocks the parent by existing. A source that was _not_ a ticket (a spec document, a plan, the conversation) has nothing to parent — skip this step.

## Readiness — leave it unset

Leave the readiness role unset on a fresh split — drafted work is not yet blessed for pickup, and the readiness decision and who makes it are recorded in `backlog-policy.md` § Readiness decision. **Note the option** to apply readiness on approval — the confirmation gate _is_ a human confirmation, so a user who wants it may bless the tickets on the spot.

## No stale content

A ticket carries **no file paths and no code snippets.** They rot the moment the codebase moves; a ticket is intent and the slice, not implementation — describe the module, the contract, or the shape in prose instead.

The single exception: a **prototype-validated snippet** that encodes a decision more precisely than prose can — a state machine, a reducer, a schema, a type shape. Inline only that decision-rich fragment and note it came from a prototype. Absent that exception, everything is prose.
