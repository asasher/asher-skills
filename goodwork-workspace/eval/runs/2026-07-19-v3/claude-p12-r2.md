# P12 round 2 — Claude executor (fresh fable subagent, S+R daily.md context pasted, 2026-07-19)

Answer from the two pasted files only.

## First three actions, in order

**Action 1 — Read `reference/framework.md`.** Decided by SKILL.md: "Read reference/framework.md once per
session before running any command." This is a fresh session and `daily` is a command, so the framework
read comes before anything else.

**Action 2 — Load `reference/daily.md` and follow it.** Decided by SKILL.md Routing rule 2: "First word
matches a command: load the matching reference and follow it."

**Action 3 — Run the reconcile sweep before building today's queue** (checking `capabilities.json` →
`reconcile.last_run_at`, a state touch, so `reference/state.md` loads with it, and the sweep itself means
loading `reference/reconcile.md`). Decided by reference/daily.md: "Start every `daily` with the
reconcile.md sweep, unless one already ran today (`capabilities.json` → `reconcile.last_run_at`) or the
user declines it". After 9 days away, no reconcile ran today, and the user hasn't declined, so the sweep
runs. The `manual` cadence is explicitly irrelevant here — reference/daily.md: "The recorded cadence
governs *standalone* reconcile scheduling only — it never exempts `daily` from sweeping first."

Only after the sweep do I build the morning action queue.

## The journal-gap question

The 9-day gap trips the cadence flag: "3+ days with no journal entry → ask once whether to shrink the
daily footprint or pause the campaign honestly (a declared pause beats a silent fade)." Asked in plain
language, on its own, awaited. **How many times: exactly once** — "ask once", reinforced by "raise,
don't nag". If the user ignores or deflects it, not re-raised.

**One minor ambiguity, flagged:** "unless … the user declines it" doesn't specify whether to *offer* the
sweep (inviting a decline) or run it unless pre-emptively declined. The imperative "Start every `daily`
with the reconcile.md sweep" reads as run-by-default, so it runs without asking — but the file doesn't
settle this explicitly.
