# Code Review

Two-axis diff review since a fixed point: **Standards** (documented repo standards plus a Fowler smell
baseline and a structural-ambition bar, repo overriding, everything a judgement call) and **Spec**
(missing requirements, scope creep,
implemented-but-wrong, each finding quoting the spec line). Axes run as separate subagents so neither
pollutes the other, and are reported side by side, never merged or reranked.

## When to use

- Reviewing a change request, a branch, or work-in-progress changes against what was actually asked for
  and how this repo writes code.

## Dependency surface

- **Bundled:** `reference/smells.md` (the smell baseline) and `reference/structure.md` (the structural
  bar), both pasted in full into the Standards brief.
- **Project:** the tracker binding in `docs/agents/platform.md`, for fetching the originating ticket.
- **Siblings (optional, by name):** `to-subagent` — axis dispatch; absent it, both axes run in-session
  sequentially.

## Provenance

- **Sources:** Matt Pocock's MIT-licensed
  [`code-review`](https://github.com/mattpocock/skills/tree/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/code-review)
  (two-axis structure, smell baseline, aggregation rules); Cursor's MIT-licensed
  [`thermo-nuclear-code-quality-review`](https://github.com/cursor/plugins/blob/a29f5a8ca161b1de4ffc5484454958bebc04eaa5/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)
  (the structural bar: ambition directive, presumptive blockers, remedies, weighting, clean-pass
  criteria). Licenses in `THIRD_PARTY_LICENSES.md`.
- **Local changes:** dispatch through `to-subagent` with an in-session degrade; fixed point defaults to
  the change request base or merge-base with the default branch; spec discovery reads the repo's
  `docs/agents/platform.md` binding and `docs/specs/` convention.
