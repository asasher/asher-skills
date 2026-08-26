# Playbook: Evidence

> Project playbook for this repo. The `prove-your-work` skill reads this file for what to capture, the format/storage contract, and the presentation contract that makes artifacts render for the human. How to run, seed, and authenticate against the app — and the capture drivers — are in `environment.md`; the review surface this presents to is bound in `platform.md`, and the artifact store media uploads to is bound in `platform.md` § Artifact store. The PR body outline that consumes the prepared evidence block is in `change-description.md`.

## What to capture

For a repo with a real running app, evidence is **real check/test output plus artifacts driven through the actual app** — screenshots and recordings of the running surface, terminal transcripts of the real check commands. A transcript that reasons about what would happen is not evidence. If no runnable surface exists, state that the behavior remains unverified.

Per change type — the shipped baseline; tune to this repo:

- Pure logic or backend fix: nothing beyond green checks — the targeted test is the proof.
- UI change: before/after screenshots of the changed surface; a short GIF for flows.
- Workflow or auth change: an app-level walkthrough naming the account/state used, the expected result, and the observed result.
- Data or migration change: the migration/command result plus before/after proof that the affected store is safe.
- One-work scaffolding scripts (per `environment.md` § Driving the app): the script's run and output are captured here before the script is dropped — the evidence package is where a dropped script's proof survives.
- Repo-specific expectations beyond these: _<add yours, or "none">_.

Timing: capture once after adversarial review converges, each artifact mapped to the criterion it proves. A prior capture may be reused only when the reviewer confirmed the intervening change was styling-only.

## Obligation scales with absence

- **Unattended (AFK) run** — nobody watched, so the PR owes the full package above: every artifact at the final reviewed HEAD, each mapped to the acceptance criterion it proves.
- **Interactive work the human witnessed live** — the obligation may degrade to the PR body's verification grades (each criterion marked with its grade); note that the human observed the behavior directly. Capture full artifacts anyway when the change is risky or the reviewer isn't the person who watched.

## Format and storage

- Static states: PNG or JPEG screenshots.
- Flows: record MP4 for local inspection, then convert the seconds that show the criterion (≤ ~10s) to a GIF with a two-pass palette — `ffmpeg -i in.mp4 -filter_complex "fps=12,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" out.gif` — and keep it well under 10 MB, a common inline-rendering ceiling (it is GitHub's).
- **Media is never committed to the repo.** Upload every artifact via the `to-web` sibling — the bucket bound in `platform.md` § Artifact store is its permanent home — and embed by the returned URL. The URLs are immutable and unguessable; main carries no media, ever. Absent the `to-web` sibling, say so and stop: state the requirement rather than committing media as a silent fallback.
- Name uploads so the key says what it proves: `c<criterion>-<what-it-shows>.png`.

## Presentation — artifacts must render inline

The contract is binding-independent: the deliverable is a **ready-to-paste block** grouped by the acceptance criterion each artifact proves, every artifact rendering inline where the review happens — a click-through link defeats the evidence. This step is detached from PR creation: the PR body holds an evidence placeholder waiting for it (see `change-description.md`); standalone there may be no PR at all. Upload the artifacts, build the block, verify it mechanically, and hand it back to the invoking thread — do not post, attach, or comment anything from this step.

- Embed form — one line per artifact, wrapped so the inline image click-opens full size: `[![<criterion>](<url>)](<url>)`, where `<url>` is the `to-web` URL.
- **Verify mechanically, not by eye** — the agent often cannot view the rendered page. Before handing the block back, check each artifact: image markdown syntax; the URL answers (an HTTP `200` with an image content type); the extension is PNG/JPEG/GIF, never MP4 — review surfaces generally cannot render video inline. These checks catch the known failure modes without a browser.
- When `environment.md` names a browser driver that can reach the review surface, the invoking thread additionally eyeballs the rendered body after it swaps the block in — this step posts nothing, and the eyeball never substitutes for the mechanical checks.
- Local binding: the review file (`platform.md` § Change review) uses the same URL embeds, which render in any markdown viewer with no repo-relative path plumbing. When the human reviews away from the machine, the `to-tailnet` skill (where installed) may serve the rendered review file on demand — the committed file stays the source of truth.
- Other bindings: recorded by `backlog setup` when the review surface renders external images differently — the embed form that renders inline there, its known failure modes, and a mechanical check per artifact, verified at setup per `platform.md` § Custom bindings.
