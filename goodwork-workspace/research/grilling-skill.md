# Analysis: `grilling` skill (mattpocock/skills)

## 1. Verbatim file contents

The GitHub API directory listing shows the skill contains **exactly one file** — `SKILL.md` (666 bytes).

### `skills/productivity/grilling/SKILL.md` (full, verbatim)

```markdown
---
name: grilling
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a question can be answered by exploring the codebase, explore the codebase instead.
```

## 2. Interviewing technique analysis

- **Strictly one question at a time**, with the rationale stated in-prompt ("multiple questions at once is bewildering") so the model generalizes rather than mechanically obeys.
- **Tree traversal, not a checklist**: depth-first exploration of a decision space; each answer opens child branches.
- **Dependency ordering**: upstream decisions settled before dependent ones asked.
- **Recommendation-anchored questions**: every question ships with the interviewer's proposed answer. Reacting to a stance is cheaper than free recall; disagreement forces articulation of hidden constraints. The skill's pushback mechanism in disguise.
- **Stopping condition**: "until we reach a shared understanding" — subjective, mutual; "relentlessly" biases toward over-asking.
- **Tone**: one word — "relentlessly" — licenses persistence and not accepting hand-waving; one-question pacing is the tone governor.
- **Sourcing discipline**: "If a question can be answered by exploring the codebase, explore the codebase instead" — never spend a user turn on something the agent can look up.
- **No deliverable** — ends in conversation state, a genuine gap.

## 3. Transfer to a career-profiling interview skill

Transfer directly:
1. One question at a time, with rationale stated.
2. Recommendation-anchored → **hypothesis-anchored questions**: offer a working read for the user to correct ("Sounds like you're more systems-builder than people-manager — right?"). Corrections are information-dense. Most valuable transferable technique.
3. Tree traversal with dependency ordering (values → constraints → skills → evidence → trajectory).
4. "Explore the codebase instead" → **"explore the record instead"**: mine resume, LinkedIn, GitHub, prior conversation before asking.
5. Licensed persistence: push on vague, socially-desirable answers ("What does impact concretely mean?").

Adapt:
6. Stopping condition should be coverage-based (each profile section has a concrete, verified example) plus a user escape hatch — career interviews are fatigue-prone.
7. Add the deliverable grilling lacks: a written profile artifact, plus a "play the profile back for correction" pass (hypothesis-anchoring applied to the whole deliverable).
8. Tone: "curious and concrete," not adversarial — challenge the vagueness, not the person.

**Meta-lesson:** ~90 words works because it encodes a few high-leverage behavioral rules rather than a script of questions. Specify interviewing *mechanics*, let the model generate the questions.
