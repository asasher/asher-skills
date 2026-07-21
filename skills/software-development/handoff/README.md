# Handoff

Compacts the current conversation into a handoff document in the OS temp directory: what a fresh agent
needs to continue, a suggested-skills section, references (never copies) to content already captured in
durable artifacts, and sensitive information redacted.

## When to use

- Ending a session whose work another session will continue.
- Feeding a thread or subagent a starting prompt richer than one paragraph.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Siblings:** none — a sealed primitive.

## Provenance

- **Source:** Matt Pocock's MIT-licensed
  [`handoff`](https://github.com/mattpocock/skills/tree/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/productivity/handoff),
  near-verbatim. License in `THIRD_PARTY_LICENSES.md`.
