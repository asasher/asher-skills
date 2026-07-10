# CLAUDE.md

@AGENTS.md

The import above pulls in the harness-neutral base — layout, vocabulary, conventions, the skill map —
at session start (Claude Code never reads `AGENTS.md` on its own). This file adds only what applies when
the harness is Claude Code.

## Staffing

The machine roster — rankings, pins, routing, floor, mechanics — is the **global base** in
`~/.claude/CLAUDE.md` § Staffing (Codex sessions read the filtered layer in `~/.codex/AGENTS.md`), owned by
the `staffing` skill. Resolve staffing questions against the base plus the deltas below; anything not named
here is inherited from the base unchanged.

This repo's deltas:

- Probe evals run **dual-executor**: a Claude subagent in-session plus gpt-5.6-sol via `codex exec`
  (`docs/agents/probe-evals.md`) — this repo's evals routinely shell out to Codex.
- "Skill design" counts as orchestration-grade work here: it stays with the most capable model in the
  session, never delegated to the mechanical builder.
- The compiled per-role roster for the backlog loop lives in `docs/agents/environment.md` § Model staffing.
