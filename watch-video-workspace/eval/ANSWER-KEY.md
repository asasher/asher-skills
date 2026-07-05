# watch-video eval — answer key

Written 2026-07-05, BEFORE any executor run. Method: situated dry-run probes
(see memory: skill-eval-dry-run-probes). Executor: codex CLI, read-only sandbox.
Grade each probe pass/fail against the key; an executor flagging genuine
ambiguity is a PASS and a finding, not a failure.

## Session A — execution (SKILL.md in context)

**P1 — 47-min recording, "when does the crash dialog appear?"**
PASS: segments the video — one 80-frame sheet per ~20-minute chunk (any split
into 2–3 segments with `--frames 80 --start S --duration D`); cites the
"Past ~25 minutes, build one 80-frame sheet per ~20-minute segment" sentence.
FAIL: a single index sheet over all 47 min, or jumping straight to scene-cut
detection without an index pass.

**P2 — tile at 5:51 looks like an error toast; user asks what it says.**
PASS: refuses to read text at tile resolution; extracts a full-res frame
(`ffmpeg -ss 351 -i VIDEO -frames:v 1 …`); cites "Mandatory before asserting
on-screen text, counts, identity…". FAIL: answers from the tile, or louping
without converting 5:51 → 351s correctly.

**P3 — full-summary request; index alone is narratable. Window everything?**
PASS: no — cites "Stop at the shallowest pass that answers the question".
Bonus (not required): notes any text/count/identity claim still needs loupe.
FAIL: insists on windowing every scene, or claims the Index completion
criterion forces windows.

**P4 — "what does the presenter say at 2:10?"**
PASS: flags that sheets are silent; transcribe audio separately if a tool
exists, else state the answer omits audio; cites the Probe audio sentence or
the Audio blind-spot bullet. FAIL: builds a window sheet at 2:10 and lip-reads
or guesses.

**P5 — suspected ~0.5s logo flash; 30-frame index shows nothing.**
PASS: runs the scene-cut listing (`select='gt(scene,0.3)',showinfo` …
`grep pts_time`) and windows around the cuts; cites the sub-interval bullet.
FAIL: just increases --frames on a uniform index (0.5s event needs ~360
uniform frames over 3 min — not a sheet-legible density), with no cut-biasing.

**P6 — draft answer says "in the top-right tile of the second sheet…"**
PASS: rewrites to cite the burned-in timestamp; cites the grid-order bullet.
FAIL: sees nothing wrong.

**P7 — YouTube URL, yt-dlp NOT installed. (ambiguity probe)**
PASS: identifies the gap — skill says `curl -L` for files and yt-dlp "if
installed" for streaming sites, but gives no procedure for streaming-without-
yt-dlp — and proposes something honest (ask user / offer install / report
blocked). FAIL: invents a confident procedure (curl-ing the YouTube page for
an mp4) or silently pretends curl will work.

**P8 — dense look at 4:00–4:45 of clip.mp4: exact command.**
PASS: `framesheet.py clip.mp4 OUT.png --start 240 --duration 45 --frames N`
with N ≈ 15–22 (tile every 2–3s, per the Window pass); converts 4:00 → 240.
MARGINAL (note, don't fail): N=12 (3.75s/tile — outside the stated 2–3s).
FAIL: wrong seconds conversion, or a loupe/full-res approach for a 45s window.

## Session B — invocation (descriptions only, no file access)

**M1 — ".mov of the bug happening — find where it goes wrong"** → watch-video.
**M2 — "compress this 80MB demo video so I can email it"** → none (transcoding,
not content understanding; watch-video description scopes to "asks anything
about its content").
**M3 — "summarize this podcast mp3"** → none (audio, not video; watch-video
firing here is a description-wording finding).
**M4 — "screen recording of the app freezing — what did I click right
before?"** → watch-video.
**M5 — "teach me video editing"** → learn-anything (the word "video" must not
steal the trigger).

Session B passes if 5/5 route correctly; any misroute is a description-wording
finding to fix, not just a score.
