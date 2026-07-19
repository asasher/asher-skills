# Authoring-context leakage — what the failure is called, and how to guard it

The failure: private authoring-time context (the design conversation, the change history, the
rationale) leaks into content whose audience was never in that context — skill prose read by a
future agent, UI copy read by an end user, docs read by a newcomer. At best inert load; at worst
confusing or contradictory. Researched 2026-07-20; all sources verified live.

## The names

**The cause — curse of knowledge.** Camerer, Loewenstein & Weber, *JPE* 97(5) 1989: better-informed
agents cannot ignore their private information when anticipating less-informed agents'
judgments. <https://www.journals.uchicago.edu/doi/abs/10.1086/261651>. Standard illustration:
Elizabeth Newton's 1990 tapping study — tappers predicted ~50% of listeners would name the song;
2.5% did. Steven Pinker calls it the chief cause of bad prose ("Why Academics Stink at Writing,"
*Chronicle* 2014; *The Sense of Style*). <https://www.chronicle.com/article/why-academics-stink-at-writing/>

**The mechanism — recipient design failure.** Sacks, Schegloff & Jefferson, *Language* 50(4) 1974:
talk is "constructed or designed in ways which display an orientation and sensitivity to the
particular other(s) who are the co-participants." The leaked sentence was designed for the wrong
recipient — the collaborator in the authoring session, not the actual reader. Cousins: Bell's
audience design (*Language in Society* 13(2) 1984); Clark & Brennan's grounding — the leak is an
**ungrounded common-ground presupposition** (assuming as mutual what was never grounded with this
reader).

**Domain-local names for the same thing:**

| Field | Name | Source |
|---|---|---|
| UX copy | maker-centric language; Nielsen heuristic #2 violation ("speak the users' language… rather than internal jargon") | <https://www.nngroup.com/articles/user-centric-language/>, <https://www.nngroup.com/articles/ten-usability-heuristics/> |
| Code | comments-as-version-control; review-thread context that never reaches the code | <https://coding.abel.nu/2012/07/comments-are-not-version-control/>, <https://google.github.io/eng-practices/review/developer/handling-comments.html> |
| LLM contexts | **context confusion** (Breunig: "superfluous information in the context is used by the model to generate a low-quality response"), shading into **context clash**; umbrella: **context rot** (Chroma 2025; Anthropic's context-engineering guidance); the canonical paper: Shi et al., "LLMs Can Be Easily Distracted by Irrelevant Context," ICML 2023 | <https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html>, <https://research.trychroma.com/context-rot>, <https://arxiv.org/abs/2302.00093> |
| Journalism | inside baseball | <https://en.wikipedia.org/wiki/Inside_baseball_(metaphor)> |
| Fiction craft | **scaffolding** — prose written for the author's own understanding, removed before shipping | craft usage, no single canonical origin |

Not established terms (don't lead with them): "prompt contamination," "context pollution."
"Ship your org chart" is a later colloquialism on Conway's law (Sinofsky attribution is
secondary-source only).

## Why an LLM author is *especially* cursed

For a human the authoring context is merely known; for an in-session agent it is **in the prompt,
actively attended** while the copy is generated. Sentences addressed to the collaborator —
justifications, comparisons to the previous design, reassurances that a decision was made — surface
in text addressed to the artifact's reader. The verbosity audit's fingerprints were exactly this
class: "There is no separate plan stage" (justifying a decision to the collaborator), "(Matt's
posture)" (provenance), "from the #46 self-approval incident" (history), "backlog's earlier vNN
stamps are retired" (change-log-in-artifact).

## The detector

One question per sentence: **"Does this sentence still work for a reader who wasn't in the room?"**
Mechanical markers of provenance-dependence:

- time-anchored to the authoring act: *now, no longer, formerly, previously, the old way*
- alternatives not taken: *instead of, rather than the earlier, replaces*
- the authoring conversation itself: *we decided, as discussed, this addresses the feedback*
- justification-of-correctness: explaining why the text is right instead of what the reader does

If deleting the sentence changes nothing about what the reader does → it was addressed to the wrong
recipient.

## The structural fix — the cold reader

You cannot un-know (that's the whole bias), but a fresh context genuinely doesn't know. The reliable
guard is a **cold-reader pass**: a subagent with none of the authoring conversation reads the
artifact and flags every sentence it cannot ground in the artifact itself. This is the tapping study
inverted — hire a listener instead of trusting the tapper.

## Proposed encodings (owner to confirm)

1. **Machine-level rule** (global agent instruction files, both harnesses): audience-facing text is
   written for readers who weren't in this conversation; strike sentences that presuppose it —
   what-changed/why-we-chose/what-used-to-be-true belongs in commit messages and chat, never the
   artifact.
2. **Reviewer blocker**: add "authoring-context leakage" to the change-reviewer brief (shipped
   template + this repo's playbook) — quote the leaked sentence, name the recipient it was actually
   addressed to.
3. **Cold-reader check** for major audience-facing deliverables (skill prose, UI copy, docs):
   context-free subagent flags ungrounded sentences before ship.
