# Playbook: Diagnosing Bugs

> Project-specific delta owned by `diagnosing-bugs setup`. The installed skill owns the six-phase method;
> this file keeps only this repo's seams, commands, substitutions, and known hazards.

## This repo

- Test framework, suite location, and narrowest regression command: **no unit-test framework.** A skill bug is
  a wrong decision, broken route, or failing script. Reproduce it with the triggering situated probe through
  both executors in `docs/agents/probe-evals.md`; for a script bug, run `python3 -m py_compile <script>` then
  drive the failing path. The reproducing scenario becomes a probe in that skill's `evals/`.
- Logging, debugger, profiler, or trace entry points: none special. Skills expose reasoning in executor
  transcripts; stdlib scripts use stdout/stderr.
- Known flaky or hard-to-reproduce surfaces: **model-dependent skill behavior.** Reproduce across at least two
  executor runs, ideally Claude plus `codex exec`, and rerun the same corpus before calling it fixed.
- Deliberate house-practice substitutions: probe-eval equivalence is the regression seam for prose skills;
  script changes additionally require compilation and a driven path.
