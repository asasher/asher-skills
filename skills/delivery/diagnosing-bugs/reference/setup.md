# Setup — project diagnosis delta

Reconcile exactly one owned artifact: `docs/agents/diagnosing-bugs.md`.

1. Read the repo's test/check configuration, debugging entry points, and known flaky surfaces.
2. If the playbook is absent, create it from `templates/diagnosing-bugs.md` and replace placeholders only with
   facts verified in this repo.
3. If it exists, preserve every project delta and deliberate house-practice substitution. Offer only missing
   or stale factual corrections; never replace the file wholesale and never copy the six-phase method into it.
4. Re-read the result and confirm it contains only project-specific deltas. Re-running setup with unchanged
   facts must produce no diff.

Do not write another skill's playbook or any global instruction file.

Completion criterion: the project playbook exists, its commands and seams are real, repo-owned edits remain,
and an immediate rerun is idempotent.
