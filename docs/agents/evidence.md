# Playbook: Evidence

> Project playbook for this repo. The backlog `evidence` subskill reads this file for what to capture, the format/storage contract, and the presentation contract that makes artifacts render for the human; the gates are in the skill's `reference/evidence.md`. How to run, seed, and authenticate against the app — and the capture drivers — are in `environment.md`; the review surface this presents to is bound in `platform.md`. The PR body outline that consumes the prepared evidence block is in `change-description.md`. Keep the presentation section for this repo's bound review surface; the others are reference for a rebind.

## What to capture

This repo is the **no-running-app case**: there is no product surface to drive, so the honest proof is the probe-eval transcript (plus rendered-HTML screenshots for the skills that emit one). On a repo *with* a running app, evidence would instead be real check/test output plus screenshots driven through the actual app — a probe transcript is not a substitute there. Here, probes are the substitute because there is nothing else to drive.

Evidence is proof of a separate checked criterion, not a catch-all for anything a human reviews. Research
briefs, source packets, findings, and rendered research reports stay under `research/` (or the owning
`<skill>-workspace/research/` route in `researching.md`). A research dossier's citations and claim audit are
intrinsic provenance; do not copy the dossier into `evidence/`. Likewise, plans and prototypes remain in their
own canonical locations. A screenshot or probe transcript proving a change to one of those artifacts may be
evidence; the artifact itself is not.

Per change type — tuned for a skills repo, where the proof is usually an eval transcript, not a screenshot:

- Skill behavior change (SKILL.md, references, routing): the **probe-eval result** — the executor transcript plus a pass/fail table mapping each probe to its answer-key criterion (`docs/agents/probe-evals.md`). For a reworked skill, show the before/after verdict shift on the scenarios that motivated the change.
- Script change (stdlib Python): the terminal transcript of `python3 -m py_compile <script>` plus the script driven through the changed path (e.g. `review-server.py --sweep` output).
- Skill that renders a visual artifact (`maquette`, a generated plan/prototype HTML): before/after screenshots of the rendered HTML; a short GIF for an interaction flow.
- Pure docs/prose change: nothing beyond the diff and a note on which contract it satisfies — no artifact.
- Repo-specific expectations beyond these: an eval transcript is the default proof for anything touching a skill's behavior; a green "it renders" screenshot alone is not enough when the change is about *what the skill decides*.

Captured once, after adversarial review converges, each artifact mapped to the acceptance criterion it proves.
Styling-only verification captures may be reused only when their HEAD is the final reviewed HEAD and the
Reviewer records **“no product-code change; no recapture”**; product-code, fixture, environment, or HEAD drift
forces fresh final-HEAD evidence.

## Format and storage

- Static states: PNG or JPEG screenshots.
- Flows: record MP4 for local inspection, then convert the seconds that show the criterion (≤ ~10s) to a GIF with a two-pass palette — `ffmpeg -i in.mp4 -filter_complex "fps=12,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" out.gif` — and keep it well under 10 MB, a common inline-rendering ceiling (it is GitHub's).
- Commit the PNG/JPEG/GIF artifacts under `evidence/<slug>/` — never the MP4: review surfaces generally cannot render a committed video inline, GitHub not in any form.
- Name files `c<criterion>-<what-it-shows>.png` — they also render in the change's file view.

## Presentation — artifacts must render inline

The contract is binding-independent: the deliverable is a **ready-to-paste block** built against the published evidence commit, grouped by the acceptance criterion each artifact proves, every artifact rendering inline where the review happens — a click-through link defeats the evidence. This step is detached from PR creation: the PR body holds an evidence placeholder waiting for it (see `change-description.md`); standalone there may be no PR at all. Commit the artifacts, publish the branch, build the block, verify it mechanically, and hand it back to the invoking thread — do not post, attach, or comment anything from this step. The mechanics below are per review-surface binding.

### GitHub binding

> GitHub renders committed images inline through same-origin `github.com` blob URLs with `?raw=1` — those are not camo-proxied, so they render on public and private repos alike (private: for viewers with repo access). `raw.githubusercontent.com` and `/raw/<sha>/` URLs ARE camo-proxied and 404 on private repos; there is no API or CLI path to the drag-and-drop attachment CDN.

- Push the branch before building the block — the URLs below only resolve for a pushed SHA.
- Embed form — one line per artifact, wrapped so the inline image click-opens full size:
  `[![<criterion>](https://github.com/<owner>/<repo>/blob/<commit-sha>/evidence/<slug>/<file>.png?raw=1)](https://github.com/<owner>/<repo>/blob/<commit-sha>/evidence/<slug>/<file>.png)`
- Never `raw.githubusercontent.com`, never `/raw/<sha>/`, never a plain non-embedded link.
- SHA reachability is the one failure mode: a rebase or force-push orphans the pinned commit and GitHub 404s the blob. Pin to the branch-head SHA at capture time and re-pin after any history rewrite. A broken embed is almost always an orphaned SHA — re-pin it (or use a branch-name ref `.../blob/<branch>/...?raw=1`, which follows head); do not "fix" it by switching to plain links.
- **Verify mechanically, not by eye** — the agent often cannot view the rendered page (`gh` returns raw markdown, not the render). Before handing the block back, check each artifact: image syntax with a `blob/<commit-sha>/…?raw=1` URL; the SHA is on the remote (`gh api repos/<owner>/<repo>/commits/<sha>` — 404 means unpushed or orphaned); the file exists at that path in that commit (`git cat-file -e <sha>:evidence/<slug>/<file>`); the extension is PNG/JPEG/GIF, never MP4. These checks catch every known failure mode without a browser.
- When `environment.md` names a browser driver that can reach GitHub, the invoking thread additionally eyeballs the rendered PR body after it swaps the block in — this step posts nothing, and the eyeball never substitutes for the mechanical checks.

### Local binding

The review file (`platform.md` § Change review) lives on the same branch as the artifacts, so embeds are **repo-relative paths** — `![<criterion>](../../evidence/<slug>/<file>.png)` relative to the review file — which render in any markdown viewer and on the presentation surface alike, with no SHA pinning and no proxy pitfalls.

- Mechanical checks before handing the block back: each path resolves from the review file's location at the branch's HEAD (`git cat-file -e HEAD:evidence/<slug>/<file>`); the extension is PNG/JPEG/GIF, never MP4.
- When the human reviews away from the machine, the evidence step may additionally publish the rendered review file to the presentation surface (`environment.md` § Presenting) — the committed file stays the source of truth, served in place by the `review-loop` skill. Publishing must preserve relative-path resolution: expose the review file *with* its `evidence/` tree (publish a directory root, not the lone file), or skip the publish — a page of broken embeds fails the gate.

### Other bindings

Recorded by `backlog setup` when the review surface is neither of the above: the embed form that renders inline there, its known failure modes, and a mechanical check per artifact — verified at setup, per `platform.md` § Custom bindings.
