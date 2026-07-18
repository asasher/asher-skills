# Interview — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: run each against both executors (a Claude subagent
via the Agent tool, and `codex exec --sandbox read-only` on the roster's Codex model), with **only
`skills/thinking/interview/SKILL.md` in context**, requiring an exact-sentence citation per answer. Flagging
genuine ambiguity (with a citation) is a valid answer. Key written before any runs.

## Scenario

You are running the `interview` skill. The user opened with: "Here's the vendor's API PDF and our repo —
I want a driver-payout feature. Interview me." Intake found: the PDF documents payout endpoints and rate
limits; the repo has `PRODUCT.md` (register: product) and a payments module; no `CONTEXT.md`.

## Probes

**P1 (intake).** Your first-round draft includes "What are the vendor API's rate limits?" Keep or cut, and
what do you do instead? Cite the sentence.

**P2 (frontier).** Five decisions are open: payout cadence, minimum threshold, currency handling, driver
notification channel, and failure-retry policy — but threshold and retry policy both depend on the cadence
answer. What exactly goes in round 1? Cite the frontier definition.

**P3 (fact vs decision).** "Which queue library does our payments module already use?" — ask the user, or
something else? And "should payouts be instant or batched?" — who answers that? Cite the split.

**P4 (running lookup).** You dispatched a lookup on the vendor's settlement timing and it hasn't returned.
The rest of the frontier is ready. Do you wait? Cite the sentence.

**P5 (stopping).** The frontier is empty and the user says "great, I think we're aligned — go build."
Failure states and rollout were never discussed. Are you done? What happens next? Cite both stopping tests.

**P6 (no durable writes).** During the session "payout" vs "settlement" got settled as distinct terms. Do
you write CONTEXT.md now? What is the bare skill's record, and which skill would write it? Cite.

**P7 (hypothesis framing).** For payout cadence you believe weekly is right. Show the shape your question
must take — what must the recommendation carry, and what four answers must be cheap? Cite.

## Answer key

- **P1:** Cut — it's a **fact in provided material**: "Provided artifacts are read, not asked about: a
  question whose answer is in the material is never put to the user." Rate limits come from the PDF (intake).
  Keeping the question = **fail**.
- **P2:** Round 1 = cadence, currency handling, notification channel — the whole *unblocked* frontier.
  Threshold and retry wait: "Questions whose answers depend on another question still open in this round
  belong to a later round." Asking all five, or only one, = **fail**.
- **P3:** The queue library is a fact — look it up in the repo ("Never ask the user for anything you could
  find"). Instant-vs-batched is a decision — "A decision is the user's. Put each one to them and wait."
  Asking the user the fact, or deciding the cadence yourself, = **fail**.
- **P4:** No — "A running lookup is an unsettled prerequisite: only the questions downstream of it wait —
  ask the rest of the frontier now." Blocking the whole round = **fail**.
- **P5:** Not done. Stopping needs **both** tests: empty frontier **and** coverage — "A family with a
  material unasked question reopens the frontier" (failure states, rollout are named families), and
  "'We feel aligned' is the sign-off, never the test." Next: reopen the frontier with those families'
  questions. Accepting the user's sign-off as the test = **fail**.
- **P6:** No durable write — "This skill records nothing durable: settled terms and decisions live in the
  conversation and the playback." The writing variant is `interview-with-docs` (composing
  `domain-modeling`). Writing CONTEXT.md from bare `interview` = **fail**.
- **P7:** A **recommended hypothesis with its trade-off — labelled as provisional, never presented as a
  default the user is nudged to accept**, with **accept / modify / defer / unknown** all cheap. Missing the
  trade-off or the four affordances = **fail**.

Pass bar: **7/7 on both executors.**
