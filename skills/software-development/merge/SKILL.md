---
name: merge
description: Merge review-ready PRs on the user's explicit request — the human authorization gate.
disable-model-invocation: true
metadata:
  requires: [worktree]
  optional: [writing-for-humans]
---

# Merge

A request may name several PRs; each passes the gate one at a time.

Merging is a human-authorized operation. Automated review approval, green checks, `ready-for-agent`, or a reviewer's `LGTM` are prerequisites where configured; they are never authorization to merge. Authorization is the user's explicit merge request: invoking this skill, or naming the PRs to merge in their own words. Operate only on the PRs named or unambiguously included in that request: "merge #51" does not license merging its stack-mates.

Reports follow the `writing-for-humans` sibling. Absent it, write plainly and say the standard was not loaded.

## Steps

1. **Resolve scope.** Enumerate the exact PRs the request names. For each, verify it is still open and review-ready: review converged with an `LGTM` naming a head, no unresolved blocking comments, branch not superseded, and the approval not stale. An approval is stale when commits landed after the head it covers; a stale approval sends the PR back through review, never into the merge. Anything failing this is reported and dropped from scope. A scope ambiguity stops the run with the ambiguity named.
2. **Order.** Determine dependency and stacking relationships (a child PR into a spec branch, `Depends on` links, overlapping surfaces) and compute the merge order: bases before dependents.
3. **Gate on CI.** Immediately before each merge, re-query the required checks on the current head with `gh pr checks`; only its own completed checks count. A pending check is watched at the cadence it actually changes: an eight-minute run deserves one check near minute eight, not a poll every thirty seconds. A failing required check stops that merge and its dependents until resolved.
4. **Merge in order** with `gh pr merge`, squash unless the repo says otherwise. A child's PR into a spec branch does not close its issue, because `Closes` fires only on the base branch: close the child yourself in the same act, `gh issue close <child> --comment "Merged into <spec branch> at <sha>"`. That closure is what clears the spec issue's blocker. A PR into the base branch closes its issue through its `Closes` line. Branch deletion stays out of the merge verb: it is step 6's, after working-copy teardown, since a delete bundled into the merge fails on the held local branch.
5. **Reconcile after each merge.** Update or rebase dependent branches; reconciliation is done when every open dependent branch contains the merged base and its required checks have been re-queried green, or its blocker is named in the report. Conflicts resolve on a three-rung ladder, always at the lowest rung that answers:
   - **Rung 1, mechanical.** Keep-both resolutions of additive lists, lockfile refresh plus the project's install command, regenerated artifacts. Resolve.
   - **Rung 2, intent-resolvable.** Trace both sides to their specs and issues; resolve by the documented intent, never by inventing behavior neither side documents, and record the trade-off on the PR.
   - **Rung 3, spec versus spec.** Two blessed intents genuinely contradict. That is a shaping collision, not a merge decision: stop and report it for the human; the remaining queue is left unmerged.
6. **Clean up.** Remove each merged PR's working copy through the `worktree` skill; its Remove owns the teardown order and refuses dirty or unregistered paths. Then delete each merged branch, local and remote, and verify both are gone by querying them: `git branch --list <branch>` and `git ls-remote --heads origin <branch>`, both returning nothing. For each issue this merge closed, delete its `artifact/<issue>` branch the same way. A spec branch that open children still target outlives its child merges; tear it down only after the promotion PR merges.
7. **Report.** Merged PRs with resulting commit SHAs, the order used, reconciliations performed with any rung-2 trade-offs recorded, issues closed, teardown outcomes (working copies removed, branches verified gone), and anything left unmerged with its reason.

## Boundaries

- A merge blocked by someone else's branch stops with the blocker named: never force-push over, close, or delete that branch to make the merge work.
- The whole flow is judgment-light coordination and stays with this session. Nothing is delegated.
