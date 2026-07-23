# Implement — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are running the `implement` skill on ticket #142: a payout-summary feature whose ticket also
mentions "the retry handler throws on empty queues" and asks to "tidy up the payments module while
you're in there."

## Probes

**P1 (routing).** Three strands are in the ticket: the new feature, the throw-on-empty defect, the
tidy-up. Where does each go? Cite.

**P2 (seams).** The ticket names no seams for the feature. What happens before the first test? Cite.

**P3 (cadence).** When does the full test suite run, and what runs along the way? Cite.

**P4 (authority).** The ticket settles cadence=weekly but delegates the batch size. You prefer daily
cadence. What may you change? Cite.

## Answer key

- **P1:** Defect → "runs through the `diagnosing-bugs` skill"; new behavior → "runs through the `tdd`
  skill at pre-agreed seams"; tidy-up → fits neither route — flag it, citing the two routes ("A defect —
  something that should work and doesn't"; "New behavior — a feature, an enhancement"). Doing the
  tidy-up = **fail**.
- **P2:** Seams get proposed and recorded first — "the ticket or spec's named seams, or seams proposed
  and recorded before the first test." Testing at unrecorded seams = **fail**.
- **P3:** "Run typechecking and the touched test files regularly; run the full suite once at the end —
  and let each run finish before starting another in the same tree."
  Skipping the final full suite = **fail**.
- **P4:** Batch size only — "what it settles is settled; what it delegates is yours to decide and worth
  a line in the commit message." Changing cadence = **fail**.

Pass bar: **4/4 on both executors.**
