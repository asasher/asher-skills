# OBS educational-video runs

The coordinator writes and improves the skills. A separate T3 agent performs ordinary production work without being told about the eval. Asher reviews the resulting video here.

- `iteration-1`: preserved setup failure; unrelated global skills leaked into the initial catalog. Interrupted, not scored.
- `iteration-2`: landscape working assumption, stopped after the user selected a portrait short. Partial work is preserved without scoring.
- `iteration-3`: first portrait baseline, using the September 19 14:54 OBS group and skill revision `57fb7fa`. One focused 1080 × 1920 short for YouTube, Instagram, and TikTok. Finished at 39.57 seconds; transcript and 125 artifact hashes captured. Human review is pending.

The portrait project is `~/Projects/random/obs-sep19-short`. Open **OBS September 19 · Portrait short** in the asher-skills T3 sidebar. Its `run.json` records the thread identity.

`run.json` pins the prompt, footage, package hashes, model settings, and initial project revision. `launch-evidence.json` checks the actual provider context. Captures preserve transcripts and media hashes without committing media to Git. Each iteration freezes its review contract in `rubric.json`. The portrait contract includes caption and graphic geometry checks; actual organic app previews remain a separate check. Human feedback and coordinator judgments are recorded separately.

See `AGENTS.md` for prepare/start/status/capture commands and iteration rules. The participant project is kept for inspection and playback; it has no source remote or links to coordinator records.

After capture, run `python3 video-edit-workspace/inspect-export.py --video VIDEO --captions SRT --out video-edit-workspace/evals/iteration-N/inspection` for independent full-decode, stream, encoded-loudness, and caption-timing evidence. Keep subjective judgments separate.

[Open the first portrait review](https://pub-6d5eb34d234d4f3cad4464870d8d0482.r2.dev/asher-skills/video-portrait-first-trial/dd604bb7f50e39fa20b33eb9d12554682b648d2bbca53b288717b777fb7587dd-cf42e22a-f1fa-4b1c-ba2f-ae368e6a6d65/review.html). It includes the video, voice comparison, guide toggle, and downloadable timestamped feedback. The baseline output is unchanged; the coordinator records one minor face-edge/reference-mask conflict separately.
