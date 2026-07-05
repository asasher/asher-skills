# Playbook: Refactoring

> Project playbook for this repo. The triage `refactor` subskill reads this file for the technique; the gates are in the skill's `reference/refactor.md`. Tailor the **This repo** section; replace the technique with house practice if this team refactors differently.

## Lock behavior first

- Before touching implementation, pin the behavior that must not change with tests at the public seams of the surface being refactored — the interfaces callers actually use, not the internals that are about to move. Tests coupled to the current structure will break on the refactor and tell you nothing.
- Characterization tests follow the same standards as `implementing.md` § Tests worth keeping: behavior through public interfaces, expected values from an independent source of truth, mocks only at system boundaries.
- If the surface has no testable seam, creating one is the first refactor — a separate, minimal step of its own.
- If the surface has no logic to lock — pure presentation, judged per `implementing.md` § What deserves a test — the net is visual comparison through the verify step instead of characterization tests. Say so explicitly rather than writing tests that pin pixels.

## Refactor under the net

- Small, reversible moves, with the locked tests green at each step — not just at the end. A red step means back out and re-approach, not push through.
- Never change behavior and structure in the same commit.

## Done when

- The diff is behavior-preserving, the locked tests pass **unmodified**, and the repo's required checks (see `verifying.md`) are green. A locked test you had to edit is a behavior change — call it out and justify it.

## This repo

- Test framework and command: _<add yours>_.
- Conventions this repo cares about (naming, module boundaries, file layout): _<add yours>_.
