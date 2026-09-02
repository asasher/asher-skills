---
name: adversarial-review
description: Converge a PR to LGTM through alternating reviewer and fixer passes. Use once a PR exists and needs review pressure without a human in the loop.
metadata:
  requires: [code-review, to-subagent]
  optional: [diagnosing-bugs]
---

# Adversarial Review

Two roles converge on one PR: a reviewer that re-reviews until a pass is clean, and a fixer that addresses findings until LGTM lands. The PR is their only shared state — findings, fixes, and the verdict all live in its comments and commits.

The session running this skill is the **driver**. Each role runs as one bounded pass dispatched via the `to-subagent` skill.

Both roles' briefs are in [conduct](reference/conduct.md); each dispatch carries it.

## The loop

Alternate bounded passes until `LGTM` or a bound:

1. **Review pass.** Dispatch the reviewer against the current head (conduct § Reviewer); it returns its verdict — `LGTM` naming the head it covers, or the open findings.
2. On `LGTM`, the loop is converged: report it, naming the covered head.
3. **Fix pass.** Dispatch the fixer with the open findings (conduct § Fixer); it returns its pass report.
4. Review again, from step 1.

## Turn discipline

The driver holds the loop for its whole life and returns only with an outcome: **converged** (`LGTM`, the covered head SHA) or **stopped at a bound** (the open findings and which bound) — a state comment records the loop's position, it does not keep the loop alive. Between dispatching a pass and reading its return there is nothing to watch and no poll to keep alive — the dispatched pass's completion is the wake.

A pass that has returned is complete: act on its report. No confirmation follows a return — waiting for one blocks on a message that cannot arrive.

## Bounds

An iteration cap (default: three full review passes) and a timeout (named by the caller, defaulting to one hour), both enforced by the driver on the passes it dispatches. The caller may size the cap to the change: the default suits a contained change; a large or multi-surface change warrants naming a larger cap at dispatch rather than planning on extensions. On the timeout, stop and report the open findings as unresolved; at the cap, do the same unless the § Cap exhaustion ruling below authorizes a bounded extension.

The driver names each pass's deadline in its `to-subagent` dispatch, so a pass that outlives it comes back as the dispatch's timeout return, waking the driver. A pass that dies without returning is re-dispatched from the PR's persisted state (conduct § Shared rules), picking up with the next expected actor.

## Cap exhaustion

Cap exhaustion is the bound doing its job: it forces an explicit driver ruling instead of an unbounded loop — a reported decision point, not a fault. The LGTM bar holds (conduct § Reviewer); exhaustion puts one of three rulings in front of the driver:

- **Extend** when convergence is visibly progressing — each pass resolves the prior findings and the new ones are fewer or narrower. An extension is a named number of additional passes, recorded in a state comment with its rationale; each further extension takes the same fresh ruling — never an open-ended "keep going".
- **Stop with findings open** when convergence is not visible — findings holding steady, recurring, or widening — or when the residue needs rework beyond review-scale fixes, such as a change that wants splitting. Report the open findings as unresolved per the bound-stop rule above; the caller owns what happens next.
- **Surface a product question and stop** when a remaining finding hinges on what the behavior should be — more passes cannot answer it. Route it to a human ruling per conduct's product-semantics ruling.
