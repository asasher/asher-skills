---
name: build
description: Take one ready ticket from checkout to a review-ready change request — implement, verify and fix, open the change request, adversarial review, evidence. Use on a single ticket in a session of its own.
argument-hint: "<ticket id>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [adversarial-review, implement, prove-your-work, to-subagent, verify-your-work]
  optional: []
---

# Build

Run one ticket to a review-ready change request. This session is the owner and the fixer; the heavy
lifting is dispatched, via the `to-subagent` skill, into fresh contexts.

## 1. Implement

Read the ticket; dispatch the `implement` skill with it. The work lands as commits on this checkout's
current branch.

## 2. Verify, then fix

Dispatch the `verify-your-work` skill against the changes — fresh eyes, so the builder's assumptions
don't verify themselves. The verifier reports; **this session fixes**. Re-dispatch verification after
fixing; loop until the report is clean.

## 3. Open the change request

Create the change request through the platform verbs in `docs/agents/platform.md`, carrying the ticket's
closing reference (the platform's `Closes #N` form) so merging closes the ticket. The description states
what changed and why in the ticket's terms.

## 4. Adversarial review

Run the `adversarial-review` skill on the change request; it converges to LGTM or reports unresolved
findings. Unresolved findings are this session's to settle before going further.

## 5. Evidence

Dispatch the `prove-your-work` skill against the change request: the evidence package lands as a change
request comment for whoever decides the merge.

## Done

Report the change request as review-ready: its URL, the verification and review outcomes, and any named
gaps. Merging is not this session's call — it waits for explicit authorization.
