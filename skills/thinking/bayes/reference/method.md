# The method

The synthesized theory behind every command: how beliefs are represented, how numbers are elicited from a
user who owes you no math, how updates are computed, and the failure modes each piece of machinery exists to
defeat. Read once per session before running any command.

## Representation: the board is a probability vector

A question carries 2–5 named hypotheses plus **something else**, with credences in whole percent summing
to 100. Two tracks: the **user's** (theirs alone — never overwrite it) and the **agent's** (yours, updated
independently from the same evidence). Forecast questions ("will X by date") may collapse to two hypotheses
(happens / doesn't) — the machinery is identical.

Internally you think in odds, because odds make updating honest: *posterior odds = prior odds × likelihood
ratio*, and in log form evidence simply **adds**. Measure evidence strength in decibels,
`dB = 10·log₁₀(LR)`. Never show this machinery unprompted; translate at the boundary.

## The strength bands

All evidence talk with the user happens in band words; dB and LR live in parentheses and in the page's fine
print.

| Band | LR (approx) | dB | Plain reading |
|---|---|---|---|
| whisper | ~1.5–2× | ~2–3 | "slightly more what you'd expect if H than if not" |
| clear | ~3× | ~5 | "noticeably better explained by H" |
| strong | ~10× | ~10 | "hard to explain unless H" |
| decisive | ~100× | ~20 | "you basically don't see this unless H" |

Anchors for credence talk: 50% is a coin flip; 67% is 2:1; 90% is 9:1 — "you'd be genuinely surprised
otherwise"; 99% is the honest ceiling. **0 and 1 are not credences** — they are infinite log-odds, positions
no evidence can move, and the page refuses them.

## Elicitation: natural frequencies, always

People fail at probabilities and succeed at counts (Gigerenzer). Every number is elicited as a count of
imagined cases, never as an abstract percent:

- **Priors** — "Think of 100 situations that looked like this one at this point. In how many does ⟨H⟩ turn
  out to be the story?" Pin the reference class *first* and out loud ("similar launches by teams this size,"
  "vendors who've already slipped twice") — the base-rate gate: no case-specific details may be discussed
  until the prior is drawn from the class.
- **Likelihoods** — for a piece of evidence E against each live hypothesis: "In 100 worlds where ⟨H₁⟩ is
  true, how many show ⟨E⟩? And in 100 worlds where ⟨H₂⟩ is true?" Accept coarse answers — 5, 20, 50, 80,
  95 — precision beyond that is theater.
- **Ranges are first-class.** " 10 to 25 out of 100" is more honest than "17." Carry the range; compute on
  the midpoint; note when the *decision* would differ across the range (that's the sensitivity check).

## The update step (you do this; the user never does)

For evidence E with elicited expectedness e_h ("out of 100 worlds where h, how many show E") for each
hypothesis h:

1. posterior_h ∝ prior_h × e_h, renormalize to 100, round to whole percent, floor live hypotheses at 1%.
2. Report the movement in plain language: which hypotheses rose, which fell, by how much.
3. For the waterfall, log the leader's shift in dB: `10·log₁₀(odds_after / odds_before)` of the leading
   hypothesis against the field.
4. Run both tracks: the user's update from *their* elicited numbers, yours from yours. Show both.
5. Append the row to the trajectory — never edit an old one.

The user may veto or hand-adjust their own posterior ("that feels too far"). Record the adjusted number *and*
a one-line note of the veto — a felt override is data about either the elicitation or the user.

## Diagnosticity (the ACH discipline)

From Heuer's Analysis of Competing Hypotheses: evidence is only as valuable as its ability to **separate**
hypotheses. Every evidence item is scored against *every* column of the board, not just the favorite —
working *across the row*. Evidence consistent with everything is worthless however vivid it is; the matrix
makes that visible. Choosing the next observation (`hunt`) is a search for the cheapest row that would
most separate the current leaders — expected movement per unit effort, not "more support for the leader."
Prefer looks that could *disconfirm* the leader: ruling out is more constraining than piling on.

## Conservation of expected evidence (why cards come first)

You cannot expect evidence to confirm you: if seeing E would raise credence in H, then seeing not-E must
lower it, in exact proportion. The pre-registration card operationalizes this — every card lists the
outcomes the look could return and the pre-committed update for each. **The rigged-card test:** if every
listed outcome moves the board the same direction, the card is invalid; either find the outcome that would
move it the other way, or admit this look is not evidence-gathering but decoration.

## Failure modes → built-in countermeasures

Each mechanism in this skill exists because a documented bias defeats willpower. Don't skip the mechanism
because the user seems sharp — the biases are load-bearing in everyone.

| Failure | What it does | The countermeasure (built in) |
|---|---|---|
| Base rate neglect | vivid case detail swamps prevalence | base-rate gate: reference class and prior before any details |
| Confirmation bias | search and reading skew toward the favorite | ACH row-scoring; every `hunt` includes one look that could cut the leader |
| Motivated stopping | search ends when the wanted answer leads | stopping rule pre-committed on the card: what's enough, decided before looking |
| Anchoring on hypothesis #1 | first story becomes the frame | silent generation: draft your hypothesis list *before* showing the user's prompt for theirs; merge after |
| Double counting | correlated echoes multiplied as independent | lineage on every item; clusters update once |
| Hindsight bias | priors quietly rewritten after the fact | append-only trajectory; postmortems compare against recorded rows only |
| Hypothesis blindness | truth isn't on the board; math renormalizes over a false set | *something else* holds explicit mass; misfit trigger — evidence unlikely under every column reopens the board |
| Pseudo-quantification | vibes laundered into decimals | bands not decimals, ranges not points, pedigree labels on every number, sensitivity checks vs the decision threshold |

## Question types

| Type | Resolves | Scoring |
|---|---|---|
| **Forecast** — "will X by ⟨date⟩" | by calendar, against written criteria | Brier over the whole trajectory |
| **Diagnosis** — "why did X happen" | by investigation: one hypothesis validated or the board exhausted | evidence audit; Brier if ground truth emerges |
| **Standing** — "is this ⟨vendor/hire/strategy⟩ sound" | never fully; reviewed on a cadence | each review re-confirms or reopens; scored on decision quality |

Type is chosen at `pose` and shapes the resolution criteria, not the machinery.

## Teaching style

One sentence, at the moment of first use, in terms of *their* question — then move on. Examples of the
register:

- *Prior:* "Before we look at anything specific to Acme, we start from how often vendors in this position
  deliver at all — that starting number is called a prior."
- *Likelihood ratio:* "What matters isn't whether a missed milestone is bad news — it's how much *more*
  often you'd see it from a failing vendor than a healthy one. That ratio is the whole game."
- *Diagnostic:* "This check is worth doing because the two stories predict different results. Anything both
  stories predict equally can't teach us anything."
- *Posterior→prior:* "Today's ending number is next session's starting number — that's the whole trick of
  doing this over multiple sittings."

Never stack two explanations. Never say "Bayes' theorem states." If the user asks for the math, give it
gladly and fully — the appendix mode is for when *they* open the door.
