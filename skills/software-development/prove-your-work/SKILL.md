---
name: prove-your-work
description: Publish reproducible, current-revision evidence on a PR so a human can review the change without watching the build.
metadata:
  requires: [to-web]
  optional: [technical-writing]
---

# Prove your work

Read the accepted verification report. Reuse tool steps, commands, scripts, outputs, and captures only when head, base, spec revision, environment, and relevant fixtures match. Inspect reused visuals yourself. Recapture missing or stale proof; a defect returns to the existing review loop before packaging continues.

## Package

Use `technical-writing` when available. Include:

- What changed and why, naming the checked head and base.
- Every claim or acceptance criterion with its verdict, exact check, useful output, and evidence.
- Reproduction details, including fixture setup, browser actions and observations, and the exact contents or durable source of removed temporary scripts.
- Data-safety evidence for destructive operations.
- Each unverified claim, pre-existing failure, and explicit waiver with its reason.

For UI claims, include inspected screenshots of static states and recordings or GIFs when motion or interaction proves the criterion. Images must show the claimed result legibly without clipping. If a preview is unavailable, use a labeled local run; if that too is inaccessible, record the verification gap.

## Publish

Upload the HTML report and media through `to-web`. Keep evidence images, screenshots, MP4s, and GIFs out of Git; failed publication leaves the package incomplete. Preserve tool steps, commands, and any script text in the published report so temporary branches can later be deleted.

Use PNG/JPEG for states. For flows, capture MP4 and make a short GIF when inline playback helps. See [media](reference/media.md) for conversion and embedding. Link videos; embed images and GIFs. Fetch every URL and verify its content type; visually inspect each embed's source.

Recheck the PR head and target base before posting. A moved input needs renewed verification. Post the package as a PR comment and link it from the body, within the task's existing publication authorization.

Complete when every claim has evidence or an explicit gap, every URL works, every visual was inspected, and the package identifies the current revisions. Claims with gaps retain their unverified verdict.
