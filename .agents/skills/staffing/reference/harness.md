# Codex harness mechanics

Global pointer: `~/.codex/AGENTS.md` § Staffing. Deferred module:
`~/.codex/asher-skills/staffing.md`.

Native Codex work uses watched native agent threads. Codex→Claude work runs only inside a watched Codex
wrapper named for the external Claude model and task, such as `claude-opus:review-auth`. Staff that relay with
the cheapest native Codex model allowed by the floor. It runs bounded
`claude -p --model <verified-alias> '<self-contained prompt>' </dev/null`, never adds `--bare`, and returns
raw output plus separate lifecycle status.

Probe every roster-name→CLI-alias mapping after CLI upgrades; never pass a display name without an alias
probe. If native spawn cannot select or report the wrapper model, the route may remain observable and usable,
but floor/cost compliance remains unproven and must be reported red.

ChatGPT-in-Chrome, Computer Use, and native Imagegen are Codex harness/tool providers, not model traits.
Record their effect-probed routes and project fallbacks before ranking an eligible executor.
