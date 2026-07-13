---
name: review-loop
description: Present a rendered HTML artifact — a plan, prototype, maquette, or doc — to a human for sign-off, and block until a verdict. Use to serve an artifact for review, await the verdict, or sweep dead hub entries — directly or from a sibling skill that needs a sign-off gate. Not for writing the artifact.
argument-hint: "[setup | serve <artifact.html> | stop | await | sweep]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: []
  optional: [staffing]
  setup: reference/setup.md
---

# Review Loop

Owns rendered-HTML sign-off: detached serving, anchored annotations, hash-bound verdicts, revision ledger,
and repo hub. It never authors the artifact.

## Commands

- **setup** — reconcile only the project's presentation section via [setup](reference/setup.md).
- **serve** — run `scripts/review-server.py` with the flags in [scripts](reference/scripts.md). Return only
  after the detached worker passes its authenticated identity check; its lifetime is independent of this turn
  and any watcher.
- **stop** — `scripts/review-server.py --stop --state <dir>`; verified and idempotent.
- **await** — `scripts/review-await.py --state <dir> --timeout <secs>`; exits `0` approve, `3` nits, `10`
  changes, `124` timeout. Hold the loop-until-verdict wait on a dedicated Floor-class watcher selected with
  `staffing route <watcher task>`; completion wakes the parent. Never park the orchestrator or poll
  `events.jsonl`.
- **sweep** — `scripts/review-server.py --sweep --surface <dir>` removes dead hub rows.

With a rendered artifact and no command, serve then await.

## Loop contract

Load [review-loop](reference/review-loop.md) and [surface-and-hub](reference/surface-and-hub.md). Serve-time
chrome leaves the committed HTML unchanged. Feedback submits one batched verdict anchored to stable element
ids. Approval must match the current content hash. On changes, disposition every annotation before re-arm;
approve only ends the loop. Stop the worker when the owning workflow is terminal.

Missing surface config degrades to local open—never a public tunnel. Missing staffing runs the watcher on the
current model in a subagent and reports the gap.

## Dependency surface

- **Bundled:** setup, loop, surface, watch, and CLI references plus `scripts/` and annotation chrome.
- **Project:** the presentation section under `docs/agents/`.
- **Sibling:** optional `staffing`, used only for the watcher; no sibling files are imported.
