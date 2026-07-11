# Playbook: Verifying

> Project playbook for this repo. The backlog `verify` subskill reads this file for check commands and where acceptance criteria come from. How to run, isolate, seed, and authenticate against the app is in `environment.md`; the evidence contract lives in `evidence.md`.

## Checks

Run narrowest-first, then broaden by touched surface. `setup` **discovers these from the repo and verifies each invocation by running it** — from `.intent/`, `package.json` scripts, a `Makefile`/`Justfile`, `pyproject.toml`/`tox.ini`, `Cargo.toml`, gradle/maven, etc. — recording only commands it has seen launch and execute the check, verbatim. Judge the invocation, not the exit code: a command that runs but reports failures (a currently-red suite) is still the real gate — record it with its baseline status, do not blank it. Only a missing script, a typo, or the wrong runner is omitted. A command that needs the running stack is confirmed with the stack up (`environment.md`). Do not record a guessed command.

- Unit/targeted tests: _<the verified command, e.g. `npm test -- <path>`>_.
- Lint: _<verified, or blank>_.
- Type check: _<verified, or blank>_.
- Build: _<verified, or blank>_.
- Full / aggregate gate (before PR): _<e.g. a single `check` command that runs lint+typecheck+test>_.
- Independent second-opinion verification: _<default: delegate to `codex exec` per `environment.md` § Driving the app when a criterion needs real UI interaction, screenshots, or a runtime check outside the current context; checks the session can run directly stay local>_.

## CI merge gate

> The host CI's required checks — the gate that blocks the merge, distinct from the local checks above. `setup` discovers this from the CI config (e.g. `.github/workflows/*.yml`, required status checks); `verify` and the PR step read it (`change-description.md`).

- The check set CI runs to gate a merge: _<the required jobs, or "none — no CI">_.
- Where CI diverges from the local commands: _<note any check CI runs that the local gate doesn't, or "same">_.
- Merge precondition: the PR is not mergeable until this CI gate is green. Local checks prove the change; CI-green is the merge condition — neither substitutes for the other.

## Acceptance criteria

- Where criteria come from: the issue, and for an enhancement the approved plan's definition of done. The verifier writes them as explicit pass/fail checks against a running app.
- Repo-specific expectations every change must satisfy beyond the issue text: _<add yours, or "none">_.
