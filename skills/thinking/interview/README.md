# Interview

Interviews the user relentlessly until shared understanding is real, walking the work's **design tree** in
**frontier rounds**: every currently-askable question in one numbered round, each with a recommended
answer. Facts are looked up, never asked; provided artifacts are read, not asked about; the session is
done when the frontier is empty and the user confirms shared understanding.

## When to use

- An idea, problem, PDF, or half-formed direction needs its decisions surfaced and settled before spec,
  tickets, or a build.

## Shape

- **Intake first** — whatever the opening message hands over is read before the first question.
- **Frontier rounds** — the whole unblocked set per round, numbered, each with a recommended answer; a
  question depending on one still open this round waits for a later round.
- **Facts vs decisions** — environment facts dispatched via `to-subagent` (a running lookup blocks only
  its downstream questions); decisions go to the user and wait.
- **Done** — frontier empty, nothing silently assumed, and the user confirms shared understanding before
  anyone acts on it.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Siblings (optional, by name):** `to-subagent` — fact lookups; absent it, facts are looked up
  in-session.

## Provenance

- **Sources:** Matt Pocock's MIT-licensed
  [`batch-grill-me`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/in-progress/batch-grill-me/SKILL.md)
  (frontier scheduling, rounds, facts-not-asked) and
  [`grilling`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/productivity/grilling/SKILL.md)
  (decisions-are-the-user's, shared-understanding confirmation). License in `THIRD_PARTY_LICENSES.md`.
- **Local changes:** intake-first artifact ingestion; fact lookups dispatched through the `to-subagent`
  skill.
