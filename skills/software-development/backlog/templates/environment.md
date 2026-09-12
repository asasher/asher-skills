# Playbook: Environment

Record this repository's demonstrated capabilities, configuration pointers, and invocation requirements. Tailor each section to the project; mark inapplicable items with a reason. The family skills own workflow policy.

## Branching

- Base branch: _<e.g. `main`>_. Worktree root: _<e.g. sibling `<repo-name>-worktrees/`>_.
- Merge protection: _<target-branch rules, strict up-to-date required checks or merge-group verification/review gate, actor bypass behavior, and configuration gaps>_.
- PR result: _<preview deployment or other output>_.
- Merge result and promotion path: _<deployment targets and how changes reach production>_.
- Deploy constraints: _<runtime, packaging, asset limits>_.

## Running locally

- Start detached and log output: _<canonical entrypoint and additional wrapper if needed>_. Stop: _<entrypoint>_.
- Services, ports, and hostnames: _<configuration pointers>_.
- Per-worktree bring-up and teardown: _<entrypoints and how both identify the same isolated stack and disposable volumes>_.

## Checks

- Full gate: _<CI definition, checked integration tree, and local entrypoint>_. Fresh-run requirements: _<cache overrides or other requirements>_.
- Focused checks: _<formatter, linter, typecheck, tests, and other applicable entrypoints>_.
- Runner traps: _<watch defaults, filtering, gated suites, or none known>_.
- Generated files: _<generator configuration and additional invocation requirements>_.
- Conventions beyond linting: _<project-specific naming, placement, or idioms>_.

## Agent-readiness

Record the `agent-ready-codebase` assessment: _<date, capabilities demonstrated with evidence, gaps, and justified inapplicable items>_.

- Concurrent-build limit: _<tested capacity>_. Admission mechanism: _<dispatch owner or shared lock and how to acquire/release it>_.
- Shared singletons: _<resource, what use or change collides, and isolation or serialization required>_.
- Punch list: _<gaps and issue links, or none>_.

## Seed

- Seed or dataset loader: _<entrypoint>_. Fresh contents: _<available feature states>_.
- Drive-to-feature paths: _<routes, roles, navigation, and preconditions for each feature area>_.

## Authenticating

- Auth model and session creation: _<agent-usable login flow>_.
- Per-run auth isolation and storage: _<account allocation, independent sessions, and ignored storage location>_.
- Credentials: _<test account references and secret variable/store names only>_.

## Verification data

- Standing accounts and tenants: _<what each unlocks>_.
- Per-run fixture allocation and cleanup: _<collision-safe naming and ownership>_.
- Disposable stores: _<explicit reset/drop/wipe targets and how each is isolated>_.

## Driving the app and capturing evidence

- Surfaces: _<CLI, web, mobile, desktop>_.
- Web driver: _<headless Playwright entrypoint/configuration, or an alternative demonstrated under `verify-your-work`'s isolation requirements>_.
- Runtime support: _<tested execution hosts, browser provisioning, app reachability, per-run browser/session isolation, and capture paths>_.
- Other surfaces: _<drivers, isolation, and capture methods>_.
- Gaps and fallbacks: _<unavailable capabilities and demonstrated alternatives>_.

## Artifact store

- Provider: _<S3-compatible service>_. Bucket: _<name>_. Base URL: _<URL>_.
- Credential environment variable names: _<names only>_.
- Upload: _<canonical entrypoint and provider endpoint requirements>_.
