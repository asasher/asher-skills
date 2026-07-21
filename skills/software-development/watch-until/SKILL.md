---
name: watch-until
description: Watch a target — file, URL, tracker thread, CI run, review surface — until a condition holds, then relay what changed. Use to wait on external state without burning the session's attention on polling.
argument-hint: "<target, condition, and what to relay on trigger>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [to-subagent]
---

# Watch Until

Watch a target until a condition holds, relay what changed, stop.

## The spec of a watch

- **Target** — anything observable: a file, a URL, a tracker thread, a CI run, a review surface.
- **Condition** — decidable from the observation, whether mechanical ("a maintainer comment containing
  LGTM", "the run concluded", "the verdict block is filled in") or a judgment the watcher is equipped to
  make ("no unaddressed findings remain", "the iteration cap is reached"). State it so the watcher can
  decide it from what it observes.
- **Relay** — what to report on trigger. Quote the triggering observation; the watch observes and relays,
  it never acts on the content.
- **Deadline** — every watch has one. On expiry, report the last observed state; no watch runs forever.

## How to watch — cheapest that works

1. **Harness-tracked child.** If the target is a child this harness already tracks, do nothing —
   completion wakes you. Polling a tracked child is pure waste.
2. **Harness-native watch facilities** — a monitor or timer tool, a file-watch hook — where they exist.
3. **A watcher via the `to-subagent` sibling.** Its whole prompt is observe → check the condition →
   relay — the condition statement is the whole brief.
4. **Poll from this session**, at the cadence the target actually changes — an eight-minute CI run
   deserves one check near minute eight, not eight one-minute checks.
