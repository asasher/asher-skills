# Code Review

Two-axis review against pinned head and base revisions: **Standards** covers documented repo rules and concrete structural costs; **Spec** covers missing, incorrect, or unrequested behavior. A coherent change uses one context for both axes. Larger reasoning loads can split the axes into concurrent read-only subagents. Blocking findings and optional suggestions are reported separately.

## Dependency surface

Composes with the optional `to-subagent` sibling for axis dispatch; reads the issue with `gh` and the spec from the issue's artifact branch at its blessed hash; the smell baseline and structural bar are bundled under `reference/`.

## Provenance

- **Sources:** Matt Pocock's MIT-licensed [`code-review`](https://github.com/mattpocock/skills/tree/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/code-review) (two-axis structure, smell baseline, aggregation rules); Cursor's MIT-licensed [`thermo-nuclear-code-quality-review`](https://github.com/cursor/plugins/blob/a29f5a8ca161b1de4ffc5484454958bebc04eaa5/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md) (the structural bar: ambition directive, presumptive blockers, remedies, weighting, clean-pass criteria). Licenses in `THIRD_PARTY_LICENSES.md`.
- **Local changes:** dispatch through `to-subagent` with an in-session degrade; base ref defaults to the PR base or merge-base with the default branch; spec discovery reads the issue's spec projection.
