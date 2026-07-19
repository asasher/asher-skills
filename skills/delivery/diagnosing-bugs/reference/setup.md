# Setup — project diagnosis delta

Reconcile exactly one owned artifact: `docs/agents/diagnosing-bugs.md`.

1. Read the repo's test/check configuration, debugging entry points, known flaky surfaces, and source shape.
2. If the playbook is absent, use `templates/skill-authoring/diagnosing-bugs.md` when the repo authors skills
   (`SKILL.md` files under a `skills/` source tree); otherwise use `templates/diagnosing-bugs.md`. Replace
   placeholders only with facts verified in this repo.
3. If it exists, preserve every project delta and deliberate house-practice substitution. Offer only missing
   or stale factual corrections; never replace the file wholesale and never copy the six-phase method into it.
4. Re-read the result and confirm it contains only project-specific deltas.

Do not write another skill's playbook or any global instruction file.

Completion criterion: the project playbook exists, its commands and seams are real, repo-owned edits remain,
and an immediate rerun is idempotent.
