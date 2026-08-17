---
name: watch-until
description: Watch a target until a condition holds or its timeout expires, then relay the outcome. Use when the session must wait on external state.
argument-hint: "<target, condition, timeout, and what to relay on trigger>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [to-subagent]
---

# Watch Until

## The brief of a watch

- **Target** — anything observable: a file, a URL, a tracker thread, a CI run, a review surface.
- **Condition** — decidable from the observation, whether mechanical ("a maintainer comment containing LGTM", "the run concluded", "the verdict block is filled in") or a judgment the watcher is equipped to make ("no unaddressed findings remain", "the discussion has settled").
- **Relay** — what to report on trigger. Quote the triggering observation; the watch observes and relays, it never acts on the content.
- **Timeout** — every watch takes one. On expiry the watch reports **timed out** — the condition unmet, plus the last observed state; what happens next is outside the watch.

## How to watch — cheapest that works

Work down the ladder and take the first rung available to you.

1. **Harness-tracked child.** If the harness itself notifies you when the target completes, the notification is the observation — check the condition against it and relay per the brief.
2. **Harness-native watch facilities** — a monitor or timer tool, a file-watch hook — where they exist.
3. **A watcher via the `to-subagent` sibling.** Its prompt is the watch's brief — nothing else. Absent the sibling, fall to rung 4.
4. **Poll from this session**, at the cadence the target actually changes — an eight-minute CI run deserves one check near minute eight.
