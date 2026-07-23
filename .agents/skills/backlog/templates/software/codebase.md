# Playbook: Codebase

> Project playbook for this repo — how this codebase is written and checked. Read before editing by
> whoever builds (`implement`, `tdd`, `diagnosing-bugs`) and consulted by whoever checks
> (`verify-your-work`, `code-review`). `setup` seeds it from the repo's own docs and configs; after
> that it accretes: a session that learns one of these facts the hard way — a runner trap, a naming
> rule discovered mid-review, a harness seam — writes it into the matching section as part of its
> change, so the next session reads it instead of re-deriving it.

## Conventions

- Naming and file placement: _<e.g. snake_case filenames, feature-folder layout; where new modules go>_.
- Import/module rules: _<e.g. import ordering, path aliases, barrel-file policy>_.
- Language idioms this repo enforces beyond the linter: _<e.g. `string[]` over `Array<string>`,
  explicit return types on exports; or "linter is the whole story">_.
- Repo-specific patterns a newcomer would miss: _<e.g. i18n fallback policy (new copy lands in English,
  locales follow), error-shape conventions, feature-flag idiom>_.

## Checks

- The full gate, exactly as CI runs it: _<command>_ — and the force-uncached form when the runner
  caches: _<e.g. `pnpm check --force`; or "no cache layer">_.
- Formatter / linter / dead-export check over touched files, run before the full gate: _<commands>_.
- Test runner invocation traps: _<e.g. the `--` that flips a filtered run into the whole suite; watch
  mode as the default; DB-gated suites that skip without a local store; or "none known">_.

## Testing patterns

- Test-harness seams: _<e.g. the backend test harness and its setup helper, the jsdom config and what
  it cannot exercise (real focus, portals), the factory/fixture helpers to use>_.
- Where tests live and how they're named: _<paths and naming rule>_.
- What this repo mocks and what it never mocks: _<e.g. external HTTP always, the database never>_.

## Generated artifacts

- Files that are generated, never hand-edited, each with its regeneration recipe and what the recipe
  needs (a running stack, a schema): _<paths and commands; or "none">_.
- Scope rule: regeneration drift beyond the change at hand is surfaced on the ticket, not silently
  committed.
