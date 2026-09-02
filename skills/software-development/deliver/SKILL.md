---
name: deliver
description: Take one unit of work — a ready GitHub issue, or a spec'd piece of work with no issue — to a review-ready PR in one worktree. Use in a session of its own.
metadata:
  requires: [adversarial-review, implement, prove-your-work, to-subagent, verify-your-work]
  optional: [capture, diagnosing-bugs, technical-writing]
---

# Deliver

Run one unit of work to a review-ready PR in one worktree. The unit is an issue, the normal dispatched path, or a spec'd piece of work with no issue. This session is the owner and the fixer; the heavy lifting is dispatched via the `to-subagent` skill into fresh contexts. Every stage dispatch is a blocking call whose return is the stage's result. Stages that can run at once are several blocking calls in one turn. Never dispatch a stage to walk away from.

PR text, reports, and issue comments follow the `technical-writing` sibling. Absent it, write plainly and say the standard was not loaded.

## 0. Provision

Bring the worktree up per `docs/agents/environment.md`: dependencies, environment files, migrations, the stack the checks need. Done when the playbook's recipes come up green: stack started, seed loaded, a check command exits 0. A gap here fails fast; report the blocker instead of letting verification discover it. While the build is live the worktree has one writer, this session and what it dispatches, and it is the one working copy for the whole pipeline: every subagent receives this exact directory.

## 1. Read the unit

With an issue, read it with `gh issue view <n> --comments` from this worktree, proving the read works where the work runs. A read that fails is a blocker to report, never a cue to build from the dispatch prompt's paraphrase. The issue is one of four kinds, and the kind decides the rest of the run:

- **Unshaped**: no spec projection on the issue. The issue text is the brief. The test split (which checks are durable guards, which are throwaway scripts) has not been declared: ask the user when one is attending; when dispatched unattended, decide it and say so in the PR body.
- **Shaped**: the issue carries a spec projection with a blessed hash. Read the spec from the artifact branch at that hash; it is the brief and declares the test split per acceptance criterion.
- **Child of a spec issue**: the parent's spec at its blessed hash is the brief, narrowed to this child's slice. The PR targets the spec branch, not the base branch.
- **Spec issue**: the `spec` label, every child closed. Run § The coverage check instead of § 2.

Without an issue, the spec handed to this session is the brief.

## 2. Implement, verify, fix

Dispatch the `implement` skill with the brief; the work lands as commits on this checkout's current branch. A change that adds a feature extends the seed in the same change.

Then dispatch the `verify-your-work` skill against the changes, fresh eyes. The verifier reports; this session fixes: go red on the finding first, on the surface the verifier saw it fail, then fix. A defect that survives a fix pass routes through the `diagnosing-bugs` skill instead of a second guess; absent that sibling, say so and run a deliberate diagnosis before any second attempt. Re-dispatch verification after fixing; loop until the report is clean.

## 3. Open the PR

Before opening, the tree is clean: only the intended changes, tool and probe residue gone, every throwaway verification script dropped, its run kept for the evidence.

Open with `gh pr create`. The target is the base branch from `environment.md`, or the spec branch for a child. The body, in this order:

- The closing reference `Closes #<issue>` when the PR targets the base branch. A child's PR carries none: `Closes` never fires on a non-default branch, and the `merge` skill closes the child at merge. Without an issue, name the spec and its blessed hash; this PR is the record.
- **Summary**: what changed and why, in the issue's terms, including any scope discovery.
- **Changes**: the significant modules with the design reasoning a reviewer needs, not a file list.
- **Checks run**: each check command from `environment.md` and its result. **CI status**: the merge gate, green or not, disclosed either way.
- **Verification**: per acceptance criterion, the outcome and which checks are guards versus dropped scripts.
- **Evidence**: a placeholder, "captured after review converges".

## 4. Adversarial review

Run the `adversarial-review` skill on the PR; it converges to LGTM or reports unresolved findings. Step 5 starts only at LGTM: fix unresolved findings through step 2's loop and re-run the review until it does.

## 5. Evidence

Dispatch the `prove-your-work` skill against the PR: the evidence package lands as a PR comment for whoever decides the merge. A defect discovered while assembling evidence stops the package; fix through step 2's loop, re-enter review, then re-assemble.

## The coverage check

For a spec issue, the children are merged into the spec branch and this worktree is on it. Dispatch `verify-your-work` with the spec at its blessed hash as the claims: every acceptance criterion against the merged whole, plus the seed reaching every feature the spec added. A small gap is fixed here through step 2's loop. A gap that is a slice of its own is filed via the `capture <spec issue>` skill, which re-blocks the spec issue; report and stop, since the coverage check re-runs when that child closes. On a clean report, open the promotion PR from the spec branch to the base branch with `Closes #<spec issue>`, then run steps 4 and 5.

## Done

Report the PR as review-ready: its URL and head SHA, the per-criterion verification verdicts, the review's converged outcome, the check commands with their exit codes, deviations from the brief with rationale, and residual risks or named gaps. With an issue, post the same as the claim's outcome comment; that is where the dispatcher and anyone else reads it. Merging waits for explicit human authorization.
