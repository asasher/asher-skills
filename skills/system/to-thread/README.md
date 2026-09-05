# To Thread

Interactive dispatch adapter for the outermost harness: detects it, loads one of five routes (T3 Code, Claude Code CLI, Claude Desktop, Codex CLI, Codex desktop app), and reports success only on liveness. `SKILL.md` carries the shared contract.

## Dependency surface

Composes with the optional `worktree` and `writing-for-humans` siblings; the five route files and dispatch scripts are bundled.

## Provenance

No external sources. Runtime compatibility is capability-tested at use rather than version-pinned, so the installed CLI is always the ground truth.
