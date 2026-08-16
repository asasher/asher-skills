---
name: shape
description: Shape one subject — an idea or ticket — until it carries a spec blessed at a commit hash. Interviews the decisions, models the terms, researches what needs sources, prototypes what paper can't settle; a settled subject crystallises into a spec on its artifact branch automatically. Use when work needs shaping before anything builds on it.
argument-hint: "<idea or ticket id>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [domain-modeling, interview, to-spec, worktree]
  optional: [plain-language, prototype, research, to-backlog, to-slices, to-subagent, watch-until]
---

# Shape

Settle **one subject's** strategic decisions, ending in a spec blessed at a commit hash. One subject per thread. A **stateful composite**: everything it settles lands in durable artifacts — the ticket thread and the spec on its artifact branch — and a resumed session reads those artifacts, never chat memory.

A shaping thread **never merges anything.** Its repo output is the artifact branch (`artifact/<ticket>-<slug>`; `artifact/<slug>` when the subject is ticketless), never merged to main; its exit is the user's blessing at a hash; a clean worktree removal is the only teardown. Glossary terms and ADR drafts travel in the spec's **context delta** and reach main only through the build that makes them true — main's context files describe the code that is.

User-facing text follows the `plain-language` sibling — ASD-STE100 plain language, `CONTEXT.md` as the dictionary, no bare ticket or PR numbers. Absent it, write plainly and say the standard was not loaded.

## Intake

Read the subject: the ticket thread and linked artifacts when it's a ticket, the handed material when it's an idea, plus the **repo context files** — `CONTEXT.md`, and `PRODUCT.md`/`DESIGN.md` where they exist — and the project instruction file's `## Context documents` index for the documents whose clauses match. Seed the decision tree with what is settled and what is open.

When the dispatcher supplied a worktree, inspect it through the `worktree` skill and record the directory and branch. Every repository artifact produced during shaping stays in that worktree, on the subject's artifact branch.

## The loop

- Run the `interview` skill on the subject, inline in this thread.
- Run the `domain-modeling` skill alongside: terms and ADR-worthy decisions crystallise into the spec's **context delta**, per its own contract — never directly onto main during shaping.
- A question that needs source-backed investigation goes to the `research` skill; a question paper can't settle goes to the `prototype` skill — each dispatched via the `to-subagent` skill (absent it, run them inline). A dispatched question blocks only what depends on it; results re-enter the frontier as evidence, their artifacts landing on artifact branches with links in the record.
- When the subject is a ticket, record settled decisions on its thread as they land — the thread is the resume state.
- An item surfacing mid-thread that is real work but not this subject — a bug mentioned in passing, an adjacent idea — is offered to the `to-backlog` skill for capture, not absorbed into the subject or lost with the chat.

## Crystallise — the spec is the exit

When the subject's frontier is empty, run the `to-spec` skill on it — automatically, not on request. Per its contract: the spec is an HTML file on the subject's artifact branch, diagram first, canonical; the ticket gets the **projection** — a plain-language summary, the `to-web` render URL, and the commit hash it was rendered from (to-spec creates the ticket when the subject was only an idea). The spec declares the **context delta** and the **test split**. Posting a spec is a proposal, not a state change — readiness still waits for the user's blessing. A spec may end by recommending a split; executing one via the `to-slices` skill happens only on the user's explicit approval, in a comment or here in the thread.

## The comment watch

Once the spec is published and the user has gone AFK, the thread is not done. Run the `watch-until` skill on the spec'd ticket — condition: a new comment from the user, or an explicit readiness signal ("LGTM", "ready for agent"), in a comment or here in the thread. Absent that sibling, say comments need an explicit ping. On a comment: apply the requested tweak as a new commit on the artifact branch, refresh the ticket's projection, reply with what changed, resume watching. The watch carries a timeout; when it reports timed out, surface the open state and stop.

## Blessed at a hash

The user's readiness blessing records the **artifact-branch commit hash** it covers — the user blesses the spec they read, and a subject-scoped signal blesses exactly that hash. Any later commit past the blessed hash mechanically invalidates readiness; the changed spec needs a fresh blessing at its new hash. Lifecycle labels are never shape's judgment: shape stamps nothing on its own — it executes the user's explicit calls, the blessing and an approved split.

## Done

The subject carries a spec blessed at a hash. Report what settled and what remains open. Nothing merges: remove a supplied worktree through the `worktree` skill; the artifact branch stays as the record until it is spent.

## Re-entry

A blessed spec the code later contradicts returns its subject to shaping — the ticket goes back to needs-shaping and a fresh shape thread picks it up. Same engine, seeded by the contradiction.

## Resume

A fresh session on the same subject reads the record — the ticket thread, the artifact branch at its head, the repo context files — recomputes the frontier from what is still open, and re-asks nothing the record answers.

## Dependency surface

- **Siblings (required):** `interview` and `domain-modeling` (§ The loop), `to-spec` (§ Crystallise), `worktree` (§ Intake, § Done). Absent one, state the requirement and stop.
- **Siblings (optional):** `research`, `prototype`, `to-subagent`, `to-backlog` (§ The loop), `to-slices` (§ Crystallise), `watch-until` (§ The comment watch), `plain-language` (all user-facing text). Absent one, park the affected work as open and say so; never silently skip.
- **Project surface:** the repo context files and the `## Context documents` index (§ Intake); the tracker and branch bindings in `docs/agents/platform.md` when the subject is a ticket. Absent a tracker, idea shaping still works — the record lives on the artifact branch and in the raising conversation.
