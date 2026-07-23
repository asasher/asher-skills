# v1 → v2 consumer migration plan

Migrate the four repos carrying v1 backlog-family installations — **metis**, **pipelines**,
**integrations-v2**, and **asher-skills itself** — onto the v2 SDLC family, losing nothing important.
Grounded in a full per-repo audit: every mount, playbook line, tracker label, in-flight artifact, and
script was inventoried and mapped (`migration-maps.md` in this directory carries all 260 per-artifact
actions; `migration-inventories.json` the raw inventories). This plan is the executable synthesis and
was adversarially reviewed against those tables; the migrating agent works with plan and tables open
together — where a per-repo table row is more specific than a plan step, the table row governs.

## Ground rules

- **Never `npx skills remove`** — with a local-source lockfile it deletes skill *sources*. Retired
  mounts are removed by hand: the `.agents/skills/<name>` dir, the `.claude/skills/<name>` entry, and
  the lockfile record.
- **Reconcile, never overwrite**: every existing playbook is repo-owned; earned content moves to its
  named v2 target *before* the old file is deleted. The per-repo action tables name the target file and
  section for every line.
- **Third-party/domain mounts are untouched** (convex, clerk, shadcn, railway, etc.), and so are
  repo-internal skills — metis's `migration` skill is Metis-authored repo content whose only copy lives
  in `.agents/skills/`.
- **Staffing keeps its variant contract**: recompile both provider trees and keep
  `.agents/asher-skills/variant-lock.json`; a declared variant's `.claude` mount is a real compiled
  directory, never a symlink.
- **Bindings are verified per repo, never copied across repos.** `backlog setup` live-verifies every
  platform verb in each repo; a verb recorded live in one repo (asher-skills'
  `.issue_dependencies_summary` read) is a known-stale gotcha in another (pipelines) — the live probe
  in *that* repo decides, and pipelines' recorded working alternative stays.
- Work per repo lands as a reviewed change (branch + PR), like any other change. asher-skills follows
  the same post-merge path as the consumers: PR #90 ships the family; this issue's agent migrates all
  four repos from main afterward.

## Sequence (per repo, in order)

**0. Rescue pass — commit the uncommitted, close the dispatch window.** Before any other git or mount
   operation:
   - metis: commit issue-233/235's untracked plan HTMLs and issue-236's modified product code in their
     worktrees.
   - pipelines: commit the main checkout's uncommitted changes and the untracked
     `ask-syncron-parts-planning` mount; backfill its lock entry.
   - asher-skills: pin `rescue/reconcile-consumers` on detached HEAD `2493ecb` before any worktree
     cleanup; pull `ready-for-agent` from #80 (or hold all builds) so no v1 run can dispatch it
     mid-migration.
   - All repos: backfill lockfile entries for every lock-less mount the tables flag (metis:
     `migration`, `web-design-guidelines`, `vercel-composition-patterns`; pipelines:
     `qa-user-journeys`, `sentry-cli`; integrations-v2: its five) — **before** any bulk or
     lockfile-driven operation, so "set matches lockfile" checks can never read a repo-earned mount as
     deletable.

**1. Migrate the tracker labels.** Create `needs-shaping`, `shaping`, `building` (and any missing v2
   role labels) so later steps have somewhere to park work. The `in-flight` → `building` question has
   two valid shapes — rename via `gh label edit` (label follows historical issues) or keep the name
   and bind the `building` role to `in-flight` in backlog-policy (zero tracker mutation) — see
   Decisions. asher-skills: rename `needs-spec` → `needs-shaping` (description already matches; #92
   rides along). Existing human-workflow labels stay neutral and are never repurposed. Renames wait
   until step 2's drain confirms no live v1 thread still greps the old name.

**2. Drain the live v1 machinery.** Nothing is swapped under a running loop.
   - Deliver or park pending review-server verdicts (metis #233 round-2; pipelines' live review PID
     for the preferred-supplier-routing plan). Parked work goes to the now-existing `needs-shaping` or
     `ready-for-human` with the open state commented.
   - integrations-v2, **before any mount is touched**: post the `.git/backlog/runs` handoff's exact
     unblock steps for #242 and #250 as comments on those issues, and archive `run-state.py` and the
     run dirs (tar into the repo's evidence area) — the mount swap deletes the runs' only reader. Its
     7 open PRs #257–#263 **finish under current v1 semantics** — no relabel, no reset, no
     re-dispatch; whether the swap waits for them is a Decision.
   - `review-server.py --stop` each live state dir, `--sweep` the repo's surface hub, clear the
     tailscale serve path handlers.
   - Let running build/plan threads finish or park them (metis's two live v1 runs resume through
     `.agents/skills/backlog/reference/` paths that the reinstall deletes — drain first).

**3. Atomic v2 install** — one `npx skills add <asher-skills repo> --skill <roster> -y` from main,
   with the **complete** roster in a single command (sequential adds replace earlier selections):
   backlog, shape, build, adversarial-review, code-review, implement, tdd, diagnosing-bugs,
   verify-your-work, prove-your-work, merge-changes, to-spec, to-tickets, interview, domain-modeling,
   research, prototype, to-thread, to-subagent, watch-until, serve-via-tailnet, handoff, staffing —
   **plus, on asher-skills, `skill-loop`** (and any other repo-recorded extras in that repo's
   lockfile: the per-repo table's install row is the authoritative set). Then hand-remove the retired
   v1 mounts: `plan`, `review-loop`, `improve`, `diagnose`, `setup-asher-skills` — and, **after their
   Decisions resolve**, the old third-party `tdd`/`handoff` copies (they'd shadow the v2 skills of the
   same name), `greploop`, and pipelines' `uncodixfy`. Repair the known lockfile oddities (metis `yjs`
   missing `skillPath`; pipelines `database-migrations`/`shadcn` self-referential sources).

**4. Reconcile the playbooks** — run v2 `backlog setup` (and `staffing setup`) in reconcile mode, then
   execute the migrate actions from the repo's table:
   - `platform.md`, `backlog-policy.md`, `environment.md`, `evidence.md`, `change-description.md`:
     same files, new sections — carry every earned binding forward (staging-base rules, `Dispatch:`
     block requirements, optimistic claim + orphan-sweep rules, deferred-closure labels), fill the new
     v2 sections (headless stack contract, deploy-target constraints, credential preflight,
     per-ticket-disposable stores, lane mechanics + lock path, quiet horizon, claim attribution).
   - **`codebase.md` is born from the retired files**: TYPESCRIPT.md/MODULES.md/I18N.md
     (integrations-v2), frontend.md (pipelines), and the repo-specific seams, check commands, and
     gotchas embedded in implementing.md/verifying.md/refactoring.md/diagnosing-bugs.md across all
     repos. Their generic method prose is superseded by the v2 skills and drops; their repo facts are
     the payload.
   - Then delete the retired playbooks — each only after its earned lines are placed: planning.md
     (after the plan-form Decision), implementing.md, verifying.md, change-reviewer.md,
     change-fixer.md, refactoring.md, researching.md, prototyping.md, diagnosing-bugs.md (file, not
     skill), frontend.md.
   - Rewrite literal `.agents/skills/review-loop/scripts/` paths in environment.md to
     `.agents/skills/serve-via-tailnet/scripts/` (same script lineage, same verdict semantics).

**5. Disposition of remaining tracker state** — a groom, human-confirmed: per-ticket and per-branch
   proposals for what steps 0–2 didn't already settle (metis #233/#235/#236/#234 residue; pipelines
   #232 and its unmerged branch set; asher-skills #80's superseded-or-residual call and the codex/*
   branches). Committed plans (`plans/*.html`, `.plans/*.html`) stay in git as historical artifacts
   with their ac-N anchors regardless of the plan-form Decision.

**6. Verify.** Installed set matches the (now-backfilled) lockfile; `backlog setup`'s live verb
   verification passes in this repo; staffing eval expectations hold for the recompiled variants; then
   one small real ticket through the full v2 pipeline (groom → build → review → evidence) as the smoke
   test.

## Decisions for the human

1. **Browser verification.** v2 hard-defaults to Playwright-driving-Chrome and demotes agent-browser.
   metis has no Playwright; pipelines' earned policy was agent-browser-first. Recommendation: adopt
   the v2 default (install Playwright per repo, record headed fallback and gaps) — the transcripts
   showed agent-browser wedging across repos — but it reverses an earned policy, so it's yours.
2. **Plan-artifact form going forward** (metis, integrations-v2): keep committed self-contained HTML
   plans with ac-N anchors (approved via serve-via-tailnet annotated mode), or move fully to v2
   spec-on-ticket with `AC-N` markdown ids. Recommendation: spec-on-ticket, HTML plans grandfathered
   in place. metis's planning.md deletion waits on this.
3. **integrations-v2 swap timing**: drain-first (wait for PRs #257–#263 to merge — clean, but gated on
   the human unblocking #242) or swap-now with the PRs finishing under v1 semantics around the new
   mounts. Either way the PRs themselves are not relabeled or re-dispatched.
4. **Label mechanics** (pipelines, asher-skills option too): rename `in-flight` → `building`, or keep
   the name and bind the role in backlog-policy (zero mutation). Recommendation: rename, post-drain.
5. **Old third-party `tdd`/`handoff` mounts** (integrations-v2 esp.): confirm replace-with-v2 before
   the atomic install — they'd shadow the family versions.
6. **`greploop`** (pipelines): retire, or redeclare as an external if still used.
7. **`uncodixfy`** (pipelines): retired from the family but load-bearing for frontend playbook text —
   recommended: declared external requirement in `external-dependencies.lock.json`.
8. **impeccable's divergent copies** (metis, pipelines): declare a provider variant, reconcile to one
   copy, or leave untouched with a provenance note. Someone must vouch for the divergence first.
9. **asher-skills staffing mount**: recompile the Claude variant as a real dir per variant-lock
   (recommended) or re-declare as unvaried.
10. **writing-great-skills provenance** (asher-skills): adopt a source dir under `skills/` or
    re-record as an external.
11. **Issue #80** (asher-skills): superseded by PR #90's decoupling, or residual scope into a
    v2-shaped ticket?
12. Small per-repo calls surfaced in-flow: lane-lock path + stale horizon defaults, pre-push hook
    management (metis), `needs-triage` deletion (integrations-v2), ticketizing the I18N translation
    backlog at first groom, parallelism-verdict re-derivation where the v1 record conflated
    "serialize" with "user chose sequential".

## Must-not-lose (aggregated crown jewels — full lists per repo in the tables)

- Every repo's **earned platform/tracker bindings**: staging-base + promotion-closure semantics,
  `Dispatch:` block requirement with skip-don't-infer, optimistic claim + never-silently-reset orphan
  sweep, native dependency verbs — including pipelines' stale-counter gotcha (bindings live-verified
  per repo, never copied).
- **Uncommitted work**: metis's untracked plan HTMLs and modified issue-236 code; pipelines' dirty
  main checkout and untracked mount; the detached-HEAD rescue commit — all committed in step 0.
- **integrations-v2's `.git/backlog/runs` handoff content** — posted to #242/#250 and archived before
  the only reader is removed.
- **integrations-v2's convention files** (TYPESCRIPT.md, MODULES.md, I18N.md incl. the enumerated
  hardcoded-English backlog) and **pipelines' frontend.md** — the seed corpus for `codebase.md`.
- **metis's `migration` skill** and every lock-less repo-earned mount (backfilled in step 0).
- **Committed plan artifacts** with ac-N anchors that existing evidence links point into.
- **Unmerged branches** — every one gets an explicit disposition before any cleanup.
- **Staffing variant-lock contracts** and recorded per-direction reachability state.
- **Review-server verdict/event logs** — stopped and swept, archived where their state dirs are
  removed, never silently deleted while their tickets are open.

## Rollback

Each repo's migration is one branch/PR, so the git side reverts cleanly. The out-of-git mutations are:
label creations/renames (each a reversible `gh label edit`), issue comments (additive), review-server
stops/sweeps and tailscale handler removal (re-servable from the swept state), and the archival of
dead review-state and run-state dirs (tarred before removal — restorable, not regenerable). Retired
mounts are recoverable from the lockfile record + this repo's history.
