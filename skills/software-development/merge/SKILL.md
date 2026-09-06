---
name: merge
description: Review open PRs and suggest a merge order; merge only the PRs the human explicitly selects.
disable-model-invocation: true
metadata:
  optional: [writing-for-humans]
---

# Merge

## review

`merge review`, or an invocation without a merge selection, is read-only. Read all open PRs, their tickets, heads, targets, review, CI, and evidence. Group them as **ready**, **blocked**, **stale**, or **dependent**, with the reason and suggested order. Show straightforward candidates first, applying the same proof gates to each.

## Merge a selection

Require the human's explicit selection before merging. For each selected PR, bases before dependents:

1. Require an open PR, no unresolved blockers, and LGTM covering its current head and target base. Require current-head evidence. Also require behavioral verification, a justified light-work omission, or explicit head-specific waivers for named claims. A changed head or base needs renewed checks and review; equal patch-id alone is insufficient.
2. Require all required PR checks to pass. Wait within a bounded timeout; recheck the head and base immediately before merging.
3. Merge atomically against the verified head (`--match-head-commit <verified-sha>` with GitHub CLI), squashing unless the repo says otherwise. Confirm `MERGED`; queued is still pending.
4. Confirm ticket closure. Close a child merged into a spec branch explicitly, recording its merge SHA. Do the same when the configured base is not the repository's default branch.
5. Reconcile dependent branches with the merged base. Resolve mechanical conflicts or conflicts settled by the approved intent; record tradeoffs. Conflicting approved behavior stops for a ruling. Changed dependents need renewed checks and review before their turn.
6. Tear down the merged ticket's stack using the playbook, then remove its secondary worktree and Git registration using native Git. Preserve dirty or unknown files; remove only known disposable residue. Keep the primary checkout and its branch unchanged throughout cleanup.
7. Delete finished work and artifact branches locally and remotely only after checking for dependent PRs, active claims, and unique unmerged work; retain and report any such branch. Verify deletions. Keep a spec branch until its promotion merges. Retain published HTML and evidence URLs after branch cleanup.

Report merged SHAs, ticket closures, retained work, and blockers. Stop affected dependents when a prerequisite fails. Never force over another actor's branch or bypass the merge gate. Use `writing-for-humans` when available.
