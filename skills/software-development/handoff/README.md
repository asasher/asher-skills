# Handoff

Compacts the current conversation into a handoff document in the OS temp directory, for a fresh agent to continue from; mechanics in `SKILL.md`.

## When to use

- Ending a session whose work another session will continue.
- Seeding a `to-thread` or `to-subagent` dispatch with a starting prompt richer than one paragraph.

## Provenance

- **Source:** Matt Pocock's MIT-licensed [`handoff`](https://github.com/mattpocock/skills/tree/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/productivity/handoff), near-verbatim. License in `THIRD_PARTY_LICENSES.md`.
