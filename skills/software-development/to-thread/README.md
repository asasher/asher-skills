# To Thread

Interactive dispatch adapter for the outermost harness. The SKILL carries the shared contract — name, standalone prompt, exact directory, the dispatching session's model and effort (staffing is never consulted for threads), explicit permission mode, the dispatch declaration, and liveness-before-success: a spawn reports success only when the thread is observably alive and attendable. The outermost harness is detected from host context at runtime (asking the user when signals are ambiguous), then exactly one of five route files loads: T3 Code, Claude Code CLI, Claude Desktop (spawn via CLI, import stopped sessions via `claude://resume`), Codex CLI, or the Codex desktop app. The adapter uses a supplied directory exactly and invokes the `worktree` sibling only when direct isolation is explicitly requested. A failed turn start deletes its partially created T3 thread before the temporary credential is revoked.

## Dependency surface

- **Bundled:** `reference/` (five route files), `scripts/t3-thread.py`, `scripts/name-codex-thread.py`, and `evals/`.
- **Sibling (required, by name):** `worktree`.
- **Sibling (optional, by name):** `plain-language` — the standard for the declaration and the report.

## Provenance

No external sources. Runtime compatibility is capability-tested at use rather than version-pinned, so the installed CLI is always the ground truth.
