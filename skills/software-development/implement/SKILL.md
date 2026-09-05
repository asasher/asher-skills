---
name: implement
description: Implement one issue or spec'd work in the current checkout. Routes defects to diagnosing-bugs and new behavior to tdd; commits to the current branch.
metadata:
  requires: [diagnosing-bugs, domain-modeling, principle-codebase-design, principle-type-system-discipline, tdd]
  optional: [typescript-best-practices]
---

# Implement

Implement the work described in the issue or spec handed to this session, in the current checkout, on the current branch. Before editing, read `docs/agents/environment.md` § Checks where it exists: check commands, runner traps, conventions, and generated files live there.

## Route by the nature of the work

- **A defect** — something that should work and doesn't — runs through the `diagnosing-bugs` skill.
- **New behavior** — a feature, an enhancement — runs through the `tdd` skill at pre-agreed seams — that skill owns confirming them.

## While building

Apply `principle-codebase-design` when implementation details force a module or seam decision. Keep behavior behind the smallest sufficient interface and test it at that seam. In a statically typed codebase, apply `principle-type-system-discipline` to domain models and external boundaries. For TypeScript and TSX, also use `typescript-best-practices` when available.

Run the applicable typecheck, touched tests, formatter, linter, and dead-export checks before committing. For behavioral changes, run the full suite once after the final edit. For work proven to have no executable behavior or operational effect, use the relevant document or artifact checks and state why the other checks do not apply. Let each run finish before another uses the same mutable test state.

Honor the issue's authority boundary — what it settles is settled; what it delegates is yours to decide and worth a line in the commit message. When a settled item **collides with reality** — a repo convention, a sibling skill's rule, this session's constraints — stop and surface the collision on the issue or PR for a ruling; the same for scope the issue never granted, like patching third-party internals. A **load-bearing assumption** — from the spec's Assumptions list, or one the design visibly leans on — is checked against the code before building on it; a broken one is surfaced.

**Generated files** are regenerated via the recipe recorded in `docs/agents/environment.md`, never hand-edited; regeneration drift beyond the issue's scope is surfaced.

**Context files arrive already committed.** Shaping writes `CONTEXT.md` terms and ADRs on the issue's work branch, so this change inherits them — never re-land them. Work that was never shaped (issueless spec'd work, a term this change itself makes real) writes them directly via the `domain-modeling` skill as part of the change.

**A failure that predates the change** — proven by running the same check on the base commit, or with the change stashed — is pre-existing: file it as an issue and keep it out of this change's scope — the filed issue is what keeps it from being read as new breakage.

## Done

The applicable checks pass, apart from failures proven pre-existing and filed as issues, and changes are committed to the current branch with messages that say why. Return the resulting SHA, check commands and exit codes, decisions made within the brief, and any remaining risks. Preserve this report so a later fix pass can recover the implementation context.
