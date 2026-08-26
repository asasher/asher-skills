# Implement

Thin routing composite: one ticket or spec'd work in, committed changes out on the current branch.

## When to use

- A single ticket or spec'd work needs building in the current checkout.

## Dependency surface

Routes defects to the `diagnosing-bugs` sibling and new behavior to `tdd`. Applies the `principle-codebase-design` and `principle-type-system-discipline` siblings, with `typescript-best-practices` for TypeScript when available. Reads `docs/agents/codebase.md` when present.

## Provenance

- **Source:** route structure inspired by Matt Pocock's MIT-licensed [`implement`](https://github.com/mattpocock/skills/tree/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/implement). License in `THIRD_PARTY_LICENSES.md`.
- **Local changes:** explicit defect/new-behavior routing; review is separate work downstream.
