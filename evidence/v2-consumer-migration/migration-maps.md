

# metis

## [MIGRATE] mount: backlog (v1, .agents/skills/backlog + .claude symlink)
v2 backlog mount, installed atomically with the full v2 roster (backlog, shape, build, adversarial-review, code-review, implement, tdd, diagnosing-bugs, verify-your-work, prove-your-work, merge-changes, to-spec, to-tickets, interview, domain-modeling, research, prototype, to-thread, to-subagent, watch-until, serve-via-tailnet, handoff, staffing) via one `npx skills add` command
ORDER MATTERS: reinstall only after live runs 20260723-236-plan and 20260723-233-235 settle (finish or park), because v1 run threads resume through .agents/skills/backlog/reference/ paths and run-state.py, both deleted by the reinstall. v2 ships no reference/ dir — platform.md's 'spawned threads read bundled references at .agents/skills/backlog/reference/' row must be re-derived by v2 setup against the new mounts.

## [RETIRE] mount: plan (v1)
Replaced by the v2 shape skill (interactive settling, composing interview/domain-modeling) + to-spec (spec on the ticket, diagram first). Nothing lost: the 20 committed plans/*.html artifacts stay in git and keep their ac-N anchor contract for existing evidence; the plan-approval machinery (hash-bound verdicts) lives on in serve-via-tailnet's annotated mode.

## [RETIRE] mount: review-loop (v1, ships review-server.py + review-await.py invoked by literal path)
Replaced by serve-via-tailnet's annotated mode — the SAME review-server.py/review-await.py lineage now ships at .agents/skills/serve-via-tailnet/scripts/ with the same verdict semantics (hash-bound approve/request-changes, hub, --stop/--sweep) and review-await exit-code contract. Nothing lost IF sequenced: (1) deliver or park pending verdicts (#233 round-2), (2) `review-server.py --stop` each live state dir and `--sweep --surface ~/.backlog/surface/metis`, (3) clear tailscale serve path handlers, (4) delete the mount, (5) rewrite environment.md's literal .agents/skills/review-loop/scripts/ paths to .agents/skills/serve-via-tailnet/scripts/.

## [MIGRATE] mount: diagnosing-bugs (v1)
Refresh to v2 skills/software-development/diagnosing-bugs; its repo playbook retires (see playbook action) with seams moving to codebase.md

## [MIGRATE] mount: prototype (v1)
Refresh to v2 skills/software-development/prototype; prototyping.md's repo bindings move to codebase.md § Conventions

## [MIGRATE] mount: research (v1)
Refresh to v2 skills/software-development/research; researching.md's repo bindings move to backlog-policy.md (research work-type) and environment.md

## [RETIRE] mount: setup-asher-skills (v1 installer: install.py/catalog.py/render-global.py)
Replaced by the `npx skills add <repo> --skill <names...> -y` atomic-install flow that the asher-skills repo now standardizes on; skills-lock.json remains the provenance record. Nothing lost: the installer's job (copy sources, write lockfile, mount aliases) is what npx skills does.

## [MIGRATE] mount: staffing (declared provider variant — .agents codex tree + .claude REAL compiled claude tree + .agents/asher-skills/variant-lock.json)
Refresh to v2 staffing preserving the variant contract: recompile BOTH provider trees and keep variant-lock.json — never 'clean up' .claude/skills/staffing into a symlink and never delete .agents/asher-skills
v2 staffing also carries the new Playwright-first browser-verification default (commit 5dac012), which interacts with the environment.md driver decision below.

## [RETIRE] mount: tdd (mattpocock third-party origin, installed as part of the v1 family)
Superseded by the v2 Asher-authored tdd skill (red→green with pre-agreed seams + anti-pattern list) installed in the roster batch. The repo-tuned facts it was referenced through (implementing.md/refactoring.md test commands) migrate to codebase.md, so nothing repo-specific rides on the old mount.

## [KEEP] mount: clerk-backend-api
Third-party domain skill, lockfile-tracked, orthogonal to the family swap

## [KEEP] mount: clerk-cli
Third-party domain skill, lockfile-tracked, untouched

## [KEEP] mount: cloudflare
Third-party domain skill, lockfile-tracked, untouched

## [KEEP] mount: use-railway (ships own python scripts)
Third-party domain skill with its own tooling, untouched

## [KEEP] mount: vercel-cli
Third-party domain skill, untouched

## [KEEP] mount: yjs (lockfile entry missing skillPath)
Third-party domain skill; while editing skills-lock.json for the family swap, repair the missing skillPath field so a future lockfile-driven operation doesn't mishandle it

## [KEEP] mount: impeccable (NOT in lockfile; two divergent real copies .claude vs .agents)
Do not dedupe or symlink during migration — the divergence may be a deliberate undeclared provider variant; leave both real dirs byte-untouched pending the human decision below

## [KEEP] mount: migration (Metis-authored INTERNAL domain skill; only copy lives in .agents/skills)
Repo-owned content that must survive: exclude .agents/skills/migration from any mounts-directory wipe; add a provenance record (lockfile entry with local/internal source, or move canonical source into the repo proper) so the next cleanup can't mistake it for a stale install

## [KEEP] mount: web-design-guidelines (no lockfile entry)
Third-party SKILL.md-only mount; exclude from lockfile-driven cleanup; optionally backfill a lockfile entry

## [KEEP] mount: vercel-composition-patterns (no lockfile entry)
Third-party mount with AGENTS.md + rules/; exclude from lockfile-driven cleanup; optionally backfill a lockfile entry

## [MIGRATE] playbook: docs/agents/backlog-policy.md
Reconciled in place against v2 templates/common/backlog-policy.md — same file, new sections
Migrates verbatim: label bindings incl. the 'never substitute the human workflow labels ready for planning/ready for implementation' rule → § Label roles neutral list; staging label semantics → § Closure ('built'-style deferred-closure binding: merged to staging, closed by the promotion PR's Closes #n); work-type set incl. draft (judgment-terminal, provisioned 2026-07-10) and the research/draft/code routing rule → § Label roles work-type + boundary note; Dispatch: block requirement (Surface/Coordination class/reason; missing → skip, never infer) → § Dispatch metadata; blocker = priority-not-dependency → § Neutral; native dependencies + legacy body lines + read-the-list-not-counters → § Dependencies; human-confirmed shortlist rule → § Readiness decision; optimistic claim marker, re-read-before-mark, 7-day orphan sweep never-silently-reset → § Building hygiene (new: claims must now be actor-attributed per v2). New sections to fill: Work domain = software; needs-shaping/shaping roles (new labels below); in-flight→building rename.

## [MIGRATE] playbook: docs/agents/environment.md
Reconciled in place against v2 templates/common/environment.md
Migrates: staging-as-base + fork-from-origin/staging + codex/<n>-<slug> naming + PR/deploy facts → § Branching & deploys (new rows to fill: deploy-target constraints, credential preflight — e.g. cheap live reads for Vercel/Railway/PartyKit/QStash creds); pnpm dev service list, portless URLs, fixed ports, log commands (from diagnosing-bugs.md) → § Running locally (NEW headless-stack contract: pnpm dev needs a recorded detached wrapper + teardown audit); cloud-singleton regime, setup:worktree copies-but-does-not-remap fact, full 16-row singleton table → § Worktree isolation (ADD the v2-mandated parent-.git lock row); seed=none/drive-the-app + CLI JSONL load → § Seed data (+ new drive-to-feature paths); AgentMail OTP/magic-link recipe, AGENT_EMAIL/AGENTMAIL_API_KEY, never-print-secrets → § Authenticating (+ new session-reuse storage-state row); VERIFY-<issue>-<purpose> naming, retain-through-evidence, scale-criteria-blocked rule → § Verification data (NEW per-ticket-disposable-stores row to fill); drivers + codex-exec second-opinion + deferred-checks list → § Driving the app (CONFLICT: v2 defaults to Playwright and disqualifies agent-browser — decision below); tailnet review surface, LaunchAgent com.asher.backlog-surface:8377, tailscale serve recipes, static-publish symlink, keep-awake=none → § Presenting to the human, now owned by serve-via-tailnet setup, with every literal .agents/skills/review-loop/scripts/ path rewritten to .agents/skills/serve-via-tailnet/scripts/; staffing no-override + worktree note → § Staffing delta; serialize-verification verdict + its reasons → § Parallelism verdict (NEW lane-mechanics lock path + stale horizon to choose — decision below).

## [MIGRATE] playbook: docs/agents/platform.md
Reconciled in place against v2 templates/common/platform.md
Migrates: dunnharland/metis gh binding → § Tracker; effect-verified blocker read via the dependencies/blocked_by LIST endpoint — deliberately overriding the v2 template's default counter-based read, because metis proved counters lag (effect-verified 2026-07-14) — and the POST/DELETE write verbs → § Tracker verbs; staging-PR-does-not-close + promotion-PR-must-carry-Closes → Close-on-merge linkage; gh pr create --base staging, exact-LGTM approval, human-merges-squash → § Change review; worktree-add-from-origin/staging + squash-merge-orphans-pinned-SHAs re-pin rule → § Version control incl. Pinned-SHA semantics; cross-harness worker routes (codex exec --cd / claude -p no --bare, worker-only never coordinator) → § Harness (new rows: wrapper staffing evidence, directional reachability + successors, route-trust drift handling); Monitor/native-watcher wakeup → Durable monitor row. Retired: the bundled-references path row (v1 .agents/skills/backlog/reference/ no longer exists) — re-answered by v2 setup against the new mounts.

## [MIGRATE] playbook: docs/agents/verifying.md
File retires; content splits: check commands, pnpm check aggregate + its recorded baseline warnings, and the CI facts (ci.yml jobs; CI does NOT run tests; CI-green procedural-not-host-enforced with the 403 rulesets finding) → docs/agents/codebase.md § Checks; per-change-type evidence bars (logic/UI/data) + repo-wide expectations (Clerk boundaries, Yjs persistence, migrations, Drive, background jobs, responsive/a11y) → docs/agents/evidence.md § What to capture repo-specific rows; codex-exec second-opinion delegation → environment.md § Driving the app

## [MIGRATE] playbook: docs/agents/implementing.md
File retires; its shipped tdd doctrine is superseded by the v2 tdd skill (drop); earned content: vitest/tsx-test seams + single-file invocation + colocated foo.test.ts naming → codebase.md § Testing patterns; Conventional Commits + the pre-push-hook auto-commit fact + snake_case-new-files + package-boundary + docs/UI.md deference → codebase.md § Conventions

## [MIGRATE] playbook: docs/agents/evidence.md
Reconciled in place against v2 templates/software/evidence.md
Much of metis's earned content is now upstream template text (GIF two-pass recipe, ?raw=1 blob-URL rule with private-repo camo facts, mechanical-verification checks, MP4 ban, styling-only reuse) — reconcile rather than duplicate. Keep as repo rows: probes-are-not-evidence stance, evidence/<slug>/ + c<criterion>- naming, squash-merge-orphans-SHAs re-pin rule (also in platform.md), the exact reviewer verdict string 'no product-code change; no recapture', capture-once-after-convergence hands-back-posts-nothing.

## [MIGRATE] playbook: docs/agents/planning.md
File retires (the plan skill is gone); plan threshold (multi-subsystem / migrations / risky / >1 day) → backlog-policy.md § Dispatch metadata as the route:direct vs orchestrator-required guidance; hash-bound-approval-not-comments + ledger-disposition-per-annotation → carried natively by serve-via-tailnet's annotated mode (record surface binding in environment.md § Presenting); the committed-HTML-plan contract (plans/<n>-<slug>.html, inline SVG via mmdc, ac-N data-criterion anchors, commit-to-work-branch-before-dispatch, posterity digest comment) → change-description.md § This repo (the outline's SHA-pinned Plan row consumes it) — pending the plan-form decision below; the ac-N anchor contract must stay documented regardless because 20 committed plans and 23 evidence dirs key on it

## [MIGRATE] playbook: docs/agents/change-reviewer.md
File retires (v2 code-review skill supersedes the Fowler/Cursor template body); repo scrutiny list (Clerk boundaries, Yjs, Drive, background jobs/email, API compat, a11y, staging/prod credential leakage) + presumptive blockers (~1000-line files, ad-hoc flags, feature logic in shared paths, thin wrappers, sequential orchestration) + open-every-cited-test rule → codebase.md § Conventions / repo-specific patterns (read by code-review); product-semantics-questions-are-ruling-requests → the v2 adversarial-review contract carries this; exact-LGTM + exact recapture verdict → platform.md § Change review and evidence.md

## [MIGRATE] playbook: docs/agents/change-description.md
Reconciled in place against v2 templates/common/change-description.md — the v2 outline already matches metis's earned order (Closes+work-type, Summary w/ scope discovery, Changes-as-reasoning, SHA-pinned Plan, Checks run, CI disclosed, Verification caveats, Evidence placeholder, research→dossier section); keep as § This repo: PR title = Conventional Commits subject because squash-merge makes it the commit subject

## [RETIRE] playbook: docs/agents/change-fixer.md
Superseded by the v2 adversarial-review skill's fixer contract, which carries the same discipline (address every actionable comment, reply with change + SHA, reasoned non-fixes, re-prompt reviewer); the file was mostly-template and its earned lines are restatements of that contract — nothing repo-specific lost

## [MIGRATE] playbook: docs/agents/diagnosing-bugs.md
File retires (v2 diagnosing-bugs skill needs no per-skill playbook); seams (vitest/tsx-test, one-file regression command) → codebase.md § Testing patterns; logs:workflows/logs:redis/logs:db commands + pnpm-dev-for-repro → environment.md § Running locally

## [MIGRATE] playbook: docs/agents/prototyping.md
File retires; register-prototype-scripts-in-owning-package + apps/web routing + snake_case → codebase.md § Conventions; ?variant= URL-param gating + screenshot-each-variant-via-the-environment-driver → codebase.md § Conventions with the capture route deferring to environment.md § Driving

## [RETIRE] playbook: docs/agents/refactoring.md
Superseded by v2 tdd/implement; its earned lines (test commands, snake_case, package boundaries, store/migration patterns) are duplicates of content already migrating to codebase.md § Checks and § Conventions from implementing.md/verifying.md — nothing unique lost

## [MIGRATE] playbook: docs/agents/researching.md
File retires (v2 research skill is self-contained); research/<slug>/ durable root + scratch-in-temp + stays-out-of-evidence/ → backlog-policy.md research work-type row; serialize-shared-database/provider-mutations → environment.md § Parallelism; cite-stable-locators + preserve-customer-data are v2 research skill invariants (no repo delta lost)

## [MIGRATE] playbook target: docs/agents/codebase.md
NEW file created by v2 backlog setup from templates/software/codebase.md — the landing zone for implementing.md/verifying.md/refactoring.md/change-reviewer.md/prototyping.md earned content as itemized above; also document the unmanaged .git/hooks/pre-push auto-fix behavior under § Conventions so it stops living only in a retired playbook

## [RENAME] label: in-flight (live on #236, #234)
in-flight → building: `gh label edit in-flight --name building --repo dunnharland/metis` — an in-place rename keeps the label attached to #236/#234 and preserves their branch+date claim comments
Sequence after the two live v1 runs settle (or accept that v1 run threads still grepping 'in-flight' must not run post-rename). v2 additionally expects claim comments to name the runner's actor — backfill on any claim that survives the migration.

## [RENAME] labels: needs-shaping, shaping (v2 additions)
Create: `gh label create needs-shaping --repo dunnharland/metis --description "parked for strategic shaping"` and `gh label create shaping --repo dunnharland/metis --description "a shaping thread is attending it"`; bind in backlog-policy.md § Label roles

## [KEEP] label: staging (~24 open issues carry it)
Binds directly to v2 backlog-policy § Closure's deferred-closure slot ('merged to staging, closure deferred to the promotion merge'); do not rename or wipe — it is the ONLY record of which open issues are merged-but-unpromoted, and the promotion PR must still carry Closes #n for each

## [KEEP] labels: ready-for-agent, ready-for-human, needs-info
Identity mapping to the v2 roles of the same names; #227 (needs-info) and #179 (ready-for-human) carry over with no relabeling

## [KEEP] labels: bug, enhancement, refactor, research, draft (work-types)
Map 1:1 to v2 work-type roles — v2 now natively defines the draft (judgment-terminal) and research (epistemic-terminal) branches metis pioneered, plus the same routing boundary rule

## [KEEP] labels: wontfix, duplicate, invalid, superseded, blocker, and the neutral human-workflow set
Exclusions map 1:1; blocker stays bound as priority-metadata-not-a-dependency-edge; 'ready for planning'/'ready for implementation'/etc. stay neutral and explicitly off-limits as role substitutes, recorded in backlog-policy.md § Neutral

## [KEEP] in-flight ticket #236 (LGTM at f81be065, evidence gate pending; worktree has UNCOMMITTED product code + tests)
Finish under the v1 machinery before the family swap: commit the worktree's modified files immediately, run the evidence gate, merge to staging, apply staging label — its run dir and the review-loop scripts it resumes through must survive until then

## [KEEP] in-flight ticket #234 (fix committed, branch pushed)
Finish: drive to PR/review under whichever family is live at the time (it needs no v1-only machinery beyond the label); on merge it takes the staging label per policy

## [KEEP] in-flight tickets #233/#235 (plan-approval round-2 awaiting verdict; worktrees hold UNTRACKED plan HTML)
Commit the two plans/*.html files in worktrees issue-233/issue-235 NOW (they are the only copies); then per the decision below either finish the round-2 approval on the v1 review surface before sweeping it, or park both tickets to needs-shaping and re-enter via v2 shape

## [KEEP] ~24 staging-labeled open issues (#70 #166 #173 ... #226)
No relabeling; the pending staging→main promotion PR carrying Closes #n for each is unchanged by the migration and remains the closure path

## [RETIRE] .git/backlog/runs/* (six run-state dirs incl. two LIVE)
Superseded by v2's tracker-as-the-run-ledger (claim + outcome comments; dispatcher resumes by reconciling claims against worktrees/branch tips) — but only AFTER runs 20260723-236-plan and 20260723-233-235 finish or are parked; then archive the dirs (e.g. tar to a repo-external archive) rather than rm, since board.md/handoff.md/review subdirs are the only record of how those changes were reviewed

## [RETIRE] worktrees /Users/asher/Projects/metis-worktrees/issue-{70,223,225,226}
Their issues carry staging (merged); after confirming each branch has no commits ahead of origin/staging and no uncommitted files, tear down via the recorded worktree-remove verb — v2 merge-changes owns this cleanup going forward

## [KEEP] worktrees issue-233, issue-235, issue-236 (uncommitted content)
Untouchable until their untracked plan HTML (233/235) and modified product code (236) are committed — any prune loses the only copies; dispose per their tickets' finish/park path

## [KEEP] six /Users/asher/.claude/worktrees/metis/agent-* worktrees (codex/183, 173, 180, 177, 181, 182)
Park pending per-branch audit: their issues carry staging, but the branches are reported ahead of origin/staging — diff each against origin/staging and only tear down branches proven fully merged; a blanket cleanup would destroy unmerged commits

## [KEEP] local-only branch zippy-wren (yjs forced-reconnection + sync-status tests, no remote)
Push a remote backup (`git push -u origin zippy-wren`) or explicitly park with a note on a tracker issue before any branch hygiene — it is the only copy of that work

## [KEEP] plans/ (20 committed artifacts) and evidence/ (23 committed dirs)
Git-safe; their consumers' contracts survive via the migrated playbooks — ac-N anchors documented in change-description.md § This repo, SHA re-pin rule in platform.md/evidence.md; never rebase staging (orphans pinned evidence SHAs)

## [KEEP] research/ and datasets/ dirs
research/<slug>/ remains the durable research root under the v2 research work-type binding in backlog-policy.md

## [MIGRATE] live review-surface state: ~/.backlog/surface/metis (issue dirs 181/182/183, registry.json), LaunchAgent com.asher.backlog-surface, tailscale serve path handlers
Swept with the v1 tooling, then rebound to serve-via-tailnet: run review-server.py --stop per live state dir and --sweep on the surface BEFORE the review-loop mount is deleted (it is the only tool that knows the registry), clear stale `tailscale serve` path handlers; the LaunchAgent + surface dir + /review proxy carry over unchanged as serve-via-tailnet's surface, recorded by its setup into environment.md § Presenting to the human

## [RETIRE] script: .agents/skills/backlog/scripts/run-state.py + evals/test_run_state.py
No v2 successor by design — the tracker is the run ledger; deleted with the v1 backlog mount after live runs settle (their state archived per the .git/backlog/runs action)

## [RETIRE] scripts: .agents/skills/review-loop/scripts/review-server.py + review-await.py
Same-lineage scripts ship in the v2 serve-via-tailnet mount (scripts/review-server.py, scripts/review-await.py, same verdict + exit-code contract); every literal invocation recorded in environment.md is rewritten to the new path as part of the environment.md reconcile

## [RETIRE] scripts: .agents/skills/setup-asher-skills/scripts/{install.py,catalog.py,render-global.py}
Deleted with the setup-asher-skills mount; npx skills add + skills-lock.json replace install/catalog, and the v2 staffing skill owns global-module rendering

## [MIGRATE] script: .agents/skills/staffing/scripts/render-global.py
Carried by the v2 staffing refresh's compiled provider variants — reinstall recompiles it into both trees per variant-lock.json

## [KEEP] script: scripts/setup_worktree.sh (repo-owned, pnpm setup:worktree)
Repo-owned and referenced by environment.md § Worktree isolation, including the earned copies-but-does-not-remap caveat that motivates the cloud-singleton verdict

## [KEEP] .git/hooks/pre-push (auto-commits lint/format fixes)
Unmanaged by any installer; its behavior migrates from implementing.md into codebase.md § Conventions so the fact survives, with the commit-it-into-the-repo question left to the decision below

## [KEEP] LaunchAgent com.asher.backlog-surface (port 8377 → ~/.backlog/surface)
Machine-level plumbing independent of the skill family; becomes the serving substrate serve-via-tailnet's setup records in environment.md § Presenting

## DECISIONS NEEDED
- Tickets #233/#235: finish the round-2 plan approval on the live v1 review surface before sweeping it, or park both to needs-shaping and re-enter through v2 shape (discarding the pending v1 approval round but keeping the committed plan HTML as shaping input)?
- Plan artifact form going forward: keep metis's committed self-contained HTML plans (plans/<n>-<slug>.html with ac-N anchors, approved via serve-via-tailnet annotated mode) as the repo's spec deliverable, or adopt to-spec's spec-on-the-ticket form? Existing plans/evidence keep the ac-N contract either way.
- Browser verification: v2 environment.md hard-defaults to Playwright driving Chrome and disqualifies agent-browser as a verification route, but metis has no Playwright and its recorded driver IS agent-browser — adopt Playwright (add e2e/, verify headless launch, accumulate specs as the regression suite) or record browser verification as a hard gap? This decides how the deferred-checks list (Clerk login, screenshots, recording) is re-verified.
- impeccable's two divergent real copies (.claude vs .agents, no lockfile entry): declare a provider variant in variant-lock.json, reconcile to one copy, or leave as-is with provenance noted? Requires knowing whether the divergence was deliberate.
- Lane mechanics for serialize-verification (new v2 requirement): choose the lock path (e.g. /Users/asher/Projects/metis/.backlog-lane.lock beside the primary checkout) and the stale horizon — metis previously had 'one thread exercises the full stack, no exception lane' with no lock artifact at all.
- Headless stack contract (new v2 requirement): pnpm dev is a multi-service foreground launcher — a detached wrapper with logs, recorded stop/restart, and audited teardown must be authored and verified; decide the wrapper form before setup can mark the section verified.
- Pre-push hook: commit the auto-fix hook into the repo (managed, survives fresh clones) or leave it as unmanaged .git/hooks state documented in codebase.md?
- Timing of the in-flight → building rename relative to #236/#234: rename now (label follows the issues, but any still-running v1 thread greps the old name) or after both runs land?

## MUST NOT LOSE
- The 16-row shared-singleton collision table + the serialize-verification parallelism verdict + the setup:worktree copies-but-does-not-remap finding — derived from a live-stack audit (2026-07-14) v2 setup cannot cheaply repeat
- Effect-verified GitHub dependency verbs: read the dependencies/blocked_by LIST (counters lag — this deliberately overrides the v2 template's counter-based default) and the POST/DELETE write shape, verified on throwaway issues 2026-07-14
- The staging-label closure semantics and the ~24 open staged issues: the label is the only record of merged-but-unpromoted state, and the promotion PR must carry Closes #n for each — wiping or renaming it makes closure state unrecoverable
- Live-run resume state until #236 and #233/#235 settle: .git/backlog/runs/{20260723-236-plan,20260723-233-235} plus the uncommitted files in worktrees issue-236 (product code + tests) and issue-233/issue-235 (only copies of their plan HTML), and the local-only branch zippy-wren
- The review-machinery handover ordering: stop/sweep live review servers with the v1 review-server.py BEFORE deleting the review-loop mount, and rewrite environment.md's literal script paths to serve-via-tailnet — otherwise orphaned tailscale handlers and registry rows remain with no tool to reap them, and the recorded review commands dangle
- CI-divergence facts: CI runs lint/format/typecheck/build-boot but NOT tests (pnpm test is local-gate-only), CI-green is procedural not host-enforced (rulesets API 403 on this plan), and the pnpm check baseline of one lint + one workspace-lint warning — losing these re-teaches them via a bad merge
- The AgentMail auth recipe (AGENT_EMAIL sign-in, OTP/magic-link read via AGENTMAIL_API_KEY, same inbox for invitations) — the only recorded path for an agent to mint a real session
- The internal 'migration' skill: its only copy lives in .agents/skills/migration and no lockfile entry protects it — any mounts-directory wipe deletes a Metis-authored skill outright
- The staffing provider-variant structure: .claude/skills/staffing is a real compiled tree recorded in .agents/asher-skills/variant-lock.json — a symlink-normalizing cleanup silently breaks the variant contract


# asher-skills

## [RETIRE] mount .agents/skills/backlog (v1 monolith) + .claude/skills/backlog symlink
Replaced by v2 skills/software-development/backlog via one atomic `npx skills add <repo> --skill <complete set> -y` committed on the sdlc-lifecycle branch. Nothing lost: v1 SKILL/templates/reference are git-tracked (recoverable from history); the run-state machinery is superseded by v2's tracker-as-ledger (claim comment + outcome comment + resume reconciliation, SKILL.md § build); the v1 step templates it carried are covered by the migrate actions on docs/agents/*.md below. NEVER `npx skills remove` — the lockfile's local source path would delete the v2 source itself; delete the mount dir, symlink, and lockfile entry by hand, then reinstall.
Mount-only files with no v2 counterpart: scripts/run-state.py, evals/test_run_state.py, evals/liveness-probes.md, reference/, templates software/{change-fixer,change-reviewer,implementing,refactoring,verifying}.md, skill-authoring/verifying.md.

## [RETIRE] mount scripts: .agents/skills/backlog/scripts/run-state.py + evals/test_run_state.py + evals/liveness-probes.md
v2 backlog has no run-state scripts by design: 'the tracker is the run ledger' — attributed claim comments, outcome comments, per-dispatch deadlines, and resume-time reconciliation against live worktrees/branch tips replace run-state files and liveness probes. Verdict waits stay with the canonical serve-via-tailnet review-await.py. Git history retains the v1 machinery.

## [RETIRE] mount .agents/skills/diagnosing-bugs (5-line drift)
Replaced by the refreshed v2 source skills/software-development/diagnosing-bugs in the same atomic install; docs/agents/diagnosing-bugs.md (its repo playbook) is kept and reconciled, so the earned content survives outside the mount.

## [RETIRE] mount .agents/skills/merge-changes (2 files drifted)
Replaced by v2 source skills/software-development/merge-changes in the atomic install; drift is stale-mount lag, no repo-earned content lives in the mount.

## [RETIRE] mount .agents/skills/prototype (6-line drift)
Replaced by v2 source skills/software-development/prototype in the atomic install; docs/agents/prototyping.md keeps the repo-earned content and remains a v2 reader target.

## [RETIRE] mount .agents/skills/research (7-line drift)
Replaced by v2 source skills/software-development/research in the atomic install; docs/agents/researching.md keeps the repo-earned content and remains a v2 reader target.

## [RETIRE] mount .agents/skills/staffing (14-line drift) + variant-lock.json oddity
Replaced by refreshed skills/system/staffing via staffing's own install-and-reconcile/apply step (provider trees under .agents/ are compiled, never hand-edited — codebase.md). The apply step must resolve the invalid state: variant-lock.json declares two provider variants with different effective_hash values while .claude/skills/staffing is physically a symlink to the codex mount. Either recompile a real Claude variant directory or drop the variant declaration — see decisions. render-global.py and eval suites ride along in the refreshed mount; canonical eval suites already run from the source per codebase.md, so nothing is mount-only.

## [KEEP] mount .agents/skills/skill-loop
Byte-identical to source skills/system/skill-loop; not part of the SDLC family and not superseded (it consumes probe evals as input). It MUST be named in the atomic `npx skills add` set — sequential/partial adds replace earlier selections, so omitting it drops it.

## [KEEP] mount .agents/skills/writing-great-skills (third-party, mattpocock/skills)
Keep the mount untouched — it is the ONLY working-tree copy (skills-lock records a local source that does not exist under skills/, so any lockfile-driven reinstall of it fails and a mount wipe loses it from the working tree). Exclude it from the atomic add command and verify afterward the add did not disturb it; fix its provenance record separately (see decisions).

## [KEEP] docs/agents/backlog-policy.md
Reconcile in place against templates/common/backlog-policy.md — edited, never overwritten. Section map: work-domain 'software' line → § Work domain (recorded choice stands); readiness identity mappings → § Label roles (with the two label fixes below); work-type labels + draft/research routing rule → § Label roles work-type + the boxed boundary note (v2 template now carries the same rule — dedupe, keep the repo's phrasing where sharper); dispatch metadata block requirement → § Dispatch metadata (matches v2 verbatim in spirit; keep 'missing fields are a grooming gap, never permission to infer'); GitHub-native in-review/closed → § Label roles Closure paragraph; blocked_by native relation + duplicate-of/superseded-by conventions → § Dependencies; readiness confirmation rule (agent applies ready-for-agent only to human-confirmed shortlist) → § Readiness decision; orphan sweep (7-day quiet horizon, never silently reset) and optimistic-claim concurrency → NEW § Building hygiene (v2 adds attributed claims — record that the claim comment names runner actor + branch + dispatch date, upgrading the v1 'branch name and dispatch date' comment).

## [RENAME] label in-flight (0 open issues)
in-flight → building: `gh label edit in-flight --name building --repo asasher/asher-skills` (add a description matching the v2 role). Zero open issues carry it, so the rename is clean; update backlog-policy.md's binding line in the same commit. The in-flight comment convention (branch + dispatch date) survives as the v2 attributed claim comment.

## [RENAME] label needs-spec (1 open: #92) vs playbook binding needs-shaping
needs-spec → needs-shaping: `gh label edit needs-spec --name needs-shaping` — the label's description ('Parked for strategic shaping') already IS the v2 role, and #92 keeps the label through the rename. Alternative is recording needs-shaping → needs-spec as the bound alias in backlog-policy.md § Aliases; either way the playbook and tracker must stop disagreeing (today the playbook binds a label that does not exist). See decisions.

## [RENAME] label shaping (does not exist)
create new: `gh label create shaping --repo asasher/asher-skills --description "A shaping thread is attending it"` — v2 groom sets it at thread dispatch, replacing needs-shaping, so a subject never gets two threads. Setup creates it with user consent per SKILL.md § setup.

## [KEEP] labels ready-for-agent, ready-for-human, needs-info; work-types bug/enhancement/refactor/research/draft; exclusions wontfix/duplicate/superseded/invalid; neutral documentation/question/good-first-issue/help-wanted
All identity mappings to v2 defaults — v2 setup reuses existing labels rather than minting duplicates; record them explicitly in the reconciled § Label roles / § Exclusion / § Neutral so nothing is re-derived.

## [KEEP] docs/agents/environment.md
Reconcile in place against templates/common/environment.md. Existing earned lines land in matching v2 sections: base branch/branch naming → § Branching & deploys; 'no CI, no preview, no deploy on merge — merge just updates main' → § Branching & deploys (change-request/merge produce nothing); 'skills repo, no dev stack; running the app = driving a probe scenario' → § Running locally; worktree regime local-isolatable + `git worktree add <path> -b <branch> main` → § Worktree isolation; shared singletons (GitHub tracker serialized writes, tailnet surface one-review-at-a-time) → § Worktree isolation singleton table; seed regime none / probe scenario in evals/ → § Seed data; gh-as-asasher + Codex own-subscription auth, never hardcode/echo → § Authenticating for testing; VERIFY-<issue>-<purpose> fixtures, never shared mutable fixtures, synthetic-prompt validity boundary → § Verification data; drivers (Claude subagent, `codex exec -s read-only --skip-git-repo-check`, python3 direct) + evidence-per-surface → § Driving the app & capturing evidence; ALL tailnet content (root URL, surface dir, bring-up rules, http.server 8390 + `tailscale serve --set-path` recipe, publish-a-doc symlink recipe, review-server self-host invocation, review-await exit codes 0/3/10/124, hub sweep, reap rules incl. stale /review:8377, port 8377 held, 'always open <url>') → § Presenting to the human under serve-via-tailnet ownership; keep-awake: none → note kept beside Presenting; staffing deltas (skill design orchestration-grade, dual-executor, no floor override) → § Staffing delta; serialize-verification-by-choice → § Parallelism verdict.
New v2 sections to fill during reconcile: § Branching & deploys credential preflight (gh auth status + `codex exec` cheap live read — this is what backlog build's per-run preflight uses) and deploy facts (n/a — record 'skills consumed via npx skills add; no deploy target'); § Running locally headless contract (record 'no dev stack — nothing to detach'); § Verification data per-ticket-disposable stores (the ticket's own worktree, its VERIFY-* fixtures, its ~/.backlog/surface/asher-skills/<issue>/ entry — everything else shared); § Worktree isolation parent-.git contention row (template-shipped, add verbatim); § Parallelism lane mechanics (choose a lock path if serialize-verification stands — see decisions); § Driving the app: record that the Playwright-default web-driver bullet is n/a here (no browser-driven app surface; probe executors are the drivers), keeping the template's rule visible for rendered-HTML artifacts.

## [KEEP] docs/agents/platform.md
Reconcile in place against templates/common/platform.md — every earned verb already fits a v2 section: tracker binding + list/view/comment/edit/create/close verbs → § Tracker; the LIVE-VERIFIED blocked_by read (`--jq '.issue_dependencies_summary'`) and write (resolve numeric id, POST dependencies/blocked_by) → § Tracker blocker verbs (v2 template ships the same commands — the repo's 'verified live, do not substitute task-list prose' note stays); Closes #<n> default + direct close exception → § Tracker close-on-merge; PR verbs, exact-LGTM approval, human-or-authorized-merge-changes merge, loop-never-merges → § Change review; worktree/sync/push verbs + pinned-SHA force-push orphaning → § Version control; Claude Code harness, Agent tool isolation:'worktree', bounded `codex exec --cd`, bounded `claude -p` NEVER --bare, directional reachability → § Harness; spawned threads read .claude/skills/<name>/ + docs/agents/ → § Harness reference-readability bullet; ScheduleWakeup/Monitor + review-await blocking + watch-until ladder → § Harness durable-monitor bullet.
New v2 bullets to fill: wrapper staffing evidence (record what the native spawn reports, or 'unproven' per template) and the route-trust/drift paragraph (template-shipped, adopt as-is).

## [KEEP] docs/agents/codebase.md
Already the v2-shape file (codebase.md is new in v2 and this repo has it, earned). Reconcile against templates/software/codebase.md and make it the landing zone for the retired step playbooks' migrations (below). Existing map: skill-prose-is-product + redundant-negation rule + commit style → § Conventions; catalog gate (PATH=/usr/bin:$PATH python3 tools/test_catalog.py), site/check.py exit-code-masking trap, staffing eval suites + BASELINE_BYTES*0.8 byte budget, zsh `==` runner trap → § Checks; probe answer-key re-cite rule + stdlib unittest one-file-per-tool → § Testing patterns; mounts-are-build-products / never-npx-skills-remove / staffing trees compiled-not-hand-edited → § Generated artifacts.

## [KEEP] docs/agents/evidence.md
Reconcile against templates/software/evidence.md — much of its earned content has been upstreamed into the v2 template, so reconcile = dedupe to template text and keep the repo-specifics. Repo-specific keepers: probe-eval transcript as the honest no-running-app proof (v2 § What to capture's greenfield clause, add the repo's 'on a repo with an app this is NOT a substitute' warning); research dossiers stay under research/, never copied into evidence/ → § What to capture repo-specific bullet; per-change-type table (skill behavior/script/visual/prose) and 'green it-renders screenshot is not enough' → § What to capture repo-specific; styling-only reuse only at final reviewed HEAD with the exact reviewer verdict phrase → § What to capture Timing; AFK-vs-witnessed → v2 § Obligation scales with absence (template now carries it — dedupe). Template-absorbed (verify identical, then defer to template): GIF ffmpeg recipe + 10MB ceiling + never-MP4 + c<criterion>- naming → § Format and storage; ?raw=1 same-origin embeds, camo-proxy 404s, no-CDN-API, embed form, mechanical checks (gh api commits/<sha>, git cat-file -e), orphaned-SHA re-pin → § GitHub binding; repo-relative embeds + publish-directory-root-or-skip → § Local binding.

## [KEEP] docs/agents/change-description.md
Reconcile against templates/common/change-description.md: no-PR-template + imperative sentence-case title → § This repo; Closes #<n> and the Claude Code attribution line → § This repo; 'no CI — readiness is green probe eval + LGTM' → the CI-status bullet; research-dossier substitution for Evidence → now template-shipped in the Evidence bullet (dedupe); evidence placeholder wording → template-shipped.

## [KEEP] docs/agents/probe-evals.md
Repo-authored eval discipline, not a backlog-setup product — referenced 21 times across v2 skill sources. Keep untouched; it is the substrate the v2 family's verification model leans on (two tiers, answer-key-before-runs, dual-executor, context-fidelity split, citation requirement, canonical examples).

## [KEEP] docs/agents/diagnosing-bugs.md (playbook)
Still a first-class v2 consumer surface — skills/software-development/diagnosing-bugs/SKILL.md, README, setup reference, and answer key all point at it. Reconcile with the v2 diagnosing-bugs setup template; all earned lines stay: skill-bug definition + reproduce-through-both-executors, reproducing scenario becomes a probe in that skill's evals/, py_compile-then-drive for script bugs, model-variance flaky-surface rule, probe-eval equivalence as the prose-skill regression seam.

## [KEEP] docs/agents/prototyping.md
Still referenced by the v2 prototype skill (SKILL.md, README, reference/prototyping.md). Reconcile; earned lines stay: no build system, self-contained single-file HTML for tailnet rendering, prototypes live OUTSIDE skill dirs (workspace/scratchpad) so throwaway code never ships in a self-contained skill.

## [KEEP] docs/agents/researching.md
Still referenced by the v2 research skill (SKILL.md, README, setup reference). Reconcile; earned lines stay: research/<slug>/ durable root, workspace option, scratch-to-tempdir, research-out-of-evidence/ rule, primary local sources + stable locators, never publish credentials, serialized writes, Presentation policy.

## [MIGRATE] docs/agents/implementing.md
File retires (no v2 reader — the implement/tdd skills replace the step playbook); earned lines move to docs/agents/codebase.md: 'no unit-test framework; tests are probe scenarios; test-first = write/adjust probe + answer key first, confirm current skill fails, then change and re-run' → codebase.md § Testing patterns; 'tests live in each skill's own evals/' → codebase.md § Testing patterns (where tests live); repo conventions reviewers expect (self-contained dirs, compose-by-name, stdlib-only Python 3, probe eval for new/reworked skills) → codebase.md § Conventions; bare-minimum-ux sibling wins on UI conflict + impeccable PRODUCT.md/DESIGN.md ambient-context rule → codebase.md § Conventions (repo-specific patterns a newcomer would miss); commit style → already in codebase.md § Conventions (dedupe, drop here).

## [MIGRATE] docs/agents/verifying.md
Content splits; the file then retires (or survives only as the optional 'check playbook' change-description.md § Checks-run mentions — see decisions). Line map: checks-narrowest-first (probe eval, py_compile-then-drive on Python 3.14, no npm/lint/build pipeline) → codebase.md § Checks; site-drift rule (any SDLC-family skill change runs python3 site/check.py; errors block) → codebase.md § Checks; aggregate pre-PR gate (probe eval green vs answer key + scripts compile and run; pre-deployment eval for new/reworked skills) → codebase.md § Checks (the full gate line); second-opinion codex-exec executor for subjective criteria → probe-evals.md dual-executor contract already carries it (dedupe); cold-reader authoring-context-leakage check (subagent with no authoring context flags ungroundable sentences; 'now'/'no longer'/'replaces' fixed before review-ready) → codebase.md § Checks as a named pre-review check; 'no CI merge gate — readiness is green probe eval + LGTM' → change-description.md CI-status line (already there, dedupe); acceptance-criteria-by-entryway + answer-key-is-executable-criteria → the entryway routing is v2 build/verify-your-work skill behavior (superseded); keep the one repo-specific sentence 'a skill's answer key is the executable form of its acceptance criteria' → codebase.md § Testing patterns; every-change-must-satisfy list → codebase.md § Conventions (merge with the same list arriving from implementing.md); rendered-HTML happy/empty/error states + both color schemes + bare-minimum-ux accessibility → environment.md § Driving the app & capturing evidence (the visual-artifact surface entry).

## [MIGRATE] docs/agents/refactoring.md
File retires (no v2 reader); earned lines move: behavior lock = probe eval (capture affected skill's verdicts before, identical scenario→verdict after, re-run ≥2 executors for model variance) → codebase.md § Testing patterns (the regression seam, alongside diagnosing-bugs.md's matching rule); script refactors = py_compile + same driven paths same output → codebase.md § Checks; refactor-must-not-turn-compose-by-name-into-file-dependency + copy-a-technique/extract-a-primitive → codebase.md § Conventions (cite AGENTS.md § Conventions as canonical, keep the one-line reviewer-facing reminder).

## [MIGRATE] docs/agents/change-reviewer.md
File retires — v2 adversarial-review/code-review own reviewer behavior, and code-review pulls repo standards from codebase.md. Line map: repo-specific review concerns (self-containment, stdlib-only scripts, agents/openai.yaml where Codex presentation matters, passing probe eval, judging rendered plan/prototype HTML for taste) → codebase.md § Conventions; authoring-context-leakage-in-shipped-text is a BLOCKER (quote sentence, name real recipient, require rewrite) → codebase.md § Conventions as a standing review standard; ~1000-line file-growth presumptive blocker → codebase.md § Conventions; exact-'LGTM' approval → platform.md § Change review (already bound, dedupe); styling-only reuse verdict exact phrase 'no product-code change; no recapture' + only-at-final-HEAD → evidence.md § What to capture Timing; open-every-cited-fixture-before-accepting and product-semantics-are-ruling-requests-not-review-edits → shipped v2 code-review/adversarial-review behavior (superseded, verify the v2 skills state them before dropping).

## [RETIRE] docs/agents/change-fixer.md
All shipped-default text with zero repo-specific additions (per audit); the v2 adversarial-review fixer subagent carries the same contract (reply per comment with SHA, reasoned non-fixes, re-prompt reviewer). Nothing to migrate.

## [KEEP] open PR #90 'Implement the SDLC lifecycle end to end' (branch sdlc-lifecycle, checked out)
Finish — this PR IS the v2 migration. All mount replacements, label renames, and playbook reconciles land as commits on this branch so the v1→v2 cutover is reviewable and reversible. Nothing may reset/clean the primary checkout while it is checked out.

## [MIGRATE] issue #80 ready-for-agent + branch 80-decouple-planning-from-run
Park immediately: remove ready-for-agent (or hold all builds) until the v2 mounts are installed — a backlog run started mid-migration would dispatch it under v1 semantics. Then re-groom under v2: it is plausibly superseded by PR #90 (which decouples planning from the AFK loop); if so, label superseded + 'superseded by #90' body line and harvest/delete the branch after checking it for unmerged content a human wants. See decisions.

## [MIGRATE] unmerged branches 84-interview-domain-modeling, codex/research-skill (+ worktree asher-skills-research-skill), codex/reconcile-installed-skills, codex/until-zero-skill (worktree manage-runway-skill)
State, not files — per-branch disposition after PR #90 merges: diff each against sdlc-lifecycle; content absorbed by the v2 work (research-skill and reconcile-installed-skills are the likely cases) → close/delete after harvest; content still live (84, until-zero) → park with a one-line note on its ticket and finish under v2. No branch is deleted before a human sees its unmerged diff. See decisions.

## [MIGRATE] worktree /Users/asher/Projects/asher-skills-worktrees/reconcile-consumers (DETACHED HEAD 2493ecb)
Rescue first: check for a dirty tree, commit or stash anything found, and pin the head with `git branch rescue/reconcile-consumers 2493ecb` before any cleanup — a detached head plus worktree removal is the one state where work is unrecoverable. Only then remove the worktree.

## [KEEP] worktrees 61-harness-specific-skills, goodwork-viz (on main), manage-runway-skill
Park through the migration: 61 and manage-runway hold live branches (dispositioned with the branch action above); goodwork-viz sits on main — verify clean, then it is free to remove any time. None block the v2 install; merge-changes cleanup handles them per environment.md teardown once their work closes.

## [KEEP] plans/ (22 plan HTML files) and evidence/ (per-issue dirs 1..84, sdlc-lifecycle, v2-probe-runs, v2-fix-verification)
Working-state artifacts of the loop per AGENTS.md § Layout, and the v2-era dirs are the migration's own proof. v2 evidence.md keeps evidence/<slug>/ as the storage contract — no move needed.

## [RETIRE] ~/.backlog/runs/asher-skills/{32,35} and ~/.backlog/state/asher-skills/{2-review-loop,8-to-spec}
v1 run-state for runs that are over; v2 keeps no run-state (tracker is the ledger). Archive or delete these asher-skills-scoped entries only after confirming no live run references them; ~/.backlog is shared with metis/pipelines/integrations-v2, so cleanup never touches sibling namespaces or ~/.backlog/handoffs/metis-*.

## [RETIRE] stray un-namespaced ~/.backlog/state/{1-extract-staffing,10-sprite-sheet-extractor,7-review} and ~/.backlog/runs/6
Pre-namespacing leftovers — retire only those provably from this repo's early runs (1-extract-staffing matches plans/1-extract-staffing.html; verify each by contents before deleting); anything not attributable stays, because the state root is shared across projects.

## [RETIRE] ~/.backlog/review-state/asher-skills/until-zero-skill-migration and ~/.backlog/reviews/asher-skills/{44-backlog-decomposition,73-plan,goodwork-viz}
Dead review-server state for settled reviews; the mechanism survives in the canonical serve-via-tailnet scripts. Reap paired tailscale handlers first (below), then delete; keep any whose review is genuinely still awaiting a verdict (until-zero pairs with the parked until-zero branch — retire only when that work closes).

## [RETIRE] tailscale serve handlers: /asher-skills/44/review→54984, /asher-skills/until-zero/review→50072, stale /review→8377
Reap per environment.md's own rule: `tailscale serve --set-path <path> off` for each dead handler (44 is closed; until-zero waits on its branch decision; /review:8377 is the documented stale handler — check dead, then off). The hub handler /asher-skills→8390 and the surface dir ~/.backlog/surface/asher-skills stay — v2 presenting still runs through serve-via-tailnet on this surface.

## [KEEP] ~/.backlog/surface/asher-skills/{registry.json,index.html} and ~/.backlog/handoffs/metis-backlog-run-2026-07-12.md
The surface is live v2 infrastructure (hub already empty of issue dirs); the metis handoff belongs to another repo sharing the state root — out of scope, never touched by this migration.

## [KEEP] skills/software-development/serve-via-tailnet/scripts/review-server.py and review-await.py
Canonical v2 machinery — the retired v1 review-loop's surviving mechanics live here (annotated mode), and the reconciled environment.md § Presenting and platform.md wakeups reference them by these paths.

## [MIGRATE] skills-lock.json
Rewritten by the atomic `npx skills add` for the complete v2 set (backlog, shape, build, adversarial-review, code-review, implement, tdd, diagnosing-bugs, verify-your-work, prove-your-work, merge-changes, to-spec, to-tickets, interview, domain-modeling, research, prototype, to-thread, to-subagent, watch-until, serve-via-tailnet, handoff, staffing, skill-loop) in ONE command; the writing-great-skills entry is hand-corrected (see decisions), never fed to a reinstall.

## DECISIONS NEEDED
- needs-spec vs needs-shaping: rename the live label to the v2 default (`gh label edit needs-spec --name needs-shaping`, clean — description already matches, #92 rides along) or keep needs-spec and record it as the bound alias in backlog-policy.md § Aliases. Either ends the current playbook/tracker disagreement; pick one.
- Staffing provider variant: variant-lock.json declares distinct Claude and Codex variants (different effective_hash), but .claude/skills/staffing is a symlink to the codex mount — physically impossible per the declaration. Should the reinstall compile a real separate Claude variant tree, or drop the variant declaration and keep the symlink? Requires knowing whether a Claude-specific staffing variant was ever intended.
- writing-great-skills provenance: adopt a source directory under skills/ (making the lockfile's local-source claim true) vs re-record it in the lockfile/external-dependencies as an upstream mattpocock/skills install. Until decided, it is excluded from any reinstall and its mount is hands-off.
- Issue #80 + branch 80-decouple-planning-from-run: is the decoupling fully delivered by PR #90 (→ superseded, close, harvest branch) or does residual scope survive into a v2-shaped ticket? A human should read the branch diff before closure.
- Parallelism verdict under v2 semantics: the v1 record says 'serialize-verification' but justifies it as 'user chose sequential' — v2 distinguishes these. If serialize-verification stands, lane mechanics need a lock path chosen (e.g. .backlog-lane.lock beside the primary checkout); if the real preference is sequential, record that instead. Also reconfirm the standing choice of no keep-awake (AFK reviews may find the machine asleep).
- verifying.md afterlife: retire it entirely (contents folded into codebase.md/environment.md per the migrate action) or keep a slim docs/agents/verifying.md as the optional 'check playbook' that v2 change-description.md § Checks-run points at. Either preserves content; the choice is about where builders look for the gate.
- Disposition per unmerged branch (84-interview-domain-modeling, codex/research-skill, codex/reconcile-installed-skills, codex/until-zero-skill): finish under v2, or close as absorbed by sdlc-lifecycle — each needs a human glance at its diff; the plan only guarantees none is deleted unread.

## MUST NOT LOSE
- The live-verified GitHub dependency verbs in platform.md: read blockers via `gh api .../issues/<n> --jq '.issue_dependencies_summary'` and write via numeric-id resolve + POST .../dependencies/blocked_by — earned by live verification; losing them regresses to task-list prose that backlog build cannot read.
- The 'never npx skills remove here' hazard and the one-atomic-add rule: with a local source path, remove deletes the canonical skill SOURCE under skills/, and sequential adds replace earlier selections — a naive CLI cleanup during this very migration would destroy the v2 sources it is installing.
- writing-great-skills' mount is the only working-tree copy (lockfile points at a nonexistent local source) — any mount wipe or lockfile-driven reinstall loses it.
- The tailnet serving facts in environment.md § Presenting: sandboxed macOS tailscale cannot serve file paths (hence http.server 8390 + `tailscale serve --set-path`), port 8377 is held by the stale pre-existing /review handler, the reap recipes, the bring-up/never-cycle-a-healthy-connection rule, and the standing 'always open the published URL locally' instruction — all earned by failed publishes.
- docs/agents/probe-evals.md wholesale: answer-key-before-runs, dual-executor contract, context-fidelity session split, citation requirement, and the canonical Tier 1/Tier 2 examples — it is the repo's entire testing substrate and 21 v2 references point at it.
- The staffing compiled-load byte budget (BASELINE_BYTES * 0.8 in test_global_apply.py) and 'provider trees are compiled by apply, never hand-edited' — losing either invites hand-edits that silently break the budget.
- The GitHub evidence-embed mechanics (same-origin ?raw=1 blobs, camo-proxied 404s on private repos, mechanical SHA/path/extension checks, re-pin-don't-plain-link) — now also in the v2 template, but the reconcile must not drop them from the repo playbook the skills actually read.
- backlog-policy.md's dispatch-metadata block requirement with 'missing fields are a grooming gap, never permission to infer', the research/draft routing boundary, and the never-silently-reset orphan rule (the branch may hold unmerged work).
- The runner traps: bare `==` in a zsh command line breaks the command; site/check.py's exit code masked if piped through tail in a && chain — each cost a debugging session.
- Whatever sits at DETACHED HEAD 2493ecb in the reconcile-consumers worktree — pin a rescue ref and check for a dirty tree before any worktree cleanup.


# integrations-v2

## [RETIRE] mount: backlog (v1)
Replaced by v2 backlog (skills/software-development/backlog) installed in one atomic `npx skills add` with the rest of the roster; v2's tracker-is-the-run-ledger design replaces run-state.py
Before removal, archive a copy of scripts/run-state.py beside .git/backlog/runs so the two run dirs stay readable forever (it is their only reader).

## [RETIRE] mount: plan (v1)
Superseded by v2 shape + to-spec + build flow (no same-name v2 skill); plan-skeleton.html dies with it once planning.md's earned content migrates; committed .plans/ history is kept untouched
See planning.md migrate action and the plan-convention decision.

## [RETIRE] mount: review-loop (v1)
Superseded by serve-via-tailnet's annotated-review mode (same review-server lineage, canonical copy now lives in that skill)
Drain first: run review-server.py --stop/--sweep on the 9 live state dirs and remove this repo's tailscale serve subpaths BEFORE deleting the mount — environment.md's recorded commands invoke the mount path. The LaunchAgent and ~/.backlog/surface hub stay (shared, machine-level).

## [RETIRE] mount: setup-asher-skills (v1)
Replaced by `npx skills add <repo> --skill <names...>` plus `backlog setup` for playbook install/reconcile; catalog.py/install.py/render-global.py have no consumer-side role in v2

## [RETIRE] mount: staffing (v1, with claude provider variant)
Replaced by v2 staffing (harness loads its global module + this repo's deltas)
The reinstall must recompile the declared claude provider variant and refresh .agents/asher-skills/variant-lock.json — .claude/skills/staffing is a real compiled directory, not a symlink; a symlink-normalizing cleanup would destroy the variant or invalidate the lock.

## [RETIRE] mount: diagnosing-bugs (v1)
Replaced by v2 diagnosing-bugs (refreshed same-name skill)

## [RETIRE] mount: prototype (v1)
Replaced by v2 prototype

## [RETIRE] mount: research (v1)
Replaced by v2 research

## [RETIRE] mount: tdd (mattpocock third-party)
Replaced by v2 tdd — v2 implement/build compose `tdd` by name, so the third-party copy would shadow the family version (see decision if Asher wants otherwise)

## [RETIRE] mount: diagnose (mattpocock third-party)
Superseded by v2 diagnosing-bugs; the environment.md § Tools reference to `diagnose` is rewritten during the playbook migration

## [RETIRE] mount: handoff (mattpocock third-party)
Replaced by v2 handoff (family version, composed by name in the v2 roster)

## [RETIRE] mount: greploop
No v2 successor and nothing in playbooks depends on it — removing it loses nothing

## [KEEP] mount: shadixfy
Asher-authored creative skill outside the SDLC supersede set; leave installed, refresh separately later against its restructured source path

## [KEEP] mount: agent-browser
Survives as the interactive browsing/diagnosis driver bound in environment.md; whether it remains a *verification* route is the open Playwright decision (v2 template demotes it from verification)

## [KEEP] mount: agentmail
OTP email driver bound in environment.md § Authenticating for testing — carries into the v2 auth section verbatim

## [KEEP] mount: btca-local
Domain tooling with btca.config.jsonc at repo root; untouched by this migration

## [KEEP] mount: convex
Referenced by environment.md § Tools; backfill its missing skills-lock.json entry so a future lockfile-driven reinstall cannot drop it

## [KEEP] mount: convex-best-practices
Domain mount, in lock; untouched

## [KEEP] mount: convex-realtime
Domain mount, in lock; untouched

## [KEEP] mount: humanizer
Domain mount, in lock; untouched

## [KEEP] mount: vercel-composition-patterns
Domain mount; backfill missing skills-lock.json entry

## [KEEP] mount: vercel-react-best-practices
Domain mount; backfill missing skills-lock.json entry

## [KEEP] mount: web-design-guidelines
Domain mount; backfill missing skills-lock.json entry

## [KEEP] mount: xlsx
Domain mount (full office scripts tree); backfill missing skills-lock.json entry

## [MIGRATE] v2 roster additions (no v1 counterpart)
Install build, shape, adversarial-review, code-review, implement, verify-your-work, prove-your-work, merge-changes, to-spec, to-tickets, interview, domain-modeling, to-thread, to-subagent, watch-until, serve-via-tailnet in the SAME single atomic `npx skills add` as the refreshed backlog/tdd/handoff/diagnosing-bugs/prototype/research/staffing
Sequential single-skill adds can replace earlier selections — one command, complete set.

## [MIGRATE] environment.md: branch naming / CI / preview-deploy lines
docs/agents/environment.md (v2) § Branching & deploys — branch codex/<issue>-<slug>, base/target main, preview deploy `pnpm --filter @workspace/backend deploy:vercel` + preview_seed:run as 'what a change request produces'
#242's empty preview CONVEX_DEPLOY_KEY / obsolete Convex team slug becomes the first Credential-preflight row (new v2 section) — the cheap live read that proves the deploy credential before work hits that gate. CI-runs-pnpm-check-but-no-branch-protection goes to codebase.md § Checks.

## [MIGRATE] environment.md: local-dev lines (services, hostnames, dotenvx, pinned pnpm)
environment.md (v2) § Running locally — services (portless app/email/ui.onboardings, convex dev, Ladle), *.localhost hostnames, `dotenvx run --`, pinned pnpm@10.4.1 purge hazard
v2's new headless-stack contract requires recording detached start + log + audited teardown — author this at setup; it was implicit in v1.

## [MIGRATE] environment.md: worktree-isolation lines (setup-worktree.mjs, dev:isolated, singleton audit table)
environment.md (v2) § Worktree isolation — regime local-isolatable; `node scripts/setup-worktree.mjs`; dev:isolated / dev:seed:isolated / worktree:env; cold-start 30s-window caveat; generated state (.env.worktree, .worktree/convex-home, .worktree/portless); the effect-verified 2026-07-14 shared-singleton table (Convex/ports/env isolatable; Clerk dev instance NOT; AgentMail inbox NOT; dev:reset targets exclusive) verbatim
v2 adds the standing parent-.git lock row — append it. This table is the crown jewel: not regenerable without re-running the two-worktree live audit.

## [MIGRATE] environment.md: seed lines
environment.md (v2) § Seed data — dev:seed dry-run/apply, dev:reset-and-seed, reset-deletes-ALL-Clerk-orgs warning, seed contents (Dunn Harland/Demo Dealer/Demo System Owner, 12 stage projects), isolated seed refuses live keys, NO verified safe cleanup for 'Dunn Harland [<suffix>]' smoke orgs — leave them
v2's new drive-to-feature path is authored here from diagnosing-bugs.md's dev:isolated recipe (printed worktree URL, seeded namespace).

## [MIGRATE] environment.md: auth lines
environment.md (v2) § Authenticating for testing — Clerk JWTs trusted by Convex, public routes /sign-in + /invitations, agentmail onboardings-dev@agentmail.to OTP path (consume programmatically, never print), do-NOT-trust-initially-active-org trap
v2 adds a session-reuse row (mint once, persist browser storage state) — author it; v1 re-authenticated per run.

## [MIGRATE] environment.md: verification-data and fixture-hygiene lines
environment.md (v2) § Verification data — VERIFY-<issue>-<purpose> naming, [<worktree-suffix>] for shared-Clerk orgs, never run shared reset as cleanup, never share mutable scratch across issues
v2's new per-ticket-disposable-stores row: worktree-local Convex deployment only; shared Clerk instance, AgentMail inbox, and dev:reset targets sit explicitly OUTSIDE the destructive line.

## [MIGRATE] environment.md: browser/capture lines (agent-browser sessions, Computer Use, evidence formats)
environment.md (v2) § Driving the app & capturing evidence — per-worktree isolated named sessions, ChatGPT-in-Chrome only on explicit request, Computer Use per-task authorization never carried forward, delete-the-auth-recording + review-captures-for-secrets rules
Driver binding itself is the open Playwright-vs-agent-browser decision; whichever wins, these hygiene rules carry.

## [MIGRATE] environment.md: review-surface lines (LaunchAgent, tailscale serve, publish/stop/sweep/await commands)
environment.md (v2) § Presenting to the human, rewritten by serve-via-tailnet setup — durable facts carry (root https://ashers-macbook-pro.tail045dd5.ts.net/review, surface dir ~/.backlog/surface/integrations-v2, port-8377 LaunchAgent, Funnel-stays-off, `tailscale status` preflight, symlink publish form); the review-loop mount-path commands (review-server.py invocation, review-await exit codes 0/3/10/124, stop/sweep) retire with the mount, replaced by serve-via-tailnet's annotated-mode equivalents

## [MIGRATE] environment.md: parallelism lines
environment.md (v2) § Parallelism verdict — serialize-verification, forcing rows named (Clerk + AgentMail), serialized exception lane (ALL isolated startups/seeds serialize because dev:isolated auto-seeds Clerk; concurrent after ready+authenticated)
v2 replaces 'orchestrator owns the lane' prose with explicit lane mechanics: author the lock path (e.g. .backlog-lane.lock beside the primary checkout), atomic-mkdir acquire, release-after-cleanup-proof, stale horizon.

## [MIGRATE] platform.md: tracker lines
platform.md (v2) § Tracker — binding github dunnharland/integrations-v2; gh issue view FAILS (deprecated Projects-classic GraphQL, verified 2026-07-11) so read via `gh api repos/.../issues/<n>` (+/comments); blocked_by read (`.../dependencies/blocked_by`, exercised 2026-07-14) and write (resolve numeric id via --jq '.id', POST/DELETE -F issue_id) verbatim; Closes #<n> close-on-merge

## [MIGRATE] platform.md: change-review lines
platform.md (v2) § Change review — gh pr view/edit FAIL, edit via `gh api --method PATCH .../pulls/<n> --input -`; gh pr list/checks work; approval = exact 'LGTM' comment (from change-reviewer.md); merge = human `gh pr merge <n> --squash` (house policy, NOT platform-enforced); --delete-branch fails while a worktree holds the local branch — remove worktrees first

## [MIGRATE] platform.md: version-control lines
platform.md (v2) § Version control — `git worktree add <path> -b codex/<issue>-<slug> origin/main`; pinned-SHA semantics (rebase/force-push orphans pins, re-pin branch-head SHA after any rewrite); stacked-PR post-squash reconciliation recipe (merge origin/main, one-sided conflicts keep both additions, pnpm install + pnpm check before push, stacked merges strictly after base)

## [MIGRATE] platform.md: harness lines
platform.md (v2) § Harness — Codex native agent threads; cross-harness only via named native wrapper subagent (external_claude_<role>) staffed at the cheapest eligible native model, babysit/relay only
Extend with v2's external-worker contract: wrapper tees raw output to a file and captures the CLI's resumable session id; record directional reachability + successor per direction.

## [MIGRATE] backlog-policy.md: readiness label bindings
backlog-policy.md (v2) § Label roles — ready-for-agent, ready-for-human (also abort target for verify caps/environment blockers), needs-info bind unchanged; in-flight binds to the `building` role via the label rename; claim comment (branch + date, GitHub has no native claim field) carries into v2's attributed-claims rule (claim posted by the runner's own tracker actor); new shaping/needs-shaping rows bind the created labels

## [MIGRATE] backlog-policy.md: work-type labels + tie-break rule
backlog-policy.md (v2) § Work-type — bug→diagnose, enhancement→implement (v1's plan→implement: shaping now happens upstream in groom), refactor, research (dossier under research/<slug>/), draft (judgment-terminal, done = human review verdict, artifact kept); tie-break sources-terminal→research / voice-fit→draft / behavior-change keeps code type matches v2's shipped boundary text — confirm, don't duplicate

## [MIGRATE] backlog-policy.md: dispatch metadata block
backlog-policy.md (v2) § Dispatch metadata — Surface / Required capabilities / Coordination (routine|orchestrator-required) / Reason / Known uncertainty as a stable Dispatch: block; missing metadata → skip, never infer
v2 adds a required `route: direct` field for enhancements (why strategic decisions are settled/delegated) — grooming gains this field.

## [MIGRATE] backlog-policy.md: exclusions, neutral labels, dependencies, in-flight hygiene
backlog-policy.md (v2) § Exclusion (duplicate/invalid/wontfix; superseded → wontfix + linking comment), § Neutral (codex, design, documentation, good first issue, help wanted, question), § Dependencies (native blocked_by via platform.md; skip while any blocker open), § Building hygiene (optimistic claim, re-read immediately before marking, orphan = branch gone or quiet past 7 days → human-confirmed reset only, never silent)

## [MIGRATE] TYPESCRIPT.md
codebase.md § Conventions (language idioms) — types over interfaces, strippable TS/no enums, as-casts only with comment, T[]/readonly T[], attempt/attemptAsync from es-toolkit over try-catch, early returns, kebab-case filenames, no non-ASCII punctuation in output; delete the file after fold-in

## [MIGRATE] MODULES.md
codebase.md § Conventions (import/module rules) — no barrel files anywhere, import directly from source; delete the file after fold-in

## [KEEP] I18N.md
Kept as a standalone repo-owned doc (too large and load-bearing for one codebase.md bullet); codebase.md § Conventions gains the newcomer traps (en.json canonical + request-time deep-merge fallback, namespace-per-screen/no common grab-bag, ICU + identical placeholders, logical Tailwind utilities ms-/me-/ps-/pe- in i18n-touched code, packages/ui stays locale-agnostic, messages.test.ts gate via pnpm --filter web test) plus a pointer to I18N.md
The enumerated hardcoded en-US call sites and the translation-pass backlog are work, not conventions — ticketize them during the first v2 groom.

## [MIGRATE] verifying.md: check commands + '--' trap + red baseline
codebase.md § Checks — full gate `pnpm check` (same as CI's check.yml; no required status checks, main NOT branch-protected — house policy is disclose + green before human merge); package filters (web/@workspace/backend/ui/emails check, lint, typecheck, format, build, lint:ws); invocation trap: NEVER insert '--' in `pnpm --filter <pkg> test <path>` — it runs the full suite (615/478 tests); recorded red baseline as of 2026-07-14: TS2307 missing 'mermaid' from apps/web/lib/block-document-export/mermaid-image.ts
Any migration smoke test gating on green pnpm check will falsely fail without the baseline carried. Also file a ticket to actually fix the mermaid baseline.

## [MIGRATE] verifying.md: evidence-bar and criterion lines
evidence.md (v2) § What to capture — repo tunings beyond the shipped baseline: email change = rendered/captured preview without secrets; seed/reset/deploy = dry-run or safe-env proof with destructive commands called out; auth/org/role/invitation/email/data-export surfaces need explicit permission or side-effect criteria; each claimed criterion names the actual runtime seam and cited tests are opened to confirm coverage

## [MIGRATE] implementing.md
Split: test locations (web under apps/web, backend under packages/backend/convex + /mcp, Vitest via Turbo/pnpm filters) → codebase.md § Testing patterns; commit style (concise imperative, Conventional Commits NOT enforced), never-commit list (.env values, backups, .next, .turbo, caches, node_modules), pnpm/pnpm dlx only, Convex filename charset rule, nuqs for URL-shareable state, autosave + optimistic-update idiom → codebase.md § Conventions; under-specified issue → needs-info (never guess) → backlog-policy.md § Label roles
Its generic test-first guidance is superseded by the v2 tdd skill — drop.

## [RETIRE] planning.md
Flow superseded by shape → to-spec (spec on the ticket, diagram first, blessed in the shaping thread before ready-for-agent); the plan-threshold list (multi-subsystem, data model/authz/migration, seeded-data/auth/email/preview behavior, high-risk workflow state, >~1 day) survives as grooming guidance in backlog-policy.md § Readiness decision; hash-bound approval + per-annotation ledger dispositions live on in serve-via-tailnet's annotated mode; the 29 committed .plans/ files stay untouched (SHA-pinned from PR bodies)

## [MIGRATE] evidence.md (v1 playbook)
evidence.md (v2) — the shipped template already carries this repo's earned contract verbatim (blob/<sha>?raw=1 embed form, raw.githubusercontent 404s on private repos, mechanical checks via gh api commits + git cat-file -e, PNG/JPEG/GIF never MP4, two-pass-palette GIF recipe, c<criterion>- naming, orphaned-SHA re-pin rule) — reconcile, don't duplicate; repo-specific carries: probe/dry-run transcripts are NOT evidence here, and the styling-only reuse clause requiring the reviewer's verbatim 'no product-code change; no recapture' at final reviewed HEAD → § What to capture (timing)

## [MIGRATE] change-description.md (v1 playbook)
change-description.md (v2) § This repo — work-type on the close line, scope-discovery in Summary, CI status must disclose red/pending AND the lack of branch protection (never describe the workflow as platform-enforced), workarounds framed as environment gaps vs product issues, research work-type swaps Evidence for a Research-dossier section (canonical dossier link, as-of boundary, claim-audit result)
The gh-pr-edit-fails PATCH workaround dedupes into platform.md § Change review — change-description points there.

## [MIGRATE] change-reviewer.md
Repo scrutiny list (Clerk-claims + Convex access checks for authz/tenant isolation; schema/validator/generated-API compatibility; collaboration + optimistic-update behavior; email/invitation/webhook side effects; a11y/responsive/design-system/no-overlap; direct imports, pnpm-only, Convex filename rules, no secret leakage) and the ~1000-line-file presumptive-decomposition blocker → codebase.md, as a repo-owned § Review scrutiny section (setup reconciles, never overwrites); exact-'LGTM' → platform.md § Change review; styling-verdict verbatim clause → evidence.md
The Reviewer/Fixer choreography (ruling requests to the coordinator, re-review new HEAD) is superseded by the v2 adversarial-review skill.

## [MIGRATE] change-fixer.md
Targeted-checks-then-pnpm-check with disclosed pre-existing baseline, and markdown-only-fixes-need-no-pnpm-check-unless-PR-changed-code → codebase.md § Checks
Commit-and-push-before-handback / reply-per-comment-with-SHA / escalate-rulings mechanics are superseded by the v2 adversarial-review fixer role.

## [MIGRATE] diagnosing-bugs.md (playbook)
Repo seams → codebase.md § Testing patterns: Vitest layout + no-'--' trap (dedupe with § Checks), Convex investigation layers (web caller → generated API → validator/schema → mutation/query/action logic → Clerk/Convex auth state, + packages/backend/mcp when the failure crosses MCP), no recorded logging/debugger/profiler entry points, no recorded flaky tests, shared Clerk tenant as the standing collision hazard; the app-visible-bug recipe (dev:isolated, serialize startup/auth, drive printed worktree URL, record URL/account/namespace/behavior) → environment.md § Seed data drive-to-feature path
The six-phase process is superseded by the v2 diagnosing-bugs skill.

## [MIGRATE] prototyping.md
Repo bindings → codebase.md § Conventions: pnpm scripts + Turbo registration in the owning package's package.json, App Router under apps/web, shared UI in packages/ui with Ladle at ui.onboardings.localhost, UI variants must use @workspace/ui + existing design-system conventions
The prototype process (throwaway artifact, winner marked) is superseded by the v2 prototype skill.

## [MIGRATE] researching.md
Dossier root research/<slug>/ + scratch-in-temp-uncommitted + stays-out-of-evidence/ → backlog-policy.md § Work-type (research row); serialize rate-limited/tenant-mutating sources → environment.md § Parallelism verdict (serialized exception lane); primary sources = official integration-provider docs/APIs via authenticated connectors or browser sessions → environment.md § Driving the app (supporting tools)
The dossier discipline itself is the v2 research skill.

## [MIGRATE] refactoring.md
Preserve-list (public behavior, URL state, authz, generated API contracts, seed/reset behavior), never-mix-behavior-and-structure-in-one-commit, locked-test-must-change = behavior change → stop for product ruling, no-testable-seam → seam creation is the first separate minimal refactor → codebase.md § Conventions; Convex generated API (_generated tree, regeneration needs convex dev/codegen against a schema) → codebase.md § Generated artifacts (new v2 section)
Characterization-test mechanics are superseded by v2 implement/tdd on the refactor branch.

## [RENAME] label: in-flight (6 open claimed issues)
in-flight → building: `gh api -X PATCH repos/dunnharland/integrations-v2/labels/in-flight -f new_name=building`
In-place rename keeps the label attached to #240 #241 #243 #244 #245 #250 and leaves their claim comments (branch + date) intact — no per-issue relabeling, no orphaned claims for groom's orphan sweep.

## [RENAME] labels: needs-shaping + shaping (new v2 roles)
Additions: `gh api -X POST repos/dunnharland/integrations-v2/labels -f name=needs-shaping -f color=<hex> -f description='parked for strategic shaping'` and the same for `shaping` — created with user consent per backlog setup

## [RETIRE] label: needs-triage
Nothing lost: 0 open issues carry it; v2 expresses un-triaged as no-readiness-label (groom target) and strategic parking as needs-shaping — delete the label or demote it to neutral (minor decision)

## [KEEP] labels: ready-for-agent, ready-for-human, needs-info; work-type bug/enhancement/refactor/research/draft; exclusions duplicate/invalid/wontfix; neutrals codex/design/documentation/good-first-issue/help-wanted/question
Bind as-is in the v2 backlog-policy.md — names already match v2 defaults; superseded-→-wontfix-plus-linking-comment convention carries; neutrals stay neutral

## [KEEP] state: 7 open PRs #257-#263 and their 6 in-flight + 1 ready-for-human tickets
Disposition: FINISH under current semantics, do not relabel/reset/re-dispatch — human squash-merges the ready ones (#257 LGTM x2, #259 LGTM), converges the rest, and unblocks #242 (obsolete Convex team slug / empty preview CONVEX_DEPLOY_KEY) and #250 (missing reachable Clerk test-org fixture) per the run handoff's exact steps; Closes #<n> linkage closes the issues at merge; the label rename keeps their claims valid meanwhile

## [KEEP] state: 7 live worktrees under /Users/asher/Projects/integrations-v2-worktrees
Untouched until each backing PR merges — no git worktree prune/remove, no branch deletion (also: --delete-branch fails while the worktree exists); after merge, v2 merge-changes (or manual) removes worktree before branch

## [MIGRATE] state: .git/backlog/runs (2 run dirs, status.json, board.md, handoff.md, 398 events)
The live blocker knowledge in handoff.md — #242's Convex-deploy-key unblock steps and #250's Clerk-fixture unblock steps — is posted as comments on those issues (the tracker is v2's run ledger, so this is where a v2 resume looks); then archive the run dirs together with a copy of run-state.py so they stay readable
The v1 'rerun backlog audited-resume' protocol becomes moot once the 7 PRs drain; v2 build reconstructs from claim/outcome comments.

## [MIGRATE] state: ~/.backlog/review-state/integrations-v2 (9 review-loop state dirs)
Drain before the review-loop mount is removed: `review-server.py --sweep` / `--stop` each, `tailscale serve --set-path ... off` per handler; archive the state dirs (their approval ledgers back the committed plans' approvals); future reviews run through serve-via-tailnet's annotated mode

## [KEEP] state: ~/.backlog/surface hub + LaunchAgent com.asher.backlog-surface + tailscale serve /review
Machine-level and shared with asher-skills, metis, and pipelines — never torn down for one repo's migration; serve-via-tailnet's setup records this repo's surface config (root path, surface dir, publish/proxy commands) into environment.md § Presenting

## [KEEP] state: .plans/ (29 tracked plan files) + plans/152-real-timeline-dates.html
SHA-pinned from open and merged PR bodies — deleting or rewriting history 404s them; kept as history; new work follows whichever plan convention the open decision lands on

## [KEEP] state: evidence/ (32 committed per-issue dirs)
PR bodies embed them via blob/<sha>?raw=1 — no history rewrite, no pruning, ever; the constraint itself migrates into evidence.md's re-pin rule

## [KEEP] state: ~27 unmerged non-worktree branches (codex/195-tracker-three-axis 16-ahead, etc.)
Disposition: PARK — ahead-counts are inflated by squash-merge history, but each branch needs an explicit merged-or-orphaned judgment before deletion; file one groom ticket to adjudicate the list; not a migration blocker

## [KEEP] state: research/ dossier root + backups/convex-prod-with-files-20260616-132914.zip
research/ carries over as the v2 research work-type's dossier root; the Convex production backup is never touched by any cleanup step

## [MIGRATE] script: .agents/skills/backlog/scripts/run-state.py
Copy out of the mount (e.g. beside .git/backlog/runs or under docs/agents/archive/) before the mount swap — it is the only reader of the run state; v2 has no successor because the tracker replaces run-state entirely

## [RETIRE] scripts: review-loop review-server.py + review-await.py
Replaced by serve-via-tailnet's annotated-review machinery (same lineage — the canonical review-server now ships with that skill); used one last time to drain/sweep the 9 state dirs before the mount is deleted

## [RETIRE] scripts: setup-asher-skills install.py / catalog.py / render-global.py
Replaced by `npx skills add` (install) and `backlog setup` (playbook reconcile); no consumer-side catalog rendering exists in v2

## [RETIRE] script: staffing/scripts/render-global.py
v2 staffing owns the global-module render for both harnesses; goes with the staffing mount swap

## [RETIRE] script: diagnose/scripts/hitl-loop.template.sh
Goes with the diagnose mount; v2 diagnosing-bugs ships its own red-capable loop

## [KEEP] machine: ~/Library/LaunchAgents/com.asher.backlog-surface.plist
Shared machine infrastructure serving four repos' review surfaces — reused by serve-via-tailnet, not this repo's to modify

## DECISIONS NEEDED
- Verification browser driver: v2's environment template makes Playwright-driving-Chrome the default verification route and explicitly demotes agent-browser ('not a verification route'); this repo has no Playwright e2e suite and every recorded evidence recipe uses agent-browser with per-worktree sessions. Adopt Playwright (seed an e2e/ dir, rewrite § Driving the app, keep agent-browser for interactive diagnosis only) or record agent-browser as an explicit named deviation from the v2 default?
- Migration timing: drain-first (wait for the 7 open PRs #257-#263 to merge before swapping the backlog and review-loop mounts — clean, but gated on the human unblocking #242's Convex deploy key and #250's Clerk fixture) versus swap-now (migrate mounts immediately and finish the open reviews with the archived review-server/run-state copies). Drain-first is safer; swap-now only needs the drain steps for review-loop done first.
- Plan artifact convention going forward: keep committed .plans/<issue>-<slug>.html (self-contained HTML, ac-N anchors, SHA-pinned from PR bodies) for new enhancements, or move to v2's spec-on-ticket via to-spec (diagram first, blessed in the shaping thread)? Affects how change-description.md's 'Plan' section binds. Existing .plans/ files stay either way.
- needs-triage label: delete (0 open issues carry it) or demote to neutral? Trivial, but backlog setup will ask.
- Third-party tdd and handoff mounts: the recommendation is replace-with-v2 (the v2 pipeline composes tdd and handoff by name, so the mattpocock copies would shadow the family versions), but the audit flagged both as decide-replace-vs-keep — confirm before the atomic install.
- Whether to ticketize the I18N translation-pass backlog (8 screens still hardcoded English, 8 enumerated en-US call sites, unlocalized emails) during the first v2 groom, or leave it inside the kept I18N.md doc.

## MUST NOT LOSE
- The effect-verified (2026-07-14, two simultaneous worktrees) shared-singleton audit: Clerk dev instance NOT isolatable (serialize auth mutation, suffix-namespaced orgs), AgentMail inbox NOT isolatable (serialize OTP, match fresh message), dev:reset targets exclusive — plus the serialized-lane rule that ALL isolated startups/seeds serialize because dev:isolated auto-seeds Clerk. Not regenerable without re-running live audits.
- The destructive-command lines: pnpm dev:reset deletes ALL Clerk orgs in the test instance, and there is NO verified safe cleanup for the suffix-namespaced 'Dunn Harland [<suffix>]' smoke orgs — leave them. Losing these invites a shared-tenant wipe.
- platform.md's verified gh workarounds: gh issue view / gh pr view / gh pr edit all FAIL on this repo (deprecated Projects-classic GraphQL) — REST verbs via gh api only, including the exercised blocked_by read/write pair and the PATCH-pulls body edit.
- The '--' targeted-test trap (inserting -- flips a filtered run into the full 615/478-test suite) and the recorded red pnpm check baseline (TS2307 missing 'mermaid') — a v2 setup smoke that gates on green pnpm check falsely fails without it.
- .git/backlog/runs handoff.md's exact unblock steps for #242 (obsolete Convex team slug / empty preview CONVEX_DEPLOY_KEY) and #250 (missing reachable Clerk test-org fixture) — must land as issue comments before the backlog mount (and run-state.py, the runs' only reader) is swapped.
- The evidence/plan pinning constraint: 32 evidence dirs and 29 .plans files are blob/<sha>?raw=1- and SHA-pinned from PR bodies — any history rewrite or 'cleanup' deletion 404s every rendered artifact on the 7 open PRs.
- The 7 live worktrees backing open PRs #257-#263: no prune, no branch deletion, no dev:reset in them, until the human squash-merges.
- The staffing claude provider variant: .claude/skills/staffing is a real compiled directory recorded in .agents/asher-skills/variant-lock.json — the v2 reinstall must recompile the variant, and any symlink-normalizing cleanup destroys it.
- The five lock-less mounts (convex, vercel-composition-patterns, vercel-react-best-practices, web-design-guidelines, xlsx): a lockfile-authoritative reinstall silently drops them; backfill skills-lock.json before any bulk operation.
- The CI-disclosure rule: GitHub Actions runs pnpm check but main has NO branch protection — PR bodies must disclose CI status and never describe the workflow as platform-enforced.


# pipelines

## [RETIRE] mount: backlog (v1)
Replaced by v2 backlog (skills/software-development/backlog) via one atomic npx skills add. Run supervision moves to tracker-as-ledger (claim/outcome comments, SKILL.md § build), so nothing run-state.py did is needed going forward; historical run records stay in .git/backlog/ untouched.
Reinstall only after the live review-loop process is resolved and uncommitted lockfile changes are committed.

## [RETIRE] mount: plan (v1)
Superseded by v2 to-spec + shape (spec on the ticket, diagram first). Earned planning.md content migrates separately (see planning.md rows); committed plans/*.html stay valid history.

## [RETIRE] mount: review-loop (v1)
Machinery lives on in serve-via-tailnet's annotated mode (canonical review-server.py per asher-skills copy-a-technique convention) — approve/nits/request-changes verdicts survive. Retire ONLY after PID 62436's round-2 verdict lands or a deliberate `review-server.py --stop` + `tailscale serve --set-path /pipelines/licon-pss-test/review off`.
Deleting the mount while PID 62436 runs from it kills a live awaited review — hard sequencing constraint.

## [RETIRE] mount: setup-asher-skills (v1)
Superseded by the v2 install flow (npx skills add from asher-skills). Uninstall BY HAND (rm .agents/skills/setup-asher-skills, the .claude symlink, the lock entry) — never `npx skills remove` in this repo (local-source lock entries make it destructive).

## [MIGRATE] mount: staffing (v1, declared provider variant)
Refreshed v2 staffing, reinstalled preserving the provider-variant contract: recompiled real dir at .claude/skills/staffing plus updated .agents/asher-skills/variant-lock.json — never flattened to a symlink, never left with a stale variant-lock.

## [RETIRE] mount: research (v1)
Refreshed v2 research replaces it 1:1; repo-earned researching.md lines migrate to backlog-policy.md and environment.md (see playbook rows).

## [RETIRE] mount: prototype (v1)
Refreshed v2 prototype replaces it; prototyping.md's repo patterns migrate to codebase.md § Conventions.

## [RETIRE] mount: diagnosing-bugs (v1)
Refreshed v2 diagnosing-bugs replaces it; the repo playbook's earned diagnosis facts migrate to codebase.md and environment.md (see playbook rows).

## [RETIRE] mount: tdd (v1, mattpocock provenance)
v2 asher-authored tdd replaces it. The mattpocock copy is recoverable from git history and its upstream; credits live in the v2 skill's README per repo convention.

## [RETIRE] mount: improve (orphan, shadcn/MIT)
v2 roster retires it; no playbook references it; no lock entry so hand-delete both mount paths. Recoverable from git history and its upstream — nothing unique lost.

## [RETIRE] mount: greploop (third-party greptileai)
Retired in the v2 roster; no playbook references it. Mount is git-tracked, so deletion is recoverable from history plus the greptileai upstream.
If Asher still uses it ad hoc, redeclare as an external requirement instead — flagged in decisions.

## [KEEP] mount: uncodixfy (third-party, load-bearing)
Retired from the v2 family but kept in this repo as a declared external requirement (external-dependencies.lock.json entry with provenance) because frontend work depends on it. Its invocation pointer moves from implementing.md/prototyping.md into codebase.md § Conventions (frontend work: load uncodixfy, bare-minimum-ux, shadcn, docs/agents/frontend.md).
Deleting it without rewriting those references leaves dead pointers; third-party source means deletion is not recoverable from asher-skills.

## [KEEP] mount: impeccable (undeclared, two independent real dirs)
Freeze both copies until dispositioned: diff .agents/skills/impeccable against .claude/skills/impeccable; if identical, normalize to primary + symlink and either declare in the lock or delete after a provenance check. No symlink-normalization pass may touch it before the diff.
Genuinely open — see decisions.

## [KEEP] mount: qa-user-journeys (repo-earned, no lock entry)
Exists nowhere else; add a provenance/lock record so no lockfile-driven sweep can destroy it. Its docs/qa/journeys content becomes the drive-to-feature path in v2 environment.md § Seed data.

## [KEEP] mount: sentry-cli (repo-earned, no lock entry)
Repo-specific Sentry/Railway/PR #194 observability skill, exists nowhere else; add a provenance/lock record. Referenced from codebase.md § Conventions observability pointers after migration.

## [KEEP] mount: ask-syncron-parts-planning (untracked mount + uncommitted lock entry)
Commit the untracked .agents/skills/ask-syncron-parts-planning dir and its skills-lock.json entry BEFORE any migration git operation — it currently exists only as uncommitted work.

## [KEEP] mount: bare-minimum-ux (creative family)
Out of SDLC migration scope; remains a named sibling for frontend work via the rewritten codebase.md § Conventions pointer.

## [KEEP] mount: agent-browser
Mount stays (exploration/QA), but its 'primary verification route' role is contested: v2 environment.md § Driving the app rules agent-browser out as a verification route in favor of Playwright-driving-Chrome. Final role set by the browser-policy decision.
See decisions — do not silently copy either the v2 default or the v1 policy.

## [KEEP] mount: agentmail
Feeds v2 environment.md § Authenticating for testing (OTP/invite flows, AGENTMAIL_API_KEY + AGENT_EMAIL).

## [KEEP] mounts: better-auth-best-practices, better-auth-security-best-practices, create-auth-skill, email-and-password-best-practices, organization-best-practices, two-factor-authentication-best-practices
Third-party domain skills (better-auth/skills), untouched by the SDLC migration; lock entries already valid.

## [KEEP] mounts: elysiajs, resend, tanstack-form, tanstack-query, tanstack-virtual, use-railway, vercel-cli
Third-party domain skills with valid upstream lock entries; untouched by the migration. use-railway's db-analysis scripts stay with the mount.

## [KEEP] mount: database-migrations (local-source lock oddity)
Mount stays (implementing.md requires it before migrations; the pointer moves to codebase.md § Generated artifacts). Repair the lock entry: source is the repo itself with an empty-string sha256 — rebind to the true upstream or declare it repo-owned so hash checks mean something and `npx skills remove` can never resolve it to repo content.

## [RETIRE] lock entry: db-migrations (ghost — no mount)
Delete the lock line only. No directory exists on disk and the hash is the empty string, so removing the entry loses nothing.

## [KEEP] mount: shadcn (local-source lock oddity)
Required for shadcn/base-ui work (pointer moves to codebase.md § Conventions). Repair the local-source lock entry the same way as database-migrations.

## [MIGRATE] playbook backlog-policy.md: label bindings (1:1, no aliases) + neutral list + native in-review/closed
v2 docs/agents/backlog-policy.md § Label roles (bind ready-for-agent/ready-for-human/needs-info 1:1; in-flight becomes building; list documentation/good-first-issue/help-wanted/question/needs-triage/design/observability/rfq/admin under § Neutral; the native-GitHub in-review/closed note is now template text).

## [MIGRATE] playbook backlog-policy.md: ready-for-agent requires exactly one work-type; Dispatch: block (Surface/Coordination/reason); missing metadata = skip
v2 backlog-policy.md § Dispatch metadata — the template now carries the GitHub 'stable Dispatch: block' encoding and skip-on-missing rule; record the repo's exact block format there. Add the v2-new route:direct line requirement for enhancements as a grooming delta.

## [MIGRATE] playbook backlog-policy.md: in-flight set at dispatch + branch/date comment; ready-for-human as abort target with blocker commented; draft/research semantics + dossier root research/<slug>/
v2 backlog-policy.md § Label roles — the building, ready-for-human, draft, and research rows carry these natively; add research/<slug>/ as the repo's dossier root on the research row.

## [MIGRATE] playbook backlog-policy.md: blocked_by read via list endpoint with X-GitHub-Api-Version: 2026-03-10, write via numeric id POST, and the 2026-07-14 stale .issue_dependencies_summary GOTCHA
v2 docs/agents/platform.md § Tracker (blocked-by verbs) — REPLACING the v2 template's default read, which is exactly the known-broken `.issue_dependencies_summary` path; backlog-policy.md § Dependencies points at platform.md as the single home, collapsing the v1 duplication.
Copying the template verbatim would reintroduce a live-probed failure. Crown jewel.

## [MIGRATE] playbook backlog-policy.md: orphan sweep — dead/quiet branch = corpse, surface to human, never silently reset
v2 backlog-policy.md § Building hygiene — template carries the mechanism; set the quiet horizon to this repo's earned 7 days.

## [MIGRATE] playbook backlog-policy.md: Syncron inbound batch explicitness in issues; DB enum/domain-state changes require a bun-run-check type-safety acceptance criterion; UI-heavy work requires frontend.md + local UI skills
v2 backlog-policy.md § Readiness decision (Syncron batch fields and the type-safety criterion as repo readiness bars) and § Dispatch metadata (surface: ui implies the frontend playbook + UI skill loads, pointer into codebase.md § Conventions).

## [MIGRATE] playbook environment.md: base branch, codex/<n>-<slug> naming, PR target, CI command, no preview deploys, Railway deploy doc
v2 docs/agents/environment.md § Branching & deploys — plus fill the v2-new deploy-facts and credential-preflight rows (Railway per docs/deploy/railway.md with confirm-before-assuming-auto-deploy; cheap live reads for gh auth and Railway token).

## [MIGRATE] playbook environment.md: bun run dev stack composition, *.localhost:1355 URLs, db:up/bucket:up/sftp-egress:up/reset:*/db:migrate commands
v2 environment.md § Running locally — plus satisfy the v2-new headless contract: record the detached-with-log start form of bun run dev and its stop/teardown audit, verified headlessly at setup.

## [MIGRATE] playbook environment.md: worktree isolation (worktree-env.ts family, COMPOSE_PROJECT_NAME derivation, ports 21000-31000, per-worktree hostnames/env), cleanup/reap commands, PIPELINES_WORKTREE_ISOLATION=off
v2 environment.md § Worktree isolation — regime: local-isolatable; bring-up via scripts/setup-worktree.sh, teardown via scripts/cleanup-worktree.sh + bun run reset:worktree-stacks; add the v2-new parent-.git lock-contention row.

## [MIGRATE] playbook environment.md: shared port-1355 proxy (intentional) and non-isolatable Railway/Resend/AgentMail/OpenAI/PostHog/Sentry/customer-SFTP
v2 environment.md § Worktree isolation shared-singleton table — one row each, isolatable-yes for the proxy (per-worktree subdomains), isolatable-no for the cloud/SFTP singletons; these rows also justify the serialized exception lane in § Parallelism verdict.

## [MIGRATE] playbook environment.md: explicit-QA-fixtures-only seeding, qa:seed-rfq-comparison guards, qa:generate-syncron-inbound-batch, journeys in docs/qa/journeys/
v2 environment.md § Seed data — including the v2-new drive-to-feature path row, seeded from docs/qa/journeys (the qa-user-journeys skill's content).

## [MIGRATE] playbook environment.md: Better Auth email OTP, AUTH_EMAIL_PROVIDER=noop console OTPs, PLATFORM_ADMIN_EMAILS, agentmail path; missing AGENT_EMAIL/QA_ORG_SLUG = explicit blocker, never invent an account
v2 environment.md § Authenticating for testing — fill the v2-new session-reuse row (persisted browser storage state) when the browser-driver decision lands; the blocker-not-invention rule goes on the test-accounts row.

## [MIGRATE] playbook environment.md: browser policy (agent-browser primary per plan asher-skills#73, ChatGPT-in-Chrome per-use carve-out, repo Puppeteer qa:browser:probe authorized fallback 2026-07-22 owning bundled Chrome) + web baseline health-check recipe
v2 environment.md § Driving the app & capturing evidence — but the v2 template mandates Playwright-driving-Chrome and bars agent-browser as a verification route, so this section is written only after the browser-policy decision; whichever route wins, the earned facts (health-check baseline, Puppeteer owns bundled Chrome, never attaches to user profile, session-per-check) are recorded, not dropped.
Genuine conflict — see decisions.

## [MIGRATE] playbook environment.md: load fixtures only for scale/memory criteria, fixture names carry issue number + timestamp, owning thread cleans up via reset:*
v2 environment.md § Verification data — scale-affordances and lifetime rows; list the per-worktree Postgres/MinIO/SFTP stores as the v2-new per-ticket-disposable stores (reset:db / reset:object-storage / reset:sftp), everything else shared.

## [MIGRATE] playbook environment.md: review surface (tailnet root /review, ~/.backlog/surface/pipelines hub, LaunchAgent com.asher.backlog-surface:8377, ln -sfn publish, Funnel off, tailscale status preflight)
v2 environment.md § Presenting to the human — recorded there by serve-via-tailnet setup, which owns the surface; the existing LaunchAgent, surface dir, and proxy paths carry over as this repo's config, not rebuilt.

## [RETIRE] playbook environment.md: review-loop interactive commands (review-server.py/--sweep, review-await.py exit codes, tailscale serve proxy/teardown)
Replaced by serve-via-tailnet's annotated mode, which carries the same server/await/verdict machinery as canonical sibling scripts; the hardwired .agents/skills/review-loop/scripts/* paths die with the mount. Nothing procedural is lost — the verdict contract (approve / approve-with-nits / request-changes) survives in the sibling.

## [MIGRATE] playbook environment.md: staffing evidence (codex-cli 0.144.3→gpt-5.6-sol; claude 2.1.207 aliases effect-verified; versioned aliases REJECTED; Claude→codex exec unavailable in unattended children) + codex-exec second-opinion route + parallel-safe verdict (15 isolation tests, 2026-07-14)
v2 environment.md § Staffing delta (alias/rejection evidence, second-opinion route) + § Parallelism verdict (verdict: parallel-safe with the test evidence; serialized exception lane: shared Railway / real third-party providers / external SFTP; fill v2-new lane mechanics with a lock path) + platform.md § Harness directional-reachability row (Claude→codex unavailable unattended, fall back within harness).

## [MIGRATE] playbook platform.md: tracker binding + verified gh verbs (list/view/comment/edit-labels/create-serialized/close) and close-on-merge Closes #<n>
v2 docs/agents/platform.md § Tracker — carry every verified command verbatim, including the serialized main-branch-writer note on create; blocked-by rows come from the backlog-policy migration above (stale-summary override).

## [MIGRATE] playbook platform.md: PR verbs (gh pr create --base main --body-file, ready not draft; gh pr edit; inline comments via pulls API; exact 'LGTM' approval; human merges, loop never merges)
v2 platform.md § Change review — verb-for-verb; the exact-'LGTM' string is the approval signal row. Merge row updates to name merge-changes as the explicitly-authorized route with the human as authorizer.

## [MIGRATE] playbook platform.md: worktree create off origin/main with fetch+pull, push -u publish, worktree remove + stack reap, pinned-SHA orphaned-by-rewrite semantics
v2 platform.md § Version control — including the re-pin-after-rewrite policy the evidence embeds depend on.

## [MIGRATE] playbook platform.md: spawned threads read .agents/skills/backlog; Claude spawns via Agent/Task tool with isolation: worktree; Codex via native collaboration threads
v2 platform.md § Harness — update the readable-references path to the v2 backlog mount, re-verify both spawn routes at v2 setup, and fill the v2-new wrapper-staffing-evidence and route-trust rows.

## [MIGRATE] playbook evidence.md: probe-not-evidence rule, capture-after-convergence timing, evidence/<slug>/ + c<criterion>- naming, no-MP4, ffmpeg two-pass GIF recipe, ?raw=1 blob embeds vs camo-proxied raw URLs, mechanical verification checks, orphaned-SHA re-pin rule
v2 docs/agents/evidence.md — the v2 template has absorbed nearly all of this verbatim (§ What to capture, § Format and storage, § GitHub binding), so reconciliation is mostly confirming template text matches; repo-specific residue to keep explicitly: the c<criterion>- naming (template default matches), and the exact styling-only reuse verdict string 'no product-code change; no recapture' recorded beside the template's reuse rule.

## [MIGRATE] playbook change-description.md: body order, research-dossier section variant, sentence-case imperative title + issue number
v2 docs/agents/change-description.md — § Body outline is now template-carried (including the research dossier variant); the title convention and issue-number rule land in § This repo, along with implementing.md's plan-deviations-in-PR-body rule.

## [RETIRE] playbook change-fixer.md
The v2 adversarial-review skill's fixer role carries the generic protocol (address-all-comments scope rule, reply-with-SHA, re-prompt reviewer). Its one repo pointer — run checks from verifying.md — survives as codebase.md § Checks, which the fixer reads natively.

## [MIGRATE] playbook change-reviewer.md: Syncron behavior-risk surfaces, end-to-end type-safety scrutiny, migration/rollback/stale-caller checks, security/ops list (secrets, SFTP creds, bounded pools)
v2 docs/agents/codebase.md § Conventions (repo-specific patterns a newcomer would miss: the Syncron pipeline risk surfaces and type-narrowness law) — read by code-review in the v2 loop; the ruling-request protocol is generic v2 adversarial-review behavior and needs no repo copy.

## [MIGRATE] playbook change-reviewer.md: test coverage bar (regression for bugs, characterization for refactors, journey evidence for workflows) + frontend loading/error/empty/disabled states requirement
v2 codebase.md § Testing patterns (coverage bar) and § Conventions (frontend states, via the docs/agents/frontend.md pointer); the exact 'LGTM' and 'no product-code change; no recapture' strings live in platform.md § Change review and evidence.md respectively (see those rows).

## [MIGRATE] playbook diagnosing-bugs.md: tests beside source as *.test.ts(x), bun test invocations, record-exact-repro-when-no-test, #203 freeze forensics entry points (freeze-forensics.test.ts, supervisor.test.ts, captured logs)
v2 codebase.md § Testing patterns — including the known-hard-surface row for issue #203 with its named test files, which is the only map into that open defect.

## [MIGRATE] playbook diagnosing-bugs.md: Syncron triage stage enumeration, content-date filename invariants + injected logger wiring (apps/worker/src/index.ts), Sentry init (packages/observability/src/server.ts) + local sink, infra log commands (db:logs/bucket:logs/sftp-egress:logs), reproduce-locally-not-shared rule
v2 codebase.md § Conventions (triage stages, worker invariants, observability paths) + environment.md § Running locally (log commands) + § Worktree isolation singleton table (shared SFTP/Railway reproduce-locally rule). The stale chatgpt-in-chrome-primary browser routing line is dropped in favor of environment.md's newer 2026-07-22 policy — the reconciliation the inventory flagged, resolved by the browser-policy decision.

## [KEEP] playbook frontend.md (all earned UI conventions: sonner feedback grammar, inline form errors, never-swallow query errors, seed-from-server forms, datalist ban, commit-on-select pickers, valid-options-only, tree-not-flat, completion greps)
Stays at docs/agents/frontend.md as a repo-owned auxiliary playbook — too dense and load-bearing to inline; v2 codebase.md § Conventions binds it ('all UI work follows docs/agents/frontend.md') so every v2 builder and reviewer still reaches it.
Exists nowhere else; crown jewel.

## [MIGRATE] playbook implementing.md: commit style, in-memory-processing preference, type-source narrowness, database-migrations-skill-first rule, frontend skill loads, simpler-path stop-and-report
v2 codebase.md § Conventions (commit style, in-memory preference, type narrowness, rewritten frontend skill-load pointer) + § Generated artifacts (database-migrations skill before generating/editing migrations); simpler-path stop-and-report and plan-deviation recording are generic v2 build/implement behavior plus the change-description.md § This repo note. Then retire the file.

## [MIGRATE] playbook planning.md: plan-threshold list (subsystems, schema/enums/contracts, new deps/flags/workflows, Syncron semantics, risky/>1-day)
v2 backlog-policy.md § Label roles needs-shaping row / § Readiness decision — the threshold becomes groom's routing bar for what needs shaping vs routes direct (feeding the v2 route:direct metadata line).

## [MIGRATE] playbook planning.md: plans/<ts>-<slug>.html format, inline-SVG diagrams, stable ac-N anchors, hash-bound approval (comment is NOT approval), ledger dispositions on request-changes
Format and skeleton are superseded by v2 to-spec (spec on the ticket, diagram first, presented via serve-via-tailnet); the surviving contract — stable ac-N anchors that verify/evidence key on, verdict-only approval, per-annotation dispositions — is serve-via-tailnet annotated-mode behavior, recorded in environment.md § Presenting to the human. Committed plans/*.html keep their anchors; nothing rewrites them. Then retire the file.

## [MIGRATE] playbook prototyping.md: bun/Turbo task registration, with-worktree-env wrapper for DB scripts, frontend routing under apps/frontend/src, ?variant= URL-param switcher pattern with screenshots per variant
v2 codebase.md § Conventions (task registration, wrapper, ?variant= prototype pattern — read by the v2 prototype skill) with the driver reference resolving to environment.md § Driving the app. Then retire the file.

## [MIGRATE] playbook refactoring.md: characterization-tests-first, Bun test commands, DB-backed via with-worktree-env, no-widening + no cross-package reshapes, stop-and-reclassify on real bugs
v2 codebase.md § Testing patterns (characterization-first, commands) + § Conventions (widening/reshape rules, deduped with the reviewer/implementing copies); no-behavior-change-in-refactor and reclassify-on-bug are generic v2 implement routing. Then retire the file.

## [MIGRATE] playbook researching.md: research/<slug>/ durable root, scratch-in-temp, research-out-of-evidence, primary sources = official Syncron/provider docs, serialize shared systems + preserve customer files
v2 backlog-policy.md § Label roles research row (dossier root, primary-source expectation) + environment.md § Verification data / § Worktree isolation (customer-data and shared-system rules); the v2 research skill owns the method. Then retire the file.

## [MIGRATE] playbook verifying.md: check ladder, bun run check composition (sherif + knip --no-config-hints + turbo run check --concurrency=1), CI gate identical to local, known non-fatal warnings, stale-caller-must-fail-check expectation
v2 codebase.md § Checks (full gate exactly as CI runs it, per-package ladder, runner traps: chunk-size advisory, worker#build no-output warning) + § Conventions (stale-caller expectation) + environment.md § Branching & deploys (CI = bun install --frozen-lockfile + bun run check).

## [MIGRATE] playbook verifying.md: Syncron inbound verification evidence list (manifest path, run detail URL, final status, egress listing, row-level proof), migration-verification form, UI/SFTP evidence forms, codex-exec second opinion
v2 evidence.md § What to capture — repo-specific expectations rows (Syncron inbound package, migration proof, UI states incl. loading/error/disabled, SFTP listing with credentials omitted); second-opinion delegation → environment.md § Staffing delta. Then retire the file — its generic role is the v2 verify-your-work skill.

## [RENAME] label: in-flight
in-flight → building: `gh label edit in-flight --name building --repo dunnharland/pipelines` (label follows by id, so historical issues keep it) — executed now, in the zero-open-in-flight window; backlog-policy.md § Label roles records 'formerly in-flight' so old comments still parse.
Alternative (zero-mutation): bind the v2 building role to the existing in-flight name — see decisions.

## [RENAME] label: needs-shaping (new)
(none) → needs-shaping: `gh label create needs-shaping --repo dunnharland/pipelines --description 'Parked for strategic shaping' --color <pick>` — v2 groom's park target; bound in backlog-policy.md § Label roles.

## [RENAME] label: shaping (new)
(none) → shaping: `gh label create shaping --repo dunnharland/pipelines --description 'A shaping thread is attending it' --color <pick>` — set by groom at thread dispatch so a subject never gets two threads.

## [KEEP] labels: ready-for-agent, ready-for-human, needs-info
Names match v2 defaults exactly; bound 1:1 in v2 backlog-policy.md § Label roles.

## [KEEP] labels: bug, enhancement, refactor, research, draft (work types)
Names match v2 work-type defaults; bound 1:1, still required alongside ready-for-agent.

## [KEEP] labels: duplicate, invalid, wontfix, superseded (exclusions)
Bound as v2 exclusion roles verbatim.

## [KEEP] labels: documentation, good first issue, help wanted, question, needs-triage, design, observability, rfq, admin
Listed as neutral in v2 backlog-policy.md § Neutral — ignored for selection and routing, exactly as today.

## [KEEP] tickets: #240 #239 #237 #236 #213 (ready-for-agent)
Labels carry over unchanged; before the first v2 `backlog build`, audit each for a complete Dispatch: block (Surface / Coordination class / reason, plus the v2-new route:direct line for enhancements) — v2 skips tickets with missing metadata rather than inferring, so gaps go through one v2 groom pass first.

## [KEEP] tickets: #247 #235 #233 #223 #184 #183 #123 (ready-for-human) and #263 #255 #226 #214 (needs-info)
Parked roles are identical in v2; no relabeling, no redispatch.

## [MIGRATE] state: run 20260715-quote-import-wave-1 left 'active' for issue #232
Close out the run record explicitly (a closing event/handoff note in .git/backlog/runs/20260715…, never deletion) and re-groom #232 under v2 — it carries no in-flight label, so the run file is the only claim on it.
Disposition of #232 itself (ready / needs-shaping / close) is a groom call — see decisions.

## [KEEP] in-flight: LIVE review-server PID 62436 (LICON/alarkan plan, round 2 awaiting)
Untouched until the round-2 verdict lands or Asher chooses a deliberate stop (`review-server.py --stop --state ~/.backlog/reviews/pipelines/2026-07-23-0005-…` + `tailscale serve --set-path /pipelines/licon-pss-test/review off`); only then may the review-loop mount be removed. The possibly-twin alarkan plan file in the same 0005 slot gets checked for divergence before either is archived.

## [KEEP] in-flight: review surface (~/.backlog/surface/pipelines, registry.json, LaunchAgent com.asher.backlog-surface:8377, /review proxy)
Machine-level state owned by serve-via-tailnet in v2 — carried over as this repo's recorded surface config in environment.md § Presenting to the human; a repo-scoped skills purge must not strand it, and the migration must not rebuild it.

## [KEEP] in-flight: uncommitted main-checkout changes (.gitignore, AGENTS.md +35, skills-lock.json +6, untracked ask-syncron mount + SPP/report/script files)
Committed deliberately (or explicitly triaged with Asher) BEFORE any reinstall or cleanup — the 2026-07-22 run's checkpoint explicitly preserved them; no git reset --hard / git clean -fd at any migration step.

## [KEEP] in-flight: .git/backlog/runs/ (three runs: events, boards, handoffs, review/225 server logs)
Historical archive of the v1 loop — v2 needs none of it (tracker is the ledger) but it is the only record of the 20260715 active anomaly and the review/225 round; retained in place, never deleted.

## [RETIRE] in-flight: leftover worktrees pipelines-224 / -229 / -231 (merged, clean)
Nothing lost: branches are merged and trees clean. Remove properly — `git worktree remove` then scripts/cleanup-worktree.sh / `bun run reset:worktree-stacks` for derived stacks — ideally after PR #254 (the teardown-hygiene fix) merges; the deliberately retained #225 compose volume is deleted only on Asher's say-so; /Users/asher/Projects/opportunity-alarkan-pipelines is excluded from any pipelines-* glob.

## [KEEP] in-flight: open PR #254 (codex/worktree-teardown-hygiene)
Drive to merge through the existing review path (or as the first v2 adversarial-review) — it fixes the very cleanup protocol the worktree reaping above depends on.

## [KEEP] in-flight: unmerged branches (codex/119, codex/125, codex/127, codex/api-contract-persistence-cleanup, codex/fix-rfq-demand-large-import, agent/reconcile-asher-skills, backup, advisor/001-010; remote diag/worker-freeze-forensics, fix/worker-supervisor-watchdog)
Per-branch judgment, never bulk delete: many codex/* only look unmerged due to squash merges (verify each against merged PRs); diag/worker-freeze-forensics and fix/worker-supervisor-watchdog back open issue #203 and must survive; advisor/* pair with committed plans/001-010.

## [KEEP] in-flight: plans/ (~40 committed plan docs with stable ac-N anchors), evidence/ (39 SHA-pinned dirs), research/ + reports/
All committed history the v2 loop still leans on: newest plans back open work, evidence embeds are SHA-pinned (so no history rewrites, per platform.md § Version control), research/ stays the dossier root bound in backlog-policy.md. v2 to-spec changes how NEW specs are made; it does not touch these.

## [RETIRE] script: .agents/skills/backlog/scripts/run-state.py (+ evals)
v2 backlog replaces file-based run state with tracker-as-ledger (attributed claim + outcome comments; resume reconciles claims against worktrees/branch tips) — the capability is fully covered; historical .git/backlog output stays.

## [RETIRE] scripts: review-loop review-server.py / review-await.py
Canonical copies live with serve-via-tailnet's annotated mode (same server/await/verdict-exit-code machinery); removed only after PID 62436 resolves; environment.md's hardwired .agents/skills/review-loop paths are rewritten to the sibling in § Presenting.

## [RETIRE] scripts: setup-asher-skills install.py / catalog.py / render-global.py (+ evals) and staffing render-global.py
Superseded by the v2 install flow and the refreshed v2 staffing skill, which ships its own current scripts; old copies recoverable from git history.

## [KEEP] scripts: .claude/worktree-setup.sh, .claude/worktree-teardown.sh, .codex/environments/environment.toml
Targets of GLOBAL harness worktree hooks — not skill files; deleting them breaks worktree create/cleanup for every future session. Referenced from v2 environment.md § Worktree isolation as the bring-up/teardown bindings.

## [KEEP] scripts: repo-owned worktree machinery (scripts/worktree-env.ts, with-worktree-env.ts, setup-worktree.sh, cleanup-worktree.sh, reap-worktree-stacks.ts, worktree-stacks.ts + tests)
Repo product code, not skill material; it IS the isolation regime v2 environment.md § Worktree isolation records, with its 15-test suite as the parallel-safe verdict's evidence.

## DECISIONS NEEDED
- Live review PID 62436 (LICON preferred-supplier-routing plan, round 2): let the verdict land before migrating, or stop deliberately now (--stop + tailscale serve off)? Also: is plans/2026-07-23-0005-alarkan-…-test.html a renamed twin to archive, or separate work?
- Browser verification policy: v2 mandates Playwright-driving-Chrome and bars agent-browser as a verification route; pipelines' earned policy (agent-browser primary per asher-skills#73, repo Puppeteer qa:browser:probe fallback, no Playwright suite). Adopt Playwright and start an e2e/ spec suite, or record the repo Puppeteer probe as this repo's driver deviation in environment.md § Driving the app?
- Label mechanics: rename in-flight → building via gh label edit (mutates the display on historical issues), or keep the existing name and bind the v2 'building' role to label 'in-flight' in backlog-policy.md (zero tracker mutation)? Either works; pick one before setup runs.
- uncodixfy and greploop: both third-party and retired from the v2 family. uncodixfy is load-bearing for frontend playbook text — keep it as a declared external requirement (recommended) or retire and fold its role into frontend.md? greploop is unreferenced — retire, or redeclare if still used?
- impeccable: diff the two independent real dirs; if identical, which disposition — normalize + declare in the lock, or delete (provenance unknown, so someone must vouch for it first)?
- Issue #232 (run 20260715 left 'active', no in-flight label): re-groom to ready-for-agent, park to needs-shaping, or close?
- Lock provenance repair for database-migrations and shadcn (source = the repo itself, empty-string hashes): rebind to their true upstreams, or declare them repo-owned skills with real hashes?
- Per-branch disposition of the unmerged local branches (advisor/001-010, codex/119/125/127, api-contract-persistence-cleanup, fix-rfq-demand-large-import, backup, agent/reconcile-asher-skills) and whether the deliberately retained #225 compose volume can now be deleted.

## MUST NOT LOSE
- The blocked_by dependency read/write commands with X-GitHub-Api-Version: 2026-03-10 and the 2026-07-14 live-probed GOTCHA that .issue_dependencies_summary stays stale — the v2 platform.md template's default read is EXACTLY that broken summary path, so a verbatim template copy silently reintroduces a known failure.
- docs/agents/frontend.md in full: the sonner/inline-error feedback grammar, never-swallow-query-errors rule, datalist ban, commit-on-select picker semantics, valid-options-only filtering, tree-not-flat rendering, and the completion greps — dense earned UI law that exists nowhere else.
- The check contract: bun run check = sherif + knip --no-config-hints + turbo run check --concurrency=1, the per-package ladder, and the fact that CI runs the identical gate — plus the stale-caller-must-fail-check type-safety expectation across DB/API/SQL/frontend.
- The worktree isolation contract: worktree-env.ts derivation (COMPOSE_PROJECT_NAME, ports 21000-31000, per-worktree *.localhost:1355 subdomains on the intentionally shared 1355 proxy), the non-isolatable singleton list (Railway, Resend, AgentMail, OpenAI, PostHog, Sentry, customer SFTP), and the parallel-safe verdict's test evidence.
- The exact verdict strings the loop keys on: 'LGTM' (approval) and 'no product-code change; no recapture' (styling-only evidence reuse) — protocol constants, not prose.
- The unlocked repo-earned mounts qa-user-journeys and sentry-cli (plus the untracked ask-syncron-parts-planning mount and its uncommitted lock entry): any lockfile-driven 'reinstall the locked set, delete the rest' sweep destroys content that exists nowhere else.
- The never-npx-skills-remove rule for this repo: three lock entries resolve to the repo itself with empty-string hashes, so a remove can delete repo content.
- Issue #203's diagnosis map: apps/worker/src/freeze-forensics.test.ts, supervisor.test.ts, the remote diag/worker-freeze-forensics and fix/worker-supervisor-watchdog branches, and the content-date/daily-run worker invariants.
- .git/backlog/runs/ event logs — the only record that run 20260715 (issue #232) was left active, plus the review/225 server logs; archive, never delete.
- The GitHub evidence presentation law (blob ?raw=1 same-origin embeds, camo-proxied raw URLs 404 on private repos, mechanical SHA/file checks, re-pin-never-replain on orphaned SHAs) — now template-carried in v2 evidence.md, but the repo binding must land verbatim, and platform.md must keep the re-pin-after-rewrite policy that protects the 39 committed evidence dirs.
- Staffing/reachability evidence: versioned model aliases rejected by the installed Claude CLI, and Claude→codex exec unavailable in unattended children — facts that prevent repeating dead-route dispatches.
