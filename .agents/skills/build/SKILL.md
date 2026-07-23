---
name: build
description: Take one ready ticket from checkout to a review-ready change request — implement, verify and fix, open the change request, adversarial review, evidence. Use on a single ticket in a session of its own.
argument-hint: "<ticket id>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [adversarial-review, implement, prove-your-work, to-subagent, verify-your-work]
  optional: [diagnosing-bugs]
---

# Build

Run one ticket to a review-ready change request. This session is the owner and the fixer; the heavy
lifting is dispatched, via the `to-subagent` skill, into fresh contexts.

## 0. Provision

Bring the worktree up per `docs/agents/environment.md` before any work: dependencies, environment
files, migrations, the stack the checks need. A gap here fails fast — report the blocker instead of
letting verification discover it. While the build is live the worktree has **one writer** — this
session and what it dispatches.

## 1. Implement

Read the ticket through the platform verbs, from this worktree — proving the read works where the work
runs. A read that fails here is a blocker to report, never a cue to build from the dispatch prompt's
paraphrase. Then dispatch the `implement` skill with it; the work lands as commits on this checkout's
current branch.

## 2. Verify, then fix

Dispatch the `verify-your-work` skill against the changes — fresh eyes, so the builder's assumptions
don't verify themselves. The verifier reports; **this session fixes**: reproduce the finding as a
failing check first, on the same surface the verifier saw it fail — a browser finding gets a browser
proof — then fix. A defect that survives a fix pass routes through the `diagnosing-bugs` skill instead
of a second guess. Re-dispatch verification after fixing; loop until the report is clean.

## 3. Open the change request

Create the change request through the platform verbs in `docs/agents/platform.md`, carrying the ticket's
closing reference (the platform's `Closes #N` form) so merging closes the ticket. The description states
what changed and why in the ticket's terms — in the repo's change-description format
(`docs/agents/change-description.md`) when one is recorded. Before opening it, the tree is clean: only
the intended changes staged, tool and probe residue gone.

## 4. Adversarial review

Run the `adversarial-review` skill on the change request; it converges to LGTM or reports unresolved
findings. Unresolved findings are this session's to settle before going further.

## 5. Evidence

Dispatch the `prove-your-work` skill against the change request: the evidence package lands as a change
request comment for whoever decides the merge. A defect discovered while assembling evidence stops the
package — fix through step 2's loop, re-enter review, then re-assemble.

## Done

Report the change request as review-ready with a completion report: its URL and head SHA, the
verification and review outcomes per acceptance criterion, the gate commands with their exit codes,
deviations from the ticket with rationale, and residual risks or named gaps. Merging is not this
session's call — it waits for explicit authorization.
