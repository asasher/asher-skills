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

## Checks

- Catalog gate: `PATH=/usr/bin:$PATH python3 tools/test_catalog.py` (17 tests).
- Site manifest gate: `PATH=/usr/bin:$PATH python3 site/check.py` — **its exit code is the verdict;
  don't pipe it through `tail` in a `&&` chain or the failure is masked.**
- Staffing eval suites (run from `skills/system/staffing/evals/`): `test_global_apply.py`,
  `test_global_templates.py`, `test_provider_pilot.py`. The compiled per-provider staffing load has a
  hard byte budget (`BASELINE_BYTES * 0.8` in `test_global_apply.py`) — prose added to
  `install-and-reconcile.md` or `harness.md` must fit inside it.
- Runner trap: bare `==` in a zsh command line (e.g. `echo ===`) breaks the whole command — quote it
  or avoid it.

## Testing patterns

- Skill behavior is proven by situated dry-run probes, dual-executor, per `docs/agents/probe-evals.md`;
  probe answer keys cite exact sentences from the skill's files, so editing a cited sentence means
  re-citing the key in the same change.
- Python tests are stdlib `unittest`, one file per tool, run directly.

## Generated artifacts

- `.agents/skills/` and `.claude/skills/` mounts are build products of `npx skills add` — edit the
  skill source and reinstall, per `AGENTS.md` (and never `npx skills remove`: with a local source path
  it deletes the source itself).
- The staffing provider trees under `.agents/` are compiled by staffing's apply step — regenerate,
  don't hand-edit.
