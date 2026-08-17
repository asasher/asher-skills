<!-- Setup template: the staffing trigger for a project's agent instruction file.
     Reconciled by `staffing setup` into the file every harness loads — the harness-neutral
     base (AGENTS.md) where one exists, else the instruction file the repo's harnesses read.
     Reconcile, never overwrite: if a § Staffing section exists, bring it to this content;
     foreign sections are untouched. Harness-neutral by design — do not add per-harness
     wording here; a harness-specific delta belongs in that harness's own instruction file. -->

## Staffing

Read `docs/agents/staffing.md` fully before model choice, delegation, subagent or worktree creation, or capability-provider work. It is the sole authority for this repo: the roster table, pins, declared capability routes, and this repo's deltas. Every harness reads this same file. Resolution is the `staffing` skill's doctrine — state the task's bars, drop models below them, take the cheapest survivor; on a route failure warn and fall back.

Do not resolve from a home-directory roster or from the `staffing` skill's bundled seed. If a machine-level staffing instruction is loaded ahead of this one, it is superseded — the repo's playbook wins.

If the playbook is missing, say so and run `staffing setup` rather than inventing a roster.
