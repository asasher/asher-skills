# Diagnose

Target: a bug issue, a failing report, or a described defect. Runs standalone or as the `bug` branch of the loop.

Read `docs/agents/diagnosing-bugs.md` for this repo's reproduction and debugging conventions. To run or authenticate against the app while reproducing, read `docs/agents/environment.md`. If either is missing, report a setup gap and stop.

## Steps

1. Reproduce before fixing.
   - Establish a failing path you can observe — a test, a command, or a recorded behavior. Make the failure repeatable.
   - Completion criterion: you can trigger the failure on demand, or you have stated precisely why it cannot be reproduced and what that implies.

2. Locate the cause.
   - Trace from the observed failure to the responsible code. Name the cause, not just the symptom.
   - Completion criterion: you can state the root cause and the smallest change that addresses it.

3. Fix and confirm.
   - Apply the fix per the playbook's conventions. Re-run the failing path and confirm it now passes.
   - Completion criterion: the previously failing path passes, and no check the playbook requires has regressed.

Standalone with a PR intended: continue to `reference/verify.md`.
