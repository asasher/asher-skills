---
name: unslop
description: Cut AI tells from any writing. Must always apply.
---

Edit text to remove AI patterns. Scan for the patterns below, rewrite while preserving the meaning, then self-audit: "What makes this obviously AI-generated?" Fix what you find and ask again until the answer is nothing.

## Content tells

- Puffery and promotional words ("testament to", "pivotal", "vibrant", "groundbreaking"). State what happened.
- Superficial "-ing" add-ons ("highlighting...", "ensuring...", "reflecting..."). Delete, or expand with the real detail.
- Vague attribution ("experts believe", "reports suggest"). Name the source or delete.
- Generic conclusions ("the future looks bright"). State the specific fact or plan.

## Language tells

- AI vocabulary ("delve", "showcase", "underscore", "crucial", "intricate", "tapestry") and fancy ways to say "is" ("serves as", "boasts"). Use the plain word: "is", "has", "use".
- Formula shapes: "not just X, but Y", forced groups of three, false "from X to Y" ranges. Say the point directly, use the natural number of points.
- Synonym cycling (protagonist, main character, hero in one paragraph). Pick one word and repeat it.
- Filler and stacked hedges. "In order to" becomes "to", "due to the fact that" becomes "because", "it is important to note that" gets deleted, "could potentially possibly" becomes "may".
- Abstract metaphor jargon. "Substrate" becomes "base", "vector" becomes "way", "ratchet" becomes "a limit that only tightens", "gold-plating" becomes "more than the job needs", "north star" becomes the actual goal, "flywheel" becomes the actual mechanism. Pick the concrete word.
- Fancy synonyms. "Utilize" and "leverage" become "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if".

## Style tells

- Em dashes read as AI, and swapping them for parentheses or en dashes trades one tell for another. End the sentence or use a comma.
- Colons before lists and examples only, never as mid-sentence connectors.
- Straight quotes.
- Sentence-case headings, no decorative emojis, no bolding every noun.
- A bold label and colon that restates its line ("**Performance:** Performance improved...") becomes prose. A bold lead-in ending in a period, followed by genuinely new detail, is fine.

## Chat artifacts

- "Great question!", "I hope this helps!", "Let me know if...", "While details are limited...". Respond directly.

## Plain speech

- Say what it does, not how it feels. Name the mechanism or the number ("`.toSQL()` returns the exact string sent to the database"). If a sentence cannot be restated as a concrete instruction, fact, or question, cut it. If it could appear unchanged in another project, it says nothing about this one; cut it too.
- One idea per sentence. Split anything the reader must backtrack to parse.
- Active voice with a named actor: "the compiler validates queries", not "queries are validated". Passive only when the actor is unknown or irrelevant.
- An adverb propping up a weak verb means the verb is wrong: "significantly improves" becomes the measured delta.
