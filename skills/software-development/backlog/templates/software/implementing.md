# Playbook: Implementing

> Project playbook for this repo. The backlog `implement` subskill reads this file for how to build; the gates are in the skill's `reference/implement.md`. Base branch, branch naming, and running locally are in `environment.md`. The test-first technique below is the shipped default — replace it with house practice if this team builds differently.

## What deserves a test

Test-first is the default for logic-bearing work, not a ritual for every change. Test where behavior can be wrong in ways the compiler can't catch — branching, state transitions, calculations, parsing, contracts between modules. Skip tests where they add churn without catching anything:

- **Enforced by end-to-end type safety** — exhaustive unions, compiler-checked wiring, schema-derived types. The type checker is already the test; a unit test restating it is tautological.
- **Fluid UI** — visual appeal, layout, spacing, copy, a button's label. Correctness here is judged by eye and changes too often to lock down; the verify step and evidence capture cover it against the running app.
- **Declarative glue with no branching** — configuration, straight pass-through wiring.

When in doubt, the tie-breaker is the cost of being wrong: a payment calculation deserves a test even where it looks type-safe; a marketing page never does. A skipped test is a stated decision, not an omission.

## Build test-first

For the work that deserves tests, work red → green in vertical slices:

- **Agree the seams first.** A seam is the public boundary you test at — the interface where behavior is observable without reaching inside. The plan's acceptance criteria name the behaviors; before writing any test, list the seams they will be tested at — and the surfaces deliberately left untested, with why — and record both against the plan. Testing effort lands on critical paths and complex logic, not every edge case — and never on internals.
- **Red before green.** Write one failing test, then only enough code to make it pass. No speculative features, no anticipating future tests.
- **One slice at a time** — one seam, one test, one minimal implementation per cycle, each test a tracer bullet that responds to what the last cycle taught you. Never write all tests first: bulk-written tests verify imagined behavior and commit you to structure before you understand the implementation.
- **Refactoring is not part of the loop.** Structural cleanup happens after the behavior is in, under the tests you just wrote — and gets scrutinized again in adversarial review.

## Tests worth keeping

- Verify behavior through the public interface. A good test reads like a specification — "user can check out with a valid cart" — and survives refactors because it doesn't care about internal structure.
- Expected values come from an independent source of truth: a known-good literal, a worked example, the spec. Never recompute the expectation the way the code computes it — that test passes by construction and can never disagree with the code.
- Red flags: mocking internal collaborators, testing private methods, asserting on call counts or order, verifying through a side channel (querying the database instead of using the interface), test names that describe *how* instead of *what*, tests that break on refactors when behavior hasn't changed.
- Mock at system boundaries only — external APIs, time, randomness, sometimes filesystem and database (prefer a test DB). Never mock your own modules. Pass boundary dependencies in (dependency injection), and prefer specific SDK-style functions per external operation over one generic fetcher, so each mock returns one shape with no conditional logic in test setup.

## Commits

- Commit style this repo expects (Conventional Commits, message format, sign-off): _<add yours>_.

## UI surfaces

- Building UI loads the `bare-minimum-ux` sibling skill where installed (the UX baseline overlay — it wins on conflict); absent, state the gap rather than skipping. When
  the project's `external-dependencies.lock.json` records the consented `impeccable` external, load it too:
  `PRODUCT.md`/`DESIGN.md` are ambient context for every UI change (DESIGN.md wins on visual decisions,
  PRODUCT.md on strategy/voice), and its craft rules govern the build.
- Ship every interactive state — default, hover, focus, disabled, loading, error, empty — not just the happy
  path; the verify step inspects them (`verifying.md` § UI surfaces).

## Code conventions

- Defer to `CLAUDE.md` / linters / formatters in this repo for style.
- Anything not captured by tooling that reviewers still expect: _<add yours>_.

## Scope discipline

- Build only what the approved plan (or agreed small change) calls for. Record any deviation against the plan.

## This repo's testing setup

- Test framework and how to run a single test: _<add yours>_.
- Where tests live relative to source: _<add yours>_.
