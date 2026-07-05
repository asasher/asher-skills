# Verify

Target: a branch, working tree, or PR. Confirms the change **behaves** as the issue asked. Runs standalone or as the verify step of the loop, where it gates progress to evidence and the PR.

The check commands and where acceptance criteria come from live in `docs/agents/verifying.md`; the isolation regime, how to bring up and seed a testable stack, and how to mint a session in `docs/agents/environment.md`. If either is missing, report a setup gap and stop.

## Staffing

As the loop's verify step, this whole loop runs in a delegated subagent filling the **checker** role — see `reference/staffing.md` for the role and its fallback ladder, and the Model staffing section of `docs/agents/environment.md` for the roster. The issue thread stays coordinator either way. Standalone runs execute wherever they were invoked.

Verification produces a **verdict**, not artifacts. Capturing human-facing proof is the separate, terminal `reference/evidence.md` step — do not capture evidence here. Take a screenshot only when you need one to diagnose a failure.

## Loop

1. **Criteria stated** — explicit, testable criteria derived from the issue and, for an enhancement, the approved plan's definition of done; for a bug, the previously failing path now passing. Work from the issue's intent, not the implementer's description of what they built. Each criterion independently checkable as pass or fail.
2. **Checks run** — every check the PR will claim, per `verifying.md`, with its result known.
3. **Stack up** — an isolated, seeded, authenticated stack per `environment.md`, populated enough to exercise every criterion, or a stated blocker. In the cloud-singleton regime, follow the playbook's serialization rule rather than assuming a private stack.
4. **Verdict per criterion** — exercise the app against the running stack and record a pass or fail per criterion, naming the gap on any fail. Record *how* each criterion was actually exercised: when a blocker forces a workaround (a tool erroring, an unreachable surface), verify through the nearest observable substitute and record the substitution as a **caveat** — the criterion, the gap, the substitute observation. Caveats travel to the PR body's Verification section; a disclosed workaround is a pass with a caveat, a silent one is a false claim.
5. **Loop or report** — as the loop's verify step: hand each failed criterion back to the branch that built it — `implement.md` (enhancement), `diagnose.md` (bug), `refactor.md` (refactor), the fix executing on the **builder** for its surface per `reference/staffing.md` — then re-verify only what changed. A post-fix verdict comes only from **re-running the criterion's check against the running app** — never from reasoning that the fix should work; an inferred pass is the one self-grading failure this loop's design permits, so it is banned outright. Stop when all criteria pass, five verify/fix iterations are reached, or a blocker is hit; on cap or blocker, report to the issue thread and do not proceed to evidence. Two triggers escalate to the issue thread instead of burning iterations — a failure that points at a design gap rather than a mechanical slip, or the same criterion failing twice — reporting the criterion, the observed gap, and what was tried. Standalone: report the verdict.

All criteria passing proceeds, in the loop, to the create-PR step per `reference/issue-loop.md`; standalone with a PR intended, continue to `reference/evidence.md` directly.
