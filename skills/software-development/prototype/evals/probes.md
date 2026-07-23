# Prototype — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` +
`reference/prototyping.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a
citation is valid. Key before runs.

## Scenario

You are running the `prototype` skill on "should the payout flow be a wizard or a single form?" raised
by ticket #142.

## Probes

**P1 (question).** The request had been "prototype the payout stuff." What happens before building?
Cite.

**P2 (presentation decisions).** The variants differ in which actions are overt on each step. Is that
the implementer's taste call later? Cite.

**P3 (exposure).** The three variants are built. What does gate 2 require before iterating on them?
Cite.

**P4 (capture).** The user picks the wizard. Where does the answer land? Cite.

**P5 (cleanup).** The wizard variant's code is decent. Ship it? Cite.

## Answer key

- **P1:** Narrow it — "Run on an explicit question; if it is vague, narrow it before building." One
  question per prototype ("Record one question"). Building on the vague ask = **fail**.
- **P2:** No — "An interface's non-obvious presentation choices ... are decisions, not taste calls: a
  variants prototype settles them; implementation never invents them." Deferring to the implementer =
  **fail**.
- **P3:** "Provide one command or URL and visible state. Open rendered answer sheets locally; drive
  live interactive artifacts directly." Iterating without exposing the variants = **fail**.
- **P4:** "into the record of the work that raised the question — the ticket thread, or the
  conversation that asked" — here ticket #142's thread. Leaving it only in the artifact = **fail**.
- **P5:** No — gate 4: "Absorb only the validated core into real work; the artifact leaves the
  mainline — parked on a throwaway branch pointed to from the record, or deleted." Shipping the
  prototype wholesale = **fail**.

Pass bar: **5/5 on both executors.**
