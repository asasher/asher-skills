# CLAUDE.md

Read `AGENTS.md` first — repo layout, conventions, and the pointer to `docs/patterns/` all live there.
This file adds only what applies when the harness is Claude Code.

## Staffing

Rankings, higher = better. Cost reflects what this machine's owner actually pays, not list price.
Intelligence is how hard a problem you can hand the model unsupervised. Taste covers UI/UX, code quality,
API design, and copy.

| model         | cost | intelligence | taste |
|---------------|------|--------------|-------|
| gpt-5.6-sol   | 4    | 9            | 5     |
| gpt-5.6-terra | 6    | 5            | 3     |
| sonnet-5      | 5    | 5            | 5     |
| opus-4.8      | 3    | 7            | 7     |
| fable-5       | 1    | 9            | 9     |

Capability pins — gates checked before any ranking (a task needing the capability goes to the pinned model;
the rankings never override a pin):

| capability   | pinned model  | via                          |
|--------------|---------------|------------------------------|
| browser-use  | gpt-5.6-terra | the Codex computer-use client |
| computer-use | gpt-5.6-terra | the Codex computer-use client |

(Claude-side headless Chrome is blocked on this machine, so browser work routes through Codex too.)

How to apply:

- These are defaults, not limits. Standing permission to override: if a cheaper model's output doesn't meet
  the bar, rerun with a smarter model without asking. Judge the output, not the price tag.
- Cost is a tie-breaker only; when axes conflict for anything that ships, intelligence > taste > cost.
- Mechanical work (clear-spec implementation, bulk edits, research fan-outs, eval executor runs):
  gpt-5.6-sol via the Codex CLI. This repo's evals routinely shell out to Codex.
- Anything user-facing (UI, copy, API design) needs taste ≥ 7: fable-5 or opus-4.8.
- Skill reviews and probe grading: fable-5 or opus-4.8, optionally gpt-5.6-sol as an extra independent
  perspective.
- Orchestration, skill design, and hard diagnosis: the most capable model in the session.
- Watcher/cron duty (verdict watches, PR-merge watches, scheduled check-ins): sonnet-5 in-session;
  gpt-5.6-terra for Codex-side scheduled jobs. Watchers only wait and relay — judgment escalates to the
  orchestrator.
- Floor — the cheapest class anything may staff at: sonnet-5 (Claude-side) or gpt-5.6-terra (Codex-side).
  Never use Haiku.

Mechanics:

- gpt-5.6-sol/terra are reachable only through the Codex CLI: `codex exec -s read-only
  --skip-git-repo-check -m <model>` for investigation/review/eval-executor runs
  (`-c tools.web_search=true -o <outfile>` for research); `-s workspace-write` when it must edit. Give it a
  self-contained prompt.
- **One thread pattern everywhere: orchestrator + subagents.** Every delegated thread — Claude or Codex —
  runs as a subagent the orchestrator watches; completion wakes the orchestrator. From Claude Code, that is
  the Agent tool; a Codex thread is held by a thin wrapper subagent (floor class, low effort, labeled
  `gpt-5.6-sol:…`) that composes the self-contained codex prompt, runs `codex exec` via Bash, and returns
  the report. A Codex-driven orchestrator uses Codex's native agent threads the same way. No raw
  fire-and-forget background shells for delegated work.
- Claude participants (subagents, eval executors, reviewers) run **in-session** via the Agent tool — never
  `claude -p` / `claude --print`, which authenticates as a separate metered client. Codex CLI is fine
  because it bills to its own subscription.
- Research and bulk background fan-outs go to `codex exec`, not Fable subagent fleets — Fable fan-outs
  burn session limits fast.
