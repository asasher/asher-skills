---
name: retro
description: Review recent local build and shaping transcripts, compare friction with project issues, and propose tracker changes for the user's selection.
metadata:
  requires: [capture]
---

# Retro

Sweep recent work for problems worth fixing in this project. Run the sweep when requested; findings become tracker changes only after the user's selection. Upstream escalation belongs to whoever later resolves the issue.

1. Resolve this repository's local transcripts and [checkpoint](reference/checkpoint.md), including sessions from linked worktrees. Use the harness's session index or metadata to select completed build and shaping sessions. First run: the latest three. Later runs: the next three new or updated sessions after the checkpoint, oldest first. A user-specified scope overrides this default. State the selected sessions and any access gaps; read their transcripts before drawing conclusions.
2. Identify concrete friction: repeated corrections, misunderstood instructions, broken tooling, failed verification, or recovery trouble. Separate observed failures from suspected causes. Group the same problem; one well-supported occurrence can justify a proposal.
3. Search this project's open and closed issues for each finding. Read likely matches and their comments. Classify it as a new issue, additional evidence for an open issue, already covered, or a possible regression after closure. If tracker access is unavailable, disclose that duplicate checking is incomplete.
4. Present a compact table with the problem, evidence, matching issue, and proposed action. Offer the exact new issue or comment for selection. Keep credentials and unrelated transcript details private. Wait for the user's decisions; dismissal is a valid outcome.
5. Use `capture` for selected new issues, scoped to the approved findings. Add only selected comments to existing issues. Verify each tracker write and return its link. Leave implementation and upstream reporting to the resulting work.
6. After the discussion and selected writes are complete, advance the checkpoint through the reviewed batch, including dismissed findings. If there are no actionable findings, checkpoint the completed review directly. Report remaining sessions and offer another batch.

The checkpoint records review coverage; project issues hold accepted findings. An interrupted discussion or failed write leaves the batch pending; check existing issues again before retrying.
