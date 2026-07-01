# shadixfy eval workspace

Eval-driven evaluation of the [`shadixfy`](../skills/shadixfy/) skill, following the
[agentskills.io eval methodology](https://agentskills.io/skill-creation/evaluating-skills),
extended to **two agents** and **three conditions**.

- **Agents:** `claude` (Claude Code) and `codex` (Codex CLI) — every task is built by both.
- **Conditions:** `no_skill` (baseline) · `uncodixfy` (the original) · `shadixfy` (this skill).

So each test case produces **6 outputs**. Comparing `shadixfy` against both `no_skill` and
`uncodixfy`, on both agents, is the whole point: does pegging to the shadcn token system beat
"no rules" *and* beat the skill it forks?

## Layout

```
skills/shadixfy/evals/
  evals.json                 # test cases + assertions (authored by hand — the core input)
  files/                     # input files for evals (none needed yet)

shadixfy-workspace/
  conditions/
    uncodixfy.md             # snapshot of cyxzdev/uncodixfy SKILL.md (injected for that condition)
    shadixfy.md              # snapshot of this iteration's shadixfy SKILL.md
  scripts/                   # the harness (see below)
  iteration-1/
    <eval>/<agent>/<condition>/
      prompt.txt             # exact prompt sent (skill body + task), for reproducibility
      agent_response.json|txt# raw agent transcript/response
      outputs/index.html     # the built UI
      outputs/screenshot.png # rendered screenshot (for visual review)
      timing.json            # { total_tokens, duration_ms }
      grading.json           # assertion results (auto + manual-pending)
    benchmark.json           # aggregated per agent×condition, with deltas vs no_skill
    feedback.json            # human review notes (you write this)
```

## How a condition is applied

The skill is injected by **prepending its `SKILL.md` body to the task prompt** (see
`scripts/lib.sh:build_prompt`). This is deliberate:

- It's **identical for both agents.** Codex has no Claude-style description-triggered skill
  auto-invocation, so loading the skill "natively" wouldn't be comparable. Injecting the rules
  measures the effect of *the instructions themselves*, which is what the skill is.
- It's **deterministic** — no reliance on the model deciding to invoke the skill.

`no_skill` sends only the task.

## Isolation (why results aren't contaminated)

Each run executes in a fresh `mktemp -d` **outside this repo**, so no ambient `.claude/`,
`CLAUDE.md`, project skills, or `AGENTS.md` leak in. Additionally:

- **Codex** runs with a temporary `CODEX_HOME` containing only a copy of `auth.json` +
  `config.toml` — its ambient `~/.codex/skills`, `rules`, and `AGENTS.md` are **not** present.
- **Claude**'s global `~/.claude/skills` is empty; running outside the repo avoids project skills.
- Your global `~/.claude/CLAUDE.md` (user memory), if any, still loads — but it's constant across
  all three conditions, so it doesn't bias the comparison.

## Running

Prereqs: `codex`, `node`, `jq`, and Google Chrome (for screenshots) — all already present on this
machine. (`claude` is **not** invoked as a CLI: `claude` cells are produced by the orchestrating agent
via a subagent, and are skipped by the harness by default — see **Agent execution** in `AGENTS.md`.)

The full matrix runs `codex` cells via the Codex CLI (subscription-billed) and consumes real model
usage. Confirm the intended scope before starting a full run.

```bash
cd shadixfy-workspace

# Full matrix for iteration 1: 3 evals × 2 agents × 3 conditions = 18 cells. The 9 codex
# cells run via CLI; the 9 claude cells are skipped (prompt.txt saved) for the orchestrator
# to fill via subagent. Then screenshot + auto-grade + aggregate.
bash scripts/run_all.sh 1

# Subsets while iterating (env vars):
AGENTS="claude" CONDITIONS="no_skill shadixfy" bash scripts/run_all.sh 1
CLAUDE_MODEL=sonnet CODEX_MODEL=gpt-5-codex bash scripts/run_all.sh 1

# A single cell:
bash scripts/run_one.sh dashboard claude shadixfy 1
bash scripts/screenshot.sh iteration-1/dashboard/claude/shadixfy/outputs/index.html
node scripts/grade.mjs dashboard iteration-1/dashboard/claude/shadixfy
```

Runs are **sequential** by default (kind to rate limits). `PARALLEL=1 bash scripts/run_all.sh`
backgrounds the agent calls.

## Review dashboard

`scripts/build_dashboard.mjs` scans every `iteration-*/` and emits a self-contained
**`dashboard.html`** at the workspace root — a whichai.dev-style gallery in the shadcn idiom.
`run_all.sh` rebuilds it automatically; regenerate any time with:

```bash
node scripts/build_dashboard.mjs && open dashboard.html
```

It has: a benchmark table (pass-rate bars, deltas, tokens, time per agent×condition), an outputs
gallery (filter by eval and agent) of every screenshot with its pass badge, a click-to-open
lightbox showing the full render + per-assertion grading with evidence + the prompt, an iteration
selector, and the review notes from `feedback.json`. Open it from the workspace root so the
relative screenshot paths resolve (no server needed).

## Grading

Two layers, per the methodology:

1. **Mechanical (automated)** — `scripts/grade.mjs` checks the objectively verifiable assertions
   straight from the HTML/CSS: gradients, glassmorphism, max border-radius, oversized/colored
   shadows, banned fonts (Inter/Roboto/…), blue-leaning accents, eyebrow kickers, conic glows.
   Each lands in `grading.json` with evidence. Heuristic checks say so in their evidence — confirm
   them visually.
2. **Visual / structural (human or LLM)** — assertions about layout, focus states, "no hero
   block," "renders correctly," and overall polish are marked `"manual": true`. Grade these from
   `screenshot.png`. For a holistic cross-condition score, use the blind-judge prompt in
   `scripts/grade_visual.md`.

`auto_pass_rate` in `benchmark.json` reflects **only** the mechanical layer. After you grade the
manual assertions (set their `passed` in each `grading.json`) and re-run `aggregate.mjs`, the
numbers reflect the full rubric.

## The iteration loop

1. `bash scripts/run_all.sh N`
2. Review `screenshot.png`s + `grading.json`s. Record specifics in `iteration-N/feedback.json`
   (keyed by `<eval>/<agent>/<condition>`; empty string = looked fine).
3. Hand failed assertions + feedback + the current `SKILL.md` to an LLM; apply lean, reasoned edits.
4. Re-snapshot: `cp ../skills/shadixfy/SKILL.md conditions/shadixfy.md`.
5. Re-run into `iteration-(N+1)/`. `run_all.sh` automatically screenshots, grades, aggregates, and
   rebuilds `dashboard.html`.
6. If you update any grading, feedback, or iteration artifacts manually, re-run
   `node scripts/aggregate.mjs N` and then `node scripts/build_dashboard.mjs` before reporting.
7. Stop when feedback is consistently empty or gains plateau.

Local agent instructions live in `AGENTS.md` (with `CLAUDE.md` pointing to it). They keep this
dashboard-update contract scoped to the shadixfy eval workspace without contaminating generated eval
cells.

## Notes & limitations

- **Codex token counts** aren't reliably machine-readable from `codex exec`, so `total_tokens` may
  be `null` for codex cells; `duration_ms` (wall clock) is always recorded. Claude reports both.
- Screenshots use headless Chrome at a tall fixed window (≈full page). Very long pages may clip.
- `grade.mjs`'s color/shadow/eyebrow checks are heuristic by nature — they flag, the human confirms.
- The whole matrix makes real agent calls and costs tokens/time. Start with a subset.
