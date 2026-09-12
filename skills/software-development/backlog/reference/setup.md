# Setup — the environment playbook and the labels

Setup records durable repo environment facts and creates the fixed labels. Check machine state at use. Reconcile an existing playbook section by section.

Confirm authenticated tracker access to the intended repository; report a failure as a setup blocker.

1. **Environment playbook** → `docs/agents/environment.md`, from [templates/environment.md](../templates/environment.md). Fill every section from what this repo actually does: the base branch, how the stack starts detached and logs, per-worktree bring-up and teardown, the canonical CI check definitions, the seed, how an agent authenticates to the app, the drivers for each surface, and the artifact store (bucket, base URL, credential variable names, upload command; ask the owner for the store facts, and record names, never values). Link existing project command definitions and record additional invocation requirements. Verify the resolved commands headlessly: a start command that only works in a terminal gets its detached wrapper recorded instead. Reconcile an existing playbook section by section; a row naming a command, branch, or tool this repo does not use is a defect to fix.

2. **Certification** → the playbook's § Agent-readiness. Walk the checklist the `agent-ready-codebase` reference sibling owns (worktrees, stack per worktree, auth per worktree, seed, artifact publication through `to-web`) and demonstrate each item in this repo. Write the answers, the concurrent-build limit and admission mechanism, the shared-singleton table, and the punch list. Default to three builds and one dispatch owner until the repo has a tested shared admission lock. Record ordinary PR creation, never drafts; review-readiness is a later verdict. The verdict is a pass or a punch list of gaps; each gap is a groomable issue. Repeatable on demand: certification is upkeep, and a build that breaks an answer fixes the answer.

3. **Labels** → compare all repository labels with the table in [labels.md](labels.md). Present missing labels and differences, apply the approved changes, then read back the result. Preserve unrelated labels.
