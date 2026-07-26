# CLAUDE.md

@AGENTS.md

The import above pulls in the harness-neutral base — layout, vocabulary, conventions, the skill map, and
§ Staffing — at session start (Claude Code never reads `AGENTS.md` on its own). This file adds only what
applies when the harness is Claude Code.

## Staffing — Claude Code delta

The roster and the trigger are in `AGENTS.md` § Staffing, which the import above already pulled in; both
harnesses use the same one. Nothing about resolution differs here.

One Claude-specific note: a machine-level `~/.claude/CLAUDE.md` § Staffing may still be loaded ahead of this
file and may still instruct you to read a home-directory roster. **It is superseded.** Resolve from
`docs/agents/staffing.md` and ignore the home-directory module; it is retained only until the repos still
resolving through it have migrated, and is being retired.
