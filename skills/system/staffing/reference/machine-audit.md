# Machine audit — verify the shipped defaults against this machine

The module templates ship **seed defaults** (model rows, provider bindings, wake paths). The audit's job is
to verify each default against the current machine: prune rows the machine cannot reach, surface unsupported
provider bindings to the owner and ask what to bind instead, add reachable models the seed omits, and hand
the judgment numbers to the owner to tune. Never install a default this machine failed to verify.

## The audit procedure

Read [install-and-reconcile](install-and-reconcile.md) once before probing — the external-worker
contract and the scope-decision flow there govern how steps (1), (2), and (4) are judged. Then run
these probes and record the results:

1. **Which routes work from this harness?** Enumerate native models, then probe the sibling-harness route
   defined by the compiled `reference/harness.md`. Record command shape, timestamp, return/failure class,
   native wrapper label/model evidence, and fallback successor. A failure removes this direction only. Real
   invocation behavior is the operational signal.
2. **Which sibling harness CLIs are installed?** Probe `codex --version` and `claude --version`, then retain
   only the routes step 1 actually exercised. Presence alone is not reachability. The result decides which
   mechanics the base includes.
3. **Which harness memory layer exists?** Use the exact global pointer and deferred-module paths in the
   compiled `reference/harness.md`. This also feeds the scope-decision flow.
4. **Do global staffing rules already exist?** Read the detected memory layer for an existing staffing
   roster. Its presence or absence chooses the scope-decision branch.
5. **Which waits does each harness track?** Probe the wake mechanisms — background-task completion, subagent
   completion, monitors, cron — and record which ones re-invoke the session, effect-verified. These become
   the Wake-paths rows.

Steps (1)–(2) feed § Writing the roster; the judgment numbers cannot be probed — see § The default seed.

## The default seed (numbers the user tunes)

Cost/intelligence/taste/effort can't be probed, so the seed values come from the shipped module template and
**the user edits them to fit their own machine and pricing.** Keep only rows for models the audit found
reachable; drop any seed row whose model this machine can't reach, and add a seeded row for any reachable
model the template omits.

### Example of audit output (illustrative only — NOT the shipped roster)

The following is **one machine's audit result**, shown so you know the shape to write. Reproduce the
*shape*, not these values:

```
# Rankings (higher = better) — SEED VALUES, tune to your machine
| model         | cost | intelligence | taste | effort |
|---------------|------|--------------|-------|--------|
| gpt-5.6-sol   | 4    | 9            | 5     | high   |
| gpt-5.6-terra | 6    | 5            | 3     | xhigh  |
| sonnet-5      | 5    | 5            | 5     | high   |
| opus-4.8      | 3    | 7            | 7     | high   |
| fable-5       | 1    | 9            | 9     | high   |

# Capability providers — effect-probed harness/tool routes, never model traits
| need | primary provider | fallback | eligible executor |
|------|------------------|----------|-------------------|
| browser-use | scripted Playwright driving Chrome | `agent-browser` (unreliable — interactive exploration only) · user-session carve-out (chrome provider, per-use consent) | active harness route |
| computer-use | gated: recorded project use case + explicit user approval, then computer-use provider | none — unmet gate is a hard gap | active Codex route |
| imagegen | native imagegen provider | repo headless skill | active Codex route |

# Task-pins
| task type         | pinned model |
|-------------------|--------------|
| mechanical / bulk | gpt-5.6-sol  |

# Floor: sonnet-5 (Claude-side) / gpt-5.6-terra (Codex-side). Watcher/cron duty runs at the Floor per
# harness — a Floor assignment, not a pin (watch-until's watcher runs at the Floor via to-subagent).

# Wake paths — cheapest verified wake first; a model watcher only where nothing is tracked
| harness | tracked wake (no model) | watcher fallback |
|-------------|-------------------------------------------------------------|--------------------|
| Claude Code | background tasks / subagent completions / Monitor re-invoke | sonnet-5, low effort |
| Codex CLI   | none verified                                               | gpt-5.6-terra loop |

# Effort rule: dispatch at the model row's effort value; pure wait/relay and cron duty runs at low
# regardless of model.

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
