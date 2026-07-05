# The Constraints Framework

The Theory of Constraints synthesis underneath every command. Read this before running any command for the first time in a session.

## The premise

A system's performance against its goal is limited by one active constraint — or a very small number — at any moment. Improving anything else feels productive but doesn't move the goal. Goldratt's one-word summary of ToC: **focus**. The constraint is not the biggest problem or the loudest complaint; it is the current limiting factor. That reframe is the whole skill: the constraint is a *leverage point*, not merely a pain.

Three questions structure all the work (Goldratt's thinking-process spine):

1. **What to change?** — find the constraint (`map`, `find`, `dig`).
2. **What to change to?** — design the exploit/subordinate plan and injections (`plan`, `cloud`).
3. **How to cause the change?** — experiments with predictions and review dates (`experiment`, `review`).

## The Five Focusing Steps

1. **Identify** the constraint. Operational test: *if this one thing had a little more usable capacity or less waiting, would the whole system produce more goal-units now?*
2. **Exploit** it — get the most from what already exists, spending nothing: never starve it, never feed it defective or low-value work, quality-check before it, offload what doesn't truly need it, kill its interruptions.
3. **Subordinate** everything else — release work at the constraint's pace, cap WIP in front of it, let non-constraints idle rather than pile up queues, change priorities and metrics to protect it.
4. **Elevate** — only after exploit and subordinate are visibly exhausted: hire, buy, automate, redesign, or (for a market constraint) grow demand. Test any elevation with throughput accounting: does throughput rise enough to justify the added investment and operating expense?
5. **Repeat** — the constraint moves. Go back to step 1, and *don't let inertia become the constraint*: rules, buffers, and metrics built for yesterday's constraint are prime suspects for today's.

The two mistakes that dominate practice: **jumping to elevate** (buying/hiring before exploiting — exploit and subordinate usually expose hidden capacity for free) and **inertia at step 5** (still optimizing the old constraint after it moved).

## Constraint types

| Type | What it looks like | Note |
|---|---|---|
| **Physical / capacity** | A machine, role, specialist, test environment, cash, calendar capacity | The classic case, rarer than assumed |
| **Policy** | A rule, approval path, batch size, metric, incentive, "how we do things" | The most common in practice — and invisible because long-established |
| **Paradigm / belief** | The assumption under the policy: "everyone must be fully utilized", "senior approval reduces risk" | Break the belief and the policy falls |
| **Market / demand** | The system can deliver more than customers currently buy | Exploit means offer, positioning, conversion, trust — not more production |
| **Time / attention** | The scarce cognition of a founder, reviewer, manager, or the user themself | The default suspect in solo knowledge work |

**Internal vs external is the first fork.** Two doubling tests decide it:

- *If delivery capacity doubled next month, would revenue/throughput rise?* Yes → internal constraint.
- *If qualified demand doubled next month, could you fulfill profitably?* No → internal constraint is already binding; Yes → the market is the constraint.

When someone says "we need more people," suspect a policy constraint masquerading as capacity: *what rule makes the existing capacity unavailable?*

## Evidence beats opinion

Every constraint claim carries a confidence mark:

- **suspected** — named in conversation, no observable backing yet
- **evidenced** — backed by queue counts, wait times, aging work, expedite frequency, calendar load, or concrete recent episodes
- **validated** — an exploit-level intervention at it moved a *system* metric (throughput, lead time), or the doubling counterfactual survives scrutiny

The evidence hierarchy, strongest first: timestamp/flow data → WIP counts and work-item age → calendar/interrupt logs → recent concrete examples → interview consensus → strong feelings without examples. Consensus tells you where to look; it never justifies elevation spending.

Convert opinions to observables before recording them: "review is slow" → median and 85th-percentile review time, count of items older than SLA. "The founder is the bottleneck" → items waiting on founder, decisions only the founder may make.

## Signature symptoms of a constraint

Work **waits** in front of it (biggest queue, oldest items). Downstream is **starved**. **Expediting** clusters around it. Everyone has a **workaround** for it. It gets the heroics, the status meetings, the exceptions. Upstream over-produces because it can't flow through. The pace of the whole system tracks its pace.

## Throughput accounting (the decision lens)

Three measures: **Throughput** (goal-units delivered per time; in business, sales minus truly variable cost), **Investment/Inventory** (money and effort locked in the system, including unfinished work), **Operating Expense** (what it costs to run). Judge every intervention by: does T rise, does I fall, does OE fall — in that priority order.

Corollaries worth quoting:

- *An hour lost at the bottleneck is an hour lost for the entire system. An hour saved at a non-bottleneck is a mirage.*
- Local efficiency is the enemy: a non-constraint at 100% utilization mostly manufactures WIP, lead time, and expediting.
- Don't balance capacity; balance flow. Idle time away from the constraint can be the price of flow.
- A non-constraint's proper utilization is set by the constraint, not by its own potential.

## Drum-Buffer-Rope (the operating pattern for `plan`)

The constraint is the **drum** — it sets the pace. Protect it with a **buffer** of ready work so variation never starves it. The **rope** releases new work into the system only at the pace the constraint absorbs it. Buffer state is the priority signal: green = normal, amber = watch, red = expedite *and investigate why*. Buffers always full → releasing too early; buffers repeatedly pierced → capacity, quality, or release timing is wrong.

## When ToC is the wrong lens

Say so and stop rather than force it:

- The **goal is contested** — facilitate goal agreement first; without a goal there is no constraint.
- The work is **exploratory with no repeatable flow** (research, early product discovery, unknown product-market fit) — use discovery/small-bets framing instead.
- The issue is **safety, ethics, compliance, trust, or governance legitimacy** — those are hard conditions, not optimization variables.
- Many **independent value streams** with no shared throughput measure — split into systems first; each may have its own constraint.
- A solvable **formal optimization** exists and precision matters (stable product-mix/scheduling) — ToC heuristics can lose to the math.

And the standing hedges: treat "the constraint is X" as a hypothesis with a confidence mark, timebox the diagnosis (don't let analysis become the constraint), prefer reversible experiments to reorgs, and re-identify on a cadence.

## The workspace

The skill is installed at a **constraints workspace** root. Each system under study is its own folder — kebab-case slug of the system name — holding `constraint.html` (state + artifact, see [artifact.md](artifact.md)) and `sources/` (evidence files: exports, screenshots, logs). Folders are siblings; a system is self-contained, shareable, and deletable on its own.

`constraint.html` is the single source of truth. Its six sections mirror the arc — **Goal → Map → Find → Plan → Experiments → Loop** — and each carries a `data-status`. The Loop section holds the constraint history: one entry per broken/moved constraint, because step 5 is the operating loop, not a postscript.

## Sources

Goldratt & Cox, *The Goal*; Goldratt, *It's Not Luck* and *Critical Chain*; Cox & Schleier (eds.), *Theory of Constraints Handbook*; Dettmer, *The Logical Thinking Process*; Scheinkopf, *Thinking for a Change*; TOCICO Body of Knowledge and Dictionary; TOC Institute (five focusing steps, goal, constraint definitions); LeanProduction/Vorne ToC guide; Kim, Behr & Spafford, *The Phoenix Project* and the Three Ways; Anderson's kanban lineage and Kanban University's STATIK; Tendon's TameFlow (constraints in knowledge work, management attention as constraint); Clarke Ching, *The Bottleneck Rules*; Deming PDSA / Rother's Improvement Kata / Lean A3 (experiment discipline); Weisbord's six-box model (organizational overlay). Full research notes: `constraints-research/` in the skills repo.
