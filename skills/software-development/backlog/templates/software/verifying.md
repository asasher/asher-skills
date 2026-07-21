# Playbook: Verifying

> Project playbook for this repo. The backlog `verify` subskill reads this file for check commands and where acceptance criteria come from. How to run, isolate, seed, and authenticate against the app is in `environment.md`; the evidence contract lives in `evidence.md`.

## Checks

Run narrowest-first, then broaden by touched surface. Discovered and invocation-verified by `backlog setup` (its step 5 contract): verbatim, seen-to-run commands only; a currently-red command is still the real gate — recorded with its baseline status, never blanked; a stack-dependent check is confirmed with the stack up (`environment.md`). Do not record a guessed command.

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

- Where criteria come from — by entryway, since the dev tail is invariant but its inputs are not:
  - a ticketed run: the ticket's acceptance block (inheriting its spec's per-slice acceptance);
  - a spec without tickets: the spec's acceptance for the slice being built;
  - interactive chat-and-build: the criteria the build loop recorded in the issue thread at loop start
    (the PR body carries them from creation) — verify
    always has a target, even without a ticket.
  The verifier writes them as explicit pass/fail checks against a running app.
- Evidence obligation scales with absence (`evidence.md`): an AFK run owes the full evidence package —
  nobody watched; interactive work may degrade to the PR body's verification grades where the playbook
  allows — the human witnessed the behavior live.
- Repo-specific expectations every change must satisfy beyond the issue text: _<add yours, or "none">_.

## UI surfaces

- Exercise every state the change touches: happy, empty, loading, error, disabled, responsive breakpoints;
  check accessibility basics (focus visibility, contrast, reduced-motion) per the `bare-minimum-ux` sibling where installed (absent, state the gap).
- When the project's `external-dependencies.lock.json` records the consented `impeccable` external, run its
  `critique`/`audit` as scored gates on the touched surface and route P0/P1 findings back into the fix loop
  before the PR is called review-ready.

## Audience-facing prose

- Any change shipping text a different audience will read — UI copy, docs, README content, prompts or
  instructions another agent will consume — gets a **cold-reader check**: a subagent with none of the
  authoring conversation reads the artifact alone and flags every sentence it cannot ground in the artifact
  itself. Authoring-context leakage — change-log framing ("now", "no longer", "replaces"), justifications
  addressed to the collaborator, provenance asides — is fixed or explicitly justified before the PR is
  review-ready; history belongs in the commit message.
