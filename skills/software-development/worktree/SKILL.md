---
name: worktree
description: Prepare, inspect, and safely remove project-owned Git worktrees. Use when a skill or session needs deterministic isolation mechanics, an existing worktree must be reconciled, or cleanup must preserve dirty work.
argument-hint: "<prepare | inspect | remove> <branch or path>"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Worktree

Perform one worktree operation. Policy stays with the workflow that selected the operation; this skill owns the fragile Git mechanics. Read the project's version-control and environment bindings before acting. A missing binding uses the repo-adjacent default below, never a harness-private directory.

## Prepare

Require a repository, work branch, and base ref. Take the worktree root from the project platform playbook; absent one, use `<repo-parent>/<repo-name>-worktrees/`. Then run:

    scripts/worktree.py prepare --repo <repo> --branch <branch> --base <base> [--root <root>]

The command creates branch and working copy in one Git operation without switching, updating, cleaning, committing, or resetting the primary checkout. Fetching a remote ref is allowed when the platform binding requires it; changing the primary checkout is not. Surface dirty, ahead, or behind primary state. Stop only when the requested base cannot be resolved without unpublished primary-checkout work.

`prepare` reuses an existing worktree only when path, branch, and its project-owned prepared-base record exactly match the request. A different ancestor is a different base and stops reuse. Before reuse, confirm the workflow's ownership record names this branch: a tracker claim for tracker-dispatched work, or the harness's live thread/child record plus its parent dispatch report for direct work. The caller owns the path provisionally between prepare and successful dispatch. A branch claimed by another live run is a conflict. Any other existing registration, directory, or unregistered branch stops the operation. A prunable registration, missing prepared-base record, or missing working directory also stops for recovery; never silently prune and recreate it. A requested path inside any registered checkout stops before Git changes either working tree.

After creation, run the repository's recorded worktree bootstrap from inside the new working copy. A failed bootstrap leaves the registration intact for inspection; never erase its evidence automatically. Report the structured result: repository, path, branch, base commit, head, and whether it was reused.

## Inspect

Run:

    scripts/worktree.py inspect --repo <repo> --path <path>

Treat Git's registration as ground truth, then validate that the directory itself points to the same Git common directory, branch, and head. Report registration, validity, prunable state, branch, head, existence, and dirty state; a missing or invalid working directory has `dirty: null`. Join that result with any workflow ownership, change-request, and environment records relevant to the decision at hand. A directory scan alone does not establish a live worktree.

## Remove

Resolve the exact registered path first. Tear down the per-worktree environment from inside that working copy using the environment playbook, then run:

    scripts/worktree.py remove --repo <repo> --path <path>

The script refuses symlinked paths, the primary checkout, prunable or identity-mismatched registrations, unregistered paths, and worktrees containing tracked, untracked, or ignored files. It also refuses assume-unchanged or skip-worktree index entries, which can hide local changes from status. It removes only the clean registered working copy; the branch remains for its lifecycle owner to publish, retain, or delete. Verify removal through a fresh Git worktree listing and report the retained branch.

## Failure contract

Stop on ambiguity. Do not add `--force`, delete an unregistered directory, adopt an unowned branch, or turn a dirty-tree refusal into cleanup. Return the diagnostic and the exact path unchanged.

## Dependency surface

- **Bundled:** `scripts/worktree.py` — the deterministic Git operations; `evals/` — real temporary-repo script tests and situated behavior probes.
- **Project playbooks:** `docs/agents/platform.md` supplies base, branch, root, publish, and removal bindings; `docs/agents/environment.md` supplies bootstrap and environment teardown.
