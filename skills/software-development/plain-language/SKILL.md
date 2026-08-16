---
name: plain-language
description: The communication standard for user-facing text — ASD-STE100 plain language, the project's glossary as the approved technical dictionary, and no opaque ticket or PR numbers. Cite it from any skill that writes to a human; read it before writing text a human will read — a question, a plan, an issue or change-request body, a report.
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Plain language

The one standard for all user-facing text. This is a reference skill: it defines the standard; sibling skills cite it by name and apply it in place.

## The three rules

1. **Simplified Technical English.** User-facing text follows ASD-STE100 discipline: short sentences, active voice, one idea per sentence, simple words. Say what happens and who does it.
2. **The dictionary is the project's glossary.** STE pairs a small approved general dictionary with your own technical names — the project's glossary is that technical dictionary; the conventional location is `CONTEXT.md` at the repo root. Use its terms exactly; do not coin synonyms for a term it already defines. A term you need that is missing goes into the glossary through the project's dictionary-maintenance practice, not into ad-hoc prose. A project without a glossary gets plain words and inline definitions: define a term of art at first use.
3. **No opaque numbers.** Every ticket or PR reference carries its id, its title, and a one-or-two-sentence digest of what it is. Relations are said in words — "#12 (rename the parent work-type) blocks #14 (the routing sweep)" — never bare id lists.

## Where it applies

All text a human will read: questions put to the user, plans presented for confirmation, issue and PR bodies, statements of work about to start, relays of another session's outcome, status reports, evidence summaries.
