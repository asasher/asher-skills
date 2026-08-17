# Domain Modeling

Builds and sharpens the project's domain model _while decisions are being made_: challenges terms against the glossary, sharpens fuzzy language into canonical terms, stress-tests concept boundaries with concrete scenarios, cross-references claims against the code — and writes the results down **the moment they crystallise**. Destinations (the is/will-be test) and the ADR gates live in `SKILL.md`.

## Shape

- Single context by default (`CONTEXT.md` + `docs/adr/` at the root); `CONTEXT-MAP.md` for multi-context repos. Files created lazily, on the first real entry.
- Formats bundled: `reference/context-format.md`, `reference/adr-format.md`.

## Dependency surface

No required siblings; optionally composes `writing-for-humans` (the communication standard).

## Provenance

- **Source:** Matt Pocock's MIT-licensed [`domain-modeling`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/engineering/domain-modeling/SKILL.md) (adopted nearly wholesale, including the CONTEXT/ADR format references). License in `THIRD_PARTY_LICENSES.md`.
- **Local changes:** house frontmatter and composition surface (run-alongside framing, the is/will-be destination routing); reference filenames lowercased; explicit "glossary and nothing else" boundary retained as the first rule in `reference/context-format.md`.
