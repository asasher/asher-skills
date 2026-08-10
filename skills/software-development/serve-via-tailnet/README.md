# Serve via Tailnet

Exposes a local HTML artifact on the tailnet so the user can view it from any of their devices — a plain detached stdlib HTTP server over the file in place, the URL reported with its stop command.

## When to use

Only when the user explicitly asks for it — no skill or session routes here by default.

- A rendered artifact (spec, prototype answer sheet, report) needs human eyes on another device.

## Dependency surface

- **Bundled:** none.
- **Project playbooks:** the consuming repo's `docs/agents/environment.md` — tailnet root, ports, proxy rules, where the repo records them.
- **Siblings:** none.
