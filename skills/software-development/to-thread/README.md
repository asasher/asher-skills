# To Thread

Interactive dispatch adapter for the outermost harness. The SKILL carries the shared contract — name, standalone prompt, exact directory, the dispatching session's model and effort (staffing is never consulted for threads), explicit permission mode, the dispatch declaration, and liveness-before-success: a spawn reports success only when the thread is observably alive and attendable. The outermost harness is detected from host context at runtime (asking the user when signals are ambiguous), then exactly one of five route files loads: T3 Code, Claude Code CLI, Claude Desktop (spawn via CLI, import stopped sessions via `claude://resume`), Codex CLI, or the Codex desktop app. The adapter uses a supplied directory exactly and invokes the `worktree` sibling only when direct isolation is explicitly requested. A failed turn start deletes its partially created T3 thread before the temporary credential is revoked.

## Dependency surface

Composes with the `worktree` sibling (optionally `writing-for-humans`); the five route files and dispatch scripts are bundled.

## Provenance

No external sources. Runtime compatibility is capability-tested at use rather than version-pinned, so the installed CLI is always the ground truth.
