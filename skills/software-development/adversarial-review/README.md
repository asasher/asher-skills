# Adversarial Review

Converges a change request to LGTM by alternating bounded reviewer and fixer passes that share
nothing but the change request itself: a reviewer pass (code-review, findings as anchored comments,
LGTM when a pass is clean and priors are addressed) and a fixer pass (fix or argue each finding,
reply per comment) — sequenced by the session driving the loop, which holds its turn until the loop
converges or hits a bound (timeout, iteration cap).

## When to use

- A change request exists and should reach review-ready without a human driving the loop.

## Dependency surface

- **Bundled:** `reference/conduct.md` — both roles' briefs: comment conduct, the LGTM bar, iteration
  state, the product-semantics ruling.
- **Siblings (required, by name):** `code-review`, `to-subagent`.
- **Siblings (optional, by name):** `diagnosing-bugs` — the fixer's route for findings reproducible
  only at runtime.

## Provenance

- **Source:** the reviewer ⇆ fixer convergence shape descends from Cursor's MIT-licensed
  [`thermo-nuclear-code-quality-review`](https://github.com/cursor/plugins/blob/a29f5a8ca161b1de4ffc5484454958bebc04eaa5/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md),
  via this repo's earlier `backlog` skill.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
