# To-Spec — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` +
`reference/synthesis.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a
citation is valid. Key before runs.

## Scenario

A long design conversation settled a driver-payout direction. Retry policy was discussed but never
decided. The user is AFK. A live tracker is bound. You are running `to-spec payouts`.

## Probes

**P1 (no interview).** Retry policy is undecided. Ask the user, or something else? Cite.

**P2 (classification).** How must every Notes line be marked before sign-off, and what does an open
blocking Note mean? Cite.

**P3 (stale content).** The conversation named `src/payments/worker.ts` and a prototype-validated
reducer snippet. Which may appear in the spec? Cite.

**P4 (AFK sign-off).** How is approval sought, and what if that sibling isn't installed? Cite.

**P5 (on approval).** What two things happen when the spec is approved? Cite.

**P6 (vocabulary).** The draft says "split this into GitHub issues." Fix it and cite the rule.

## Answer key

- **P1:** Never ask — "Do not re-elicit requirements, do not re-ask what the discussion already
  settled, and do not stop and wait on the user"; the undecided item becomes a Notes line: "record it
  as a line in the spec's Notes." Asking = **fail**.
- **P2:** Each Notes line carries **blocking / delegated / deferred**; "An open **blocking** Note means
  the direction isn't ready to split into tickets — settle it first" (SKILL.md: "say so in the
  report"). Unclassified Notes at sign-off = **fail**.
- **P3:** Only the reducer — "The spec carries **no file paths and no code snippets**"; "The single
  exception: a **prototype-validated snippet** that encodes a decision more precisely than prose can."
  Including the path = **fail**.
- **P4:** "serve the spec annotated through the optional `serve-via-tailnet` sibling"; absent it,
  "fall back to inline approval or leave the committed spec for the user to read directly." Blocking on
  the missing sibling = **fail**.
- **P5:** Commit the spec, and create the **thin tracking ticket** — "carrying the title, a one-line
  gist, and a link to the canonical spec. The projection carries links and state, never content."
  Copying spec content into the ticket = **fail**.
- **P6:** "Split this into tickets" — "Never call the downstream unit an 'issue' — that's one tracker's
  word." Keeping "issues" = **fail**.

Pass bar: **6/6 on both executors.**
