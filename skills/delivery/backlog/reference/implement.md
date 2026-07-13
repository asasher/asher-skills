# Implement

Target: an approved plan, or a small enhancement that skipped planning. Runs standalone or as the build step of the `enhancement` branch.

Staffing: build-out fills the **builder** role for its surface, resolved by the `staffing` skill (by name); in the loop, the issue thread dispatches it rather than building in its own context.

The technique — the test-first build loop, commit style, code conventions — lives in `docs/agents/implementing.md`; the base branch, branch naming, and how to run locally in `docs/agents/environment.md`. If either is missing, report a setup gap and stop.

## Gates

1. **Hypotheses falsified** — read the plan's assumptions-to-validate and run the riskiest probe first. Do not
   build dependent work until its mechanism survives the named falsification; a failure returns to planning.
2. **Built to the plan** — every item in the plan's definition of done is implemented per the playbook, or any deviation is recorded against the plan. No scope beyond what was approved.
3. **Coherent** — the work sits on a correctly named branch off the right base, with commits that match the repo's style, reviewable as a unit.

Standalone with a PR intended: continue to `reference/verify.md`, then `reference/evidence.md`.
