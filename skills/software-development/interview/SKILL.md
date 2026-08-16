---
name: interview
description: Interview the user about an idea or problem until shared understanding is real. Use to elicit and settle the strategic decisions behind new work.
argument-hint: "<idea, problem, or reference to intake material>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [writing-for-humans, to-backlog, to-subagent]
---

# Interview

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Read what was handed to this session before the first round — provided artifacts are read, not asked about.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask now without guessing at answers you haven't heard yet. Ask the whole frontier in one round, then wait for the user's answers before the next round.

**Question format.** Each question in a round is written as: ❓ then the **bold number** and **bold title**, then the body — multiple-choice options where choices genuinely exist — then ➡️ followed by your recommended answer. The format makes a big round scannable and cuts the user's typing to "1: yes, 2: B, 3: as recommended." User-facing text follows the `writing-for-humans` sibling — ASD-STE100 plain language, `CONTEXT.md` as the dictionary, no bare ticket or PR numbers.

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a later round, not this one.

Finding **facts** is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, docs), dispatch a lookup via the `to-subagent` skill (absent it, look it up in-session) — don't ask the user for anything you could look up yourself. Don't block on it: a running lookup is an unsettled prerequisite, so only the questions downstream of it wait for the subagent to report — ask the rest of the frontier now. The **decisions** are the user's — put each to them and wait.

An interview also surfaces items that are real work but not this tree's subject — a bug the user mentions in passing, an adjacent idea. Offer them to the `to-backlog` skill for capture (absent it, list them explicitly at the close) rather than absorbing them into the tree or losing them with the chat.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
