# Playbook: Verifying

> Project playbook for this repo. The triage `verify` subskill reads this file for check commands. How to run and authenticate against the app is in `environment.md`; the evidence capture format is built into the skill.

## Checks

Run narrowest-first, then broaden by touched surface. This repo's commands:

- Unit/targeted tests: _<e.g. `npm test -- <path>`>_.
- Lint: _<add yours>_.
- Type check: _<add yours>_.
- Build: _<add yours>_.
- Full suite (before PR): _<add yours>_.

## Evidence required

- What evidence this repo expects for a change, beyond green checks (e.g. before/after for visual changes; none for pure logic): _<add yours>_.
- The capture format is standard and the PR body is the evidence index — see the `verify` reference.
