# Playbook: Evidence

> Project playbook for this repo. The triage `evidence` subskill reads this file for what to capture, the format/storage contract, and the presentation contract that makes artifacts render for the human; the gates are in the skill's `reference/evidence.md`. How to run, seed, and authenticate against the app — and the capture drivers — are in `environment.md`. The PR body outline that consumes the prepared evidence block is in `pr.md`.

## What to capture

Per change type — the shipped baseline; tune to this repo:

- Pure logic or backend fix: nothing beyond green checks — the targeted test is the proof.
- UI change: before/after screenshots of the changed surface; a short GIF for flows.
- Workflow or auth change: an app-level walkthrough naming the account/state used, the expected result, and the observed result.
- Data or migration change: the migration/command result plus before/after proof that the affected store is safe.
- Repo-specific expectations beyond these: _<add yours, or "none">_.

Captured once, after adversarial review converges, each artifact mapped to the acceptance criterion it proves.

## Format and storage

- Static states: PNG or JPEG screenshots.
- Flows: record MP4 for local inspection, then convert the seconds that show the criterion (≤ ~10s) to a GIF with a two-pass palette — `ffmpeg -i in.mp4 -filter_complex "fps=12,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" out.gif` — and keep it well under 10 MB, GitHub's rendering ceiling.
- Commit the PNG/JPEG/GIF artifacts under `evidence/<slug>/` — never the MP4: GitHub cannot render a committed video inline at all, in any form.
- Name files `c<criterion>-<what-it-shows>.png` — they also render in the PR's Files-changed tab.

## Presentation — artifacts must render inline

> GitHub renders committed images inline through same-origin `github.com` blob URLs with `?raw=1` — those are not camo-proxied, so they render on public and private repos alike (private: for viewers with repo access). `raw.githubusercontent.com` and `/raw/<sha>/` URLs ARE camo-proxied and 404 on private repos; there is no API or CLI path to the drag-and-drop attachment CDN.

- **This step is detached from PR creation.** The PR body holds an evidence placeholder waiting for it (see `pr.md`); standalone there may be no PR at all. Either way the deliverable is a ready-to-paste markdown block: commit the artifacts, push the branch (the URLs below only resolve for a pushed SHA), build the block against that commit, verify it mechanically, and hand it back to the invoking thread — do not post, attach, or comment anything from this step.
- Embed form — one line per artifact, wrapped so the inline image click-opens full size:
  `[![<criterion>](https://github.com/<owner>/<repo>/blob/<commit-sha>/evidence/<slug>/<file>.png?raw=1)](https://github.com/<owner>/<repo>/blob/<commit-sha>/evidence/<slug>/<file>.png)`
- Never `raw.githubusercontent.com`, never `/raw/<sha>/`, never a plain non-embedded link — a click-through defeats the evidence.
- SHA reachability is the one failure mode: a rebase or force-push orphans the pinned commit and GitHub 404s the blob. Pin to the branch-head SHA at capture time and re-pin after any history rewrite. A broken embed is almost always an orphaned SHA — re-pin it (or use a branch-name ref `.../blob/<branch>/...?raw=1`, which follows head); do not "fix" it by switching to plain links.
- Group artifacts by the acceptance criterion they prove, one caption each.
- **Verify mechanically, not by eye** — the agent often cannot view the rendered page (`gh` returns raw markdown, not the render). Before handing the block back, check each artifact: image syntax with a `blob/<commit-sha>/…?raw=1` URL; the SHA is on the remote (`gh api repos/<owner>/<repo>/commits/<sha>` — 404 means unpushed or orphaned); the file exists at that path in that commit (`git cat-file -e <sha>:evidence/<slug>/<file>`); the extension is PNG/JPEG/GIF, never MP4. These checks catch every known failure mode without a browser.
- When `environment.md` names a browser driver that can reach GitHub, additionally eyeball the rendered PR body after posting — but never substitute the eyeball for the mechanical checks.
