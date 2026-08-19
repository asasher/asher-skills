---
name: to-branch
description: Commit files to a branch without visiting it — no checkout, no worktree switch — and return the commit hash. Use when publishing an artifact (a spec, prototype, or dossier) to its artifact branch from a worktree that must stay on its own branch.
argument-hint: "<branch> <file[:dest]>... -m <message>"
metadata:
  requires: []
  optional: []
---

# To Branch

Publish files to a branch the current worktree never visits. Run the bundled script:

    scripts/to-branch.py <branch> <file[:dest]>... -m "<message>" [--push]

It commits via a temporary index — read the branch tip's tree (forking from `HEAD` when the branch is new), add the files, `commit-tree`, `update-ref` — then pushes when asked, and prints the new commit hash. The current worktree's branch, index, and uncommitted files are untouched.

Rules:

- **Publish at record time.** Draft as untracked scratch files on your desk; a commit lands here only when the result is written to its record (ticket comment, conversation) — publish and link are one move, and every commit on the branch is a revision somebody was shown.
- The printed hash is the revision's identity — projections and blessings bind to it.
- Never force-update: the script refuses a non-fast-forward ref move; a conflict means someone else published — read the branch tip first.
