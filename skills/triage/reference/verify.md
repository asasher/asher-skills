# Verify

Target: a branch, working tree, or PR. Confirms the change **behaves** as the issue asked. Runs standalone or as the verify step of the loop, where it gates progress to evidence and the PR.

Read `docs/agents/verifying.md` for this repo's check commands, where acceptance criteria come from, and what evidence a change requires. Read `docs/agents/environment.md` for the isolation regime, how to bring up and seed a testable stack, and how to mint a session. If either is missing, report a setup gap and stop.

Verification produces a **verdict**, not artifacts. Capturing human-facing proof is the separate, terminal `reference/evidence.md` step — do not capture evidence here. Take a screenshot only when you need one to diagnose a failure.

## Steps

1. State the acceptance criteria.
   - Derive explicit, testable criteria from the issue and — for an enhancement — the approved plan's definition of done. For a bug, the criterion is the previously failing path now passing. Work from the issue's intent, not the implementer's description of what they built.
   - Completion criterion: a list of criteria, each independently checkable as pass or fail.

2. Run the checks.
   - Run the narrowest meaningful checks first, then the broader checks `verifying.md` requires for the touched surface.
   - Completion criterion: every check the PR will claim has been run, with its result known.

3. Stand up a testable stack.
   - Bring up an isolated, seeded stack per `environment.md`'s isolation and seed regimes, then mint a session per its auth model. If the repo is the cloud-singleton regime, follow the playbook's serialization rule rather than assuming a private stack.
   - Completion criterion: a running app reachable and authenticated, populated enough to exercise every criterion, or a stated blocker.

4. Verify behavior against each criterion.
   - Exercise the app against the running stack and record a pass or fail per criterion, naming the gap on any fail.
   - Completion criterion: every criterion has a pass/fail verdict with evidence of the gap on failures.

5. Loop or report.
   - As the loop's verify step: hand every failed criterion back to `implement.md` (enhancement) or `diagnose.md` (bug), then re-verify only what changed. Stop when all criteria pass, five verify/fix iterations are reached, or a blocker is hit. On cap or blocker, report it to the issue thread; do not proceed to evidence.
   - Standalone: report the verdict.
   - Completion criterion: all criteria pass (proceed to `reference/evidence.md`), or the loop ends at its cap or an explicit blocker.
