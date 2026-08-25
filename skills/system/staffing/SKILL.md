---
name: staffing
description: Different tasks require different models and how they are used. Use this when choosing a model for a task.
---

# Staffing

Pick the type of task and its staffed fields from the table below. Keep the model and effort separate when passing them to a harness.

If a route is unavailable report back and stop, otherwise report the picked model to the user using this format:

```
🤖 <codex|claude> <model-name>-<effort> because <reason>
```

## Roster

| type of task | model | effort | harness | execution |
| --- | --- | --- | --- | --- |
| judgement, shaping, taste, user-facing ui, copy, codebase-design, architecture, orchestration | fable-5 | high | claude-code | native |
| implementation, bug-fix | gpt-5.6-sol | high | codex-cli | native |
| research | gpt-5.6-terra | high | codex-cli | native |
| research-synthesis | gpt-5.6-sol | high | codex-cli | native |
| hardest tasks, trickiest bugs | fable-5 | high | claude-code | native |
| browser-use | gpt-5.6-sol | medium | codex-cli | scripted Playwright driving Chrome |
| imagegen | gpt-image-2 | — | codex-cli | native |
