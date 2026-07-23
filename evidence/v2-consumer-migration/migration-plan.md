# v1 → v2 consumer migration plan

Migrate the four repos carrying v1 backlog-family installations — **metis**, **pipelines**,
**integrations-v2**, and **asher-skills itself** — onto the v2 SDLC family, losing nothing important.
Grounded in a full per-repo audit: every mount, playbook line, tracker label, in-flight artifact, and
script was inventoried and mapped (`migration-maps.md` in this directory carries all 260 per-artifact
actions; `migration-inventories.json` the raw inventories). This plan is the executable synthesis; the
action tables are its appendix and the migrating agent works with both open.

## Ground rules

- **Never `npx skills remove`** — with a local-source lockfile it deletes skill *sources*. Retired
  mounts are removed by hand: the `.agents/skills/<name>` dir, the `.claude/skills/<name>` entry, and
  the lockfile record.
- **Reconcile, never overwrite**: every existing playbook is repo-owned; earned content moves to its
  named v2 target *before* the old file is deleted. The per-repo action tables name the target file and
  section for every line.
- **Third-party/domain mounts are untouched** (convex, clerk, shadcn, railway, etc.), and so are
  repo-internal skills — metis's `migration` skill is Metis-authored repo content whose only copy lives
  in `.agents/skills/`; any mounts-directory sweep must exclude it (give it a provenance record so the
  next cleanup can't mistake it for a stale install).
- **Staffing keeps its variant contract**: recompile both provider trees and keep
  `.agents/asher-skills/variant-lock.json`; a declared variant's `.claude` mount is a real compiled
  directory, never a symlink.
- Work per repo lands as a reviewed change (branch + PR), like any other change.

## Sequence (per repo, in order)

**1. Drain the live v1 machinery.** Nothing is swapped under a running loop.
   - Deliver or park pending review-server verdicts (metis #233 round-2; pipelines' live review
     PID for the preferred-supplier-routing plan). Parked work goes to `needs-shaping` or
     `ready-for-human` with the open state commented.
   - `review-server.py --stop` each live state dir, `--sweep` the repo's surface hub, clear the
     tailscale serve path handlers.
   - Let running build/plan threads finish or park them the same way (metis's two live v1 runs resume
     through `.agents/skills/backlog/reference/` paths that the reinstall deletes — drain first).

**2. Migrate the tracker labels.** Create `needs-shaping`, `shaping`, `building` (and any missing v2
   role labels); rename `in-flight` → `building` after the drain (`gh label edit` — the label follows
   historical issues, which is fine once no live v1 thread greps the old name). asher-skills: rename
   `needs-spec` → `needs-shaping` (description already matches; #92 rides along). Bind everything else
   per the repo's reconciled `backlog-policy.md`; existing human-workflow labels stay neutral and are
   never repurposed.

**3. Atomic v2 install.** One `npx skills add <asher-skills repo> --skill <full v2 roster> -y`
   (from main, post-merge): backlog, shape, build, adversarial-review, code-review, implement, tdd,
   diagnosing-bugs, verify-your-work, prove-your-work, merge-changes, to-spec, to-tickets, interview,
   domain-modeling, research, prototype, to-thread, to-subagent, watch-until, serve-via-tailnet,
   handoff, staffing. Then hand-remove the retired v1 mounts: `plan`, `review-loop`, `improve`,
   `uncodixfy`*, `greploop`, `diagnose`, `setup-asher-skills`, and the old third-party `tdd`/`handoff`
   copies that would shadow the v2 skills of the same name. (*pipelines: see Decisions — uncodixfy is
   load-bearing for its frontend playbook and may become a declared external instead.) Repair lockfile
   oddities met along the way (metis `yjs` missing `skillPath`; pipelines `database-migrations`/`shadcn`
   self-referential sources).

**4. Reconcile the playbooks** — run v2 `backlog setup` (and `staffing setup`) in reconcile mode, then
   execute the migrate actions from the repo's table. The shape of it, common to all four:
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
   - Then delete the retired playbooks: planning.md, implementing.md, verifying.md,
     change-reviewer.md, change-fixer.md, refactoring.md, researching.md, prototyping.md,
     diagnosing-bugs.md (file, not skill), frontend.md — each only after its earned lines are placed.
   - Rewrite literal `.agents/skills/review-loop/scripts/` paths in environment.md to
     `.agents/skills/serve-via-tailnet/scripts/` (same script lineage, same verdict semantics).

**5. Disposition of in-flight tracker state** — a groom, human-confirmed: per-ticket and per-branch
   proposals for everything the audit surfaced (metis #233/#235/#236/#234 and the orphaned run
   threads; pipelines #232 and its unmerged branch set; integrations-v2's 7 open PRs #257–#263;
   asher-skills #80 + its branch, and the codex/* branches). Committed plans (`plans/*.html`,
   `.plans/*.html`) stay in git as historical artifacts with their ac-N anchors; new work uses v2
   spec-on-ticket with `AC-N` markdown ids.

**6. Verify.** Installed set matches the lockfile; `backlog setup`'s live verb verification passes;
   staffing eval expectations hold for the recompiled variants; then one small real ticket through the
   full v2 pipeline (groom → build → review → evidence) as the smoke test.

## Decisions for the human (grouped; everything else the agent proposes and you confirm in-flow)

1. **Browser verification.** v2 hard-defaults to Playwright-driving-Chrome and demotes agent-browser
   from verification. metis has no Playwright; pipelines' earned policy was agent-browser-first.
   Recommendation: adopt the v2 default (install Playwright per repo, record headed fallback and gaps),
   since the transcripts showed agent-browser wedging across repos — but it changes an earned policy,
   so it's yours to call.
2. **impeccable's divergent copies** (metis and pipelines both carry two differing real dirs, no
   lockfile entry): declare a provider variant, reconcile to one copy, or leave untouched with a
   provenance note. Someone must vouch for the divergence before any dedupe.
3. **uncodixfy in pipelines**: retired from the family but load-bearing for frontend playbook text —
   recommended: keep as a declared external requirement in `external-dependencies.lock.json`.
4. **asher-skills staffing mount**: variant-lock declares two variants but `.claude/skills/staffing`
   is a symlink — recompile the Claude variant as a real dir (recommended) or re-declare as unvaried.
5. **writing-great-skills provenance** (asher-skills): adopt a source dir under `skills/` or re-record
   as an external.
6. **Issue #80** (asher-skills): superseded by PR #90's decoupling, or does residual scope survive?
7. Small per-repo calls the agent will surface in-flow: lane-lock path + stale horizon defaults,
   pre-push hook management (metis), `needs-triage` deletion (integrations-v2), whether to ticketize
   the I18N translation backlog during the first v2 groom, parallelism-verdict re-derivation where the
   v1 record conflated "serialize" with "user chose sequential".

## Must-not-lose (the crown jewels, aggregated — full lists per repo in the tables)

- Every repo's **earned platform/tracker bindings**: staging-base + promotion-closure semantics,
  `Dispatch:` block requirement with skip-don't-infer, optimistic claim + never-silently-reset orphan
  sweep, native dependency verbs with numeric-id write recipe.
- **integrations-v2's convention files** (TYPESCRIPT.md, MODULES.md, I18N.md incl. the enumerated
  hardcoded-English backlog) and **pipelines' frontend.md** — the seed corpus for `codebase.md`.
- **metis's `migration` skill** (repo-authored, only copy in the mounts dir).
- **Committed plan artifacts** with ac-N anchors that existing evidence links point into.
- **Unmerged branches** flagged per repo — every one gets an explicit disposition before any cleanup.
- **Staffing variant-lock contracts** and the recorded per-direction reachability state.
- The **review-server verdict/event logs** under each repo's state dirs — swept, not deleted, until
  their tickets close.

## Rollback

Each repo's migration is one branch/PR; the tracker label renames are the only out-of-git mutations,
and each is a single reversible `gh label edit`. Nothing deletes review-server state dirs or committed
artifacts; retired mounts are recoverable from the lockfile record + this repo's history.
