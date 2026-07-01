# Dissolve — binding instructions for this task

You are dissolving a confusing question. **Dissolving ≠ answering.** Do not pick a side and defend it. Instead
deconstruct the mental algorithm that makes the question *feel* like a question, until no confusion remains. As
Yudkowsky puts it, write *a stack trace of the internal algorithm*, not a verdict. Proving the question
"meaningless" is also not enough — you must show *why a mind generates it and feels it as urgent*.

Run these five moves in order (loop back when a later move exposes an earlier one):

1. **Pose & find the itch.** Restate the question, then name *why it feels like a hanging question* — the
   sensation (two intuitions colliding, a word that seems to point at something you can't pin down, a yes/no
   that seems to carry big consequences with no way to check). The confusion is in the map, not the territory.
2. **Taboo the word.** Ban the loaded term *and its synonyms* (especially weasel words: *real, really, true,
   actually, just, is*) and re-ask using only what it stands for. Where the rewrite flows, the word was cheap.
   Where you **cannot** rewrite without smuggling the word back, you've *located* the confusion.
3. **Stack-trace & unbundle.** Trace, step by step, how a mind arrives at the feeling of this question. Then
   unbundle: a single contested word usually packs several *independent* questions. List them as distinct
   sub-questions and diagram the split (a Mermaid `graph TD`).
4. **Reduce to anticipated experience.** For each sub-question, state what you'd actually *expect to observe*
   if the answer were yes vs. no. If both predict the **same** experience, the sub-question is **empty** —
   dissolved on contact. Otherwise it is real; mark it *empirical* (a fact) or *value-laden* (a preference/ethics
   call).
5. **Resolve & run the gate.** State what remains of the original once the word is tabooed and the parts
   separated (empty? a bundle of sharper questions? a relocated value disagreement?). Then run the gate: reread
   the original question and check honestly whether **any lingering feeling of a hanging question** remains. If
   yes, it is not dissolved — say where the pull is and loop back to move 2.

## Output — fill the provided page

A file `dissolution.html` is already in your working directory, seeded with the question. It is your entire
deliverable and its five sections map to the five moves. Fill it and save it in place:

- Edit only **between** the `<!-- FILL: name -->` … `<!-- /FILL: name -->` markers; leave the markers, the
  `.hint` guidance paragraphs, and the scaffolding intact.
- As each move completes, set that `<section>`'s `data-status` **and** its rail chip `data-s` to `active` then
  `done`; set `<b id="overall">` to `dissolved` if the gate passes.
- **taboo** section: fill the two-column table (banned word → what it stood for; note any irreplaceable word).
- **trace** section: prose stack trace + a real Mermaid `graph TD` decomposing the question into sub-questions
  (keep node labels short, quote labels containing `()` or `:`).
- **anticipate** section: one table row per sub-question with *if yes* / *if no* predictions and a Verdict
  (`empty` / `empirical` / `value`).
- **resolution** section: the verdict sentence, the lingering-confusion check, and open threads.

## Constraints for this run

- **Work solo.** There is no human to consult. Play both roles honestly — hold the method *and* report your own
  residual confusion at the gate. Do not pretend the itch is gone if a sub-question is still fused.
- **No web search, no outside sources.** Dissolve from first principles using only this method. Do not look up
  any article, definition, or prior treatment of the question.
- Produce exactly one file: `dissolution.html` in the current directory. No commentary outside it is graded.
