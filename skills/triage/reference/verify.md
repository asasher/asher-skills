# Verify

Target: a branch, working tree, or PR. Runs standalone or as the verify step of the loop.

Read `docs/agents/verifying.md` for this repo's check commands and which evidence is required, and `docs/agents/environment.md` for how to run and authenticate against the app. If either is missing, report a setup gap and stop.

## Steps

1. Run the checks.
   - Run the narrowest meaningful checks first, then the broader checks `verifying.md` requires for the touched surface.
   - Completion criterion: every check the PR will claim has been run, with its result known.

2. Capture evidence.
   - Capture only the evidence `verifying.md` requires. Access and run the app per `environment.md`.
   - Store artifacts under `evidence/<slug>/`: static visuals as PNG/JPEG; short flows recorded as MP4 for local inspection, converted to a small GIF, and committed.
   - The PR body is the index for a change's evidence — each artifact is linked or embedded there (see the create-PR step in `reference/issue-loop.md`). Do not add a separate index file.
   - Completion criterion: the evidence `verifying.md` requires exists under `evidence/<slug>/` ready to embed in the PR, or none is required.
