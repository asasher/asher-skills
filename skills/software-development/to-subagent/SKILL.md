---
name: to-subagent
description: Dispatch a unit of non-interactive work to a subagent — staffed from the roster, isolated when it edits files, with a wake path. Use whenever work should run outside this session without the user attending it.
argument-hint: "<the unit of work to dispatch>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [staffing]
---

# To Subagent

Dispatch a unit of work to a non-interactive agent and relay its result. This is the one place staffing
and dispatch mechanics live — other skills say "via `to-subagent`" and stop there.

## Staffing

Pick the subagent's model and effort from the staffing roster (the `staffing` sibling: the machine's
global module plus the repo's deltas), matched to the kind of work — mechanical, review, orchestration.
Absent the roster, run the subagent on this session's own model and effort; never downgrade on a guess.

## The prompt

Self-contained — the subagent sees nothing of this conversation. State the goal, the inputs by path or
id, what done looks like, and that its final message is the deliverable itself: the data asked for, not a
status note. When the result must be structured, state the exact shape.

## Isolation

Work that edits files this session or a parallel subagent may also touch gets its own worktree. Read-only
work runs in place.

## Wake path

Prefer the harness-tracked child: its completion wakes the dispatcher, so never poll it. Work the harness
cannot track (an external process, another harness) follows the roster's wake-path ladder — a floor-model
watcher at low effort. With neither, poll at the cadence the work actually changes.

## Relay

Report the result in this session's own words at the altitude the next decision needs — never a pasted
transcript. A subagent that died or came back empty is a reported outcome, not a silent gap.
