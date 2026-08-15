# Shape

Settles one subject's strategic decisions — an idea or a ticket — in an interactive thread: interview rounds inline, terms and ADR drafts modeled into the spec's context delta as they land, and questions the conversation can't settle dispatched out (research for sources, prototype for artifacts). Stateful: the record lives in the ticket thread and on the subject's artifact branch, and a resumed session re-asks nothing the record answers. A settled subject crystallises automatically: to-spec writes the spec as an HTML file on the artifact branch, diagram first, and projects it onto the ticket — summary, render link, commit hash. The thread then watches the spec'd ticket for AFK comments — tweaks applied as branch commits and replied to — until the user's blessing, which records the hash it covers; any later commit past that hash mechanically invalidates readiness. A shaping thread never merges anything: the artifact branch is the record, a clean worktree removal the only teardown, and the context delta reaches main only through the build that makes it true. A recommended split runs to-slices only on the user's approval; shape stamps nothing of its own judgment. Mid-thread items that aren't the subject are offered to to-backlog for capture.

## When to use

- Work needs its strategic decisions settled before anything builds on it.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Siblings (required, by name):** `interview`, `domain-modeling`, `to-spec`, `worktree`.
- **Siblings (optional, by name):** `research`, `prototype`, `to-subagent` (their dispatch), `to-slices` (the approved split), `to-backlog` (mid-thread capture), `watch-until` (the comment watch), `plain-language` (the communication standard).
- **Project surface:** the instruction file's `## Context documents` index; the tracker and branch bindings in `docs/agents/platform.md` when the subject is a ticket.

## Credits

The frontier questioning style grew out of Matt Pocock's `batch-grill-me` and `grilling` skills (MIT), via this repo's `interview` skill — see its README for the full lineage.
