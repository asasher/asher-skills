---
name: prove-your-work
description: Assemble the evidence that a change works — claims, the proof each passed, what wasn't verified — and post it where the merge decision happens. Use when a change request is ready and the decider won't be watching the work live.
argument-hint: "<the change request or branch to evidence>"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Prove Your Work

Assemble the evidence package for a finished change. The audience is whoever decides to merge without
having watched the work happen: the package must let them decide from the evidence alone.

## What the package carries

- **What changed and why** — one paragraph, in the ticket's terms.
- **The proof per claim** — each thing the change claims to do, keyed to the ticket's acceptance-criterion
  ids where they exist, with the check that demonstrated it: the exact command and its trimmed output, or
  for UI work the artifacts of whatever drives that surface — a browser driver's trace, screenshots,
  recording; an emulator or app driver's equivalent for mobile — from the scripted check, captured per
  the environment playbook (`docs/agents/environment.md`) when the repo has one. A visual artifact goes
  into the package **looked at**: it shows the content the claim names, legibly and without clipping —
  existence is not proof. A destructive data operation (migration, cast, backfill) carries its
  data-safety argument and the evidence behind it. Proof is reproducible: a reader must be able to run
  the same command and see the same result.
- **What was not verified, and why** — named plainly. An honest gap outranks a padded package; hiding an
  unverified claim is the one unforgivable move here.

A defect discovered while assembling the proof stops the package: report it to whoever owns the
changes — the package resumes after the fix lands and re-enters review.

## Where it goes

Post the package on the change request, through the platform verbs recorded in
`docs/agents/platform.md`. A repo with an evidence playbook (`docs/agents/evidence.md`) sets the format
and bar; honor it when present.

## Obligation scales with absence

The less the decider saw, the more the package carries. Work done while they watched and steered may
compress to the checks and their results; work done fully AFK carries the complete package — every
claim, every command, every gap.
