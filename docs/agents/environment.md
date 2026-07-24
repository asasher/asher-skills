# Playbook: Environment

> Project playbook for this repo. Shared — read by any stage that builds a branch, runs, or tests the app (`implement`, `verify-your-work`, `prove-your-work`, `diagnosing-bugs`, the change-request step, the `adversarial-review` fixer) and by `backlog build` for the parallelism verdict. Tailor every section to this codebase. `backlog setup` fills the isolation, seed, and parallelism sections from its audit.

## Branching & deploys

- Base branch: **main** — create work branches (and any worktrees) from it, and target PRs at it. Sync it per `platform.md` § Version control before branching.
- Branch naming: `<issue-number>-<slug>` (e.g. `6-slim-backlog-composer`).
- What a PR produces: nothing automated — no CI, no preview deploy. Review is human + `adversarial-review`.
- What a merge produces: nothing automated. Skills are consumed elsewhere via `npx skills add <repo-url> --skill <name>`; a merge just updates `main`. No deploy step, no promotion path.
- Deploy-target constraints: **n/a** — skills are consumed via `npx skills add`; there is no deploy target.
- Credential preflight (run before work that will hit either gate): `gh auth status` proves the tracker/PR credential is live; a cheap `codex exec -s read-only --skip-git-repo-check "reply OK"` proves the second-executor route. This is what `backlog build`'s per-run preflight uses.

## Running locally

> This is a **skills repository**, not a running product. "The app" is the skills themselves; there is no dev stack, no services, no ports.

- Start the full dev stack: **n/a** — nothing to boot.
- To exercise a skill (the equivalent of "running the app"): invoke it in a harness against a scenario. From Claude Code, the `Skill` tool or a subagent that reads the skill's `SKILL.md`; from Codex, per the skill's `agents/openai.yaml`. A "run" is a probe scenario driven through an executor model — see § Driving the app.
- Scripts the skills ship (e.g. `scripts/review-server.py`) are stdlib-only Python 3 — run directly with `python3`, no install.
- Services / ports / URLs: **none**, except the presentation surface (§ Presenting) and any transient review-server port.
- Headless contract: **no dev stack — nothing to detach.** The only long-lived processes are review servers, which already run detached with logs and a recorded stop (`--stop --state <dir>`); teardown is audited via `tailscale serve status` plus the reap rule in § Presenting.

## Worktree isolation

> Set by `setup` per `reference/worktree-isolation.md`.

- Regime: **local-isolatable** — skills are files + stdlib-Python scripts with no shared runtime state, so a `git worktree` is a complete isolated copy. No derived env, no ports to remap.
- How to bring up an **isolated** stack for one worktree: `git worktree add <path> -b <branch> main` is sufficient — there is nothing else to stand up. Sequential verdict means the loop normally works the main checkout on a branch and does not fan out worktrees.
- **Shared-singleton list** — there is no code-level shared runtime (no DB, no ports, no shared build cache; each skill is files + stdlib scripts), so the code isolates completely. The only singletons are loop infrastructure, both handled without serializing code work:

  | Singleton | Collision mode | Locally isolatable? |
  |-----------|----------------|---------------------|
  | GitHub tracker | one issue graph | no — but serialized main-branch writes handle it |
  | Tailnet presentation surface | one URL root | no — one review published at a time |

  Neither collides with two worktrees editing skill files, so they do not force serialized *verification* of the code.

  One row is standing in every multi-worktree repo: the parent `.git` itself. Concurrent git operations from parallel worktrees can collide on its locks (`index.lock`, ref locks) — a lock error is contention, so wait and retry briefly; a lock that outlives the retry with no live git process behind it is a crashed operation's leftover, and only then safe to remove.

## Seed data

- Seed regime: **none — drive the skill.** There is no data store to seed.
- Command (if any): n/a.
- **Drive-to-feature path:** the "state" a skill needs is a **probe scenario** — a situated dry-run prompt plus an answer key, per `docs/agents/probe-evals.md`. A skill's own `evals/` directory holds its scenarios; verification drives those scenarios through an executor model (§ Driving the app) rather than seeding a database and navigating a UI. (This is the greenfield/no-app case evidence.md names — there is no running app surface to drive, so probes are the honest substitute here.)

## Authenticating for testing

- Auth model: **none for exercising skills** — running a skill against a scenario needs no login. Two credentials support the loop's infrastructure, both already provisioned on this machine:
  - GitHub tracker/PRs: `gh` CLI, authed as `asasher` (keyring). Mints nothing per-run.
  - Codex executor (gpt-5.6-sol / gpt-5.6-terra): the Codex CLI, authed to its own subscription (`codex --version` → 0.144.1). Billed separately from the session.
- How an agent mints a session: n/a — no app session to mint.
- Test accounts / where credentials live: `gh` keyring and `~/.codex/`; never hardcode, never echo them.

## Verification data

- Standing accounts/tenants and permissions: local filesystem fixtures plus the authenticated GitHub repo
  with issue/PR read-write access; no product test tenant or second application user is required here.
- Per-issue fixture naming: `VERIFY-<issue>-<purpose>` under a temporary directory or the owning
  `<skill>-workspace/`; never share a mutable fixture across issue runs.
- Scale: use generated temporary skill trees for catalog/closure tests and temporary state/surface roots for
  review lifecycle tests.
- Approved synthetic substitutes: situated prompt fixtures may exercise skill decisions because this repo has
  no product runtime; they do not substitute for live GitHub API behavior or script lifecycle/process checks.
- Lifetime/cleanup: the owning test retains fixtures through its final assertion/evidence capture, then
  removes only its own temporary root.
- **Per-ticket-disposable stores** — what a single ticket may reset or wipe wholesale: the ticket's own
  worktree, its `VERIFY-<issue>-*` fixtures and temporary roots, and its own
  `~/.backlog/surface/asher-skills/<issue>/` entry. Everything else is shared, and destructive verbs stop
  at this line.

## Driving the app & capturing evidence

> Set by `backlog setup`'s app-access audit; read by `verify-your-work` (to exercise the app) and `prove-your-work` (to capture proof). One entry per surface the loop verifies.

- Form factor(s): **skill** — a Claude Code / Codex skill (SKILL.md + references/scripts). Not CLI/web/mobile/desktop. The thing under test is a prompt-driven procedure, so "driving the app" means running the skill against a scenario and judging the transcript.
- Web driver: the v2 **Playwright-driving-Chrome** default is **n/a here** — there is no browser-driven app surface; probe executors are the drivers. The rule stays visible for the one browser-shaped case this repo has: judging **rendered HTML artifacts** (plans, prototypes, maquettes) covers happy/empty/error states in both color schemes, with screenshots as evidence; harness-native browser tools and `agent-browser` remain non-verification routes.
- Driver per surface:
  - **In-session executor (Claude):** spawn a subagent (Agent tool, `subagent_type: claude` or `general-purpose`) that reads the target skill's `SKILL.md` and works a probe scenario. This is the primary driver — Opus/Fable in-session.
  - **Independent executor (gpt-5.6-sol):** `codex exec -s read-only --skip-git-repo-check` (or `-s workspace-write` when the run must edit) with a self-contained prompt that points at the skill and scenario. A second, differently-modeled executor per `docs/agents/probe-evals.md`.
  - Any stdlib script a skill ships (e.g. `review-server.py`) is driven directly with `python3`.
- Independent runtime verification: delegate a scenario to `codex exec` for a second executor outside the orchestrator's context (mechanics in `~/.claude/CLAUDE.md` § Staffing → Mechanics, the global base). Reading skill files, grading transcripts against an answer key, and running a skill's `scripts/` stay local.
- Evidence capture per surface: the **eval transcript** (the executor's run) plus a **pass/fail verdict table** mapping each probe to its answer-key criterion. For a skill that produces a visual artifact (e.g. `maquette`, a rendered plan), also a screenshot of the rendered HTML. Terminal transcripts for script behavior.
- Supporting tools: `docs/agents/probe-evals.md` (the eval harness), the skill's own `evals/` dir, and the review surface (§ Presenting) for artifacts a human should eyeball.
- Gaps: no automated CI — every check is agent-driven on demand. A skill whose value is subjective (taste of copy, feel of a flow) can't be fully graded mechanically; the fallback is a human review pass on the presentation surface.

## Presenting to the human

> Owned by the **`serve-via-tailnet`** skill (composed by name): the presentation surface and interactive review — how plans, prototypes, and review sheets reach a human who may not be at the machine. Read by `prototype` and `to-spec` when they pause for review; serve-via-tailnet's setup records this repo's surface config here. The shipped default is a singular tailnet surface; local-only and custom channels are legitimate alternates.

- Surface: **tailnet** (`tailscale serve`, Funnel off — private to Asher's own devices: this MacBook + iphone-14-pro-max).
- **Always open in the browser:** whenever a plan or prototype is published for review, open its URL locally with `open <url>` immediately after presenting — standing instruction from Asher, every presentation, no need to ask.
- Root URL: `https://ashers-macbook-pro.tail045dd5.ts.net/asher-skills` (machine root `https://ashers-macbook-pro.tail045dd5.ts.net`; tailscale 1.98.8).
- Surface directory: `~/.backlog/surface/asher-skills` — holds `registry.json` and the generated `index.html` (the hub) at its root, plus each issue's published static docs under `<issue>/`.
- Bringing the tailnet up (precondition for every publish/serve below; contract: serve-via-tailnet `reference/surface-and-hub.md` § Bringing the tailnet up): all the `tailscale serve` commands here assume this node is on the tailnet. Before publishing a review, check with `tailscale status` — it exits non-zero and prints `Logged out.` / `Tailscale is stopped.` when the node is down. Only when it is down **and** a review is being published now, run `tailscale up` to reconnect. If `tailscale status` already succeeds (node connected, peers listed), do nothing — never `tailscale down`/`up` to "reset" a healthy connection. If `tailscale up` prints an auth URL or fails (expired key, SSO/admin approval), surface that to Asher as the blocker and fall back to opening the file locally (`open <file>`) with a note that remote review is unavailable — never enable Funnel or improvise a public tunnel.
- Document server: the sandboxed macOS tailscale app cannot serve file paths, so static docs are served by a stdlib static server rooted at the surface dir and proxied once:
  - `python3 -m http.server 8390 --directory ~/.backlog/surface/asher-skills` (a stable port; pick another if 8390 is taken — 8377 is already held by a prior `/review` handler).
  - `tailscale serve --bg --set-path /asher-skills http://localhost:8390`.
- Publish a document: `mkdir -p ~/.backlog/surface/asher-skills/<issue> && ln -sfn <absolute path to the committed HTML> ~/.backlog/surface/asher-skills/<issue>/<name>.html` → resolves at `<root URL>/<issue>/<name>.html`.
- Review server (annotated review with a recorded verdict — optional: spec sign-off lives on the ticket and prototype feedback arrives in chat, so this serves only artifacts that need one; contract: serve-via-tailnet `reference/annotation-contract.md`; scripts ship with the `serve-via-tailnet` skill — self-host path `skills/software-development/serve-via-tailnet/scripts/`): `python3 skills/software-development/serve-via-tailnet/scripts/review-server.py --doc <file> --title "…" --issue <n> --kind plan --state <run state dir> --surface ~/.backlog/surface/asher-skills --port <p> --public-url https://ashers-macbook-pro.tail045dd5.ts.net/asher-skills/<n>/review`, with the port proxied once — `tailscale serve --bg --set-path /asher-skills/<n>/review http://localhost:<p>`. The agent blocks on `python3 skills/software-development/serve-via-tailnet/scripts/review-await.py --state <run state dir> --timeout <secs>` (exit 0 approve / 3 nits / 10 changes / 124 timeout).
- Hub: `https://ashers-macbook-pro.tail045dd5.ts.net/asher-skills/` serves the generated `index.html` beside `registry.json`; swept by `python3 skills/software-development/serve-via-tailnet/scripts/review-server.py --sweep --surface ~/.backlog/surface/asher-skills`.
- Expose a live prototype: `tailscale serve --bg --set-path /asher-skills/<n>/proto http://localhost:<port>`.
- Reap rule: on teardown, remove the issue's symlinks under `~/.backlog/surface/asher-skills/<n>/` and turn off its proxies — `tailscale serve --set-path /asher-skills/<n>/review off` (and `.../proto off`); `tailscale serve status` lists live handlers for the orphan sweep. **Note:** the pre-existing `/review → http://localhost:8377` handler (the v1 multi-repo hub) was reaped 2026-07-24 during the v2 migration; the LaunchAgent `com.asher.backlog-surface` still serves `~/.backlog/surface` on 8377 locally, and port 8377 remains taken.
- Keep-awake: **none** (setup choice) — the surface is up when the machine is awake; harnesses hold sleep assertions during active runs. No LaunchAgent, no `caffeinate`. AFK reviews that outlast an active run may find the machine asleep; revisit if that bites.

## Model staffing

Resolve the active harness's deferred global staffing module, then apply `CLAUDE.md` § Staffing. This repo
adds two deltas only: skill design remains orchestration-grade, and probe evals use the dual-executor contract
in `docs/agents/probe-evals.md`. There is no project floor, capability-provider, or succession override.

## Parallelism verdict

> Read by `backlog build` before dispatch.

- Verdict: **parallel-safe** — re-derived 2026-07-24 under v2 semantics (asher-skills#95): the v1 record said `serialize-verification` but justified it as "user chose sequential", and the shared-singleton audit above shows **no code-level collision** — nothing environmental forces serialization. v2 distinguishes constraint from preference, so the honest verdict is parallel-safe.
- Standing dispatch preference: **sequential** — Asher's recorded working preference is one issue thread at a time; `backlog build` defaults to that unless he asks for fan-out. This is policy, not environment: no lane lock, no exception lane, and the preference can change per-run without re-auditing.
- The tracker and review surface handle concurrency by serializing their own writes, never by serializing code verification. (Keep-awake stays **none** — reconfirmed 2026-07-24; the note lives beside § Presenting.)
