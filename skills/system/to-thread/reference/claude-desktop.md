# Route: Claude Desktop

Use spawn-then-import for Claude Desktop. `claude --bg` writes the CLI daemon's session roster; importing a stopped session creates the desktop's `local_*` sidebar record.

## Dispatch

Run `claude-cli.md`'s Dispatch and Liveness before success sections, then report per Report below.

## The import bridge

Once the thread's transcript exists and the session is **stopped**, chain the import:

    claude://resume?session=<full-cli-session-uuid>

Use the full CLI session UUID. The import brings the stopped session into the desktop sidebar, where the user resumes it as a desktop thread. Importing a **running** session puts two writers on one transcript — live inspection stays on `claude attach`.

## Report

Give the user both halves: `claude attach <id>` for live inspection now, and the `claude://resume?session=<uuid>` link (full UUID) for importing into the sidebar once the session stops — plus the spawned thread's model, effort, and permission mode: the import resumes on the desktop's defaults, so the user re-applies them.
