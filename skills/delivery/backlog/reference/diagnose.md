# Diagnose — lifecycle handoff

Target: a bug issue, failing report, or described defect. Runs standalone or as the issue loop's `bug` branch.

## Guarded direct fix

Skip diagnosis only when all three facts are recorded: a human report, an observable visual/copy defect, and
a named, self-evident styling/copy cause. Staff one narrow fix through the builder role, preserve the pre-fix observation,
then visually check the affected states (both themes for theme-sensitive work) and run the required checks.
If the observation confirms the named cause, return the fix and visual result to the issue loop and continue
to its formal verify step; do not invoke the diagnosis sibling.
The first contradictory observation—unchanged symptom, behavioral scope, or a cause wider than the named
style/copy seam—ends this lane. Preserve that observation and the attempted diff, pass both into
`diagnosing-bugs`, and do not make a second direct guess.

For every other bug, invoke the **`diagnosing-bugs`** sibling by name in the issue thread. Give it the reporter's exact symptom,
the issue/worktree identity, `docs/agents/environment.md` for running and authentication, the repo's required
checks, and the durable issue record for its ranked hypotheses and root cause. Do not restate or edit its
six-phase method here.

Accept the handoff only when it returns the red-capable command and captured symptom, minimal reproduction,
named root cause, fix, regression proof or explicit no-seam finding, original loop green, cleanup, and project
checks. A missing loop is a blocker, not a diagnosis: record what access/artifact/instrumentation would unblock
it and return the issue through the caller's normal blocked path.

Backlog retains the lifecycle: worktree/issue status, any design ruling or escalation, commits, PR creation,
verification, evidence, review, and merge. If the fix exposes a contested design decision, pause the diagnosis
handoff and route that question through the existing prototype/approval path before resuming it.

Standalone with a PR intended: continue to `reference/verify.md`, then `reference/evidence.md`.
