# Setup — the environment playbook and the labels

Setup records durable repo environment facts and creates the fixed labels. Check machine state at use. Reconcile an existing playbook section by section.

Preflight: `gh auth status` succeeds and `gh repo view` resolves this repo. Report either failure as a setup blocker.

1. **Environment playbook** → `docs/agents/environment.md`, from [templates/environment.md](../templates/environment.md). Fill every section from what this repo actually does: the base branch, how the stack starts detached and logs, per-worktree bring-up and teardown, the check commands exactly as CI runs them, the seed, how an agent authenticates to the app, the drivers for each surface, and the artifact store (bucket, base URL, credential variable names, upload command; ask the owner for the store facts, and record names, never values). Verify each command headlessly as it is recorded: a start command that only works in a terminal gets its detached wrapper recorded instead. Reconcile an existing playbook section by section; a row naming a command, branch, or tool this repo does not use is a defect to fix.

2. **Certification** → the playbook's § Agent-readiness. Walk the checklist the `agent-ready-codebase` reference sibling owns (worktrees, stack per worktree, auth per worktree, seed, artifact publication through `to-web`) and demonstrate each item in this repo. Write the answers, the concurrent-build limit and admission mechanism, the shared-singleton table, and the punch list. Default to three builds and one dispatch owner until the repo has a tested shared admission lock. Record ordinary PR creation, never drafts; review-readiness is a later verdict. The verdict is a pass or a punch list of gaps; each gap is a groomable issue. Repeatable on demand: certification is upkeep, and a build that breaks an answer fixes the answer.

3. **Labels** → the fixed set in [labels.md](labels.md). Run `scripts/reconcile-labels.py --repo <owner/name> --dry-run`, show the user what would change, then apply with `--create` on their consent. The script reconciles the family's labels, preserving the repo's other labels.
