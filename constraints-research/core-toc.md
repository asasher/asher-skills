# Theory of Constraints: Practitioner Reference

TOC’s operating premise: a system’s performance against its goal is limited by one active constraint or a very small number of constraints. Improving anything else may feel productive, but it will not materially improve system throughput. Goldratt’s one-word summary was “FOCUS.” ([tocinstitute.org](https://www.tocinstitute.org/five-focusing-steps.html))

## 0. Start With The Goal

Before finding the constraint, define the system and its goal.

- Business: make more money now and in the future, while satisfying necessary conditions like customers, employees, legality, quality, safety.
- Product/team: deliver validated customer value faster, more predictably, or with higher quality.
- Personal workflow: complete the few outcomes that matter, without burning down necessary conditions like health or relationships.

A constraint only exists relative to a goal. If the goal is vague, every annoyance looks like a constraint. TOC Institute emphasizes that “without a Goal there can be no constraint.” ([tocinstitute.org](https://www.tocinstitute.org/what-is-the-goal.html))

## 1. The Five Focusing Steps

### 1. Identify The Constraint

Name the current limiting factor in the defined system.

Operational test: if this one thing had a little more usable capacity, better availability, or less waiting, would the whole system produce more goal units now?

Look for:

- WIP, requests, decisions, bugs, leads, or tasks piling up before one step.
- Downstream people or processes waiting for input.
- Frequent expediting, exception handling, or priority overrides.
- The place everyone complains about, works around, or protects.
- The person, role, machine, approval, queue, market, or policy that sets the pace.
- A capacity-vs-demand mismatch: demand load exceeds effective capacity at one point.

Common mistakes:

- Naming “everything” as the constraint.
- Confusing a chronic problem with the active constraint.
- Picking the loudest complaint instead of the place that limits throughput.
- Ignoring system boundary: multiple product lines or workflows may mean multiple systems.

### 2. Exploit The Constraint

Get the most out of the constraint using what already exists.

In practice:

- Ensure the constraint is never starved for good work.
- Stop feeding it defective, incomplete, low-value, or premature work.
- Put the best-prepared work first.
- Remove interruptions, context switching, meetings, maintenance, setup waste, waiting, rework.
- Put quality checks immediately before the constraint.
- Offload work that does not truly require the constraint.
- Give the constraint clear priority rules and visible queue status.

This is the step teams skip. TOC Institute explicitly warns against jumping straight to buying, hiring, or expanding; proper exploit/subordinate work often exposes hidden capacity before investment. ([tocinstitute.org](https://www.tocinstitute.org/five-focusing-steps.html))

Common mistakes:

- Elevating too soon: buying tools, hiring, automating, or reorganizing before using existing capacity well.
- Keeping the constraint busy with low-value work.
- Optimizing non-constraints because they are easier to manage.
- Measuring utilization instead of usable throughput.

### 3. Subordinate Everything Else

Align the rest of the system to the constraint.

In practice:

- Release work only at the rate the constraint can absorb.
- Cap WIP before the constraint.
- Let non-constraints be idle when more work would only create queues.
- Change priorities, metrics, incentives, meetings, SLAs, and staffing to protect the constraint.
- Ensure upstream produces the right work at the right time.
- Ensure downstream has enough sprint capacity so the constraint is never blocked.
- Make the constraint the priority for support, QA, maintenance, decision access, and escalation.

Common mistakes:

- Trying to keep everyone busy.
- Rewarding local efficiency, which creates excess WIP and longer lead times.
- Allowing every stakeholder to inject “urgent” work.
- Treating idle time at non-constraints as waste, when it may be necessary protection for flow.

### 4. Elevate The Constraint

Only after exploit and subordinate, add or redesign capacity.

Examples:

- Hire scarce skill.
- Add equipment.
- Automate a constraint task.
- Outsource overflow.
- Redesign product, process, architecture, approval path, pricing, or demand generation.
- Change policy or governance.
- Increase market demand if the constraint is external.

Evaluate elevation with throughput accounting: will it increase throughput enough to justify the added investment and operating expense?

Common mistakes:

- Capital spend before fixing misuse of existing capacity.
- Adding capacity to the wrong place.
- Automating a bad policy.
- Elevating an internal constraint when demand is already the real constraint.
- Breaking the current constraint without watching where the next one emerges.

### 5. Repeat, And Prevent Inertia

When the constraint is broken, the system has a new constraint. Return to step 1.

The danger is inertia: old rules, buffers, metrics, org charts, dashboards, or habits that were useful for yesterday’s constraint become today’s constraint. The Goal’s five-step formulation ends with the warning not to let inertia become the system’s constraint. ([tocinstitute.org](https://www.tocinstitute.org/the-goal-summary.html))

Common mistakes:

- Treating TOC as a one-off improvement project.
- Institutionalizing temporary workarounds.
- Continuing to optimize the old constraint after it has moved.
- Letting old measurements keep driving old behavior.

## 2. Types Of Constraints

- Physical/capacity: machine, team, role, specialist, test environment, compute, cash, floor space, supplier, calendar capacity.
- Market/demand: the system can produce more than customers currently buy or adopt.
- Policy: a rule, metric, approval path, batch-size rule, incentive, budgeting practice, vendor rule, WIP policy, roadmap process, or “how we do things here.”
- Paradigm/belief: the assumption underneath policy, such as “everyone must be fully utilized,” “large batches are efficient,” or “senior approval reduces risk.”
- Time/attention: the scarce cognitive capacity of a founder, manager, reviewer, designer, engineer, buyer, or individual.

Internal vs external:

- Internal constraint: market demand exceeds the system’s ability to deliver.
- External constraint: the system can deliver more than the market currently demands.
- If demand is external, do not keep optimizing production capacity; improve offer, market access, sales conversion, pricing, trust, or product-market fit.

Policy constraints are usually the most common in practice because physical bottlenecks are often created or amplified by rules: batch policies, cost accounting, approval gates, utilization targets, priority systems, purchasing rules, and incentives. LeanProduction notes policy constraints are commonly the most frequent and hard to see because they are long-established and taken for granted. ([leanproduction.com](https://www.leanproduction.com/theory-of-constraints/))

## 3. How Practitioners Identify The Constraint

Use evidence, not opinion.

Fast field protocol:

1. Define the flow unit: order, feature, ticket, lead, claim, decision, invoice, workout, writing session.
2. Map the flow from demand to goal achievement.
3. Ask at every step: where does work wait?
4. Count WIP and age of WIP at each queue.
5. Compare effective capacity to demand load.
6. Ask who is expediting, who is starved, and who is always interrupted.
7. Test the candidate: if we improved only this, would total throughput rise?

Observable symptoms:

- Largest queue or oldest work items before a step.
- Chronic late work at the same step.
- Expediters cluster around it.
- Downstream people wait for it.
- Upstream creates excess inventory because it cannot flow through it.
- Work is batched there.
- It gets the most exceptions, status meetings, and heroic effort.
- Everyone has a workaround for it.
- Customers wait because of it.

LeanProduction’s practitioner checklist includes WIP accumulation, expediting, cycle-time review, and asking operators where demand is not being met. ([leanproduction.com](https://www.leanproduction.com/theory-of-constraints/)) TOC Institute similarly frames the problem as finding the active constraint that governs the whole value chain. ([tocinstitute.org](https://www.tocinstitute.org/identify-your-constraint.html))

## 4. Throughput Accounting

TOC uses three core operating measures:

- Throughput: rate at which the system generates money or goal units through actual sales/delivery. In business: sales minus truly variable cost.
- Investment / Inventory: money tied up in the system: inventory, equipment, buildings, partially done work, capitalized assets.
- Operating Expense: money spent to turn investment into throughput: payroll, rent, utilities, software, management, fixed operating costs.

Decision test:

- Does this increase throughput?
- Does this reduce investment/inventory?
- Does this reduce operating expense?
- What happens to net profit: `T - OE`?
- What happens to ROI: `(T - OE) / I`?

Local efficiencies are the enemy because they optimize parts instead of the system. A non-constraint running at full utilization mostly creates WIP, longer lead times, stale inventory, more coordination, and more expediting. The Goal summary highlights how conventional efficiency metrics caused Alex’s plant to improve the wrong things while missing actual throughput. ([tocinstitute.org](https://www.tocinstitute.org/the-goal-summary.html)) LeanProduction summarizes TOC’s accounting stance: prioritize throughput first, then investment, then operating expense. ([leanproduction.com](https://www.leanproduction.com/theory-of-constraints/))

## 5. Drum-Buffer-Rope

DBR is the TOC flow-control mechanism.

- Drum: the constraint sets the pace. Schedule around it.
- Buffer: protective time or stock before the constraint or delivery point so variation does not starve the constraint or miss customer commitments.
- Rope: release work into the system only when the constraint can absorb it.

Rules of thumb:

- Do not release work early just to keep people busy.
- Protect the constraint with a buffer, not the whole system with excess WIP.
- Use buffer status as priority: green = normal, yellow = watch, red/black = expedite and investigate.
- Analyze repeated buffer penetration to find root causes.
- If buffers are always full, WIP is too high or release is too early.
- If buffers are repeatedly penetrated, capacity, reliability, quality, or release timing is wrong.

LeanProduction describes DBR as synchronizing production to the constraint while minimizing WIP, with the drum setting pace, buffer protecting flow, and rope controlling release. ([leanproduction.com](https://www.leanproduction.com/theory-of-constraints/))

## 6. Aphorisms And Mental Models

- “An hour lost at a bottleneck is an hour lost for the entire system.” The Goal’s plant example shows bottleneck downtime should be costed as lost system throughput, not local machine cost. ([tocinstitute.org](https://www.tocinstitute.org/the-goal-summary.html))
- “An hour saved at a non-bottleneck is a mirage.”
- The constraint dictates the pace.
- Do not balance capacity; balance flow.
- “The closer you come to a balanced plant, the closer you are to bankruptcy.” ([tocinstitute.org](https://www.tocinstitute.org/the-goal-summary.html))
- A non-constraint’s utilization is determined by the constraint, not by its own potential.
- The system is not improved by making every part look efficient.
- Idle time away from the constraint may be the price of flow.
- The constraint is a leverage point, not merely a problem.
- When the constraint moves, the management system must move with it.

## Sources

- Eliyahu M. Goldratt & Jeff Cox, *The Goal: A Process of Ongoing Improvement*, North River Press; public chapter summary via TOC Institute. ([tocinstitute.org](https://www.tocinstitute.org/the-goal-summary.html))
- James F. Cox III & John G. Schleier, eds., *Theory of Constraints Handbook*, McGraw-Hill, 2010.
- TOC Institute, “The Five Focusing Steps (POOGI).” ([tocinstitute.org](https://www.tocinstitute.org/five-focusing-steps.html))
- TOC Institute, “Definition of Constraint.” ([tocinstitute.org](https://www.tocinstitute.org/constraint-definition.html))
- TOC Institute, “What is the Goal of Business?” ([tocinstitute.org](https://www.tocinstitute.org/what-is-the-goal.html))
- LeanProduction / Vorne, “Theory of Constraints.” ([leanproduction.com](https://www.leanproduction.com/theory-of-constraints/))