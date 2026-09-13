---
name: to-tailnet
description: Serve a local HTML artifact over the private Tailscale network for viewing from the user's devices.
disable-model-invocation: true
---

# to-tailnet

Serve a local HTML artifact over the tailnet. The consuming repo's `docs/agents/environment.md` records the tailnet host, port ranges, and any reverse-proxy rules where the repo has them — honor them; absent any record, bind to the machine's Tailscale address and report the artifact's exact URL.

Serving is **detached**: the server outlives this turn.

## Serve

Serve the unchanged file from its directory through a detached HTTP server on a free port; the reported URL ends in the file's name. Verify that exact URL returns HTTP 200 and the artifact's content. Report where verification ran: a local fetch proves the endpoint responds from the serving machine; remote-device reachability requires a check from another tailnet device.

## Report

Done when the user has the exact URL and working, copy-pasteable shutdown instructions for the server.
