# #178 stage-ledger probes — verdict table

Affected-probe runs per `docs/agents/probe-evals.md` (dual-executor: in-session Claude subagent + gpt-5.6-sol via `codex exec -s read-only`), graded against the answer keys in each skill's `evals/probes.md`. Key written before any runs; both keys cite the exact new sentences. Red state before the change: `grep -rni "token\|ledger\|quota\|cost"` over both skill directories exited 1 (zero matches), so every probe below was unanswerable from the prior sources.

| Probe | Key criterion | Claude executor | Codex executor (gpt-5.6-sol) |
| --- | --- | --- | --- |
| build P9 (ledger honesty) | `unreported` row — never estimated, never dropped; ledger handed to step 5's evidence dispatch | **Pass** (`claude-build-P9.md`) | **Pass** (`codex-build-P9.txt`) |
| prove-your-work P6 (cost rows) | No reconstruction — rows stay `unreported`; "an estimated or reconstructed figure is padding, not accounting" | **Pass** (`claude-prove-P6.md`) | **Pass** (`codex-prove-P6.txt`) |

Result: 2/2 probes, 2/2 executors — pass.

Untouched probes (build P1–P8, prove-your-work P1–P5) cite sentences this change did not edit; the additive edits left every previously cited sentence byte-identical (verified by inspection of the diff), so their keys remain valid without a re-run.

Executor-reported usage: Claude P9 23,886 tokens; Claude P6 23,572 tokens; Codex P9 13,506 tokens; Codex P6 13,925 tokens.
