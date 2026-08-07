---
name: merge-changes
description: Merge review-ready changes on the user's explicit request — the human authorization gate at the end of every change.
argument-hint: "<PRs, branches, or 'everything review-ready'>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [worktree]
  optional: [watch-until]
---

# Merge Changes

Merging is a human-authorized operation. Automated review approval, green checks, `ready-for-agent`, or a reviewer's `LGTM` are prerequisites where configured — **they are never authorization to merge**. Authorization is the user's explicit merge request: invoking this skill, naming the changes to merge in their own words, or giving the documented readiness signal after a shaping thread presents the exact shaping change request and states that narrow effect. Operate only on the changes named or unambiguously included in that request — "merge #51" does not license merging its stack-mates, and shaping readiness licenses only the presented shaping change.

Platform verbs (merge, checks-read, PR-read, branch ops) come from the project's `docs/agents/platform.md` when present; on a bare GitHub repo, use `gh` directly. Absent any change-review binding, state the gap and stop.

## Steps

1. **Resolve scope.** Enumerate the exact PRs/changes in the request. For each, verify it is still open and review-ready: review converged (approval/`LGTM` per the project's convention), no unresolved blocking comments, branch not superseded — and the approval covers the head being merged: where the LGTM names the SHA it reviewed, compare it to the current head; an approval naming no head covers the head current when it was posted. Either way, commits landed since the approval send the change back through review rather than into the merge. Anything failing this is reported and dropped from scope — never merged "while we're here".
2. **Order.** Determine dependency and stacking relationships (stacked branches, `Depends on` links, overlapping surfaces) and compute the merge order: bases before dependents.
3. **Gate on CI, per merge, at merge time.** Immediately before each merge, re-query the required checks on the current head — only its own completed checks count; a local run, an earlier head's green, or timing inferred from another change never stands in for them. A pending or failing required check stops that merge (and its dependents) until resolved.
4. **Merge in order,** using the platform's recorded merge mechanics (squash policy). Branch deletion stays out of the merge verb: the change's working copy still holds its branch at merge time, so a delete bundled into the merge fails on the local branch — and can abort before the remote branch is touched. Branch cleanup is step 7's, downstream of working-copy teardown.
5. **Reconcile after each merge.** Update or rebase dependent branches as needed; resolve conflicts only when the intended resolution is mechanical and unambiguous (keep-both provenance, regenerated artifacts, lockfile refresh + the project's install command). Re-run the affected checks after any reconciliation.
6. **Stop and report, don't guess.** A conflict needing product or implementation judgment, a check that fails after reconciliation, or a scope ambiguity stops the run with the blocker named — the remaining queue is left unmerged and reported.
7. **Report.** Merged PRs with resulting commit SHAs, the order used, reconciliations performed, and anything left unmerged with its reason. Apply the tracker's post-merge lifecycle (labels, issue closure) where the platform binding records it. Then clean up: remove each merged change's working copy through the `worktree` skill — its Remove owns the teardown order (environment torn down from inside the working copy, then the copy itself) and refuses dirty or unregistered paths. Only then delete each merged branch, local and remote, per platform policy — branch deletion waits for working-copy removal because the working copy holds the branch — and **verify both are gone by querying them** — on git, `git branch --list <branch>` and `git ls-remote --heads origin <branch>`, both returning nothing — never by trusting the delete commands' own output: a failed branch delete reports on stderr, where it is easy to skim past. Report each branch as deleted on the strength of those queries, not a delete command's silence.

## Boundaries

- Never merge outside the request's scope.
- Never force-push over, close, or delete someone else's branch to make a merge work.
- The whole flow is judgment-light coordination — it stays with this session; delegate nothing but mechanical check-watching (via the `watch-until` sibling when installed).

## Dependency surface

- **Sibling (required, by name):** `worktree` for inspected, refusal-aware working-copy teardown.
- **Sibling (optional, by name):** `watch-until` for mechanical check-watching.
