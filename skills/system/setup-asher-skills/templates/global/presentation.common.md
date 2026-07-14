# Machine presentation policy

- Write HTML deliverables—plans, reports, prototypes, and review sheets—as local files in the repo or workspace.
- When Asher is at this machine, open the local file. When he is remote, use the project’s `docs/agents/` tailnet surface. Always open whatever is presented; never only print a link.
- Disk is the default presentation surface. Do not use ChatGPT canvas/site, Claude artifacts, or another harness-hosted page. Publish to a cloud surface only when Asher explicitly asks.
- This machine’s tailnet root is `https://ashers-macbook-pro.tail045dd5.ts.net`; Funnel stays off.
- Before publishing, run `tailscale status`. Run `tailscale up` only when the node is down and something is being published now. Never cycle a healthy connection. If authentication or startup fails, report it and open locally; never enable Funnel or improvise a public tunnel.
- Serve through a stdlib static server and `tailscale serve --bg --set-path /<path> http://localhost:<port>`. On teardown run `tailscale serve --set-path /<path> off`; use `tailscale serve status` for orphan checks.
- The project surface playbook overrides the root path, surface directory, and keep-awake choice.
