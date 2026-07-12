# Codex probe evidence

Executor `gpt-5.6-sol` via `codex exec -s read-only`, running probes P12 and P13 against `skills/setup-asher-skills` at commit `3f6373d`, graded against `evals/answer-key.md`. This is the graded rerun after an earlier attempt stalled.

Reading additional input from stdin...
2026-07-11T21:20:45.996733Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when Client(HttpRequest(HttpRequest("http/request failed: error sending request for url (http://127.0.0.1:29979/mcp)")))
OpenAI Codex v0.144.1
--------
workdir: /Users/asher/Projects/asher-skills
model: gpt-5.6-sol
provider: openai
approval: on-request
sandbox: read-only
reasoning effort: high
reasoning summaries: none
session id: 019f530d-de9c-76d0-b6d8-3fe8860bf25c
--------
user
You are executing the setup-asher-skills skill. Its files are at /Users/asher/Projects/asher-skills/skills/setup-asher-skills/ — read SKILL.md and reference/ as needed, but do NOT open anything under evals/. Answer the situated question with your concrete next actions. Cite the file and exact sentence that decided each choice. If anything is under-specified, flag the ambiguity explicitly.

Answer the following two probes SEPARATELY (P12 first, then P13).

P12 — self-host write guard. "You're invoked with `setup` on the `asasher/asher-skills` repo itself (git remote is `asasher/asher-skills`; the closure you're installing — `backlog`, `plan`, `review-loop`, `staffing`, `prototype` — has its sources in the repo's own `skills/`). You've reached Phase 4 (Write); the user approved the plan. Which install commands do you emit for those repo-owned skills, how does each one end up loadable by the harness (name the paths that exist afterwards), and what do you still write to the repo? Cite the file and sentence."

P13 — silent install miss. "In Phase 4 you run `npx skills add https://github.com/asasher/asher-skills --skill plan -y`. It prints `✖ No matching skills found for: plan` and exits 0. How do you determine whether `plan` actually installed, and what do you do if it did not? Cite the file and sentence."
2026-07-11T21:20:46.248840Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when Client(HttpRequest(HttpRequest("http/request failed: error sending request for url (http://127.0.0.1:29979/mcp)")))
2026-07-11T21:20:47.251635Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when Client(HttpRequest(HttpRequest("http/request failed: error sending request for url (http://127.0.0.1:29979/mcp)")))
2026-07-11T21:20:49.874304Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when Auth(AuthorizationRequired)
2026-07-11T21:20:49.996395Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when Auth(AuthorizationRequired)
codex
I’m using the requested `setup-asher-skills` skill and will inspect its instructions and references only, excluding `evals/`.
exec
/bin/zsh -lc "sed -n '1,240p' skills/setup-asher-skills/SKILL.md && find skills/setup-asher-skills/reference -type f -maxdepth 2 -print" in /Users/asher/Projects/asher-skills
 succeeded in 0ms:
---
name: setup-asher-skills
description: The prompt-driven installer for this skills repo. Use to set a project up with the right asher-skills, add a skill with its sibling closure, or audit an existing install for drift — an interview, one decision at a time, project-local by default, pulled only from this repo. Not for authoring skills or installing from anywhere else.
argument-hint: "[setup | audit]"
user-invocable: true
---

# setup-asher-skills

This skill owns one capability: take a project from *no asher-skills* (or a drifted install) to *the right
skills, dependency-complete, mapped, and pulled only from this repo* — through a prompt-driven interview, not
a script. It is modeled on `setup-matt-pocock-skills` (explore → present decisions one at a time with
explainers → confirm → write) and adapted as ours: it audits **three** surfaces, guarantees each skill's
sibling closure, and defaults every install to project-local.

It ships **no runtime** — no server, no installer binary. It drives the existing `npx skills` tooling, invokes
the `staffing` skill for the machine audit, and runs each installed skill's own setup.

## Command surface

- **`setup`** (default) — run the four phases below for a project. Load
  [interview](reference/interview.md) (the audit → decide → confirm → write contract) and
  [catalog](reference/catalog.md) (which skills fit which project, the sibling closure rules, and the
  this-repo-only invariant).
- **`audit`** — re-check an existing install: fetch this repo's current catalog, diff it against what's
  installed (project + global), and report overlap, drift, broken closures, and scope conflicts, proposing
  fixes one at a time. Load [audit-mode](reference/audit-mode.md).

Invoked with no argument, route on prior-install evidence, not the block alone. **Greenfield** — no
`## Agent skills` block and no installed asher-skills anywhere — runs `setup`. **Has block** — a
`## Agent skills` block — runs `audit`; **has skills, no block** — a `skills-lock.json` with asher-skills
entries, a skill under `.claude/skills/` or `.agents/skills/` traceable to this repo, or the repo itself being
`asasher/asher-skills` — also runs `audit`. There is no third mode: audit repairs that last case with a
**Missing map** finding whose proposed fix writes the block.

## The four phases (setup)

The full contract is in [interview](reference/interview.md); the sequence is **audit → interview → confirm →
write**, and nothing touches disk until the user approves the whole plan at confirm.

1. **Audit — three surfaces, silently.** Before recommending anything, audit **three things**: the **repo**
   (git remotes, `AGENTS.md`/`CLAUDE.md` and any existing `## Agent skills` block, skills installed both
   project and global — project `skills-lock.json`, `.claude/skills/`, `.agents/skills/`; global
   `~/.claude/skills/`, `~/.agents/skills/` — resolving symlinks before comparing, plus `docs/agents/`
   playbooks); the **machine** (the reachable models + whether the Codex CLI is present — done by invoking
   the **`staffing`** skill by name, not by re-deriving a roster); and the **user/project** (one question:
   *what is this project for?*).
2. **Interview — one decision at a time.** Recommend a skill set keyed to the project type, then walk the
   decisions **one at a time**, each with a **plain-language explainer** that assumes the user doesn't know
   the term. Accepting a composer **auto-pulls its sibling closure and says so** in plain language — never a
   silent, hidden pull. Scope is surfaced only where it matters: project-local by default, global offered only
   for `staffing`.
3. **Confirm — the whole write, before any write.** Show the resolved plan — skills and their scope, the
   `## Agent skills` block draft, the playbooks that will be guaranteed, the repo pointer — and let the user
   edit it. Nothing is written until this is approved.
4. **Write.** For each skill in the closure, `npx skills add https://github.com/asasher/asher-skills --skill
   <name> -y` (add `-g` for a consented global staffing install: `-g -y`; project-local is the default) —
   **only this repo**. In the self-host case, repo-owned skills are **still mounted**, from the repo's own
   root as a local source (`npx skills add <repo-root> --skill <name> -y`): a canonical copy lands at
   `.agents/skills/<name>` with a per-harness symlink at `.claude/skills/<name>`, refreshed by reinstall from
   `skills/` and never edited in place — `skills/<name>/` itself is never an install destination. After each
   command, verify the skill landed on the filesystem rather than trusting the exit code, and fall back to
   direct placement on a miss (lock entry in the specified fallback shape: native fields plus
   `"fallbackOrigin": true`, no fabricated `computedHash`). The `-y` skips the confirmation prompt since the
   user already confirmed at phase 3. Then run each installed skill's own setup (staffing's roster, review-loop's
   surface config, backlog's `docs/agents/` suite), write the `## Agent skills` block into the harness memory
   file, write the repo pointer, and — consent-gated, if absent — seed the **global conventions**
   (`templates/global-conventions.md`: local-first HTML presentation, tailnet up/down) into the harness's
   global memory file.

## How it composes

- **`staffing`** — the **machine audit** (phase 1) and every "which model does this?" question. setup invokes
  it by name for the reachable-models + Codex probe and for the consent-gated global roster write; it never
  re-derives a roster. Absent staffing, setup states the need rather than inventing one.
- **The installed skills own their own playbooks.** setup **guarantees** the `docs/agents/` playbooks by
  running each installed skill's setup — it authors only the cross-cutting artifacts no single skill owns (the
  `## Agent skills` map and the repo pointer) and **never re-copies another skill's templates.** This keeps
  composition by-name and prevents template drift.

## Dependency surface

Three kinds of dependency, per `AGENTS.md` § Conventions:

1. **Bundled references** — this skill's own contract under `reference/` ([interview](reference/interview.md),
   [catalog](reference/catalog.md), [audit-mode](reference/audit-mode.md)) plus the seed templates under
   `templates/` (`agent-skills-block.md`, `repo-pointer.md`, `global-conventions.md`). These carry the full
   contract so the skill runs standalone; they import no other skill's files.
2. **Project artifacts it writes** — the `## Agent skills` context block written into the target repo's
   `AGENTS.md`/`CLAUDE.md` (the per-project skill map — no separate `ask-asher` router), the repo pointer,
   and the consent-gated global `## Conventions` seed (local-first HTML presentation, tailnet up/down) in the
   harness's global memory file. The `docs/agents/` playbooks are **guaranteed, not authored here**: each
   installed skill's own setup writes them.
3. **Sibling skills it installs and guarantees** — every skill in this repo, pulled **only** from
   `https://github.com/asasher/asher-skills`. `staffing` is composed by name for the machine audit; the rest
   (`review-loop`, `plan`, `prototype`, `backlog`, `to-spec`, `to-tickets`, `maquette`, `to-sprites`, and the
   catalog skills) are installed per the interview, with their sibling closures guaranteed
   ([catalog](reference/catalog.md)).
skills/setup-asher-skills/reference/audit-mode.md
skills/setup-asher-skills/reference/interview.md
skills/setup-asher-skills/reference/catalog.md

exec
/bin/zsh -lc "sed -n '1,280p' skills/setup-asher-skills/reference/interview.md && sed -n '1,300p' skills/setup-asher-skills/reference/catalog.md" in /Users/asher/Projects/asher-skills
 succeeded in 0ms:
# The interview — audit, decide, confirm, write

The authoritative contract for a `setup` run. Adapted from `setup-matt-pocock-skills`: explore first, present
decisions one at a time with plain-language explainers, confirm the whole thing, then write. This file stands
alone — it imports no other skill's files and names the siblings it composes only by plain name.

The sequence is **audit → interview → confirm → write.** Nothing touches disk until the user approves the
whole plan at confirm.

## Phase 1 — Audit three surfaces (silently)

Before recommending anything, audit **three things** and hold the findings; ask the user nothing yet except
the single project question in (3).

1. **The repo.** Read: the git remotes (`git remote -v`) — this is also how you confirm the pull endpoint;
   `AGENTS.md` and `CLAUDE.md`, including any existing `## Agent skills` block; prior-install evidence, not
   the block alone, decides routing: greenfield (no block and no installed asher-skills) runs `setup`, while a
   block or installed asher-skills routes to `audit` — see [audit-mode](audit-mode.md). Read the skills
   already installed **both project and global** (project: `skills-lock.json`, `.claude/skills/`,
   `.agents/skills/`; global: `~/.claude/skills/`, `~/.agents/skills/`), resolving symlinks before comparing;
   and the `docs/agents/` playbooks present.
2. **The machine.** Determine the **reachable models** and whether the **Codex CLI** is installed — the
   staffing probe. **Do this by invoking the `staffing` skill by name**, not by re-deriving a roster:
   staffing owns the machine audit, the rankings seed, and the consent-gated global write. If `staffing`
   isn't reachable, state that the machine audit needs it rather than inventing a roster. Also check the
   harness's **global memory file** (`~/.claude/CLAUDE.md` or equivalent) for a `## Conventions` section —
   phase 4 seeds it when absent.
3. **The user/project.** Ask **one** question: *what is this project for?* — a shipping web product, a
   research effort, an ops/infra repo, a greenfield pitch, a content project, a library. The answer keys the
   recommendation in [catalog](catalog.md); everything else in this phase is read silently.

Completion criterion: you can name what's already installed, which models the machine can reach, and what the
project is for.

## Phase 2 — Interview, one decision at a time

Recommend a skill set keyed to the project type ([catalog](catalog.md) § By project type), then walk the
decisions. The rules:

- **One decision at a time.** Present a single skill (or a single tightly-bound group), get a yes/no, then
  move on. Never dump the whole catalog as a checklist.
- **Plain-language explainer, every time.** Each decision leads with one or two sentences that assume the
  user does not know the term — say what the skill *does for them*, not its name. ("`review-loop` shows you a
  plan or design in your browser and lets you approve it or leave comments — you'll want it if you want to
  sign off on work before an agent runs with it.")
- **Default to what fits; the user can decline.** Recommend, don't interrogate. State the recommendation and
  why it fits this project, and let the user say no.
- **Accepting a composer auto-pulls its sibling closure — and you say so.** When the user accepts a skill
  that depends on others, add the whole closure ([catalog](catalog.md) § The closure rules) and **tell the
  user in plain language which siblings came along and why** ("Adding `plan` also brings `review-loop`, which
  you'll use to approve the plan, and `staffing`, which picks which model writes it — they work together").
  Never pull a sibling silently and invisibly.
- **Scope is surfaced only where it matters.** Everything is **project-local by default**; the only skill
  offered a **global** install is `staffing`, because a model roster is genuinely reusable across every
  project. Offer staffing global with a one-sentence explainer and route the global write through staffing's
  own consent gate. Never offer any other skill global.

Completion criterion: a resolved set of skills, each with a scope, each sibling closure complete.

## Phase 3 — Confirm the whole write

Before writing anything, show the user the complete plan and let them edit it:

- the skills to install, with the auto-pulled siblings marked and each skill's scope (project / global);
- a draft of the `## Agent skills` block that will go into `AGENTS.md`/`CLAUDE.md`;
- the `docs/agents/` playbooks that will be guaranteed (named, with which skill's setup writes each);
- the repo pointer.

Nothing touches disk until the user approves this. This is the single write gate.

Completion criterion: the user has approved the resolved plan (as-is or after edits).

## Phase 4 — Write

Execute the approved plan:

1. **Install, from this repo only.** For each skill in the closure:
   first establish whether this is the **self-host case** using the canonical "repo is the source" detection
   in [audit-mode](audit-mode.md) step 1 (the repo's git remote is `asasher/asher-skills`, or a local
   `skills/` dir holds these skills). This is one shared notion consumed by the READ path (audit's catalog
   choice) and this WRITE path (Phase 4's install guard), so the two cannot diverge.

   In the self-host case, a repo-owned skill — one whose install source is this repo's own `skills/<name>/` —
   **still gets mounted**: source presence is not an install. The harness loads installed skills from
   `.agents/skills/` / `.claude/skills/`, never from `skills/`, so a register-only write (block + pointer +
   playbooks with nothing mounted) leaves the closure non-functional. The **guard** constrains the mechanics
   of the mount, not whether to mount:

   - **Local source, not the endpoint.** Install repo-owned skills from the repo's own root as a local
     source — `npx skills add <repo-root> --skill <name> -y` — never from the
     `https://github.com/asasher/asher-skills` endpoint, which may lag the local branch (the same
     repo-is-the-source reasoning as audit's self-catalog choice).
   - **`skills/<name>/` is never an install destination.** The mount lands as a **canonical copy** at
     `.agents/skills/<name>` plus a **per-harness symlink** `.claude/skills/<name> ->
     ../../.agents/skills/<name>`, with the tool's own `skills-lock.json` entry (`sourceType: "local"`,
     tool-computed `computedHash`). Verified on `skills` v1.5.15: the tool creates the symlink only when
     `.claude/skills/` already exists — when the project is worked from Claude Code, ensure that directory
     exists before installing, or add the symlink afterwards.
   - **The mount is a build product, the copy is deliberate.** The canonical mount is a real directory copy
     (identical twins with `skills/<name>/`), not a symlink into `skills/` — the same shape every consumer
     project gets. The drift this invites is handled by discipline, not linkage: never edit
     `.agents/skills/<name>` in place; edit `skills/<name>/` and refresh by re-running the same local-source
     install (the repo's `AGENTS.md` § Vocabulary records this under *Installed skill*).

   Still write the `## Agent skills` block, the repo pointer, and the guaranteed playbooks, exactly as for any
   other install.

   For every skill not under the self-host guard, run
   `npx skills add https://github.com/asasher/asher-skills --skill <name> -y`
   — project-local by default (the tool's project install; `-y` skips the prompt the user already answered at
   phase 3), or `-g -y` for a consented global `staffing` install (`-g` is scope, `-y` still skips the prompt
   — they are orthogonal). Flags verified against `skills` v1.5.15 (`-s/--skill`, `-g/--global`,
   `-y/--yes`). **Every install command targets `asasher/asher-skills` and nothing else** — see
   [catalog](catalog.md) § Pull only from this repo.

   After each `npx skills add`, verify `<name>` actually landed on the filesystem: check the project install
   dir (`.claude/skills/<name>/` or `.agents/skills/<name>/`) and/or the `skills-lock.json` entry for
   `<name>`. Do not trust the exit code: `npx skills add` can print `✖ No matching skills found` and exit 0
   after installing nothing, and `-y` mode can under-report the count (it reported "Installed 3 skills" when
   4 were requested).

   On a verified miss, place the skill's files directly instead of trusting the failed install. This is the
   **direct-placement fallback**: copy from this repo's own `skills/<name>/` in the self-host case, else fetch
   the skill from the `https://github.com/asasher/asher-skills` endpoint. It never breaks
   pull-only-from-this-repo, and it mirrors the mount shape the tool would have produced — a canonical copy at
   `.agents/skills/<name>` plus the per-harness symlink `.claude/skills/<name>` where that harness is present.

   A hand-placed `skills-lock.json` fallback entry has a **specified shape**: the tool's native fields —
   `source` (the repo root path in the self-host case, else `https://github.com/asasher/asher-skills`),
   `sourceType` (`"local"` / `"github"`), and `skillPath` for github sources — plus exactly one extension
   field, `"fallbackOrigin": true`, and **no `computedHash`**. Never fabricate `computedHash` (it is not a
   plain sha256 of `SKILL.md`), and add no free-form fields (`note` and the like). The `skills` CLI does not
   know `fallbackOrigin`; if a later successful run rewrites the entry — dropping the marker, computing a real
   hash — the tool has simply adopted the skill, which is the desired end state, not breakage. Tell the user
   the entry is fallback-origin; `audit-mode` treats such an entry (marked `fallbackOrigin`, or missing
   `computedHash`) as expected, not drift.
2. **Guarantee the playbooks by delegation.** Run each installed skill's own setup so its `docs/agents/`
   playbooks land: `staffing` writes the roster (global base + project delta, with consent); `review-loop`
   (or `backlog setup`, which composes it) writes the presentation surface config; `backlog setup` writes its
   `docs/agents/` suite. **setup does not re-copy any skill's templates.**
3. **Write the `## Agent skills` block.** From `templates/agent-skills-block.md`, write the per-project skill
   map into the harness memory file — **prefer `AGENTS.md` if it exists, else `CLAUDE.md`.** It lists each
   installed skill with a one-line plain-language purpose, notes the sibling relationships, and links the repo
   pointer. **There is no separate `ask-asher` router skill** — this block is the map.
   **Guarantee the import when the block lands in `AGENTS.md`:** Claude Code never reads `AGENTS.md` on its
   own — only `CLAUDE.md` (per the official memory docs; `@`-imports inline at session start). When the
   target repo will also be worked from Claude Code, ensure its `CLAUDE.md` begins with an `@AGENTS.md`
   import (create a minimal `CLAUDE.md` holding just the import if none exists); without it the map is
   invisible to that harness. A prose "read AGENTS.md first" line is not equivalent — it depends on the
   model obeying and costs a read every session.
4. **Write the repo pointer.** From `templates/repo-pointer.md`, record that these skills come from
   `https://github.com/asasher/asher-skills` and that updates/reconciliation run by re-invoking this skill.
5. **Seed the global conventions (consent-gated).** If phase 1 found no `## Conventions` section in the
   harness's global memory file, offer to seed it from `templates/global-conventions.md` — the local-first
   HTML presentation rule (author locally, open locally or over tailnet; cloud artifacts only on explicit
   request) and the machine's tailnet up/down commands (fill the placeholder during the interview). Like
   staffing's global write, this touches home-directory memory: write it **only with explicit consent**, and
   only the sections not already present. Projects override via their `docs/agents/` playbooks.

Completion criterion: the closure is installed from this repo, each skill's playbooks are present, the
`## Agent skills` block + pointer are written, and the global conventions are seeded or explicitly declined.

## What this skill does not do

- **Author or edit any installed skill.** setup composes the skills as they are; changing one is that skill's
  own concern.
- **Install anything from outside this repo.** External good ideas are already adapted and shipped here — see
  [catalog](catalog.md) § Pull only from this repo.
- **Write a `docs/agents/` playbook itself.** It guarantees them via each skill's setup (phase 4 step 2).
- **Ship an `ask-asher` router.** The `## Agent skills` block is the per-project map.
# The catalog — what to install, and the rules that bind it

Which skills fit which project, the sibling closure rules setup guarantees, and the hard invariant that every
install comes from this repo only. This file stands alone and names siblings by plain name.

## Pull only from this repo

**Every skill setup installs comes from `https://github.com/asasher/asher-skills` — the slug `asasher/asher-skills`
— and nothing else.** Every `npx skills add` command this skill emits targets that endpoint — or, in the
self-host case ([interview](interview.md) Phase 4), the same repo's own root as a local source: the identical
source at a local address. setup **never installs, recommends, or emits an install command for a skill from
any other host or account** (not `mattpocock/*`, not any vendor repo, not a gist).

The reason is a design stance, not a limitation: good ideas from elsewhere are **brought in, adapted, and
shipped here as our own** (for example `to-spec` is our adaptation of Matt Pocock's `to-prd`). So when a user
asks for an external skill by name — "install the TDD skill" — the move is: **offer our adapted equivalent if
we ship one, or say plainly that we don't ship it. Never reach out to the external repo.** If we have no
equivalent, that is an honest answer, not a reason to break the invariant.

## By project type — the recommendation seed

Recommend from this map, then confirm each choice one decision at a time ([interview](interview.md) § Phase 2).
The map is a starting point tuned by the project answer, not a fixed bundle.

| Project is for… | Recommend | Why |
|---|---|---|
| A shipping product / app repo, ongoing work | `backlog` (pulls its full closure) | The issue→reviewed-PR loop; brings plan, prototype, review-loop, staffing |
| A one-off feature or decision that needs sign-off | `plan` (pulls review-loop + staffing + prototype) | Reviewed plan with an approval gate, no full backlog machinery |
| A design/state question that needs to be tried | `prototype` (pulls review-loop + staffing) | Throwaway artifact that settles one question |
| A greenfield product to pitch/sell | `maquette` (pulls review-loop) | High-fidelity clickable prototype for a demo |
| Turning a decided conversation into a written spec | `to-spec` (review-loop optional) | Synthesize a spec; feeds `to-tickets` |
| Splitting a spec/plan into backlog tickets | `to-tickets` | Vertical-slice tickets with blocking edges into backlog's convention |
| Any project that will route work across models | `staffing` — offer **global** | A reusable model roster; the one skill worth installing once for every project |
| Game/asset work with sprite sheets | `to-sprites` (+ `codex-imagegen` for `--generate`) | Extract/generate sprite assets |

The single-purpose catalog skills (`bayes`, `constraints`, `dissolve`, `eloquent`, `fair-deal`, `goodwork`,
`learn-anything`, `smallbets`, `teamdrive`, `watch-video`, `shadixfy`, `bare-minimum-ux`, `skill-loop`) are
offered only when the project answer clearly calls for one; they carry no sibling closure. `fair-deal` installs
inside a deal project and is **never** global.

## The closure rules

Accepting a composer installs its **transitive sibling closure** — setup computes it at accept time and never
ships a half-wired composer. Two roots depend on nothing; everything closes over them.

- **Roots (depend on nothing):** `staffing`, `review-loop`.
- **`plan` ⇒ ensure `review-loop` + `staffing` + `prototype`.** (plan renders the artifact, review-loop signs
  it off, staffing picks who authors/builds, prototype settles logic/UI design questions — a soft edge, but
  installed with plan so gate 2 works out of the box.)
- **`prototype` ⇒ ensure `review-loop` + `staffing`.** (the two roots.)
- **`maquette` ⇒ ensure `review-loop`.** (maquette signs off its brief and journeys; it does not compose
  staffing.)
- **`backlog` ⇒ ensure ALL of `staffing`, `review-loop`, `plan`, `prototype`.** The transitive closure adds
  nothing beyond those four (plan pulls prototype and the two roots; prototype pulls only the roots).
- **Soft edges, noted not force-installed:** `to-tickets` reads backlog's `backlog-policy.md`/`platform.md`
  conventions but does not require the whole skill; `to-sprites` uses `codex-imagegen` only for `--generate`.
  Mention these; install them only if the user wants that path.

When a closure adds a sibling, **tell the user which siblings came along and why** — the pull is never silent
([interview](interview.md) § Phase 2).

## Scope — project-first

- **Project-local by default.** Every skill installs into the project unless it is `staffing`. Project installs
  never touch the user's home directory.
- **Global only for `staffing`, only with consent.** A model roster is the one genuinely cross-project thing,
  so `staffing` is the only skill offered a global install, routed through staffing's own consent gate. No
  other skill is offered global (and `fair-deal` is explicitly never global).

codex
The decisive distinction is clear: P12 is a self-host mount from the local repo root, while P13 requires post-command filesystem verification because exit status is explicitly non-authoritative. I’m collecting exact line locations for each cited sentence.
exec
/bin/zsh -lc "nl -ba skills/setup-asher-skills/reference/interview.md | sed -n '65,155p'; nl -ba skills/setup-asher-skills/SKILL.md | sed -n '48,82p'" in /Users/asher/Projects/asher-skills
 succeeded in 0ms:
    65	- a draft of the `## Agent skills` block that will go into `AGENTS.md`/`CLAUDE.md`;
    66	- the `docs/agents/` playbooks that will be guaranteed (named, with which skill's setup writes each);
    67	- the repo pointer.
    68	
    69	Nothing touches disk until the user approves this. This is the single write gate.
    70	
    71	Completion criterion: the user has approved the resolved plan (as-is or after edits).
    72	
    73	## Phase 4 — Write
    74	
    75	Execute the approved plan:
    76	
    77	1. **Install, from this repo only.** For each skill in the closure:
    78	   first establish whether this is the **self-host case** using the canonical "repo is the source" detection
    79	   in [audit-mode](audit-mode.md) step 1 (the repo's git remote is `asasher/asher-skills`, or a local
    80	   `skills/` dir holds these skills). This is one shared notion consumed by the READ path (audit's catalog
    81	   choice) and this WRITE path (Phase 4's install guard), so the two cannot diverge.
    82	
    83	   In the self-host case, a repo-owned skill — one whose install source is this repo's own `skills/<name>/` —
    84	   **still gets mounted**: source presence is not an install. The harness loads installed skills from
    85	   `.agents/skills/` / `.claude/skills/`, never from `skills/`, so a register-only write (block + pointer +
    86	   playbooks with nothing mounted) leaves the closure non-functional. The **guard** constrains the mechanics
    87	   of the mount, not whether to mount:
    88	
    89	   - **Local source, not the endpoint.** Install repo-owned skills from the repo's own root as a local
    90	     source — `npx skills add <repo-root> --skill <name> -y` — never from the
    91	     `https://github.com/asasher/asher-skills` endpoint, which may lag the local branch (the same
    92	     repo-is-the-source reasoning as audit's self-catalog choice).
    93	   - **`skills/<name>/` is never an install destination.** The mount lands as a **canonical copy** at
    94	     `.agents/skills/<name>` plus a **per-harness symlink** `.claude/skills/<name> ->
    95	     ../../.agents/skills/<name>`, with the tool's own `skills-lock.json` entry (`sourceType: "local"`,
    96	     tool-computed `computedHash`). Verified on `skills` v1.5.15: the tool creates the symlink only when
    97	     `.claude/skills/` already exists — when the project is worked from Claude Code, ensure that directory
    98	     exists before installing, or add the symlink afterwards.
    99	   - **The mount is a build product, the copy is deliberate.** The canonical mount is a real directory copy
   100	     (identical twins with `skills/<name>/`), not a symlink into `skills/` — the same shape every consumer
   101	     project gets. The drift this invites is handled by discipline, not linkage: never edit
   102	     `.agents/skills/<name>` in place; edit `skills/<name>/` and refresh by re-running the same local-source
   103	     install (the repo's `AGENTS.md` § Vocabulary records this under *Installed skill*).
   104	
   105	   Still write the `## Agent skills` block, the repo pointer, and the guaranteed playbooks, exactly as for any
   106	   other install.
   107	
   108	   For every skill not under the self-host guard, run
   109	   `npx skills add https://github.com/asasher/asher-skills --skill <name> -y`
   110	   — project-local by default (the tool's project install; `-y` skips the prompt the user already answered at
   111	   phase 3), or `-g -y` for a consented global `staffing` install (`-g` is scope, `-y` still skips the prompt
   112	   — they are orthogonal). Flags verified against `skills` v1.5.15 (`-s/--skill`, `-g/--global`,
   113	   `-y/--yes`). **Every install command targets `asasher/asher-skills` and nothing else** — see
   114	   [catalog](catalog.md) § Pull only from this repo.
   115	
   116	   After each `npx skills add`, verify `<name>` actually landed on the filesystem: check the project install
   117	   dir (`.claude/skills/<name>/` or `.agents/skills/<name>/`) and/or the `skills-lock.json` entry for
   118	   `<name>`. Do not trust the exit code: `npx skills add` can print `✖ No matching skills found` and exit 0
   119	   after installing nothing, and `-y` mode can under-report the count (it reported "Installed 3 skills" when
   120	   4 were requested).
   121	
   122	   On a verified miss, place the skill's files directly instead of trusting the failed install. This is the
   123	   **direct-placement fallback**: copy from this repo's own `skills/<name>/` in the self-host case, else fetch
   124	   the skill from the `https://github.com/asasher/asher-skills` endpoint. It never breaks
   125	   pull-only-from-this-repo, and it mirrors the mount shape the tool would have produced — a canonical copy at
   126	   `.agents/skills/<name>` plus the per-harness symlink `.claude/skills/<name>` where that harness is present.
   127	
   128	   A hand-placed `skills-lock.json` fallback entry has a **specified shape**: the tool's native fields —
   129	   `source` (the repo root path in the self-host case, else `https://github.com/asasher/asher-skills`),
   130	   `sourceType` (`"local"` / `"github"`), and `skillPath` for github sources — plus exactly one extension
   131	   field, `"fallbackOrigin": true`, and **no `computedHash`**. Never fabricate `computedHash` (it is not a
   132	   plain sha256 of `SKILL.md`), and add no free-form fields (`note` and the like). The `skills` CLI does not
   133	   know `fallbackOrigin`; if a later successful run rewrites the entry — dropping the marker, computing a real
   134	   hash — the tool has simply adopted the skill, which is the desired end state, not breakage. Tell the user
   135	   the entry is fallback-origin; `audit-mode` treats such an entry (marked `fallbackOrigin`, or missing
   136	   `computedHash`) as expected, not drift.
   137	2. **Guarantee the playbooks by delegation.** Run each installed skill's own setup so its `docs/agents/`
   138	   playbooks land: `staffing` writes the roster (global base + project delta, with consent); `review-loop`
   139	   (or `backlog setup`, which composes it) writes the presentation surface config; `backlog setup` writes its
   140	   `docs/agents/` suite. **setup does not re-copy any skill's templates.**
   141	3. **Write the `## Agent skills` block.** From `templates/agent-skills-block.md`, write the per-project skill
   142	   map into the harness memory file — **prefer `AGENTS.md` if it exists, else `CLAUDE.md`.** It lists each
   143	   installed skill with a one-line plain-language purpose, notes the sibling relationships, and links the repo
   144	   pointer. **There is no separate `ask-asher` router skill** — this block is the map.
   145	   **Guarantee the import when the block lands in `AGENTS.md`:** Claude Code never reads `AGENTS.md` on its
   146	   own — only `CLAUDE.md` (per the official memory docs; `@`-imports inline at session start). When the
   147	   target repo will also be worked from Claude Code, ensure its `CLAUDE.md` begins with an `@AGENTS.md`
   148	   import (create a minimal `CLAUDE.md` holding just the import if none exists); without it the map is
   149	   invisible to that harness. A prose "read AGENTS.md first" line is not equivalent — it depends on the
   150	   model obeying and costs a read every session.
   151	4. **Write the repo pointer.** From `templates/repo-pointer.md`, record that these skills come from
   152	   `https://github.com/asasher/asher-skills` and that updates/reconciliation run by re-invoking this skill.
   153	5. **Seed the global conventions (consent-gated).** If phase 1 found no `## Conventions` section in the
   154	   harness's global memory file, offer to seed it from `templates/global-conventions.md` — the local-first
   155	   HTML presentation rule (author locally, open locally or over tailnet; cloud artifacts only on explicit
    48	2. **Interview — one decision at a time.** Recommend a skill set keyed to the project type, then walk the
    49	   decisions **one at a time**, each with a **plain-language explainer** that assumes the user doesn't know
    50	   the term. Accepting a composer **auto-pulls its sibling closure and says so** in plain language — never a
    51	   silent, hidden pull. Scope is surfaced only where it matters: project-local by default, global offered only
    52	   for `staffing`.
    53	3. **Confirm — the whole write, before any write.** Show the resolved plan — skills and their scope, the
    54	   `## Agent skills` block draft, the playbooks that will be guaranteed, the repo pointer — and let the user
    55	   edit it. Nothing is written until this is approved.
    56	4. **Write.** For each skill in the closure, `npx skills add https://github.com/asasher/asher-skills --skill
    57	   <name> -y` (add `-g` for a consented global staffing install: `-g -y`; project-local is the default) —
    58	   **only this repo**. In the self-host case, repo-owned skills are **still mounted**, from the repo's own
    59	   root as a local source (`npx skills add <repo-root> --skill <name> -y`): a canonical copy lands at
    60	   `.agents/skills/<name>` with a per-harness symlink at `.claude/skills/<name>`, refreshed by reinstall from
    61	   `skills/` and never edited in place — `skills/<name>/` itself is never an install destination. After each
    62	   command, verify the skill landed on the filesystem rather than trusting the exit code, and fall back to
    63	   direct placement on a miss (lock entry in the specified fallback shape: native fields plus
    64	   `"fallbackOrigin": true`, no fabricated `computedHash`). The `-y` skips the confirmation prompt since the
    65	   user already confirmed at phase 3. Then run each installed skill's own setup (staffing's roster, review-loop's
    66	   surface config, backlog's `docs/agents/` suite), write the `## Agent skills` block into the harness memory
    67	   file, write the repo pointer, and — consent-gated, if absent — seed the **global conventions**
    68	   (`templates/global-conventions.md`: local-first HTML presentation, tailnet up/down) into the harness's
    69	   global memory file.
    70	
    71	## How it composes
    72	
    73	- **`staffing`** — the **machine audit** (phase 1) and every "which model does this?" question. setup invokes
    74	  it by name for the reachable-models + Codex probe and for the consent-gated global roster write; it never
    75	  re-derives a roster. Absent staffing, setup states the need rather than inventing one.
    76	- **The installed skills own their own playbooks.** setup **guarantees** the `docs/agents/` playbooks by
    77	  running each installed skill's setup — it authors only the cross-cutting artifacts no single skill owns (the
    78	  `## Agent skills` map and the repo pointer) and **never re-copies another skill's templates.** This keeps
    79	  composition by-name and prevents template drift.
    80	
    81	## Dependency surface
    82	

codex
## P12 — self-host write guard

Assuming the approved plan kept all five skills project-local, I emit:

```sh
npx skills add /Users/asher/Projects/asher-skills --skill backlog -y
npx skills add /Users/asher/Projects/asher-skills --skill plan -y
npx skills add /Users/asher/Projects/asher-skills --skill review-loop -y
npx skills add /Users/asher/Projects/asher-skills --skill staffing -y
npx skills add /Users/asher/Projects/asher-skills --skill prototype -y
```

Decision sentence: “Install repo-owned skills from the repo's own root as a local source — `npx skills add <repo-root> --skill <name> -y` — never from the `https://github.com/asasher/asher-skills` endpoint…” ([interview.md:89](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:89)).

Afterward, each skill is loadable through:

- Canonical copies:
  - `.agents/skills/backlog`
  - `.agents/skills/plan`
  - `.agents/skills/review-loop`
  - `.agents/skills/staffing`
  - `.agents/skills/prototype`
- Claude harness symlinks:
  - `.claude/skills/backlog -> ../../.agents/skills/backlog`
  - `.claude/skills/plan -> ../../.agents/skills/plan`
  - `.claude/skills/review-loop -> ../../.agents/skills/review-loop`
  - `.claude/skills/staffing -> ../../.agents/skills/staffing`
  - `.claude/skills/prototype -> ../../.agents/skills/prototype`
- `skills-lock.json` gains local-source entries with tool-computed hashes.

Decision sentence: “The mount lands as a canonical copy at `.agents/skills/<name>` plus a per-harness symlink `.claude/skills/<name> -> ../../.agents/skills/<name>`, with the tool's own `skills-lock.json` entry (`sourceType: "local"`, tool-computed `computedHash`).” ([interview.md:93](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:93)).

Because this repo uses Claude Code, I ensure `.claude/skills/` exists before installing or create the missing symlinks afterward. Decision sentence: “Verified on `skills` v1.5.15: the tool creates the symlink only when `.claude/skills/` already exists — when the project is worked from Claude Code, ensure that directory exists before installing, or add the symlink afterwards.” ([interview.md:96](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:96)).

I do not install into or modify `skills/<name>/`; those remain the sources. Decision sentence: “The canonical mount is a real directory copy … not a symlink into `skills/`…” ([interview.md:99](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:99)).

I still write or guarantee in the repo:

- The `## Agent skills` map in `AGENTS.md`.
- The repo pointer.
- The required `docs/agents/` playbooks, by running the installed skills’ setups—not by copying their templates.
- The `@AGENTS.md` import in `CLAUDE.md` if it is not already present.

The direct governing sentence is: “Still write the `## Agent skills` block, the repo pointer, and the guaranteed playbooks, exactly as for any other install.” ([interview.md:105](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:105)). Playbook ownership is decided by: “Run each installed skill's own setup so its `docs/agents/` playbooks land…” ([interview.md:137](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:137)).

Ambiguity: the probe does not state whether Phase 3 approved `staffing` as global. Project-local is the documented default. If global staffing was explicitly approved, its command instead includes `-g -y`, and its mount is global rather than the project-local paths above. The deciding sentence is: “Everything is project-local by default; the only skill offered a global install is `staffing`…” ([SKILL.md:51](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/SKILL.md:51)).

## P13 — silent install miss

I do not use exit status as evidence. I inspect:

1. `.agents/skills/plan/`
2. `.claude/skills/plan/`, resolving the symlink if present
3. The `plan` entry in `skills-lock.json`

The decisive sentence is: “After each `npx skills add`, verify `<name>` actually landed on the filesystem: check the project install dir (`.claude/skills/<name>/` or `.agents/skills/<name>/`) and/or the `skills-lock.json` entry for `<name>`.” ([interview.md:116](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:116)). The warning exactly covers this result: “Do not trust the exit code: `npx skills add` can print `✖ No matching skills found` and exit 0 after installing nothing…” ([interview.md:118](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:118)).

If `plan` did not land, I use direct placement:

- Fetch `plan` only from `https://github.com/asasher/asher-skills`.
- Copy it to `.agents/skills/plan`.
- Create `.claude/skills/plan -> ../../.agents/skills/plan` where Claude is present.
- Add a fallback-origin lock entry containing:
  - `"source": "https://github.com/asasher/asher-skills"`
  - `"sourceType": "github"`
  - the appropriate `"skillPath"`
  - `"fallbackOrigin": true`
  - no `computedHash` or informal fields such as `note`
- Tell the user that the entry is fallback-origin.

Fallback decision sentence: “On a verified miss, place the skill's files directly instead of trusting the failed install.” ([interview.md:122](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:122)). Its required mount shape is specified in the same paragraph: “…a canonical copy at `.agents/skills/<name>` plus the per-harness symlink `.claude/skills/<name>` where that harness is present.” ([interview.md:125](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:125)).

The lock-entry choice is decided by: “A hand-placed `skills-lock.json` fallback entry has a specified shape: the tool's native fields — `source` … `sourceType` … and `skillPath` for github sources — plus exactly one extension field, `"fallbackOrigin": true`, and no `computedHash`.” ([interview.md:128](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:128)).
tokens used
24,216
## P12 — self-host write guard

Assuming the approved plan kept all five skills project-local, I emit:

```sh
npx skills add /Users/asher/Projects/asher-skills --skill backlog -y
npx skills add /Users/asher/Projects/asher-skills --skill plan -y
npx skills add /Users/asher/Projects/asher-skills --skill review-loop -y
npx skills add /Users/asher/Projects/asher-skills --skill staffing -y
npx skills add /Users/asher/Projects/asher-skills --skill prototype -y
```

Decision sentence: “Install repo-owned skills from the repo's own root as a local source — `npx skills add <repo-root> --skill <name> -y` — never from the `https://github.com/asasher/asher-skills` endpoint…” ([interview.md:89](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:89)).

Afterward, each skill is loadable through:

- Canonical copies:
  - `.agents/skills/backlog`
  - `.agents/skills/plan`
  - `.agents/skills/review-loop`
  - `.agents/skills/staffing`
  - `.agents/skills/prototype`
- Claude harness symlinks:
  - `.claude/skills/backlog -> ../../.agents/skills/backlog`
  - `.claude/skills/plan -> ../../.agents/skills/plan`
  - `.claude/skills/review-loop -> ../../.agents/skills/review-loop`
  - `.claude/skills/staffing -> ../../.agents/skills/staffing`
  - `.claude/skills/prototype -> ../../.agents/skills/prototype`
- `skills-lock.json` gains local-source entries with tool-computed hashes.

Decision sentence: “The mount lands as a canonical copy at `.agents/skills/<name>` plus a per-harness symlink `.claude/skills/<name> -> ../../.agents/skills/<name>`, with the tool's own `skills-lock.json` entry (`sourceType: "local"`, tool-computed `computedHash`).” ([interview.md:93](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:93)).

Because this repo uses Claude Code, I ensure `.claude/skills/` exists before installing or create the missing symlinks afterward. Decision sentence: “Verified on `skills` v1.5.15: the tool creates the symlink only when `.claude/skills/` already exists — when the project is worked from Claude Code, ensure that directory exists before installing, or add the symlink afterwards.” ([interview.md:96](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:96)).

I do not install into or modify `skills/<name>/`; those remain the sources. Decision sentence: “The canonical mount is a real directory copy … not a symlink into `skills/`…” ([interview.md:99](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:99)).

I still write or guarantee in the repo:

- The `## Agent skills` map in `AGENTS.md`.
- The repo pointer.
- The required `docs/agents/` playbooks, by running the installed skills’ setups—not by copying their templates.
- The `@AGENTS.md` import in `CLAUDE.md` if it is not already present.

The direct governing sentence is: “Still write the `## Agent skills` block, the repo pointer, and the guaranteed playbooks, exactly as for any other install.” ([interview.md:105](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:105)). Playbook ownership is decided by: “Run each installed skill's own setup so its `docs/agents/` playbooks land…” ([interview.md:137](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:137)).

Ambiguity: the probe does not state whether Phase 3 approved `staffing` as global. Project-local is the documented default. If global staffing was explicitly approved, its command instead includes `-g -y`, and its mount is global rather than the project-local paths above. The deciding sentence is: “Everything is project-local by default; the only skill offered a global install is `staffing`…” ([SKILL.md:51](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/SKILL.md:51)).

## P13 — silent install miss

I do not use exit status as evidence. I inspect:

1. `.agents/skills/plan/`
2. `.claude/skills/plan/`, resolving the symlink if present
3. The `plan` entry in `skills-lock.json`

The decisive sentence is: “After each `npx skills add`, verify `<name>` actually landed on the filesystem: check the project install dir (`.claude/skills/<name>/` or `.agents/skills/<name>/`) and/or the `skills-lock.json` entry for `<name>`.” ([interview.md:116](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:116)). The warning exactly covers this result: “Do not trust the exit code: `npx skills add` can print `✖ No matching skills found` and exit 0 after installing nothing…” ([interview.md:118](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:118)).

If `plan` did not land, I use direct placement:

- Fetch `plan` only from `https://github.com/asasher/asher-skills`.
- Copy it to `.agents/skills/plan`.
- Create `.claude/skills/plan -> ../../.agents/skills/plan` where Claude is present.
- Add a fallback-origin lock entry containing:
  - `"source": "https://github.com/asasher/asher-skills"`
  - `"sourceType": "github"`
  - the appropriate `"skillPath"`
  - `"fallbackOrigin": true`
  - no `computedHash` or informal fields such as `note`
- Tell the user that the entry is fallback-origin.

Fallback decision sentence: “On a verified miss, place the skill's files directly instead of trusting the failed install.” ([interview.md:122](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:122)). Its required mount shape is specified in the same paragraph: “…a canonical copy at `.agents/skills/<name>` plus the per-harness symlink `.claude/skills/<name>` where that harness is present.” ([interview.md:125](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:125)).

The lock-entry choice is decided by: “A hand-placed `skills-lock.json` fallback entry has a specified shape: the tool's native fields — `source` … `sourceType` … and `skillPath` for github sources — plus exactly one extension field, `"fallbackOrigin": true`, and no `computedHash`.” ([interview.md:128](/Users/asher/Projects/asher-skills/skills/setup-asher-skills/reference/interview.md:128)).
