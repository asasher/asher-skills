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
the current branch. Before editing, read `docs/agents/codebase.md` where it exists — naming, placement,
harness seams, and check commands live there, and reading them first is what keeps them out of
mid-build discovery.

## Route by the nature of the work

- **A defect** — something that should work and doesn't — runs through the `diagnosing-bugs` skill: the
  feedback loop first, then the fix with its regression test.
- **New behavior** — a feature, an enhancement — runs through the `tdd` skill at pre-agreed seams: the
  ticket or spec's named seams, or seams proposed and recorded before the first test.

## While building

Run typechecking and the touched test files regularly; run the full suite once at the end — and let
each run finish before starting another in the same tree, since overlapping runs manufacture flaky
failures. Before that final gate, run the repo's formatter and linter (and dead-export check, where the
repo has one) over the touched files — the commands live in `docs/agents/codebase.md` where it exists.

Honor the ticket's authority boundary — what it settles is settled; what it delegates is yours to
decide and worth a line in the commit message. When a settled item **collides with reality** — a repo
convention, a sibling skill's rule, this session's constraints — stop and surface the collision on the
ticket or change request for a ruling; the same for scope the ticket never granted, like patching
third-party internals. A **load-bearing assumption** — from the spec's Assumptions list, or one the
design visibly leans on — is checked against the code before building on it; a broken one is surfaced.

**Generated files** are regenerated via the repo's recorded recipe (`docs/agents/codebase.md`), never
hand-edited; regeneration drift beyond the ticket's scope is surfaced, not silently retained.

**A failure that predates the change** — proven by running the same check on the base commit, or with
the change stashed — is pre-existing: report it and file a ticket so it gets fixed soon, and keep it
out of this build's scope. The report is what keeps it from being mistaken for new breakage.

## Done

The work compiles, the full suite passes — apart from failures proven pre-existing and reported as
above — and the changes are committed to the current branch with messages that say why, not just what.
