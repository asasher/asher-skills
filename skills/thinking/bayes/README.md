# Bayes

A stateful, user-guided Bayesian facilitation for one complicated question at a time: check it's answerable
(rework it if it isn't), build a board of competing hypotheses with *something else* always on it, draw
priors from base rates in "out of 100 cases" language, pre-register every look before anyone peeks, score
returned evidence against every hypothesis, and keep an append-only trajectory of every update — across as
many sessions as the evidence takes. The user owns the beliefs; the agent owns the discipline and all of the
math. The whole state is one self-contained, visual `question.html` per question, plus a workspace-level
`calibration.md` ledger that accumulates resolved predictions into an actual calibration read.

## Shape

- **Pose → Frame → (Hunt ⇄ Update) → Resolve** — five page sections with done-when signals; most of a
  question's life is the evidence loop, and `check` sweeps (double-counting, board misfit, sensitivity,
  track divergence) run every few cycles.
- The page is the state (the `dissolve` pattern): `data-status` per section, a dashboard that answers
  "where does this stand?" in one glance, FILL-marker regions, a session log — with one hard novelty: the
  **trajectory and waterfall are append-only**, the structural defense against hindsight bias.
- Two credence tracks — the user's and the agent's, independently updated; divergence triggers a mini
  double-crux rather than a winner.
- Guidance-first: bare `/bayes` reads the state and proposes the next step; the user never needs a
  subcommand or a definition of "prior."

## Sources

Synthesized from: the LessWrong Bayes corpus (Yudkowsky's *Intuitive Explanation of Bayes's Theorem*, the
Arbital Bayes guide lineage, *A Visual Explanation of Bayesian Updating* — posterior-becomes-prior as the
session loop); Jaynes's odds/decibel formulation and *0 and 1 Are Not Probabilities*; Gigerenzer & Hoffrage
on natural frequencies as the elicitation format; Heuer's *Psychology of Intelligence Analysis* and Analysis
of Competing Hypotheses (the matrix, diagnosticity, working across the row); Tetlock & Gardner's
*Superforecasting* (outside view first, small frequent updates, keeping score); the Sequences' Bayesian
disciplines (conservation of expected evidence → pre-registration cards, making beliefs pay rent → the
"rent" field, privileging the hypothesis → silent generation, motivated stopping → stopping rules on cards);
prediction-platform question hygiene (Metaculus-style resolution criteria, PredictionBook/Fatebook-style
calibration ledgers, Brier scoring); and the bias literature's countermeasures (base-rate gate, evidence
lineage/clustering, append-only records against hindsight). Research notes from the design session are
summarized in the reference files.

## Companions

Suggestions, not dependencies: a question that keeps circling a loaded word may want `dissolve` rather than
an answer; a belief that resolves into "place many cheap wagers" territory rhymes with `smallbets`; a
question about where a *system* is stuck is `constraints`' hunt, with this skill as the honest bookkeeper
for any single contested hypothesis inside it.
