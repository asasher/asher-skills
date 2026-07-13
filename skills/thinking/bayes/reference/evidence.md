# The evidence loop

Where a question spends most of its life: **hunt** (pre-register the next look) ⇄ **update** (score what
came back). A typical session does both — score the cards the user returned with, then write the card they
leave with. Never the reverse order: returned evidence is scored *before* new looks are planned, so the plan
reflects the updated board.

## Hunt — choose the look, write the card

### Choosing what to look at

Scan the board and ask: **which cheap observation would most separate the current leaders?** Not "what
would support the leader" — what would *split* the top hypotheses, or best threaten the leader. Offer 2–3
candidate looks with your read on their diagnostic value; the user picks by what they can actually get
(access, cost, time). Rough guide: expected movement per unit effort. A look both leaders predict equally
is decoration, however easy — say so and strike it.

Every few cycles, make one hunt a deliberate **disconfirmation round**: "what's the cheapest observation
that would cut your confidence in ⟨leader⟩ in half?" If neither of you can name one, treat that as an alarm
— unfalsifiable leads are how motivated reasoning wins.

### The card

One `.ev` card per planned look, `data-state="open"`:

- **Look** — what will be checked, where, by when (the card carries a date; it's the session's takeaway).
- **Outcomes** — the 2–4 results the look could realistically return, *including the boring one*.
- **Pre-registered updates** — for each outcome, direction and band per affected hypothesis ("supplier
  answers within a day → whisper toward *healthy*; dodges the question → clear toward *failing*").
- **Stopping rule** — what makes this line of investigation *enough* ("two more clean milestones and we
  stop auditing them"), written before results exist, applied symmetrically to wanted and unwanted answers.

**Rigged-card test before saving:** if every outcome updates the same direction, the card is invalid —
find the outcome that moves the other way or admit the look isn't evidence. This is conservation of
expected evidence doing its job; explain it in one sentence the first time it fires.

*Done when:* at least one open card exists with outcomes, pre-registered updates, a stopping rule, and a
date — and the user knows which card they're taking away.

## Update — score what came back

### 1. Attach or admit

Match the returned evidence to its open card. Evidence that arrives *without* a card (the world volunteers
things) is welcome but flagged `unplanned` — elicit its likelihoods fresh, and be twice as suspicious of
strength inflation, because nobody pre-committed.

### 2. Lineage and clustering

Before any scoring: **where does this come from, and does anything already on the page share that source or
a common cause?** Same memo quoted five places, three dashboards fed by one pipeline, two colleagues who
heard it from the same meeting — chain them into one cluster. A cluster updates **once**, at the strength
of its best member. Record the lineage on the card; the waterfall renders clusters as single bars so the
picture can't overstate independence.

### 3. Score across the whole board

The ACH move: for *every* live hypothesis, elicit "in 100 worlds where ⟨H⟩ is true, how many show this
result?" — coarse answers (5/20/50/80/95), ranges fine. Evidence roughly equally expected everywhere is
marked **non-diagnostic** on its card and moves nothing; that verdict is worth showing, it teaches the user
what evidence is for.

### 4. Compute, show, append

Run the update step from method.md on both tracks. Report in plain language first ("this moves you from
about 55 to about 70 — a clear push toward *failing*"), numbers second. The user may veto their own
posterior; record the override with its one-line reason. Then:

- **Append** the trajectory row (date, driver, both tracks, dB shift of the leader). Never edit old rows.
- **Re-render** the board bars, the waterfall, the dashboard tiles.
- **Close the card** — `data-state="scored"`, with the outcome that actually happened and whether the
  pre-registered update held. If the user wants to update *more* than the card pre-committed, the excess
  needs a stated reason on the card — "it felt bigger in person" is exactly the drift pre-registration
  exists to catch. If evidence contradicted its stopping rule ("one more look, the last one was a fluke"),
  name the motivated-continuation pattern gently and hold the rule unless the user overrules on the record.

### 5. Misfit check

After scoring: was this evidence unlikely under *every* named hypothesis? Then it votes for **something
else** — raise it and say so. Two such votes in a row trigger the board-reopen conversation (`check` in
review.md, run inline).

*Done when:* every returned item is scored or clustered, the trajectory has its rows, no card is left
half-scored, and a fresh open card (or the resolve step, if criteria are met) ends the session.
