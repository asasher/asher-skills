# Playbook: Evidence

> Project playbook for a skill-authoring repo. The `prove-your-work` skill reads this file for what to capture, storage, and presentation. How to run executor-harness probes and direct script checks is in `environment.md`.

## What to capture

For skill behavior, the default proof is the **cited transcript from each executor role** plus a **pass/fail verdict table mapping every probe to every prewritten answer-key criterion**. Preserve the exact scenario and context each role received. For a behavioral rework, show the relevant before/after verdict shift.

- Skill behavior change: both executor transcripts and the per-probe, per-criterion verdict table.
- Bundled script change: syntax-check transcript plus a direct invocation through the changed path.
- Skill producing a visual surface: behavioral proof plus rendered screenshots and a short flow artifact when interaction is a criterion.
- Pure explanatory prose: the diff and the criterion it satisfies; _<add stricter repo expectations if needed>_.

After review converges, copy the final verify step's raw transcript and verdict record into the evidence package without rerunning or independently regrading it. If review changed behavior, reverify the affected criteria first. An uncited executor summary or a screenshot without the keyed behavioral verdict is not sufficient proof of a skill decision.

## Format and storage

- Executor runs: _<plain-text or Markdown transcripts stored under the repo's evidence convention>_.
- Verdicts: a Markdown table with one row per probe criterion and columns for expected result, both executors, citation, and pass/fail.
- Visual states: PNG/JPEG; interactive flows: a short GIF where supported. **Media is never committed to the repo**: upload it via the `to-web` sibling to the artifact store bound in `platform.md` and embed by the returned URL. Absent that sibling, say so and state the requirement rather than committing media as a silent fallback.
- Transcript/verdict file naming and location: _<add the repo's convention>_.
- Secrets and private context: redact credentials and unrelated user data without removing the cited decision needed for grading.

## Presentation

The deliverable is a ready-to-review evidence block grouped by acceptance criterion. Include the verdict table and concise links or excerpts that make both transcripts inspectable. Every visual artifact must render inline on the bound review surface. Prepare and verify the block, then hand it back to the invoking thread; do not post or comment from the evidence step.

### GitHub binding

- Store committed transcripts and verdict tables at paths the change review can reach; embed media by its `to-web` URL, one `[![<criterion>](<url>)](<url>)` line per artifact.
- Verify every referenced file exists in the published revision, every media URL answers, and every image uses a renderable format (PNG/JPEG/GIF, never MP4).

### Local binding

- Use repo-relative links from the review file to transcripts and verdict tables; media embeds use the same `to-web` URLs, which render in any markdown viewer.
- Verify every referenced path exists at the reviewed revision and every media URL answers.
