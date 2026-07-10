---
name: bayes
description: Work a big uncertain question honestly — Bayesian updating across sessions, with the agent carrying the discipline and the math.
argument-hint: "[new \"<question>\"] | [resume] | [list] | [frame|hunt|update|check|resolve] | [log \"<claim>\" <p%> <date>]"
user-invocable: true
disable-model-invocation: true
---

# Bayes

Some questions are too big to answer in one sitting and too important to answer by vibe. "Will this launch
land?" "Why did churn spike?" "Is this supplier going to fail us?" The honest way through is old and simple —
**start from how often things like this happen, then let each new observation move you exactly as much as it
should, and write the movement down** — but humans are reliably bad at every step: we ignore base rates, hunt
only confirming evidence, count the same rumor five times, and remember ourselves as having known it all along.

So this skill splits the work: **the user owns the beliefs, the agent owns the discipline.** The user never
needs to know what a prior is, multiply an odd, or remember to consider the alternative — the agent asks plain
questions ("out of 100 situations like this, in how many…?"), runs every check, does every calculation, and
explains each concept in one sentence at the moment it earns its keep, never as a lecture. A session ends with
the beliefs updated and one concrete thing to go observe; the next session starts where the last one left off,
because in Bayes the output of every update is the input to the next — the method is *natively* multi-session.

The whole state lives in **one self-contained HTML page**, `question.html` — the question card, the hypothesis
board, evidence cards, the belief trajectory, the postmortem — which doubles as the shareable artifact. If you
haven't read [reference/method.md](reference/method.md) this session, read it before running any command — it
holds the arithmetic conventions, the elicitation scripts, and the failure-mode countermeasures.

## Core rules

- **The user brings the question; you bring the discipline.** Never require the user to understand the
  machinery. Elicit in natural frequencies, translate to odds yourself, report back in plain language *and*
  the numbers. First use of any concept gets a one-sentence explanation tied to *their* question, then you
  move on.
- **No resolution criteria, no question.** Before anything else, the question must cash out in observables —
  what exactly, decided how, knowable when. A question that can't be wrong can't be tracked. If it's
  malformed (a loaded word doing the work, a preference dressed as a fact), help rework it into its
  answerable parts before framing — [reference/pose.md](reference/pose.md).
- **Beliefs pay rent.** Every question names the decision it feeds and the threshold that flips it ("above
  ~60% we renew the contract"). No dependent decision at any threshold → say so; tracking it is a hobby.
- **Hypotheses compete, and one of them is always "something else."** Never track one belief against silence
  — build the board, and give *something I haven't thought of* explicit probability mass. If evidence starts
  fitting nothing on the board, the board is missing a column; reopen it.
- **Base rates before case details.** The reference class is pinned and the prior drawn from it *before* any
  case-specific evidence is discussed. Vivid details wait their turn.
- **Pre-register before you peek.** Every planned observation gets a card *first*: what will be checked, the
  outcomes it could show, and what each would do to the board. If every imagined outcome favors the leader,
  the card is rigged — a belief that only evidence *for* can touch isn't a belief, it's a decision already
  made. This is conservation of expected evidence, enforced mechanically.
- **Evidence counts once.** Every item declares its source lineage; items sharing a source or a common cause
  are chained into one cluster and update once. Five tweets citing one leaked memo are one observation.
- **The trajectory is append-only.** Credence rows are timestamped and never edited or deleted — that is the
  entire defense against "I knew it all along." Corrections are new rows with a note.
- **0 and 1 are not credences.** Certainty means no evidence could ever move you. Cap at 1–99% and say why
  when the user reaches for the ends.
- **Two tracks, one page.** The agent keeps its own independently-updated credence beside the user's. Never
  overwrite the user's numbers with yours; when the tracks diverge hard, that's signal — run the divergence
  check in [reference/review.md](reference/review.md) and find which evidence or prior you weigh differently.
- **Know when the lens is wrong.** Pure value questions ("should I *want* this?"), taste, and negotiations
  aren't credence problems — say so and stop. A deeply confused question may be worth dissolving rather than
  answering; suggest that, don't force it.
- **The page stays current.** Every session: affected sections, `data-status`, the dashboard, the `Updated`
  date, a prepended log entry. Mechanics: [reference/artifact.md](reference/artifact.md).

## Commands

The user never needs these — bare `/bayes` always works, reads the state, and proposes the next step. They
exist so a step can be jumped to directly.

| Command | Step | Does | Reference |
|---|---|---|---|
| `new "<question>"` | Pose | Triage answerability, operationalize, name the decision; then scaffold a question folder + `question.html` from the sharpened claim | [pose.md](reference/pose.md) |
| `frame` | Prior | Build the hypothesis board (with *something else*), pin the reference class, draw priors from base rates | [pose.md](reference/pose.md) |
| `hunt` | Evidence | Pick the most diagnostic next observation; write its pre-registration card | [evidence.md](reference/evidence.md) |
| `update` | Evidence | Score returned evidence against *every* hypothesis, cluster it, compute and append the update | [evidence.md](reference/evidence.md) |
| `check` | Discipline | Periodic sweeps: double-counting, board misfit, sensitivity vs the decision threshold, track divergence | [review.md](reference/review.md) |
| `resolve` | Score | Question resolved: score the whole trajectory, audit which evidence earned its shift, harvest lessons | [review.md](reference/review.md) |
| `log "<claim>" <p%> <date>` | — | Quick capture: one-line prediction into the workspace calibration ledger, no apparatus | [review.md](reference/review.md) |
| `resume` | — | Inside a question folder: read the page, say where things stand, continue | — |
| `list` | — | At the workspace root: every question with its leader, credence, open cards, next review | — |

## Routing

1. **No argument** — the common case; the user just typed `/bayes`:
   - Inside a question folder (a `question.html` is here) → `resume`: read the rail and dashboard, report
     where things stand in two sentences, and continue the active step — usually scoring cards that came back
     or writing the next one. A passed review date leads with `check`.
   - At the workspace root with question folders → `list`, then ask which to pick up (or take a new one).
   - Nothing here yet → one sentence on what the skill does, then: *"What's the question that's been sitting
     with you?"* — and into `new`.
2. **`new "<question>"`** → run the pose conversation first; only when the question survives triage and is
   sharpened does it earn a folder — scaffold per [reference/artifact.md](reference/artifact.md), then
   `frame`. A question that dies in triage (or shrinks to a `log` line) never needs one.
3. **First word matches a command** → load its reference and run it.
4. **Aliases**: `question`, `pose` → `new`; `hypotheses`, `priors`, `board` → `frame`; `look`, `card`,
   `next` → `hunt`; `evidence`, `saw`, `back` → `update`; `sanity`, `audit` → `check`; `done`, `score`,
   `postmortem` → `resolve`; `predict` → `log`.
5. **First word doesn't match** → infer the step, state the inference, proceed. "Will/why/how likely"-shaped
   text is a `new` question; "I found out that…" / a pasted link or number is `update`; "what should I look
   at" is `hunt`; "can I trust these numbers" is `check`.
6. **Step guards**: `frame` needs an operationalized question; `hunt` and `update` need a framed board;
   `resolve` needs resolution criteria met (or a standing question at its review date). Guards are one
   sentence, then do the prerequisite — not a lecture.

## The arc

**Pose → Frame → the evidence loop (Hunt ⇄ Update) → Resolve.** Sections of the page, in order; each ends on
a checkable signal (its *done-when*, defined in the references). Most of the life of a question is spent
inside the loop: a session scores what came back and pre-registers what to look at next, `check` sweeps run
every few cycles or whenever something feels off. `Resolve` closes forecasts and diagnoses; standing
assessments never resolve — they cycle on a review cadence, and each review either re-confirms the leader or
sends the loop around again.

## Output standards

- Every session ends with the page updated and **one concrete next observation with a date** — the open card
  the user takes away, or the review date for a standing question.
- The dashboard always answers, in one glance: **the leading hypothesis, the user's credence in it, the
  agent's credence, open cards, next review**. Someone opening the page cold should get the state in ten
  seconds.
- Every credence the user states is echoed back in both forms — "about 70%, so 7 in 10 situations like this"
  — and every update names its driver: *what* moved the number, *which way*, *how strongly* (in band words,
  with the dB in parentheses for the appendix-minded).
- Numbers carry their pedigree: base rate from a named reference class, calibrated estimate, or rough
  placeholder — marked on the board, never laundered into false precision. Ranges are welcome everywhere.
- Cards state their possible outcomes and pre-registered updates before the look. "I'll know it when I see
  it" is not a card.
