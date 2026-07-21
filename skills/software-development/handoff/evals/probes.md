# Handoff — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

A long session shaped a payout feature (spec committed at `docs/specs/payouts.html`, decisions on ticket
#142) and touched an API key in `.env`. The user runs `handoff "next session implements ticket 142"`.

## Probes

**P1 (location).** Where is the document saved? Cite.

**P2 (duplication).** Do you copy the spec's decisions into the handoff? Cite.

**P3 (secrets).** The conversation displayed the API key. Does it appear? Cite.

**P4 (skills + argument).** What section must the document include, and how does the argument shape the
content? Cite.

## Answer key

- **P1:** "Save to the temporary directory of the user's OS — not the current workspace." Writing into
  the repo = **fail**.
- **P2:** No — "Do not duplicate content already captured in other artifacts (specs, plans, ADRs,
  tickets, commits, diffs). Reference them by path or URL instead." Inlining the spec = **fail**.
- **P3:** No — "Redact any sensitive information, such as API keys, passwords, or personally
  identifiable information." The key appearing = **fail**.
- **P4:** A "suggested skills" section "naming the skills the next agent should invoke"; the argument
  is "a description of what the next session will focus on" — tailor toward implementing #142.
  Missing either = **fail**.

Pass bar: **4/4 on both executors.**
