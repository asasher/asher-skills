# Code Review — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` +
`reference/smells.md` + `reference/structure.md` in context**, exact-sentence citation per answer.
Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are reviewing branch `142-payout-summary`. The repo's `CONTRIBUTING.md` endorses long parameter
lists for builder functions. No ticket reference or spec can be found anywhere.

## Probes

**P1 (fail fast).** What do you confirm before dispatching anything, and why there? Cite.

**P2 (repo overrides).** The diff has a five-parameter builder — Data Clumps per the baseline. Flag it?
Cite.

**P3 (no spec).** Nothing identifies a spec. What does the Spec axis do? Cite.

**P4 (aggregation).** Suppose a spec *had* been found, Standards reported 4 issues, and Spec reported 1
severe one. Present a single ranked list? Cite.

**P5 (smell posture).** How is a baseline smell reported — hard violation or something else? Cite.

**P6 (degrade).** `to-subagent` is not installed. How do the axes run? Cite.

**P7 (structural ambition).** The diff adds a fourth boolean flag to an already busy function; each
flag works correctly and no documented standard forbids flags. Clean Standards pass? Cite.

## Answer key

- **P1:** "Confirm the ref resolves (`git rev-parse`) and the diff is non-empty before dispatching
  anything — a bad ref or empty diff fails here, not inside two subagents." Dispatching first =
  **fail**.
- **P2:** No — "**The repo overrides.** A documented repo standard always wins; where it endorses
  something the baseline would flag, suppress the smell." Flagging it = **fail**.
- **P3:** "the Spec axis skips and the report says 'no spec available'" (after the search order:
  ticket references → argument path → `docs/specs/` → ask). Inventing a spec = **fail**.
- **P4:** No — "Do **not** merge or rerank findings across axes"; per-axis totals and worst issue
  within each; "Don't pick a single winner across axes." A merged ranking = **fail**.
- **P5:** "Each smell is a labelled heuristic ('possible Feature Envy'), never a hard violation — and,
  like any standard here, skip anything tooling already enforces." Hard-violation framing = **fail**.
- **P6:** "absent it, run them yourself, Standards first, in one pass each." Refusing to review =
  **fail**.
- **P7:** No — a presumptive blocker: "Ad-hoc conditionals, one-off flags, or scattered special cases
  bolted into unrelated flows — a design problem, not a stylistic nit," and "Correct behavior alone is
  not a clean Standards pass." The finding sketches the simpler reframing. Passing it because it works
  and no documented standard forbids it = **fail**.

Pass bar: **7/7 on both executors.**
