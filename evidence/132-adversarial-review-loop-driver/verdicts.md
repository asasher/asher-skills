# Probe verdicts — adversarial-review rework (#132)

Dual-executor per `docs/agents/probe-evals.md`: Claude subagent in-session (`before-claude.md`,
`after-claude.md`) and gpt-5.6-sol via `codex exec -s read-only` (`before-codex.txt`,
`after-codex.txt`). Probes and answer key: `skills/software-development/adversarial-review/evals/probes.md`
— key written before any run. BEFORE = the skill text as of `main` (`59069f6`); AFTER = the reworked
text on this branch. Grading is against the prewritten key; "pass*" marks an answer that reached the
keyed behavior by inference without an explicit contract sentence to cite — the gap the rework closes.

| Probe | Criterion (key) | Before: Claude | Before: Codex | After: Claude | After: Codex |
|---|---|---|---|---|---|
| P1 reviewer's hands | never edits code; post as finding | pass | pass | pass | pass |
| P2 LGTM bar | cap with open finding → unresolved, never LGTM | pass | pass | pass | pass |
| P3 crash recovery | respawn from persisted CR state alone | pass | pass | pass | pass |
| P4 product question | stop, surface for human ruling | pass | pass | pass | pass |
| P5 fixer disagreement | fix or reasoned non-fix reply; no silence | pass | pass | pass | pass |
| P6 mid-loop turn boundary | stay in turn; tracked return is the wake; no poll | **fail** (AMBIGUOUS) | **fail** (AMBIGUOUS) | pass | pass |
| P7 after convergence | returned pass is complete; report now | pass* | pass* | pass | pass |
| P8 state-comment SHA | read at writing time, never retyped | pass* | **fail** (AMBIGUOUS) | pass | pass |
| P9 undeliverable report | post outcome on the change request | pass* | **fail** (AMBIGUOUS) | pass | pass |

Totals against the key's explicit-citation bar: BEFORE 5/9 (Claude, +3 by-inference) and 5/9 (Codex);
AFTER 9/9 and 9/9. Both BEFORE executors flagged P6 as undecidable from the text — the same gap the
two production stalls fell into (PRs #130, #131): the text never told the session driving the loop
what a turn boundary means for it.

The AFTER transcripts here are from the shipped text (post cold-reader fixes). An intermediate AFTER
run against the pre-cold-reader draft of the same rework also scored 9/9 on both executors, so the
prose fixes did not move any verdict.
