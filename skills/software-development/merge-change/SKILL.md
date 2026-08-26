---
name: merge-change
description: Merge review-ready changes on the user's explicit request — the human authorization gate.
metadata:
  requires: [worktree]
  optional: [writing-for-humans, watch-until]
---

# Merge Change

A request may name several changes; each passes the gate one at a time.

Merging is a human-authorized operation. Automated review approval, green checks, `ready-for-agent`, or a reviewer's `LGTM` are prerequisites where configured — **they are never authorization to merge**. Authorization is the user's explicit merge request: invoking this skill, or naming the changes to merge in their own words. Operate only on the changes named or unambiguously included in that request — "merge #51" does not license merging its stack-mates.

Platform verbs (merge, checks-read, PR-read, branch ops) come from the project's `docs/agents/platform.md` when present; on a bare GitHub repo, use `gh` directly. With neither a `platform.md` nor a GitHub remote to drive with `gh`, state the gap and stop.

Reports follow the `writing-for-humans` sibling. Absent it, write plainly and say the standard was not loaded.

## Steps

1. **Resolve scope.** Enumerate the exact change requests the request names. For each, verify it is still open and review-ready: review converged (approval/`LGTM` per the project's convention), no unresolved blocking comments, branch not superseded — and the approval is not stale: an approval is stale when commits landed after the head it covers (the named SHA, or the head current when it was posted); a stale approval sends the change back through review, never into the merge. Anything failing this is reported and dropped from scope — never merged "while we're here". A scope ambiguity stops the run with the ambiguity named.
2. **Order.** Determine dependency and stacking relationships (stacked branches, `Depends on` links, overlapping surfaces) and compute the merge order: bases before dependents.
3. **Gate on CI.** Immediately before each merge, re-query the required checks on the current head — only its own completed checks count; a local run, an earlier head's green, or timing inferred from another change never stands in for them. A pending or failing required check stops that merge (and its dependents) until resolved.
4. **Merge in order,** using the platform's recorded merge mechanics (squash policy). A slice merging into a **feature branch** gets its ticket the `delivered` label role in the same act as the merge: `Closes #n` fires only on default-branch merges, so the slice ticket does not close here — it stays open and `delivered`, awaiting promotion, and closes natively when the promotion change request (the spec ticket's change request into the default branch, carrying one `Closes` line per slice) merges. Apply the tracker's post-merge lifecycle (remaining labels and issue closure) where the platform binding records it. Branch deletion stays out of the merge verb: it is step 6's, after working-copy teardown — a delete bundled into the merge fails on the held local branch.
5. **Reconcile after each merge.** Update or rebase dependent branches; reconciliation is done when every open dependent branch contains the merged base and its required checks have been re-queried green — or its blocker is named in the report. Conflicts resolve on a three-rung ladder — always resolve at the lowest rung that answers, never abort where a rung does:
   - **Rung 1 — mechanical.** Keep-both resolutions of additive lists (changelogs, provenance files), lockfile refresh plus the project's install command, regenerated artifacts. Resolve.
   - **Rung 2 — intent-resolvable.** Trace both sides to their specs and tickets — intent is addressable by construction: spec projections, blessed hashes, change descriptions. Resolve by the documented intent, never by inventing behavior neither side documents, and record the trade-off on the change request.
   - **Rung 3 — spec versus spec.** Two blessed intents genuinely contradict. That is a shaping collision, not a merge decision: stop and report it for the human — the remaining queue is left unmerged.
6. **Clean up.** Remove each merged change's working copy through the `worktree` skill — its Remove owns the teardown order (environment torn down from inside the working copy, then the copy itself) and refuses dirty or unregistered paths. Only then delete each merged branch, local and remote, per platform policy, and **verify both are gone by querying them**: on git, `git branch --list <branch>` and `git ls-remote --heads origin <branch>`, both returning nothing. Report a branch as deleted only on the strength of those queries — a failed delete reports on stderr, easy to skim past. A feature branch that open-and-`delivered` slices still target outlives its slice merges; tear it down only after the promotion change request merges.
7. **Report.** Merged change requests with resulting commit SHAs, the order used, reconciliations performed with any rung-2 trade-offs recorded, teardown outcomes (working copies removed, branches verified gone), and anything left unmerged with its reason.

## Boundaries

- A merge blocked by someone else's branch stops with the blocker named — never force-push over, close, or delete that branch to make the merge work.
- The whole flow is judgment-light coordination — it stays with this session; delegate nothing but mechanical check-watching, via the `watch-until` sibling; absent it, watch the checks in this session.
