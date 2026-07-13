# Verify

Target: a branch, working tree, or PR. Confirms the change **behaves** as the issue asked. Runs standalone or as the verify step of the loop, where it gates progress to evidence and the PR.

The check commands and where acceptance criteria come from live in `docs/agents/verifying.md`; the isolation regime, how to ready and seed the verification surface, and how to mint any required session live in `docs/agents/environment.md`. A surface may be an executor harness, CLI, web app, mobile app, or desktop app. If either playbook is missing, report a setup gap and stop.

## Staffing

As the loop's verify step, this whole loop runs in a delegated subagent filling the **checker** role — the role and its fallback ladder are resolved by the `staffing` skill (by name). The issue thread stays coordinator either way. Standalone runs execute wherever they were invoked.

Verification produces a **verdict and its raw evidence record (the grading record)**, not presentation artifacts. Preserve the check output, cited executor transcripts, and per-criterion results needed to substantiate that verdict; the separate, terminal `reference/evidence.md` step packages that raw record and captures any additional human-facing proof against the final reviewed HEAD. Do not render, commit, publish, or attach the evidence package here. Take a screenshot only when you need one to diagnose a failure.

## Loop

1. **Criteria stated** — explicit, testable criteria derived from the issue and, for an enhancement, the approved plan's definition of done; for a bug, the previously failing path now passing. Work from the issue's intent, not the implementer's description of what they built. Each criterion independently checkable as pass or fail.
2. **Checks run** — every check the PR will claim, per `verifying.md`, with its result known.
3. **Surface ready** — the isolated verification surface named in `environment.md` is ready and seeded with enough state to exercise every criterion, with any required authentication established, or a blocker stated. For skill behavior this is the executor harness loaded with the skill's situated scenario, deployment context, and prewritten answer key — no app or stack is assumed. For product behavior it is the relevant CLI or running app stack. In the cloud-singleton regime, follow the playbook's serialization rule rather than assuming a private surface.
4. **Verdict per criterion** — exercise each criterion against that ready surface and record a pass or fail, naming the gap on any fail. Record *how* each criterion was actually exercised: when a blocker forces a workaround (a tool erroring, an unreachable surface), verify through the nearest observable substitute and record the substitution as a **caveat** — the criterion, the gap, the substitute observation. Caveats travel to the PR body's Verification section; a disclosed workaround is a pass with a caveat, a silent one is a false claim.
5. **Loop or report** — as the loop's verify step: hand each failed criterion back to the branch that built it — `implement.md` (enhancement), `diagnose.md` (bug), `refactor.md` (refactor), the fix executing on the **builder** for its surface, resolved by the `staffing` skill (by name) — then re-verify only what changed. A post-fix verdict comes only from **re-running the criterion's check against the same verification surface** — never from reasoning that the fix should work; an inferred pass is the one self-grading failure this loop's design permits, so it is banned outright. Stop when all criteria pass, five verify/fix iterations are reached, or a blocker is hit; on cap or blocker, report to the issue thread and do not proceed to evidence. Two triggers escalate to the issue thread instead of burning iterations — a failure that points at a design gap rather than a mechanical slip, or the same criterion failing twice — reporting the criterion, the observed gap, and what was tried. Standalone: report the verdict.

All criteria passing proceeds, in the loop, to the create-PR step per `reference/issue-loop.md`; standalone with a PR intended, continue to `reference/evidence.md` directly.
