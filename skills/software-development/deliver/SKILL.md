---
name: deliver
description: Take one unit of work to a review-ready PR in one worktree, or resume it from its issue and PR records.
metadata:
  requires: [adversarial-review, implement, prove-your-work, to-subagent, verify-your-work]
  optional: [capture, technical-writing]
---

# Deliver

Own one issue or spec'd unit through implementation, convergence, and evidence. Dispatch workers via `to-subagent` as blocking calls in this exact worktree. Keep one writer: implementation and fixes finish before checks start; every check returns before another writer starts. The session coordinates and validates results.

Use `technical-writing` for durable text when available; otherwise write plainly.

## 1. Read and resume

Read `docs/agents/environment.md`, the issue with `gh issue view <n> --comments`, its claim, and any existing PR. A failed issue read is a blocker; a dispatch paraphrase cannot replace it. Without an issue, use the supplied spec and the branch's PR as the record.

The unit determines the brief and target:

- **Unshaped issue**: the issue text is the brief. Choose undeclared test seams and the guard/throwaway split within its authority boundary; record the choices in the PR.
- **Shaped issue**: read the spec at its blessed artifact-branch hash. Check the artifact branch still names that revision; a later revision returns the issue to shaping.
- **Child of a spec issue**: read the parent's blessed spec, narrowed by the child's acceptance criteria and test contract. Target the spec branch.
- **Spec issue**: confirm every child closed and inspect its merged PR. A closed child without merged work needs an explicit scope ruling. Use the whole spec as the claims and the spec branch as the work branch. The convergence loop performs the coverage check before promotion.

All other PRs target the base branch from the playbook. For children and spec issues too, compare the parent's artifact tip with its blessing before building; stale readiness returns to shaping.

Maintain one checkpoint: on the issue before a PR exists, then in the PR body with a pointer from the issue. For issueless work before PR creation, use an untracked scratch checkpoint and report its path. Take the absolute deadline from the claim or supplied brief; absent one, record four hours from the run's start. Record the brief's revision, target, risk, absolute deadline, pass budget consumed, worker resume reference when available, and these stages:

- Implemented at SHA, with check results and the implementer's report.
- Verified at SHA, with per-criterion verdicts, or the justified light-work omission.
- Reviewed at SHA and base SHA, with the LGTM report.
- Evidence at SHA, with the package pointer.
- Review-ready, or stopped with its reason and next action.

Update the checkpoint after each returned stage and before pausing. On resume, compare it with the local branch, remote head, PR comments, and artifacts. Reuse only results whose inputs still match; missing proof is pending work. Resume at the first incomplete stage, preserving consumed passes and the deadline. A stopped bound or product question remains stopped until its recorded condition is resolved. A stopped bound may resume only through the convergence driver's recorded extension ruling, never by a fresh default budget. Inspect dirty work and ownership before resuming; preserve unexplained changes. Reuse an existing PR instead of opening another.

## 2. Provision and size the work

Bring up or validate the stack using the playbook's recipes: dependencies, environment, migrations, seed, and a relevant check. Reuse an already healthy stack. Report an environment gap before dispatching a builder. Independent source reads may overlap provisioning, but checks wait for a healthy stack.

Record what must happen first, any shared mutable state, and whether the unit is still one independently demoable slice. Several layers or disjoint files can belong to one slice. If the work needs multiple independently deliverable slices or contradicts its blessed scope, record the discovery, return the issue to `needs-shaping`, and stop for a revised direction.

Choose verification depth from the actual risk, retaining or increasing the spec's declaration:

- **Light**: demonstrably no executable behavior, interface, deployment, permission, or data change. Run the relevant checks and one review context covering both axes. A separate behavioral verifier may be omitted with the reason recorded.
- **Normal**: behavioral changes require independent behavioral verification and review.
- **High**: auth, money, destructive data operations, or interactions across surfaces require verification of the affected boundaries and failure paths. Data changes also require a runtime data-safety check.

File count never determines risk. Dispatch read-only exploration only for specific unresolved code questions whose answers the builder needs. Include the returned findings in the implementation brief.

## 3. Implement and open the PR

Dispatch `implement` with the brief, risk, seams, test split, and deadline. Retain its report and resume reference for fixes. For a spec issue whose children already supplied the implementation, proceed from their merged commits instead.

When implementation checks pass, remove probe residue, retain verification runs outside the tracked tree, and push the clean branch. Open the PR now, draft by default unless the playbook records another convention. CI can run while convergence proceeds.

The PR body carries:

- `Closes #<issue>` only when targeting the repository's default branch. For a child targeting a spec branch, name the child without a closing keyword. For a different configured base, record that issue closure must be explicit after merge. Without an issue, identify the supplied spec and its revision when one exists.
- What changed, why, and any scope discovery or delegated decisions.
- Risk, test seams, and the per-criterion guard/throwaway split.
- Check commands and results; required CI status, including pending or failed checks.
- Verification and evidence pointers, initially pending.
- The checkpoint from step 1.

## 4. Converge

Run `adversarial-review` as the driver in this session. Supply the claims and test contract for behavioral verification, risk, exact directory, implementation report and resume reference, consumed passes, any head-specific verification waivers, and absolute deadline. For a spec issue, limit fixes to small coverage gaps; a missing independently deliverable slice requires a product question. Light work may explicitly omit behavioral verification. Set the total review-pass budget to two for light work and three otherwise unless the work requires another stated budget. One pass is sufficient when it returns clean.

Act on its returned outcome:

- **Converged**: accept only current-head verification and LGTM, then record both in the checkpoint.
- **Product question**: record it, return the issue to `needs-shaping`, and stop for a ruling.
- **Stopped at a bound** or **verification incomplete**: persist the reports and remaining work, report the blocker, and stop. Keep the consumed budget; restarting the skill is not an extension.

For a spec issue, verification covers every criterion against the merged whole, including seed reach. A missing slice returns the parent to shaping and stops promotion. Use `capture <parent>` for the gap only when issue publication is already authorized or an attending user confirms it; otherwise persist the proposed gap on the parent for the next shaping session.

## 5. Evidence and completion

Dispatch `prove-your-work` with the converged SHA and verification artifacts. Reuse captures whose code, fixture state, and environment still match. Light work may use a compact package of checks and their results. A newly discovered defect reopens the same convergence run with its remaining budget; a used-up budget remains a stop.

Before reporting review-ready, confirm the remote head and reviewed base still match the accepted reports, the tree is clean, and evidence names that head. A moved head invalidates verification, review, and evidence; a moved base requires renewed integration checks and review. Required CI must be green on the current head; watch pending checks within the remaining deadline. A late CI failure reopens the same convergence run with the failing output and remaining budget; a timeout leaves the PR pending with the reason recorded. Any unverified claim needs an explicit human waiver recorded against this head before it can count as review-ready.

Mark a draft ready only after these gates pass. Report the PR URL and head, verification and review outcomes, check results, evidence, deviations, and residual risks. Post the same outcome on the issue. Merging requires explicit human authorization.
