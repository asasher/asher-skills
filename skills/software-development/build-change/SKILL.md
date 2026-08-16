---
name: build-change
description: Take one unit of work — a ready ticket, or a spec'd piece of work with no ticket — to a review-ready change request in one worktree: implement, verify and fix, open the change request, adversarial review, evidence. Use on a single unit of work in a session of its own.
argument-hint: "<ticket id or spec reference>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [adversarial-review, implement, prove-your-work, to-subagent, verify-your-work]
  optional: [diagnosing-bugs, writing-for-humans]
---

# Build Change

Run one unit of work to a review-ready change request in one worktree. The unit is a ticket — the normal dispatched path — or a spec'd piece of work with no ticket, in which case the change request is the record. This session is the owner, the fixer, and the bookkeeper; the heavy lifting is dispatched, via the `to-subagent` skill, into fresh contexts.

**Stage dispatch is synchronous.** Every stage dispatch is a blocking call whose return is the stage's result. Stages that can run at once are several blocking calls in one turn — they run concurrently and return together. Never dispatch a stage to walk away from and get notified later; nothing in this pipeline waits on a wake.

User-facing text — the change request description, reports, tracker comments — follows the `writing-for-humans` sibling: ASD-STE100 discipline, `CONTEXT.md` as the dictionary, no bare ticket or PR numbers.

## The stage ledger

Cost review of a run should be a read of the evidence, not an archaeology project — so this session keeps a per-stage token ledger alongside the pipeline. As each stage lands, record its row: the stage (implement, each verify pass, each fix pass, each review pass, evidence), the tokens it consumed, and the harness quota percentage at that point where the harness exposes one. A dispatched stage's tokens come from its dispatch return's usage report; work this session does itself is covered by the harness's own usage surface where it has one. A number no surface reported is recorded as `unreported` — an estimate is not accounting, and a dropped row hides exactly the cost spike the ledger exists to show. The finished ledger goes to step 5 with the evidence dispatch. The evidence stage's own row is the one entry this session cannot close; the evidence step adds it before posting.

## 0. Provision

Bring the worktree up per `docs/agents/environment.md` before any work: dependencies, environment files, migrations, the stack the checks need. A gap here fails fast — report the blocker instead of letting verification discover it. While the build is live the worktree has **one writer** — this session and what it dispatches. It is also the one working copy for the entire pipeline: every subagent receives this exact directory, and no stage requests harness-native or nested isolation.

## 1. Implement

With a ticket, read it through the platform verbs, from this worktree — proving the read works where the work runs. A read that fails here is a blocker to report, never a cue to build from the dispatch prompt's paraphrase. Without a ticket, the spec handed to this session is the brief. Then dispatch the `implement` skill with it; the work lands as commits on this checkout's current branch.

## 2. Verify, then fix

Dispatch the `verify-your-work` skill against the changes — fresh eyes, so the builder's assumptions don't verify themselves. The verifier reports; **this session fixes**: reproduce the finding as a failing check first, on the same surface the verifier saw it fail — a browser finding gets a browser proof — then fix. A defect that survives a fix pass routes through the `diagnosing-bugs` skill instead of a second guess. Re-dispatch verification after fixing; loop until the report is clean.

## 3. Open the change request

Create the change request through the platform verbs in `docs/agents/platform.md`. With a ticket, carry the ticket's closing reference (the platform's `Closes #N` form) so merging closes the ticket — unless this change targets a feature branch rather than the default branch, where the closing reference never fires: a slice's ticket closes at promotion, through the `Closes` lines the promotion change request carries. Without a ticket, name the spec (and its blessed hash where one exists) in the description — this change request is the record.

The description states what changed and why in the work's own terms — in the repo's change-description format (`docs/agents/change-description.md`) when one is recorded. Before opening it, the tree is clean: only the intended changes staged, tool and probe residue gone, and every verification script the spec declared throwaway dropped — its run lives in the evidence, its file never merges.

## 4. Adversarial review

Run the `adversarial-review` skill on the change request; it converges to LGTM or reports unresolved findings. Unresolved findings are this session's to settle before going further.

## 5. Evidence

Dispatch the `prove-your-work` skill against the change request, handing over the stage ledger: the evidence package lands as a change request comment for whoever decides the merge. A defect discovered while assembling evidence stops the package — fix through step 2's loop, re-enter review, then re-assemble.

## Done

Report the change request as review-ready with a completion report: its URL and head SHA, the verification and review outcomes per acceptance criterion, the gate commands with their exit codes, deviations from the brief with rationale, and residual risks or named gaps. With a ticket, the same outcome lands on the tracker as the claim's outcome comment — that is where the dispatcher and anyone else reads it; nobody is watching this session. Merging is not this session's call — it waits for explicit authorization.
