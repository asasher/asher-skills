---
name: adversarial-review
description: Converge a change request to LGTM through driver-sequenced bounded passes — a reviewer that re-reviews until a pass finds nothing new, and a fixer that addresses findings until LGTM lands. Use once a change request exists and needs review pressure without a human in the loop.
argument-hint: "<change request>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [code-review, to-subagent]
  optional: [diagnosing-bugs]
---

# Adversarial Review

Two roles converge on one change request: a reviewer that re-reviews until a pass finds nothing new, and a fixer that addresses findings until LGTM lands. The change request is their only shared state — findings, fixes, and the verdict all live in its comments and commits, so any pass can die and the loop resumes from that record.

The session running this skill is the **driver**. Each role runs as one bounded pass dispatched via the `to-subagent` skill; a pass is a harness-tracked child, so its return is the wake that moves the loop — the roles never wait on each other, and nothing in the loop waits across a turn boundary.

Both briefs — comment conduct, the LGTM bar, iteration state, the product-semantics ruling — are in [conduct](reference/conduct.md); each dispatch carries it.

## The loop

Alternate bounded passes until a verdict:

1. **Review pass.** Dispatch the reviewer against the current head (conduct § Reviewer): it runs the `code-review` skill, posts each finding as an anchored change-request comment, persists its state, and returns its verdict — `LGTM` naming the head it covers, or the open findings.
2. On `LGTM`, the loop is converged: report it, naming the covered head.
3. **Fix pass.** Dispatch the fixer with the open findings (conduct § Fixer): it addresses every one — fix commit or reasoned pushback — pushes, replies to each comment, persists its state, and returns.
4. Review again, from step 1.

## Turn discipline

The driver holds the loop for its whole life and returns only with an outcome: **converged** (`LGTM`, the covered head SHA) or **stopped at a bound** (the open findings and which bound). Between dispatching a pass and reading its return there is nothing to watch and no poll to keep alive — the tracked child's completion is the wake. Ending the turn with the loop unconverged and unreported is a contract violation — a state comment records the loop's position, it does not keep the loop alive.

A pass that has returned is complete: act on its report. No confirmation follows a return — waiting for one blocks on a message that cannot arrive.

## Bounds

An iteration cap (default: three full review passes) and a timeout (named by whoever dispatched the review, defaulting to one hour), both enforced by the driver on the passes it dispatches. On either bound, stop and report the open findings as unresolved — a stuck convergence is a reported outcome, not an endless loop.

The driver names each pass's own bound at its dispatch, and treats a pass that outlives that bound as one that died. A pass that dies without returning is re-dispatched from the change request's persisted state (conduct § Shared rules), picking up at the next expected action.
