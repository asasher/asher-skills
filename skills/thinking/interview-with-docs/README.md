# Interview With Docs

The composed entry point to the lifecycle's shaping stage: run the `interview` skill with the
`domain-modeling` skill active throughout, so the useful shape is written down the moment it crystallises —
glossary terms into `CONTEXT.md`, three-gate decisions into ADRs — and everything else deliberately
evaporates with the conversation. Extraction over transcript: downstream synthesis (`to-spec`, `to-tickets`)
reads crystallised artifacts plus the exit classification of open threads, not chat memory.

## When to use

- The decisions being elicited should outlive the session — they feed a spec, tickets, or future sessions.
- Use bare `interview` instead when nothing durable is wanted.

## Shape

A thin composer, deliberately: both capabilities are siblings invoked **by name**, never files imported.
Absent either sibling it states the requirement and offers the degraded form (bare interview, classification
recorded in-conversation only).

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Siblings (required, by name):** `interview`, `domain-modeling`.

## Provenance

- **Pattern source:** Matt Pocock's MIT-licensed
  [`grill-with-docs`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/engineering/grill-with-docs/SKILL.md)
  — a 7-line composer of `grilling` × `domain-modeling`; this skill is the same composition over our
  `interview`. License in `THIRD_PARTY_LICENSES.md`.
