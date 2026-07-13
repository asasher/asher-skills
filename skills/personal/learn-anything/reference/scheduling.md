# Scheduling — spaced practice for drills, not cards

Anki's unit is a fact scored recall/no-recall. Ours is a **drill scored against a performance criterion** —
a different data model, and motor decay is slower and sleep-consolidated, so don't Anki-ify the intervals.
State lives in each drill file's frontmatter; `status` derives the picture from them. No separate database.

## Per-drill state (frontmatter of `drills/<name>.md`)

```yaml
stage: cognitive | associative | autonomous
criterion: "8/10 reps self-scored pass at full tempo"
history:            # append one line per session
  - 2026-07-05: 6/10, tempo 80%
last_practiced: 2026-07-05
status: active | consolidating | maintenance | retired
```

## What "due" means

A drill is due when any of:

- **Not at criterion and not practiced this cycle** — active drills want short gaps (every 1–2 days;
  consolidation happens between, so daily grind on one drill buys little over alternating days).
- **At criterion but unconfirmed** — the real test of last session's gains is *next-session-first-reps*,
  cold. Passing cold at criterion twice, spaced, is what promotes a drill (to a harder variant, or to
  `maintenance`).
- **In maintenance and its interval has lapsed** — maintenance intervals stretch as cold checks pass
  (roughly: 3 days → 1 week → 2 weeks → monthly). A failed cold check drops it back to active with an easier
  variant; that's the system working, not a setback.

## Assembling a session's set

1. Take the due list; pick **2–4 drills**, favoring a mix of stages and sub-skills over depth in one —
   interleaving is a scheduling decision as much as an in-session one.
2. Add **at most one stretch drill** slightly past current level. One; ambition concentrates, sessions
   scatter.
3. First reps of the session are the **cold check** on whatever was trained last time — before warm-up
   flatters the numbers. Log them separately (`cold: 4/10` vs `warm: 8/10`); the cold number is the truth.
4. Cap total session length at the stop conditions in `reference/session-protocol.md`, not at a target
   duration. A short clean session logs as a full success.

## Progression and retirement

- **Ratchet** when the criterion is met cold, twice, spaced: raise tempo, lengthen the phrase, noisier
  context, thinner feedback (fading the feedback *is* a progression axis).
- **Regress without ceremony** after two consecutive failed sessions: easier variant, or back to
  `reference/loop-design.md` step 2 — persistent failure usually means the gap was two gaps.
- **Retire** a drill when its parent sub-skill survives in whole-skill performance (the reassembled phrase,
  the conversation in accent, the danced song) across two human checkpoints or performance contexts. Retired
  drills stay on file; a failed checkpoint can reactivate them.
- **Whole-skill sessions are scheduled too** — periodic sessions of just the reassembled skill in realistic
  conditions, no drill structure. Drills exist to serve these; a schedule that never surfaces one has
  optimized the parts and lost the whole.
