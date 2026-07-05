# Check, Resolve & the ledger

The discipline sweeps that keep a long-running question honest (`check`), the closing move (`resolve`), and
the workspace-level calibration ledger that makes the user measurably better over time (`log` and scoring).

## Check (`check`)

Run every few update cycles, at any standing question's review date, or whenever either party feels the
numbers have drifted from the truth of the page. Four sweeps, each a conversation, not a report:

1. **Double-count sweep.** Walk the scored cards' lineages: do any "independent" items share a source, a
   pipeline, an incentive, a rumor chain? Merge late-discovered clusters and *recompute forward from the
   merge point* — as new appended rows with a note, never edits. The waterfall shrinking is the honest
   picture returning.
2. **Misfit / board sweep.** Is *something else* growing? Is any evidence sitting awkwardly under every
   column? Reopen hypothesis generation — silent drafting again, outsider framings welcome ("what would a
   competitor / an auditor / your bluntest friend say is going on?"). A new column inherits mass from
   *something else*, not from zero, and the trajectory notes its birth date.
3. **Sensitivity vs the decision.** The question exists to flip a decision at a threshold. Ask: does the
   decision change anywhere across the honest range of priors and the ranges carried on the evidence? If
   the answer is the same everywhere — **say so and stop gathering**; further evidence is entertainment,
   and the rent has been paid. If it flips inside the range, that gap is precisely what the next card
   should target.
4. **Divergence check.** When the two tracks part by more than ~15 points on the leader, run a mini
   double-crux: walk the trajectory to the row where the tracks split, and name the crux — the evidence
   weighed differently or the prior drawn from a different class. Each side states what observation would
   move *them* toward the other; that observation is usually the best next card. Neither track wins by
   authority — yours is a second opinion, not a grade.

*Done when:* each sweep has either passed or produced its correction (a merge, a new column, a stop, a
crux card) — recorded in the session log.

## Resolve (`resolve`)

For forecasts at their date, diagnoses at a validated hypothesis (or an exhausted board), and standing
questions being retired.

1. **Referee the criteria.** Resolve against the *written* resolution criteria, not the vibe of the
   outcome. Partial/ambiguous resolutions get called honestly (resolved-ambiguous is a real verdict; note
   what wording would have prevented it — that lesson feeds the next question).
2. **Score the trajectory.** Brier score each appended row of the user's track against the outcome
   (`(p−outcome)²`, lower is better), and the same for yours. Show the score's *shape* over time — early
   wrongness that corrected fast is good Bayes; late confidence that was wrong is the expensive kind.
3. **Audit the evidence.** Which cards earned their pre-registered shift? Which updates the postmortem now
   calls too big or too small? Which cluster, in hindsight, was one voice wearing three coats? Two or three
   sentences each — this is where the user's *next* question gets cheaper.
4. **Harvest.** Append to the workspace `calibration.md`: date, question, final credence before resolution,
   outcome, Brier, one-line lesson. Set the page's Resolution section, flip its status to `done`, final log
   entry. The page stays — resolved questions are the workspace's institutional memory.

**Hindsight guard:** the postmortem quotes only *recorded* rows. "I basically knew by March" is answered by
the March row, whatever it says.

## The calibration ledger (`log` and scoring)

The workspace root carries **`calibration.md`** — one table, append-only, shared by all questions:

| date | claim | p | by | resolved | outcome | Brier | source |
|---|---|---|---|---|---|---|---|

Two feeders:

- **`log "<claim>" <p%> <date>`** — the quick-capture side door. One line, no folder, no board: sharpen the
  claim to referee-able in one exchange, cap the ends, append. This is deliberate volume-building —
  calibration is trained on dozens of small predictions, not three big ones.
- **Resolved questions** — every `resolve` appends its row (source: the question's slug).

**Scoring session.** When ~20+ rows have resolved (check opportunistically at `list`/`resume`), offer the
calibration read: bucket by stated confidence, compare each bucket's hit rate, and deliver the one-line
diagnosis in plain terms — "your 80s land like 60s: when you feel 80, say 65 for a while." Update the
standing correction note at the top of `calibration.md`; from then on, when the user states a credence in a
skewed bucket, mention the correction *once* per session, gently, with the receipts one click away.
