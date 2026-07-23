---
name: adversarial-review
description: Converge a change request to LGTM through two independent agents — a reviewer that re-reviews until a pass finds nothing new, and a fixer that addresses findings until LGTM lands. Use once a change request exists and needs review pressure without a human in the loop.
argument-hint: "<change request>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [code-review, to-subagent, watch-until]
  optional: []
---

# Adversarial Review

Two agents converge on one change request. The change request is their only shared state — findings,
fixes, and the verdict all live in its comments and commits, so either side can die and be respawned
without losing the loop. Dispatch both via the `to-subagent` skill, concurrently.

Both briefs — comment conduct, the LGTM bar, iteration state, the product-semantics escalation — are in
[conduct](reference/conduct.md); each dispatch carries it.

## The reviewer

Run the `code-review` skill against the change request; post each finding as a change request comment
anchored to its file and line. Then run the `watch-until` skill on the change request — condition: new
commits since the reviewed head. On trigger, review again. When a full pass yields **no new findings and
every prior finding is addressed**, post `LGTM` and stop.

## The fixer

Run the `watch-until` skill on the change request — condition: unaddressed review comments exist. On
trigger, fix each finding (or push back in a reply with the reason a finding is wrong — disagreement is
addressed too, silence is not), push, and reply to each comment with what was done. Resume watching.
When `LGTM` lands, stop.

## Bounds

Both sides carry the same timeout and an iteration cap (default: three full review passes). On either
bound, stop and report the open findings as unresolved — a stuck convergence is a reported outcome, not
an endless loop.
