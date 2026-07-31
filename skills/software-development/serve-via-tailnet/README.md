# Serve via Tailnet

Exposes a local HTML artifact on the tailnet so the user can view it from any of their devices — plain detached serving for
view-only artifacts, or the bundled annotation surface (`scripts/review-server.py` +
`scripts/review-await.py`): serve-time chrome injection over a byte-pure file, comments anchored to
stable element ids, batched feedback with hash-bound verdicts, and a per-repo hub of live surfaces.

## When to use

Only when the user explicitly asks for it — no skill or session routes here by default.

- A rendered artifact (spec, prototype answer sheet, report) needs human eyes on another device.
- A review needs structured talk-back: anchored comments plus an approve / nits / request-changes
  verdict a waiting session can block on.

## Dependency surface

- **Bundled:** `scripts/review-server.py`, `scripts/review-await.py`, `scripts/pages/` (annotation
  chrome), `reference/annotation-contract.md`, `reference/scripts.md`, `reference/surface-and-hub.md`.
- **Project playbooks:** the consuming repo's `docs/agents/environment.md` — tailnet root, ports,
  proxy rules, where the repo records them.
- **Siblings:** none.
