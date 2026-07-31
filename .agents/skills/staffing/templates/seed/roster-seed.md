# Roster seed — Codex

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

The Codex models are coordinator-eligible through native agent threads. The Claude rows are bounded worker routes for the audit to effect-verify, not coordinator-eligible until durable child ownership is separately proven. Add a fable-5 row only after its CLI alias and requested effect are verified on this machine. Floor: gpt-5.6-terra for native Codex roles.

## Capability providers

Each row is a role slot with a suggested default binding; setup probes that default on the target machine and asks the owner about gaps. Nothing here is a verified route until the audit says so.

| need | primary provider (default binding) | fallback / hard edge |
| --- | --- | --- |
| browser-use | scripted **Playwright driving Chrome**, staffed by terra — verification is a script with artifacts, headed or headless | machine `agent-browser` and harness-native web bindings have proven unreliable — never the default, only for interactive exploration a script cannot serve; ChatGPT-in-Chrome (the Codex chrome-control tool) **only** when the test case needs the user's own signed-in session, with per-use explicit consent; a failed driver launch is a tool failure to surface, never a license to switch surfaces |
| computer-use | **gated**: requires a concrete use case recorded in the project's `environment.md` **and** explicit user approval for the engagement; then the Codex computer-use tool, staffed by terra | none — an unmet gate is a hard capability gap; never fall back to the user's browser or desktop |
| imagegen | image-generation route — default the Codex system `imagegen` skill/tool | repo `codex-imagegen` skill through bounded Codex CLI |

## Pins and succession

Seed values — setup keeps only what the audit found reachable.

- Pins short-circuit ranking: mechanical/bulk → sol; browser-use → Playwright-driving-Chrome scripts/terra (`agent-browser` only for interactive exploration), ChatGPT-in-Chrome only via the recorded user-session carve-out; computer-use → only through its approval gate. Imagegen selects its provider without pretending image access is a model trait.
- General/mechanical succession: sol → opus → sonnet → terra. UI/review: opus. Watcher/cron: terra → sol, wait/relay only. A missing capability provider reports a hard gap; do not relabel another tool or model as capable.

## Wake paths

| harness | tracked wake (preferred, no model) | watcher fallback |
| --- | --- | --- |
| Codex (this harness) | none verified by default — setup probes; hold via a watched native subagent loop | Floor model wait/relay loop |
| Claude Code (sibling) | tracked background tasks / subagent completions re-invoke its session | Floor model, low effort |
