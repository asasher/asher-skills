---
name: prove-your-work
description: Assemble the evidence that a change works and post it on the PR where the merge decision happens. Use when a PR has converged and the decider won't be watching the work live.
metadata:
  optional: [technical-writing, to-web]
---

# Prove Your Work

Assemble the evidence package for a finished change. The audience is the **decider**, whoever merges without having watched the work: the package must let them decide from the evidence alone.

The package's text follows the `technical-writing` sibling. Absent it, write plainly and say the standard was not loaded.

## What the package carries

- **What changed and why**: one paragraph, in the terms of the issue or spec, naming the head SHA the evidence was captured at. That is how a decider checks the artifacts still describe the code being merged.
- **The proof per claim**: each thing the change claims to do, with the check that demonstrated it.
  - Key each claim to the issue's acceptance-criterion ids where they exist.
  - The check is the exact command and its trimmed output, or for UI work the artifacts of whatever drives that surface (a Playwright trace, screenshots, a recording; an emulator or app driver's equivalent for mobile) from the scripted check, captured per `docs/agents/environment.md` § Driving the app.
  - A visual artifact goes into the package **looked at**: it shows the content the claim names, legibly and without clipping. Existence is not proof.
  - A destructive data operation (migration, cast, backfill) carries its data-safety argument and the evidence behind it.
  - Proof is reproducible: a reader must be able to run the same command and see the same result.
- **The runs of dropped throwaway scripts**: a check the spec declared throwaway is deleted before the PR is final. Its run (the exact command, its output, its captured artifacts) lives here, the recoverable record of what it proved.
- **What was not verified, and why**, named plainly. An honest gap outranks a padded package; hiding an unverified claim is the one unforgivable move here.

## Media and format

Evidence media lives in the artifact store, never in the repo. Screenshots, videos, and GIFs upload through the `to-web` sibling, which returns a durable hash-keyed URL; absent `to-web`, name the local artifact paths and state the gap. Name each upload so the key says what it proves: `<criterion>-<what-it-shows>.png`.

- Static states: PNG or JPEG. Flows: record MP4 locally, then convert the seconds that show the criterion (about ten at most) to a GIF with a two-pass palette, `ffmpeg -i in.mp4 -filter_complex "fps=12,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" out.gif`, kept well under GitHub's inline ceiling of 10 MB. Videos link; images and GIFs embed.
- Embed form, one line per artifact, grouped by the criterion it proves, wrapped so the inline image click-opens full size: `[![AC-n](<url>)](<url>)`.
- Verify mechanically before posting: each URL answers HTTP 200 with an image content type, and the extension is PNG, JPEG, or GIF, never MP4. The agent often cannot view the rendered page; these checks catch the known failure modes without a browser.

A defect discovered while assembling the proof stops the package: report it to whoever owns the changes; the package resumes after the fix lands and the change re-enters review.

A capture surface that cannot be reached (an auth-gated preview, a vanished fixture) steps down one rung: capture the same claim on the local stack, labeled as such; failing that too, the claim lands in the not-verified section with the reason.

The package is complete when the what-changed paragraph names the head SHA, every claim has a proof entry or a not-verified line, every embed passed the mechanical check, and every dropped throwaway script's run is recorded.

## Where it goes

Post the package as a comment on the PR with `gh pr comment`, and replace the PR body's evidence placeholder with a pointer to it.

## Obligation scales with absence

The less the decider saw, the more the package carries. Work done while they watched and steered may compress to the checks and their results; work done fully unattended carries the complete package: every claim, every command, every gap.
