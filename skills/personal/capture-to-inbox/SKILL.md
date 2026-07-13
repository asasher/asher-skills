---
name: capture-to-inbox
description: Capture shared text, links, and files through a project-bound queue, then drain them safely into Inbox. Use when a capture queue should be set up or reconciled, when queued captures should be previewed or drained, or when another skill needs the capture-to-Inbox intake capability.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
  setup: reference/setup.md
  external: [{"name":"shortcuts-playground","kind":"codex-plugin","source":"https://github.com/viticci/shortcuts-playground-plugin","capability":"build-apple-shortcuts","version":"1.2.x"}]
---

# Capture to Inbox

Owns one intake path: authenticated Apple Shortcut captures enter a durable project-bound queue, and a drain
appends them to the project's Inbox before marking them drained remotely.

## Commands

- **`setup`** - load [setup](reference/setup.md), [deployment](reference/deployment.md), and
  [shortcut-contract](reference/shortcut-contract.md). Reconcile a consumer-owned instance end to end.
- **`drain`** (default) - run `scripts/drain_capture_queue.py --project <consumer-root>`. Pass through
  `--dry-run`, `--limit <n>`, or `--keep-remote` when requested.

Setup uses `scripts/setup_instance.py` only for deterministic local materialization. Deployment, external
plugin consent, Shortcut generation, signing, and the live smoke test remain effect-verified setup steps.

## Drain Contract

1. Load paths, deployment URL, token name, and private token-file binding from the consumer instance
   configuration. Read the token file first, falling back to the process environment only when the file has
   no matching assignment; never print it.
2. List the queue; a dry run stops after reporting new versus already-recorded Queue IDs.
3. For each new item, verify any payload before an atomic local write, then append one Inbox entry carrying
   `Queue ID: \`<id>\``.
4. Delete that remote item only after every required local write succeeds. A rerun seeing the Queue ID marker
   skips the append and may finish the pending remote delete.
5. Return nonzero when any item fails; never turn a partial drain into a success report.

## Dependency Surface

- **Bundled:** the API template, setup and drain scripts, and the deployment and Shortcut contracts above.
- **Project:** `control-plane/config.json` plus the consumer-owned capture instance and Inbox paths it binds.
- **Siblings:** none. The external `shortcuts-playground` Codex plugin supplies
  `build-apple-shortcuts` during setup; it is not an internal sibling and none of its files are copied here.
