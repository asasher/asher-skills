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

No external sources. T3 Code 0.0.30, Claude Code 2.1.220, and codex-cli 0.144.5 were the latest live
probes for their respective command shapes; runtime compatibility is capability-tested rather than
version-pinned.
