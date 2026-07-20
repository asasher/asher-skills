# Machine staffing — Claude Code

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
| fable-5 | 1 | 9 | 9 | high |

Coordinator-eligible: fable-5, opus-4.8, sonnet-5 through native Agent/Workflow children. Floor: sonnet-5 Claude-side / gpt-5.6-terra Codex-side.

## Capability providers reachable from Claude Code

Claude Code has no native ChatGPT-in-Chrome, Computer Use, or image-generation provider. Each row is a
role slot with this machine's default binding; setup probes the default and asks the owner about gaps.

| need | reachable route (default binding) | fallback / hard edge |
|---|---|---|
| browser-use | isolated browser driver — default machine `agent-browser` (isolated or headless profile) | explicit Codex app handoff to ChatGPT-in-Chrome **only** when the test case needs the user's own signed-in session, with per-use explicit consent; unattended `codex exec` cannot supply it. A failed driver launch is a tool failure to surface, never a license to switch surfaces |
| computer-use | none in Claude Code | explicit Codex Computer Use handoff **only** behind its gate: a concrete use case recorded in the project's `environment.md` **and** explicit user approval for the engagement; otherwise a hard capability gap — never fall back to the user's browser or desktop |
| imagegen | image-generation route — default the installed repo `codex-imagegen` skill through bounded Codex CLI | explicit Codex app handoff to the system `imagegen` skill/tool |

Capabilities belong to harness/tool providers, never model rows. Resolve need → effect-verified provider → recorded fallback/handoff → eligible executor → model ranking. Installation alone is not reachability. Name the actual machine or Codex provider; never attribute its effect to Claude. For user-facing images, generation and taste review are separate stages.

## Resolve

- Issue dispatch requires groomed work type, surface/capabilities, coordination class/reason, and known uncertainty. Missing data stops dispatch. Record the route and upward successor before child/worktree creation.
- Routine coordinators resolve only over the native coordinator-eligible set; orchestrator-required work stays with the session orchestrator. Worker pins cannot add Codex routes to that set.
- Pins short-circuit ranking: mechanical/bulk → sol through Codex CLI. Capability work follows the provider table above; do not turn a provider into a model capability.
- Otherwise apply required provider and taste ≥ 7 gates, then rank eligible models by intelligence, taste, cheaper cost.
- Effort: dispatch at the model row's effort value; pure wait/relay and cron duty runs at low regardless of model. Effort never substitutes for a failed taste or capability gate.
- Succession: orchestrator fable → opus → sonnet; mechanical sol → fable → opus → sonnet; UI/review fable → opus; watcher/cron sonnet → fable → opus (Codex-side cron: terra). Watchers wait/relay only. A missing capability provider reports a hard gap.

## Wake paths

Cheapest verified wake first; a model watcher only where nothing is tracked. Watchers wait/relay only.

| harness | tracked wake (preferred, no model) | watcher fallback |
|---|---|---|
| Claude Code | background tasks, Agent/Workflow completions, Monitor conditions — completion re-invokes the session | Floor model, low effort |
| Codex CLI (sibling) | none verified by default — setup probes | Floor model wait/relay loop |

Hold any out-of-band wait (review verdicts, merge watches) on the top verified row for the harness running the wait: on Claude Code, a tracked background process whose exit wakes the session — no watcher model at all.

## Mechanics

Claude models use native Agent/Workflow. **Native wake paths are the default — do not poll where the harness tracks.** Tracked background tasks, subagent completions, and Monitor conditions re-invoke the session; a Claude-led run has a verified wake path natively and must not adopt bounded-polling machinery built for harnesses without wakeups. Only genuinely untracked waits (fire-and-forget shells, external CI, review verdicts) need an explicit owner, deadline, and wake source.

**The hiring orchestrator owns the worker's permission envelope, in both directions.** Whoever spawns a worker grants, in the dispatch command itself, every permission the job needs — prompt text never grants permissions. Machine policy default: **yolo both ways**, matching how the orchestrators themselves run. Hardening path (documented, not active): role-scoped envelopes — `--sandbox workspace-write` plus explicit network config for Codex builders, `--sandbox read-only` for reviewers.

Claude→Codex work uses a watched native wrapper staffed by the Floor model at low effort and named for the external model and task, such as `gpt-5.6-sol:inspect-lock`. The parent owns the prompt, judgment, and effect verification; the wrapper only supervises the bounded process and relays its raw output and lifecycle status — it is **never repurposed to edit or build**. Under an explicit generous timeout it runs, from inside the target worktree, with closed stdin and worktree isolation when parallel:

```
codex exec --cd <worktree> --sandbox danger-full-access '<self-contained prompt>' </dev/null
```

Never use `claude -p`.

- **Effect-class probe first.** Before the first substantive dispatch on any cross-harness route, run a reversible probe matching the role's effect class: a one-line file write (then revert) for a builder, a read for a reviewer. Exit 0 with the effect denied quarantines the route *directionally* and reroutes immediately — never spend a full worker turn discovering a permission wall.
- **Session identity.** Capture the codex session id at launch; resume by id, never `resume --last` — parallel wrappers collide on it and can silently resume a sibling's session.
- **Telemetry.** Record the spawned model, effort, role, route, and session id in the run-state spawn event and assert model+effort against the staffed role before dispatch; a mismatch is a dispatch blocker, not a note.
