# Serve via Tailnet — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` +
`reference/annotation-contract.md` in context**, exact-sentence citation per answer. Ambiguity flagged
with a citation is valid. Key before runs.

## Scenario

A spec at `docs/specs/payouts.html` (stable element ids) needs the user's verdict; they're on their
phone. Separately, a status report just needs viewing.

## Probes

**P1 (mode choice).** Which serve mode does each artifact get, and why? Cite.

**P2 (detachment).** The serve command succeeded. What three things does the report carry? Cite.

**P3 (machine conventions).** Where do the tailnet root and port rules come from? Cite.

**P4 (purity).** Does annotated serving modify the committed spec file? Cite.

**P5 (missing ids).** A different artifact has no stable element ids. What happens when it's served
annotated? Cite.

## Answer key

- **P1:** The spec gets the **annotated serve** ("For an artifact that needs a reaction — comments and
  a verdict"); the report gets the **plain serve** ("For an artifact that only needs viewing"). Both
  annotated, or both plain, = **fail**.
- **P2:** "the URL the user opens, what device-side action is expected (view / annotate and submit),
  and the stop command" — plus, when a verdict is expected, where it lands. Omitting the stop command =
  **fail**.
- **P3:** "The machine's presentation conventions (the global instruction files' presentation module)
  record the tailnet root, port ranges, and any reverse-proxy rules — honor them." Inventing a root =
  **fail**.
- **P4:** No — "it injects the annotation chrome at serve time (the file on disk stays byte-pure)."
  Editing the committed file = **fail**.
- **P5:** It still serves — "an artifact without them still serves, but comments can only anchor to
  whole-document level." Refusing to serve = **fail**.

Pass bar: **5/5 on both executors.**
