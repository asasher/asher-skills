# OBS educational-video runs

The coordinator writes and improves the skills. A separate T3 agent performs ordinary production work without being told about the eval. Asher reviews the resulting video.

- `iteration-1`: setup failure. Ambient skills leaked into the catalog; stopped without scoring.
- `iteration-2`: landscape working assumption, superseded by the user's portrait selection. Partial work preserved without scoring.
- `iteration-3`: first portrait baseline, skill revision `57fb7fa`. The human rejected its inset composition. Transcript, 125 artifact hashes, exact feedback, and the proposed correction are preserved.
- `iteration-4`: corrected composition baseline, skill revision `5ddbbd5`. Captured 125 artifact hashes and the completed transcript. The 44.87-second result restores graphics above and portrait camera below, filling the frame. Export checks pass. The human praised the layout and graphics but requested complete thoughts and sentences; actual app previews remain pending. The project design and rubric also changed; footage, prompt, model, effort, and toolchain stayed the same.

- `iteration-5`: candidate skill revision `59e52b7`, adding narration completeness checks. Only `edit-video/SKILL.md` changes in the 236-file production skill set. Other comparison inputs match iteration 4. The completed 62.2-second cut, transcript, and 129 artifact hashes are captured. Narration structure and export checks pass; human review remains pending.

The current thread is **OBS September 19 · Portrait story**, id `371a3e0b-0c55-4bba-9c86-9190804b679a`, in the asher-skills T3 sidebar. Its project is `~/Projects/random/obs-sep19-story`.

Each `run.json` pins the prompt, footage, package hashes, model settings, and initial project revision. `launch-evidence.json` checks the actual provider context. Captures preserve transcripts and media hashes without committing media. Each iteration freezes its rubric. Human feedback and coordinator judgments remain separate.

See `AGENTS.md` for prepare/start/status/capture commands. Participant projects have no source remote or links to coordinator records.

After capture, run `python3 video-edit-workspace/inspect-export.py --video VIDEO --captions SRT --out video-edit-workspace/evals/iteration-N/inspection` for independent decode, stream, loudness, and caption-timing evidence. Review the full composition before local UI clearance. Ad-template overlaps alone do not establish organic UI failures.

Published URLs and content hashes live in each iteration's `publication.json`. The rejected first portrait review remains available as historical evidence; it is not the current design reference.

[Review the corrected portrait cut](https://pub-6d5eb34d234d4f3cad4464870d8d0482.r2.dev/asher-skills/video-stacked-portrait/389d508c1fa54ba617698666d99c495bcad7bbae732bdabfa0f409a4bf2db48c-537c60dd-65ed-41cf-8a92-179dcdc3fa15/review.html). The page includes paired voice excerpts and downloadable timestamped feedback. URL keys, source revisions and verified content hashes are recorded in `iteration-4/publication.json`.

[Review the narration revision](https://pub-6d5eb34d234d4f3cad4464870d8d0482.r2.dev/asher-skills/video-complete-thoughts/58ba4387d104557df4548bbbe4d3e03199f09c0c12e531873b2b66a9be4de9a9-c5a466ff-ccff-497e-80ba-0b50c49e2e60/review.html). This is the current review page, with the previous cut, voice comparison, caption transcript and timestamped feedback. URL keys, source revisions and verified hashes are recorded in `iteration-5/publication.json`.
