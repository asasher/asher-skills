# Adversarial Review

Converges a change request to LGTM with two concurrent subagents that share nothing but the change
request itself: a reviewer (code-review per pass, findings as anchored comments, re-review on new
commits, LGTM when a pass is clean and priors are addressed) and a fixer (fix or argue each finding,
reply per comment, stop on LGTM) — both bounded by a deadline and an iteration cap.

## When to use

- A change request exists and should reach review-ready without a human driving the loop.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Siblings (required, by name):** `code-review`, `watch-until`, `to-subagent`.

## Provenance

- **Source:** the reviewer ⇆ fixer convergence shape descends from Cursor's MIT-licensed
  [`thermo-nuclear-code-quality-review`](https://github.com/cursor/plugins/blob/a29f5a8ca161b1de4ffc5484454958bebc04eaa5/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md),
  via this repo's earlier `backlog` skill.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
