---
name: to-branch
description: Commit files to another branch while preserving the current worktree, and return the commit hash. Use when publishing an artifact (a spec, prototype, or dossier) to an issue's artifact branch from a worktree that must stay on its own branch.
---

# To Branch

Publish files to another branch while keeping the current worktree in place. Run the bundled script:

    scripts/to-branch.py <branch> <file[:dest]>... -m "<message>" [--push]

It commits via a temporary index: read the branch tip's tree (forking from `HEAD` when the branch is new), add the files, `commit-tree`, `update-ref`, then push when asked, and print the new commit hash. The current worktree's branch, index, and uncommitted files are untouched.

Rules:

- Before publication on another machine, fetch the remote artifact branch. Create its local ref from the remote tip without checking it out, or reconcile a behind/diverged local ref while preserving unique commits. The script reads local refs, so establish the existing remote history locally first.

- **Publish at record time.** Draft as untracked scratch files; a commit lands here only when the result is written to its record (an issue comment, the conversation). Publish and link are one move, and every commit on the branch is a revision somebody was shown.
- The printed hash is the revision's identity: projections and approvals bind to it.
- Use fast-forward updates. The script rejects a conflicting ref move; read the branch tip and reconcile concurrent publication before retrying.
