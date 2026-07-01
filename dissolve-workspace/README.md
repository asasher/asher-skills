# dissolve — workspace

Working directory for the `dissolve` skill (whose source lives in `skills/dissolve/`): evals, run artifacts, and
any maintenance scripts for the skill. The first thing here is the eval below.

## Eval

Tests whether the skill actually lets agents dissolve a question. The example
question is **"Is alcoholism a disease?"** — the central worked example of Scott Alexander's *Diseased Thinking*,
so a real article exists to grade fidelity against **later**.

In **no** automated eval does the agent see the article or the answer key. The framework is the only input; the
article is our reference point, applied by a human afterward.

## The three evals

| # | Eval | Question | Automatable | Here |
|---|---|---|---|---|
| 1 | **Solo** — one agent, no human, no peer | Can the skill alone dissolve it? | yes | `runs/solo/{claude,codex}/` |
| 2 | **Pair** — two agents collaborate | Can two agents dissolve it together? | yes | `runs/pair/` |
| 3 | **Human + agent** | Can a human + agent dissolve it? | no (needs a human) | done manually, later |

Mechanism: **Claude = a subagent** (never `claude -p` — see `AGENTS.md` > Agent execution), **Codex = the
`codex` CLI** run headless in an isolated `CODEX_HOME` so no ambient skills/AGENTS.md leak in. Each agent is
blind: no web search, no reading any file but its own workspace.

## Layout

```
dissolve-workspace/
  conditions/
    dissolve.md          # the skill's method, injected as binding instructions (solo)
    dissolve-pair.md     # + the turn/critique protocol (pair)
  reference/article-key.md   # ground truth from the article — for HUMAN grading later; agents never see it
  scripts/lib.sh         # seed() a fresh dissolution.html; run_codex() headless+isolated
  runs/
    solo/PROMPT.txt      # the exact solo prompt (method + task)
    solo/claude/dissolution.html   # + preview.png
    solo/codex/dissolution.html    # + preview.png, codex.log
    pair/dissolution.html          # the joint artifact (+ preview.png)
    pair/discussion.md             # the turn-by-turn debate log
```

## Reproduce

```bash
cd dissolve-workspace && source scripts/lib.sh
# Solo (codex): seed then run
seed runs/solo/codex && run_codex runs/solo/codex runs/solo/PROMPT.txt
# Solo (claude): run a subagent with runs/solo/PROMPT.txt against a seeded runs/solo/claude/dissolution.html
# Pair: seed runs/pair, then alternate turns (see conditions/dissolve-pair.md), Claude subagent <-> run_codex.
```

Each `dissolution.html` is self-contained — open in a browser. Section `data-status` shows how far each run got;
`overall` = `dissolved` when the run passed its gate.

## Grading (done later, by a human, against `reference/article-key.md`)

Score each `dissolution.html` on: taboo recovered? which of the article's four bundled sub-questions
(harm · fault/blame · does-medical-treatment-help · sympathy) were surfaced as *distinct*? was the bare label
flagged **empty**? did it reach the consequentialist resolution? And **convergence**: overlap between the two
solo runs, and quality of the pair's joint decomposition.
