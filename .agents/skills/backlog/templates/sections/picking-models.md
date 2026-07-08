## Picking models

Rankings, higher = better. Cost reflects what this machine's owner actually pays, not list price. Intelligence is how hard a problem you can hand the model unsupervised. Taste covers UI/UX, code quality, API design, and copy.

| model    | cost | intelligence | taste |
|----------|------|--------------|-------|
| gpt-5.5  | 7    | 8            | 5     |
| sonnet-5 | 5    | 5            | 7     |
| opus-4.8 | 4    | 7            | 8     |
| fable-5  | 2    | 9            | 9     |

How to apply:

- These are defaults, not limits. Standing permission to override them: if a cheaper model's output doesn't meet the bar, rerun or redo the work with a smarter model without asking. Judge the output, not the price tag. Escalating costs less than shipping mediocre work.
- Don't let cost keep the work off the right model. Instead, use cheaper options to gather information and try things before moving the work to a more expensive option.
- Cost is a tie-breaker only; when axes conflict for anything that ships, intelligence > taste > cost.
- Mechanical and implementation-type work (clear-spec implementation, data analysis, migrations, bulk edits): gpt-5.5.
- Anything user-facing (UI, copy, API design) needs taste ≥ 7.
- Reviews of plans and implementations: fable-5 or opus-4.8, optionally gpt-5.5 as an extra independent perspective.
- Orchestration, design, and hard diagnosis: the most capable model reachable in the session.
- Never use Haiku.
- A model the current harness cannot reach is not an option; fall back per the succession line in `docs/agents/environment.md` § Model staffing.

Mechanics:

- gpt-5.5 is reachable only through the Codex CLI — `codex exec` / `codex review` (`~/.codex/config.toml` sets the default model). Delegate with a self-contained prompt: `codex exec -s read-only --skip-git-repo-check` for investigation and review; `-s workspace-write` when it must edit.
- Codex runs can outlive shell timeouts — pass an explicit timeout, or run in the background and poll for the report.
- Independent runtime verification (real UI interaction, screenshots, simulator or device state, a second opinion outside the current context) can also be delegated to `codex exec`; ordinary code reading, typechecking, linting, and tests the current session can run directly stay local.
