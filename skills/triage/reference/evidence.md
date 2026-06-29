# Evidence

Target: a branch whose behavior `reference/verify.md` has confirmed against its acceptance criteria. Terminal capture step — runs once, after the verify loop converges and before the PR. Never run it on a change that has not passed verification; the point is to prove to a human that the criteria are met, so capturing a half-working state defeats it.

Read `docs/agents/verifying.md` for what evidence this repo requires, and `docs/agents/environment.md` for how to stand up, seed, and authenticate against the app. If either is missing, report a setup gap and stop.

## Steps

1. Capture only what is required, mapped to criteria.
   - Capture the evidence `verifying.md` requires for the touched surface, against the now-confirmed-working stack, and tie each artifact to the acceptance criterion it demonstrates. Capture nothing for a change whose playbook requires no evidence beyond green checks.
   - Completion criterion: each required artifact exists and names the criterion it proves, or none is required.

2. Store the artifacts.
   - Store under `evidence/<slug>/`: static visuals as PNG/JPEG; short flows recorded as MP4 for local inspection, converted to a small GIF, and committed.
   - Completion criterion: every artifact is committed under `evidence/<slug>/` ready to embed.

3. Index in the PR body.
   - The PR body is the index for a change's evidence — each artifact is linked or embedded there (see the create-PR step in `reference/issue-loop.md`). Do not add a separate index file.
   - Completion criterion: every artifact is reachable from the PR body, grouped by the criterion it proves.
