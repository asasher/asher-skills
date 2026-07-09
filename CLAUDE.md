# CLAUDE.md

Read `AGENTS.md` first — repo layout, conventions, and the pointer to `docs/patterns/` all live there.
This file adds only what applies when the harness is Claude Code.

## Staffing

Rankings, higher = better. Cost reflects what this machine's owner actually pays, not list price.
Intelligence is how hard a problem you can hand the model unsupervised. Taste covers UI/UX, code quality,
API design, and copy.

| model    | cost | intelligence | taste |
|----------|------|--------------|-------|
| gpt-5.5  | 7    | 8            | 5     |
| sonnet-5 | 5    | 5            | 7     |
| opus-4.8 | 4    | 7            | 8     |
| fable-5  | 2    | 9            | 9     |

How to apply:

- These are defaults, not limits. Standing permission to override: if a cheaper model's output doesn't meet
  the bar, rerun with a smarter model without asking. Judge the output, not the price tag.
- Cost is a tie-breaker only; when axes conflict for anything that ships, intelligence > taste > cost.
- Mechanical work (clear-spec implementation, bulk edits, research fan-outs, eval executor runs): gpt-5.5
  via the Codex CLI. This repo's evals routinely shell out to Codex.
- Anything user-facing (UI, copy, API design) needs taste ≥ 7.
- Skill reviews and probe grading: fable-5 or opus-4.8, optionally gpt-5.5 as an extra independent
  perspective.
- Orchestration, skill design, and hard diagnosis: the most capable model in the session.
- Never use Haiku.

Mechanics:

- gpt-5.5 is reachable only through the Codex CLI: `codex exec -s read-only --skip-git-repo-check` for
  investigation/review/eval-executor runs (`-c tools.web_search=true -o <outfile>` for research);
  `-s workspace-write` when it must edit. Give it a self-contained prompt; run long jobs in the background
  with an explicit timeout and poll the outfile.
- Claude participants (subagents, eval executors, reviewers) run **in-session** via the Agent tool — never
  `claude -p` / `claude --print`, which authenticates as a separate metered client. Codex CLI is fine
  because it bills to its own subscription.
- Research and bulk background fan-outs go to `codex exec`, not Fable subagent fleets — Fable fan-outs
  burn session limits fast.
