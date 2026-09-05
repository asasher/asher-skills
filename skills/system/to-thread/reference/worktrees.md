# Prepare a ticket worktree

Use native Git. Read the environment playbook's base branch, worktree root, and bring-up recipe. Default the root to a sibling `<repo-name>-worktrees/` directory. The caller supplies the ticket's work branch and creation base; a child's base is its spec branch.

1. Inspect `git worktree list --porcelain`, local/remote refs, and the ticket's ownership record. Fetch the remote. Keep the primary checkout's branch and files unchanged; do not stash its changes to start this task.
2. Reuse the matching registered worktree only after the prior run is stopped or an explicit handoff is recorded. Inspect dirty work and diverged commits; preserve and reconcile them before proceeding.
3. With no matching worktree, select the existing branch before considering creation:
   - Local branch: `git worktree add <path> <branch>`.
   - Remote-only branch: `git worktree add -b <branch> <path> origin/<branch>`.
   - New work: `git worktree add -b <branch> <path> <creation-base>`.
4. Verify the working copy's branch, repository registration, and expected commits. An existing path or conflicting registration needs inspection, never force. Bring up the stack once using the playbook.

Record the path and branch on the ticket before spawning. Preserve unpublished commits; another machine can resume only after they are pushed. A failed preparation retains work and reports the exact blocker. Cleanup is the workflow owner's responsibility.
