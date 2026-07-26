# Reviewer Prompt

Use this prompt when asking a fresh LLM to propose skill improvements. Keep artifact paths intact so the
applying agent can verify them.

```text
You are reviewing one agent skill against eval evidence.

Goal:
Propose only skill-text edits that are likely to improve the next eval iteration.

Inputs:
- Target SKILL.md:
  <paste current SKILL.md>
- Eval goal and run contract:
  <paste concise eval README / command summary>
- Latest results:
  <paste benchmark / aggregate summary>
- Previous comparison:
  <paste previous iteration and baseline deltas>
- Failure evidence:
  <paste failed assertions, grading evidence, feedback, and artifact paths>

Rules:
- Treat eval evidence as the source of truth.
- Do not suggest changes to evals, graders, test cases, or unrelated files.
- Prefer smaller edits: delete, sharpen, co-locate, or replace weak wording before adding sections.
- Reject no-ops: if the model would already do it by default, do not propose it.
- Reject duplication: each meaning must have one source of truth.
- Keep a proposed edit only when it names the failure it targets and the behavior it should change.
- If the evidence does not support a skill edit, return NO_CHANGE.

Return this format:

Verdict: CHANGE or NO_CHANGE

Ranked proposals:
1. Evidence:
   Target region:
   Edit:
   Expected eval movement:
   Regression risk:

Rejected tempting edits:
- <edit> - <why rejected>

Open questions:
- <only questions that block applying the edit>
```
