---
name: plain-language
description: The communication standard for user-facing text — ASD-STE100 plain language, the project's CONTEXT.md as the approved technical dictionary, and no opaque ticket or PR numbers. Cite it from any skill that writes to a human; read it before wording an interview round, groom plan, issue or PR body, dispatch declaration, relay, or report.
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Plain language

The one standard for all user-facing text. This is a reference skill: it defines the standard, it never runs as a workflow. Sibling skills cite it by name; each applies it in place.

## The three rules

1. **Simplified Technical English.** User-facing text follows ASD-STE100 discipline: short sentences, active voice, one idea per sentence, simple words. Say what happens and who does it.
2. **The dictionary is the project's context files.** STE pairs a small approved general dictionary with your own technical names — `CONTEXT.md` is that technical dictionary. Use its terms exactly; do not coin synonyms for a term it already defines. The `domain-modeling` sibling maintains the dictionary; a term you need that is missing goes there, not into ad-hoc prose.
3. **No opaque numbers.** Every ticket or PR reference carries its id, its title, and a one-or-two-sentence digest of what it is. Relations are said in words — "#12 (rename capstone) blocks #14 (groom sweep)" — never bare id lists.

## Where it applies

All text a human will read: interview rounds, groom plans, issue and PR bodies, dispatch declarations, outcome relays, status reports, evidence summaries.

## Dependency surface

- **Bundled:** none — this file is the whole standard.
- **Project context:** `CONTEXT.md` and `docs/adr/` supply the vocabulary; no playbook and no setup.
- **Siblings:** `domain-modeling` maintains the dictionary. Absent this skill, callers write plainly and say the standard was not loaded.
