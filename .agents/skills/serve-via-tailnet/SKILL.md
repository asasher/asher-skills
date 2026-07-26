---
name: serve-via-tailnet
description: Serve a local HTML artifact over the tailnet so the user can view it from any of their devices — plain, or with an annotation surface that collects comments and a verdict. Use whenever a rendered artifact needs human eyes that aren't at this machine.
argument-hint: "<artifact.html> [--annotate]"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: []
---

# Serve via Tailnet

Expose a local HTML artifact on the tailnet and hand the user its URL. The machine's presentation
conventions (the global instruction files' presentation module) record the tailnet root, port ranges, and
any reverse-proxy rules — honor them; absent any, bind to the tailscale interface address and report
`http://<tailnet-host>:<port>/...`.

Serving is **detached**: the server outlives this turn, and the URL is reported with how to stop it.

## Plain serve

For an artifact that only needs viewing: serve the file (or its directory) with a detached stdlib HTTP
server on a free port, verify it answers, report the URL. No chrome, no state.

## Annotated serve

For an artifact that needs a reaction — comments and a verdict — serve it through
`scripts/review-server.py`: it injects the annotation chrome at serve time (the file on disk stays
byte-pure), anchors comments to the artifact's stable element ids, collects batched feedback with one of
three verdicts (approve / approve-with-nits / request-changes) bound to the document's content hash, and
maintains a per-repo hub of live surfaces. `scripts/review-await.py` blocks until the verdict lands.
Contract and CLI: [annotation-contract](reference/annotation-contract.md), [scripts](reference/scripts.md),
[surface-and-hub](reference/surface-and-hub.md).

The artifact must give reviewable elements stable ids; an artifact without them still serves, but
comments can only anchor to whole-document level.

## Report

Whichever mode: the URL the user opens, what device-side action is expected (view / annotate and submit),
and the stop command. When a verdict is expected, say where the verdict lands and what happens on each
outcome.
