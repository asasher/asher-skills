---
name: to-spec
description: Turn the current conversation into a spec — the direction document a design discussion earned but never wrote down. Pure synthesis, no interview; writes a self-contained HTML deliverable at docs/specs/<name>.html for to-tickets to split into tickets. Use when closing out a conversation that reached a decision. Not for eliciting requirements.
argument-hint: "[<name for the spec>]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: thread
  requires: []
  optional: [review-loop]
---

# To-Spec

To-spec owns one move: **take a conversation that already reached a decision and write the spec it earned.**
A long back-and-forth with the agent ends with a direction settled but nothing durable to hand off; the next
step — splitting that direction into pickup-able work — has nothing to read. To-spec closes that gap. It reads
the current conversation and the codebase/project understanding built up in it, captures what was **decided**,
and writes a **spec**: the high-level direction document that `to-tickets` later consumes. It is a synthesis
primitive, not an interviewer.

The defining constraint is **pure synthesis, no interview.** To-spec does not re-elicit requirements, does not
re-ask what the conversation already settled, and does not stall waiting on the user. It captures what's
decided and **flags what isn't in the spec's Notes** — an open question recorded is worth more here than a
question asked. Shipped as our own — no external skill is installed for this.

## Command surface

- **`to-spec [<name>]`** — synthesize the current conversation into a spec and write it to
  `docs/specs/<name>.html`. With no name, derive a short kebab-case one from the decided direction. This is
  the only command; invoked bare, it runs the synthesis.

Load [synthesis](reference/synthesis.md) for the method (what to mine, the no-interview rule, dev-vs-non-dev
gating, the no-stale-content rule, sign-off) and [template-guide](reference/template-guide.md) for what goes
in each section. The fillable scaffold is [templates/spec-skeleton.html](templates/spec-skeleton.html).

## How a spec gets written

The full method is in [synthesis](reference/synthesis.md); the shape:

1. **Mine, don't ask.** Read the conversation and the codebase/project understanding it built. When the
   conversation ran through the `interview` / `interview-with-docs` siblings, their crystallised artifacts —
   `CONTEXT.md` terms, ADRs, the exit classification of open threads — are the primary inputs: synthesis
   reads the record, not memory alone. Extract the problem, the decided solution, the decisions taken and
   the constraints that forced them. Anything left undecided becomes a line in **Notes**, never a question
   back to the user.
2. **Classify the work — dev or non-dev.** Our work isn't all software. A **dev spec** keeps the dev-only
   sections (Testing decisions, Test seams) and runs the seams step below; a **non-dev spec** skips both and
   uses only the core sections.
3. **For dev specs only — sketch the test seams.** Name the public seams the work would be tested at and
   **prefer the highest existing seam**. Skip this entirely for non-dev specs.
4. **Write the spec** from the skeleton into `docs/specs/<name>.html`, in generic vocabulary — a
   self-contained HTML deliverable with stable element ids, same house style as a plan.
5. **Audit fidelity, then classify the Notes.** Before sign-off: every material decision from the
   conversation appears in the spec, and every Notes line is classified **blocking** (must be settled
   upstream before tickets), **delegated** (the executor may choose; boundary named), or **deferred**
   (parked, with a home). A spec with an unclassified material Note, or an open blocking Note, must not
   feed `to-tickets`.
6. **Sign-off — the direction's approval gate.** There is no separate plan stage; the spec's approval *is*
   the gate, and per-ticket tactics are made just-in-time in execution. If the user is present, open the
   rendered spec and take approval inline. If they're AFK, serve it through the optional `review-loop`
   sibling (it is already review-ready HTML). **On approval:** commit the spec, and — when a live tracker
   is bound (`docs/agents/platform.md`) — create a **thin tracking ticket**: title, one-line gist, and a
   link to the canonical spec. Links and state, never content; `to-tickets` wires the slice tickets to it.

## What a spec is (and isn't)

- **Generic vocabulary.** A spec describes direction; `to-tickets` splits it into **tickets**. Say "spec" and
  "ticket" — never GitHub-specific "issue." The unit of downstream work is a ticket.
- **The artifact is a repo doc** at `docs/specs/<name>.html` — a self-contained HTML deliverable (stable
  element ids, no external fetches) that `to-tickets` consumes and `review-loop` can serve as-is. It is
  coarser than a plan: a plan is per-ticket and gated for approval before implementation; a spec is the
  pre-ticket direction the tickets are cut from.
- **No file paths or code snippets.** They rot as the codebase moves; the spec is direction, not
  implementation. The single exception — carried over from the plan/PRD rule — is a **prototype-validated
  snippet** that encodes a decision more precisely than prose can (a state machine, a schema, a type shape);
  inline only that decision-rich part and note it came from a prototype. Everything else is prose.
- **Adaptable to non-dev work.** The dev-only sections are optional; a spec for a process, a piece of content,
  or a decision uses the core sections alone.

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory: [synthesis](reference/synthesis.md)
  (the no-interview synthesis method, dev-vs-non-dev gating, the seams step, the no-stale-content rule, and
  sign-off) and [template-guide](reference/template-guide.md) (what each section holds and which are dev-only),
  plus the fillable scaffold [templates/spec-skeleton.html](templates/spec-skeleton.html). These are the authority; they import no
  other skill's files.
- **Project playbooks** — the repo's **spec conventions**: where specs live and the spec→ticket vocabulary.
  Defaults to `docs/specs/`; a repo may record a different location or naming rule in its `docs/agents/`. When
  the optional review-loop sign-off is used, the repo's **presentation-surface config** (its `docs/agents/`
  surface playbook) governs where the rendered spec is served.
- **Sibling skills** — **optional `review-loop` only.** When the user is AFK, to-spec presents the spec for
  sign-off through `review-loop`, composed by name — the spec is already a self-contained review-ready HTML
  with stable element ids, so it serves as-is. When the user is present, approval is inline. This is the sole
  sibling and it is **not** a hard dependency: skipping review-loop still produces a valid, committed spec.
  To-spec depends on no other skill.
