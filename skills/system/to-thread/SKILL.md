---
name: to-thread
description: Spawn a named session in the outermost harness. Use when a unit of work should continue in its own attended session from T3 Code, Claude Code, or Codex.
metadata:
  requires: [worktree]
  optional: [writing-for-humans]
---

# To Thread

Spawn one named, interactive session in the outermost harness, verify it is alive, and tell the user how to attach. The outermost harness owns the session; nothing flows back to this one, outcomes land in the tracker.

## Shared contract — every route

- **Name** — short, human, specific (`shape-142-driver-payouts`, not `session-2`).
- **Prompt** — standalone. The thread sees none of this conversation: state the goal, inputs by path or ticket id, what done looks like, and any skill it should run.
- **Directory** — run in the supplied directory exactly. Isolation only when explicitly requested and no prepared directory was supplied: use the `worktree` sibling first and dispatch inside its returned path — the caller is provisional owner until spawn, the spawned thread then owns merge/cleanup, and its standalone prompt says so.
- **Model and effort** — the dispatching session's current model and effort, passed explicitly. The user never leaves their outermost harness — a thread is the user's own seat continuing elsewhere, so staffing is never consulted for threads; the roster staffs only unattended subagent work. A user-specified override wins.
- **Permission mode** — pass the mode selected for this session explicitly.
- **The dispatch declaration** — every spawn opens with a declaration in the transcript, posted before the call goes out: "Dispatching <work> — model <X>, effort <Y>, harness <Z>, deadline <absolute time>." The deadline comes from the composing workflow (a build claim, for example); on a direct invocation that supplies none, omit it. A statement, never a question: the human can interrupt, nobody must approve, and the transcript is the audit trail. User-facing text — the declaration and the report — follows the `writing-for-humans` sibling; absent it, write plainly and say the standard was not loaded.
- **Liveness before success** — a spawn reports success only when the thread is observably alive and attendable, never merely because the create command exited zero. Fail fast: surface at dispatch what would otherwise fail async in-app — each route file names the observable signal. If the outermost harness has no attachable session surface, say so and hand the user the standalone prompt.
- **Attach is inspection** — attach-ability exists so the user can look in, not so anyone must attend; threads may run unattended.
- **Report** — after a verified spawn, give the user the name/id, the attachment path, the exact directory, and the branch, whether the directory was prepared here or supplied by a composing workflow.

## Step 1 — detect the outermost harness

Detect from host context at runtime — never from recorded machine facts, which go stale and vary by machine.

Signals that T3 is outermost:

- System or runtime host metadata says this session runs inside T3 Code.
- A call to the `t3-code` MCP server reports this session's own tab or session context — for both Codex and Claude providers.
- `T3_MCP_BEARER_TOKEN` corroborates T3-hosted Codex, but is not universal.
- The T3 runtime file is present under the T3 base dir (default `~/.t3`).

Non-signals:

- Mere installation or reachability of the `t3-code` MCP server; only the signals above show ownership.
- The model name — a Codex or Claude provider running inside T3 always creates a T3 thread.

Otherwise the provider harness is outermost: distinguish its CLI from its desktop app by how the user is actually attending this session.

When the signals are ambiguous, ask the user which harness is outermost. One question beats a wrong guess that fails async in an app the user is not watching.

## Step 2 — load exactly one route

- On T3 Code as the outermost harness: read `reference/t3.md`.
- On Claude Code attended in a terminal: read `reference/claude-cli.md`.
- On Claude Desktop as the attended surface: read `reference/claude-desktop.md`.
- On Codex attended in a terminal: read `reference/codex-cli.md`.
- On the Codex desktop app as the attended surface: read `reference/codex-desktop.md`.
