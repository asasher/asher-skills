# Route: Codex CLI

Ground truth: the installed `codex` — flags drift between releases, so recheck `codex --help` if a flag misses. A CLI thread has a UUID and an optional name.

## Dispatch

1. Spawn detached in the resolved directory, capturing the first JSONL `thread.started` id:

   cd <directory> && codex exec --json -s <sandbox> -m <model> \
    -c model_reasoning_effort="<effort>" '<prompt>' > <log-file> 2>&1 &

2. Name it with `scripts/name-codex-thread.py <uuid> "<name>"`.

Never pass `--ephemeral`; it makes the thread unresumable.

## Liveness before success

The `thread.started` event in the log is the liveness signal: confirm it appeared and carries a thread id, and that the process is still running, before reporting success. A spawn whose log shows no `thread.started`, or an immediate error, is a failed dispatch reported now — never a name handed to the user for a thread that never lived.

## Report

Tell the user: `codex resume '<name>'` opens it for inspection; bare `codex resume` is the picker. When the user attends through the Codex desktop app instead, use the `codex-desktop.md` route — an exec-created thread is filtered from the app's surface.
