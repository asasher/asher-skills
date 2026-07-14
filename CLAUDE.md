# CLAUDE.md

@AGENTS.md

The import above pulls in the harness-neutral base — layout, vocabulary, conventions, the skill map —
at session start (Claude Code never reads `AGENTS.md` on its own). This file adds only what applies when
the harness is Claude Code.

## Staffing

Load the harness-specific global module through `~/.claude/CLAUDE.md` § Staffing, then apply only the deltas
below. Codex does the same through `~/.codex/AGENTS.md`.

This repo's deltas:

- Probe evals run **dual-executor**: a Claude subagent in-session plus gpt-5.6-sol via `codex exec`
  (`docs/agents/probe-evals.md`) — this repo's evals routinely shell out to Codex.
- "Skill design" counts as orchestration-grade work here: it stays with the most capable model in the
  session, never delegated to the mechanical builder.
