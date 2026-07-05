## Part A: From Constraint To Experiment

**Operating rule:** treat the identified constraint as the current best hypothesis about leverage, then move through Goldratt’s sequence: identify, exploit, subordinate, elevate, repeat. TOC Institute explicitly warns against jumping to investment before exploitation/subordination and gives concrete exploit/subordinate/elevate examples. ([tocinstitute.org](https://www.tocinstitute.org/five-focusing-steps.html))

### 1. Baseline The Constraint

Capture before changing:

- System goal: throughput definition, customer outcome, economic outcome.
- Constraint hypothesis: resource, policy, market, supplier, skill, decision queue, or demand.
- Evidence: queue/WIP, utilization, wait time, buffer penetration, late work, rework, expedite frequency.
- Scope: one value stream only; independent flows may each have their own constraint. TOC Institute notes that as system definition becomes too complex, “constraint” loses clarity. ([tocinstitute.org](https://www.tocinstitute.org/constraint-definition.html))

### 2. Exploit-First Checklist

No or low-spend actions before elevation:

- Reduce constraint idle time: protect staffing, breaks, materials, approvals, tools, data, maintenance, changeovers.
- Prevent starvation/blockage: maintain a small protective buffer before the constraint and enough space/capacity after it.
- Offload non-constraint work: move prep, inspection, admin, packaging, setup, triage, meetings, reporting, and rework elsewhere.
- Quality-check before constraint: do not spend constraint minutes on defective, incomplete, unqualified, or low-priority work.
- Sequence intelligently: run the constraint’s schedule as the “drum”; avoid local priority churn.
- Batch deliberately: reduce transfer batches to improve flow, but manage process batches where setup time dominates; use SMED/standard work if setup consumes constraint time.
- Measure lost constraint minutes by cause: starved, blocked, setup, rework, unavailable operator, waiting decision, waiting input.

### 3. Subordination Policies

Make every non-constraint serve the constraint:

- Release work at the rate the constraint can absorb, not at the rate upstream teams can start.
- Cap WIP upstream; excess upstream output only lengthens lead time.
- Change priority rules: constraint work beats local efficiency, utilization, and departmental targets.
- Freeze or stabilize the constraint schedule for a short horizon.
- Use buffer management: expedite only when the constraint/shipping buffer is meaningfully penetrated.
- De-optimize non-constraints when needed: idle, help, clean, prep, inspect, fetch, or absorb variability.
- Align metrics: stop rewarding non-constraint utilization if it creates WIP before the constraint.

### 4. Elevation Options

Escalate only after exploitation/subordination are visibly exhausted.

| Elevation | Typical Cost | Main Risk |
|---|---:|---|
| Overtime / extended hours | low-medium OpEx | fatigue, quality loss |
| Cross-training / reassignment | medium | ramp time, partial skill |
| Better tooling / fixtures / automation aid | medium | integration delay |
| Outsourcing constraint work | medium-high | quality, dependency |
| Add specialist / machine / team | high recurring or CapEx | demand may not justify |
| Redesign product/process | high | broader disruption |
| Pricing, product mix, demand shaping | variable | customer impact |
| Sales/marketing expansion for demand constraint | high uncertainty | causal lag |

### 5. Intervention As Experiment

Use this form:

> If we change **X** at constraint **Y**, because mechanism **Z**, then **throughput/lead time/WIP/utilization** should change by **N** within **T**, while **guardrails** remain acceptable.

Minimum experiment record:

- Hypothesis: what causal belief is being tested.
- Prediction: observable numeric change and timing.
- Scope: team/product/customer segment/shift/work type.
- Measurement: baseline, sampling interval, data owner.
- Review cadence: daily for operations, weekly for knowledge work, per campaign for market constraints.
- Decision rule: adopt, adapt, abandon, elevate, or re-identify constraint.

This is directly compatible with PDSA/PDCA: Deming Institute emphasizes theory, prediction, study of actual results, and revision of theory. ([deming.org](https://deming.org/explore/pdsa/)) IHI’s Model for Improvement uses aim, measures, change idea, and small-scale PDSA tests. ([ihi.org](https://www.ihi.org/resources/how-to-improve))

### 6. Metrics To Watch

Core:

- Throughput: completed valuable units per time; for commercial systems, contribution/throughput dollars.
- Lead time: request to delivery.
- WIP at/before constraint: queue depth, age, buffer color/status.
- Constraint utilization: productive constraint time divided by available constraint time.
- Constraint lost time: starved, blocked, setup, rework, waiting, unavailable.
- First-pass yield before constraint.
- Due-date performance / OTIF.
- Operating expense and inventory/WIP as guardrails.

Interpretation:

- Throughput up, WIP stable/down: good.
- Constraint utilization up, throughput flat: likely feeding wrong work, quality loss, downstream blockage, or false constraint.
- WIP before constraint up, throughput flat: release/subordination failure.
- Lead time down but throughput flat: useful flow improvement, but not necessarily constraint elevation.

### 7. Knowing The Constraint Moved

The constraint likely moved when:

- The old constraint has available time while another step accumulates WIP/late work.
- Extra capacity at old constraint no longer increases system throughput.
- Buffer penetrations shift location.
- Expedites, wait states, or customer delays concentrate elsewhere.
- Market demand, not internal capacity, becomes the limiter.
- Product mix changes make a different resource binding.

Re-identify after every material improvement, every product-mix shift, and on a fixed cadence.

### 8. Adjacent Methods

- Improvement Kata: current condition, target condition, obstacle, next experiment; useful for coaching disciplined constraint experiments. ([www-personal.umich.edu](https://www-personal.umich.edu/~mrother/Homepage.html))
- Lean A3: problem, current state, countermeasures, action plan, and evidence on one page; useful as the facilitation artifact. ([lean.org](https://www.lean.org/lexicon-terms/a3-report/))
- Small Bets: cheap exploratory actions under uncertainty; useful where constraint diagnosis is weak or creative/market work is involved. ([simonandschuster.com](https://www.simonandschuster.com/books/Little-Bets/Peter-Sims/9781439170434))
- Lean/Six Sigma: use Lean to remove waste around the constraint; use Six Sigma where variation/defects consume constraint capacity.

## Part B: Critiques And Pitfalls

### Legitimate Criticisms

- Single-constraint simplification: TOC is powerful when a value stream has one dominant limiter, but complex systems may have multiple independent flows, shifting product mixes, feedback loops, or coupled bottlenecks.
- Knowledge/creative work ambiguity: “throughput” may be hard to define; WIP can be cognitive; slack may be necessary for discovery, not waste.
- Market constraints are murky: “exploit demand” is not like exploiting a machine. It may require positioning, pricing, channel, product quality, trust, or category timing.
- Boundary disputes: TOC says where to improve; Lean says how to improve flow/waste; Six Sigma says how to reduce variation. Treating them as rival religions creates bad analysis.
- Optimization critique: TOC heuristics can be inferior to formal optimization for product mix or scheduling when the model is stable and solvable. See Linhares on product-mix complexity and Gupta & Snyder’s TOC/MRP/JIT literature review.
- Evidence critique: parts of TOC practice are case-heavy and consultant-driven; empirical generalization varies by domain.
- People/policy risk: “subordinate everything” can become top-down coercion unless local incentives, autonomy, and learning are redesigned.

### When TOC Is The Wrong Lens

Use another lens first when:

- The goal is not agreed.
- The issue is safety, ethics, compliance, or existential risk.
- The work is exploratory with no stable repeatable flow.
- Product-market fit is unknown.
- There are many independent systems with no shared throughput measure.
- The bottleneck is political trust, conflict, or governance legitimacy.
- Failure modes are rare/high-impact, needing resilience or risk analysis.
- A solvable mathematical optimization model exists and precision matters.

### Modern Practitioner Hedges

- Treat “the constraint is X” as a hypothesis with confidence level and evidence.
- Timebox diagnosis; do not let constraint analysis become the constraint.
- Run small experiments before reorgs or CapEx.
- Re-identify regularly.
- Separate value streams before naming a single constraint.
- Keep guardrail metrics: quality, safety, morale, cost, customer trust.
- Combine methods pragmatically: TOC for focus, A3/PDSA/Kata for learning, Lean/Six Sigma for countermeasures.

Key sources: TOC Institute on focusing steps and constraint management; Deming Institute and IHI on PDSA; Lean Enterprise Institute on A3; Rother/Toyota Kata; Peter Sims’ *Little Bets*; Rahman 1998, Gupta & Snyder 2009, Nave 2002, and Linhares 2009 for review/critique context.