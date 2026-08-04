---
name: writing-technical-docs
description: Controlled technical prose for drafting and rewriting READMEs, API references, runbooks, procedures, error messages, getting-started guides, deprecation notices, release notes, and pull-request descriptions. Use when technical text must be clear, concise, consistent in terminology, easy to translate, or free of AI-sounding filler. Use the strict branch when the user asks for ASD-STE100 or safety-critical controlled English. Not for marketing copy or prose whose main purpose is voice.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Writing Technical Docs

Treat technical documentation as a **reader contract**: give a specified reader the facts and actions required to reach a specified result. Controlled prose fixes form, not substance. A clean sentence that says nothing is still a defect.

## 1. Build the reader contract

Inspect the code, interface, issue, existing documentation, house style, and supplied evidence before drafting. Establish:

- the artifact type and its exact output location.
- the reader, the task they must complete, and what they already know.
- prerequisites, inputs, outputs, failure states, and recovery actions.
- canonical names for each concept, including exact identifiers and user-visible strings.
- facts that need verification and claims that the available sources do not support.

Do not invent behavior, compatibility, performance, safety, or guarantees. Ask only when a missing fact changes the meaning and cannot be recovered from the available sources. Preserve exact code, commands, identifiers, protocol fields, UI labels, and quoted messages even when they do not follow the prose rules.

Completion: the artifact, reader, job, source facts, canonical terms, and unresolved material facts are known.

## 2. Select the control level

Use **controlled technical prose** by default. Keep exact domain terminology, but control sentence structure, word meaning, and information order.

Use the **strict source-backed branch** only when the user requests ASD-STE100, a contract requires it, or the text is safety-critical. Read [the ASD-STE100 boundary](reference/asd-ste100.md) before drafting. Full compliance requires the contractually applicable official standard, the applicable terminology source, and qualified human review. Without those inputs, label the result `STE-inspired` or `controlled technical prose`. Do not claim ASD-STE100 compliance before the required qualified review.

Do not apply the strict branch to marketing, narrative, or other voice-led prose. If a document mixes technical and voice-led sections, control only the technical sections.

Read the matching section of [artifact patterns](reference/artifact-patterns.md) before drafting. For a mixed document, read each matching section.

Completion: the control level and every applicable artifact pattern are selected, and any compliance or safety gate is explicit.

## 3. Plan the information path

Start with the result, definition, or condition the reader needs. Remove throat-clearing sections that only announce the document. Order prerequisites before actions, causes before effects, and conditions before the commands they govern.

For procedures, use a numbered vertical list. Put one action in each step unless actions must occur at the same time. Include an observable result or verification step.

For descriptions, introduce one topic at a time and add detail gradually. Keep one topic in each paragraph and no more than six sentences in a paragraph.

Completion: every section advances the reader's job, every prerequisite precedes its dependent action, and no section exists only as an introduction or closing flourish.

## 4. Draft controlled prose

Apply all of these rules:

- Use one canonical name for one concept. Do not rotate synonyms for variety.
- Give a common word one meaning in its local context. Keep a different word when the meanings differ.
- Prefer active voice. Use passive voice only when the actor is genuinely unknown or the contract requires it.
- Use a direct verb for an action: `analyze the log`, not `perform an analysis of the log`.
- Remove stacked helpers and hedges. Replace `may potentially help to reduce` with the supported result or state the uncertainty precisely.
- Replace vague phrasal verbs with specific verbs: use `start`, `remove`, or `investigate` when those are the actual actions.
- Split independent ideas. Keep instructions at 20 words or fewer and descriptive sentences at 25 words or fewer, excluding immutable literals.
- Do not use semicolons. Treat an em dash as a review signal, not a banned character. Keep it only when it does not join ideas that need separate sentences.
- Use articles and explicit referents. Do not make the reader infer what `it`, `this`, or `they` names.
- Remove unsupported promotional labels such as `seamless`, `robust`, or `powerful`. Replace each claim with observable behavior or delete it.
- Use American English unless the project has a different house style.

Do not shorten by deleting necessary conditions, limitations, examples, units, or recovery steps. Shorter is useful only when meaning remains complete.

Completion: every sentence has one job, every term is stable, every claim is concrete, and every immutable literal is unchanged.

## 5. Run the truth pass

Check the draft against its sources, not against how plausible it sounds:

- Trace each behavior, default, limit, version, command, and compatibility claim to code or an authoritative source.
- Run commands and examples when the task authorizes it and the environment permits it.
- Distinguish a verified fact, a documented claim, and an assumption.
- Preserve required legal and safety wording. Do not weaken or reclassify a warning to make it shorter.
- Remove empty promises, generic benefits, duplicate conclusions, and summary sentences that add no information.

When a claim cannot be verified, remove it, qualify it precisely, or report the gap outside the artifact. Do not hide uncertainty inside vague prose.

Completion: every checkable claim matches a source. Every runnable example is tested or identified as unverified. No fact exists only to make the text sound complete.

## 6. Check mechanics and finish

Resolve `<skill-dir>` to the directory that contains this `SKILL.md`. Do not resolve `scripts/` from the consumer project's working directory. Run the bundled checker on prose files:

```sh
python3 <skill-dir>/scripts/check_prose.py <file>                  # descriptive limit: 25 words
python3 <skill-dir>/scripts/check_prose.py --max-words 20 <file>  # procedures and safety instructions
```

For mixed documents, run the 25-word check on the file and separately check each procedural block with the 20-word limit. The checker uses an approximate word count, not the official ASD-STE100 word-count method.

The checker ignores frontmatter and fenced code. It counts each inline code span and quoted string as one immutable unit. It reports hard errors for long sentences and semicolons. It also reports review warnings for likely passive voice, contractions, progressive constructions, hedges, nominalizations, phrasal verbs, promotional terms, and dashes. Resolve every correct error. Preserve immutable text when it causes a false finding, and record the exception. Inspect every warning in context. Change it when the rule applies, and keep it when an exact term or correct meaning requires it. The checker cannot judge terminology consistency, factual accuracy, completeness, or ASD-STE100 compliance.

Read the document once as the target reader. Confirm that the reader can identify what happened, what to do, what result to expect, and how to recover from failure without decoding the prose.

Return the finished artifact first. Add a short verification note only when assumptions, untested examples, or compliance limits remain.

Completion: the checker has no unresolved applicable errors, every warning was inspected, the reader contract is complete, and all remaining gaps are stated.

## Dependency surface

- **Bundled** — [artifact patterns](reference/artifact-patterns.md), [the ASD-STE100 boundary](reference/asd-ste100.md), and [the mechanical prose checker](scripts/check_prose.py).
