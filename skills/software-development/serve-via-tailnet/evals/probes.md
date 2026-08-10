# Serve via Tailnet — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

A status report at `docs/reports/payouts.html` needs viewing; the user is on their phone and has explicitly asked for it to be served.

## Probes

**P1 (detachment).** The serve command succeeded. What does the report carry? Cite.

**P2 (repo conventions).** Where do the tailnet root and port rules come from? Cite.

**P3 (purity).** Does serving modify or copy the committed file? Cite.

## Answer key

- **P1:** "The URL the user opens, and the stop command" — and the server is detached ("the server outlives this turn, and the URL is reported with how to stop it"). Omitting the stop command = **fail**.
- **P2:** "The consuming repo's `docs/agents/environment.md` records the tailnet root, port ranges, and any reverse-proxy rules where the repo has them — honor them; absent any record, bind to the tailscale interface address." Inventing a root, or pointing at a machine-level instruction file, = **fail**.
- **P3:** No — "The file is served in place — no chrome, no state, no diverging copy." Editing or copying the committed file = **fail**.

Pass bar: **3/3 on both executors.**
