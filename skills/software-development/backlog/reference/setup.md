# Setup — the environment playbook and the labels

Two jobs. Setup writes the repo's environment facts and creates the fixed labels; it never records machine state. Anything a live check can re-derive is checked at use. A repo-owned playbook is edited and reconciled, never blindly overwritten.

Preflight: `gh auth status` succeeds and `gh repo view` resolves this repo. Absent either, stop and say so; nothing below works without them.

1. **Environment playbook** → `docs/agents/environment.md`, from [templates/environment.md](../templates/environment.md). Fill every section from what this repo actually does: the base branch, how the stack starts detached and logs, per-worktree bring-up and teardown, the check commands exactly as CI runs them, the seed, how an agent authenticates to the app, the drivers for each surface, and the artifact store (bucket, base URL, credential variable names, upload command; ask the owner for the store facts, and record names, never values). Verify each command headlessly as it is recorded: a start command that only works in a terminal gets its detached wrapper recorded instead. Reconcile an existing playbook section by section; a row naming a command, branch, or tool this repo does not use is a defect to fix.

2. **Certification** → the playbook's § Agent-readiness. Walk the checklist the `agent-ready-codebase` reference sibling owns (worktrees, stack per worktree, auth per worktree, seed) and demonstrate each item in this repo. Write the answers, the shared-singleton table, and the punch list. The verdict is a pass or a punch list of gaps; each gap is a groomable issue. Repeatable on demand: certification is upkeep, and a build that breaks an answer fixes the answer.

3. **Labels** → the fixed set in [labels.md](labels.md). Run `scripts/reconcile-labels.py --repo <owner/name> --dry-run`, show the user what would change, then apply with `--create` on their consent. The script touches only the family's labels and never the repo's other labels.
