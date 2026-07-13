# Verify

Target: a branch, working tree, or PR. Confirms the change **behaves** as the issue asked. Runs standalone or as the verify step of the loop, where it gates progress to evidence and the PR.

The check commands and where acceptance criteria come from live in `docs/agents/verifying.md`; the isolation regime, how to bring up and seed a testable stack, and how to mint a session in `docs/agents/environment.md`. If either is missing, report a setup gap and stop.

## Staffing

As the loop's verify step, this whole loop runs in a delegated subagent filling the **checker** role — the role and its fallback ladder are resolved by the `staffing` skill (by name). The issue thread stays coordinator either way. Standalone runs execute wherever they were invoked.

Verification produces a **verdict**, not an evidence package. Take screenshots only to exercise or diagnose
a criterion. For a styling-only change, a final-HEAD verification capture may later be reused under
`reference/evidence.md`'s Reviewer-confirmed exception; verification never declares that reuse itself.

## Loop

1. **Criteria and promised artifacts stated** — derive criteria from the issue/approved plan, then open every
   claimed test, fixture, document, or probe and confirm it exists and exercises the cited seam. Never trust a
   filename or implementer summary as coverage.
2. **Fixtures provisioned** — read each criterion's entities, scale, account/tenant, lifetime, and observation
   mechanism. Create missing fixtures with the playbook's unique per-issue names before the loop and retain
   them through final evidence. An infeasible requirement returns to the approved substitute or ruling; do
   not invent one here.
3. **Checks run** — every check the PR will claim, per `verifying.md`, with its result known.
4. **Stack up** — an isolated, seeded, authenticated stack per `environment.md`, populated enough to exercise every criterion, or a stated blocker. In the cloud-singleton regime, follow the playbook's serialization rule rather than assuming a private stack.
5. **Verdict per criterion** — exercise the app and record pass/fail plus the observation. When a pre-approved substitute is required, record the criterion, gap, and substitute as a **caveat**; a silent substitute is a false claim.
6. **Loop or report** — hand each failed criterion back to its builder, then re-run the criterion against the running app. Never infer a pass. Stop when all pass, five verify/fix iterations are reached, or a blocker is hit. A design gap or the same criterion failing twice escalates to the issue thread with the observation and attempts; standalone runs report the verdict.

All criteria passing proceeds, in the loop, to the create-PR step per `reference/issue-loop.md`; standalone with a PR intended, continue to `reference/evidence.md` directly.
