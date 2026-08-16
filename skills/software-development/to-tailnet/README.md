# Serve via Tailnet

Exposes a local HTML artifact on the tailnet so the user can view it from any of their devices — a plain detached stdlib HTTP server over the file in place, the URL reported with its stop command.

## When to use

- A rendered artifact (spec, prototype answer sheet, report) needs human eyes on another device — on the user's ask, or when the session judges another device is the right surface.
- Never the default way to present an artifact — repo playbooks name the standing presentation routes.

## Dependency surface

No sibling skills; reads the consuming repo's tailnet bindings from `docs/agents/environment.md` where recorded.
