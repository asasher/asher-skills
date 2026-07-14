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

| need | primary provider | fallback |
|---|---|---|
| browser-use | `chrome:control-chrome` / ChatGPT-in-Chrome, staffed by terra | project-recorded `agent-browser` |
| computer-use | `computer-use:computer-use`, staffed by terra | none |
| imagegen | Codex system `imagegen` skill/tool | repo `codex-imagegen` skill through bounded Codex CLI |

Capabilities belong to harness/tool providers, never model rows. Resolve need → effect-verified provider → recorded fallback → eligible executor → model ranking. Installation alone is not reachability. Read the selected provider skill fully before use. For user-facing images, generation and taste review are separate stages.

## Resolve

- Issue dispatch requires groomed work type, surface/capabilities, coordination class/reason, and known uncertainty. Missing data stops dispatch. Record the route and upward successor before child/worktree creation.
- Pins short-circuit ranking: mechanical/bulk → sol; browser-use → Chrome/terra, then project `agent-browser`; computer-use → Computer Use/terra. Imagegen selects its provider without pretending image access is a model trait.
- Otherwise apply required provider and taste ≥ 7 gates, then rank eligible reachable workers by intelligence, taste, cheaper cost. Opus is the verified taste-qualified Codex→Claude worker; a sibling-route failure removes that direction only and reruns resolution.
- General/mechanical succession: sol → opus → sonnet → terra. UI/review: opus. Watcher/cron: terra → sol, wait/relay only. A missing capability provider reports a hard gap; do not relabel another tool or model as capable.

## Mechanics

Use one orchestrator thread with watched native subagents; no fire-and-forget shells. Config: `~/.codex/config.toml` (`max_depth=3`, `max_threads=20`).

Codex→Claude runs only inside a watched native wrapper staffed by the cheapest native model allowed by the current floor—`gpt-5.6-terra` on this roster—and named for the external worker and task, such as `claude-opus:review-auth`. The parent owns the prompt, judgment, and effect verification; the wrapper only supervises the bounded process and relays its raw output and lifecycle status. It runs `claude -p --model <verified-alias> '<self-contained prompt>' </dev/null`, never adds `--bare`, and captures the durable result.

If native spawn cannot select or report the wrapper model, do not claim floor/cost compliance: use the observable wrapper, record the staffing gap, and keep that criterion red until the spawn seam is fixed.

Verified roster-name → CLI-alias mapping: `sonnet-5` → `sonnet`; `opus-4.8` → `opus`. Display names are never passed to the CLI without an alias probe. Route state is directional: effect-verified, intentionally disabled, or unavailable with a captured failure class.
