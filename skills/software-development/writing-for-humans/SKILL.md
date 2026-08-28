---
name: writing-for-humans
description: The communication standard for user-facing prose. Apply when writing responses, questions, plans, tickets, change requests, reports, specifications, or other text a person will read.
---

Write user-facing prose in three passes: a clear base, then a scan for tells, then soul. Each pass reads the whole text.

## Pass 1: clear base

- Use ASD-STE100 Simplified Technical English as the base. Prefer common words, short sentences, active voice, and one idea per sentence.
- Use the ubiquitous language from the project's `CONTEXT.md` when available.
- Say what it does, not how it feels. Name the mechanism or the number; if a sentence cannot be restated as a concrete instruction, fact, or question, cut it. If it could appear unchanged in another project, it says nothing about this one; cut it too.
- Support judgments with the project detail that caused them. An adverb propping up a weak verb means the verb is wrong: "significantly improves" becomes the measured delta.
- Give each ticket or change-request identifier its human meaning. On first mention, add its title and a one- or two-sentence digest when available.
- State relationships in words. For example, `#12 (rename the parent work-type) blocks #14 (update routing)`.

## Pass 2: tells

Scan for these patterns and rewrite. Preserve the meaning.

- Puffery and promotional words ("testament to", "pivotal", "vibrant", "groundbreaking"). State what happened.
- AI vocabulary and inflated verbs ("delve", "showcase", "underscore", "leverage"; "serves as", "boasts"). Use the plain word: "is", "has", "use".
- Superficial "-ing" add-ons ("highlighting...", "ensuring...", "reflecting..."). Delete, or expand with the real detail.
- Formula shapes: "not just X, but Y", forced groups of three, false "from X to Y" ranges, synonym cycling. Say the point directly, use the natural number of points, repeat the one word.
- Filler, hedging, canned transitions, and generic conclusions ("in order to", "it is important to note that", "while details are limited", "the future looks bright"). Delete, or state the specific fact or plan.
- Vague attribution ("experts believe", "reports suggest"). Name the source or delete.
- Chatbot artifacts ("Great question!", "I hope this helps!", "Let me know if..."). Respond directly.
- Abstract metaphor jargon ("substrate", "north star", "flywheel"). Pick the concrete word.
- Punctuation tells: em dashes (and swapping them for parentheses or en dashes, which trades one tell for another), colons as mid-sentence connectors, curly quotes. End the sentence or use a comma; keep colons for lists and examples; use straight quotes.
- Format tells: a bold label and colon that restates its line ("**Performance:** Performance improved..."), bolding every noun, title-case headings, decorative emojis. Convert label bullets to prose (a bold lead-in ending in a period, followed by new detail, is fine), and use sentence case.

## Pass 3: soul

Removing tells is half the job. Sterile, voiceless prose reads as machine-made.

- Match the user's tone and level of formality.
- Have opinions. React to facts instead of neutrally listing them, and use "I" when it makes ownership or a recommendation clearer.
- Acknowledge complexity. "Works, but the retry path worries me" beats "works".
- Vary rhythm. Short sentences. Then longer ones that take their time. Perfect parallel structure looks manufactured, so let some mess in.

Finish with a self-audit from the recipient's point of view: "What makes this obviously AI-generated?" Fix what you find and ask again. The text is complete when the answer is nothing, it is clear on the first read, and it sounds like someone who knows this project.
