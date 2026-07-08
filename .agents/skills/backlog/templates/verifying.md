# Playbook: Verifying

> Project playbook for this repo. The backlog `verify` subskill reads this file for check commands and where acceptance criteria come from. How to run, isolate, seed, and authenticate against the app is in `environment.md`; the evidence contract lives in `evidence.md`.

## Checks

Run narrowest-first, then broaden by touched surface. This repo's commands (populate from `.intent/` or the package scripts if a catalog exists):

- Unit/targeted tests: _<e.g. `npm test -- <path>`>_.
- Lint: _<add yours>_.
- Type check: _<add yours>_.
- Build: _<add yours>_.
- Full / aggregate gate (before PR): _<e.g. a single `check` command that runs lint+typecheck+test>_.
- Independent second-opinion verification: _<default: delegate to `codex exec` per `environment.md` § Driving the app when a criterion needs real UI interaction, screenshots, or a runtime check outside the current context; checks the session can run directly stay local>_.

## Acceptance criteria

- Where criteria come from: the issue, and for an enhancement the approved plan's definition of done. The verifier writes them as explicit pass/fail checks against a running app.
- Repo-specific expectations every change must satisfy beyond the issue text: _<add yours, or "none">_.
