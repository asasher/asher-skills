# Playbook: Staffing

> **The sole authority for this repo's roster.** Resolution reads this file plus its machine-local
> overlay and nothing else — there is no machine-level staffing module and no bundled roster read at
> runtime. The `staffing` skill ships a *seed* that `staffing setup` reads once when writing this file;
> after that the seed is not consulted. Doctrine — how resolution ranks, how wake paths are chosen, the
> command shapes for cross-harness dispatch — lives in the skill's own references, not here. This file
> carries **data**.
>
> Read it before model choice, delegation, child/worktree creation, capability-provider work, watcher assignment, or route-loss fallback.

## Machine record — the overlay

<!-- machine-local: docs/agents/local/staffing.md setup="staffing setup" -->

Everything machine-probed lives in the gitignored overlay declared above, opening with the stamp of
the machine that probed it: the probe record, per-harness eligibility observations,
capability-provider rows, directional reachability and its evidence, the CLI alias mapping, wake
paths, and the permission envelope. Judgment numbers travel between machines; probe results do not.
When the overlay is missing, or its stamp names another machine, run `staffing setup` before
dispatching, and treat every reachability row as unverified until it completes. This does not replace
the effect-class probe required before a first cross-harness dispatch — it decides whether recorded
state is worth trusting at all.

## Models

Judgment numbers, higher-is-better, harness-independent. Effort is the dispatch level for the row.

| model         | cost | intelligence | taste | effort |
| ------------- | ---: | -----------: | ----: | ------ |
| gpt-5.6-sol   |    4 |            9 |     5 | high   |
| gpt-5.6-terra |    6 |            5 |     3 | xhigh  |
| sonnet-5      |    5 |            5 |     5 | high   |
| opus-5        |    3 |            8 |     8 | high   |
| fable-5       |    1 |            9 |     9 | high   |

**Floor:** sonnet-5 for Claude-side roles, gpt-5.6-terra for Codex-side roles.

**Succession** — orchestrator: fable-5 → opus-5 → sonnet-5. Mechanical: gpt-5.6-sol → fable-5 → opus-5 →
sonnet-5. UI/review: fable-5 → opus-5. Watcher/cron: sonnet-5 → fable-5 → opus-5 Claude-side, gpt-5.6-terra
Codex-side.

**Pins** — mechanical/bulk work pins to gpt-5.6-sol through the Codex CLI.

Which models are actually reachable from which harness, and by what route, is a machine fact — the
overlay's eligibility and reachability rows decide it.

## Repo deltas

Two, and no others — no project floor, capability-provider, or succession override:

- **Probe evals run dual-executor** — a Claude subagent in-session plus gpt-5.6-sol via `codex exec`, per
  `probe-evals.md`. This repo's evals routinely shell out to Codex.
- **Skill design is orchestration-grade** — it stays with the most capable model in the session and is never
  delegated to the mechanical builder, whatever the general ranking would pick.
