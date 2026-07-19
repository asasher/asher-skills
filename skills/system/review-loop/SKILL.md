---
name: review-loop
description: Present a rendered HTML artifact for human sign-off and block until the verdict; also sweeps dead hub entries.
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
- **serve** — run `scripts/review-server.py` with the flags in [scripts](reference/scripts.md).
- **stop** — `scripts/review-server.py --stop --state <dir>`; verified and idempotent.
- **await** — `scripts/review-await.py --state <dir> --timeout <secs>`; exits `0` approve, `3` nits, `10`
  changes, `124` timeout. Delegate the wait to a watcher — a pure wait-and-relay job staffed by the cheapest
  harness-native model the roster's published Floor allows ([watch](reference/watch.md) § Who holds it — a
  floor-staffed watcher subagent): it only runs the await script and relays the verdict and comments to the
  parent, no synthesis. Never park the orchestrator or poll `events.jsonl`.
- **sweep** — `scripts/review-server.py --sweep --surface <dir>` removes dead hub rows.

With a rendered artifact and no command, serve then await.

## Loop contract

Load [review-loop](reference/review-loop.md) and [surface-and-hub](reference/surface-and-hub.md). Serve-time
chrome leaves the committed HTML unchanged. Feedback submits one batched verdict anchored to stable element
ids. Approval must match the current content hash. On changes, disposition every annotation before re-arm;
approve only ends the loop. Stop the worker when the owning workflow is terminal.

Missing staffing runs the watcher on the current model in a subagent and reports the gap.

## Dependency surface

- **Bundled:** setup, loop, surface, watch, and CLI references plus `scripts/` and annotation chrome.
- **Project:** the presentation section under `docs/agents/`.
- **Sibling:** optional `staffing`, used only for the watcher; no sibling files are imported.
