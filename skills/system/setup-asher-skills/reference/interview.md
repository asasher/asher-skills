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
- the deterministic dependency-first install/setup order compiled from the selected roots, including optional
  siblings that are already installed or explicitly selected;
- a draft of the `## Agent skills` block that will go into `AGENTS.md`/`CLAUDE.md`;
- the `docs/agents/` playbooks that will be guaranteed (named, with which skill's setup writes each);
- the repo pointer.

Nothing touches disk until the user approves this. This is the single write gate.

Completion criterion: the user has approved the resolved plan (as-is or after edits).

## Phase 4 — Write

Execute the approved plan:

1. **Compile, then install from this repo only.** Resolve the selected roots from the bundled generated
   catalog, fail before writes on a missing required sibling or required cycle, and install in deterministic
   dependency-first order. An optional sibling joins only when already installed or explicitly selected.
   First establish whether this is the **self-host case** using the canonical "repo is the source" detection
   in [audit-mode](audit-mode.md) step 1 (the repo's git remote is `asasher/asher-skills`, or a local
   `skills/` dir holds these skills). This is one shared notion consumed by the READ path (audit's catalog
   choice) and this WRITE path (Phase 4's install guard), so the two cannot diverge.

   In the self-host case, a repo-owned skill — one whose install source is its catalog-resolved
   `skills/<category>/<name>/` directory —
   **still gets mounted**: source presence is not an install. The harness loads installed skills from
   `.agents/skills/` / `.claude/skills/`, never from `skills/`, so a register-only write (block + pointer +
   playbooks with nothing mounted) leaves the closure non-functional. The **guard** constrains the mechanics
   of the mount, not whether to mount:

   - **Local source, not the endpoint.** Install repo-owned skills from the repo's own root as a local
     source — `npx skills add <repo-root> --skill <ordered names...> -y` — never from the
     `https://github.com/asasher/asher-skills` endpoint, which may lag the local branch (the same
     repo-is-the-source reasoning as audit's self-catalog choice).
   - **The source directory is never an install destination.** The mount lands as a **canonical copy** at
     `.agents/skills/<name>` plus a **per-harness symlink** `.claude/skills/<name> ->
     ../../.agents/skills/<name>`, with the tool's own `skills-lock.json` entry (`sourceType: "local"`,
     tool-computed `computedHash`). Verified on `skills` v1.5.15: the tool creates the symlink only when
     `.claude/skills/` already exists — when the project is worked from Claude Code, ensure that directory
     exists before installing, or add the symlink afterwards.
   - **The mount is a build product, the copy is deliberate.** The canonical mount is a real directory copy
     (identical twins with the catalog-resolved source), not a symlink into `skills/` — the same shape every consumer
     project gets. The drift this invites is handled by discipline, not linkage: never edit
     `.agents/skills/<name>` in place; edit the catalog-resolved source and refresh by re-running the same local-source
     install (the repo's `AGENTS.md` § Vocabulary records this under *Installed skill*).

   Still write the `## Agent skills` block, the repo pointer, and the guaranteed playbooks, exactly as for any
   other install.

   For a non-self-host install, use
   `npx skills add https://github.com/asasher/asher-skills --skill <ordered names...> -y`
   — project-local by default (the tool's project install; `-y` skips the prompt the user already answered at
   phase 3), or `-g -y` for a consented global `staffing` install (`-g` is scope, `-y` still skips the prompt
   — they are orthogonal). Flags verified against `skills` v1.5.15 (`-s/--skill`, `-g/--global`,
   `-y/--yes`). Build `<ordered names...>` per scope from the union of that scope's already-installed public
   asher-skills and the compiled new closure, in deterministic dependency-first order. Run **one command per
   scope**: repeated single-skill calls can replace earlier selections from the same source. Every install
   command targets `asasher/asher-skills` and nothing else — see
   [catalog](catalog.md) § Pull only from this repo.

   After the batch, verify every named skill actually landed on the filesystem: check the project install
   dirs (`.claude/skills/<name>/` or `.agents/skills/<name>/`) and the `skills-lock.json` entries. Do not trust
   the exit code: `npx skills add` can print `✖ No matching skills found` and exit 0
   after installing nothing, and `-y` mode can under-report the count (it reported "Installed 3 skills" when
   4 were requested).

   On a verified miss, place only the missing skill's files directly instead of trusting the failed install. This is the
   **direct-placement fallback**: copy from this repo's catalog-resolved source in the self-host case, else fetch
   the skill from the `https://github.com/asasher/asher-skills` endpoint. It never breaks
   pull-only-from-this-repo, and it mirrors the mount shape the tool would have produced — a canonical copy at
   `.agents/skills/<name>` plus the per-harness symlink `.claude/skills/<name>` where that harness is present.

   A hand-placed `skills-lock.json` fallback entry has a **specified shape**: the tool's native fields —
   `source` (the repo root path in the self-host case, else the slug `asasher/asher-skills`),
   `sourceType` (`"local"` / `"github"`), and `skillPath` for github sources — plus exactly one extension
   field, `"fallbackOrigin": true`, and **no `computedHash`**. Never fabricate `computedHash` (it is not a
   plain sha256 of `SKILL.md`), and add no free-form fields (`note` and the like). The `skills` CLI does not
   know `fallbackOrigin`; if a later successful run rewrites the entry — dropping the marker, computing a real
   hash — the tool has simply adopted the skill, which is the desired end state, not breakage. Tell the user
   the entry is fallback-origin; `audit-mode` treats such an entry (marked `fallbackOrigin`, or missing
   `computedHash`) as expected, not drift.
2. **Invoke owner setup branches dependency-first.** After installation, invoke `<skill> setup` by public
   skill name in the same dependency-first order. A skill without a declared setup branch is a valid no-op.
   Staffing preserves an existing global base and writes a missing one only with explicit consent; otherwise
   it reconciles the project delta. Review-loop reconciles only its presentation-surface section. Backlog
   writes its own playbook suite. **setup-asher-skills never reads, copies, or interprets another skill's
   setup reference.**

   Before each invocation, atomically record the owner and status in
   `.agents/setup-asher-skills/setup-state.json`; after success, record the owned writes. A failure stops every
   dependent, reports the public owner and partial write set, and leaves completed dependencies intact. A
   retry recompiles the same graph and re-invokes idempotently from the failed owner.
3. **Write the `## Agent skills` block.** From `templates/agent-skills-block.md`, write the per-project skill
   map into the harness instruction layout. When neither instruction file exists, create canonical
   `AGENTS.md`; when Claude Code will work in the project, also create a minimal `CLAUDE.md` beginning with
   `@AGENTS.md`. When either file already exists, preserve that deliberate layout and reconcile its map or
   import instead of replacing it. The block lists each
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
