---
name: to-tailnet
description: Serve a local HTML artifact over the tailnet so the user can view it from any device — the deliberate don't-publish path beside to-web.
argument-hint: "<artifact.html>"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: []
  optional: [docs/agents/environment.md]
---

# to-tailnet

Serve a local HTML artifact over the tailnet. The consuming repo's `docs/agents/environment.md` records the tailnet host, port ranges, and any reverse-proxy rules where the repo has them — honor them; absent any record, bind to the machine's Tailscale address (`tailscale ip -4`) and report `http://<that-address>:<port>/...`.

Serving is **detached**: the server outlives this turn.

## Serve

Serve the file's directory with a detached stdlib HTTP server on a free port; the reported URL ends in the file's name. Then fetch the URL exactly as reported — the fetch itself proves tailnet reachability — and confirm HTTP 200 returning the artifact's content. The file is served in place, unmodified.

## Report

Done when the user has the exact URL and an exact, copy-pasteable stop command (e.g. `kill <pid>` with the server's real PID).
