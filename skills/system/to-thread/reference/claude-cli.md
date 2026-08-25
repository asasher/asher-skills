# Route: Claude Code CLI

Ground truth: the installed `claude` — flags drift between releases, so recheck `claude --help` if a flag misses.

## Dispatch

    cd <directory> && claude --bg -n "<name>" --model <model> --effort <level> \
      --permission-mode <mode> "<prompt>"

The directory is already resolved, so omit Claude's worktree flag.

## Liveness before success

`claude --bg` writes the CLI daemon's session roster. After spawn, confirm the session is observably alive — `claude agents` lists it and shows it running — before reporting success; a session the roster does not show, or shows already dead, is a failed dispatch reported now.

## Report

Tell the user: `claude agents` lists sessions; `claude attach <id>` attaches for inspection.
