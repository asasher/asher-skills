# To Thread

Interactive dispatch adapter for the outermost supervisor. T3-hosted providers create visible T3
threads through short-lived authenticated local HTTP; standalone Claude and Codex sessions retain their
native attach surfaces. The adapter uses a supplied directory exactly, defaults to the current model and
effort, and invokes the `worktree` sibling only when direct isolation is explicitly requested. A failed
turn start deletes its partially created T3 thread before the temporary credential is revoked.

## Dependency surface

- **Bundled:** `scripts/t3-thread.py`, `scripts/name-codex-thread.py`, and `evals/`.
- **Sibling (required, by name):** `worktree`.

## Provenance

No external sources. Each adapter's command shape was probed live against the locally installed T3
Code, Claude Code, and codex-cli (last full pass 2026-07); runtime compatibility is capability-tested
at use rather than version-pinned, so the installed CLI is always the ground truth.
