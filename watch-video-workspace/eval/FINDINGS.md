# watch-video eval — findings

2026-07-05 · method: situated dry-run probes (memory: skill-eval-dry-run-probes)
· executor: codex CLI 0.140.0, read-only sandbox · answer key written before runs.

## Score: 13/13

| Session | Probes | Result |
|---|---|---|
| A — execution (SKILL.md in context) | P1–P8 | 8/8 pass |
| B — invocation (description among 4 real decoys) | M1–M5 | 5/5 routed per key |

## Notable

- **P1 (long-video segmenting)**: executor produced the exact 3-segment 80-frame
  plan and cited the "Past ~25 minutes" sentence verbatim — the sentence carries
  the behavior on its own.
- **P2/P8 (arithmetic)**: both timestamp→seconds conversions correct (5:51→351,
  4:00→240); P8 chose `--frames 18` (2.5s/tile), dead center of the stated 2–3s
  window cadence.
- **P7 (planted gap, streaming URL without yt-dlp)**: executor flagged the gap
  and asked for a local file or an install — no hallucinated fallback. The
  "if installed" wording degrades honestly; leaving the gap in place is the
  correct design (a download procedure for arbitrary streaming sites doesn't
  belong in this skill).
- **Invocation scoping held**: compression (M2) and audio-only (M3) correctly
  got "none" — "asks anything about its content" fences out transformation
  tasks; "teach me video editing" (M5) went to learn-anything, so the word
  "video" alone doesn't steal triggers.

## Verdict

Ship as-is. No wording changes indicated by any probe. Second-tier (live smoke
test of tool mechanics) already effectively done during authoring: framesheet.py
was exercised against a real 596s video (index/dense/window/--cols/error paths)
before the skill was written.
