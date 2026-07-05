# Theory of Constraints outside manufacturing

Reference for an AI facilitation tool that helps people find the current constraint in a business, software delivery system, team, project, or personal workflow.

## Operating frame

Theory of Constraints (ToC) is useful outside manufacturing when the system has a goal, recurring work, finite attention/capacity, and enough repeatability that flow can be observed. The constraint is not "the biggest problem"; it is the current limiting factor that prevents more progress toward the goal. In knowledge work, that limiter may be a queue, a scarce skill, one overloaded person, an approval rule, a decision bottleneck, market demand, or management attention.

Use ToC as a focusing method:

1. Define the goal and the unit of throughput.
2. Map how work, decisions, or customers flow to that goal.
3. Find where the flow is limited now.
4. Exploit the constraint before spending money.
5. Subordinate the rest of the system to the constraint.
6. Elevate only after exploitation/subordination are insufficient.
7. Re-identify, because the constraint will move.

For an AI tool, treat every suspected constraint as a hypothesis until it survives evidence checks. The facilitation goal is not to make the user feel certain; it is to make the next highest-leverage experiment obvious.

## 1. Knowledge work and software delivery

### Mapping ToC to team flow

In software and other knowledge work, the "material" is invisible: ideas, requirements, decisions, code, reviews, tickets, designs, tests, incidents, releases, customer feedback. Kanban's importance is that it makes invisible work and queues visible, limits work in progress, and gives teams flow metrics such as lead time, delivery rate/throughput, WIP, and work item age. Kanban University explicitly frames Kanban as a way to manage professional services / knowledge work by visualizing work, limiting WIP, managing flow, making policies explicit, and improving experimentally. [Kanban Guide]

ToC translation:

| Manufacturing term | Knowledge-work equivalent |
| --- | --- |
| Product | Work item, decision, deliverable, customer outcome |
| Inventory | WIP, unfinished tickets, open decisions, unvalidated ideas, unreleased code |
| Work center | Person, role, review step, environment, meeting, approval, service team |
| Bottleneck / constraint | Step or resource that limits completed valuable outcomes |
| Starvation | Constraint waiting for input, clarity, test data, access, decision, deploy slot |
| Blockage | Constraint output cannot move downstream because deploy, QA, approval, or customer acceptance is blocked |
| Buffer | Ready work before the constraint; slack/time protection; decision options |
| Rope | Work release rule that prevents overloading the system before the constraint can absorb it |

Anderson's kanban lineage matters because the early software Kanban story is not just "sticky notes from Toyota." The lineage includes attempts to apply ToC and Drum-Buffer-Rope to software/IT work, followed by the emergence of Kanban as a practical way to visualize, limit WIP, and improve service delivery in knowledge work. TameFlow summarizes this lineage as David Anderson applying ToC in software engineering, with Kanban emerging from that experience; Kanban University describes the current method as managing knowledge work on top of an existing workflow. [TameFlow Knowledge Work] [Kanban Guide]

### The Phoenix Project / DevOps flow

The Phoenix Project applies ToC to IT through the character Brent: a highly skilled engineer whose knowledge is needed everywhere, causing interrupts, queues, hidden dependencies, and stalled delivery. The useful abstraction is not "Brent is bad"; it is "the system has allowed a scarce knowledge resource to become the pacing constraint." The remedy is to protect the constraint, offload non-constraint work, make work visible, reduce unplanned work, create repeatable paths, and change policies so the organization stops routing everything through one person. The book's official page positions it as a novel about IT, DevOps, and business flow, and IT Revolution explicitly lists the Three Ways and Theory of Constraints as underpinning principles. [Phoenix Project]

DevOps' First Way is almost pure ToC thinking: optimize the whole value stream, not local silos; understand flow from requirements to operations; avoid local optimization that damages the system. The Second Way adds fast feedback loops, and the Third Way adds continual experimentation and learning. For a facilitator, that means the "constraint" conversation should not end at diagnosis. It should ask: how do we improve flow, amplify feedback, and learn whether the suspected constraint is really the limiter? [Three Ways]

### Common software delivery constraints

| Suspected constraint | Observable signs | Evidence to gather | Exploit first | Subordinate / elevate |
| --- | --- | --- | --- | --- |
| Code review | PRs age; reviewers overloaded; many "ready for review" items; rework after late review | PR age, review queue length, reviewer calendar load, review turnaround by repo/team | Smaller PRs, review SLAs, reviewer rotation, review checklists, pre-review CI/lint, pair on risky changes | Stop starting new coding when review queue is red; add reviewers; change ownership; improve architecture boundaries |
| CI/test pipeline | Long wait for builds; flaky tests; developers context-switch while waiting; deploys delayed by test failures | Build duration, queue time, flake rate, retries, failure categories | Quarantine flaky tests, parallelize high-value tests, fail fast, fix top recurring failures | Prioritize CI reliability over new feature starts; invest in infra; split test suites |
| Deployment/release | Work "done" but unreleased; release windows scarce; manual approval queues; rollback fear | Deployment frequency, release queue, lead time from merge to prod, failed-change rate | Smaller releases, deployment checklist, feature flags, rehearsed rollback, release owner focus | Align planning to deploy capacity; automate; change approval policy; increase environments |
| Product decisions | Engineers wait for clarifications; late scope churn; many started items blocked by "waiting on product" | Aging blocked tickets, decision latency, meeting/calendar data, rework caused by ambiguity | Decision log, explicit tradeoff rules, office hours, smaller decision batches | Do not start work without decision-ready criteria; add product/UX capacity; delegate decisions |
| Architecture / one expert | One senior person is on every critical path; high interrupt load; work pauses when they are unavailable | Calendar interrupts, mentions/requests, blocked items by person, bus-factor map | Protect focus blocks, queue requests, offload documentation/reviews, create decision templates | Freeze noncritical requests to the expert; pair/mentor successors; invest in docs/platform abstractions |
| Security/compliance | Late gates; repeated findings; emergency escalations; teams treat review as external inspection | Review lead time, finding recurrence, queue length, exception count | Shift-left checklists, pre-approved patterns, reusable controls, threat-model office hours | Make security patterns default; add embedded capacity; change governance from approval to guardrails |
| Customer feedback / validation | Team ships but does not learn; backlog grows with assumptions; sales/support anecdotes dominate | Time from release to feedback, experiment cadence, usage telemetry, win/loss data | Instrument top assumptions, narrow experiments, weekly learning review | Stop building unvalidated work; add research/sales feedback loops |

### TameFlow's knowledge-work distinction

Steve Tendon/TameFlow makes a useful distinction for AI facilitation:

- Constraint in the work process: inside a team or workflow column, where a type of activity is limiting progress.
- Constraint in the work flow: a team/service that carries disproportionate load relative to others.
- Constraint in work execution: the temporary, current "today" limiter caused by events, incidents, absence, or overload.

This matters because a Kanban board may show a local queue while the real system constraint is elsewhere: a team with the highest load, an executive attention bottleneck, or a mental model/policy that keeps work fragmented. TameFlow also points out that management attention can itself be the constraint when managers are overloaded with decisions and inboxes; the practical move is to offload or simplify decisions so the right decisions happen at the right time. [TameFlow Knowledge Work]

### Attention/focus as the solo knowledge-work constraint

For solo work, the constraint is often not "time" in the calendar but usable focused attention. The evidence is not how busy the person is; it is whether important work moves to completion.

Signs that focus is the constraint:

- Many started projects, few shipped outputs.
- Long work-item age without external dependency.
- Days filled by low-value maintenance, inbox, meetings, or tool fiddling.
- Important work requires high cognition but is attempted in fragmented leftovers.
- The person says "I know what to do, I just cannot get to it."
- Work expands because no hard finish criteria exist.

Exploit focus before elevating:

- Define one throughput unit for the week: shipped proposal, published page, closed sale, released feature, finished analysis.
- Reduce active WIP to 1-3 meaningful items.
- Reserve the best cognitive block for the constraint task, not admin.
- Pre-decide next action before ending a work block.
- Remove non-constraint work from peak attention: templates, batching, delegation, automation.
- Make "done" externally observable.
- Protect recovery; exhausted attention cannot be exploited by adding hours.

Subordinate the rest:

- Email, meetings, admin, tools, and learning are scheduled around the focus constraint.
- New opportunities wait unless they directly feed the current constraint.
- Planning is constrained by available focus blocks, not wishful capacity.

Elevate:

- Buy back attention with admin help, childcare, automation, better tools, coaching, health interventions, or fewer commitments.
- Increase skill only if skill is proven to be the constraint; otherwise learning can be disguised avoidance.

## 2. Small business, startups, solopreneurs

### Typical constraint sequence as a business grows

Many small businesses cycle through a recognizable constraint sequence. It is not universal, but it is operationally useful as a hypothesis ladder:

1. Leads / attention: not enough qualified people know the offer exists.
2. Conversion / trust: enough people see it, too few buy.
3. Fulfillment / delivery: enough people buy, delivery is slow or inconsistent.
4. Capacity / repeatability: delivery works, but only at small volume.
5. Owner's time / decisions: the business depends on the owner for sales, delivery, approvals, quality, and prioritization.
6. Team/management system: people exist, but priorities, handoffs, incentives, and accountability are unclear.
7. Market / offer ceiling: the current offer/channel can no longer absorb more throughput at acceptable economics.

Operational table:

| Growth stage | Current constraint hypothesis | What to ask | Bad fix | Better ToC move |
| --- | --- | --- | --- | --- |
| No demand | Market/lead flow | "If fulfillment capacity doubled tomorrow, could we sell it?" | Hire ops, polish internal process | Increase qualified conversations; sharpen niche/offer/channel |
| Interest but no sales | Conversion/trust | "Where do prospects drop or stall?" | More leads | Improve offer, proof, risk reversal, sales follow-up |
| Sales but poor delivery | Fulfillment | "What work waits longest after payment?" | More marketing | Stabilize delivery, reduce custom work, check quality before owner review |
| Delivery works but cannot scale | Capacity/process | "What part of fulfillment always runs out?" | Add random hires | Standardize constraint step, offload, train, create buffers |
| Everything waits on founder | Owner attention/decision | "What cannot move without the owner?" | Founder works nights | Decision rules, delegation, assistant/ops lead, narrow founder role |
| Team exists but chaos grows | Policy/management | "Which policy causes WIP, rework, or priority conflict?" | More meetings | Explicit priorities, work release rules, accountability, dashboards |

### Market constraints vs internal constraints

Market constraint:

- Capacity exists but demand is insufficient at the current price/offer/channel.
- Utilization is low in delivery.
- Sales pipeline lacks qualified opportunities.
- Discounts or founder heroics are needed to close.
- Improving internal efficiency will not increase throughput unless it changes the market offer.

Internal constraint:

- Demand exceeds ability to deliver or decide.
- Customers wait; deadlines slip; quality falls; backlog grows.
- Sales are paused because delivery is overloaded.
- More marketing would worsen the system.

Facilitator test:

> If we doubled delivery capacity next month, would revenue increase?

- If yes, internal capacity may be the constraint.
- If no, market demand, positioning, pricing, trust, or sales conversion is probably the constraint.

Second test:

> If we doubled qualified leads next month, could we fulfill profitably without breaking quality?

- If yes, lead flow/market may be the constraint.
- If no, fulfillment/capacity/owner attention is already constraining.

### When the constraint is the owner

The owner is the constraint when the owner is the scarce resource whose availability determines sales, fulfillment, quality, or decisions.

Observable signs:

- Work waits for founder review, approval, or context.
- Sales stops when the owner is delivering.
- Delivery stops when the owner is selling.
- Employees ask the owner to resolve routine tradeoffs.
- The owner is copied on everything.
- The calendar, not customer demand, determines throughput.
- Customers buy "the founder" rather than the system.

Exploit owner time:

- List all owner-only work; challenge each item.
- Remove admin, scheduling, formatting, status reporting, basic research.
- Create decision rules for common approvals.
- Batch owner reviews at fixed times.
- Protect selling or product judgment if that is the true constraint.
- Stop routing low-value quality checks through the owner.

Subordinate:

- Team priorities are set to keep the owner-constraint working only on highest-throughput work.
- Staff prepare inputs before owner review: clear ask, options, recommendation, risk.
- New initiatives wait unless they increase throughput through the owner constraint.

Elevate:

- Hire an operator, assistant, salesperson, delivery lead, editor, or account manager depending on which owner function constrains throughput.
- Productize/custom-limit the offer.
- Build assets that replace repeated owner explanations: templates, playbooks, demos, FAQs, scripts, onboarding.

Common error: saying "the owner is the problem." The ToC framing is "the system depends on an owner-only capability." That keeps the intervention concrete and non-blaming.

## 3. Critical Chain Project Management in brief

Critical Chain Project Management (CCPM) is Goldratt's project-management application of ToC. The project constraint is the longest resource-leveled chain of dependent work, not just the precedence-only critical path. CCPM focuses on resource contention, bad multitasking, and aggregated buffers. [Critical Chain]

Core problems CCPM addresses:

- Student syndrome: people start late because task estimates contain safety.
- Parkinson's law: work expands to fill the time allowed.
- Bad multitasking: people switch between projects to satisfy many local due dates, slowing all of them.
- Local safety hoarding: each task owner protects their own date, but the project still slips.
- Resource dependencies: the same scarce person/tool/team appears on multiple paths.

CCPM moves:

- Estimate tasks aggressively, often around a 50 percent confidence duration rather than padded local commitments.
- Remove individual task safety and aggregate it into shared buffers.
- Add a project buffer at the end of the critical chain.
- Add feeding buffers where non-critical chains feed the critical chain.
- Add resource buffers/alerts so scarce resources are ready when needed.
- Manage by buffer consumption, not by punishing every local task variance.
- Use a fever chart: percent project complete vs percent buffer consumed.

AI facilitation prompts:

- "Which named people or teams appear on multiple critical paths?"
- "Where do projects wait for the same expert, environment, approval, or customer input?"
- "What work is being multitasked only because each project manager is protecting their local date?"
- "Where is safety hidden: task estimates, review cycles, approval windows, release calendars?"
- "What buffer would protect the project without hiding safety in every task?"

## 4. Personal productivity applications of ToC

Personal ToC is not generic productivity advice. It asks: what is the single limiting factor preventing more of the desired outcome?

Define the personal system:

- Goal: income, published work, health, job search progress, client delivery, learning milestone.
- Throughput unit: shipped artifact, sales call completed, workout completed, applications sent, pages revised, bugs closed.
- Inventory: open loops, drafts, unread notes, half-built projects, unmade decisions.
- Operating expense: time, energy, money, stress, attention.

Constraint patterns:

| Personal constraint | Signs | Exploit | Subordinate | Elevate |
| --- | --- | --- | --- | --- |
| Attention | Fragmented days; many starts; few finishes | One-item WIP, focus block, clear done criteria | Admin waits; notifications off | Better environment, support, health, fewer obligations |
| Decision | Research loops; no commitments | Decision deadline, reversible/irreversible split | Stop gathering low-value info | Coach/advisor, decision framework |
| Energy | Work quality collapses after short periods | Schedule high-value work at energy peak | Low-energy tasks later | Sleep, health, workload reduction |
| Skill | Repeated failure at same capability | Deliberate practice on bottleneck skill | Do less unrelated learning | Training, mentor, hire/collaborate |
| Courage / exposure | Assets exist but are not published/sold | Small public reps, scripts, risk caps | Perfection work waits | Accountability, therapy/coaching, audience practice |
| Environment | Interruptions dominate | Physical/digital boundary | Household/team agreements | Coworking, childcare, equipment |

Personal failure mode: optimizing a non-constraint because it feels productive. Example: designing a better note system when the constraint is publishing; learning another framework when the constraint is asking customers to buy; waking earlier when the constraint is an unclear offer.

## 5. How practitioners run constraint-finding sessions

### Facilitation principles

1. Start with the goal. Without the goal, "constraint" degenerates into complaint sorting.
2. Separate evidence from interpretation. "PRs wait 4.8 days for review" is evidence; "engineering is slow" is interpretation.
3. Look for queues, waiting, starvation, expediting, rework, and scarce attention.
4. Do not ask only "what is broken?" Ask what limits more throughput when nothing unusual is broken.
5. Convert every suspected constraint into a testable hypothesis.

### Questions consultants ask

Goal and throughput:

- "What is the goal of this system right now?"
- "What would count as more throughput?"
- "What should happen more often, faster, or more reliably?"
- "If the system were twice as good, what number would be twice as high or half as low?"
- "What is the unit of value that actually matters to the customer or owner?"

Flow and waiting:

- "Where does work wait longest?"
- "Where does work pile up?"
- "What queue is always aging?"
- "What gets expedited most often?"
- "Where do people chase status?"
- "What work is done but not yet useful to the customer?"
- "Where does downstream work starve for input?"
- "Where do defects, clarifications, or approvals send work backward?"

Scarce resource:

- "What do you always run out of?"
- "Whose calendar determines whether work moves?"
- "Who is mentioned in the most blocked-item explanations?"
- "If one person disappeared for two weeks, what would stop?"
- "What skill, environment, data, tool, or decision right is in shortest supply?"
- "What do people avoid using because it is hard to book?"

Magic-wand/doubling:

- "If you could magically double one thing for a month, what would most increase throughput?"
- "If you could double one person's available time, whose time would matter most?"
- "If you could make one queue disappear, which queue would improve the whole system?"
- "If we doubled this suspected constraint, what would become the next constraint?"

Policy and decision:

- "What rule causes good work to wait?"
- "What approval exists because of an old failure?"
- "What metric rewards local efficiency but hurts system flow?"
- "What decision is repeatedly escalated?"
- "Where are people not allowed to use capacity they already have?"
- "What policy makes the capacity look scarce?"

Market/business:

- "If you had twice the demand, could you fulfill it profitably?"
- "If you had twice the capacity, could you sell it?"
- "Where in the funnel does qualified demand disappear?"
- "What promise do customers hesitate to believe?"
- "What segment/channel absorbs the offer fastest?"

Solo/personal:

- "What do you already know you should do but are not doing?"
- "What work has the highest payoff but gets the worst attention?"
- "What repeats every week without creating throughput?"
- "What is open because you have not decided, not because you lack time?"

### Workshop formats

#### 60-90 minute quick constraint triage

Use when the system is small, the user needs a next experiment, or the tool is in an interactive chat session.

Agenda:

1. Define goal and throughput metric.
2. List current work stages or funnel stages.
3. Ask waiting/queue/scarce-resource questions.
4. Identify 2-3 suspected constraints.
5. Gather quick evidence: examples, timestamps, queue counts, blocked items.
6. Pick the strongest hypothesis.
7. Define an exploit-first experiment for 1-2 weeks.
8. Define what would prove/disprove it.

Output:

- Constraint hypothesis.
- Evidence table.
- Exploit action.
- Subordination rule.
- Metrics and review date.

#### Half-day flow mapping / Kanban STATIK-style session

Use when work crosses a team or service and the current workflow is not shared. Kanban University's STATIK approach typically runs from hours to days and includes dissatisfaction, demand, system capability, workflow, classes of service, and system design. [Kanban Guide]

Agenda:

1. Sources of dissatisfaction: customers and delivery team.
2. Demand analysis: work item types, arrival patterns, channels.
3. Capability analysis: lead time, delivery rate, predictability, failure demand.
4. Workflow model: real current steps, not desired process.
5. Queue and WIP map: count work at each step and age it.
6. Policy map: entry/exit criteria, approval rules, priority rules, WIP limits.
7. Constraint hypothesis: where flow is limited and why.
8. Design experiment: WIP limit, review policy, swarming rule, or offloading action.

Output:

- Current workflow map.
- Queue/aging evidence.
- Constraint hypothesis with confidence.
- Explicit policy change to test.

#### 1-2 day deeper ToC diagnostic

Use when symptoms are scattered and political, or when the constraint may be a policy/paradigm. Combine flow evidence with Current Reality Tree / conflict-cloud work.

Agenda:

1. Define goal and necessary conditions.
2. Elicit undesirable effects (UDEs).
3. Cluster UDEs by causal themes.
4. Build causal logic: "If X, then Y."
5. Look for a small number of root causes or a core conflict.
6. Translate root cause into a constraint hypothesis.
7. Validate against flow data.
8. Design exploit/subordinate/elevate experiments.

Output:

- Root-cause/current-reality map.
- Policy or paradigm candidates.
- Validation plan before major change.

#### 1-4 week evidence sprint

Use when opinions conflict or data is absent.

Instrumentation:

- Timestamp work entry/exit by stage.
- Count WIP and age WIP twice weekly.
- Track blocker reason codes.
- Sample calendar/interrupt load for suspected people constraints.
- Track arrivals vs completions in the funnel.
- Track rework and defect loops.
- Track throughput before and after exploit action.

Output:

- Constraint evidence dashboard.
- Decision: exploit more, subordinate, elevate, or re-identify.

### Evidence vs opinion

Practitioners let people give opinions, then convert them into observable claims.

| Opinion | Evidence conversion |
| --- | --- |
| "Review is slow." | Median/85th percentile PR review time; PRs older than SLA; reviewer load |
| "We need more developers." | Arrival rate vs completion rate; code waiting for review/test/deploy; dev idle/starved time |
| "The founder is the bottleneck." | Items waiting for founder; founder calendar; decisions only founder can make |
| "Sales is the problem." | Funnel conversion by stage; qualified lead volume; sales cycle age; lost reasons |
| "Ops blocks us." | Deploy queue, change-failure rate, approval latency, environment availability |
| "People are multitasking." | Active WIP per person; interrupt log; cycle time vs touch time |

Evidence hierarchy:

1. Direct timestamp/flow data.
2. Work item age and queue counts.
3. Calendar/interrupt logs.
4. Recent concrete examples.
5. Interview consensus.
6. Strong feelings without examples.

Interview consensus is useful for finding where to look, not enough to justify elevation spending.

### Validating a suspected constraint before acting

Validation checklist:

1. Goal linkage: explain how this constraint limits throughput, not just comfort.
2. Queue evidence: show WIP, wait time, rework, starvation, or expediting around it.
3. Capacity-demand check: compare arrival rate to completion capacity.
4. Exploit test: improve the suspected constraint without major spend.
5. System response: total throughput, lead time, or reliability improves.
6. Constraint movement: after improvement, the queue moves elsewhere or the next limiter appears.
7. Counterfactual: if this constraint were doubled, name the next likely constraint.

If improving the suspected constraint only improves a local metric and system throughput does not change, it was probably not the constraint or the intervention failed to subordinate the rest of the system.

### Using Weisbord / organizational diagnosis as an overlay

Weisbord's six-box model is not ToC, but it is useful when the apparent constraint is organizational rather than physical. Use it to locate policy constraints masquerading as capacity constraints:

- Purpose: is the goal unclear or contested?
- Structure: do handoffs or reporting lines create waiting?
- Relationships: do conflicts create rework or avoidance?
- Rewards: do incentives reward local efficiency over flow?
- Leadership: is management attention or decision authority the constraint?
- Helpful mechanisms: are information systems, meetings, tools, or policies blocking flow?

The AI tool should use this overlay after a user says "we need more people." Often the missing capacity is created by unclear purpose, bad structure, conflicting incentives, or approval mechanisms. [Weisbord]

## 6. Common failure modes

### Fixing non-constraints

Symptom: the team improves a visible annoyance, but throughput does not improve.

Examples:

- Optimizing coding speed when review/deploy is constrained.
- Improving documentation style when sales conversion is constrained.
- Adding automation to an underused internal process while the market constraint remains.
- Improving personal note-taking when publishing is constrained.

Guardrail: before acting, ask "If this improves by 50 percent, what system-level metric changes?"

### Local optimization

Symptom: one department gets more efficient while the whole system slows.

Examples:

- Developers start more tickets to stay utilized, increasing review/test WIP.
- Sales sells custom work to hit quota, overwhelming fulfillment.
- Support closes tickets fast, causing repeat contacts.
- Founder clears inbox instead of moving the constraint outcome.

Guardrail: optimize global throughput and lead time, not local utilization.

### Jumping to elevation

Symptom: the proposed fix is hiring, buying tools, adding process, or reorganizing before exploitation.

Exploit-first questions:

- Is the constraint ever idle for preventable reasons?
- Is it doing work someone/something else could do?
- Does bad input make it waste capacity?
- Are setup/context switches consuming it?
- Is its priority clear?
- Is downstream blockage preventing its output from mattering?

### Constraint moves after elevation

Symptom: the team celebrates a fix, then performance stalls somewhere else.

This is normal. Step 5 is not a postscript; it is the operating loop.

Guardrail:

- After each intervention, re-map queues.
- Ask "Where did the waiting move?"
- Keep historical notes so old policies do not preserve a broken constraint.

### Mistaking symptom for constraint

Symptom: the loudest pain is treated as the limiter.

Examples:

- "QA is slow" because upstream sends large, ambiguous, low-quality batches.
- "Engineering is slow" because product decisions are late.
- "Sales is weak" because the offer is unclear.
- "I lack discipline" because the personal system has too much WIP and no protected attention.

Guardrail: trace the symptom upstream and downstream. A true constraint limits system throughput; a symptom may simply be where pain is visible.

### Policy constraints masquerading as capacity constraints

Symptom: everyone says "we need more people," but the real limiter is a rule.

Examples:

- Only one person is allowed to approve routine changes.
- Work is pushed into teams regardless of WIP.
- Incentives reward starting projects, not finishing.
- Security review happens only at the end.
- Founder must approve discounts below an arbitrary threshold.
- Teams cannot talk directly to customers.

Guardrail:

- Ask "What policy makes this capacity unavailable?"
- Ask "If the rule changed, would existing capacity be enough?"
- Run a reversible policy experiment before hiring.

### Personalizing the constraint

Symptom: the constraint is framed as a person's flaw.

Better framing:

- Bad: "Brent is the bottleneck."
- Better: "The organization has concentrated too much scarce knowledge and interrupt load in Brent."
- Bad: "The founder cannot delegate."
- Better: "The business lacks decision rules and quality mechanisms that let non-founder work move safely."

Guardrail: name the system dependency, not the character defect.

### Treating complex/creative work as a stable factory

ToC can fail when:

- Work is novel enough that flow is not repeatable.
- The goal is exploratory learning, not throughput.
- Multiple interacting constraints dominate and cannot be reduced to one practical focus.
- Demand is highly uncertain and the main task is discovery.
- Quality, safety, ethics, or legality are hard constraints, not optimization variables.

Modern hedge:

- Treat the constraint as a timeboxed hypothesis.
- Use small experiments.
- Re-identify regularly.
- Combine ToC with discovery, Lean Startup, PDCA, Improvement Kata, or A3 thinking.

## AI facilitation design implications

### Data objects

Minimum useful model:

- System: goal, throughput metric, necessary conditions.
- Flow stages: name, entry/exit policy, WIP, age, owner.
- Work item types: arrival rate, completion rate, lead time.
- Suspected constraints: type, evidence, confidence, owner, exploit options.
- Policies: rule, purpose, effect on flow, reversibility.
- Experiments: hypothesis, action, prediction, metric, review date.
- Constraint history: old constraint, action taken, result, next constraint.

### Suggested AI session flow

1. Goal: "What is this system for? What should increase?"
2. Throughput: "What unit of valuable output can we count weekly?"
3. Flow map: "What stages does work/customer value pass through?"
4. Queue scan: "Where does work wait longest or pile up?"
5. Scarcity scan: "What do you always run out of?"
6. Policy scan: "What rule or approval causes waiting?"
7. Market/internal check: "If capacity doubled, could demand absorb it? If demand doubled, could capacity absorb it?"
8. Constraint hypothesis: write one sentence.
9. Evidence table: separate observed facts from interpretations.
10. Exploit experiment: choose a no/low-spend intervention.
11. Subordination rule: what must other parts stop/start doing to protect the constraint?
12. Review: date, metric, prediction, re-identification prompt.

### Constraint hypothesis template

```text
The current constraint appears to be [resource/step/policy/market/attention],
because [evidence: queue/wait/starvation/expedite/capacity-demand],
which limits [throughput metric/goal].
If we exploit it by [action] and subordinate by [rule],
we predict [metric] will change by [amount/direction] within [timebox].
If not, we will re-check [alternate constraint].
```

### Intervention template

```text
Hypothesis:
  [Constraint] is limiting [throughput].

Exploit action:
  [Low/no-spend way to get more from current constraint.]

Subordination rule:
  [What upstream/downstream/non-constraints will change to support it.]

Prediction:
  [Throughput/lead time/WIP/queue age will improve.]

Measure:
  [Metric, baseline, target, cadence.]

Review:
  [Date/person/decision rule.]

Possible next constraint:
  [Where waiting is expected to move.]
```

## Source anchors

- TOCICO: current public framing of ToC as a practical improvement method across companies, hospitals, supply chains, IT teams, government agencies, plus certification/body-of-knowledge role. [TOCICO]
- TOC Institute: Five Focusing Steps and core constraint definitions. [TOC Institute Focusing Steps]
- TameFlow / Steve Tendon: knowledge-work constraints, management attention as constraint, market/policy constraints, and distinctions among work-process, workflow, and work-execution constraints. [TameFlow Knowledge Work]
- Kanban University: Kanban as knowledge-work management; visualize invisible work, limit WIP, manage flow, explicit policies, feedback loops, STATIK workshop timing and steps. [Kanban Guide]
- IT Revolution: The Phoenix Project as DevOps/ToC allegory; Three Ways as flow/systems thinking, feedback loops, experimentation/learning. [Phoenix Project] [Three Ways]
- Clarke Ching: practitioner framing of bottleneck work for people who have read The Goal and need to make ToC practical; cited here as "bottleneck rules" style facilitation rather than academic theory. [Clarke Ching]
- Goldratt: The Goal for core ToC and Herbie; Critical Chain for CCPM, student syndrome, Parkinson's law, and aggregated buffers.
- Weisbord: six-box organizational diagnosis as an adjacent facilitation overlay for policy/organization constraints. [Weisbord]

[TOCICO]: https://www.tocico.org/
[TOC Institute Focusing Steps]: https://www.tocinstitute.org/five-focusing-steps.html
[TameFlow Knowledge Work]: https://tameflow.com/blog/2021-06-30/daily-flow-chat-with-steve-tendon-about-constraints-in-knowledge-work/
[Kanban Guide]: https://kanban.university/kanban-guide/
[Phoenix Project]: https://itrevolution.com/product/the-phoenix-project/
[Three Ways]: https://itrevolution.com/articles/the-three-ways-principles-underpinning-devops/
[Clarke Ching]: https://clarkeching.com/
[Critical Chain]: https://en.wikipedia.org/wiki/Critical_chain_project_management
[Weisbord]: https://doi.org/10.1177/105960117600100405
