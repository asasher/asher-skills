# Machine audit — compile the roster, don't hardcode it

The roster is **compiled from the current machine, never shipped fixed.** Native models and effect-verified
sibling harness routes differ by machine, person, and direction. Setup audits them and writes rankings,
capabilities, coordinator eligibility, and CLI mechanics from observed results—not from an example. This is
an agent-driven procedure; **it ships no scripts.**

## The audit procedure

Run these probes and record the results:

1. **Which routes work from this harness?** Enumerate native models, then probe the sibling-harness route
   defined by the compiled `reference/harness.md`. Record command shape, timestamp, return/failure class,
   native wrapper label/model evidence, and fallback successor. A failure removes this direction only. Do not
   poll vendor policy or credit notices; real invocation behavior is the operational signal.
2. **Which sibling harness CLIs are installed?** Probe `codex --version` and `claude --version`, then retain
   only the routes step 1 actually exercised. Presence alone is not reachability. The result decides which
   mechanics the base includes (see [install-and-reconcile](install-and-reconcile.md) § External-worker contract).
3. **Which harness memory layer exists?** Use the exact global pointer and deferred-module paths in the
   compiled `reference/harness.md`. This also feeds the scope-decision flow.
4. **Do global staffing rules already exist?** Read the detected memory layer for an existing staffing
   roster. Its presence or absence chooses the scope-decision branch (see install-and-reconcile).

From (1) you have the **rows** of the rankings table and directional route states. Independently effect-probe
installed skills/plugins/tools to build the capability-provider registry. From (2) you have the **sibling harness
mechanics** the base needs. What the audit **cannot** probe is the *judgment numbers* — cost, intelligence,
and taste are human assessments, not machine-detectable — so seed them, then let the user tune.

## The default seed (numbers the user tunes)

Cost/intelligence/taste can't be probed, so the audit seeds them from a documented default and states plainly
that **the user edits these to fit their own machine and pricing.** Seed only rows for models the audit found
reachable; drop any example row whose model this machine can't reach, and add a seeded row for any reachable
model the example omits.

### Example of audit output (illustrative only — NOT the shipped roster)

The following is **one machine's audit result**, shown so you know the shape to write. It is an *example of
output*, never the authoritative table — a different machine produces a different set of rows. Reproduce the
*shape*, not these values:

```
# Rankings (higher = better) — SEED VALUES, tune to your machine
| model         | cost | intelligence | taste |
|---------------|------|--------------|-------|
| gpt-5.6-sol   | 4    | 9            | 5     |
| gpt-5.6-terra | 6    | 5            | 3     |
| sonnet-5      | 5    | 5            | 5     |
| opus-4.8      | 3    | 7            | 7     |
| fable-5       | 1    | 9            | 9     |

# Capability providers — effect-probed harness/tool routes, never model traits
| need | primary provider | fallback | eligible executor |
|------|------------------|----------|-------------------|
| browser-use | isolated browser CLI (`agent-browser`) | user-session carve-out (chrome provider, per-use consent) | active harness route |
| computer-use | gated: recorded project use case + explicit user approval, then computer-use provider | none — unmet gate is a hard gap | active Codex route |
| imagegen | native imagegen provider | repo headless skill | active Codex route |

# Task-pins
| task type         | pinned model |
|-------------------|--------------|
| mechanical / bulk | gpt-5.6-sol  |

# Floor: sonnet-5 (Claude-side) / gpt-5.6-terra (Codex-side). Watcher/cron duty runs at the Floor per
# harness — a Floor assignment, not a pin (review-loop reads the Floor directly for its watcher).

# Reachability (illustrative): active harness → sibling route works through the compiled native wrapper.
# The direction has its own timestamp, failure class, and successor.
```

Everything above is **audit output for one environment**. On a machine with, say, no Codex CLI and a
different model lineup, the audit produces a different table, different pins, and different CLI mechanics.
Never present the five-model rows as the canonical staffing roster; they are a labeled example of what step
(1) plus the seed produces here.

## Writing the roster from the audit

1. Reachable models → rows of the rankings table, each seeded with cost/intelligence/taste and flagged
   "tune these".
2. Effect-probed harness skills/plugins/tools → the capability-provider registry, with primary, fallback,
   eligible executor, and route state. Installation or model documentation alone is insufficient.
3. Task/provider pins → the named pin list; carry the mechanical/bulk pin if its worker route is reachable, else leave
   it for the user to set.
4. CLI mechanics → include only effect-verified directions; never infer symmetry from one working route.
5. Coordinator eligibility → among the reachable routes, record which can own a durable issue child and
   dispatch/escalate its worker stages. Presence or low cost alone does not qualify a route.
6. Floor → set to the lowest capability class the user wants staffed; default it and tell the user to
   confirm.

Then hand the seeded numbers to the user to tune — the deliberately-untested part of this skill is the
subjective quality of those seed numbers.
