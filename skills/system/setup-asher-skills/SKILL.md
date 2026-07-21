---
name: setup-asher-skills
description: "The prompt-driven installer for this skills repo: set a project up, add a skill with its closure, or audit an install for drift. Not for authoring skills or undeclared installs."
argument-hint: "[setup | add <skill> | audit]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: thread
  requires: [staffing]
  optional: []
---

# setup-asher-skills

Prompt-driven install/audit for Asher-authored skills from this repo. The read-only compiler validates public
identities, invocation/execution policy, sibling closure, external declarations, internal holds, setup
pointers, provider overlays, and dependency order; provider installers perform approved writes. Other skills
own their setup behavior.

## Commands

- **setup** — load [interview](reference/interview.md) and [catalog](reference/catalog.md).
- **add `<skill>`** — compile one root plus required and selected/already-present optional siblings and merged
  external requirements, then run interview confirm/write. Unknown, internal, missing, cyclic, or conflicting
  declarations fail before writes.
- **audit** — load [audit-mode](reference/audit-mode.md); compare current catalog with project/global installs,
  report drift/overlap/broken closure/scope conflicts, and propose fixes one at a time.

No argument routes to setup only when neither installed asher-skills nor an `## Agent skills` block exists;
otherwise audit, including self-host and “skills but no map” cases.

## Setup sequence

**Audit** → **interview** → **confirm** → **write**, per [interview](reference/interview.md) Phases 1–4;
every gate lives there.

## Dependency surface

- **Bundled:** the three references, the catalog/provider compiler (`scripts/catalog.py`), mount
  publisher/auditor, and this skill's templates.
- **Project/global artifacts:** map, repo pointer, consented setup-owned presentation pointer/module, and the
  per-owner global apply (module + pointer section, read-back verified).
- **Sibling:** required `staffing` for machine audit/routing after bootstrap; selected skills are install
  targets, not imports.
- **External:** none. External requirements in a selected skill's compiled closure are install targets, not
  dependencies of this installer.
