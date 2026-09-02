---
name: interview
description: Interview the user about an idea or problem until shared understanding is real. Use to elicit and settle the decisions behind new work.
metadata:
  optional: [writing-for-humans, capture, to-subagent]
---

# Interview

Interview the user relentlessly. Map the work as a **design tree**: every decision branches into the decisions that hang off it.

**Intake first** — read what was handed to this session before the first round.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled. Ask the whole frontier in one round, then wait for the user's answers before the next round. After each round, recompute the frontier.

**Question format.** Each question in a round is written as: ❓ then the **bold number** and **bold title**, then the body — multiple-choice options where choices genuinely exist — then ➡️ followed by your recommended answer. User-facing text follows the `writing-for-humans` sibling. Absent it, write plainly and say the standard was not loaded.

Finding **facts** is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, docs), dispatch a lookup via the `to-subagent` skill (absent it, look it up in-session). A running lookup is an unsettled prerequisite: only its downstream questions wait for the subagent to report — ask the rest of the frontier now. The **decisions** are the user's — put each to them and wait.

An interview also surfaces **off-tree** items — real work outside this tree's subject: a bug mentioned in passing, an adjacent idea. Offer them to the `capture` skill (absent it, list them explicitly at the close).

The session is done when the frontier is empty — every assumption surfaced as a decision — and the user confirms shared understanding.
