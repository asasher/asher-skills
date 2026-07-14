# Machine staffing — Claude Code

{{COMMON}}

## Models

| model | cost | intelligence | taste |
|---|---:|---:|---:|
| gpt-5.6-sol | 4 | 9 | 5 |
| gpt-5.6-terra | 6 | 5 | 3 |
| sonnet-5 | 5 | 5 | 5 |
| opus-4.8 | 3 | 7 | 7 |
| fable-5 | 1 | 9 | 9 |

Coordinator-eligible: fable-5, opus-4.8, sonnet-5 through native Agent/Workflow children. Floor: sonnet-5 Claude-side / gpt-5.6-terra Codex-side; never Haiku.

## Capability providers reachable from Claude Code

Claude Code has no native ChatGPT-in-Chrome, Computer Use, or image-generation provider.

| need | reachable route | fallback / hard edge |
|---|---|---|
| browser-use | project-recorded machine `agent-browser` | explicit Codex app handoff to `chrome:control-chrome`; unattended `codex exec` cannot supply it |
| computer-use | none in Claude Code | explicit Codex Computer Use handoff; no substitute |
| imagegen | installed repo `codex-imagegen` skill through bounded Codex CLI | explicit Codex app handoff to the system `imagegen` skill/tool |

Capabilities belong to harness/tool providers, never model rows. Resolve need → effect-verified provider → recorded fallback/handoff → eligible executor → model ranking. Installation alone is not reachability. Name the actual machine or Codex provider; never attribute its effect to Claude. For user-facing images, generation and taste review are separate stages.

## Resolve

- Issue dispatch requires groomed work type, surface/capabilities, coordination class/reason, and known uncertainty. Missing data stops dispatch. Record the route and upward successor before child/worktree creation.
- Routine coordinators resolve only over the native coordinator-eligible set; orchestrator-required work stays with the session orchestrator. Worker pins cannot add Codex routes to that set.
- Pins short-circuit ranking: mechanical/bulk → sol through Codex CLI. Capability work follows the provider table above; do not turn a provider into a model capability.
- Otherwise apply required provider and taste ≥ 7 gates, then rank eligible models by intelligence, taste, cheaper cost.
- Succession: orchestrator fable → opus → sonnet; mechanical sol → fable → opus → sonnet; UI/review fable → opus; watcher/cron sonnet → fable → opus (Codex-side cron: terra). Watchers wait/relay only. A missing capability provider reports a hard gap.

## Mechanics

Claude models use native Agent/Workflow. Claude→Codex work uses a watched native wrapper staffed by the cheapest Claude model allowed by the floor—`sonnet-low` on this roster—and named for the external model and task, such as `gpt-5.6-sol:inspect-lock`. The parent owns the prompt, judgment, and effect verification; the wrapper only supervises the bounded process and relays its raw output and lifecycle status. Under an explicit timeout it runs `codex exec` read-only for investigation or workspace-write for edits, with closed stdin and worktree isolation when parallel. Never use `claude -p`.
