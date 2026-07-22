# To-Spec — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` +
`reference/synthesis.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a
citation is valid. Key before runs.

## Scenario

A long design conversation settled a driver-payout direction. Retry policy was discussed but never
decided. The user is AFK. A live tracker is bound; no ticket exists for this direction yet. You are
running `to-spec payouts`.

## Probes

**P1 (no interview).** Retry policy is undecided. Ask the user, or something else? Cite.

**P2 (classification).** How must every Notes line be marked before sign-off, and what does an open
blocking Note mean? Cite.

**P3 (stale content).** The conversation named `src/payments/worker.ts` and a prototype-validated
reducer snippet. Which may appear in the spec? Cite.

**P4 (AFK sign-off).** How is approval sought while the user is AFK, and does to-spec apply a
readiness label on their LGTM? Cite.

**P5 (home & revision).** Where does the spec land, and what accompanies a later revision? Cite.

**P6 (vocabulary).** The draft says "split this into GitHub issues." Fix it and cite the rule.

**P7 (diagram first).** What is the first thing in the spec body, and in what form on this tracker?
Cite.

**P8 (too big).** The direction is clearly three builds' worth. Do you split it into tickets? Cite.

## Answer key

- **P1:** Never ask — "Do not re-elicit requirements, do not re-ask what the discussion already
  settled, and do not stop and wait on the user"; the undecided item becomes a Notes line: "record it
  as a line in the spec's Notes." Asking = **fail**.
- **P2:** Each Notes line carries **blocking / delegated / deferred**; "An open **blocking** Note means
  the direction isn't ready to build on — settle it first" (SKILL.md: "say so in the
  report"). Unclassified Notes at sign-off = **fail**.
- **P3:** Only the reducer — "The spec carries **no file paths and no code snippets**"; "The single
  exception: a **prototype-validated snippet** that encodes a decision more precisely than prose can."
  Including the path = **fail**.
- **P4:** The spec is already where feedback lands — "the spec already sits where the user's comments
  reach it; their LGTM on the ticket (or in the conversation) is the approval." And no label —
  "To-spec applies no readiness label." Serving via tailnet (that's the no-tracker fallback path), or
  stamping readiness on LGTM, = **fail**.
- **P5:** On the ticket — "**The ticket body is canonical** ... **create the ticket**" (no ticket
  exists here). Revisions: "Every revision rewrites the body in place and posts a **short comment
  noting what changed**." A repo doc while a tracker is bound, or revisions as new full-spec comments,
  = **fail**.
- **P6:** "Split this into tickets" — "Never call the downstream unit an 'issue' — that's one tracker's
  word." Keeping "issues" = **fail**.
- **P7:** A diagram — "Every spec **opens with a diagram** of the moving parts — before any prose";
  "On a tracker that renders it, a fenced `mermaid` block." Prose first, or no diagram without saying
  why, = **fail**.
- **P8:** No — "end the spec with a **Recommended split** section ... It is a proposal only —
  splitting is the user's call." Performing the split = **fail**.

Pass bar: **8/8 on both executors.**
