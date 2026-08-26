---
name: prove-your-work
description: Assemble the evidence that a change works and post it where the merge decision happens. Use when a change request is ready and the decider won't be watching the work live.
metadata:
  optional: [writing-for-humans, to-web]
---

# Prove Your Work

Assemble the evidence package for a finished change. The audience is the **decider** — whoever merges without having watched the work: the package must let them decide from the evidence alone.

The package's text follows the `writing-for-humans` sibling. Absent it, write plainly and say the standard was not loaded.

## What the package carries

- **What changed and why** — one paragraph, in the terms of the ticket or spec, naming the head SHA the evidence was captured at — that's how a decider checks the artifacts still describe the code being merged.
- **The proof per claim** — each thing the change claims to do, with the check that demonstrated it:
  - Key each claim to the ticket's acceptance-criterion ids where they exist.
  - The check is the exact command and its trimmed output — or for UI work, the artifacts of whatever drives that surface (a browser driver's trace, screenshots, recording; an emulator or app driver's equivalent for mobile) from the scripted check, captured per the environment playbook (`docs/agents/environment.md`) when the repo has one.
  - A visual artifact goes into the package **looked at**: it shows the content the claim names, legibly and without clipping — existence is not proof.
  - A destructive data operation (migration, cast, backfill) carries its data-safety argument and the evidence behind it.
  - Proof is reproducible: a reader must be able to run the same command and see the same result.
- **What it cost to produce** — the stage ledger the invoking workflow hands over: one row per stage it ran, with the tokens that stage consumed and the harness quota percentage at that point where the harness exposes one. This skill's run closes the ledger with its own evidence row before posting. A number no surface reported stays `unreported` — an estimated or reconstructed figure is padding, not accounting. With no ledger handed over, say so and carry the rows this session can observe.
- **The runs of dropped scaffolding scripts** — a check the spec declared throwaway is deleted before the change request is final. Its run — the exact command, its output, its captured artifacts — lives here, the recoverable record of what it proved.
- **What was not verified, and why** — named plainly. An honest gap outranks a padded package; hiding an unverified claim is the one unforgivable move here.

**Evidence media lives on the bound store, never in the repo:** screenshots, videos, and GIFs upload through the `to-web` sibling, which returns a durable hash-keyed URL, and the package embeds them by URL — images and GIFs inline, videos as links. Absent `to-web`, name the local artifact paths and state the gap.

A defect discovered while assembling the proof stops the package: report it to whoever owns the changes — the package resumes after the fix lands and the change re-enters review.

A capture surface that can't be reached — an auth-gated preview, a vanished fixture — steps down one rung: capture the same claim on the local stack, labeled as such; failing that too, the claim lands in the not-verified section with the reason.

The package is complete when the what-changed paragraph names the head SHA, every claim has a proof entry or a not-verified line, the ledger is closed with this run's row, and every dropped scaffolding script's run is recorded.

## Where it goes

Post the package on the change request, through the platform verbs recorded in `docs/agents/platform.md`. An evidence playbook (`docs/agents/evidence.md`), when present, sets the format and bar; honor it.

## Obligation scales with absence

The less the decider saw, the more the package carries. Work done while they watched and steered may compress to the checks and their results; work done fully AFK carries the complete package — every claim, every command, every gap.
