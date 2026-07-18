# Implement

Target: the issue's plan — an approved plan artifact where one exists (e.g. a spec-derived slice), otherwise the issue thread's just-in-time tactical plan, recorded in the thread and the PR body. Runs standalone or as the build step of the `enhancement` branch.

Staffing: build-out fills the **builder** role for its surface, resolved by the `staffing` skill (by name); in the loop, the issue thread dispatches it rather than building in its own context.

The technique — the test-first build loop, commit style, code conventions — lives in `docs/agents/implementing.md`; the base branch, branch naming, and how to run locally in `docs/agents/environment.md`. If either is missing, report a setup gap and stop.

## Gates

1. **Hypotheses falsified** — read the plan's assumptions-to-validate (for a tactical plan, its named risks) and run the riskiest probe first. Do not
   build dependent work until its mechanism survives the named falsification; a failure returns to the issue thread — revise the tactical plan within delegated authority, or hand back `needs-spec` per `issue-loop.md` when it invalidates a strategic decision.
2. **Built to the plan** — every item in the plan's definition of done (the acceptance criteria, for a tactical plan) is implemented per the playbook, or any deviation is recorded against the plan. No scope beyond the issue's delegated authority.
3. **Coherent** — the work sits on a correctly named branch off the right base, with commits that match the repo's style, reviewable as a unit.

Standalone with a PR intended: continue to `reference/verify.md`, then `reference/evidence.md`.
