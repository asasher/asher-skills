# Rankings, capability providers, pins, and resolution order

Keep three structures separate: a model rankings table, a harness/tool provider registry, and explicit pins. Models supply judgment; installed harnesses, skills, plugins, and machine tools supply effects. Never infer a provider from a model name or treat installation alone as reachability.

## Model rankings

Rankings are higher-is-better and contain exactly:

- **cost** — this machine owner's effective cost;
- **intelligence** — unsupervised problem difficulty; and
- **taste** — UI/UX, code/API quality, and copy judgment.

No capability boolean belongs in this table. Rows are models the active harness can actually reach, including effect-verified sibling-harness workers; bounded CLI workers are not coordinator-eligible merely because they are rows.

## Capability-provider registry

Capabilities are named effects routed before model ranking:

| field | meaning |
| --- | --- |
| need | `browser-use`, `computer-use`, `imagegen`, or another required effect |
| primary provider | the skill/plugin/harness/tool that performs it |
| fallback | the separately effect-probed successor, or `none` |
| eligible executor | which reachable harness/model route may operate that provider |
| route state | effect-verified, intentionally disabled, or unavailable with failure class |

For example, ChatGPT-in-Chrome and Computer Use are Codex harness/tool providers, not Terra capabilities; native Imagegen and the repo `codex-imagegen` skill are separate provider routes. Claude Code may dispatch a Codex provider or use a recorded machine fallback, but must not claim the effect as native Claude capability.

Provider selection is a hard gate. Select an effect-verified primary, then its recorded fallback if needed; only after that form the model candidate set from executors eligible to operate the selected route. A missing provider reports a capability gap. Never substitute a different effect or another model.

## Pins

A pin is an explicit routing decision resolved before general ranking:

- a **task pin** binds a task type such as mechanical/bulk work to a worker route;
- a **provider pin** binds a need to a named provider route and eligible executor.

A matching pin short-circuits the general choice, but it does not manufacture reachability: the named route must still be effect-verified. On route loss, follow its recorded provider/model successor and resolve again (a transiently-down pinned route at or past its retry-at gets the inline probe of § Self-heal at the point of use before its successor is taken).

## Resolution order

**Issue-coordinator pre-gate.** Before child/worktree creation, the caller supplies groomed work type, surface/required effects, coordination class/reason, and known uncertainty. Missing data stops dispatch. `orchestrator-required` returns the orchestrator. `routine` starts from the reachable coordinator-eligible set and continues below; it never means cheapest-first.

1. **Matching task/provider pin?** Select it and stop general ranking, subject to effect verification.
2. **Required effect?** Resolve need → effect-verified primary provider → recorded fallback. If neither works, report a hard capability gap. Filter to reachable executors eligible to operate the selected provider.
3. **Taste gate?** For user-facing UI, copy, or API design, remove every model below taste 7. This is a hard gate, not a preference.
4. **Rank survivors** by `intelligence > taste > cost`: intelligence descending, then taste descending, then cheaper cost. Ranking never resurrects a route removed by provider reachability or taste.
5. **Fallback.** If the selected route becomes unreachable, apply the recorded provider/model successor and rerun the same order — a transient-unavailable route at or past its retry-at is probed per § Self-heal at the point of use before being passed over. If no model remains reachable, use the current model in a subagent and report the staffing gap; never skip the stage.

### Browser example (illustrative — one machine's audited bindings, not shipped policy)

Resolve `browser-use` to its named primary provider — in this example scripted Playwright driving Chrome, with the machine's `agent-browser` and harness-native web bindings recorded as interactive-exploration fallback only, never the default. If the primary's effect probe fails, that is a tool failure to surface; the only recorded further fallback is the user-session carve-out (ChatGPT-in-Chrome with per-use explicit consent, for test cases that need the user's real signed-in session). Computer Use is not a browser fallback: it is gated behind a recorded project use case plus explicit user approval, and an unmet gate is a hard capability gap. Then form the eligible executor set and rank it. A smarter model that cannot operate either provider never enters the survivor set.

### Mechanical example

A matching mechanical/bulk task pin selects its recorded worker route at step 1. This is a pin, not a ranking derivation.

## Self-heal at the point of use

A transient-unavailable route heals as a side effect of normal resolution, never through a human or a setup run. The class split and the retry-at token are the machine audit's § Route classification; this section is what a resolver does with them.

- **Probe inline, at the point of use.** Whichever resolution first wants a transient row at or past its retry-at — or carrying none — runs the cheap invocation probe right then, before passing over the row: the staffing route command, a dispatcher preflight, a dispatch adapter's staffing step, whichever got there first. It writes the row with the outcome and proceeds on it. Healing never waits for a particular preflight, a human, or a setup run.
- **A pass restores the prior state.** A passing cheap probe restores the previously established state, effect-verified included, when the CLI version is unchanged and no upgrade cue applies — the limit gated invocation, not effects, so prior effect evidence for the same CLI version still stands. The upgrade cue is orthogonal and always wins: after a CLI upgrade, recovery requires the full effect class before the route backs builder work. A cheap pass under an upgrade cue restores nothing: the probing session writes the fresh observation — the new CLI version, the invocation outcome — and the row stands unverified, re-established only by the effect-class probe any unverified route clears before its first substantive dispatch.
- **A failure reclassifies by observation.** A failed re-probe writes the class actually observed: the same transient class refreshes retry-at and stays transient; a durable class converts the row to durable unavailable. No counters, no auto-escalation — the evidence trail carries observations, not policy state. One carve-out from "writes the row with the outcome": a re-probe whose outcome is exactly what the row records — the same class, no new reset — follows the establishing-observation rule and writes nothing.
- **Whoever probed writes.** Any session that ran a probe writes the row it probed, carrying the full five evidence fields; setup remains the whole-record regenerator. Recording a mid-run route loss — the loss-recording step the worker-death recovery path names — is this same write, with the observed class and the retry-at when the failure named one. Between same-machine sessions the overlay is last-writer-wins, with no lock: each row write is a whole row carrying its own observation evidence, so whichever write survives is something a session actually observed — acceptable for a machine-local evidence record. The fail-closed rule holds for row writes as for whole-record writes: a write that cannot be read back changes nothing.
- **The disabled boundary.** The self-heal path never probes an intentionally-disabled row, and a probe never promotes one; the disable lifts only when the owner says so.

## Effort

Where the harness exposes per-dispatch effort, dispatch at the model row's effort value from the rankings table. One exception: pure wait/relay and cron duty runs at **low** regardless of model. Effort never substitutes for a failed taste or capability gate.

## Defaults, not quality waivers

- Escalate to a more capable reachable route without asking when cheaper output misses the bar.
- Reviews favor high taste/intelligence and may add an independent second model.
