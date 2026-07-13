# Playbook: Verifying

> Project playbook for this repo. The backlog `verify` subskill reads this file for check commands and where acceptance criteria come from. How to run and isolate executor-harness probes is in `environment.md`; the transcript and verdict-table contract lives in `evidence.md`.

## Checks

Skill behavior is verified with **situated probes**, not quiz questions or instructions to drive an app. Put the scenarios in the changed skill's `evals/` directory and write their pass/fail answer key **before any executor run**. Probe the moments most likely to be misread: first use, an ambiguous answer, a mid-loop failure, and resume after a gap.

Run the same self-contained scenario through both executor roles:

1. An **in-session executor** in the harness where the skill will run.
2. An **independent CLI executor** in a read-only sandbox.

Give each role the context its real deployment surface receives. Require each answer to cite the file and exact sentence that decided it, and explicitly allow genuine ambiguity to be reported. Preserve both cited transcripts. Grade every probe against every prewritten answer-key criterion in a pass/fail verdict table; both executor roles must meet the recorded pass bar. If wording is ambiguous or a criterion fails, revise the skill and rerun the same keyed probe rather than changing the key to fit the output.

Executor probes replace “drive the app” for skill behavior. Drive bundled scripts directly through their changed paths, and record any repository checks that actually exist:

- Situated behavioral probes: _<path to probes and prewritten answer key>_.
- In-session executor invocation: _<harness role and invocation>_.
- Independent CLI executor invocation: _<verified read-only invocation>_.
- Script syntax / targeted checks: _<verified commands, or blank>_.
- Full behavioral pass bar: _<e.g. every probe passes every criterion on both executors>_.

## CI merge gate

> The host CI's required checks — the gate that blocks the merge, distinct from the behavioral probes above. `setup` discovers this from the repository's CI configuration; `verify` and the PR step read it (`change-description.md`).

- The check set CI runs to gate a merge: _<the required jobs, or "none — no CI">_.
- Where CI diverges from the local script and probe checks: _<note any difference, or "same">_.
- Merge precondition: the change is not mergeable until this CI gate is green. Probe verdicts prove the skill behavior; CI-green is the merge condition when CI exists — neither substitutes for the other.

## Acceptance criteria

- Where criteria come from: the issue, and for an enhancement the approved plan's definition of done. Before any executor run, translate each behavioral criterion into an explicit answer-key row with an observable pass/fail result.
- Grading record: _<path to the per-probe, per-criterion verdict table and both cited transcripts>_.
- Repo-specific expectations every change must satisfy beyond the issue text: _<add yours, or "none">_.
