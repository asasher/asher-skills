---
name: staffing
description: Choose a model and execution route when staffing a task.
metadata:
  requires: [codex-imagegen, verify-your-work]
---

# Staffing

Use the closest task row. User-selected models and harnesses take precedence. Routine owner stages stay inline; apply this roster when choosing a worker.

Report the selection:

```
🤖 <codex|claude|image> <model-name>[-<effort>] because <reason>
```

If the selected route is unavailable, report the blocker. Delegated review and verification use context separate from the builder/fixer; model diversity is optional. Browser verification follows `verify-your-work`.

## Roster

| Task | Model | Effort | Route | Execution |
| --- | --- | --- | --- | --- |
| Planning, shaping, orchestration, architecture | gpt-6-astra | high | codex-cli | native |
| Implementation, debugging, refactoring, performance, code review | gpt-6-astra | high | codex-cli | native |
| Taste, frontend design and implementation, visual critique, copy | claude-fable-5-1 | high | claude-code | native |
| Research synthesis, difficult fact checking | gpt-6-astra | high | codex-cli | native |
| Bounded source collection | gpt-5.6-terra | high | codex-cli | native |
| Browser driving, capture, reproduction | gpt-5.6-terra | high | codex-cli | isolated headless browser; default Playwright |
| Independent behavioral verification | gpt-6-astra | high | codex-cli | fresh context |
| Image generation | gpt-image-2 | — | codex-imagegen | use the shipped codex-imagegen skill's backend selection |
