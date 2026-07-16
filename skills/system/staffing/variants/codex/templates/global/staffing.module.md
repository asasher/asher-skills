# Machine staffing — Codex

{{COMMON}}

## Models

| model | cost | intelligence | taste |
|---|---:|---:|---:|
| gpt-5.6-sol | 4 | 9 | 5 |
| gpt-5.6-terra | 6 | 5 | 3 |
| sonnet-5 | 5 | 5 | 5 |
| opus-4.8 | 3 | 7 | 7 |

The Codex models are coordinator-eligible through native agent threads. The Claude rows are effect-verified bounded worker routes, not coordinator-eligible until durable child ownership is separately proven. Fable is omitted until its CLI alias and requested effect are verified. Floor: gpt-5.6-terra for native Codex roles.

## Capability providers

| need | primary provider | fallback / hard edge |
|---|---|---|
| browser-use | machine `agent-browser` (isolated or headless profile), staffed by terra | ChatGPT-in-Chrome (`chrome:control-chrome`) **only** when the test case needs the user's own signed-in session, with per-use explicit consent; a failed `agent-browser` launch is a tool failure to surface, never a license to switch surfaces |
| computer-use | **gated**: requires a concrete use case recorded in the project's `environment.md` **and** explicit user approval for the engagement; then `computer-use:computer-use`, staffed by terra | none — an unmet gate is a hard capability gap; never fall back to the user's browser or desktop |
| imagegen | Codex system `imagegen` skill/tool | repo `codex-imagegen` skill through bounded Codex CLI |

Capabilities belong to harness/tool providers, never model rows. Resolve need → effect-verified provider → recorded fallback → eligible executor → model ranking. Installation alone is not reachability. Read the selected provider skill fully before use. For user-facing images, generation and taste review are separate stages.

## Resolve

- Issue dispatch requires groomed work type, surface/capabilities, coordination class/reason, and known uncertainty. Missing data stops dispatch. Record the route and upward successor before child/worktree creation.
- Pins short-circuit ranking: mechanical/bulk → sol; browser-use → `agent-browser`/terra, ChatGPT-in-Chrome only via the recorded user-session carve-out; computer-use → only through its approval gate. Imagegen selects its provider without pretending image access is a model trait.
- Otherwise apply required provider and taste ≥ 7 gates, then rank eligible reachable workers by intelligence, taste, cheaper cost. Opus is the verified taste-qualified Codex→Claude worker; a sibling-route failure removes that direction only and reruns resolution.
- General/mechanical succession: sol → opus → sonnet → terra. UI/review: opus. Watcher/cron: terra → sol, wait/relay only. A missing capability provider reports a hard gap; do not relabel another tool or model as capable.

## Mechanics

Use one orchestrator thread with watched native subagents; no fire-and-forget shells. Config: `~/.codex/config.toml` (`max_depth=3`, `max_threads=20`).

**The hiring orchestrator owns the worker's permission envelope, in both directions.** Whoever spawns a worker grants, in the dispatch command itself, every permission the job needs — prompt text never grants permissions; only flags and settings do. Current machine policy (Asher, plan #73): **yolo both ways for now**, matching how the orchestrators themselves run. Hardening path (documented, not active): role-scoped envelopes — `--permission-mode acceptEdits --allowedTools …` for Claude builders, `--sandbox workspace-write` with explicit network config for Codex builders, read-only/default-deny for reviewers and checkers.

Codex→Claude runs only inside a watched native wrapper staffed by the cheapest native model allowed by the current floor—`gpt-5.6-terra` on this roster—and named for the external worker and task, such as `claude-opus:review-auth`. The parent owns the prompt, judgment, and effect verification; the wrapper only supervises the bounded process and relays its raw output and lifecycle status — it is **never repurposed to edit or build**; if the thread cap blocks a real worker, free a completed thread, queue, or report blocked. It runs, from inside the target worktree:

```
claude -p --model <verified-alias> --dangerously-skip-permissions '<self-contained prompt>' </dev/null
```

never adds `--bare`, and captures the durable result.

- **Effect-class probe first.** Before the first substantive dispatch on any cross-harness route, run a reversible probe matching the role's effect class: a one-line file write (then revert) for a builder, a read for a reviewer. Exit 0 with the effect denied quarantines the route *directionally* (build dead ≠ review dead) and reroutes immediately — never spend a full worker turn discovering a permission wall. A text-only echo probe verifies nothing about effects.
- **Session identity.** Capture the worker's session id at launch; resume by id, never `resume --last` — parallel wrappers collide on it.
- **Minimal context.** Spawn children with a self-contained task packet (issue, role, worktree, gate, expected return) — never full-history forks (`fork_turns="all"`).
- **Telemetry.** Record the spawned model, effort, role, route, and session id in the run-state spawn event and assert model+effort against the staffed role before dispatch; a mismatch is a dispatch blocker, not a note. Children inherit the picker's current model — verify the orchestrator's own model against the roster before any wave dispatch.

If native spawn cannot select or report the wrapper model, do not claim floor/cost compliance: use the observable wrapper, record the staffing gap, and keep that criterion red until the spawn seam is fixed.

Verified roster-name → CLI-alias mapping: `sonnet-5` → `sonnet`; `opus-4.8` → `opus`. Display names are never passed to the CLI without an alias probe. Route state is directional: effect-verified, intentionally disabled, or unavailable with a captured failure class.
