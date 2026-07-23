---
name: merge-changes
description: Merge review-ready changes on the user's explicit request — the human authorization gate at the end of every change.
argument-hint: "<PRs, branches, or 'everything review-ready'>"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: []
  optional: [watch-until]
---

# Merge Changes

Merging is a human-authorized operation. Automated review approval, green checks, `ready-for-agent`, or a
reviewer's `LGTM` are prerequisites where configured — **they are never authorization to merge**.
Authorization is the user's explicit merge request: invoking this skill, or naming the changes to merge in
their own words. Operate only on the changes named or unambiguously included in that request — "merge #51"
does not license merging its stack-mates.

Platform verbs (merge, checks-read, PR-read, branch ops) come from the project's `docs/agents/platform.md`
when present; on a bare GitHub repo, use `gh` directly. Absent any change-review binding, state the gap and
stop.

## Steps

1. **Resolve scope.** Enumerate the exact PRs/changes in the request. For each, verify it is still open and
   review-ready: review converged (approval/`LGTM` per the project's convention), no unresolved blocking
   comments, branch not superseded. Anything failing this is reported and dropped from scope — never merged
   "while we're here".
2. **Order.** Determine dependency and stacking relationships (stacked branches, `Depends on` links,
   overlapping surfaces) and compute the merge order: bases before dependents.
3. **Gate on CI, per merge, at merge time.** Immediately before each merge, re-query the required checks on
   the current head — only its own completed checks count; a local run, an earlier head's green, or
   timing inferred from another change never stands in for them. A
   pending or failing required check stops that merge (and its dependents) until resolved.
4. **Merge in order,** using the platform's recorded merge mechanics (squash policy, branch cleanup).
5. **Reconcile after each merge.** Update or rebase dependent branches as needed; resolve conflicts only when
   the intended resolution is mechanical and unambiguous (keep-both provenance, regenerated artifacts,
   lockfile refresh + the project's install command). Re-run the affected checks after any reconciliation.
6. **Stop and report, don't guess.** A conflict needing product or implementation judgment, a check that
   fails after reconciliation, or a scope ambiguity stops the run with the blocker named — the remaining
   queue is left unmerged and reported.
7. **Report.** Merged PRs with resulting commit SHAs, the order used, reconciliations performed, and anything
   left unmerged with its reason. Apply the tracker's post-merge lifecycle (labels, issue closure) where the
   platform binding records it. Then clean up: delete merged branches per platform policy, remove their
   worktrees, and tear down any per-change environment resources (containers, seeded stores) the
   repo's environment playbook (`docs/agents/environment.md`, when it has one) names.

## Boundaries

- Never merge outside the request's scope.
- Never force-push over, close, or delete someone else's branch to make a merge work.
- The whole flow is judgment-light coordination — it stays with this session; delegate nothing but
  mechanical check-watching (via the `watch-until` sibling when installed).
