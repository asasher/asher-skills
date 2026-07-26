#!/bin/sh
# Dual-executor probe run, Codex direction (docs/agents/probe-evals.md; staffing repo delta).
DIR=/Users/asher/.claude/worktrees/asher-skills/agent-aa633cd21d16520f2/backlog-workspace/eval-runs/2026-07-26-teardown-sweep
codex exec -s read-only --skip-git-repo-check -m gpt-5.6-sol "$(cat "$DIR/prompt.md")" > "$DIR/run-codex-gpt-5.6-sol.txt" 2>&1
echo "exit: $?"
