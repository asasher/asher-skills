# Serve via Tailnet

Exposes a local HTML artifact on the tailnet from any of the user's devices — plain detached serving for
view-only artifacts, or the bundled annotation surface (`scripts/review-server.py` +
`scripts/review-await.py`): serve-time chrome injection over a byte-pure file, comments anchored to
stable element ids, batched feedback with hash-bound verdicts, and a per-repo hub of live surfaces.

## When to use

- A rendered artifact (spec, prototype answer sheet, report) needs human eyes on another device.
- A review needs structured talk-back: anchored comments plus an approve / nits / request-changes
  verdict a waiting session can block on.

## Dependency surface

- **Bundled:** `scripts/review-server.py`, `scripts/review-await.py`, `scripts/pages/` (annotation
  chrome), `reference/annotation-contract.md`, `reference/scripts.md`, `reference/surface-and-hub.md`.
- **Machine:** the presentation module in the global agent instruction files — tailnet root, ports,
  proxy rules.
- **Siblings:** none.

## Provenance

The annotation surface is the review-loop skill's serving machinery, carried over whole when review-loop
retired in favor of this skill plus `watch-until`.
