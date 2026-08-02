# Machine audit — verify the shipped seed against this machine

The skill ships a **roster seed** (model rows, provider bindings, wake paths). The audit's job is to verify each seeded default against the current machine: prune rows the machine cannot reach, surface unsupported provider bindings to the owner and ask what to bind instead, add reachable models the seed omits, probe the dispatch aliases, and hand the judgment numbers to the owner to tune. Never write a seeded default this machine failed to verify.

The audit is what makes the project playbook trustworthy, so it also records _how_ each row was established — command shape, timestamp, result or failure class — and the machine and CLI versions the probes ran on. Those are what let a later reader on a different machine know the rows are not theirs.

## The audit procedure

Read [install-and-reconcile](install-and-reconcile.md) once before probing — the external-worker contract and the reconciliation rules there govern how steps (1), (2), and (4) are judged. Then run these probes and record the results:

1. **Which routes work from this harness?** Enumerate native models, then probe the sibling-harness route defined by the compiled `reference/harness.md`. Run step 2's version probes first: a direction whose CLI is absent is unavailable (CLI absent), with no owner question to ask. For each installed direction, ask the owner before dispatching any probe whether it is deliberately off for cost or policy — that answer classifies the direction intentionally disabled, and no dispatch probe runs down it. Classify each remaining direction into exactly one route state and record its evidence per § Route classification below, plus the native wrapper label/model evidence where a wrapper carried the probe. A failure removes this direction only. Real invocation behavior is the operational signal.
2. **Which sibling harness CLIs are installed?** Probe `codex --version` and `claude --version`, then retain only the routes step 1 actually exercised. Presence alone is not reachability. Record the versions as the probe record's metadata — part of what makes a recorded route trustworthy on this machine and stale on another, and the cue to re-probe after an upgrade — never as facts of their own that anything resolves against.
3. **Which dispatch aliases does each CLI actually accept?** Roster names are not dispatch aliases. Probe the name that would be passed to the CLI's model argument for every row that could cross a harness boundary, and record the mapping with the CLI version that produced it. A name no probe accepted must never be written as a verified route — the failure surfaces at the moment of use, long after resolution looked clean — and a name no probe ran against is recorded as unverified, never promoted to a dispatch alias by assumption. Where the results support a rule ("this CLI rejects versioned names, accepts bare ones"), its scope is the CLI whose probes established it: one CLI's rule says nothing about how the sibling treats the same names, so the sibling's rule needs its own probes.
4. **Does a project staffing playbook already exist?** Read it. It is the reconciliation target, and what it records about a previous machine or CLI version is what a fresh probe is checked against.
5. **Which waits does each harness track?** Probe the wake mechanisms — background-task completion, subagent completion, monitors, cron — and record which ones re-invoke the session, effect-verified. These become the Wake-paths rows.

Steps (1)–(5) all feed § Writing the roster from the audit; the judgment numbers cannot be probed — see § The seed (numbers the user tunes).

## Route classification — three states, each with its evidence

Every sibling-harness direction the audit records lands in exactly one of three states, and a later reader must be able to tell them apart from the playbook alone, without re-probing. A bare worked/failed record cannot express this: it reads a deliberately disabled route identically to a broken one, and neither reading carries what the successor decision needs.

- **Effect-verified** — a live probe of the role's effect class succeeded, and the row names the class it cleared (write for builders, read for reviewers). Only this state backs dispatch.
- **Intentionally disabled** — installed, but the owner has chosen not to use it, for cost or policy. This state is an owner decision, never a probe result: setup records it only from the owner's explicit choice, with the reason and the date it was made, and never infers it from a failure. On a re-run setup re-checks only the cheap premise — the CLI is still installed, a version probe with no dispatch — and leaves the choice standing. A disabled row's evidence fields hold the version probe (its command shape and the CLI version it returned), the owner's decision with its reason and date as the result, and the direction's recorded successor like any other row. A successful probe never promotes a disabled row; the disable lifts only when the owner says so — in setup's interview or by editing the playbook — never from a probe result.
- **Unavailable** — the probe failed, and the row captures the failure class rather than a bare no. The failure class is what the successor decision reads, and it comes from one of two fixed, named sets — the lists are doctrine, and a classifying session never improvises the boundary:
  - **Transient** — usage limit, rate limit, network failure, timeout: self-expiring constraints. A transient row carries its retry-at machine-readably inside the result/failure-class evidence field as the token `retry-at=<UTC instant, ISO 8601>` — e.g. a result reading `unavailable (usage limit, retry-at=2026-08-05T09:00Z)` — when the failure named a reset; when none was named it carries no token and is probeable immediately. There is no default backoff: the probe is cheap, suppression is only justified by a known reset, and pacing comes from dispatch frequency. A transient write over an established state retains that previously established state and its evidence beside the row — a restoration target, not a second state — so a later healing pass has something to restore. At or past its retry-at a transient row reads as _unverified, probeable_ rather than unavailable — what happens then is the resolver's rule, [rankings-and-routing](rankings-and-routing.md) § Self-heal at the point of use.
  - **Durable** — CLI absent, alias rejected, permission denied, effect denied: broken until a human decision or a setup re-run.

The transient/durable split is a refinement within the unavailable state, not a fourth state: the classification stays three-state, and the intentionally-disabled state is untouched by it.

The capability-provider registry's route-state field uses these same three state names with the same meaning — only an effect-verified route backs selection, and a probe never promotes a disabled one. Its rows carry the registry's own fields (primary, fallback, eligible executor) rather than this section's five, and its owner questions ride the audit's existing provider-binding interview; the contract below is stated for directions, which carry the cross-harness risk this classification exists for.

Each classification carries five evidence fields, all resolvable from its row: the CLI version observed, the timestamp, the command shape used, the result or failure class, and the recorded successor for that direction. Where one audit run established every row, the machine, CLI versions, and date may live once in the probe record the rows sit under; a row probed at any other time carries its own values inline, so the shared record never misdescribes it. The record, rows included, lives in the repo's gitignored machine-local overlay (`docs/agents/local/staffing.md`), never the tracked playbook; its machine-readable form is the stamp line `<!-- machine-record: machine=<short hostname> probed=<YYYY-MM-DD> -->` at its head — what a mechanical staleness check parses where a repo's installed skill set ships one. The machine value is the stable short hostname as a single whitespace-free token — the segment before the first dot, on macOS the local host name (`scutil --get LocalHostName`) — compared case-insensitively.

Timestamps date the observation that **established** the recorded state, not the latest run that confirmed it: a re-probe that finds a row exactly as recorded writes nothing. That is what keeps a re-run with unchanged reachability byte-identical while every row still says when its fact was observed — any change in what a probe observes is written as fresh evidence with its own date.

## The seed (numbers the user tunes)

Cost/intelligence/taste/effort can't be probed, so their starting values come from the skill's bundled roster seed and **the user edits them to fit their own machine and pricing.** Keep only rows for models the audit found reachable; drop any seed row whose model this machine can't reach, and add a seeded row for any reachable model the seed omits.

The seed is read here and nowhere else. Once the playbook exists it is the authority, and a later resolution that reaches back to the seed has resolved from a file no one reviewed against this machine.

### Example of audit output (illustrative only — NOT the shipped roster)

The following is **one machine's audit result**, shown so you know the shape to write. Reproduce the _shape_, not these values:

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

# Wake paths — cheapest verified wake first; a timed wake outranks any watcher; a model watcher
# only where nothing is tracked and no timer facility is verified
| harness | tracked wake (no model) | watcher (last resort) |
|-------------|-------------------------------------------------------------|--------------------|
| Claude Code | background tasks / subagent completions / Monitor re-invoke | sonnet-5, low effort |
| Codex CLI   | none verified                                               | gpt-5.6-terra loop |

# Effort rule: dispatch at the model row's effort value; pure wait/relay and cron duty runs at low
# regardless of model.

# Reachability (illustrative): one row per direction, e.g. active harness → sibling through the compiled
# native wrapper. Each row carries its route state — effect-verified (with the effect class cleared),
# intentionally disabled (with the owner's reason and date), or unavailable (with the failure class) —
# plus its evidence fields and successor, per § Route classification.
```

## Writing the roster from the audit

1. Reachable models → rows of the rankings table, each seeded with cost/intelligence/taste and flagged "tune these".
2. Effect-probed harness skills/plugins/tools → the capability-provider registry, with primary, fallback, eligible executor, and route state (presence alone is insufficient — step 2).
3. Task/provider pins → the named pin list; carry the mechanical/bulk pin if its worker route is reachable, else leave it for the user to set.
4. Directional reachability → one row per direction carrying its route state and evidence (§ Route classification). All three states are written — a disabled or unavailable row is what stops a later reader from re-deriving the direction wrongly — but only effect-verified directions back dispatch; never infer symmetry from one working route. Record the probed alias mapping beside them, as a per-CLI rule where the probes support one ("this CLI rejects versioned names, accepts bare names") rather than a list of pairs a future model row would fall outside of.
5. Coordinator eligibility → among the reachable routes, record which can own a durable issue child and dispatch/escalate its worker stages. Presence or low cost alone does not qualify a route.
6. Floor → set to the lowest capability class the user wants staffed; default it and tell the user to confirm.
7. Wake paths → per harness, the effect-verified tracked wake mechanisms (step 5), any verified timed-wake facility, and the Floor watcher as last resort; out-of-band waits (review verdicts, merge watches) hold on the top verified row, a timed wake outranking any watcher wherever a timer facility is verified.
8. Effort defaults → the per-role effort lever (see [rankings-and-routing](rankings-and-routing.md) § Effort), recorded where the harness exposes it.
