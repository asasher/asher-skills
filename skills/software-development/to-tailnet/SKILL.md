---
name: to-tailnet
description: Serve a local HTML artifact over the tailnet so the user can view it from any of their devices. Use when a rendered artifact needs human eyes on another device; never the default way to present an artifact.
argument-hint: "<artifact.html>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: []
---

# Serve via Tailnet

Expose a local HTML artifact on the tailnet and hand the user its URL. The consuming repo's `docs/agents/environment.md` records the tailnet root, port ranges, and any reverse-proxy rules where the repo has them — honor them; absent any record, bind to the tailscale interface address and report `http://<tailnet-host>:<port>/...`.

Serving is **detached**: the server outlives this turn, and the URL is reported with how to stop it.

## Serve

Serve the file (or its directory) with a detached stdlib HTTP server on a free port, verify it answers, report the URL. The file is served in place — no chrome, no state, no diverging copy.

## Report

The URL the user opens, and the stop command.
