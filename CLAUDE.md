# CLAUDE.md

@AGENTS.md

The import above pulls in the harness-neutral base — layout, vocabulary, conventions, the skill map —
at session start (Claude Code never reads `AGENTS.md` on its own). This file adds only what applies when
the harness is Claude Code.

## Staffing

Read `docs/agents/staffing.md` fully before model choice, delegation, child/worktree creation,
capability-provider work, watcher assignment, or route-loss fallback. It is the sole authority — the complete
roster, this repo's deltas, and the machine its reachability rows were probed on. There is no machine-level
staffing module; a home-directory roster is not consulted, and neither is the `staffing` skill's bundled seed.
Codex sessions read the same file.

If that file is missing, or its probe record names a machine other than this one, say so and run
`staffing setup` rather than dispatching on rows nobody verified here.
