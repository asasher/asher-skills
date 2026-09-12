---
name: interview
description: Interview the user about an idea or problem until shared understanding is real. Use to elicit and settle the decisions behind new work.
metadata:
  optional: [writing-for-humans, capture, to-subagent]
---

# Interview

Resolve material decisions with the user. Map the work as a **design tree**: each decision branches into the decisions that depend on it. Carry forward settled answers and choose within delegated authority; surface a choice when it changes scope, behavior, cost, risk, or an explicit constraint.

**Intake first** — read what was handed to this session before the first round.

Work the tree in **rounds**. The **frontier** contains material unresolved decisions needing the user's judgment whose prerequisites are already settled. Ask that frontier in one round, then wait for the user's answers before the next round. After each round, recompute the frontier.

**Question format.** Each question in a round is written as: ❓ then the **bold number** and **bold title**, then the body — multiple-choice options where choices genuinely exist — then ➡️ followed by your recommended answer. User-facing text follows the `writing-for-humans` sibling. Absent it, write plainly and say the standard was not loaded.

Find **facts** in the environment. When a frontier question needs a fact from the environment (filesystem, tools, docs), dispatch a lookup via the `to-subagent` skill (absent it, look it up in-session). A running lookup is an unsettled prerequisite: only its downstream questions wait for the subagent to report — ask the rest of the frontier now. Record consequential delegated choices with their rationale so the user can review them.

An interview also surfaces **off-tree** items — real work outside this tree's subject: a bug mentioned in passing, an adjacent idea. Offer them to the `capture` skill (absent it, list them explicitly at the close).

The session is done when material decisions are settled or delegated, no blocking factual lookup remains, and the user confirms shared understanding. Prior confirmation still covers unchanged decisions.
