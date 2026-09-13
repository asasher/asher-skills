---
name: merge
description: Review open PRs and suggest a merge order; merge only the PRs the human explicitly selects.
disable-model-invocation: true
metadata:
  requires: [verify-your-work]
  optional: [writing-for-humans]
---

# Merge

## review

`merge review`, or an invocation without a merge selection, is read-only. Read all open PRs, their tickets, heads, targets, review, CI, and evidence. Group them as **ready**, **blocked**, **stale**, or **dependent**, with the reason and suggested order. Show straightforward candidates first, with their current evidence link and the same proof gates.

## Merge a selection

Require the human's explicit selection before merging. Re-read each ticket and split parent for active shaping holds, newer unapproved revisions, and the split's bound revision. Merge only work released under the current approved authority. For each selected PR, bases before dependents:

1. Require an open PR with no unresolved blockers, independent code review, and verification satisfying the recorded risk and any stronger brief. Auth, money, destructive data, and cross-surface work require a verifier independent of the builder/fixer. Reports and evidence must identify the current head, base, approved spec, and tested integration tree. A light-work omission needs justification; each waived claim needs explicit human authorization at this head, which may be recorded from chat. Changed inputs require renewed checks and review within the existing budget.
2. Require passing checks on the intended integration. Read the repository's observed protections in `docs/agents/environment.md` and honor applicable rules. Branch protection is useful but optional; record its absence without blocking the merge.
3. Recheck head and base immediately before merging; moved inputs require renewed checks and review. Merge against the verified head (`--match-head-commit <verified-sha>` with GitHub CLI), squashing unless the repo says otherwise. The flag guards the head; atomic base protection depends on server rules. Confirm `MERGED` and the resulting commit/tree; queued is still pending. If the merged tree differs from the tested tree, run risk-appropriate `verify-your-work` on that merged revision and report the result before dependent work continues.
4. Confirm ticket closure. Close a child merged into a spec branch explicitly, recording its merge SHA. Do the same when the configured base is not the repository's default branch.
5. Reconcile dependent branches with the merged base. Resolve mechanical conflicts or conflicts settled by the approved intent; record tradeoffs. Conflicting approved behavior stops for a ruling. Changed dependents need renewed checks and review before their turn.
6. Tear down the merged ticket's stack using the playbook, then remove its secondary worktree and Git registration using native Git. Preserve dirty or unknown files; remove only known disposable residue. Keep the primary checkout and its branch unchanged throughout cleanup.
7. Delete finished work and artifact branches locally and remotely only after checking for dependent PRs, active claims, and unique unmerged work; retain and report any such branch. Verify deletions. Keep a spec branch until its promotion merges. Retain published HTML and evidence URLs after branch cleanup.

Report merged SHAs, ticket closures, retained work, and blockers. Stop affected dependents when a prerequisite fails. Never force over another actor's branch or bypass the merge gate. Use `writing-for-humans` when available.
