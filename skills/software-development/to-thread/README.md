# To Thread

Dispatch adapter for interactive work: spawns named, harness-native background sessions the user attends
(Claude Code `claude --bg` background agents; Codex threads via `codex exec` plus app-server naming), each
seeded with a standalone prompt and reported back to the user as attach instructions. Detached by design —
nothing flows back to the spawning session; status on request via the harness's own listing commands.

## When to use

- A dispatcher fans units of work out into sessions the user will drive (one shaping thread per ticket,
  one build thread per ready ticket).
- Any conversation should continue as its own attachable session instead of inside this one.

## Dependency surface

- **Bundled:** `scripts/name-codex-thread.py` (Codex threads can't be named at creation; this names one
  post-hoc over the app-server protocol).
- **Siblings:** none — a sealed dispatch adapter; harness knowledge lives here so no other skill carries it.

## Provenance

No external sources. Harness mechanics verified live on claude 2.1.216 and codex-cli 0.144.5 (2026-07);
the version lines in `SKILL.md` mark where to recheck when either CLI moves.
