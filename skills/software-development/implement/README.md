# Implement

Thin routing composite: one ticket in, committed changes out. Defects run through `diagnosing-bugs`
(feedback loop, then fix plus regression test); new behavior runs through `tdd` at pre-agreed seams.
Typecheck and touched tests regularly, full suite once at the end, commit to the current branch.

## When to use

- A single ticket or spec'd slice needs building in the current checkout.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Project:** `docs/agents/codebase.md` when present — conventions, check commands, generated-artifact
  recipes.
- **Siblings (required, by name):** `diagnosing-bugs`, `tdd`.

## Provenance

- **Source:** route structure inspired by Matt Pocock's MIT-licensed
  [`implement`](https://github.com/mattpocock/skills/tree/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/implement).
  License in `THIRD_PARTY_LICENSES.md`.
- **Local changes:** explicit bug/enhancement routing; review is separate work downstream.
