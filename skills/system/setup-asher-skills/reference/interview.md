# The interview — audit, decide, confirm, write

The authoritative contract for a `setup` run.

The sequence is **audit → interview → confirm → write.**

## Phase 1 — Audit three surfaces (silently)

Before recommending anything, audit **three things** and hold the findings; ask the user nothing yet except
the single project question in (3).

1. **The repo.** Read: the git remotes (`git remote -v`) — this is also how you confirm the pull endpoint;
   `AGENTS.md` and `CLAUDE.md`, including any existing `## Agent skills` block; routing per SKILL.md — see
   [audit-mode](audit-mode.md). Read the skills
   already installed **both project and global**. At project scope read `skills-lock.json`, primary mounts in
   `.agents/skills/`, and alias mounts such as `.claude/skills/`; at global scope read the provenance lock
   `~/.agents/.skill-lock.json`, primary mounts in `~/.agents/skills/`, and aliases such as
   `~/.claude/skills/`. Also read each scope's `external-dependencies.lock.json` when present and the
   `docs/agents/` playbooks. Use `scripts/install.py inspect` to classify mount shape; resolving paths alone
   can hide an invalid primary symlink or independent alias directory.
2. **The machine.** Confirm which harnesses are active; installed directories are evidence, not authority.
   Determine the **reachable models** and whether sibling harness CLIs are installed — the
   staffing probe. **Do this by invoking the `staffing` skill by name**, not by re-deriving a roster:
   staffing owns the machine audit, the rankings seed, and the consent-gated global write. If `staffing`
   isn't reachable, state that the machine audit needs it rather than inventing a roster. Also check the
   harness's **global memory file** (`~/.claude/CLAUDE.md` or equivalent) for the current
   `## Presentation` section or setup's legacy seeded `## Conventions` block; phase 4 reconciles that owned
   policy in phase 4 step 6.
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
  user in plain language which siblings came along and why** ("Adding `prototype` also brings `review-loop`, which
  presents the prototype for sign-off, and `staffing`, which picks which model builds it — they work together").
  Never pull a sibling silently.
- **Declared external requirements are a separate decision.** Show each merged external requirement pulled by
  the accepted closure in plain language: the capability and why the selected skill needs it. Its declaration
  permits an offer, not an install; provenance/version/scope/hooks and the external write get their own
  explicit consent at confirmation.
- **Scope is surfaced only where it matters** — apply [catalog](catalog.md) § Scope — project-first; route
  staffing's global write through its own consent gate.

Completion criterion: a resolved set of skills, each with a scope, each sibling closure complete.

## Phase 3 — Confirm the whole write

Before writing anything, show the user the complete plan and let them edit it:

- the skills to install, with the auto-pulled siblings marked and each skill's scope (project / global);
- the confirmed active harnesses and, for every declared variant, the real provider mounts and provider-lock
  records that replace the normal alias only for those harnesses;
- the deterministic dependency-first install/setup order compiled from the selected roots, including optional
  siblings that are already installed or explicitly selected;
- every merged external requirement, including the requiring skill, exact source, declared or unpinned
  version, inherited scope, capability, discovered install hooks, provider-specific install action, capability
  check, and the separate `external-dependencies.lock.json` write;
- a draft of the `## Agent skills` block that will go into `AGENTS.md`/`CLAUDE.md`;
- the `docs/agents/` playbooks that will be guaranteed (named, with which skill's setup writes each);
- the repo pointer.

Nothing touches disk until the user approves this. This is the single write gate.

Completion criterion: the user has approved the resolved plan (as-is or after edits).

## Phase 4 — Write

Execute the approved plan:

1. **Compile, then install Asher-authored skills from their canonical source.** Resolve the selected roots
   from the bundled generated catalog, fail before writes on a missing required sibling, required cycle,
   malformed external declaration, or conflicting external requirement, and install in deterministic
   dependency-first order. An optional sibling joins only when already installed or explicitly selected.
   First establish whether this is the **self-host case** using the canonical "repo is the source" detection
   in [audit-mode](audit-mode.md) step 1 (the repo's git remote is `asasher/asher-skills`, or a local
   `skills/` dir holds these skills).

   In the self-host case, a repo-owned skill — one whose install source is its catalog-resolved
   `skills/<category>/<name>/` directory —
   **still gets mounted**: source presence is not an install. The harness loads installed skills from
   `.agents/skills/` / `.claude/skills/`, never from `skills/`, so a register-only write (block + pointer +
   playbooks with nothing mounted) leaves the closure non-functional. The **guard** constrains the mechanics
   of the mount, not whether to mount:

   - **Local source, not the endpoint.** Install repo-owned skills from the repo's own root as a local
     source — `npx skills add <repo-root> --skill <ordered names...> -y` — never from the
     `https://github.com/asasher/asher-skills` endpoint, which may lag the local branch.
   - **The source directory is never an install destination.** The install produces the tool's own
     `skills-lock.json` entry (`sourceType: "local"`, tool-computed `computedHash`); the mount shape itself is
     defined by the verification step below. Verified on `skills` v1.5.15: the tool creates the
     `.claude/skills/<name>` symlink only when `.claude/skills/` already exists — when the project is worked
     from Claude Code, ensure that directory exists before installing, or add the symlink afterwards.
   - **The installed package is a build product, the copy is deliberate.** The primary mount is a real directory copy
     (identical twins with the catalog-resolved source), not a symlink into `skills/` — the same shape every consumer
     project gets. The drift this invites is handled by discipline, not linkage: never edit
     `.agents/skills/<name>` in place; edit the catalog-resolved source and refresh by re-running the same local-source
     install. Consumer-owned skill instances such as `control-plane/` and their state are project material;
     mount reconciliation must not edit or remove them.

   Still write the `## Agent skills` block, the repo pointer, and the guaranteed playbooks, exactly as for any
   other install.

   For a non-self-host install, use
   `npx skills add https://github.com/asasher/asher-skills --skill <ordered names...> -y`
   — project-local by default (the tool's project install; `-y` skips the prompt the user already answered at
   phase 3), or `-g -y` for a consented global `staffing` install. Flags verified against `skills` v1.5.15
   (`-s/--skill`, `-g/--global`,
   `-y/--yes`). Build `<ordered names...>` per scope from the union of that scope's already-installed public
   asher-skills and the compiled new closure, in deterministic dependency-first order. Run **one command per
   scope**: repeated single-skill calls can replace earlier selections from the same source. Install-command
   targets: [catalog](catalog.md) § Canonical source and declared externals.

   After each batch, compile every selected skill's declared variants for the confirmed active harnesses with
   `scripts/catalog.py materialize`, then publish all approved provider trees and
   `.agents/asher-skills/variant-lock.json` in one `scripts/install.py publish-variant` transaction. The lock
   records the shared source revision and each provider's effective-tree hash. The transaction preflights all
   destinations and the lock before replacing any tree; an injected or real failure restores every prior
   mount and leaves the prior lock unchanged. A second identical publication must make zero changes. Skills
   without `metadata.variants` skip this step and retain the real `.agents` primary plus alias symlinks.

   Then verify every named skill: use `scripts/install.py audit-variant` for declared variants and
   `scripts/install.py inspect` otherwise. The unvaried primary mount must be a
   real `.agents/skills/<name>` directory, and every expected harness alias must be a symlink to that primary.
   A primary symlink, independent alias directory, regular-file mount, dangling alias, or wrong-target alias
   is not a valid install. Also verify provenance in project `skills-lock.json` or, for global installs,
   `~/.agents/.skill-lock.json`; filesystem presence without the scope's lock provenance is incomplete. Do not
   trust the exit code: `npx skills add` can print `✖ No matching skills found` and exit 0
   after installing nothing, and `-y` mode can under-report the count.

   On a verified miss, place only the missing skill's files directly instead of trusting the failed install. This is the
   **direct-placement fallback**: copy from this repo's catalog-resolved source in the self-host case, else fetch
   the skill from the `https://github.com/asasher/asher-skills` endpoint. It never breaks
   canonical-source rule, and it mirrors the mount shape the tool would have produced — a real primary copy at
   `.agents/skills/<name>` plus symlink aliases where those harnesses are present. After placement, run
   `scripts/install.py reconcile`: it may create or replace only missing, dangling, or wrong-target symlink
   aliases when the primary is a real directory. It refuses a primary symlink, an independent alias directory,
   or any other destructive replacement; stop and ask the user to resolve those unsafe states.

   A hand-placed `skills-lock.json` fallback entry has a **specified shape**: the tool's native fields —
   `source` (the repo root path in the self-host case, else the slug `asasher/asher-skills`),
   `sourceType` (`"local"` / `"github"`), and `skillPath` for github sources — plus exactly one extension
   field, `"fallbackOrigin": true`, and **no `computedHash`**. Never fabricate `computedHash` (it is not a
   plain sha256 of `SKILL.md`), and add no free-form fields (`note` and the like). The `skills` CLI does not
   know `fallbackOrigin`; if a later successful run rewrites the entry — dropping the marker, computing a real
   hash — the tool has simply adopted the skill, which is the desired end state, not breakage. Tell the user
   the entry is fallback-origin.
2. **Install only consented declared external requirements.** Use the compiler's merged `external` output;
   never add an external merely because the user mentioned it. For each requirement, confirm that the fetched
   repository exactly matches the declared GitHub HTTPS `source`, resolve the declared `version` when present —
   `latest` is an agent instruction, not a tag: install the provider's current release or default branch
   and record the concrete commit actually installed — (otherwise disclose that it is unpinned), inspect provider manifests/scripts for install or lifecycle hooks,
   and compare the expected name, kind, and capability. Disclose source, resolved version/commit, inherited
   scope, capability, and every hook (or explicitly "none found") before obtaining explicit consent.

   Install a `skill` through the skill provider and a `codex-plugin` through Codex's plugin installer; follow
   that provider's scope and version mechanism rather than emitting an improvised generic install command.
   After installation, exercise the declared capability or its provider health check and verify its mounts or
   registration. Provider exit zero alone is insufficient. If consent is declined or capability verification
   fails, do not mark the requirement satisfied; report the requiring Asher-authored skill as non-operational
   and offer to remove it from the plan.

   Record each verified external in a consumer-owned `external-dependencies.lock.json`, separate from
   `skills-lock.json`: project dependencies use the project root; global dependencies use
   `~/.agents/external-dependencies.lock.json`. Preserve unrelated entries and record at least `name`, `kind`,
   declared `source`, declared and resolved version/commit, `scope`, `capability`, discovered hooks, provider,
   requiring skill names, and verification performed. This lock records observed provenance; it never expands
   what the selected skill sources declared.
3. **Invoke owner setup branches dependency-first.** After installation, invoke `<skill> setup` by public
   skill name in the same dependency-first order. A skill without a declared setup branch is a valid no-op.
   Staffing preserves an existing global base and writes a missing one only with explicit consent; otherwise
   it reconciles the project delta. Review-loop reconciles only its presentation-surface section. Backlog
   writes its own playbook suite. **setup-asher-skills never reads, copies, or interprets another skill's
   setup reference.** When both global Presentation and Staffing sections are consented, defer staffing's
   global module/pointer substep to step 6; the ordinary roster and project-delta setup may complete here,
   but no global pointer may apply before step 6 runs the owner applies.

   Before each invocation, atomically record the owner and status in
   `.agents/setup-asher-skills/setup-state.json`; after success, record the owned writes. A failure stops every
   dependent, reports the public owner and partial write set, and leaves completed dependencies intact. A
   retry recompiles the same graph and re-invokes idempotently from the failed owner.
4. **Write the `## Agent skills` block.** From `templates/agent-skills-block.md`, write the per-project skill
   map into the harness instruction layout. When neither instruction file exists, create canonical
   `AGENTS.md`. When either file already exists, preserve that deliberate layout and reconcile its map or
   import instead of replacing it. The block lists each
   installed skill with a one-line plain-language purpose, notes the sibling relationships, and links the repo
   pointer.
   **Guarantee the import when the block lands in `AGENTS.md`:** Claude Code never reads `AGENTS.md` on its
   own — only `CLAUDE.md` (per the official memory docs; `@`-imports inline at session start). When the
   target repo will also be worked from Claude Code, ensure its `CLAUDE.md` begins with an `@AGENTS.md`
   import (create a minimal `CLAUDE.md` holding just the import if none exists); without it the map is
   invisible to that harness. A prose "read AGENTS.md first" line is not equivalent — it depends on the
   model obeying and costs a read every session.
5. **Write the repo pointer.** From `templates/repo-pointer.md`, record that Asher-authored skills come from
   `https://github.com/asasher/asher-skills` and that updates/reconciliation run by re-invoking this skill.
6. **Reconcile global owner policy (consent-gated, per owner).** For each confirmed harness, offer the
   absolute pointer from `templates/global/presentation-pointer.<provider>.md` and the deferred module from
   `templates/global/presentation.common.md` — a seed whose `<owner>`/`<tailnet-root>` placeholders setup
   fills from this machine's facts; never install the placeholders verbatim. Use
   `scripts/render-global.py render`/`check` for previews, then
   `apply --audited <filled-module>` per harness: one command writes the deferred module atomically
   (read-back verified) and reconciles the `## Presentation` pointer section into that global file,
   preserving every user and sibling-owner byte. Invoke the public `staffing setup` owner to apply its own
   module and `## Staffing` section the same way. Never use an eager import. If a module is
   unreadable, preserve local opening, block publish/dispatch as its pointer specifies, and do not change a
   global file. A legacy `## Conventions` block is replaced only when its seeded setup-asher-skills marker is
   present; an unowned block stops for review. The migration also replaces setup's legacy seeded header with
   the compact native header. Apply does not rewrite an unchanged module; a second full
   reconcile leaves module/global bytes and inodes unchanged. These
   home-directory writes require explicit consent; projects may override surface details or roster fields in
   `docs/agents/`.

Completion criterion: the Asher-authored closure has the correct shared-primary/alias or provider-specific
mount shape and lock provenance; every
consented external is capability-verified and separately locked; each skill's playbooks are present; the
`## Agent skills` block + pointer are written; and global Presentation/Staffing policy is reconciled or
explicitly declined.

## What this skill does not do

- **Author or edit any installed skill.** setup composes the skills as they are; changing one is that skill's
  own concern.
- **Auto-install arbitrary external requests.**
- **Write a `docs/agents/` playbook itself.** It guarantees them via each skill's setup (phase 4 step 3).
