# Refactor

Target: a module, surface, or issue calling for behavior-preserving change. Runs standalone or as the `refactor` branch of the loop.

Read `docs/agents/refactoring.md` for this repo's test framework and refactoring conventions. If it is missing, report a setup gap and stop.

## Steps

1. Lock the behavior first.
   - Identify or add tests that pin the behavior that must not change. These are the safety net.
   - Completion criterion: the behavior to preserve is covered by passing tests before any implementation changes.

2. Refactor under the net.
   - Change structure per the playbook's conventions while keeping the locked tests green at each step.
   - Completion criterion: the locked tests still pass and behavior is unchanged.

3. Confirm scope.
   - Verify no user-facing behavior shifted beyond the intended structural change.
   - Completion criterion: the diff is structural only, or any behavior change is explicitly called out and justified.

Standalone with a PR intended: continue to `reference/verify.md`.
