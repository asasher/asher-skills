# Machine audit — verify the shipped seed against this machine

The skill ships a **roster seed** (model rows, provider bindings, wake paths). The audit's job is to verify
each seeded default against the current machine: prune rows the machine cannot reach, surface unsupported
provider bindings to the owner and ask what to bind instead, add reachable models the seed omits, probe the
dispatch aliases, and hand the judgment numbers to the owner to tune. Never write a seeded default this
machine failed to verify.

The audit is what makes the project playbook trustworthy, so it also records *how* each row was established —
command shape, timestamp, result or failure class — and the machine and CLI versions the probes ran on. Those
are what let a later reader on a different machine know the rows are not theirs.

## The audit procedure

Read [install-and-reconcile](install-and-reconcile.md) once before probing — the external-worker contract
and the reconciliation rules there govern how steps (1), (2), and (4) are judged. Then run these probes and
record the results:

1. **Which routes work from this harness?** Enumerate native models, then probe the sibling-harness route
   defined by the compiled `reference/harness.md`. Record command shape, timestamp, return/failure class,
   native wrapper label/model evidence, and fallback successor. A failure removes this direction only. Real
   invocation behavior is the operational signal.
2. **Which sibling harness CLIs are installed?** Probe `codex --version` and `claude --version`, then retain
   only the routes step 1 actually exercised. Presence alone is not reachability. Record the versions — they
   are part of what makes a recorded route trustworthy on this machine and stale on another.
3. **Which dispatch aliases does each CLI actually accept?** Roster names are not dispatch aliases. Probe the
   name that would be passed to the CLI's model argument for every row that could cross a harness boundary,
   and record the mapping. A name no probe accepted must never be written as a verified route — the failure
   surfaces at the moment of use, long after resolution looked clean.
4. **Does a project staffing playbook already exist?** Read it. It is the reconciliation target, and what it
   records about a previous machine or CLI version is what a fresh probe is checked against.
5. **Which waits does each harness track?** Probe the wake mechanisms — background-task completion, subagent
   completion, monitors, cron — and record which ones re-invoke the session, effect-verified. These become
   the Wake-paths rows.

Steps (1)–(5) all feed § Writing the roster from the audit; the judgment numbers cannot be probed — see
§ The seed (numbers the user tunes).

## The seed (numbers the user tunes)

Cost/intelligence/taste/effort can't be probed, so their starting values come from the skill's bundled roster
seed and **the user edits them to fit their own machine and pricing.** Keep only rows for models the audit
found reachable; drop any seed row whose model this machine can't reach, and add a seeded row for any
reachable model the seed omits.

The seed is read here and nowhere else. Once the playbook exists it is the authority, and a later resolution
that reaches back to the seed has resolved from a file no one reviewed against this machine.

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
| opus-5        | 3    | 8            | 8     | high   |
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
# harness — a Floor assignment, not a pin (e.g. a sibling skill's watcher dispatches at the Floor).

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
4. CLI mechanics → include only effect-verified directions; never infer symmetry from one working route. Record
   the probed alias mapping beside them, as a rule where the probes support one ("this CLI rejects versioned
   names, accepts bare names") rather than a list of pairs a future model row would fall outside of.
5. Coordinator eligibility → among the reachable routes, record which can own a durable issue child and
   dispatch/escalate its worker stages. Presence or low cost alone does not qualify a route.
6. Floor → set to the lowest capability class the user wants staffed; default it and tell the user to
   confirm.
7. Wake paths → per harness, the effect-verified tracked wake mechanisms (step 5) and the Floor watcher
   fallback; out-of-band waits (review verdicts, merge watches) hold on the top verified row.
8. Effort defaults → the per-role effort lever (see [rankings-and-routing](rankings-and-routing.md)
   § Effort), recorded where the harness exposes it.
