---
name: implement
description: Implement one ticket or spec'd piece of work in the current checkout. Routes defects to diagnosis and new behavior to test-first construction; commits to the current branch.
argument-hint: "<ticket id or spec reference>"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: [diagnosing-bugs, tdd]
  optional: []
---

# Implement

Implement the work described in the ticket or spec handed to this session, in the current checkout, on
the current branch.

## Route by the nature of the work

- **A defect** — something that should work and doesn't — runs through the `diagnosing-bugs` skill: the
  feedback loop first, then the fix with its regression test.
- **New behavior** — a feature, an enhancement — runs through the `tdd` skill at pre-agreed seams: the
  ticket or spec's named seams, or seams proposed and recorded before the first test.

## While building

Run typechecking and the touched test files regularly; run the full suite once at the end. Honor the
ticket's authority boundary — what it settles is settled; what it delegates is yours to decide and worth
a line in the commit message.

## Done

The work compiles, the full suite passes, and the changes are committed to the current branch with
messages that say why, not just what.
