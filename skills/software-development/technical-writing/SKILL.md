---
name: technical-writing
description: The writing standard for durable artifacts. Apply when writing specs, tickets, change requests, reports, or documentation.
metadata:
  requires: [unslop]
---

Write artifacts a tired reader understands on the first read. Every rule below serves that reader; when a rule makes a sentence worse, fix the sentence another way.

Apply the `unslop` skill to strip AI patterns (without it, still rewrite anything that sounds machine-made). Skip its voice advice here: an artifact wants uniformity, not personality.

## Sentences

- Write instructions as commands in present tense: "Run the migration", not "The migration should be run".
- Put the condition before the instruction it governs: "If the build fails, revert". The reader acts while they read.
- Cap procedural sentences near 20 words and descriptive ones near 25. Split rather than compress.
- Keep the articles. "Load the config before the first request" survives skimming; telegraphese does not.
- Place modifiers beside what they modify: "applies only to drafts", not "only applies to drafts".
- State the step without judging its difficulty. "Simply" and "just" read as mockery the moment the step fails.

## Terms and references

- One name per concept and one concept per name, taken from the project's `CONTEXT.md` when it exists.
- Break up noun clusters past three words: "the timeout for the queue retry", not "queue retry timeout configuration value".
- Give every "it", "this", and "they" one obvious referent; repeat the noun when in doubt.
- Give each ticket or change-request identifier its human meaning. On first mention, add its title and a one- or two-sentence digest.
- State relationships in words: `#12 (rename the parent work-type) blocks #14 (update routing)`.

## Paragraphs

- One topic per paragraph, six sentences at most.

The artifact is done when a reader who knows nothing of this session can act on it: every instruction commandable, every term single-named, every identifier explained.
