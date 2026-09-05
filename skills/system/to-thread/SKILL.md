---
name: to-thread
description: Start one named thread in the user’s harness, optionally preparing or attaching its Git worktree first.
metadata:
  optional: [writing-for-humans]
---

# To thread

Start one thread, verify it is running and attendable, and report how to attach. Outcomes belong on the ticket; no result flows back to this session.

## Prepare

Take a self-contained prompt, ticket or task identity, model/effort, deadline when supplied, and directory. Preserve the user's harness and selected permission mode. Default to this session's model and effort; user overrides win.

For shaping or building, require a secondary worktree on the work branch. If none is supplied, or the supplied directory is the primary checkout, use [worktree preparation](reference/worktrees.md) with the decided branch and base before spawning. Validate a supplied directory against the intended branch and live ownership too. A prepared directory is passed exactly; add no harness-native isolation. The originating session hands off before editing.

## Dispatch

Identify the outermost harness from current runtime signals, not the model name or an installed tool alone. T3 host metadata or this session's T3 context establishes T3 ownership. Otherwise distinguish the provider's CLI from its desktop app. Ask only if ownership remains ambiguous.

Load one route:

- T3 Code: [T3](reference/t3.md).
- Claude in a terminal: [Claude CLI](reference/claude-cli.md).
- Claude Desktop: [Claude Desktop](reference/claude-desktop.md).
- Codex in a terminal: [Codex CLI](reference/codex-cli.md).
- Codex desktop app: [Codex desktop](reference/codex-desktop.md).

State the task, model, effort, harness, directory, and deadline before dispatch. Pass the prompt, selected permissions, and directory through the route. Declare success only after its liveness check passes. If no attendable route exists, report the blocker and retain the prepared work; do not build in the primary checkout as a fallback.

Return the thread id/name, attachment route, branch, and directory. On failure, establish whether a worker started before releasing ownership. Preserve work for recovery. Use `writing-for-humans` when available.
