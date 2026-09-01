---
name: build-change
description: Take one unit of work — a ready ticket, or a spec'd piece of work with no ticket — to a review-ready change request. Use in a session of its own.
metadata:
  requires: [adversarial-review, implement, prove-your-work, to-subagent, verify-your-work]
  optional: [diagnosing-bugs, technical-writing]
---

# Build Change

Run one unit of work to a review-ready change request in one worktree. The unit is a ticket — the normal dispatched path — or a spec'd piece of work with no ticket. This session is the owner, the fixer, and the bookkeeper; the heavy lifting is dispatched, via the `to-subagent` skill, into fresh contexts. Record each stage's row as it lands — § The stage ledger.

**Stage dispatch is synchronous.** Every stage dispatch is a blocking call whose return is the stage's result. Stages that can run at once are several blocking calls in one turn — they run concurrently and return together. Never dispatch a stage to walk away from.

User-facing text — the change request description, reports, tracker comments — follows the `technical-writing` sibling. Absent it, write plainly and say the standard was not loaded.

## 0. Provision

Bring the worktree up per `docs/agents/environment.md` before any work: dependencies, environment files, migrations, the stack the checks need. Provision is done when the playbook's run recipes come up green — stack started, seed loaded, a check command exits 0. A gap here fails fast — report the blocker instead of letting verification discover it. While the build is live the worktree has **one writer** — this session and what it dispatches. It is also the one working copy for the entire pipeline: every subagent receives this exact directory.

## 1. Implement

With a ticket, read it through the platform verbs in `docs/agents/platform.md`, from this worktree — proving the read works where the work runs. A read that fails here is a blocker to report, never a cue to build from the dispatch prompt's paraphrase. Without a ticket, the spec handed to this session is the brief. Then dispatch the `implement` skill with it; the work lands as commits on this checkout's current branch.

## 2. Verify, then fix

Dispatch the `verify-your-work` skill against the changes — fresh eyes. The verifier reports; **this session fixes**: go red on the finding first, on the surface the verifier saw it fail — a browser finding gets a browser proof — then fix. A defect that survives a fix pass routes through the `diagnosing-bugs` skill instead of a second guess. Absent that sibling, say the `diagnosing-bugs` skill is not installed and run a deliberate diagnosis before any second fix attempt. Re-dispatch verification after fixing; loop until the report is clean.

## 3. Open the change request

Before opening the change request, the tree is clean: the branch carries only the intended changes, tool and probe residue gone, and every verification script the spec declared throwaway dropped — its run lives in the evidence.

Create the change request through the platform verbs. With a ticket, carry the ticket's closing reference (the platform's `Closes #N` form) so merging closes the ticket — unless this change targets a feature branch rather than the default branch, where the closing reference never fires: a slice's ticket closes at promotion, through the `Closes` lines the promotion change request carries. Without a ticket, name the spec (and its blessed hash where one exists) in the description — this change request is the record.

The description states what changed and why in the work's own terms — in the repo's change-description format (`docs/agents/change-description.md`) when one is recorded.

## 4. Adversarial review

Run the `adversarial-review` skill on the change request; it converges to LGTM or reports unresolved findings. Step 5 starts only when the change request stands at LGTM — fix unresolved findings through step 2's loop and re-run the review until it does.

## 5. Evidence

Dispatch the `prove-your-work` skill against the change request, handing over the stage ledger: the evidence package lands as a change request comment for whoever decides the merge. A defect discovered while assembling evidence stops the package — fix through step 2's loop, re-enter review, then re-assemble.

## Done

Report the change request as review-ready with a completion report: its URL and head SHA, the per-criterion verification verdicts and the review's converged outcome, the check commands with their exit codes, deviations from the brief with rationale, and residual risks or named gaps. With a ticket, the same outcome lands on the tracker as the claim's outcome comment — that is where the dispatcher and anyone else reads it. Merging waits for explicit human authorization.

## The stage ledger

Each stage's row records the stage (implement, each verify pass, each fix pass, each review pass), the tokens it consumed, and the harness quota percentage at that point where the harness exposes one — so cost review of a run is a read of the evidence. A dispatched stage's tokens come from its dispatch return's usage report; work this session does itself is covered by the harness's own usage surface where it has one. A number no surface reported is recorded as `unreported`.
