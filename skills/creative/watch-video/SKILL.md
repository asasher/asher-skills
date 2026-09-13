---
name: watch-video
description: Watch a video by reading contact sheets — tiled, timestamped frame grids sized for a vision model. Use when the user shares a video, clip, or screen recording and asks anything about its content (what happens, summarize, find a moment, verify a flow or bug on screen), or when another skill needs to understand video.
---

# Watch Video

Work like a photographer at a light table. Build a **contact sheet** — frames shrunk to tiles, timestamps burned in, packed into one image — scan it, mark the **selects**, then **loupe** the keepers at full resolution. One sheet carries minutes of temporal structure in a single image, and because the motion sits side by side, causality reads at a glance.

Use `scripts/framesheet.py` (needs ffmpeg + Pillow on PATH) to build every sheet with the tuned geometry budget.

## The drill-down

Three passes, each one sheet-read deep. Stop at the shallowest pass that answers the question; most questions die at 1 or 2.

**0. Probe.** Inspect the file’s duration and resolution; download URL sources with an available tool first. If the question hinges on speech or sound, flag it now — sheets are silent; transcribe the audio track separately if a tool exists, and say plainly when the answer omits audio.

**1. Index.** One sheet spanning the whole video: `framesheet.py VIDEO index.png --frames 30` (up to `--frames 80` for busy or fast-cut footage — tiles stay legible down to ~150 px). Past ~25 minutes, build one 80-frame sheet per ~20-minute segment so no tile stands in for more than ~20s. Read the sheet and write the scene map. Done when every stretch of the timeline is accounted for — either irrelevant to the question or a marked select with its timestamp range.

**2. Window.** For each select, a dense sheet: `framesheet.py VIDEO window.png --start S --duration 30 --frames 12`. A tile every 2–3 seconds at window tile sizes reads as a causal chain — expressions, motion blur, cause and effect. Done when you can narrate the window: what happened, in order, each beat with its timestamp.

**3. Loupe.** Extract full-resolution frames at the selected timestamps for whatever a tile can't settle. Mandatory before asserting on-screen text, counts, identity, or anything small — at tile resolution those are hypotheses, not answers.

**Answer.** Every claim traces to a tile or loupe frame actually read, cited by timestamp; every text, count, or identity claim went through the loupe. Whatever is still uncertain gets reported as uncertain, not smoothed over.

## Blind spots

- **Sub-interval events** — uniform sampling skips moments shorter than one tile interval. When hunting a beat the index missed, detect scene cuts and inspect dense windows around their timestamps.
- **Grid order** — cite tiles by their burned-in timestamp.
- **Audio** — a sheet answer to a speech question is wrong by construction; see Probe.
