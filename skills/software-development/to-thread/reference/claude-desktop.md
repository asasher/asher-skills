# Route: Claude Desktop

The desktop app has no direct spawn surface for this dispatch: `claude --bg` writes only the CLI daemon's session roster, while the desktop app lists its own `local_*` session records — a CLI-spawned session never appears in the sidebar on its own. The working bridge is spawn-then-import.

## Dispatch

Spawn through the CLI exactly as on the CLI route:

    cd <directory> && claude --bg -n "<name>" --model <model> --effort <level> \
      --permission-mode <mode> "<prompt>"

Confirm liveness the same way — `claude agents` lists the session running — before reporting success.

## The import bridge

Once the thread's transcript exists and the session is **stopped**, chain the import:

    claude://resume?session=<full-cli-session-uuid>

The full CLI session UUID is required — a prefix or short id does not resolve. The import brings the stopped session into the desktop sidebar, where the user resumes it as a desktop thread.

## Two writers — the live-inspection rule

Importing a **running** session puts two writers on one transcript. Never import a live thread: live inspection stays on `claude attach`; the sidebar import is for stopped threads only. The division of labor: while the thread runs, the user inspects via CLI attach; when it stops, the import makes it a desktop thread.

## Cold-import caveats

Model, effort, and permission mode do not carry over on import — the imported session resumes on the desktop's defaults unless the user re-applies them. Name the spawned thread's model, effort, and permission mode in the report so the user can restore them on resume.

## Report

Give the user both halves: `claude attach <id>` for live inspection now, and the `claude://resume?session=<uuid>` link (full UUID) for importing into the sidebar once the session stops — plus the settings to re-apply after import.
