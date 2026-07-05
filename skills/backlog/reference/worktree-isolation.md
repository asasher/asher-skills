# Worktree Isolation

The loop dispatches one issue thread per issue, each in its own worktree, and each verifies its change against a running app. That only works if N worktrees can stand up and exercise the dev stack at once without corrupting each other. This file is the contract `setup` audits against and the pattern it scaffolds toward. It also defines the **parallelism verdict** that `run` reads before dispatching.

"Worktree" here is the role noun for an isolated working copy; the mechanics — `git worktree add`, a jj workspace, whatever the repo uses — live in the version-control binding of `docs/agents/platform.md`. The regimes, probes, and scaffold below are about the *stack*, not the VCS, and apply unchanged across bindings.

Do not impose a scheme blindly. First classify the regime, then detect whether the repo already solves it, then — only with approval — scaffold.

## Regimes

- **Isolatable local stack** — the dev stack runs locally (containers and/or host processes: a DB, object store, queue, the app). Isolation is achievable by namespacing per worktree. This is the regime the scaffold targets.
- **Cloud-singleton backend** — the backend is shared cloud state (a managed deployment, a hosted auth tenant, a shared inbox). Local namespacing is meaningless: two worktrees pointed at the same deployment share one database no matter what ports they bind. True isolation needs a fresh per-worktree cloud deployment + auth tenant, which is rarely automated. Default to serializing verification.

A repo can be local-isolatable for its DB yet still depend on a shared external sandbox (one OAuth callback, one webhook target, one seeded tenant). Treat any shared external singleton as forcing the cloud-singleton verdict for the surfaces that touch it.

## Audit probes — what collides

Look for each; every hit is a collision point to report:

- **Fixed container names** — `container_name:` in compose. Two stacks can't both create the same named container.
- **Hardcoded host ports** — fixed `HOST:CONTAINER` ports in compose, `.env`, or app config. Second stack fails to bind.
- **No compose project namespace** — no `name:` / `COMPOSE_PROJECT_NAME`, so containers, volumes, and networks aren't namespaced per worktree.
- **Single shared datastore URL** — one `DATABASE_URL` / Redis URL reused across worktrees, so they read and write the same data even when ports differ.
- **Shared dev proxy hostnames** — a single proxy (e.g. portless on `:1355`) with hostnames hardcoded in `package.json`/`.env` (`app.<name>.localhost`). Worktrees claim the same route. Isolate by per-worktree subdomain, not by moving the proxy port.
- **Hardcoded shared cloud IDs** — a pinned managed-deployment id or hosted auth tenant key (e.g. a Convex deployment, a Clerk instance) shared by every worktree. This is the cloud-singleton signal.
- **Copy-without-remap setup** — a worktree setup script that copies `.env*` into the new worktree but rewrites nothing. Present-but-insufficient: it makes every worktree point at the same resources.

## Detect an existing solution before scaffolding

A repo may already isolate. Signs: a script that derives a per-worktree suffix and a port band from the worktree path, sets `COMPOSE_PROJECT_NAME=<project>-<suffix>`, rewrites datastore URLs and proxy subdomains, and creates per-worktree state dirs — wired to a worktree-create hook so it applies automatically, ideally with tests and an orphan reaper. If found and sound, record "parallel-safe" and defer to it; scaffold nothing.

## Scaffold pattern (local-isolatable regime, on approval)

Offer, and write only with explicit approval, an isolation layer with these parts. Adapt names to the repo; do not copy another repo's specifics.

1. **Derive a per-worktree identity** — a stable suffix from the worktree path (the main checkout keeps canonical values), and a base port derived from it for the services that bind host ports.
2. **Namespace compose** — set `COMPOSE_PROJECT_NAME=<project>-<suffix>` so containers, volumes, and networks are per worktree; parameterize compose ports through env.
3. **Per-worktree datastore and URLs** — rewrite `DATABASE_URL` and service/proxy URLs to the derived ports and a `<name>-<suffix>` subdomain.
4. **Per-worktree local state** — point data/cache dirs at gitignored paths inside the worktree.
5. **Apply automatically** — a worktree-create hook that copies base env, creates the dirs, and applies the derived env, so a freshly dispatched worktree comes up isolated with no manual step.
6. **Escape hatch and cleanup** — an opt-out flag, and a reaper for stacks whose worktree is gone.

## Parallelism verdict

Setup records one verdict in `environment.md`; `run` reads it before dispatch:

- **parallel-safe** — local-isolatable and isolation exists or was scaffolded. Issue threads may verify concurrently.
- **serialize-verification** — cloud-singleton, or local-isolatable but not yet isolated. Dispatch may still fan out worktrees, but only one may stand up the stack and verify at a time; the others queue on that resource. State which shared resource forces serialization.

A `parallel-safe` verdict may carry a **serialized exception lane**: named classes of issues that must serialize anyway — destructive operations on a shared tenant, real third-party endpoints without per-worktree credentials, features needing deliberately distinct users. Setup records the lane in `environment.md`; `run` tells any dispatched thread whose issue falls in it to serialize its verification.
