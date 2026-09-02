# Playbook: Environment

> Project playbook for this repo, and the only one the software development lifecycle skills read: how to run, seed, authenticate to, drive, and prove this application, and where its artifacts live. Read by `backlog build` (the agent-readiness gate), `backlog status` (the teardown sweep), `deliver`, `implement`, `tdd`, `verify-your-work`, `prove-your-work`, `merge`, `worktree`, and `to-web`. Tailor every section to this codebase. A session that earns a fact this playbook should have carried (a start recipe, an auth path, a runner trap) writes it into the matching section as part of its change. Repo facts accrete here; machine state is never recorded. A capability is checked at use, and a failed check warns and names its fallback.

## Branching

- Base branch: _<e.g. `main`>_. Worktrees and work branches fork from it and PRs target it. The primary checkout stays on it; work branches are born inside their worktrees.
- What a PR produces: _<e.g. a preview deployment per PR, or nothing>_.
- What a merge produces: _<e.g. a deployment to staging; the promotion path to production>_.
- Deploy-target constraints: _<runtime and version, packaging, asset limits; accrete each as discovered>_.

## Running locally

- Start the full dev stack, detached, with output to a log: _<command>_. Stop: _<command>_.
- Services that come up: _<e.g. web, API, Postgres, redis, object store>_. Ports and hostnames: _<add yours>_.
- Per-worktree bring-up: _<the command or hook that gives one worktree its own stack beside the others>_. Teardown: _<command, or "nothing to tear down">_. Teardown must resolve the same compose project the bring-up resolved (same env files, same project-name derivation, run from inside the worktree) and remove its volumes; a hardcoded compose project or container name fails this twice, since concurrent stacks collide.

## Checks

- The full gate, exactly as CI runs it: _<command>_. Force-uncached form when the runner caches: _<command, or "no cache layer">_.
- Formatter, linter, and dead-export check over touched files, run before the full gate: _<commands>_.
- Test runner traps: _<e.g. the `--` that flips a filtered run into the whole suite; watch mode as the default; DB-gated suites; or "none known">_.
- Generated files, never hand-edited, each with its regeneration recipe: _<paths and commands; or "none">_.
- Conventions the linter does not enforce: _<naming, placement, idioms a newcomer would miss; or "linter is the whole story">_.

## Agent-readiness

> The standard is the `agent-ready-codebase` reference skill; this section records this repo's answers. `backlog setup` certifies, `backlog build` dispatches only on a full pass. Re-certify on demand.

1. **Worktrees**: the `worktree` skill can create, inspect, and remove working copies here: _<pass | gap>_.
2. **Stack per worktree**: each working copy brings up its own dev stack beside the others: _<pass | gap>_.
3. **Auth per worktree**: an agent can mint a session in each copy independently: _<pass | gap>_.
4. **Seed**: seed data exists and reaches everything the app offers: _<pass | gap>_.

Shared singletons, one row each. Parallel builds may use a singleton; an issue that changes one is sliced so the change lands first.

| Singleton | Collides on | Notes |
| --- | --- | --- |
| _<e.g. one managed auth deployment>_ | _<change only>_ | _<add yours>_ |
| the parent `.git` | use (locks) | a lock error is contention: wait and retry; a lock outliving the retry with no live git process behind it is a crashed operation's leftover |

Punch list: _<the gaps certification found, each groomable as an issue; or "none, certified <date>">_.

## Seed

- Seed command: _<e.g. `pnpm dev:seed`, or the dataset-load command; or "none, drive the app">_.
- What a freshly seeded stack contains: _<add yours>_.
- The seed is a maintained artifact: a change that adds a feature extends the seed in the same PR, and the verifier treats "the seed reaches this feature" as a claim.
- Drive-to-feature paths: from a running, seeded stack, how to reach the state that exercises each feature area (entry route, navigation, precondition state such as a logged-in role or a created record): _<add yours, or "n/a, no app surface">_.

## Authenticating

- Auth model: _<e.g. email magic link, OAuth, username and password, API token>_.
- How an agent mints a session: _<e.g. trigger an OTP, read it from the test inbox, complete login in the browser driver>_.
- Session reuse: mint once per run and persist the browser storage state at _<e.g. `e2e/.auth/state.json`, gitignored>_; later checks load it.
- Test accounts and where credentials live: _<environment variable names or secrets store; never values, never `.env` contents>_.

## Verification data

- Standing accounts and tenants: _<what exists and what each unlocks>_.
- Per-issue fixture naming: `VERIFY-<issue>-<purpose>` unless this repo records another collision-safe form. Provision before verification, retain through evidence, then remove only this issue's fixtures.
- Per-issue-disposable stores, the only targets a destructive verb may reset, drop, or wipe: _<list them; everything else is shared>_.

## Driving the app and capturing evidence

> Verification is code, not improvisation: a browser check is a script whose run is reproducible. Read by `verify-your-work` and `prove-your-work`.

- Surfaces this repo's issues touch: _<CLI | web | mobile | desktop>_.
- Web driver: Playwright driving Chrome. Scripts live in _<e.g. `e2e/`>_ and run with _<e.g. `npx playwright test`>_. Evidence comes from Playwright's own artifacts (trace, screenshots, video). Headless is checked at use; headed is the fallback. Harness-native browser tools are not verification routes.
- Two kinds of check: **guards**, durable tests that protect product behavior and stay in the suite; and **throwaway verification scripts**, written to exercise the change and capture screenshots, dropped before merge, their run kept as evidence. The spec declares which each acceptance criterion gets; an unshaped issue's builder decides and says so in the PR.
- Other surfaces: _<a simulator and driver for mobile; shell plus the CLI entrypoint; desktop only behind a recorded use case and explicit approval>_.
- Gaps: _<surfaces the agent cannot drive or capture, and the fallback; or "none">_.

## Artifact store

> Read by `to-web`, and through it by `prove-your-work` (evidence media) and `shape` (spec, dossier, and prototype renders). Media is never committed to the repo. Visibility is public with unguessable keys.

- Provider: _<S3-compatible; reference example: Cloudflare R2>_.
- Bucket: _<name>_. Base URL: _<e.g. `https://<bucket>.<account>.r2.dev/`>_.
- Credential environment variable names: _<e.g. `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ACCOUNT_ID`>_. Names only, never values.
- Upload command: _<e.g. `aws s3 cp <file> s3://<bucket>/<key> --endpoint-url https://<account>.r2.cloudflarestorage.com`>_.
