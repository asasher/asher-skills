# Playbook: Staffing

> **The sole authority for this repo's roster.** Resolution reads this file and nothing else — there is no
> machine-level staffing module and no bundled roster read at runtime. The `staffing` skill ships a *seed*
> that `staffing setup` reads once when writing this file; after that the seed is not consulted. Doctrine —
> how resolution ranks, how wake paths are chosen, the command shapes for cross-harness dispatch — lives in
> the skill's own references, not here. This file carries **data**.
>
> Read it before model choice, delegation, child/worktree creation, capability-provider work, watcher
> assignment, or route-loss fallback.

## Probe record — this file is machine-specific

| | |
|---|---|
| Probed on | `Ashers-MacBook-Pro` — arm64, macOS 26.5.1 |
| Probe date | 2026-07-26 |
| Claude Code CLI | 2.1.220 |
| Codex CLI | codex-cli 0.144.5 |

**On another machine these rows are stale.** The judgment numbers travel; reachability, aliases, and CLI
versions do not. A session whose machine does not match the row above re-runs `staffing setup` before
dispatching, and treats every reachability row below as unverified until it does. A stale row is worse than a
missing one: it resolves cleanly and fails at the moment of use.

This does not replace the effect-class probe required before a first cross-harness dispatch — it decides
whether the recorded state is worth trusting at all.

## Models

Judgment numbers, higher-is-better, harness-independent. Effort is the dispatch level for the row.

| model | cost | intelligence | taste | effort |
|---|---:|---:|---:|---|
| gpt-5.6-sol | 4 | 9 | 5 | high |
| gpt-5.6-terra | 6 | 5 | 3 | xhigh |
| sonnet-5 | 5 | 5 | 5 | high |
| opus-5 | 3 | 8 | 8 | high |
| fable-5 | 1 | 9 | 9 | high |

## Eligibility — which models may take which role, per harness

| model | from Claude Code | from Codex |
|---|---|---|
| fable-5 | coordinator-eligible (native Agent/Workflow) | bounded worker route |
| opus-5 | coordinator-eligible (native Agent/Workflow) | bounded worker route — the taste-qualified one |
| sonnet-5 | coordinator-eligible (native Agent/Workflow) | bounded worker route |
| gpt-5.6-sol | bounded worker route (`codex exec`) | coordinator-eligible (native agent threads) |
| gpt-5.6-terra | bounded worker route (`codex exec`) | coordinator-eligible (native agent threads) |

**Floor:** sonnet-5 for Claude-side roles, gpt-5.6-terra for Codex-side roles.

A bounded worker route is not coordinator-eligible: invocation is verified, durable child ownership is not.
Promoting one requires separately proving it can own a durable child and dispatch its worker stages.

**Succession** — orchestrator: fable-5 → opus-5 → sonnet-5. Mechanical: gpt-5.6-sol → fable-5 → opus-5 →
sonnet-5. UI/review: fable-5 → opus-5. Watcher/cron: sonnet-5 → fable-5 → opus-5 Claude-side, gpt-5.6-terra
Codex-side. Watchers wait and relay only.

**Pins** — mechanical/bulk work pins to gpt-5.6-sol through the Codex CLI.

## Capability providers, per harness

Capabilities belong to harness and tool providers, never to model rows. Installation is not reachability.

| need | from Claude Code | from Codex |
|---|---|---|
| browser-use | scripted **Playwright driving Chrome** — verification is a script with artifacts, headed or headless (headless Chrome launches only outside the command sandbox on this machine) | same, staffed by gpt-5.6-terra |
| computer-use | **none** — no native provider; handoff to the Codex provider only behind the gate below | `computer-use:computer-use`, staffed by gpt-5.6-terra, **gated** |
| imagegen | installed repo `codex-imagegen` skill through bounded Codex CLI | Codex system `imagegen` skill/tool, with the repo `codex-imagegen` skill as fallback |

**browser-use fallbacks and hard edges.** The machine `agent-browser` and harness-native web bindings have
proven unreliable — never the default, only for interactive exploration a script cannot serve. ChatGPT-in-Chrome
(`chrome:control-chrome` on the Codex side) is reachable **only** when the test case needs the user's own
signed-in session, with per-use explicit consent; an unattended `codex exec` cannot supply it. A failed driver
launch is a tool failure to surface, never a licence to switch surfaces.

**computer-use gate.** Requires both a concrete use case recorded in `environment.md` **and** explicit user
approval for the engagement. An unmet gate is a hard capability gap — never fall back to the user's browser or
desktop.

For user-facing images, generation and taste review are separate stages.

## Reachability — directional, effect-verified

Each direction carries its own state. A failure removes one direction only; never infer symmetry.

| direction | state | evidence (2026-07-26) | successor on loss |
|---|---|---|---|
| Claude Code → Codex | **effect-verified** | `codex exec -s read-only --skip-git-repo-check`, closed stdin, rc=0, probe string returned | none needed — native Claude models remain |
| Codex → Claude Code | **effect-verified** | nested probe: `codex exec -s danger-full-access` running `claude -p --model sonnet` with closed stdin, rc=0, probe string returned end to end | native Codex models; the direction is removed, the harness is not |

### CLI alias mapping — the roster names are not dispatch aliases

The installed Claude CLI **rejects every versioned roster name and accepts every bare name.** Verified across
the whole roster on claude 2.1.220:

| passed to `--model` | result |
|---|---|
| `sonnet-5`, `opus-5`, `fable-5` | rejected — "may not exist or you may not have access to it" |
| `sonnet`, `opus`, `fable` | accepted, probe string returned |

This is a general rule for this CLI version, not a per-model quirk: **strip the version suffix when a roster
name crosses into an executable `--model` argument.** A roster name written straight into a dispatch command
produces a route that resolves cleanly and fails at the moment of use.

## Wake paths — what is verified here

The rule for choosing a wake path is doctrine and lives in the skill; these are this machine's verified rows.

| harness | tracked wake (preferred, no model) | watcher fallback |
|---|---|---|
| Claude Code | background tasks, Agent/Workflow completions, Monitor conditions — completion re-invokes the session | sonnet-5, low effort |
| Codex CLI | none verified — `codex exec` children are bounded and untracked; hold via a watched native subagent loop | gpt-5.6-terra (cron: gpt-5.6-terra) |

Out-of-band waits (review verdicts, merge watches) hold on the top verified row for the harness running the
wait. On Claude Code that is a tracked background process whose verdict-coded exit wakes the session — no
watcher model at all.

## Permission envelope

The hiring orchestrator owns the worker's permission envelope in both directions: whoever spawns a worker
grants, in the dispatch command itself, every permission the job needs. Prompt text never grants permissions.

Machine policy: **yolo both ways for now**, matching how the orchestrators themselves run. Hardening path
(documented, not active): role-scoped envelopes — `--sandbox workspace-write` plus explicit network config for
Codex builders, `--sandbox read-only` for reviewers.

## Repo deltas

Two, and no others — no project floor, capability-provider, or succession override:

- **Probe evals run dual-executor** — a Claude subagent in-session plus gpt-5.6-sol via `codex exec`, per
  `probe-evals.md`. This repo's evals routinely shell out to Codex.
- **Skill design is orchestration-grade** — it stays with the most capable model in the session and is never
  delegated to the mechanical builder, whatever the general ranking would pick.

## Open

- `fable-5` passed its CLI alias and basic effect probe on 2026-07-26, so the Codex-side bounded worker route
  is now reachable — earlier records omitted it pending exactly this verification. It stays a bounded worker
  route, not coordinator-eligible, until durable child ownership is separately proven.
- Whether `staffing setup` records the three reachability states itself, rather than a human writing them
  here, is tracked separately.
