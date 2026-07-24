# Playbook: Codebase

> Project playbook for this repo — how this codebase is written and checked. Read before editing by
> whoever builds (`implement`, `tdd`, `diagnosing-bugs`) and consulted by whoever checks
> (`verify-your-work`, `code-review`). It accretes: a session that learns one of these facts the hard
> way — a runner trap, a naming rule discovered mid-review, a harness seam — writes it into the
> matching section as part of its change, so the next session reads it instead of re-deriving it.

## Conventions

- Skill prose is the product. Skills are self-contained at the file level and compose by name
  (`AGENTS.md` § Conventions); shipped prose carries no history and no unnecessary negations — a
  prohibition earns its place only against demonstrated drift (`CONTEXT.md`, redundant-negation rule).
- Scripts are stdlib-only Python 3.
- Playbook/reference filenames are kebab-case; skill directories are `skills/<category>/<name>/`.
- Commits: imperative, sentence-case subject, no Conventional Commits prefix; Claude Code sessions end
  with its `Co-Authored-By` trailer. Commit/push only when Asher asks.
- **Every change must satisfy** (reviewers hold the diff to these beyond the issue text):
  self-contained skill directories — a change that reaches across skill directories fails;
  compose-by-name for sibling reliance — a refactor must not turn a compose-by-name pointer into a
  file dependency (copy-a-technique / extract-a-primitive per `AGENTS.md` § Conventions);
  stdlib-only Python 3 scripts; `agents/openai.yaml` where a skill must present well in Codex; and a
  **passing probe eval for any new or reworked skill** before first real use.
- Standing review standards: **authoring-context leakage in shipped audience-facing text is a
  blocker** — a sentence presupposing the authoring conversation (change-log framing like "now" /
  "no longer" / "replaces", justifications addressed to the collaborator, provenance asides) gets
  quoted, its real recipient named, and a deletion or recipient-designed rewrite required; history
  belongs in the commit message. **Open every cited fixture** — a test, probe, or document cited as
  criterion coverage is opened and confirmed to exercise the claimed seam before it counts. A file
  growing past **~1000 lines** in one change is a presumptive blocker — decompose first. Reviewers
  also judge rendered artifacts (plan/prototype HTML) for taste, not just correctness.
- UI surfaces (rare here): the `bare-minimum-ux` sibling is the UX baseline overlay and wins on
  conflict where installed (absent, state the gap); when a project's
  `external-dependencies.lock.json` records the consented `impeccable` external, its
  `PRODUCT.md`/`DESIGN.md` are ambient context for every UI change — DESIGN.md wins on visual
  decisions, PRODUCT.md on strategy/voice.

## Checks

Run narrowest-first, then broaden by touched surface. This is a skills repo — the primary "test" is a
probe eval, not a unit test; there is no npm/lint/typecheck/build pipeline.

- Targeted check (skill behavior): run the changed skill's probe scenarios through an executor per
  `docs/agents/probe-evals.md`, graded against the skill's answer key; scenarios live in the skill's
  own `evals/`.
- Script check: for any changed stdlib-Python script, `python3 -m py_compile <script>` then drive it
  directly (`--help`, `--sweep`, the real paths) on this machine's Python 3.14. A script *refactor* is
  behavior-preserving only if the same driven paths produce the same output.
- Catalog gate: `PATH=/usr/bin:$PATH python3 tools/test_catalog.py` (17 tests).
- Site manifest gate: a change touching any SDLC-family skill runs
  `PATH=/usr/bin:$PATH python3 site/check.py` (`site/MAINTENANCE.md`); errors block — **its exit code
  is the verdict; don't pipe it through `tail` in a `&&` chain or the failure is masked.**
- Staffing eval suites (run from `skills/system/staffing/evals/`): `test_global_apply.py`,
  `test_global_templates.py`, `test_provider_pilot.py`. The compiled per-provider staffing load has a
  hard byte budget (`BASELINE_BYTES * 0.8` in `test_global_apply.py`) — prose added to
  `install-and-reconcile.md` or `harness.md` must fit inside it.
- Cold-reader check (pre-review, named): any change shipping audience-facing text — skill prose,
  templates, docs — gets a subagent with none of the authoring conversation reading the artifact
  alone, flagging every sentence it cannot ground in the artifact itself; leakage is fixed or
  explicitly justified before the change is review-ready.
- Aggregate pre-PR gate: the changed skill's probe eval passes against its answer key, and any changed
  script compiles and runs; new or reworked skills clear a pre-deployment probe eval before first real
  use.
- Runner trap: bare `==` in a zsh command line (e.g. `echo ===`) breaks the whole command — quote it
  or avoid it.

## Testing patterns

- Skill behavior is proven by situated dry-run probes, dual-executor, per `docs/agents/probe-evals.md`;
  probe answer keys cite exact sentences from the skill's files, so editing a cited sentence means
  re-citing the key in the same change.
- **A skill's answer key is the executable form of its acceptance criteria.**
- No unit-test framework: tests are probe scenarios, living in each skill's own `evals/` directory.
  Test-first here means write/adjust the probe scenario and answer key the change should satisfy,
  confirm the current skill fails or under-serves it, then make the change and re-run.
- The regression seam for prose skills: capture the affected skill's probe verdicts before a change;
  a refactor is behavior-preserving only if identical scenarios produce the same verdicts after,
  re-run through **≥2 executors** to absorb model variance (`diagnosing-bugs.md` carries the matching
  flaky-surface rule).
- Python tests are stdlib `unittest`, one file per tool, run directly.

## Generated artifacts

- `.agents/skills/` and `.claude/skills/` mounts are build products of `npx skills add` — edit the
  skill source and reinstall, per `AGENTS.md` (and never `npx skills remove`: with a local source path
  it deletes the source itself).
- The staffing provider trees under `.agents/` are compiled by staffing's apply step — regenerate,
  don't hand-edit.
