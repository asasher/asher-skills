# TDD

The red → green loop with the discipline that makes its tests worth keeping: behavior through public
interfaces, tests only at pre-agreed seams, the three anti-patterns (implementation-coupled,
tautological, horizontal slicing), and the loop rules (red before green, one slice at a time, refactoring
excluded from the cycle).

## When to use

- Building a feature or fixing a bug test-first.

## Dependency surface

- **Bundled:** `reference/tests.md` (good/bad test examples), `reference/mocking.md` (mock only at system
  boundaries).
- **Siblings:** none — a sealed primitive.

## Provenance

- **Source:** Matt Pocock's MIT-licensed
  [`tdd`](https://github.com/mattpocock/skills/tree/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/tdd)
  (SKILL.md adapted; `tests.md` and `mocking.md` copied). License in `THIRD_PARTY_LICENSES.md`.
- **Local changes:** seams confirmable against a ticket/spec when no user is present; the refactoring
  rule no longer routes to a named review skill.
