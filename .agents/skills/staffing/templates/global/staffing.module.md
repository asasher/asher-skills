# Machine staffing — Codex

{{COMMON}}

## Models

Seed defaults — setup verifies each row against this machine (unreachable rows are pruned, missing
reachable models are added) and the owner tunes the judgment numbers. Effort is the model's default
dispatch level where the harness exposes one.

| model | cost | intelligence | taste | effort |
|---|---:|---:|---:|---|
| gpt-5.6-sol | 4 | 9 | 5 | high |
| gpt-5.6-terra | 6 | 5 | 3 | xhigh |
| sonnet-5 | 5 | 5 | 5 | high |
| opus-4.8 | 3 | 7 | 7 | high |

The Codex models are coordinator-eligible through native agent threads. The Claude rows are effect-verified bounded worker routes, not coordinator-eligible until durable child ownership is separately proven. Add a fable-5 row only after its CLI alias and requested effect are verified on this machine. Floor: gpt-5.6-terra for native Codex roles.

## Capability providers

Each row is a role slot with this machine's default binding; setup probes the default and asks the owner
about gaps.

| need | primary provider (default binding) | fallback / hard edge |
|---|---|---|
| browser-use | scripted **Playwright driving Chrome**, staffed by terra — verification is a script with artifacts, headed or headless | machine `agent-browser` and harness-native web bindings have proven unreliable — never the default, only for interactive exploration a script cannot serve; ChatGPT-in-Chrome (the Codex chrome-control tool) **only** when the test case needs the user's own signed-in session, with per-use explicit consent; a failed driver launch is a tool failure to surface, never a license to switch surfaces |
| computer-use | **gated**: requires a concrete use case recorded in the project's `environment.md` **and** explicit user approval for the engagement; then the Codex computer-use tool, staffed by terra | none — an unmet gate is a hard capability gap; never fall back to the user's browser or desktop |
| imagegen | image-generation route — default the Codex system `imagegen` skill/tool | repo `codex-imagegen` skill through bounded Codex CLI |

Capabilities belong to harness/tool providers, never model rows. Resolve need → effect-verified provider → recorded fallback → eligible executor → model ranking. Installation alone is not reachability. Read the selected provider skill fully before use. For user-facing images, generation and taste review are separate stages.

## Resolve

- Issue dispatch requires groomed work type, surface/capabilities, coordination class/reason, and known uncertainty. Missing data stops dispatch. Record the route and upward successor before child/worktree creation.
- Pins short-circuit ranking: mechanical/bulk → sol; browser-use → Playwright-driving-Chrome scripts/terra (`agent-browser` only for interactive exploration), ChatGPT-in-Chrome only via the recorded user-session carve-out; computer-use → only through its approval gate. Imagegen selects its provider without pretending image access is a model trait.
- Otherwise apply required provider and taste ≥ 7 gates, then rank eligible reachable workers by intelligence, taste, cheaper cost. Opus is the verified taste-qualified Codex→Claude worker; a sibling-route failure removes that direction only and reruns resolution.
- Effort: dispatch at the model row's effort value; pure wait/relay and cron duty runs at low regardless of model. Effort never substitutes for a failed taste or capability gate.
- General/mechanical succession: sol → opus → sonnet → terra. UI/review: opus. Watcher/cron: terra → sol, wait/relay only. A missing capability provider reports a hard gap; do not relabel another tool or model as capable.

## Wake paths

Cheapest verified wake first; a model watcher only where nothing is tracked. Watchers wait/relay only.

| harness | tracked wake (preferred, no model) | watcher fallback |
|---|---|---|
| Codex (this harness) | none verified by default — setup probes; hold via a watched native subagent loop | Floor model wait/relay loop |
| Claude Code (sibling) | tracked background tasks / subagent completions re-invoke its session | Floor model, low effort |

Hold any out-of-band wait (review verdicts, merge watches) on the top verified row for the harness running the wait; Codex-led runs park the wait on a Floor-model wait/relay loop, never on the orchestrator.

## Mechanics

Use one orchestrator thread with watched native subagents; no fire-and-forget shells. Config: `~/.codex/config.toml` (`max_depth=3`, `max_threads=20`).

**The hiring orchestrator owns the worker's permission envelope, in both directions.** Whoever spawns a worker grants, in the dispatch command itself, every permission the job needs — prompt text never grants permissions; only flags and settings do. Machine policy default: **yolo both ways**, matching how the orchestrators themselves run. Hardening path (documented, not active): role-scoped envelopes — `--permission-mode acceptEdits --allowedTools …` for Claude builders, `--sandbox workspace-write` with explicit network config for Codex builders, read-only/default-deny for reviewers and checkers.

Codex→Claude runs only inside a watched native wrapper staffed by the Floor model — the cheapest native model the floor allows — and named for the external worker and task, such as `claude-opus:review-auth`. The parent owns the prompt, judgment, and effect verification; the wrapper only supervises the bounded process and relays its raw output and lifecycle status — it is **never repurposed to edit or build**; if the thread cap blocks a real worker, free a completed thread, queue, or report blocked. It runs, from inside the target worktree:

```
claude -p --model <verified-alias> --dangerously-skip-permissions '<self-contained prompt>' </dev/null
```

never adds `--bare`, and captures the durable result.

- **Effect-class probe first.** Before the first substantive dispatch on any cross-harness route, run a reversible probe matching the role's effect class: a one-line file write (then revert) for a builder, a read for a reviewer. Exit 0 with the effect denied quarantines the route *directionally* (build dead ≠ review dead) and reroutes immediately — never spend a full worker turn discovering a permission wall. A text-only echo probe verifies nothing about effects.
- **Session identity.** Capture the worker's session id at launch; resume by id, never `resume --last` — parallel wrappers collide on it and can silently resume a sibling's session.
- **Minimal context.** Spawn children with a self-contained task packet (issue, role, worktree, gate, expected return) — never full-history forks (`fork_turns="all"`).
- **Telemetry.** Record the spawned model, effort, role, route, and session id in the run-state spawn event and assert model+effort against the staffed role before dispatch; a mismatch is a dispatch blocker, not a note. Children inherit the picker's current model — verify the orchestrator's own model against the roster before any wave dispatch.

If native spawn cannot select or report the wrapper model, do not claim floor/cost compliance: use the observable wrapper, record the staffing gap, and keep that criterion red until the spawn seam is fixed.

Verified roster-name → CLI-alias mapping: `sonnet-5` → `sonnet`; `opus-4.8` → `opus`. Display names are never passed to the CLI without an alias probe. Route state is directional: effect-verified, intentionally disabled, or unavailable with a captured failure class.
