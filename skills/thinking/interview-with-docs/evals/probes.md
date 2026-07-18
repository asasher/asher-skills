# Interview With Docs — situated dry-run probes

Per `docs/agents/probe-evals.md`: both executors, with **only
`skills/thinking/interview-with-docs/SKILL.md` in context** (the composition surface — not the siblings),
exact-sentence citations required. Key written before any runs.

## Probes

**P1 (division of labor).** During a session a term crystallises. Which composed skill asks the questions,
which one writes, and when does the write happen? Cite.

**P2 (degradation).** The `domain-modeling` skill is not installed in this project. What do you do? Cite.

**P3 (what survives).** The session ends. What exactly is durable, where does the open-thread classification
go, and what happens to the rest of the conversation? Cite.

## Answer key

- **P1:** `interview` asks; `domain-modeling` extracts — "inline, the moment things crystallise … never
  batched to the end." Batching, or the interview writing directly, = **fail**.
- **P2:** "State the requirement and offer the degraded form — bare `interview` with the classification
  recorded in the conversation only — rather than failing silently." Proceeding as if composed, or aborting
  without the offer, = **fail**.
- **P3:** Durable: CONTEXT.md terms, three-gate ADRs, and the exit classification "written where the caller
  directs — an issue comment, a spec's Notes." The rest "deliberately evaporates with the conversation: the
  extraction *is* the record, not a transcript." Claiming a transcript/ledger survives = **fail**.

Pass bar: **3/3 on both executors.**
