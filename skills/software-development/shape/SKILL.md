---
name: shape
description: Shape a batch of subjects — ideas or tickets — until each carries a blessed spec. Interviews the decisions, models the terms, researches what needs sources, prototypes what paper can't settle; a settled subject crystallises into a spec on its ticket automatically. Use when work needs shaping before anything builds on it.
argument-hint: "<idea or ticket id(s)>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [domain-modeling, interview, merge-changes, to-spec, worktree]
  optional: [prototype, research, to-backlog, to-slices, to-subagent, watch-until]
---

# Shape

Settle a batch of subjects' strategic decisions, ending each in a spec on its ticket. A **stateful composite**: everything it settles lands in durable artifacts — the ticket thread, `CONTEXT.md` terms, ADRs, the spec itself — and a resumed session reads those artifacts, never chat memory.

## Intake

Read each subject: the ticket thread and linked artifacts when it's a ticket (tickets whose decisions interlock are one subject, read together), the handed material when it's an idea, plus the **repo context files** — `CONTEXT.md`, and `PRODUCT.md`/`DESIGN.md` where they exist — and the project instruction file's `## Context documents` index for the documents whose clauses match. Seed each subject's decision tree with what is settled and what is open.

When backlog supplied a batch worktree, inspect it through the `worktree` skill and record the exact batch membership and branch. Every repository artifact produced during shaping stays in that worktree. Do not ask the harness or a subagent for another worktree; all engines receive the supplied directory.

## One engine per subject

A single subject runs inline. A batch of several runs one engine per subject — merely-related subjects never share one, interlocked tickets always do — each dispatched via the `to-subagent` skill, running the `interview` skill's engine mode. An interview round is then a dispatch cycle: engines return their frontiers per that mode's contract, this session combines the frontiers into **one round for the user**, then routes each subject's answers back into its engine's next dispatch. An engine whose frontier comes back empty crystallises (below) while its siblings still ask.

## The loop

- Run the `interview` skill on the subject — inline for a subject shaped in this session, its engine mode for a dispatched engine.
- Run the `domain-modeling` skill alongside: terms and ADR-worthy decisions are written the moment they crystallise, per its own contract.
- A question that needs source-backed investigation goes to the `research` skill; a question paper can't settle goes to the `prototype` skill — each dispatched via the `to-subagent` skill. A dispatched question blocks only what depends on it; results re-enter the frontier as evidence.
- When the subject is a ticket, record settled decisions on its thread as they land — the thread is the resume state.
- An item surfacing mid-thread that is real work but not a batch subject — a bug mentioned in passing, an adjacent idea — is offered to the `to-backlog` skill for capture, not absorbed into the subject or lost with the chat.

## Crystallise — the spec is the exit

When a subject's frontier is empty, run the `to-spec` skill on it — automatically, not on request: the spec lands on the subject's ticket, opening with a diagram (to-spec creates the ticket when the subject was only an idea). Posting a spec is a proposal, not a state change — readiness still waits for the user's blessing. A spec may end by recommending a split; executing one — the `to-slices` skill parenting the ticket, as capstone, over born-shaped child slices — happens only on the user's explicit approval, in a comment or here in the thread.

## Prepare the readiness gate

After every subject has a published spec, but before asking for readiness, compare the shaping branch to its recorded base. This is a branch-delta decision: include committed changes and tracked or untracked shaping artifacts; do not mistake a clean `git status` for an unchanged branch, and do not treat ignored environment residue as a shaping change.

If the branch has a repository delta, commit only this batch's shaping artifacts, open a shaping change request, and present its exact identity, head, and scope. State that a subsequent whole-batch readiness signal will authorize merging **that shaping change only**. A later repository tweak updates the change request and re-presents its new head before readiness can authorize it. If there is no repository delta, record that the clean branch will be removed when readiness is blessed.

## Done

Every subject in the batch carries a spec on its ticket, blessed by the user. Report what settled and what remains open. Lifecycle labels are never shape's judgment: shape stamps nothing on its own — it only executes the user's explicit calls: the readiness signal (below) and an approved split. Readiness is atomic for a backlog batch: no member leaves shaping before every member has finished the applicable branch lifecycle.

## After the spec — the comment watch

Once specs (and any approved split's tickets) are published and the user has gone AFK, the thread is not done. Run the `watch-until` skill on the spec'd tickets — condition: a new comment from the user, or an explicit readiness signal ("LGTM", "ready for agent"), in a comment or here in the thread. On a comment: apply the requested tweak to the ticket or spec, reply with what changed, resume watching.

On the readiness signal, note which spec revision the blessing covers, per to-spec's sign-off contract. A subject-scoped signal blesses only that subject's spec and the watch continues; the branch lifecycle begins only when the user has blessed every subject or explicitly signals readiness for the whole batch. Recompare the branch to the recorded base:

- If there is no repository delta, remove the working copy through the `worktree` skill, delete the now-unheld branch through the platform binding, verify both are gone, and apply the readiness role to every ticket in the batch. Ignored residue makes removal refuse; clean that named residue through its owning environment step and retry without force.
- If there is a repository delta and the exact current change-request head was presented **before** this readiness signal, invoke `merge-changes`, verify the recorded base contains the result, and apply readiness to the whole batch only after its worktree cleanup succeeds.
- If a repository delta has no presented change request at its current head, present or update it now and resume watching. The earlier signal is not retroactive merge authorization.

If another shaping change landed first, reconcile the later branch in its own worktree and rerun the affected checks before merge. Resolve only mechanical conflicts; a semantic conflict returns to the user and leaves the entire batch shaping. Any failed commit, change request, merge, verification, or cleanup likewise leaves every member shaping and preserves the worktree for recovery. The watch carries a timeout; when it reports timed out, surface the open state and stop.

## Resume

A fresh session on the same subject reads the record — ticket thread, the repo context files, ADRs — recomputes the frontier from what is still open, and re-asks nothing the record answers.

## Dependency surface

- **Siblings (required, by name):** `interview` (the questioning method), `domain-modeling` (terms and ADRs), `to-spec` (the crystalliser — the spec is shaping's exit), `worktree` (inspect and remove the supplied batch isolation), `merge-changes` (the changed-branch readiness gate). Absent one, state the requirement and stop.
- **Siblings (optional, by name):** `research` (source-backed questions), `prototype` (probes), `to-subagent` (their dispatch, and the batch's engines — absent it, shape the batch's subjects one at a time inline), `to-slices` (the approved split), `to-backlog` (capturing mid-thread items that aren't batch subjects), `watch-until` (the comment watch — absent it, say comments need an explicit ping). Absent one, park the affected work as open and say so; never silently skip.
- **Project surface:** the repo context files (`CONTEXT.md`, plus `PRODUCT.md`/`DESIGN.md` where they exist); the instruction file's `## Context documents` index; the tracker binding in `docs/agents/platform.md` when the subject is a ticket. Absent a tracker, idea shaping still works — the record lives in `CONTEXT.md`, ADRs, and the conversation.
