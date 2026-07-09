<!-- backlog-templates: v2026-07-06.1 -->

# Playbook: Verifying

> Project playbook for this repo. The backlog `verify` subskill reads this file for check commands and where acceptance criteria come from. How to run, isolate, seed, and authenticate against the app is in `environment.md`; the evidence contract lives in `evidence.md`.

## Checks

Run narrowest-first, then broaden by touched surface. This is a skills repo — the primary "test" is a probe eval, not a unit test. There is no `npm`/lint/typecheck/build pipeline.

- Targeted check (skill behavior): run the changed skill's probe scenarios through an executor model per `docs/patterns/probe-evals.md` — situated dry-run prompts graded against the skill's answer key. Scenarios live in the skill's `evals/`. Drive them via the executors in `environment.md` § Driving the app (Claude subagent + `codex exec`).
- Script check: for any changed stdlib-Python script, `python3 -m py_compile <script>` then drive it directly (e.g. `review-server.py --sweep`, `--help`) to confirm it runs on this machine's Python 3.14.
- Docs/prose check: skills are mostly markdown — re-read the changed reference/SKILL against the skill's own contract; no automated linter.
- Lint / type check / build: **n/a** (no build system; stdlib Python + markdown).
- Full / aggregate gate (before PR): the changed skill's probe eval passes against its answer key, and any changed script compiles and runs. New or reworked skills must clear a pre-deployment probe eval before first real use (`AGENTS.md` convention).
- Independent second-opinion verification: delegate a scenario to `codex exec` as a second, differently-modeled executor when a criterion is subjective or benefits from a perspective outside the orchestrator's context; grading against the answer key and running scripts stay local.

## Acceptance criteria

- Where criteria come from: the issue, and for an enhancement the approved plan's definition of done. For a skill, the answer key in its `evals/` is the executable form of the criteria. The verifier writes them as explicit pass/fail checks driven through an executor.
- Repo-specific expectations every change must satisfy beyond the issue text:
  - **Self-contained at the file level** — a skill's files stay in its own directory; it never imports another skill's files or a shared library (`AGENTS.md` § Conventions). A change that reaches across skill directories fails.
  - **Compose by name, not by file** — cross-skill reliance is a plain-language runtime pointer, not a file dependency.
  - **Scripts are stdlib-only Python 3** — no third-party imports.
  - **New/reworked skills carry a probe eval** — and it must pass before first real use.
  - Skills that must present well in Codex ship `agents/openai.yaml` (`docs/patterns/codex-compat.md`).
