# Playbook: Evidence

> Project playbook for this repo. The backlog `evidence` subskill reads this file for what to capture, the format/storage contract, and the presentation contract that makes artifacts reviewable by the human; the gates are in the skill's `reference/evidence.md`. How to run executor-harness probes and direct script checks is in `environment.md`; the review surface is bound in `platform.md`. The change-description outline that consumes the prepared evidence block is in `change-description.md`.

## What to capture

For skill behavior, the default proof is the **cited transcript from each executor role** plus a **pass/fail verdict table mapping every probe to every prewritten answer-key criterion**. Preserve the exact scenario and context each role received. For a behavioral rework, show the relevant before/after verdict shift on the scenario that motivated the change.

Per change type — the shipped baseline; tune to this repo:

- Skill behavior change (`SKILL.md`, references, routing): both executor transcripts and the per-probe, per-criterion verdict table.
- Bundled script change: the terminal transcript of syntax checks plus a direct invocation through the changed path.
- Skill that produces a visual surface: the behavioral proof above **plus rendered screenshots** of the changed artifact, and a short flow artifact when interaction is part of a criterion.
- Pure explanatory prose with no behavioral contract: the diff and the criterion it satisfies; _<add stricter repo expectations if needed>_.
- Repo-specific expectations beyond these: _<add yours, or "none">_.

Captured once after review converges, every transcript, verdict row, and rendered artifact is mapped to the acceptance criterion it proves. An uncited executor summary or a screenshot without the keyed behavioral verdict is not sufficient proof of a skill decision.

## Format and storage

- Executor runs: _<plain-text or Markdown transcripts stored under the repo's evidence convention>_.
- Verdicts: a Markdown table with one row per probe criterion and columns for expected result, in-session executor, independent CLI executor, citation, and pass/fail.
- Static visual states: PNG or JPEG screenshots; interactive flows: a short GIF when the review surface supports it.
- File naming and evidence directory: _<add the repo's convention>_.
- Secrets and private context: redact credentials and unrelated user data without removing the cited instruction or decision needed to grade the run.

## Presentation — artifacts must render inline

The deliverable is a ready-to-review evidence block grouped by acceptance criterion. Include the verdict table and concise links or excerpts that make both transcripts inspectable. Every visual artifact must render inline on the bound review surface; a click-through-only image does not satisfy the presentation contract. Prepare and verify the block, then hand it back to the invoking thread — do not post or comment from the evidence step.

### GitHub binding

- Store committed transcripts, verdict tables, and rendered artifacts at paths the change review can reach.
- Use same-origin inline image embeds supported by the host, pinned to a published revision when the repository requires stable evidence links.
- Verify that every referenced file exists in the published revision and that every image uses a renderable PNG, JPEG, or GIF format.
- Repo-specific embed form and mechanical check: _<add yours>_.

### Local binding

- Use repo-relative links from the review file to transcripts and verdict tables, and repo-relative image embeds for rendered artifacts.
- Verify every referenced path exists at the reviewed revision and preserves its relative-path resolution when presented.
- Repo-specific review-file location: _<add yours>_.

### Other bindings

Record the review surface's transcript-link and inline-artifact forms, known failure modes, and a mechanical check for each artifact during setup (`platform.md` § Custom bindings).
