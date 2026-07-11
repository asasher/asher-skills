# Verdict table — issue #32 / PR #43

- Date: 2026-07-11
- HEAD graded: aafe7e650406661c3ac630c95910f9cd26b630a9 (branch `32-setup-domain-packs`)
- Executors: **A** = Claude Opus 4.8 (Agent tool, in-session); **B** = gpt-5.6-sol via `codex exec -s read-only`
- Key: `skills/backlog/evals/probes.md` § "Backlog — setup work-domain probes (issue #32)", answer key written before any runs. This repo is the no-running-app case — the probe transcript is the proof (`docs/agents/evidence.md`).

## Behavioral criteria — dual-executor probes

| Probe | Criterion | Key (must show) | Executor A (opus) | Executor B (gpt-5.6-sol) |
|-------|-----------|-----------------|-------------------|--------------------------|
| P1 | ac-3 | Ask the work-domain question before scaffolding; exactly five options software/writing/research/ops/general; default `writing` for the prose repo | **PASS** — "before scaffolding anything I ask… exactly the five… I propose `writing`… the 'manuscript' case" | **PASS** — "Before scaffolding, I ask… `software`/`writing`/`research`/`ops`/`general`… I propose `writing` as the default because the repository is a manuscript" |
| P2 | ac-4 / ac-5 | Install 4 `common/` + 7 `software/` stand-ins, each header-flagged as a code-flavored stand-in, gap named in the report; domain recorded in `backlog-policy.md` § Work domain | **PASS** — "install all eleven files… From `templates/software/` as stand-ins (7)… a header flag line on each… naming the missing-`writing`-pack gap… Record the answer in the installed `backlog-policy.md` § Work domain" | **PASS** — lists 4 common + 7 software stand-ins, "Each installed software stand-in gets a header line… name the missing writing-pack gap in the setup report… recorded in `docs/agents/backlog-policy.md` under § Work domain" |
| P3 | ac-6 | Reconcile as `software` (absent § Work domain); set = common + software; write `software` into § Work domain | **PASS** — "Which domain I reconcile against: `software`… the `software` scaffold set… I record the domain `software` in § Work domain" | **PASS** — "I treat the repository as domain `software`… `templates/common/` overlaid by `templates/software/`… I add § Work domain… `- Domain: software.`" |
| P4 | ac-4 | The pack's file shadows the common same-name file (`writing/change-description.md` wins) | **PASS** — "The **`writing` pack's** `change-description.md` lands… 'a pack file with the same name shadows the common file'" | **PASS** — "`templates/writing/change-description.md` lands… It shadows `templates/common/change-description.md` because a same-name domain-pack file takes precedence" |
| P5 | ac-8 | run step-1 preflight requires the whole scaffold set (common + recorded domain's pack); for unshipped `writing`, the software stand-ins are those counterparts → all 11 | **PASS** — "the 4 `common/` files plus the 7 `software` stand-ins… all eleven files must have `docs/agents/` counterparts", cites the run.md completion criterion verbatim | **PASS** — enumerates all 11 counterparts, cites the run.md completion criterion verbatim including the unshipped-pack clause |

**Behavioral result: 10/10 — P1–P5 pass 5/5 on both executors, with citations. No probe flagged a genuine ambiguity; every answer is decided by an explicit sentence.** Pass bar (`5/5 on both executors, with citations`) met.

## Static criteria — re-checked at HEAD aafe7e6

| Criterion | Check | Observed | Verdict |
|-----------|-------|----------|---------|
| ac-1 | `find skills/backlog/templates -type f` | exactly `common/` (backlog-policy, change-description, environment, platform = 4) + `software/` (change-fixer, change-reviewer, diagnosing-bugs, evidence, implementing, refactoring, verifying = 7); `find -maxdepth 1 -type f` = 0 flat files | **PASS** |
| ac-2 | `git diff --find-renames --stat main -- templates/` | all 11 templates are renames — 10 shown `R100` (byte-identical), `backlog-policy.md` `R090` with +7 lines = the added § Work domain slot, no other content change | **PASS** |
| ac-7 | grep `docs/agents/backlog-policy.md` and `templates/common/backlog-policy.md` | `templates/common/backlog-policy.md` ships `## Work domain` slot; this repo's `docs/agents/backlog-policy.md` records "Domain: **software** … Recorded 2026-07-11 (issue #32)" | **PASS** |
| ac-9 | `git diff --name-status --find-renames main -- skills/backlog/reference/`; skill name | among bundled references only `reference/run.md` and `reference/setup.md` changed — every other reference byte-identical; `SKILL.md` frontmatter `name: backlog` unchanged (no rename) | **PASS** |
| ac-11 | `diff -rq skills/backlog/ .agents/skills/backlog/` | reports IDENTICAL — installed copy content-matches source | **PASS** |

(ac-8 also has a static face — SKILL.md/README/run.md describe the `common/` + `<domain>/` layout and a grep finds no stale flat-`templates/*.md` phrasing; both confirmed at HEAD. ac-10 is the meta-criterion "the probes pass against a pre-written key", satisfied by the 10/10 above.)

**Overall: all behavioral (P1–P5 × 2 executors = 10/10) and static (ac-1, ac-2, ac-7, ac-8, ac-9, ac-11) criteria pass at HEAD aafe7e6.**
