# Prove Your Work — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are evidencing change request #88 (a web feature plus a CLI flag). The responsive layout was never
verified — no small-viewport check ran. The user was fully AFK.

## Probes

**P1 (audience).** Who is the package for, and what must it enable? Cite.

**P2 (reproducibility).** "Tests passed ✅" — acceptable proof line? What is required? Cite.

**P3 (the gap).** The unverified responsive layout: pad around it, or what? Cite.

**P4 (obligation).** How would the package differ if the user had watched the work live? Cite.

**P5 (destination).** Where does the package go? Cite.

## Answer key

- **P1:** "whoever decides to merge without having watched the work happen: the package must let them
  decide from the evidence alone." A package assuming shared context = **fail**.
- **P2:** Not acceptable — proof is "the exact command and its trimmed output," or the driver's own
  artifacts for UI; "a reader must be able to run the same command and see the same result." A bare
  checkmark = **fail**.
- **P3:** Name it — "**What was not verified, and why** — named plainly. An honest gap outranks a
  padded package; hiding an unverified claim is the one unforgivable move here." Padding = **fail**.
- **P4:** It may compress — "Work done while they watched and steered may compress to the checks and
  their results; work done fully AFK carries the complete package." Same-size-always = **fail**.
- **P5:** "Post the package on the change request, through the platform verbs recorded in
  `docs/agents/platform.md`," honoring `docs/agents/evidence.md` when present. Leaving it in chat =
  **fail**.

Pass bar: **5/5 on both executors.**
