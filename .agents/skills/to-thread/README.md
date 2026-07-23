# To Thread

Dispatch adapter for interactive work: spawns one named, harness-native background session the user
attends (a Claude Code `claude --bg` background agent; a Codex thread via `codex exec` plus app-server
naming), seeded with a standalone prompt and reported back to the user as attach instructions. Detached
by design — nothing flows back to the spawning session; status on request via the harness's own listing
commands. One call spawns one thread; how many threads a piece of work needs is the caller's decision.

## When to use

- A unit of work should continue in a session of its own that the user drives (a shaping thread for a
  ticket, a build thread for a ready ticket).
- Any conversation should continue as its own attachable session instead of inside this one.

## Dependency surface

- **Bundled:** `scripts/name-codex-thread.py` (Codex threads can't be named at creation; this names one
  post-hoc over the app-server protocol).
- **Siblings:** none — a sealed dispatch adapter; harness knowledge lives here so no other skill carries it.

## Provenance

No external sources. Harness mechanics verified live on claude 2.1.216 and codex-cli 0.144.5 (2026-07);
the version lines in `SKILL.md` mark where to recheck when either CLI moves.
