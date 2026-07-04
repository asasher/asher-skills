# Playbook: Evidence

> Project playbook for this repo. The triage `evidence` subskill reads this file for what to capture, the format/storage contract, and the presentation contract that makes artifacts render for the human; the gates are in the skill's `reference/evidence.md`. How to run, seed, and authenticate against the app — and the capture drivers — are in `environment.md`. The PR body outline that consumes the prepared evidence block is in `pr.md`.

## What to capture

- What evidence this repo expects for a change, beyond green checks (e.g. before/after for visual changes; none for pure logic): _<add yours>_.
- Captured once, after the verify loop converges, each artifact mapped to the acceptance criterion it proves.

## Format and storage

- Static states: PNG or JPEG screenshots.
- Flows: record MP4 for local inspection, then convert the seconds that show the criterion (≤ ~10s) to a GIF with a two-pass palette — `ffmpeg -i in.mp4 -filter_complex "fps=12,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" out.gif` — and keep it well under 10 MB, GitHub's rendering ceiling.
- Commit the PNG/JPEG/GIF artifacts under `evidence/<slug>/` — never the MP4: GitHub cannot render a committed video inline at all, in any form.

## Presentation — artifacts must render inline

> Mode set by `setup` from the repo's visibility. GitHub renders committed images inline only through SHA-pinned raw URLs, and only in public repos — its image proxy cannot authenticate to private ones, and there is no API or CLI path to the drag-and-drop attachment CDN.

- **This step is detached from PR creation.** The PR body holds an evidence placeholder waiting for it (see `pr.md`); standalone there may be no PR at all. Either way the deliverable is a ready-to-paste markdown block: commit the artifacts, push the branch (the URLs below only resolve for a pushed SHA), build the block against that commit, verify it mechanically, and hand it back to the invoking thread — do not post, attach, or comment anything from this step. The thread swaps the block in for the PR body's placeholder.
- Presentation mode: _<public-inline | private-links>_.
- **public-inline** — one line per artifact, destined for the PR body: `![<criterion>](https://github.com/<owner>/<repo>/raw/<commit-sha>/evidence/<slug>/<file>.png)`. Always image syntax with a `/raw/<commit-sha>/` URL: a blob URL or a bare link renders as a link the human must click through, which defeats the evidence. Pin to the commit SHA (survives rebases and branch deletion) and push before posting — an unpushed commit shows a broken image. For an oversized capture, `<img src="…" width="700">` keeps it readable in place.
- **private-links** — inline embeds render broken in private-repo PR bodies (the image proxy cannot authenticate), so present labeled per-criterion links and say why. Open the evidence section with `Committed under evidence/<slug>/ at <short-sha> (plain links — private repo)`, then one line per criterion: `Criterion N (<what it proves>): [<file>](https://github.com/<owner>/<repo>/blob/<commit-sha>/evidence/<slug>/<file>.png)` — the blob page renders the artifact for anyone with repo access. When artifacts are many, additionally commit `evidence/<slug>/index.md` referencing them by relative path with `![]` syntax and one caption per criterion — that page renders everything inline, one click total — and link it at the top of the section.
- Group artifacts by the acceptance criterion they prove, one caption each.
- **Verify mechanically, not by eye** — the agent often cannot view the rendered page (no authenticated browser session; `gh` returns raw markdown, not the render). Before handing the embed block to the PR step, check each artifact: image syntax with a `/raw/<commit-sha>/` URL (no blob URLs, no bare links); the SHA is on the remote (`gh api repos/<owner>/<repo>/commits/<sha>` — 404 means unpushed); the file exists at that path in that commit (`git cat-file -e <sha>:evidence/<slug>/<file>`); the extension is PNG/JPEG/GIF, never MP4. In `private-links` mode the same SHA and path checks apply to each blob link, and to every relative reference in `index.md` if one was committed. These checks catch every known failure mode without a browser.
- When `environment.md` names a browser driver that can reach GitHub, additionally eyeball the rendered PR body after posting — but never substitute the eyeball for the mechanical checks.
