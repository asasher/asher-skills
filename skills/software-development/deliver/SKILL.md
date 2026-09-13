---
name: deliver
description: Build one ready GitHub ticket in its own worktree, verify it, and leave an ordinary PR for human review.
metadata:
  requires: [adversarial-review, capture, implement, prove-your-work, to-thread]
  optional: [technical-writing]
---

# Deliver

Own one ticket through implementation, proof, and a review-ready PR. Perform routine stages in this session; delegate only independent checks or bounded work that benefits from another context.

## Start or resume

Read the ticket and comments, existing PR, and `docs/agents/environment.md`. Failed reads or an unready environment are blockers. Require an approved direction or a clear ticket with delegated implementation choices. Require no open blocker. Admit either a `ready-for-agent` ticket with no live owner, or a newly reserved `building` ticket whose dispatch claim identifies this launch. Adopt that reservation rather than treating it as a prior worker. A resume uses its ownership checkpoint after confirming the prior worker stopped; expiry alone is insufficient. Record ownership before editing.

Use the ticket's worktree. From the primary checkout or wrong branch, dispatch `deliver <ticket>` through `to-thread`, requesting the correct branch and worktree, then hand off before editing. Resume existing local or remote work; keep the primary checkout stable.

| Ticket | Brief | Branch and PR target |
| --- | --- | --- |
| Clear, unshaped | Ticket text | Work branch → configured base |
| Shaped | Spec at its approved revision | Existing work branch → base |
| Child of a split | Parent spec, narrowed by child's criteria | Child branch from and into spec branch |
| Split parent (`spec`) | Whole approved spec | Spec branch → base, after every child is merged or explicitly excluded |

Check the ticket's source revision against the latest approved spec and any newer unapproved revision. For a child, also check the parent's approval and the split's bound revision; changed direction returns to shaping before implementation. Record a checkpoint on the ticket, then the PR once it exists: branch and target, spec revision, risk, stage, checked head/base and integration tree, report links, remaining review budget, deadline, and next action. Resume from actual commits and records; stale or missing proof is unfinished work.

## Build and prove

1. Validate the worktree's stack, auth, seed, and artifact upload access. Bring up only what is missing. Record setup gaps before implementation; use the stop outcomes below.
2. Run `implement` here. Choose undeclared test seams within the ticket's authority and record them. For a split parent, first account for every approved criterion against merged child work. Fix only small integration gaps inline. Propose missing slice-sized work through `capture <parent>`; obtain the required publication decision, wire and verify the new blockers, and stop promotion while gaps remain.
3. Commit and push coherent changes as they land, before checks are handed off, and before pausing. Open an **ordinary PR**, never a draft, once implementation checks pass. Reuse its existing PR on resume. Use the correct target and `Closes #<ticket>` only for the default branch; other targets need explicit ticket closure after merge.
4. Run `adversarial-review` here with the criteria, risk, worktree, checkpoint, and deadline. It owns the bounded check/fix loop. Record a stop for product questions, exhausted bounds, or incomplete verification; preserve the consumed budget.
5. Run `prove-your-work` here with the accepted verification report. Evidence or late-CI defects return to the same loop with its remaining budget.

Keep the PR body current: change and rationale, risk and test choices, check summary, current evidence link, and checkpoint. The evidence report owns per-criterion detail. Mark review-readiness after the finish gates below pass.

## Finish

Require verification, independent review, evidence, and required CI for the current head and reviewed base. Disclose the human's authorization for each named, head-specific verification waiver. Input movement reopens the existing loop with its remaining budget.

On a stop, record its reason, remaining budget, next actor, and worker liveness. Product decisions or an unapproved split return to `needs-shaping`; environment failures, exhausted bounds, and incomplete verification requiring human action return to `ready-for-human`. Published coverage gaps return the parent to `ready-for-agent` behind the verified blockers; an unresolved publication decision returns it to `ready-for-human`. Change routing only after writers have stopped; uncertain liveness retains `building` and its reservation.

Post the PR pointer and outcome on the ticket. Preserve stopped work and its next action for another machine. Merging waits for the human's named selection. Use `technical-writing` for durable records when available.
