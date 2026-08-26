---
name: worktree
description: Prepare, inspect, and remove project-owned Git worktrees. Use when work needs deterministic isolation, an existing worktree's registration and state must be validated, or cleanup must preserve dirty work.
metadata:
  optional:
    - docs/agents/platform.md
    - docs/agents/environment.md
---

# Worktree

Perform one worktree operation. This skill owns the fragile Git mechanics; the operation and its policy arrive decided. Read the project's platform and environment playbooks before acting.

## Prepare

Require a repository, work branch, and base ref. Take the worktree root from the project platform playbook; absent one, use `<repo-parent>/<repo-name>-worktrees/`, never a harness-private directory. Then run:

    scripts/worktree.py prepare --repo <repo> --branch <branch> --base <base> [--root <root>]

The command creates branch and working copy in one Git operation; the primary checkout stays untouched. Fetching a remote ref is allowed when the platform playbook requires it. A dirty primary checkout, or one ahead of or behind its upstream, is report-only; stop when resolving the requested base would require unpublished primary-checkout work.

`prepare` reuses an existing worktree only when path, branch, and its ownership record exactly match the request. A base that resolves to a different commit is a different base and stops reuse. When the script reports `reused: true`, confirm the claim on this branch before accepting the result: a tracker claim for tracker-dispatched work, or the harness's live thread/child record plus its parent dispatch report for direct work. Between prepare and successful dispatch, the path is provisionally held under that claim. Any of these stops the operation: a branch claimed by another live run; any other existing registration, directory, or unregistered branch; a prunable registration, missing ownership record, or missing working directory — stopped for recovery, the state left intact; a requested path inside any registered checkout, stopped before Git changes either working tree.

After creation, run the worktree bootstrap the environment playbook records, from inside the new working copy. Absent a recorded bootstrap, skip it and say so in the structured result. A failed bootstrap leaves the registration intact for inspection. Report the structured result: repository, path, branch, base commit, head, and whether it was reused.

## Inspect

Run:

    scripts/worktree.py inspect --repo <repo> --path <path>

Treat Git's registration as ground truth, then validate that the directory itself points to the same Git common directory, branch, and head. Report registration, validity, prunable state, branch, head, existence, and dirty state; a missing or invalid working directory has `dirty: null`. Join that result with the claim, the change request, and the per-worktree environment state the environment playbook records, and report which were found.

## Remove

Resolve the exact registered path first. Tear down the per-worktree environment from inside that working copy using the environment playbook; absent a recorded teardown, skip it and say so in the structured result. Then run:

    scripts/worktree.py remove --repo <repo> --path <path>

The script refuses symlinked paths, the primary checkout, prunable or identity-mismatched registrations, unregistered paths, and dirty worktrees — tracked, untracked, or ignored files, or assume-unchanged / skip-worktree index entries that hide changes from status. It removes only the clean registered working copy; the branch remains for its lifecycle owner to publish, retain, or delete. Report the retained branch from the script's result.

## Failure contract

Treat every stop and script refusal as final. Do not add `--force`, delete an unregistered directory, adopt an unowned branch, or turn a dirty-tree refusal into cleanup. Return the diagnostic and the exact path unchanged.
