# Shape

Settles one subject's strategic decisions — an idea, or one or more tickets grouped as a subject — in an
interactive session: the interview runs in frontier rounds, the domain model is written as terms land,
and questions the conversation can't settle are dispatched out (research for sources, prototype for
artifacts). Stateful: the record lives in the ticket thread, `CONTEXT.md`, and ADRs, and a resumed
session re-asks nothing the record answers. Crystallising the settled direction — a spec, tickets, or
straight to a build — is the user's call, and shape stamps no tracker lifecycle labels.

## When to use

- Work needs its strategic decisions settled before anything builds on it.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Siblings (required, by name):** `interview`, `domain-modeling`.
- **Siblings (optional, by name):** `research`, `prototype`, `to-subagent` (their dispatch).
- **Project surface:** the instruction file's `## Context documents` index; the tracker binding in
  `docs/agents/platform.md` when the subject is a ticket.

## Credits

The batch-frontier questioning style grew out of Matt Pocock's `batch-grill-me` and `grilling` skills
(MIT), via this repo's `interview` skill — see its README for the full lineage.
