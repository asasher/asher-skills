# Adversarial Review

Converges a PR to LGTM by alternating bounded reviewer and fixer passes, sequenced by a driver until convergence or a bound — see SKILL.md. Use once a PR exists and should reach LGTM without a human driving the loop.

## Provenance

- **Source:** the reviewer ⇆ fixer convergence shape descends from Cursor's MIT-licensed [`thermo-nuclear-code-quality-review`](https://github.com/cursor/plugins/blob/a29f5a8ca161b1de4ffc5484454958bebc04eaa5/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md), via this repo's earlier `backlog` skill.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
