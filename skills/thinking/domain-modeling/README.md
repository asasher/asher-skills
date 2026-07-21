# Domain Modeling

Builds and sharpens the project's domain model *while decisions are being made*: challenges terms against
the glossary, sharpens fuzzy language into canonical terms, stress-tests concept boundaries with concrete
scenarios, cross-references claims against the code — and writes the results down **the moment they
crystallise**: terms into `CONTEXT.md` (a glossary and nothing else), decisions passing the three-gate test
(hard to reverse ∧ surprising without context ∧ real trade-off) into one-paragraph ADRs under `docs/adr/`.

## When to use

- Pinning down domain terminology or a ubiquitous language.
- Recording an architectural decision worth remembering.
- Another skill needs the model maintained while it works: `shape` composes it with
  `interview`; groom, spec, and triage sessions may invoke it directly.
- Not for merely *reading* `CONTEXT.md` — consuming the glossary is a one-line habit any skill can do.

## Shape

- Single context by default (`CONTEXT.md` + `docs/adr/` at the root); `CONTEXT-MAP.md` for multi-context
  repos. Files created lazily, on the first real entry.
- Inline writes, never batched; ADRs offered sparingly, behind all three gates.
- Formats bundled: `reference/context-format.md`, `reference/adr-format.md`.

## Dependency surface

- **Bundled:** the two format references.
- **Siblings:** none — callers compose this skill by name.

## Provenance

- **Source:** Matt Pocock's MIT-licensed
  [`domain-modeling`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/engineering/domain-modeling/SKILL.md)
  (adopted nearly wholesale, including the CONTEXT/ADR format references). License in
  `THIRD_PARTY_LICENSES.md`.
- **Local changes:** house frontmatter and composition surface (run-alongside framing, named callers);
  reference filenames lowercased; explicit "glossary and nothing else" boundary retained and promoted.
