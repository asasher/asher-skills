---
name: setup-asher-skills
description: The prompt-driven installer for this skills repo. Use to set a project up with the right asher-skills, add a skill with its sibling closure, or audit an existing install for drift — an interview, one decision at a time, project-local by default, pulled only from this repo. Not for authoring skills or installing from anywhere else.
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

Prompt-driven install/audit for this repo only. The read-only compiler validates public identities,
invocation/execution policy, sibling closure, internal holds, setup pointers, and dependency order; `npx
skills` performs installation. Other skills own their setup behavior.

## Commands

- **setup** — load [interview](reference/interview.md) and [catalog](reference/catalog.md).
- **add `<skill>`** — compile one root plus required and selected/already-present optional siblings, then run
  interview confirm/write. Unknown, internal, missing, or cyclic roots fail before writes.
- **audit** — load [audit-mode](reference/audit-mode.md); compare current catalog with project/global installs,
  report drift/overlap/broken closure/scope conflicts, and propose fixes one at a time.

No argument routes to setup only when neither installed asher-skills nor an `## Agent skills` block exists;
otherwise audit, including self-host and “skills but no map” cases.

## Setup sequence

1. **Audit silently:** repo instructions/installs/playbooks. Use `staffing route` for machine reachability when
   present; on a direct clean bootstrap, perform the same read-only reachability inventory locally, record the
   missing required sibling, and include `staffing` in the confirmed atomic install before invoking its setup.
   Then ask what the project is for.
2. **Decide one item at a time:** plain-language recommendations; disclose every sibling pulled. Project scope
   is default; only staffing may be offered global with consent.
3. **Confirm total writes:** scopes, closure, map, repo pointer, and owner setup branches. Nothing writes first.
4. **Write:** per scope, atomically install the ordered union of existing public asher-skills and new closure
   with one `npx skills add <source> --skill <names...> -y` command. Self-host uses the repo root. Verify every
   landing/lock entry because a no-match can exit zero; direct-place only misses using the specified fallback
   lock shape. Then invoke declared owner setup branches dependency-first, record retry state, write the map
   and repo pointer, and apply consent-gated global conventions.

Repeated single-skill add commands can replace earlier selections from the same source, so batching is a
correctness rule. A missing setup pointer is a no-op; a failed owner stops dependants and retry resumes there.

## Dependency surface

- **Bundled:** the three references, generated `reference/catalog.json`, compiler, and this skill's templates.
- **Project/global artifacts:** map, repo pointer, and consented convention seed. Owner playbooks are guaranteed
  by invoking their public setup commands, never copied or interpreted here.
- **Sibling:** required `staffing` for machine audit/routing after bootstrap; selected skills are install
  targets, not imports.
