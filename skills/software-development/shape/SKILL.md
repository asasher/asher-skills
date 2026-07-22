---
name: shape
description: Shape one subject — an idea or a ticket — until its strategic decisions are settled. Interviews the decisions, models the terms, researches what needs sources, prototypes what paper can't settle. Use when work needs shaping before anything builds on it.
argument-hint: "<idea or ticket id(s)>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [domain-modeling, interview]
  optional: [prototype, research, to-subagent, watch-until]
---

# Shape

Settle one subject's strategic decisions. A **stateful composite**: everything it settles lands in
durable artifacts — the ticket thread, `CONTEXT.md` terms, ADRs — and a resumed session reads those
artifacts, never chat memory.

## Intake

Read the subject: the ticket thread and linked artifacts when it's a ticket (several tickets grouped into
one subject read together), the handed material when it's an idea, plus the project instruction file's
`## Context documents` index and the documents whose clauses match. Seed the decision tree with what is
settled and what is open.

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

## Done

The interview's stopping rule holds: frontier empty, and the user confirms shared understanding. Report
what settled and what remains open. Crystallising the direction — a spec, tickets, or straight to a
build — is the user's call. Lifecycle labels are never shape's judgment: shape stamps nothing on its
own — it only executes the user's explicit readiness call when one arrives (below).

## After crystallisation — the comment watch

When the user has crystallised — a spec committed, tickets published — and gone AFK, the thread is not
done. Run the `watch-until` skill on the published tickets (and the spec's tracking ticket) —
condition: a new comment from the user, or an explicit readiness signal ("LGTM", "ready for agent"),
in a comment or here in the thread. On a comment: apply the requested tweak to the ticket or spec,
reply with what changed, resume watching. On the readiness signal: apply the readiness role per the
tracker's label roles — the user's decision, executed. The watch carries a deadline; on expiry, report
the open state and stop.

## Resume

A fresh session on the same subject reads the record — ticket thread, `CONTEXT.md`, ADRs — recomputes
the frontier from what is still open, and re-asks nothing the record answers.

## Dependency surface

- **Siblings (required, by name):** `interview` (the questioning method), `domain-modeling` (terms and
  ADRs). Absent one, state the requirement and stop.
- **Siblings (optional, by name):** `research` (source-backed questions), `prototype` (probes),
  `to-subagent` (their dispatch), `watch-until` (the post-crystallisation comment watch — absent it,
  say comments need an explicit ping). Absent one, park the affected work as open and say so; never
  silently skip.
- **Project surface:** the instruction file's `## Context documents` index; the tracker binding in
  `docs/agents/platform.md` when the subject is a ticket. Absent a tracker, idea shaping still works —
  the record lives in `CONTEXT.md`, ADRs, and the playback.
