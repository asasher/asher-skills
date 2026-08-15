---
name: prove-your-work
description: Assemble the evidence that a change works — claims, the proof each passed, what wasn't verified — and post it where the merge decision happens. Use when a change request is ready and the decider won't be watching the work live.
argument-hint: "<the change request or branch to evidence>"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: [plain-language, to-web]
---

# Prove Your Work

Assemble the evidence package for a finished change. The audience is whoever decides to merge without having watched the work happen: the package must let them decide from the evidence alone.

The package's text follows the `plain-language` sibling: ASD-STE100 discipline, `CONTEXT.md` as the dictionary, no bare ticket or PR numbers.

## What the package carries

- **What changed and why** — one paragraph, in the ticket's terms, naming the head SHA the evidence was captured at — that's how a decider checks the artifacts still describe the code being merged.
- **The proof per claim** — each thing the change claims to do, keyed to the ticket's acceptance-criterion ids where they exist, with the check that demonstrated it: the exact command and its trimmed output, or for UI work the artifacts of whatever drives that surface — a browser driver's trace, screenshots, recording; an emulator or app driver's equivalent for mobile — from the scripted check, captured per the environment playbook (`docs/agents/environment.md`) when the repo has one. A visual artifact goes into the package **looked at**: it shows the content the claim names, legibly and without clipping — existence is not proof. A destructive data operation (migration, cast, backfill) carries its data-safety argument and the evidence behind it. Proof is reproducible: a reader must be able to run the same command and see the same result.
- **What it cost to produce** — the per-stage token ledger the invoking workflow hands over: one row per stage — implement, each verify and fix pass, each review pass, evidence — with the tokens that stage consumed and the harness quota percentage at that point where the harness exposes one. This step closes the ledger with its own row before posting. A number no surface reported stays `unreported` — an estimated or reconstructed figure is padding, not accounting. With no ledger handed over, say so and carry the rows this session can observe.
- **The runs of dropped scaffolding scripts** — a check the spec declared throwaway does not merge; its file is gone before the change request is final. Its run — the exact command, its output, its captured artifacts — lives here, the recoverable record of what it proved.
- **What was not verified, and why** — named plainly. An honest gap outranks a padded package; hiding an unverified claim is the one unforgivable move here.

**Evidence media is never committed to the repo.** Screenshots, videos, and GIFs upload through the `to-web` sibling, which returns a durable hash-keyed URL on the bound store, and the package embeds them by URL — images and GIFs inline, videos as links. Absent `to-web`, name the local artifact paths and state the gap; the media still stays out of the repo.

A defect discovered while assembling the proof stops the package: report it to whoever owns the changes — the package resumes after the fix lands and re-enters review.

A capture surface that can't be reached — an auth-gated preview, a vanished fixture — steps down one rung: capture the same claim on the local stack, labeled as such; failing that too, the claim lands in the not-verified section with the reason. The ladder is capture mechanics; the honest-gap rule above already covers the reporting.

## Where it goes

Post the package on the change request, through the platform verbs recorded in `docs/agents/platform.md`. A repo with an evidence playbook (`docs/agents/evidence.md`) sets the format and bar; honor it when present.

## Obligation scales with absence

The less the decider saw, the more the package carries. Work done while they watched and steered may compress to the checks and their results; work done fully AFK carries the complete package — every claim, every command, every gap.
