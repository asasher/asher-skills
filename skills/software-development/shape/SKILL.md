---
name: shape
description: Shape a batch of subjects — ideas or tickets — until each carries a blessed spec. Interviews the decisions, models the terms, researches what needs sources, prototypes what paper can't settle; a settled subject crystallises into a spec on its ticket automatically. Use when work needs shaping before anything builds on it.
argument-hint: "<idea or ticket id(s)>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [domain-modeling, interview, to-spec]
  optional: [prototype, research, to-subagent, to-tickets, watch-until]
---

# Shape

Settle a batch of subjects' strategic decisions, ending each in a spec on its ticket. A **stateful
composite**: everything it settles lands in durable artifacts — the ticket thread, `CONTEXT.md` terms,
ADRs, the spec itself — and a resumed session reads those artifacts, never chat memory.

## Intake

Read each subject: the ticket thread and linked artifacts when it's a ticket (tickets whose decisions
interlock are one subject, read together), the handed material when it's an idea, plus the **repo
context files** — `CONTEXT.md`, and `PRODUCT.md`/`DESIGN.md` where they exist — and the project
instruction file's `## Context documents` index for the documents whose clauses match. Seed each
subject's decision tree with what is settled and what is open.

## One engine per subject

A single subject runs inline. A batch of several runs one engine per subject — merely-related subjects
never share one, interlocked tickets always do — each dispatched via the `to-subagent` skill. Engines
are non-interactive, so an interview round is a dispatch cycle: each engine reads its subject's record,
computes its question frontier, and returns it; this session combines the frontiers into **one round
for the user**, questions tagged by subject, then routes the answers back and re-dispatches each engine
with its own. An engine whose frontier comes back empty crystallises (below) while its siblings still
ask.

## The loop

- Run the `interview` skill on the subject: frontier rounds, recommended answers, facts looked up rather
  than asked.
- Run the `domain-modeling` skill alongside: terms and ADR-worthy decisions are written the moment they
  crystallise, per its own contract.
- A question that needs source-backed investigation goes to the `research` skill; a question paper can't
  settle goes to the `prototype` skill — each dispatched via the `to-subagent` skill. A dispatched
  question blocks only what depends on it; results re-enter the frontier as evidence.
- When the subject is a ticket, record settled decisions on its thread as they land — the thread is the
  resume state.

## Crystallise — the spec is the exit

When a subject's frontier is empty, run the `to-spec` skill on it — automatically, not on request: the
spec lands on the subject's ticket, opening with a diagram (to-spec creates the ticket when the subject
was only an idea). Posting a spec is a proposal, not a state change — readiness still waits for the
user's blessing. A spec may end by recommending a split; executing one — the `to-tickets` skill
superseding the ticket with born-shaped children — happens only on the user's explicit approval, in a
comment or here in the thread.

## Done

Every subject in the batch carries a spec on its ticket, blessed by the user. Report what settled and
what remains open. Lifecycle labels are never shape's judgment: shape stamps nothing on its own — it
only executes the user's explicit calls: the readiness signal (below) and an approved split.

## After the spec — the comment watch

Once specs (and any approved split's tickets) are published and the user has gone AFK, the thread is not
done. Run the `watch-until` skill on the spec'd tickets —
condition: a new comment from the user, or an explicit readiness signal ("LGTM", "ready for agent"),
in a comment or here in the thread. On a comment: apply the requested tweak to the ticket or spec,
reply with what changed, resume watching. On the readiness signal: apply the readiness role per the
tracker's recorded label roles (`docs/agents/backlog-policy.md`) — the user's decision, executed. The watch carries a timeout; when it reports
timed out, surface the open state and stop.

## Resume

A fresh session on the same subject reads the record — ticket thread, the repo context files, ADRs —
recomputes the frontier from what is still open, and re-asks nothing the record answers.

## Dependency surface

- **Siblings (required, by name):** `interview` (the questioning method), `domain-modeling` (terms and
  ADRs), `to-spec` (the crystalliser — the spec is shaping's exit). Absent one, state the requirement
  and stop.
- **Siblings (optional, by name):** `research` (source-backed questions), `prototype` (probes),
  `to-subagent` (their dispatch, and the batch's engines — absent it, shape the batch's subjects one at
  a time inline), `to-tickets` (the approved split), `watch-until` (the comment watch — absent it,
  say comments need an explicit ping). Absent one, park the affected work as open and say so; never
  silently skip.
- **Project surface:** the repo context files (`CONTEXT.md`, plus `PRODUCT.md`/`DESIGN.md` where they
  exist); the instruction file's `## Context documents` index; the tracker binding in
  `docs/agents/platform.md` when the subject is a ticket. Absent a tracker, idea shaping still works —
  the record lives in `CONTEXT.md`, ADRs, and the conversation.
