---
name: to-thread
description: Spawn a named, interactive background session in the outermost harness and tell the user how to attach. Use when a unit of work should continue in its own attended session, including from T3 Code, Claude Code, or Codex.
argument-hint: "<name — initial prompt>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [worktree]
  optional: [plain-language]
---

# To Thread

Spawn one named, interactive session in the outermost harness, verify it is alive, and tell the user how to attach. The outermost interactive supervisor owns the session; nothing flows back to this one — outcomes land in the tracker.

## Shared contract — every route

- **Name** — short, human, specific (`shape-142-driver-payouts`, not `session-2`).
- **Prompt** — standalone. The thread sees none of this conversation: state the goal, inputs by path or ticket id, what done looks like, and any skill it should run.
- **Directory** — run in the supplied directory exactly; distinguish the registered project root from the working directory; do not infer a new worktree from edit intent. Isolation only when explicitly requested and no prepared directory was supplied: use the `worktree` sibling first and dispatch inside its returned path — the caller is provisional owner until spawn, the spawned thread then owns merge/cleanup, and its standalone prompt says so. Report the path and branch with the thread.
- **Model and effort** — the dispatching session's current model and effort, passed explicitly. The user never leaves their outermost harness — a thread is the user's own seat continuing elsewhere, so staffing is never consulted for threads; the roster staffs only unattended subagent work. A user-specified override wins.
- **Permission mode** — pass the mode selected for this session explicitly.
- **The dispatch declaration** — every spawn opens with a declaration in the transcript, posted before the call goes out: "Dispatching <work> — model <X>, effort <Y>, harness <Z>, deadline <absolute time>." A statement, never a question: the human can interrupt, nobody must approve, and the transcript is the audit trail. User-facing text follows the `plain-language` sibling.
- **Liveness before success** — a spawn reports success only when the thread is observably alive and attendable, never merely because the create command exited zero. Validate every identifier the route requires before create, or verify the thread's state briefly after start; a spawn that would fail asynchronously inside the app fails here, at the command line, instead. If the outermost harness has no attachable session surface, say so and hand the user the standalone prompt — a failed route never silently becomes a hidden thread elsewhere.
- **Attach is inspection** — attach-ability exists so the user can look in, not so anyone must attend; threads may run unattended with their outcomes landing in the tracker.
- **Report** — after a verified spawn, give the user the name/id, the attachment path, the exact directory, and the branch, whether the directory was prepared here or supplied by a composing workflow.

## Step 1 — detect the outermost harness

Detect from host context at runtime — never from recorded machine facts, which go stale and vary by machine. When system or runtime host metadata says this session runs inside T3 Code, T3 is outermost; the product-native `t3-code` MCP toolkit corroborates that for both Codex and Claude providers, while mere installation or reachability of a similarly named MCP server is not an ownership signal, and `T3_MCP_BEARER_TOKEN` additionally corroborates T3-hosted Codex but is not universal. Otherwise the provider harness is outermost: distinguish its CLI from its desktop app by how the user is actually attending this session. Never route by model name — a Codex or Claude provider running inside T3 always creates a T3 thread.

When the signals are ambiguous, ask the user which harness is outermost. One question beats a wrong guess that fails asynchronously in an app the user is not watching.

## Step 2 — load exactly one route

- On T3 Code as the outermost harness: read `reference/t3.md`.
- On Claude Code attended in a terminal: read `reference/claude-cli.md`.
- On Claude Desktop as the attended surface: read `reference/claude-desktop.md`.
- On Codex attended in a terminal: read `reference/codex-cli.md`.
- On the Codex desktop app as the attended surface: read `reference/codex-desktop.md`.

## Dependency surface

- **Bundled:** `reference/` (the five route files above); `scripts/t3-thread.py` (local T3 HTTP dispatch); `scripts/name-codex-thread.py` (Codex post-creation naming).
- **Sibling (required, by name):** `worktree` — explicit direct isolation; prepared directories from a composing workflow are used as supplied.
- **Sibling (optional, by name):** `plain-language` — the standard for the declaration and the report. Absent it, write plainly and say the standard was not loaded.
