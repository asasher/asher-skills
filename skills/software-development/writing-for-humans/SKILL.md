---
name: writing-for-humans
description: The communication standard for user-facing text; read it before writing any.
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Writing for humans

The one standard for all user-facing text — questions put to the user, plans presented for confirmation, ticket and PR bodies, statements of work about to start, relays of another session's outcome, status reports, evidence summaries. This is a reference skill: it defines the standard; sibling skills cite it by name and apply it in place.

## The three rules

1. **Simplified Technical English.** User-facing text follows ASD-STE100 discipline: sentences of at most 20 words (25 in descriptive text), active voice, one idea per sentence, words from everyday vocabulary or the project's glossary.
2. **The dictionary is the project's glossary** — the approved technical dictionary, conventionally `CONTEXT.md` at the repo root. Use its terms exactly. A term you need that is missing goes into the glossary through the project's dictionary-maintenance practice. A project without a glossary gets plain words and inline definitions: define a term of art at first use.
3. **No bare numbers.** Every ticket or PR reference carries its id, its title, and a one-or-two-sentence digest of what it is. Relations are said in words — "#12 (rename the parent work-type) blocks #14 (the routing sweep)" — never bare id lists.
