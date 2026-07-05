# act — plan the squeeze, then make it falsifiable (plan · experiment)

Focusing Steps 2–4 as working sessions. `plan` fills the **Plan** section; `experiment` fills **Experiments**.
Prerequisite: a named constraint in the verdict block.

## plan — exploit, subordinate, and the elevate gate

Order is doctrine: **exploit → subordinate → (only then) elevate.** Free capacity is almost always hiding in
misuse, and money spent before exploiting buys the same throughput a rule change would have.

### Exploit — more from the constraint, spending nothing

Walk the checklist against *this* constraint with the user; record keepers as an unchecked task list in Plan:

- **Never starved:** does the constraint ever idle waiting for input, decisions, access, materials? Why?
- **Never poisoned:** does defective, ambiguous, or premature work consume its time? Put the quality/readiness
  check *in front of* it (definition-of-ready, pre-review lint, qualified-lead criteria).
- **Only constraint-work:** what does it do that something/someone else could? Offload prep, admin, formatting,
  status reporting, routine approvals.
- **Best work first:** are its priorities explicit and visible, or does the loudest voice win? Give it one
  queue, sequenced by throughput value.
- **Interruptions:** what fragments it? Batch the requests, protect the focus block, route around it.
- **Measure lost minutes by cause:** starved · blocked · rework · waiting-decision · interrupted — a week of
  tallying is often the cheapest possible diagnostic and doubles as experiment baseline.

Per constraint type: **policy** — exploit means a reversible rule change (raise the approval threshold, delegate
the decision, shrink the batch). **Market** — exploit means more from *existing* demand: follow up every warm
lead, sharpen the offer and proof, fix the drop-off stage before buying new traffic. **Attention** (solo) —
WIP of 1–3, the best cognitive block goes to the constraint task, "done" defined externally, recovery protected
(exhausted attention can't be exploited by adding hours).

### Subordinate — the rest of the system serves the constraint

The counterintuitive half; warn the user it will *feel* wrong. Write 2–4 explicit policy sentences into Plan:

- A **release rule** (the rope): start new work only at the pace the constraint absorbs — cap WIP in front
  of it.
- A **priority rule**: constraint work beats local utilization; non-constraints may idle, help, prep, or
  quality-check rather than produce queue.
- A **buffer**: a small stock of ready work so variation never starves the constraint — with buffer state
  (green/amber/red) as the expedite signal, not stakeholder volume.
- A **metric change**: stop rewarding whatever local efficiency currently manufactures the pile-up.

If a subordination rule triggers real resistance ("but the team can't just sit idle!"), that's a conflict —
run `cloud` ([trees.md](trees.md)) on it rather than winning the argument.

### Elevate — behind the gate

List elevation options (hire, tool, automation, outsource, redesign, demand generation) in the gated table,
each with cost class and the throughput-accounting test: *ΔThroughput vs ΔInvestment + ΔOperatingExpense*. The
gate condition is written above the table: **elevation is considered when exploit + subordinate experiments
have run and the constraint still binds.** When the user arrives asking "should we hire?", this is where the
question waits while the free moves get tried.

*Done when:* at least one exploit move and one subordination rule are adopted, and elevate options (if any)
sit behind the gate. Set Plan to `done`, Experiments to `active`, and go straight into `experiment` — a plan
without a card is a wish.

## experiment — make it falsifiable

Every adopted move becomes an `.xp` card (markup in [artifact.md](artifact.md)) in the canonical form:

> If we **[change]** at **[constraint]**, because **[mechanism]**, then **[metric]** moves **[amount/direction]**
> by **[date]**, while **[guardrail]** holds.

Card discipline:

- **One change per card.** Two changes at once can't be scored.
- **Baseline before start.** No baseline → the card's first task is a week of measurement (the lost-minutes
  tally usually serves).
- **Metrics that count:** the throughput unit first; then lead time, WIP/queue-age at the constraint,
  constraint lost-time by cause. Guardrails from the Goal section's necessary conditions (quality floor,
  OE, morale). Watch the known traps: utilization up + throughput flat = feeding the wrong work; WIP up +
  throughput flat = subordination failing.
- **Prediction with a number and a date.** Wrong-but-specific beats vague — a missed prediction teaches;
  "try it and see" doesn't. Review cadence: ~daily for ops-tempo systems, weekly for teams and solo work,
  per-campaign for market constraints.
- **Decision rule pre-committed:** what result means adopt · adapt · abandon · elevate · re-identify.
- **Expected next constraint:** one line — "if this works, the pile-up should move to […]" — which is both the
  success signature and next cycle's head start.

Cap concurrent running cards at 2–3; more than that and the system can't attribute results — the experiment
queue is itself WIP in front of a constraint.

*Done when:* at least one card is `running` with baseline, prediction, review date — and the dashboard
`d-review` shows the nearest review. End the session by telling the user exactly what to measure and when
you'll score it together: that date is the default trigger for [review.md](review.md).
