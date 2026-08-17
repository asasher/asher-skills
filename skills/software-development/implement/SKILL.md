---
name: implement
description: Implement one ticket or spec'd work in the current checkout. Routes defects to diagnosing-bugs and new behavior to tdd; commits to the current branch.
argument-hint: "<ticket id or spec reference>"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: [diagnosing-bugs, tdd]
  optional: []
---

# Implement

Implement the work described in the ticket or spec handed to this session, in the current checkout, on the current branch. Before editing, read `docs/agents/codebase.md` where it exists — naming, placement, harness seams, and check commands live there.

## Route by the nature of the work

- **A defect** — something that should work and doesn't — runs through the `diagnosing-bugs` skill.
- **New behavior** — a feature, an enhancement — runs through the `tdd` skill at pre-agreed seams — that skill owns confirming them.

## While building

Run typechecking and the touched test files before each commit; then the repo's formatter and linter (and dead-export check, where the repo has one) over the touched files; then the full suite once — and let each run finish before starting another in the same tree, since overlapping runs manufacture flaky failures.

Honor the ticket's authority boundary — what it settles is settled; what it delegates is yours to decide and worth a line in the commit message. When a settled item **collides with reality** — a repo convention, a sibling skill's rule, this session's constraints — stop and surface the collision on the ticket or change request for a ruling; the same for scope the ticket never granted, like patching third-party internals. A **load-bearing assumption** — from the spec's Assumptions list, or one the design visibly leans on — is checked against the code before building on it; a broken one is surfaced.

**Generated files** are regenerated via the repo's recorded recipe (`docs/agents/codebase.md`), never hand-edited; regeneration drift beyond the ticket's scope is surfaced.

**The spec's context delta** — new `CONTEXT.md` terms, ADR drafts — lands on main with the change that makes it true. An unsplit ticket writes the terms into `CONTEXT.md` and the drafts into `docs/adr/` as part of this change. On a stacked slice the delta already sits at the feature branch's root commit — leave it there; landing it again duplicates it.

**A failure that predates the change** — proven by running the same check on the base commit, or with the change stashed — is pre-existing: file it as a ticket and keep it out of this change's scope — the filed ticket is what keeps it from being read as new breakage.

## Done

The typecheck passes, the recorded format, lint, and dead-export checks (where the repo has them) pass clean, the full suite passes — apart from failures proven pre-existing and filed as tickets — the spec's context delta is landed where this ticket owns it, and the changes are committed to the current branch with messages that say why.
