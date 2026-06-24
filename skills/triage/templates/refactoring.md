# Playbook: Refactoring

> Project playbook for this repo. The triage `refactor` subskill reads this file. Tailor it to this codebase's test framework and conventions. If the `tdd` skill is installed, defer to it for test-first technique.

## Lock behavior first

- Identify or add tests that pin the behavior that must not change before touching implementation.
- Test framework and command for this repo: _<add yours>_.

## Refactor under the net

- Keep the locked tests green at each step. Refactor in small, reversible moves.
- Conventions this repo cares about (naming, module boundaries, file layout): _<add yours>_.

## Done when

- The diff is behavior-preserving, the locked tests still pass, and the repo's required checks are green.
