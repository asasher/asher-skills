# Playbook: Verifying

> Project playbook for a skill-authoring repo. The backlog `verify` step reads this file for check commands
> and acceptance sources. How to run and isolate executor-harness probes is in `environment.md`.

## Checks

Skill behavior is verified with **situated probes**, not quiz questions or instructions to drive an app. Put
the scenarios in the changed skill's `evals/` directory and write their pass/fail answer key **before any
executor run**. Probe the moments most likely to be misread: first use, an ambiguous answer, a mid-loop
failure, and resume after a gap.

Run the same self-contained scenario through both executor roles:

1. An **in-session executor** in the harness where the skill will run.
2. An **independent CLI executor** in a read-only sandbox.

Give each role the context its real deployment surface receives. Require citations to the file and exact
sentence deciding every answer, explicitly allow genuine ambiguity, preserve both transcripts, and grade
every probe against every prewritten criterion. If wording is ambiguous or a criterion fails, revise the
skill and rerun the same keyed probe rather than changing the key.

- Situated behavioral probes: _<path to probes and prewritten answer key>_.
- In-session executor invocation: _<harness role and invocation>_.
- Independent CLI executor invocation: _<verified read-only invocation>_.
- Script syntax / targeted checks: _<verified commands, or blank>_.
- Full behavioral pass bar: _<e.g. every probe passes every criterion on both executors>_.

## CI merge gate

- Required CI jobs: _<the required jobs, or “none — no CI”>_.
- Difference from local script and probe checks: _<note any difference, or “same”>_.
- Merge precondition: CI is green when a CI gate exists; probe verdicts and CI do not substitute for one another.

## Acceptance criteria

- Where criteria come from: the issue, and for an enhancement the approved plan's definition of done.
- Grading record: _<path to the per-probe, per-criterion verdict table and both cited transcripts>_.
- Repo-specific expectations beyond the issue text: _<add yours, or “none”>_.
