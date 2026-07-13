# Issue #35 verification verdicts

> Provenance: this is the final verify verdict record copied into the evidence package without re-running or independently re-grading behavior. P1/P2 retain the recorded dual-executor verdict at `6a0bdacb1234e877148e47299e8818ad7c750370`. P3 replaces the stale earlier rows with the converged dual-executor verdict at reviewed commit `001376238342bbf4559acea0cef4c4404b08a869`.

## Probe criteria

| Probe | Prewritten criterion | Issue acceptance criteria | In-session Claude executor | Independent Codex CLI executor | Final verdict |
|---|---|---|---|---|---|
| P1 | Offer exactly six domains and propose `skill-authoring` from `skills/<name>/SKILL.md` evidence. | AC8 | PASS | PASS | **PASS** |
| P1 | Resolve eleven counterparts: three unshadowed common, four native pack files with pack environment shadowing common, and four software stand-ins. | AC10, AC12 | PASS | PASS | **PASS** |
| P1 | Header-flag every stand-in, name every gap in the setup report, and record the domain in `backlog-policy.md`. | AC10, AC11 | PASS | PASS | **PASS** |
| P1 | Trigger none of the keyed failure cases: five-value list, software default, common environment, seven stand-ins, omitted step, or silent fallback. | AC8, AC10–AC12 | PASS | PASS | **PASS** |
| P2 | Pack `environment.md` wins; native pack files remain; only the four absent steps come from software, flagged and reported. | AC10, AC12, AC13 | PASS | PASS | **PASS** |
| P2 | Run preflight fails until all four stand-ins exist; repaired scaffold has eleven counterparts. | AC13 | PASS | PASS | **PASS** |
| P2 | Trigger none of the keyed failure cases: common environment, replacing natives, preflight with seven files, or unflagged/unreported gaps. | AC10, AC12, AC13 | PASS | PASS | **PASS** |
| P3 | Write the answer key before any executor run. | AC3, AC14 | PASS | PASS | **PASS** |
| P3 | Run the same situated probes through an in-session executor and an independent read-only CLI executor. | AC3, AC14, AC15 | PASS | PASS | **PASS** |
| P3 | Require exact deciding-text citations, allow genuine ambiguity, and preserve both transcripts. | AC3, AC15 | PASS | PASS | **PASS** |
| P3 | Grade every probe per prewritten criterion in a pass/fail table; both executors meet the pass bar. | AC3, AC6, AC14, AC15 | PASS | PASS | **PASS** |
| P3 | Retain transcripts and per-criterion results as the raw grading record, then copy the final record into evidence without re-running or re-grading. | AC6, AC15 | PASS | PASS | **PASS** |
| P3 | Shared setup records `evals/` as seed state and shared verify readies/exercises the executor-harness surface without inventing an app or stack. | AC4, AC14 | PASS | PASS | **PASS** |
| P3 | Reject “drive the app and take a screenshot” as the skill-behavior seam; visual artifacts are additive only when the skill produces a visual surface. | AC3, AC6 | PASS | PASS | **PASS** |
| P3 | Trigger none of the keyed failure cases. | AC3, AC6, AC14, AC15 | PASS | PASS | **PASS** |

**Final probe result: P1–P3 3/3 on both executors.**

P3 supersedes the earlier stale runs: the shared no-app setup/verify path was repaired, then the affected probe was re-run on both executor roles. The final convergence run confirms the raw-record/package handoff and the review-triggered re-verification rule at `0013762`; no stale P3 answer or verdict is used here.

## Acceptance-criteria evidence map

| Criteria | Proof carried in this package |
|---|---|
| AC1, AC7–AC13, AC16 | Fresh terminal checks in [static-checks.txt](static-checks.txt). |
| AC2, AC4, AC5 | Reviewed source diff and the cited executor explanations of the pack contracts; no app or visual surface exists for additional capture. |
| AC3, AC6, AC14, AC15 | The dual-executor transcripts and the per-criterion table above. |
