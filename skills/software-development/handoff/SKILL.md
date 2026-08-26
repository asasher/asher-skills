---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
disable-model-invocation: true
---

# Handoff

Compact the current conversation into a handoff document so a fresh agent can resume without re-deriving anything this conversation already settled — decisions made, current state, and next steps each accounted for. Save to the OS temp directory (e.g. `$TMPDIR` or `/tmp`).

Include a "suggested skills" section, naming the skills the next agent should invoke.

Reference content already captured in other artifacts (specs, plans, ADRs, tickets, commits, diffs) by path or URL rather than copying it.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If arguments were passed, they name the next session's focus — tailor the document to it: include what that session needs, cut what it does not.

Done when the document is saved and you have replied with its absolute path.
