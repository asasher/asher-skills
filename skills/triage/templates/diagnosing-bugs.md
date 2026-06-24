# Playbook: Diagnosing Bugs

> Project playbook for this repo. The triage `diagnose` subskill reads this file. Tailor it to how this codebase is actually debugged. If the `diagnosing-bugs` skill is installed, defer to it for technique and keep this file for repo specifics.

## Reproduce

- Preferred reproduction: write a failing test that captures the defect. Put it where the suite lives.
- If a test is impractical, record the exact command and inputs that trigger the failure.

## Investigate

- Read the failing path end to end before changing anything. Confirm the cause, not just the symptom.
- Note any logging or debug entry points specific to this repo here: _<add yours>_.

## Fix

- Make the smallest change that addresses the root cause.
- Add or keep a regression test that fails before the fix and passes after.

## Done when

- The failing path passes and the repo's required checks (see `verifying.md`) are green.
