# Shape

Settles a batch of subjects' strategic decisions — ideas, or tickets grouped into subjects where their
decisions interlock — in an interactive session: one engine per subject (parallel sub-agents for a
batch), interview rounds combined across subjects and relayed to the user, the domain model written as
terms land, and questions the conversation can't settle dispatched out (research for sources, prototype
for artifacts). Stateful: the record lives in the ticket thread, `CONTEXT.md`, and ADRs, and a resumed
session re-asks nothing the record answers. A settled subject crystallises automatically: to-spec lands
the spec on its ticket, diagram first. The thread then watches the spec'd tickets for AFK comments —
tweaks applied and replied to — until the user's explicit readiness signal, which it executes; a
recommended split runs to-tickets only on the user's approval. Shape stamps nothing of its own judgment.

## When to use

- Work needs its strategic decisions settled before anything builds on it.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Siblings (required, by name):** `interview`, `domain-modeling`, `to-spec`.
- **Siblings (optional, by name):** `research`, `prototype`, `to-subagent` (their dispatch and the
  batch's engines), `to-tickets` (the approved split), `watch-until` (the comment watch).
- **Project surface:** the instruction file's `## Context documents` index; the tracker binding in
  `docs/agents/platform.md` when the subject is a ticket.

## Credits

The batch-frontier questioning style grew out of Matt Pocock's `batch-grill-me` and `grilling` skills
(MIT), via this repo's `interview` skill — see its README for the full lineage.
