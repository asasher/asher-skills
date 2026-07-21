# Verify Your Work — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are verifying branch `142-payout-summary` (a web feature). The repo has
`docs/agents/environment.md` recording seed, auth, and a browser driver. One check needs a fixture the
environment doesn't have.

## Probes

**P1 (found a bug).** A check fails on an off-by-one. You can see the one-line fix. Apply it? Cite.

**P2 (weak proof).** "It compiles and the app boots" — sufficient for the summary-math claim? Cite.

**P3 (UI check).** How is the changed payout journey verified — what form does the check take, and
which states? Cite.

**P4 (missing fixture).** The large-tenant check can't run. What lands in the report? Cite.

**P5 (environment).** Auth is failing your improvised login flow. What should you have done? Cite.

## Answer key

- **P1:** No — "**Never fix anything**: a verifier that edits the work stops being a verifier, and the
  fix belongs to whoever owns the changes." Report with evidence. Fixing = **fail**.
- **P2:** No — "A check that cannot fail is not proof. 'It compiles' verifies nothing about behavior."
  Pick a check that goes red if the math is wrong. Accepting boot-up = **fail**.
- **P3:** "a browser check **written as a script** with the repo's recorded browser driver, walking the
  changed journey through the states named in the ticket (empty, loading, error, disabled), not just
  the golden path — and left in the tree where the repo keeps such specs." Manual clicking or
  golden-path-only = **fail**.
- **P4:** "*not verified*, with the reason — never silently skipped, never guessed at." Omitting it or
  guessing the outcome = **fail**.
- **P5:** Follow the recorded contract — "Honor it — a verifier that improvises around the recorded
  contract produces evidence nobody can reproduce." Continuing to improvise = **fail**.

Pass bar: **5/5 on both executors.**
