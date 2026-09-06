---
name: adversarial-review
description: Run one bounded verification, review, and fix loop on a PR; preserve its state across interruptions.
metadata:
  requires: [code-review, implement, to-subagent, verify-your-work]
---

# Adversarial review

Run the loop in the owning session. The owner verifies routine work and makes fixes; code review uses an independent context. Use [conduct](reference/conduct.md) for findings and fix discipline.

## State and risk

Read the PR's latest state: head/base, claims, risk, reports, consumed passes, deadline, and next actor. Default to three checking passes and one hour, bounded by the supplied deadline. Preserve counts and stops across resumes. Persist before dispatch and after each return.

- **Light:** no executable or operational effect. Relevant checks plus independent review; record why behavioral verification does not apply.
- **Normal:** verify behavior here with `verify-your-work`, then obtain independent review.
- **High:** auth, money, destructive data, or cross-surface interactions. Dispatch `verify-your-work` and review in separate contexts via `to-subagent`; run them together only when runtime state is isolated.

The brief may require stronger independence. Assess risk by behavioral and operational impact. A standalone code-only review explicitly reports that behavior was not verified.

## Loop

1. Pin the pushed head and current target base. Run verification in the context required by the risk level, and dispatch one independent `code-review` pass via `to-subagent`. Review reads source; the verifier owns runtime fixtures. Finish every checking pass before editing.
2. Join findings, including evidence or CI failures supplied after a prior convergence. Reject stale reports. Product questions and missing slice-sized work stop for a human ruling. Unverified claims stop unless explicitly waived at this head.
3. With no blocking findings, current verification, and a current-head LGTM, report convergence and CI status. Optional suggestions can remain. Otherwise run `implement` here on the findings, push the fix, and repeat only when budget remains for another checking pass.

Each dispatched checking round consumes one pass, even if interrupted. Resume at the recorded next actor; inspect an interrupted fix and retain the consumed budget. Every fix invalidates both verdicts. A late evidence or CI defect reopens this same loop.

At the bound, stop with findings. The owner may record a finite extension only when findings are resolving and narrowing, within the outer deadline; product questions still require a human ruling. Confirm timed-out workers stopped before any further writer.

Return and persist **converged**, **stopped at a bound**, **product question**, or **verification incomplete**, with revisions, reports, consumed budget, deadline, and next action. Required CI still gates review-readiness and merge.
