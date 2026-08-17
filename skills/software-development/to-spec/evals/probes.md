# To-Spec — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` + `reference/synthesis.md` + `reference/template-guide.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

A long design conversation settled a driver-payout direction. Retry policy was discussed but never decided. The user is AFK. A live tracker is bound; no ticket exists for this direction yet. You are running `to-spec payouts`.

## Probes

**P1 (no interview).** Retry policy is undecided. Ask the user, or something else? Cite.

**P2 (classification).** How must every Notes line be marked before sign-off, and what does an open blocking Note mean? Cite.

**P3 (stale content).** The conversation named `src/payments/worker.ts` and a prototype-validated reducer snippet. Which may appear in the spec? Cite.

**P4 (AFK sign-off).** How is approval sought while the user is AFK, and does to-spec apply a readiness label on their LGTM? Cite.

**P5 (home & revision).** Where does the spec land, and what accompanies a later revision? Cite.

**P6 (vocabulary).** The draft says "split this into GitHub issues." Fix it and cite the rule.

**P7 (diagram first).** What is the first thing in the spec body, and in what form? Cite.

**P8 (too big).** The direction is clearly three builds' worth. Do you split it into tickets? Cite.

**P9 (artifact sweep).** Shaping produced a research dossier committed in the repo and a prototype whose answer sits on the ticket thread with a parked branch `proto/payouts-ledger`. What does the spec carry for these, and in what form? Cite.

**P10 (nothing generated).** The direction was settled on conversation and existing docs alone — no dossiers, no prototypes. What does the spec's Supporting artifacts section contain? Cite.

**P11 (conversation-only evidence).** A latency question was settled by reasoning in the conversation; nothing durable was written. Does it get a Supporting artifacts entry, and does to-spec write a dossier for it? Cite.

**P12 (exception boundary).** Given the Supporting-artifacts pointer exception, the draft's Implementation decisions section cites `docs/research/payouts.md` and `src/payments/worker.ts`. Allowed? Cite.

## Answer key

- **P1:** Never ask — "Never stall on the user: a flagged open question is the correct output; a question bounced back is not"; the undecided item becomes a Notes line: "anything genuinely undecided becomes a line in the spec's **Notes**". Asking = **fail**.
- **P2:** Each Notes line carries **blocking / delegated / deferred**; "An open **blocking** Note means the direction isn't ready to build on — say so plainly when presenting for sign-off". Unclassified Notes at sign-off = **fail**.
- **P3:** Only the reducer — "The spec carries **no file paths and no code snippets**"; "a **prototype-validated snippet** that encodes a decision more precisely than prose can". Including the path = **fail**.
- **P4:** The spec is already where feedback lands — "the projection already sits where the user's comments reach it; their LGTM on the ticket (or in the conversation) is the approval, binding to the carried hash." And no label — "To-spec applies no readiness label". Seeking approval anywhere but where the spec already sits — serving it on a separate surface, or re-asking in another channel — or stamping readiness on LGTM, = **fail**.
- **P5:** On the artifact branch, projected onto the ticket — "**The artifact branch file is canonical**"; "**The ticket holds a projection** ... **create the ticket**" (no ticket exists here). Revisions: "Every revision is a commit on that branch"; "Each revision refreshes the projection (re-render, new hash) and posts a **short comment noting what changed**". A spec living only in the ticket body, or revisions as new full-spec comments, = **fail**.
- **P6:** "Split this into tickets" — synthesis.md's "Never call the downstream unit an "issue" — that's one tracker's word". Keeping "issues" = **fail**.
- **P7:** A diagram — "Every spec **opens with a diagram** of the moving parts — before any prose"; "rendered inline in the HTML (an SVG or equivalent that displays without a build step)". Prose first, or no diagram without saying why, = **fail**.
- **P8:** No — "end the spec with a **Recommended split** section ... It is a proposal only — splitting is the user's call". Performing the split = **fail**.
- **P9:** One **Supporting artifacts** entry per artifact — "the artifact kind, the question it answered, its one-line takeaway, and a durable pointer" — the pointer per its form: "the artifact-branch file plus its render URL where one exists, a tracker-resolvable URL, or a repo-relative path." Copying artifact content inline, or a summary without its pointer, = **fail**.
- **P10:** Nothing — the section is absent: "Omit the section when nothing was generated — the same convention as Assumptions". Manufacturing an empty or placeholder section = **fail**.
- **P11:** Yes an entry, no dossier — "stating the conclusion and marking plainly that no durable artifact exists"; "it never fabricates a dossier". Writing a dossier to fill the pointer slot, or dropping the conclusion entirely, = **fail**.
- **P12:** Not allowed — the exception is confined: "Outside Supporting artifacts and the one validated snippet, every section stays prose-only." The dossier path `docs/research/payouts.md` moves to a Supporting artifacts entry; the source path `src/payments/worker.ts` is no generated artifact, so its only remedy is prose. Keeping either path in Implementation decisions = **fail**.

Pass bar: **12/12 on both executors.**
