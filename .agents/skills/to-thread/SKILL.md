---
name: to-thread
description: Spawn a named, interactive, harness-native background session seeded with a standalone prompt, and tell the user how to attach. Use when a unit of work should continue in its own session that the user attends.
argument-hint: "<name — initial prompt>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: []
---

# To Thread

Spawn one background session for one unit of work, detached: the spawn returns immediately and the
session runs under the harness's own supervisor, not under this one. Nothing flows back — the user
attends the thread. Report status only when asked, via the harness's listing commands.

## The spec of a thread

- **Name** — short, human, specific (`shape-142-driver-payouts`, not `session-2`). The name is how the
  user finds it in a list of twenty.
- **Prompt** — standalone. The thread sees nothing of this conversation: state the goal, reference
  material by path or ticket id, say what done looks like, and name any skill the thread should run.
- **Directory** — the project the work belongs to; the spawn directory is the session's permanent home.
- **Model, effort, and permission mode** — this session's own, passed explicitly, unless told otherwise.
- **Isolation** — a thread that will edit a repo this session or another live thread is also editing gets
  its own worktree.

## Claude Code

Ground truth: claude 2.1.216 — recheck `claude --help` if a flag misses.

    cd <dir> && claude --bg -n "<name>" --model <model> --effort <level> \
      --permission-mode <mode> [-w] "<prompt>"

Returns immediately, printing `backgrounded · <id> · <name>`. `-w` gives the session its own worktree.
Tell the user: `claude agents` lists everything (Enter attaches; Space peeks and replies without
attaching); `claude attach <id>` opens one in this terminal; the session also appears on claude.ai/code
and in the Claude mobile app.

## Codex

Ground truth: codex-cli 0.144.5 — recheck `codex --help` if a flag misses. A thread has a UUID and an
optional name; no flag names it at creation, so create, then name:

1. Spawn detached, capturing the id — the first JSONL event is
   `{"type":"thread.started","thread_id":"<uuid>"}`:

       cd <dir> && codex exec --json -s workspace-write -m <model> \
         -c model_reasoning_effort="<effort>" '<prompt>' > <log-file> 2>&1 &

2. Name it: `scripts/name-codex-thread.py <uuid> "<name>"` — a one-shot `codex app-server` JSON-RPC
   `thread/name/set` call.
3. Tell the user: `codex resume '<name>'` opens it in a terminal; bare `codex resume` is the picker
   (`--all --include-non-interactive` widens it to every thread).

Never pass `--ephemeral` — it makes the thread unresumable. Exec-created threads are filtered out of the
Codex desktop app's default thread list; when the user attends via the app, create app-natively instead —
app-server `thread/start` → `thread/name/set` → `turn/start` (the prompt goes in the turn) against
`codex app-server daemon` — and say the thread lives in the app's list.

## Degrade

A harness with no attachable background sessions: say so, and hand the user the composed prompt to start
the session themselves.
