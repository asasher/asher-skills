<!-- Setup template: the staffing trigger for a project's agent instruction file.
     Reconciled by `staffing setup` into the file every harness loads — the harness-neutral
     base (AGENTS.md) where one exists, else the instruction file the repo's harnesses read.
     Reconcile, never overwrite: if a § Staffing section exists, bring it to this content;
     foreign sections are untouched. Harness-neutral by design — do not add per-harness
     wording here; a harness-specific delta belongs in that harness's own instruction file. -->

## Staffing

Read `docs/agents/staffing.md` fully before model choice, delegation, child/worktree creation,
capability-provider work, watcher assignment, or route-loss fallback. It is the sole authority for this
repo: the complete roster and this repo's deltas, with per-harness eligibility, capability bindings, and
reachability in the machine-local overlay it declares (`docs/agents/local/staffing.md`). Every harness
reads these same files.

Do not resolve from a home-directory roster or from the `staffing` skill's bundled seed. If a machine-level staffing instruction is loaded ahead of this one, it is superseded — the repo's playbook wins.

If the playbook is missing, or its overlay is missing or stamped with a machine other than this one, say
so and run `staffing setup` rather than dispatching on rows nobody verified here.
