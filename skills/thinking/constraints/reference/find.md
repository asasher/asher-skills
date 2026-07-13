# find — hunt the constraint and validate it

You are identifying the constraint (Focusing Step 1). The deliverable is the **Find** section: a suspects board
the user watched narrow, and a verdict block naming **one** constraint with a type and a confidence mark. The
hunt is visual and collaborative — the user should see suspects appear, gather evidence, and get eliminated on
the page, not receive a pronouncement.

Prerequisite: a Goal and Map (run [map.md](map.md) first if empty).

## 1 — the first fork: internal or market?

Run both doubling tests and record the answers verbatim in the Find section:

- **Capacity test:** "If your delivery capacity doubled next month, would [throughput unit] actually rise?"
  *No* → demand doesn't absorb more: the constraint is the **market** (offer, positioning, conversion, trust,
  channel) and internal optimization is the classic wrong move — steer the rest of the hunt into the demand
  funnel (it has stages and queues too; map them the same way).
- **Demand test:** "If qualified demand doubled next month, could you fulfill it profitably without breaking
  quality?" *No* → an internal constraint is binding; keep hunting inside.

Yes to both is common early in a hunt — it usually means the answers are opinions. Ask for the episode: "when
did you last turn work away / last starve for work?"

## 2 — build the suspects board

From the map's scan table, nominate 2–4 suspects. Each gets a row: **suspect · type (physical / policy /
paradigm / market / attention) · evidence for · evidence against · mark**. Everything starts `suspected`.

Sharpening questions, in rough order of power:

- "If you could magically double one thing for a month, what would raise [throughput unit] most?" — and then:
  "if that doubled, what would become the *next* limit?" (a crisp answer to the follow-up is strong evidence
  they've actually located the constraint).
- "Where does work wait longest?" — the biggest, oldest queue on the map sits directly *in front of* the
  constraint.
- "Who is mentioned in the most blocked-item explanations?"
- "What does everyone have a workaround for?"
- For each capacity suspect: "what rule makes that capacity unavailable?" — policy constraints masquerade as
  capacity constraints, and a rule change is cheaper than a hire.
- Solo systems: "what do you already know you should do but aren't doing?" and "what has the highest payoff but
  gets your *worst* attention?" — attention, decision backlog, and courage-to-publish are the usual suspects,
  not calendar time.

Keep the board honest: evidence *against* is as valuable as evidence for. When two suspects survive, ask which
one the other waits on — constraints are upstream of their symptoms ("QA is slow" often traces to large
ambiguous batches arriving from upstream; the loudest pain is frequently a symptom, not the limiter).

**Escalate to `dig`** ([trees.md](trees.md)) when symptoms are scattered across the system with no visible
shared cause, when the top suspect is a policy or belief, or when stakeholders disagree strongly about what's
wrong — that's a Current Reality Tree / three-cloud job, and its output lands back on this board.

## 3 — verdict

Name **one** constraint. Write the verdict block:

> The current constraint appears to be **[resource / step / policy / market / attention]** (*type*), because
> [evidence: queue, wait, starvation, expedite, capacity-vs-demand], which limits **[throughput unit]**.
> Mark: [suspected|evidenced]. It would reach *validated* if [specific observable].

Then update the flow map — the constraint node goes `:::constraint` (red) — and the dashboard (`d-constraint`,
`d-type`, `d-conf`). The page should now answer "what's the constraint?" in ten seconds flat.

Marking rules ([framework.md](framework.md)): `evidenced` needs at least one observable (queue count, wait
time, aging report, calendar load, concrete recent episodes); `validated` needs a moved *system* metric or a
doubling counterfactual that survives scrutiny — usually that means the first exploit experiment, so don't
stall here. **An `evidenced` constraint with an experiment beats a `validated` one without.** Say explicitly:
"we're treating this as our best hypothesis — the first experiment is also the test of the diagnosis."

Refuse to name a person. If every path leads to one human, the constraint is the *dependency* — "all deploy
knowledge lives in one head", "every discount needs the founder" — and the page says so in those words.

*Done when:* the verdict block is filled, the map shows one red node (or a red funnel stage for a market
constraint), and the user agrees this is the best current hypothesis. Set Find to `done`, Plan to `active`,
and offer to continue into [act.md](act.md).
