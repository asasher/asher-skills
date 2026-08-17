# to-tailnet — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

A status report at `docs/reports/payouts.html` needs viewing; the user is on their phone.

## Probes

**P1 (detachment).** The serve command succeeded. What does the report carry? Cite.

**P2 (repo conventions).** Where do the tailnet host and port rules come from? Cite.

**P3 (purity).** Does serving modify or copy the committed file? Cite.

## Answer key

- **P1:** "Done when the user has the exact URL and an exact, copy-pasteable stop command" — and the server is detached ("the server outlives this turn"). Omitting the stop command = **fail**.
- **P2:** "The consuming repo's `docs/agents/environment.md` records the tailnet host, port ranges, and any reverse-proxy rules where the repo has them — honor them; absent any record, bind to the machine's Tailscale address (`tailscale ip -4`)." Inventing a host, or pointing at a machine-level instruction file, = **fail**.
- **P3:** No — "The file is served in place, unmodified." Editing or copying the committed file = **fail**.

Pass bar: **3/3 on both executors.**
