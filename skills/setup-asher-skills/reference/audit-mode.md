# Audit mode — reconcile an existing install

Re-invoking setup on a project that already has a `## Agent skills` block runs `audit`. A project with
installed asher-skills but no block also reaches `audit`; this mode handles that populated-but-no-map state
and repairs it through the **Missing map** finding. Compare what's installed against this repo's current
catalog and report what drifted, overlaps, or broke — then propose fixes one at a time. This file stands
alone.

## Reconciliation is an LLM audit — no version stamps

**Reconciliation is the model reading the live repo against what's installed and judging it — not a number
comparison.** setup writes **no version stamp, no `vNN` marker, no content hash, and no template-version
comment** as the drift-detection mechanism, and it does not look for one. This is a deliberate departure from
backlog, which stamps installed playbooks with `<!-- ...: vNN -->` and reconciles by comparing versions.
**setup introduces no such stamp.** If you find yourself wanting to write or diff a version token to detect
drift, that is the wrong mechanism for this skill: read the installed text and the repo, and judge.

(The `skills` tool maintains its own `skills-lock.json` hashes for its own install bookkeeping — that is the
tool's concern, not setup's reconciliation mechanism. setup does not add or read stamps of its own.)

## What the audit does

1. **Fetch the repo's current catalog.** Read this repo's current set of skills from the public GitHub
   endpoint (`https://github.com/asasher/asher-skills`) — the source of truth for what exists now. If the
   repo being audited is the source itself (git remote is `asasher/asher-skills`, or a local `skills/` dir
   holds these skills), use the local `skills/` working tree as the catalog instead of the fetched remote, and
   state the branch-vs-origin relationship (for example, "local is ahead of origin") so local work does not
   look like fleet-wide drift.
2. **Read what's installed.** Both scopes: project (`skills-lock.json`, `.claude/skills/`, `.agents/skills/`)
   and global (`~/.claude/skills/`, `~/.agents/skills/`); the `## Agent skills` block; and the `docs/agents/`
   playbooks. Resolve symlinks before comparing, so a symlinked `.claude/skills/<name>` and
   `.agents/skills/<name>` pair is one skill with two mount points, feeding the cross-harness overlap category
   instead of double-counting as two installs.
3. **Compare and report — in prose.** Describe each finding and what to do about it:
   - **Drift** — a skill installed here whose content diverges from the repo's current version (read both and
     judge; don't diff a stamp).
   - **Overlap** — a skill installed both project and global, or listed twice; say which scope should win
     (project-first: keep local, drop the redundant global unless it is `staffing`). Also report
     **cross-harness duplication** when the same skill appears in both `.claude/skills/` and `.agents/skills/`:
     a symlinked pair is note-only, not drift, because it is one underlying skill with two mount points; two
     independent copies can diverge, so flag them and recommend consolidating to one source.
   - **Broken closure** — a composer installed without its full sibling set (a `plan` with no `review-loop`,
     a `backlog` missing `prototype`); name the missing siblings from [catalog](catalog.md) § The closure
     rules.
   - **Scope conflict** — something global that should be project-local, or a project-local `staffing` that
     the user might want global; state the project-first default and let the user decide.
   - **Foreign source** — a skill whose `skills-lock.json` source is not `asasher/asher-skills`; surface and
     advise only, because an external skill may be intentional. Honor [catalog](catalog.md) § Pull only from
     this repo: offer our adapted equivalent if we ship one, or say plainly that we don't ship it, and never
     propose reinstalling from the foreign repo or auto-removing it.
   - **New in the repo** — a skill the repo now ships that fits this project and isn't installed; offer it.
   - **Orphaned map entry** — a `## Agent skills` line for a skill no longer installed; propose removing it.
   - **Missing map** — installed asher-skills are present but there is no `## Agent skills` block; propose
     writing the block, then continue the same one-fix-at-a-time audit discipline.
4. **Propose fixes one at a time.** Same discipline as `setup`: present each proposed change with a
   plain-language reason, one decision at a time, and change nothing until the user approves — then apply and
   refresh the `## Agent skills` block.

Completion criterion: every divergence between the installed set and the repo's current catalog is reported,
and the user has decided on each proposed fix.
