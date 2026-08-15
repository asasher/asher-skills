# Route: Codex desktop app

When the user attends through the Codex desktop app, create the thread app-natively so it appears on the app's surface: an exec-created CLI thread is filtered from it.

## Dispatch

Create via the Codex app-server sequence, in order:

1. `thread/start` — in the resolved directory, with the dispatching session's model, effort, and permission mode.
2. `thread/name/set` — apply the supplied name.
3. `turn/start` — the standalone prompt as the first turn.

## Liveness before success

Report success only when the sequence completed and the turn is observably running — the named thread visible on the app's surface with its first turn started. A create that succeeded but whose turn never started is a failed dispatch: report it at the command line rather than leaving a dead thread in the user's sidebar.

## Report

Tell the user the thread's name and that it is open in the Codex desktop app's thread list, running in the reported directory and branch.
