# Watch-Until — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You need to wait on a change request until the reviewer posts LGTM, and separately on a CI run that
takes about eight minutes.

## Probes

**P1 (condition).** "Watch until the code is good" — acceptable condition? Fix it and cite the rule.

**P2 (judgment conditions).** Is "no unaddressed findings remain" a legal condition even though it takes
judgment? Cite.

**P3 (tracked child).** The CI run is a harness-tracked child of this session. What's the watch? Cite.

**P4 (cadence).** The CI run is external (not tracked) and `to-subagent` is absent. Describe the
polling. Cite.

**P5 (trigger and timeout).** LGTM lands — what do you relay, and what happens if the timeout had
expired first? Cite.

## Answer key

- **P1:** Not as stated — the condition must be "decidable from the observation"; restate it
  observably ("a maintainer comment containing LGTM"). "State it so the watcher can decide it from what
  it observes." Accepting the vague form = **fail**.
- **P2:** Yes — conditions may be "a judgment the watcher is equipped to make ('no unaddressed findings
  remain', 'the iteration cap is reached')." Rejecting judgment conditions outright = **fail**.
- **P3:** "do nothing — completion wakes you. Polling a tracked child is pure waste." Any polling here =
  **fail**.
- **P4:** "Poll from this session, at the cadence the target actually changes — an eight-minute CI run
  deserves one check near minute eight, not eight one-minute checks." Minute-by-minute polling =
  **fail**.
- **P5:** "Quote the triggering observation" and stop — "the watch observes and relays, it never acts on
  the content." On expiry: "the watch ends and reports **timed out** to the caller — the condition
  unmet, plus the last observed state." Acting on the content, relaying a timeout as a trigger, or
  watching past the timeout, = **fail**.

Pass bar: **5/5 on both executors.**
