# Implement

Target: an approved plan, or a small enhancement that skipped planning. Runs standalone or as the build step of the `enhancement` branch.

Read `docs/agents/implementing.md` for this repo's commit style and code conventions, and `docs/agents/environment.md` for the base branch, branch naming, and how to run locally. If either is missing, report a setup gap and stop.

## Steps

1. Build to the plan.
   - Implement the approved plan (or the agreed small change) per the playbook's conventions. Do not expand scope beyond what was approved.
   - Completion criterion: every item in the plan's definition of done is implemented, or any deviation is recorded against the plan.

2. Keep the change coherent.
   - Branch per `environment.md`; commit per `implementing.md`, so the work is reviewable.
   - Completion criterion: the work sits on a correctly named branch off the right base, with commits that match the repo's style.

Standalone with a PR intended: continue to `reference/verify.md`.
