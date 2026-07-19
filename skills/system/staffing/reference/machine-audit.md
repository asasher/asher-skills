# Machine audit — compile the roster, don't hardcode it

The roster is **compiled from the current machine, never shipped fixed.** Native models and effect-verified
sibling harness routes differ by machine, person, and direction. Setup audits them and writes rankings,
capabilities, coordinator eligibility, and CLI mechanics from observed results—not from an example. This is
an agent-driven procedure; **it ships no scripts.**

## The audit procedure

Run these probes and record the results:

1. **Which routes work from this harness?** Enumerate native models, then probe the sibling-harness route
   defined by the compiled `reference/harness.md`. Record command shape, timestamp, return/failure class,
   native wrapper label/model evidence, and fallback successor. A failure removes this direction only. Real
   invocation behavior is the operational signal
   ([install-and-reconcile](install-and-reconcile.md) § External-worker contract).
2. **Which sibling harness CLIs are installed?** Probe `codex --version` and `claude --version`, then retain
   only the routes step 1 actually exercised. Presence alone is not reachability. The result decides which
   mechanics the base includes (see [install-and-reconcile](install-and-reconcile.md) § External-worker contract).
3. **Which harness memory layer exists?** Use the exact global pointer and deferred-module paths in the
   compiled `reference/harness.md`. This also feeds the scope-decision flow.
4. **Do global staffing rules already exist?** Read the detected memory layer for an existing staffing
   roster. Its presence or absence chooses the scope-decision branch (see install-and-reconcile).
5. **Which waits does each harness track?** Probe the wake mechanisms — background-task completion, subagent
   completion, monitors, cron — and record which ones re-invoke the session, effect-verified. These become
   the Wake-paths rows.

Steps (1)–(2) feed § Writing the roster; the judgment numbers cannot be probed — see § The default seed.

## The default seed (numbers the user tunes)

Cost/intelligence/taste can't be probed, so the audit seeds them from a documented default and states plainly
that **the user edits these to fit their own machine and pricing.** Seed only rows for models the audit found
reachable; drop any example row whose model this machine can't reach, and add a seeded row for any reachable
model the example omits.

### Example of audit output (illustrative only — NOT the shipped roster)

The following is **one machine's audit result**, shown so you know the shape to write. Reproduce the
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

# Wake paths — cheapest verified wake first; a model watcher only where nothing is tracked
| harness | tracked wake (no model) | watcher fallback |
|-------------|-------------------------------------------------------------|--------------------|
| Claude Code | background tasks / subagent completions / Monitor re-invoke | sonnet-5, low effort |
| Codex CLI   | none verified                                               | gpt-5.6-terra loop |

# Effort defaults (where the harness exposes per-dispatch effort): low — mechanical/bulk, watch/relay,
# cron; medium — default; high — orchestration, design, hard diagnosis, final adversarial review.

# Reachability (illustrative): active harness → sibling route works through the compiled native wrapper.
# The direction has its own timestamp, failure class, and successor.
```

## Writing the roster from the audit

1. Reachable models → rows of the rankings table, each seeded with cost/intelligence/taste and flagged
   "tune these".
2. Effect-probed harness skills/plugins/tools → the capability-provider registry, with primary, fallback,
   eligible executor, and route state (presence alone is insufficient — step 2).
3. Task/provider pins → the named pin list; carry the mechanical/bulk pin if its worker route is reachable, else leave
   it for the user to set.
4. CLI mechanics → include only effect-verified directions; never infer symmetry from one working route.
5. Coordinator eligibility → among the reachable routes, record which can own a durable issue child and
   dispatch/escalate its worker stages. Presence or low cost alone does not qualify a route.
6. Floor → set to the lowest capability class the user wants staffed; default it and tell the user to
   confirm.
7. Wake paths → per harness, the effect-verified tracked wake mechanisms (step 5) and the Floor watcher
   fallback; out-of-band waits (review verdicts, merge watches) hold on the top verified row.
8. Effort defaults → the per-role effort lever (see [rankings-and-routing](rankings-and-routing.md)
   § Effort), recorded where the harness exposes it.
