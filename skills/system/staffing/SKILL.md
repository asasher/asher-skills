---
name: staffing
description: Different tasks require different models and how they are used. Use this when choosing a model for a task.
---

# Staffing

Pick the type of task and its staffed fields from the table below. Keep the model and effort separate when passing them to the named route.

If a route is unavailable report back and stop. Otherwise report the picked model to the user using this format; omit the effort suffix when the roster leaves it unspecified:

```
🤖 <codex|claude|image> <model-name>[-<effort>] because <reason>
```

## Roster

| type of task | model | effort | route | execution |
| --- | --- | --- | --- | --- |
| judgement, shaping, taste, user-facing ui, copy, codebase-design, architecture, orchestration | claude-fable-5 | high | claude-code | native |
| implementation, refactoring, bug-fix, performance, long implementation | gpt-5.6-sol | high | codex-cli | native |
| design-heavy implementation, architecture-bearing refactoring, api-design, adversarial-review, complex code-review | claude-opus-5 | high | claude-code | native |
| research | gpt-5.6-terra | high | codex-cli | native |
| research-synthesis | claude-fable-5 | high | claude-code | native |
| browser-use, browser-verification, reproduction | gpt-5.6-terra | medium | codex-cli | scripted Playwright driving Chrome |
| imagegen | gpt-image-2 | — | image-api | generation or edit endpoint |
