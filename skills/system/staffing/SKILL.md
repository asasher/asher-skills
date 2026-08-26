---
name: staffing
description: Different tasks require different models and how they are used. Use this when choosing a model for a task.
---

# Staffing

Pick the type of task and its staffed fields from the table below. If a task doesn't match any of the listed types, pick the closest and inform the user.

If a route is unavailable report back and stop. Otherwise report the picked model to the user using this format:

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
| browser-use, browser-verification, reproduction | gpt-5.6-terra | high | codex-cli | scripted Playwright driving Chrome |
| imagegen | gpt-image-2 | — | codex-cli | use codex-imagegen skill when available |
