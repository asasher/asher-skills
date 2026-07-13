---
name: setup-asher-skills
description: The prompt-driven installer for this skills repo. Use to set a project up with the right asher-skills, add a skill with its sibling closure and declared external requirements, or audit an existing install for drift — one decision at a time, project-local by default. Not for authoring skills or arbitrary undeclared installs.
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
pointers, and dependency order; provider installers perform approved writes. Other skills own their setup
behavior.

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

1. **Audit silently:** repo instructions/installs/playbooks. Use `staffing route` for machine reachability when
   present; on a direct clean bootstrap, perform the same read-only reachability inventory locally, record the
   missing required sibling, and include `staffing` in the confirmed atomic install before invoking its setup.
   Then ask what the project is for.
2. **Decide one item at a time:** plain-language recommendations; disclose every sibling and external
   requirement pulled. Project scope is default; only staffing may be offered global with consent.
3. **Confirm total writes:** scopes, closure, external provenance/version/capability/hooks, provider actions,
   locks, map, repo pointer, and owner setup branches. Nothing writes first.
4. **Write:** per scope, atomically install the ordered union of existing public asher-skills and new closure
   with one `npx skills add <source> --skill <names...> -y` command. Self-host uses the repo root. Verify every
   primary mount, alias mount, and lock provenance because a no-match can exit zero; direct-place only misses
   using the specified fallback lock shape. Install only consented declared externals with their provider,
   verify capability, and record `external-dependencies.lock.json`. Then invoke owner setup branches
   dependency-first, record retry state, write the map and repo pointer, and apply consent-gated conventions.

Repeated single-skill add commands can replace earlier selections from the same source, so batching is a
correctness rule. A missing setup pointer is a no-op; a failed owner stops dependants and retry resumes there.

## Dependency surface

- **Bundled:** the three references, generated `reference/catalog.json`, catalog compiler, mount helper, and
  this skill's templates.
- **Project/global artifacts:** map, repo pointer, and consented convention seed. Owner playbooks are guaranteed
  by invoking their public setup commands, never copied or interpreted here.
- **Sibling:** required `staffing` for machine audit/routing after bootstrap; selected skills are install
  targets, not imports.
- **External:** none. External requirements in a selected skill's compiled closure are install targets, not
  dependencies of this installer.
