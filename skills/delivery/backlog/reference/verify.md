# Verify

Target: a branch, working tree, or PR. Confirms the change **behaves** as the issue asked. Runs standalone or as the verify step of the loop, where it gates progress to evidence and the PR.

The check commands and where acceptance criteria come from live in `docs/agents/verifying.md`; the isolation regime, how to ready and seed the verification surface, and how to mint any required session live in `docs/agents/environment.md`. If either is missing, report a setup gap and stop.

## Staffing

As the loop's verify step, this whole loop runs in a delegated subagent filling the **checker** role — the role and its fallback ladder are resolved by the `staffing` skill (by name). The issue thread stays coordinator either way. Standalone runs execute wherever they were invoked.

Verification produces a **verdict and its raw grading record**, not the terminal evidence package. Preserve the check output, cited executor transcripts, and per-criterion results needed to substantiate the verdict; `reference/evidence.md` packages that record and captures any additional human-facing proof against the final reviewed HEAD. Take screenshots only to exercise or diagnose a criterion. For a styling-only change, a final-HEAD verification capture may later be reused under `reference/evidence.md`'s Reviewer-confirmed exception; verification never declares that reuse itself.

## Loop

1. **Criteria and promised artifacts stated** — derive criteria from the issue or approved plan, then open every claimed test, fixture, document, or probe and confirm it exists and exercises the cited seam. Never trust a filename or implementer summary as coverage.
2. **Fixtures provisioned** — read each criterion's entities, scale, account/tenant, lifetime, and observation mechanism. Create missing fixtures with the playbook's unique per-issue names before the loop and retain them through final evidence. An infeasible requirement returns to the approved substitute or ruling; do not invent one here.
3. **Checks run** — run every check the PR will claim, per `verifying.md`, and record its result.
4. **Surface ready** — ready the isolated, seeded, authenticated verification surface named in `environment.md`, populated enough to exercise every criterion, or state a blocker. For skill behavior this is the executor harness loaded with the situated scenario, deployment context, and prewritten answer key; no app or stack is assumed. For product behavior it is the relevant CLI or running app stack. In the cloud-singleton regime, follow the playbook's serialization rule rather than assuming a private surface.
5. **Verdict per criterion** — exercise each criterion against that surface and record pass/fail plus the observation, **graded**: `live` (exercised on the real surface), `static-substitute` (inspection or a pre-approved substitute — name it), `not-run`, or `blocked`. A checker that cannot execute records `static-substitute` or `blocked` — "PASS by inspection" is `static-substitute`, never an unqualified PASS — and every report up the chain quotes the grade verbatim. Acceptance requires each criterion `live` or carrying its pre-approved substitute as a **caveat**; a silent substitute is a false claim.
6. **Loop or report** — hand each failed criterion back to its builder, then re-run the criterion against the same verification surface. Never infer a pass. Stop when all pass, five verify/fix iterations are reached, or a blocker is hit. A design gap or the same criterion failing twice escalates to the issue thread with the observation and attempts; standalone runs report the verdict.

All criteria passing proceeds, in the loop, to the create-PR step per `reference/issue-loop.md`; standalone with a PR intended, continue to `reference/evidence.md` directly.
