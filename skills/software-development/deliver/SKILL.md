---
name: deliver
description: Build one ready GitHub ticket in its own worktree, verify it, and leave an ordinary PR for human review.
metadata:
  requires: [adversarial-review, implement, prove-your-work, to-thread]
  optional: [technical-writing]
---

# Deliver

Own one ticket through implementation, proof, and a review-ready PR. Perform routine stages in this session; delegate only independent checks or bounded work that benefits from another context.

## Start or resume

Read the ticket and comments, existing PR, and `docs/agents/environment.md`. Failed reads or an unready environment are blockers. Require an approved direction or a clear ticket with delegated implementation choices. A new build requires `ready-for-agent` and no open blocker; a resume requires its existing ownership checkpoint and a stopped prior worker. Record or adopt the ticket claim before editing.

Use the ticket's worktree. From the primary checkout or wrong branch, dispatch `deliver <ticket>` through `to-thread`, requesting the correct branch and worktree, then hand off before editing. Resume existing local or remote work; keep the primary checkout stable.

| Ticket | Brief | Branch and PR target |
| --- | --- | --- |
| Clear, unshaped | Ticket text | Work branch → configured base |
| Shaped | Spec at its approved revision | Existing work branch → base |
| Child of a split | Parent spec, narrowed by child's criteria | Child branch from and into spec branch |
| Split parent (`spec`) | Whole approved spec | Spec branch → base, after every child is merged or explicitly excluded |

Check approval against the latest spec revision. Record a checkpoint on the ticket, then the PR once it exists: branch and target, spec revision, risk, stage, checked head/base, report links, remaining review budget, deadline, and next action. Resume from actual commits and records; stale or missing proof is unfinished work.

## Build and prove

1. Validate the worktree's stack, auth, seed, and artifact upload access. Bring up only what is missing. A unit needing a new product decision or a larger split returns to `needs-shaping` with the discovery recorded.
2. Run `implement` here. Choose undeclared test seams within the ticket's authority and record them. For a split parent, start from merged child work and limit fixes to small integration gaps.
3. Commit and push coherent changes as they land, before checks are handed off, and before pausing. Open an **ordinary PR**, never a draft, once implementation checks pass. Reuse its existing PR on resume. Use the correct target and `Closes #<ticket>` only for the default branch; other targets need explicit ticket closure after merge.
4. Run `adversarial-review` here with the criteria, risk, worktree, checkpoint, and deadline. It owns the bounded check/fix loop. Record a stop for product questions, exhausted bounds, or incomplete verification; preserve the consumed budget.
5. Run `prove-your-work` here with the accepted verification report. Evidence or late-CI defects return to the same loop with its remaining budget.

Keep the PR body current: change and rationale, risk and test choices, checks, per-criterion verification, evidence link, and checkpoint. Mark review-readiness after the finish gates below pass.

## Finish

Require verification, independent review, evidence, and required CI for the current head and reviewed base. Disclose any explicit head-specific verification waiver. On input movement, renew affected checks and review before claiming completion.

Post the PR URL, head, proof, remaining risks, and outcome on the ticket. Preserve stopped work and its next action for another machine. Merging waits for the human's named selection. Use `technical-writing` for durable records when available.
