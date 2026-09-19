# OBS educational-video runs

The coordinator writes and improves the skills. A separate T3 agent performs ordinary production work without being told about the eval. Asher reviews the resulting video.

- `iteration-1`: setup failure. Ambient skills leaked into the catalog; stopped without scoring.
- `iteration-2`: landscape working assumption, superseded by the user's portrait selection. Partial work preserved without scoring.
- `iteration-3`: first portrait baseline, skill revision `57fb7fa`. The human rejected its inset composition. Transcript, 125 artifact hashes, exact feedback, and the proposed correction are preserved.
- `iteration-4`: corrected composition baseline, skill revision `5ddbbd5`. Captured 125 artifact hashes and the completed transcript. The 44.87-second result restores graphics above and portrait camera below, filling the frame. Export checks pass; human quality judgments and actual app previews remain pending. The project design and rubric also changed; footage, prompt, model, effort, and toolchain stayed the same.

The current thread is **OBS September 19 · Stacked portrait**, id `7c8614d9-5dcb-44c5-9bb5-8a1258c30047`, in the asher-skills T3 sidebar. Its project is `~/Projects/random/obs-sep19-stacked`.

Each `run.json` pins the prompt, footage, package hashes, model settings, and initial project revision. `launch-evidence.json` checks the actual provider context. Captures preserve transcripts and media hashes without committing media. Each iteration freezes its rubric. Human feedback and coordinator judgments remain separate.

See `AGENTS.md` for prepare/start/status/capture commands. Participant projects have no source remote or links to coordinator records.

After capture, run `python3 video-edit-workspace/inspect-export.py --video VIDEO --captions SRT --out video-edit-workspace/evals/iteration-N/inspection` for independent decode, stream, loudness, and caption-timing evidence. Review the full composition before local UI clearance. Ad-template overlaps alone do not establish organic UI failures.

Published URLs and content hashes live in each iteration's `publication.json`. The rejected first portrait review remains available as historical evidence; it is not the current design reference.
