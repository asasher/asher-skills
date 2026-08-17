# Interview — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: run each against both executors (a Claude subagent via the Agent tool, and `codex exec --sandbox read-only` on the roster's Codex model), with **only `SKILL.md` in context**, requiring an exact-sentence citation per answer. Flagging genuine ambiguity (with a citation) is a valid answer. Key written before any runs.

## Scenario

You are running the `interview` skill. The user opened with: "Here's the vendor's API PDF and our repo — I want a driver-payout feature. Interview me." The PDF documents payout endpoints and rate limits; the repo has a payments module.

## Probes

**P1 (intake).** Your first-round draft includes "What are the vendor API's rate limits?" Keep or cut, and why? Cite.

**P2 (frontier).** Five decisions are open: payout cadence, minimum threshold, currency handling, notification channel, retry policy — threshold and retry both depend on the cadence answer. What goes in round 1? Cite.

**P3 (facts vs decisions).** "Which queue library does our payments module use?" and "should payouts be instant or batched?" — who answers each, and how? Cite the split.

**P4 (non-blocking lookup).** A dispatched lookup on settlement timing hasn't returned; the rest of the frontier is ready. Wait or ask? Cite.

**P5 (recommended answer).** Show the form each round-1 question must take. Cite.

**P6 (degrade).** The `to-subagent` skill is not installed and a question needs a fact from the vendor docs. What do you do? Cite.

**P7 (stopping).** The frontier is empty and you believe you understand the feature. Do you start acting on it? Cite.

## Answer key

- **P1:** Cut — the rate limits are in the provided PDF: "**Intake first** — read what was handed to this session before the first round." Keeping the question = **fail**.
- **P2:** Cadence, currency, notification — the whole askable frontier; threshold and retry wait, their prerequisite (cadence) is still open: "The **frontier** is every decision whose prerequisites are already settled." Asking all five, or only one, = **fail**.
- **P3:** The queue library is a fact — "Finding **facts** is your job, never the user's" (look it up / dispatch a lookup). Instant-vs-batched is a decision — "The **decisions** are the user's — put each to them and wait." Asking the user the fact, or deciding cadence yourself, = **fail**.
- **P4:** Ask the rest now — "A running lookup is an unsettled prerequisite: only its downstream questions wait for the subagent to report — ask the rest of the frontier now." Blocking the round = **fail**.
- **P5:** Numbered questions, each with a recommended answer: "number each question and give your recommended answer." Unnumbered or recommendation-free = **fail**.
- **P6:** "dispatch a lookup via the `to-subagent` skill (absent it, look it up in-session)" — the lookup happens either way; asking the user instead = **fail**.
- **P7:** No — "The session is done when the frontier is empty — every assumption surfaced as a decision — and the user confirms shared understanding." Acting on frontier-empty alone = **fail**.

Pass bar: **7/7 on both executors.**
