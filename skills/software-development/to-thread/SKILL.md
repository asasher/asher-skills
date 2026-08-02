---
name: to-thread
description: Spawn a named, interactive background session in the outermost harness and tell the user how to attach. Use when a unit of work should continue in its own attended session, including from T3 Code, Claude Code, or Codex.
argument-hint: "<name — initial prompt>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [worktree]
  optional: []
---

# To Thread

Spawn one attended session, detached: creation returns immediately and the outermost interactive supervisor owns the session. Nothing flows back — the user attends the thread. Report status only when asked, through that supervisor's listing surface.

## Thread contract

- **Name** — short, human, specific (`shape-142-driver-payouts`, not `session-2`).
- **Prompt** — standalone. The thread sees none of this conversation: state the goal, inputs by path or ticket id, what done looks like, and any skill it should run.
- **Project and directory** — distinguish the registered project root from the working directory. Run in the supplied directory exactly; do not infer a new worktree from edit intent.
- **Isolation** — when explicitly requested and no prepared directory was supplied, use the `worktree` skill first and dispatch inside its returned path. The caller is provisional owner until spawn; the spawned thread then owns merge/cleanup, and its standalone prompt says so. Its harness thread record plus the parent dispatch report are the ownership record. Report the path and branch with the thread.
- **Model and effort** — use this session's current model and effort, passed explicitly. A user-specified override wins. Do not resolve ordinary threads through staffing.
- **Permission mode** — pass the mode selected for this session explicitly.
- **Report** — after spawn, give the user the name/id, attachment path, exact directory, and branch, whether the directory was prepared here or supplied by a composing workflow.

## Route by outermost supervisor

Select the interactive control plane from explicit host context before looking at the underlying provider:

1. When system/runtime host metadata says this session is running inside T3 Code, T3 is outermost. The product-native `t3-code` MCP toolkit corroborates that context for both Codex and Claude providers; mere installation or reachability of a similarly named MCP server is not an ownership signal. `T3_MCP_BEARER_TOKEN` additionally corroborates T3-hosted Codex but is not universal.
2. Otherwise a Claude Code session uses Claude's background-session surface.
3. Otherwise a Codex session uses Codex's resumable-thread surface.

A Codex or Claude provider running inside T3 always creates a T3 thread. Never route by model name.

## T3 Code

Ground truth: the installed T3 Code. The helper discovers the local runtime at run time; the running app's schema is the authority on command shape — a command the app rejects surfaces as a capability-drift report naming the values sent, never a silent retry or fallback.

Run the bundled helper with the resolved provider, current model, and prepared directory:

    scripts/t3-thread.py --name "<name>" --prompt "<prompt>" \
      --project-directory <project-root> --directory <directory> --branch <branch> \
      --provider <codex-or-claude-instance> --model <model> --effort <effort> \
      --runtime-mode <mode>

The helper discovers the local runtime and installed server CLI, requires a loopback HTTP origin, issues a five-minute bearer session, resolves the active project by its registered root from the lightweight shell snapshot, sends `thread.create` then `thread.turn.start`, and revokes the session on every exit path. It registers a supplied external worktree path and branch; T3 supervises the conversation but does not create or clean the worktree. Creation omits the automatic title seed so the supplied name remains stable.

`--runtime-mode` takes T3's own runtime modes — currently `approval-required`, `auto-accept-edits`, `auto`, or `full-access` — never a provider sandbox name like `workspace-write`; the app refuses anything outside its schema. A payload the app rejects at schema decode comes back as HTTP 400 with an empty body, and the helper degrades that into a command-shape-drift report: which command was refused, the values it sent, the enum sets the last probed app accepted, and where to re-probe. A rejected create changed nothing, so the helper skips the compensating delete instead of manufacturing a second failure. If turn start fails after creation, the helper deletes the partial thread before revoking its credential; when that delete itself fails, the error names the orphaned thread id and title and tells the user to discard it from the T3 sidebar.

Tell the user to open the named thread in the T3 project sidebar. A missing local project, a command the app's schema refuses, authentication failure, or non-local origin is capability drift: report it and stop before falling through to the provider harness. Remote servers and custom T3 homes are unsupported.

## Claude Code

Ground truth: the installed `claude` — flags drift between releases, so recheck `claude --help` if a flag misses.

    cd <directory> && claude --bg -n "<name>" --model <model> --effort <level> \
      --permission-mode <mode> "<prompt>"

The directory is already resolved, so omit Claude's worktree flag. Tell the user: `claude agents` lists sessions; `claude attach <id>` attaches; the session also appears on Claude's attended app surfaces.

## Codex

Ground truth: the installed `codex` — flags drift between releases, so recheck `codex --help` if a flag misses. A CLI thread has a UUID and an optional name:

1. Spawn detached in the resolved directory, capturing the first JSONL `thread.started` id:

   cd <directory> && codex exec --json -s <sandbox> -m <model> \
    -c model_reasoning_effort="<effort>" '<prompt>' > <log-file> 2>&1 &

2. Name it with `scripts/name-codex-thread.py <uuid> "<name>"`.
3. Tell the user: `codex resume '<name>'` opens it; bare `codex resume` is the picker.

Never pass `--ephemeral`; it makes the thread unresumable. When the user attends through the Codex desktop app, create app-natively with app-server `thread/start` → `thread/name/set` → `turn/start` instead of creating an exec-filtered thread.

## Degrade

If the detected outermost harness has no attachable session surface, say so and hand the user the standalone prompt. A failed T3 route never silently becomes a hidden provider-native thread.

## Dependency surface

- **Bundled:** `scripts/t3-thread.py` (local T3 HTTP dispatch); `scripts/name-codex-thread.py` (Codex post-creation naming).
- **Sibling (required, by name):** `worktree` — explicit direct isolation; prepared directories from a composing workflow are used as supplied.
