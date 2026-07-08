## Picking models — Claude Code specifics

Base rankings, rules, and Codex CLI mechanics: `AGENTS.md` § Picking models. From Claude Code additionally:

- Claude models (sonnet-5, opus-4.8, fable-5) run via the Agent/Workflow `model` parameter.
- gpt-5.5 inside workflows and subagents (the model parameter only takes Claude models, so use a wrapper): spawn a thin wrapper agent with `model: 'sonnet', effort: 'low'` whose prompt instructs it to write a self-contained codex prompt, run `codex exec` via Bash, and return the report (use `schema` on the wrapper to get structured output back).
- Always label these agents with a `gpt-5.5:` prefix, e.g. `{label: 'gpt-5.5:review-auth'}` — the workflow UI shows the wrapper's Claude model, so the label is the only indication the real worker is gpt-5.5.
- Parallel gpt-5.5 implementation agents must use `isolation: 'worktree'` so codex edits don't collide in the shared checkout.
- Workflow token budgets only count Claude tokens; codex work is free and invisible to `budget.spent()`.
