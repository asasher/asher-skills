# Claude executor — build P9 (ledger honesty)

Context: in-session Claude subagent, only `skills/software-development/build/SKILL.md` in context, per `docs/agents/probe-evals.md`. Probe run 2026-08-02. Reported usage: 23,886 tokens.

## Probe

The verify pass's dispatch return carried no usage report, and the harness exposes no usage surface covering it. What do you record for that pass, and where does the ledger end up? Cite.

## Executor answer (verbatim)

I read the SKILL.md; the answer is directly settled by "The stage ledger" section — no ambiguity.

**Concrete next action:** In the per-stage token ledger this session is keeping, I record a row for that verify pass with its tokens marked `unreported` (stage: verify pass; quota column also absent, since the harness exposes no covering surface). I do not estimate the number and I do not drop the row. The pipeline then continues with step 2's fix loop for the two failing claims; the finished ledger is handed to the `prove-your-work` dispatch at step 5, whose evidence package lands as a comment on the change request — that is where the ledger ends up.

**Citations (verbatim, from § The stage ledger):**

Why the value is `unreported` rather than an estimate or an omitted row:

> "A number no surface reported is recorded as `unreported` — an estimate is not accounting, and a dropped row hides exactly the cost spike the ledger exists to show."

Why no other source can supply the number in this scenario (the dispatch return carried no usage report, and the harness has no covering surface):

> "A dispatched stage's tokens come from its dispatch return's usage report; work this session does itself is covered by the harness's own usage surface where it has one."

Why a row still exists for this specific pass (each verify pass is its own row, recorded as it lands):

> "As each stage lands, record its row: the stage (implement, each verify pass, each fix pass, each review pass, evidence), the tokens it consumed, and the harness quota percentage at that point where the harness exposes one."

Where the ledger goes:

> "The finished ledger goes to step 5 with the evidence dispatch."

and, from § 5. Evidence, where it finally lands:

> "Dispatch the `prove-your-work` skill against the change request, handing over the stage ledger: the evidence package lands as a change request comment for whoever decides the merge."

**Ambiguity check:** none on the probed point — the `unreported` sentence covers exactly this case (no usage report, no harness surface), and the destination is stated twice consistently. One minor note, not an ambiguity affecting the action: the ledger row also asks for "the harness quota percentage at that point where the harness exposes one" — the "where the harness exposes one" qualifier makes that field conditionally absent by design, so no quota entry is recorded here either.

## Verdict

**Pass** — `unreported` row kept, no estimate, ledger handed to step 5's evidence dispatch; both key citations quoted exactly.
