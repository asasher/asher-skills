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
   isn't reachable, state that the machine audit needs it rather than inventing a roster.
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

   In the self-host case, check each skill before installing. If the skill is repo-owned — its install source
   would be this repo's own `skills/<name>/` — **guard**: do not run `npx skills add` for it. `skills/<name>/`
   is never an install target, and the skill is already present as source. Still write the `## Agent skills`
   block, the repo pointer, and the guaranteed playbooks.

   For every skill not guarded, run `npx skills add https://github.com/asasher/asher-skills --skill <name> -y`
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
   **self-host fallback**: use this repo's own `skills/<name>/` in the self-host case, else fetch the skill
   from the `https://github.com/asasher/asher-skills` endpoint. It never breaks pull-only-from-this-repo, and
   uses the same direct-placement mechanism as the self-host guard. If you hand-place a `skills-lock.json`
   fallback entry, do not fabricate `computedHash`: it is not a plain sha256 of `SKILL.md`, so mark the
   entry's fallback origin and tell the user this is a rough edge. `audit-mode` treats a fallback-origin entry
   as expected, not drift.
2. **Guarantee the playbooks by delegation.** Run each installed skill's own setup so its `docs/agents/`
   playbooks land: `staffing` writes the roster (global base + project delta, with consent); `review-loop`
   (or `backlog setup`, which composes it) writes the presentation surface config; `backlog setup` writes its
   `docs/agents/` suite. **setup does not re-copy any skill's templates.**
3. **Write the `## Agent skills` block.** From `templates/agent-skills-block.md`, write the per-project skill
   map into the harness memory file — **prefer `AGENTS.md` if it exists, else `CLAUDE.md`.** It lists each
   installed skill with a one-line plain-language purpose, notes the sibling relationships, and links the repo
   pointer. **There is no separate `ask-asher` router skill** — this block is the map.
4. **Write the repo pointer.** From `templates/repo-pointer.md`, record that these skills come from
   `https://github.com/asasher/asher-skills` and that updates/reconciliation run by re-invoking this skill.

Completion criterion: the closure is installed from this repo, each skill's playbooks are present, and the
`## Agent skills` block + pointer are written.

## What this skill does not do

- **Author or edit any installed skill.** setup composes the skills as they are; changing one is that skill's
  own concern.
- **Install anything from outside this repo.** External good ideas are already adapted and shipped here — see
  [catalog](catalog.md) § Pull only from this repo.
- **Write a `docs/agents/` playbook itself.** It guarantees them via each skill's setup (phase 4 step 2).
- **Ship an `ask-asher` router.** The `## Agent skills` block is the per-project map.
