# Playbook: Environment

> Project playbook for this repo. Shared — read by any backlog subskill that builds a branch, runs, or tests the app (`implement`, `verify`, `evidence`, `diagnose`, the PR step, the review fixer) and by `run` for the parallelism verdict. Tailor every section to this codebase. `setup` fills the isolation, seed, and parallelism sections from its audit.

## Branching & deploys

- Base branch: **main** — create work branches (and any worktrees) from it, and target PRs at it. Sync it per `platform.md` § Version control before branching.
- Branch naming: `<issue-number>-<slug>` (e.g. `6-slim-backlog-composer`).
- What a PR produces: nothing automated — no CI, no preview deploy. Review is human + `adversarial-review`.
- What a merge produces: nothing automated. Skills are consumed elsewhere via `npx skills add <repo-url> --skill <name>`; a merge just updates `main`. No deploy step, no promotion path.

## Running locally

> This is a **skills repository**, not a running product. "The app" is the skills themselves; there is no dev stack, no services, no ports.

- Start the full dev stack: **n/a** — nothing to boot.
- To exercise a skill (the equivalent of "running the app"): invoke it in a harness against a scenario. From Claude Code, the `Skill` tool or a subagent that reads the skill's `SKILL.md`; from Codex, per the skill's `agents/openai.yaml`. A "run" is a probe scenario driven through an executor model — see § Driving the app.
- Scripts the skills ship (e.g. `scripts/review-server.py`) are stdlib-only Python 3 — run directly with `python3`, no install.
- Services / ports / URLs: **none**, except the presentation surface (§ Presenting) and any transient review-server port.

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

## Driving the app & capturing evidence

> Set by `setup`'s app-access audit; read by `verify` (to exercise the app) and `evidence` (to capture proof). One entry per surface the loop verifies.

- Form factor(s): **skill** — a Claude Code / Codex skill (SKILL.md + references/scripts). Not CLI/web/mobile/desktop. The thing under test is a prompt-driven procedure, so "driving the app" means running the skill against a scenario and judging the transcript.
- Driver per surface:
  - **In-session executor (Claude):** spawn a subagent (Agent tool, `subagent_type: claude` or `general-purpose`) that reads the target skill's `SKILL.md` and works a probe scenario. This is the primary driver — Opus/Fable in-session.
  - **Independent executor (gpt-5.6-sol):** `codex exec -s read-only --skip-git-repo-check` (or `-s workspace-write` when the run must edit) with a self-contained prompt that points at the skill and scenario. A second, differently-modeled executor per `docs/agents/probe-evals.md`.
  - Any stdlib script a skill ships (e.g. `review-server.py`) is driven directly with `python3`.
- Independent runtime verification: delegate a scenario to `codex exec` for a second executor outside the orchestrator's context (mechanics in `~/.claude/CLAUDE.md` § Staffing → Mechanics, the global base). Reading skill files, grading transcripts against an answer key, and running a skill's `scripts/` stay local.
- Evidence capture per surface: the **eval transcript** (the executor's run) plus a **pass/fail verdict table** mapping each probe to its answer-key criterion. For a skill that produces a visual artifact (e.g. `maquette`, a rendered plan), also a screenshot of the rendered HTML. Terminal transcripts for script behavior.
- Supporting tools: `docs/agents/probe-evals.md` (the eval harness), the skill's own `evals/` dir, and the review surface (§ Presenting) for artifacts a human should eyeball.
- Gaps: no automated CI — every check is agent-driven on demand. A skill whose value is subjective (taste of copy, feel of a flow) can't be fully graded mechanically; the fallback is a human review pass on the presentation surface.

## Presenting to the human

> Owned by the **`review-loop`** skill (composed by name): the presentation surface and interactive review — how plans, prototypes, and review sheets reach a human who may not be at the machine. Read by `plan` and `prototype` when they pause for review; review-loop's setup records this repo's surface config here. The shipped default is a singular tailnet surface; local-only and custom channels are legitimate alternates.

- Surface: **tailnet** (`tailscale serve`, Funnel off — private to Asher's own devices: this MacBook + iphone-14-pro-max).
- **Always open in the browser:** whenever a plan or prototype is published for review, open its URL locally with `open <url>` immediately after presenting — standing instruction from Asher, every presentation, no need to ask.
- Root URL: `https://ashers-macbook-pro.tail045dd5.ts.net/asher-skills` (machine root `https://ashers-macbook-pro.tail045dd5.ts.net`; tailscale 1.98.8).
- Surface directory: `~/.backlog/surface/asher-skills` — holds `registry.json` and the generated `index.html` (the hub) at its root, plus each issue's published static docs under `<issue>/`.
- Bringing the tailnet up (precondition for every publish/serve below; contract: review-loop `reference/surface-and-hub.md` § Bringing the tailnet up): all the `tailscale serve` commands here assume this node is on the tailnet. Before publishing a review, check with `tailscale status` — it exits non-zero and prints `Logged out.` / `Tailscale is stopped.` when the node is down. Only when it is down **and** a review is being published now, run `tailscale up` to reconnect. If `tailscale status` already succeeds (node connected, peers listed), do nothing — never `tailscale down`/`up` to "reset" a healthy connection. If `tailscale up` prints an auth URL or fails (expired key, SSO/admin approval), surface that to Asher as the blocker and fall back to opening the file locally (`open <file>`) with a note that remote review is unavailable — never enable Funnel or improvise a public tunnel.
- Document server: the sandboxed macOS tailscale app cannot serve file paths, so static docs are served by a stdlib static server rooted at the surface dir and proxied once:
  - `python3 -m http.server 8390 --directory ~/.backlog/surface/asher-skills` (a stable port; pick another if 8390 is taken — 8377 is already held by a prior `/review` handler).
  - `tailscale serve --bg --set-path /asher-skills http://localhost:8390`.
- Publish a document: `mkdir -p ~/.backlog/surface/asher-skills/<issue> && ln -sfn <absolute path to the committed HTML> ~/.backlog/surface/asher-skills/<issue>/<name>.html` → resolves at `<root URL>/<issue>/<name>.html`.
- Review server (interactive review — plans, prototype answer sheets; contract: review-loop `reference/review-loop.md`; scripts ship with the `review-loop` skill — self-host path `skills/review-loop/scripts/`): `python3 skills/review-loop/scripts/review-server.py --doc <file> --title "…" --issue <n> --kind plan --state <run state dir> --surface ~/.backlog/surface/asher-skills --port <p> --public-url https://ashers-macbook-pro.tail045dd5.ts.net/asher-skills/<n>/review`, with the port proxied once — `tailscale serve --bg --set-path /asher-skills/<n>/review http://localhost:<p>`. The agent blocks on `python3 skills/review-loop/scripts/review-await.py --state <run state dir> --timeout <secs>` (exit 0 approve / 3 nits / 10 changes / 124 timeout).
- Hub: `https://ashers-macbook-pro.tail045dd5.ts.net/asher-skills/` serves the generated `index.html` beside `registry.json`; swept by `python3 skills/review-loop/scripts/review-server.py --sweep --surface ~/.backlog/surface/asher-skills`.
- Expose a live prototype: `tailscale serve --bg --set-path /asher-skills/<n>/proto http://localhost:<port>`.
- Reap rule: on teardown, remove the issue's symlinks under `~/.backlog/surface/asher-skills/<n>/` and turn off its proxies — `tailscale serve --set-path /asher-skills/<n>/review off` (and `.../proto off`); `tailscale serve status` lists live handlers for the orphan sweep. **Note:** setup found a pre-existing `/review → http://localhost:8377` handler from an earlier session — reap it if dead (`tailscale serve --set-path /review off`).
- Keep-awake: **none** (setup choice) — the surface is up when the machine is awake; harnesses hold sleep assertions during active runs. No LaunchAgent, no `caffeinate`. AFK reviews that outlast an active run may find the machine asleep; revisit if that bites.

## Model staffing

> Owned by the **`staffing`** skill (composed by name): it defines the roles (its `reference/roles-and-fallback.md`: orchestrator, builder by surface, checker, floor), rankings, and the fallback ladder. Read by `run` at dispatch and by every reference that spawns work. The general rankings and routing rules live in the **global base** — `~/.claude/CLAUDE.md` § Staffing, mirrored (Codex-filtered) in `~/.codex/AGENTS.md` § Staffing — with this repo's deltas in the project `CLAUDE.md` § Staffing; resolve base-then-deltas. This section is the **compiled roster** — those rules crossed with this repo's surfaces and what each harness can actually reach; list only reachable models, since one harness usually cannot spawn another vendor's models. One model may fill several roles.

- Floor: **sonnet-5** (Claude-side) or **gpt-5.6-terra** (Codex-side) — never Haiku (global base § Staffing). Nothing staffs below the Floor in any role.
- **One thread pattern everywhere: orchestrator + subagents.** Every delegated thread — Claude or Codex — runs as an Agent-tool subagent the orchestrator watches; completion wakes the orchestrator, so it also watches the threads. A Codex thread is held by a thin wrapper subagent (`model: 'sonnet', effort: 'low'`, labeled `gpt-5.6-sol:…`) that composes a self-contained codex prompt, runs `codex exec` via Bash, and returns the report. No raw fire-and-forget background shells for delegated work.
- From **Claude Code** (this loop's harness):
  - Orchestrator: the session model — **fable-5** in current sessions; the most capable reachable Claude model in general.
  - Builder (backend / mechanical — clear-spec skill edits, reference rewrites, bulk work): **gpt-5.6-sol via `codex exec`** (`~/.claude/CLAUDE.md` § Staffing → Mechanics, the global base), through the wrapper-subagent pattern above. Parallel codex edit agents use `isolation: 'worktree'`.
  - Builder (ui / taste ≥ 7 — SKILL copy, plan/prototype HTML, anything user-facing): a Claude model via the Agent `model` override — **fable-5** (taste 9) or **opus-4.8** (taste 7).
  - Checker: probe-eval executor runs on **both** gpt-5.6-sol (`codex exec`) and a Claude model in-session, per `docs/agents/probe-evals.md`'s dual-executor design; verify⇆fix mechanics on gpt-5.6-sol; review/grading judgment on **fable-5 or opus-4.8** (skill reviews and probe grading, per `AGENTS.md`). The Reviewer handles the full criteria including rendered artifacts.
  - Watcher / cron (review-verdict watches, PR-merge watches, scheduled check-ins): the Floor — **sonnet-5** in-session; **gpt-5.6-terra** for Codex-side scheduled jobs. Watchers only wait and relay; judgment escalates to the orchestrator.
  - Capability pins (gates before ranking): **browser-use → gpt-5.6-terra**, **computer-use → gpt-5.6-terra**, both via the Codex computer-use client (Claude-side headless Chrome is blocked on this machine).
- From **Codex** (if the loop is ever driven from Codex instead): Claude models are unreachable, so every role collapses onto **gpt-5.6-sol** (terra for watch/cron). The **same orchestrator-subagent pattern holds**: the Codex orchestrator delegates each thread to its native agent-thread facility (`[agents]` in `~/.codex/config.toml` — max_depth 3, max_threads 20 on this machine) and watches them — no fire-and-forget shells there either.
- Succession: if the session model is unreachable, the most capable reachable Claude model orchestrates (**fable-5**, then opus-4.8, then sonnet-5), keeping all Claude-side roles; **gpt-5.6-sol via `codex exec`** remains the mechanical builder/checker regardless, since it bills to its own subscription.

## Parallelism verdict

> Read by `run` before dispatch.

- Verdict: **serialize-verification** — user chose sequential at setup. `run` dispatches one issue thread at a time.
- If serialized, the singletons that force it: **none at the code level** — the shared-singleton list above holds no code-level collision, so here serialize-verification is a genuine **policy choice**, not the hard constraint a real app's shared DB/build-cache would impose. Flip to `parallel-safe` by re-running `backlog setup` and choosing parallel; the tracker and review surface are handled by serialization of their own writes, not of code verification.
- Serialized exception lane: **n/a** — already fully serialized.
