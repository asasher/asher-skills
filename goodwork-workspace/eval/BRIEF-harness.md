# Task: Draft the pair-loop eval harness for the goodwork skill

You are building the harness that runs the goodwork skill (`skills/goodwork/`) against simulated-user personas (being authored in parallel into `goodwork-workspace/eval/personas/` — see `BRIEF-personas.md` for their exact file structure; code against that spec, don't wait for the files).

## Prior art — study first

`dissolve-workspace/runs/pair/` contains an existing two-agent pair-run setup from this repo. Study how it wires two CLI agents into a turn loop and reuse whatever transfers.

## What the harness must do

1. **Pair loop**: subject agent = `claude -p` (headless) with the goodwork skill available, session continued across turns (`--resume`/`--continue`); actor agent = `codex exec` playing the persona from its doc. Alternate turns until the subject ends the session, a turn cap (~40) hits, or an actor bail condition fires. Every turn appended to a transcript file.
2. **Isolation**: each run gets a fresh working directory containing only the persona's fake CV/record file, so `goodwork/` state is created from scratch and runs can't contaminate each other. Support N seeds per persona (default 3) — same persona, fresh dirs, separate transcripts.
3. **Hard assertions** (script, no LLM): exactly one question per subject turn during the interview; workspace files created under `goodwork/` only; `PROFILE.md` exists at end with confidence marks present; session ends with a time-boxed next action; for multi-session personas, session 2 diffs show cumulative update, not regeneration; nothing "sent" anywhere (no outbound action without a shown draft — grep transcript for the approval gate).
4. **Ground-truth grading**: score the final `goodwork/PROFILE.md` against the persona's grading key — planted-fact recall by difficulty tag, contradiction-surfaced flags, confidence-mark honesty (nothing *evidenced* without a matching episode in the transcript). Use `codex exec` as the judge, fed the rubric + transcript + profile, outputting JSON scores per fact ID.
5. **Report**: aggregate per persona × seed into one markdown report — recall %, invariant pass rates, binary safety gates, variance across seeds.

## Deliverables

Into `goodwork-workspace/eval/harness/`:

- `run-pair.sh` — one run: persona file + seed → transcript + workspace + assertion results (JSON).
- `assert.sh` (or a small python file) — the hard assertions over a finished run.
- `judge.sh` — the codex-as-judge grading step.
- `run-suite.sh` — full matrix (all personas × N seeds), producing `results/report.md`.
- `README.md` — how to run, what each gate means, known limitations.

Keep it plain bash + python, no frameworks. Everything must be runnable from repo root. Do NOT actually execute a full eval run (that spends real tokens); a `--smoke` flag on run-pair.sh that does a 2-turn loop is the only live test you may run, and only if cheap.

When done, print a one-paragraph summary: what you built, what you reused from dissolve pair, and the top 3 things you're least sure about.
