# Roster seed — Claude Code

> **A seed, not a roster.** `staffing setup` reads this file once, when it writes the project's staffing playbook, and never again — resolution reads the playbook alone. Values here are starting points for what cannot be probed (the judgment numbers); everything else is replaced by what the machine audit actually verified. Never install a row this machine failed to verify, and never resolve from this file at runtime.
>
> Doctrine is not seeded: ranking rules live in the skill's routing reference, harness command shapes and wake mechanics in its compiled harness mechanics. This file carries data only.

## Models

Seed defaults — setup verifies each row against this machine (unreachable rows are pruned, missing reachable models are added) and the owner tunes the judgment numbers. Effort is the model's default dispatch level where the harness exposes one.

| model         | cost | intelligence | taste | effort |
| ------------- | ---: | -----------: | ----: | ------ |
| gpt-5.6-sol   |    4 |            9 |     5 | high   |
| gpt-5.6-terra |    6 |            5 |     3 | xhigh  |
| sonnet-5      |    5 |            5 |     5 | high   |
| opus-5        |    3 |            8 |     8 | high   |
| fable-5       |    1 |            9 |     9 | high   |

Coordinator-eligible: fable-5, opus-5, sonnet-5 through native Agent/Workflow children. Floor: sonnet-5 Claude-side / gpt-5.6-terra Codex-side.

## Capability providers reachable from Claude Code

Claude Code has no native ChatGPT-in-Chrome, Computer Use, or image-generation provider. Each row is a role slot with a suggested default binding; setup probes that default on the target machine and asks the owner about gaps. Nothing here is a verified route until the audit says so.

| need | reachable route (default binding) | fallback / hard edge |
| --- | --- | --- |
| browser-use | scripted **Playwright driving Chrome** — verification is a script with artifacts, headed or headless; whether headless launches inside the command sandbox is machine-specific, so probe it | machine `agent-browser` and harness-native web bindings have proven unreliable — never the default, only for interactive exploration a script cannot serve; explicit Codex app handoff to ChatGPT-in-Chrome **only** when the test case needs the user's own signed-in session, with per-use explicit consent; unattended `codex exec` cannot supply it. A failed driver launch is a tool failure to surface, never a license to switch surfaces |
| computer-use | none in Claude Code | explicit Codex Computer Use handoff **only** behind its gate: a concrete use case recorded in the project's `environment.md` **and** explicit user approval for the engagement; otherwise a hard capability gap — never fall back to the user's browser or desktop |
| imagegen | image-generation route — default the installed repo `codex-imagegen` skill through bounded Codex CLI | explicit Codex app handoff to the system `imagegen` skill/tool |

## Pins and succession

Seed values — setup keeps only what the audit found reachable.

- Pins short-circuit ranking: mechanical/bulk → sol through Codex CLI. Capability work follows the provider table above; do not turn a provider into a model capability.
- Succession: orchestrator fable → opus → sonnet; mechanical sol → fable → opus → sonnet; UI/review fable → opus; watcher/cron sonnet → fable → opus (Codex-side cron: terra). Watchers wait/relay only. A missing capability provider reports a hard gap.

## Wake paths

| harness | tracked wake (preferred, no model) | watcher (last resort) |
| --- | --- | --- |
| Claude Code | background tasks, Agent/Workflow completions, Monitor conditions — completion re-invokes the session | Floor model, low effort |
| Codex CLI (sibling) | none verified by default — setup probes | Floor model wait/relay loop |

A harness-native timed wake outranks the watcher wherever a timer facility is verified — rung order in the compiled harness mechanics.
