# Issue 44 compactness dossier

Measured with `tiktoken` 0.13.0, `cl100k_base`, against approved-plan commit `8999bf0`. Counts include
frontmatter because the harness pays to load it.

| Entry point | Before | After | Change |
|---|---:|---:|---:|
| backlog | 1,391 | 1,374 | -17 |
| plan | 1,377 | 557 | -820 |
| prototype | 1,207 | 472 | -735 |
| review-loop | 1,322 | 589 | -733 |
| setup-asher-skills | 1,833 | 736 | -1,097 |
| staffing | 1,150 | 591 | -559 |
| all authored `SKILL.md` entry points | 39,355 (25 skills) | 36,300 (26 skills) | -3,055 despite adding diagnosing-bugs |

The seven refactored core entry points are 41–55 lines. Compactness came from moving complete disciplines
behind named interfaces, not deleting their gates.

## Representative load traces

- **Backlog run:** `backlog/SKILL.md` → `run.md` + `run-state.md` + `issue-loop.md` → project policy/platform.
  `staffing route` selects the issue coordinator before the worktree and child dispatch. A child loads only
  its branch reference and playbooks; it may ambiently invoke any matching installed model skill.
- **Bug:** `backlog/SKILL.md` → `diagnose.md` → named `diagnosing-bugs` → `method.md`; the project diagnosis
  playbook is delta-only. The added method is intentionally a small net expansion because it replaces a
  duplicated, less complete backlog template with a reusable six-phase contract.
- **Enhancement:** `plan/SKILL.md` → `plan-contract.md`; `authoring.md` and the HTML skeleton load only at the
  writing gate. `prototype` loads only for an unresolved artifact-shaped question; `review-loop` loads only
  for sign-off.
- **Review:** `review-loop/SKILL.md` → CLI reference for the selected command; loop and surface contracts load
  only for a served review. Watcher work is a separately staffed child.
- **Install:** `setup-asher-skills/SKILL.md` → interview or audit reference → generated catalog. Owner setup
  references are invoked dependency-first only after the atomic install succeeds.

## Deletion and extraction ledger

- Removed backlog's duplicated diagnosis method and replaced it with the named `diagnosing-bugs` sibling.
- Replaced repeated plan/prototype/review/staffing technique prose in composers with narrow public contracts.
- Kept setup instructions as `reference/setup.md` owned by the primary skill; no nested setup skill exists.
- Split source browsing into one category layer while keeping installed names and composition flat.
- Kept complete lifecycle, failure, fallback, and evidence rules in branch references instead of restating
  them in every caller.

## Correctness retained or added

- Catalog compiler: ten tests for identities, invocation policy, closure, cycles, internal holds, setup
  pointers, migration paths, README parity, and dependency-first order.
- Backlog durable run state: four tests for concurrent parents, per-parent sequence locking, stale process
  rejection, and complete handoffs.
- Review server: four process-boundary tests for detached survival, watcher independence, concurrent servers,
  and stale-instance cleanup safety.
- Behavioral probes cover issue #44–#55 routing, setup, diagnosis, direct-fix escape, native dependencies,
  evidence reuse, reviewer/fixer loops, and sibling-harness dispatch.
- Clean-install fixtures proved closure and zero missing siblings for staffing, backlog, maquette, bayes, and
  goodwork using one atomic command per scope.

## Independent cold read

An adversarial reader restricted itself to one module at a time. It recovered triggers, public commands,
gate order, fallbacks, dependency surfaces, and conditional pointers for all seven core skills. Its three
material ambiguities were corrected before commit: explicit-only versus ambient invocation, install closure
versus runtime reach, and clean-install staffing bootstrap. Four smaller command/README mismatches were also
corrected. Credits were complete in every reviewed skill.
