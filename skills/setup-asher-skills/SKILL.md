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
   **only this repo's endpoint**. In the self-host case, do not run `npx skills add` against this repo's own
   `skills/`; after each command, verify the skill landed on the filesystem rather than trusting the exit
   code, and fall back to self-host placement on a miss. The `-y` skips the confirmation prompt since the user
   already confirmed at phase 3. Then run each installed skill's own setup (staffing's roster, review-loop's
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
