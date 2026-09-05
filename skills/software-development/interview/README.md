# Interview

Interviews the user relentlessly until shared understanding is real, walking the work's **design tree** in **frontier rounds**: every currently-askable question in one round, each numbered with a recommended answer. Facts are looked up, never asked; intake is read before the first round; the session is done when the frontier is empty and the user confirms shared understanding.

## When to use

- An idea, problem, PDF, or half-formed direction needs its decisions surfaced and settled before spec, issues, or a build.

## Dependency surface

Composes with three optional siblings: `writing-for-humans` for user-facing text, `to-subagent` for fact lookups, and `capture` for off-tree items.

## Provenance

- **Sources:** Matt Pocock's MIT-licensed [`batch-grill-me`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/in-progress/batch-grill-me/SKILL.md) (frontier scheduling, rounds, facts-not-asked) and [`grilling`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/productivity/grilling/SKILL.md) (decisions-are-the-user's, shared-understanding confirmation). License in `THIRD_PARTY_LICENSES.md`.
- **Local changes:** intake-first artifact ingestion; fact lookups dispatched through the `to-subagent` skill.
