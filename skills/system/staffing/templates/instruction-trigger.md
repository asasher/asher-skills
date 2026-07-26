<!-- Setup template: the staffing trigger for a project's agent instruction file.
     Reconciled by `staffing setup` into the file every harness loads — the harness-neutral
     base (AGENTS.md) where one exists, else the instruction file the repo's harnesses read.
     Reconcile, never overwrite: if a § Staffing section exists, bring it to this content;
     foreign sections are untouched. Harness-neutral by design — do not add per-harness
     wording here; a harness-specific delta belongs in that harness's own instruction file. -->

## Staffing

Read `docs/agents/staffing.md` fully before model choice, delegation, child/worktree creation,
capability-provider work, watcher assignment, or route-loss fallback. It is the sole authority for this
repo: the complete roster, per-harness eligibility and capability bindings, this repo's deltas, and the
machine its reachability rows were probed on. Every harness reads this same file.

Do not resolve from a home-directory roster or from the `staffing` skill's bundled seed. If a
machine-level staffing instruction is loaded ahead of this one, it is superseded — the repo's playbook
wins.

If that file is missing, or its probe record names a machine other than this one, say so and run
`staffing setup` rather than dispatching on rows nobody verified here.
