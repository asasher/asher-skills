# Playbook: Diagnosing Bugs

> Skill-authoring project delta owned by `diagnosing-bugs setup`. The installed skill owns the six-phase
> method; this file keeps only the domain's normal seams and leaves repository-specific values editable.

## This repo

- Regression seam: a failing situated probe or confirmed misbehaving transcript, run through both an in-session executor and an independent CLI executor; bundled scripts use a direct failing invocation.
- Probe location and invocation: _<path to the changed skill's eval scenarios, answer key, and verified executor commands>_.
- Script checks or debug entry points: _<verified commands, or “none”>_.
- Known model-dependent surfaces: preserve cited transcripts; nondeterministic runs follow the bundled flaky-bug rule.
- Deliberate house-practice substitutions: _<add, or “none”>_.
