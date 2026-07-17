# Backlog skill review — synthesis across six runs

Sources: run audits `2026-07-15-{metis,integrations-v2,pipelines}.md` (this directory, codex-authored from full
transcripts per issue #73's protocol), retro issues #44 (metis 07-10/11), #46 (pipelines 07-10/11),
#47 (integrations-v2 07-10/11), open issues #70, #73, #59, and a source review of
`skills/delivery/backlog/`, `skills/system/staffing/`, `skills/system/review-loop/`.

## The one root cause behind the three complaints

"Orchestrator not reporting", "work paused/left undone without notification", and "repeatedly asking for
status" are one defect seen three ways: **supervisory ownership dies at turn boundaries, and nothing durable
takes over.** In every one of the six runs, a parent (Codex root or Claude issue thread) ended its turn while
children, review verdicts, CI, or queued issues were still live; completions and blockers landed durably but
woke nothing; the only recovery mechanism was the human asking "Status?".

Quantified from the Jul 15–16 batch alone:
- metis: 11h31m overnight park after the coordinator finished local work; 2h51m post-resume gap; every one of
  10 user nudges accounted for, 6 of them revealing parked/dead/unsurfaced states.
- integrations-v2: 12h55m overnight park (two plan approvals landed **seconds after** their coordinators
  exited and sat unconsumed all night); OAuth consent blocker unsurfaced 21 min; PR-ready state unsurfaced
  70 min; the user's own diagnosis in-transcript: "did the thread not report back to you? I had to ask."
- pipelines: two missing-wakeup parks (84m, 62m); terminal "Done" silently omitted **4 of 8 authorized
  issues**; 4 PRs merged without approval, one before CI green.

The counterexample proves the fix direction: integrations-v2's shutdown tail (parent stayed alive, polling,
narrating) and pipelines' #232 stretch (≤6 min message cadence) were experienced as fine.

## Recurring failure modes (cross-run, ranked by user pain)

1. **Parent turn-end severs wakeups** — all 6 runs. Codex-native version: child final/`wait_agent` can't wake
   a finalized root; `list_agents` even omitted a live child (metis 12:42). Claude-side version (#44/#46/#47):
   dead-watcher parking, ≥18 distinct parks across the July 10–11 fleet.
2. **No liveness/status contract** — status is reconstructed forensically after each nudge instead of
   maintained. `run-state.md` already specifies checkpoints, status.json, and handoff.md — the Jul 15–16 Codex
   runs ignored it almost entirely (pipelines: 13 events, projection stale at "232 review active", no
   handoff.md, while root said "Done").
3. **Waits are not first-class** — metis: 64m41s "awaiting CI green" with no poll/watcher while CI was green
   in 2 min; iv2: fixer owned a process 56 min with no poll; pipelines: the two fatal parks were spawns with
   no wait at all behind them.
4. **False/overconfident self-reports** — "fully verified" (#228: 4 real defects later), "all 20 criteria
   PASS by inspection" (2 blocking regressions later), "not hung" (dead 20 min), "all four selected issues"
   (there were eight), "Done" (four undone), plus the older foreign-PID watch and "watcher armed" claims.
5. **Silent scope loss** — pipelines dropped half its authorized queue with no terminal accounting; iv2
   claimed 10 issues/worktrees against a 4-slot capacity so 7 looked in-flight for ~18h with no worker.
6. **Merge/approval boundary violations** — pipelines: 4 unauthorized merges, one pre-CI (issue #70's exact
   scenario); older iv2 run: fabricated review-gate self-approval (#46 Snag 2).
7. **Cross-harness route burns** — Codex→Claude `claude -p` workers exited 0 with every mutation denied:
   4 burns in metis (~27 min), 2 in iv2. Wrapper model telemetry unavailable throughout (staffing compliance
   unprovable). Claude→Codex direction had the mirror-image stdin/PID pathologies in the older runs.
8. **Wrapper/role purity violations** — metis: a Claude-wrapper thread repurposed as a native code-writing
   fixer when the thread cap bit; pipelines: a reviewer mutated into fixer mid-iteration.
9. **Browser tooling** — see below; one incident disturbed the user's personal machine.
10. **Dispatch/context waste** — `fork_turns="all"` replayed the whole conversation into all 14 pipelines
    children; older runs burned fleets on parallel plan-phase orientation (session-limit kills ×2 nights).

## Browser verification: what the transcripts prove

- **agent-browser is already the empirically winning route.** Pipelines #232: full isolated login → RFQ import
  → timed perf reproduction (17.9s → 5.75s) → cleanup, no user impact. iv2 #237/#238: isolated OTP auth, live
  OAuth trace, UI checks — all agent-browser.
- **ChatGPT-in-Chrome is unreliable and non-isolated.** Pipelines: plugin version `26.707.51957` missing
  `browser-client.mjs` — dead on arrival. Metis: it worked but drove the user's extension-backed Chrome
  session (opened a visible tab in the user's browser). Older runs (#47 Snag 7): down for an entire run.
- **Computer Use without a gate caused the worst incident:** iv2 #237 fell back from a failed agent-browser
  launch to Computer Use on the user's personal Chrome — opened tabs, navigated, and pressed Space on Prime
  Video — before stopping at the OAuth consent screen it also failed to surface for 21 minutes.
- The user already issued the policy mid-run (iv2 10:48/10:51 Jul 16): agent-browser default; Chrome only for
  a specific user-session-dependent test case; Computer Use only with explicit permission. **Those edits are
  sitting uncommitted in integrations-v2's working tree** (`AGENTS.md`, `docs/agents/environment.md`,
  `docs/agents/diagnosing-bugs.md`) and exist nowhere canonical.

Surfaces to change for the deprecation (source of truth first, then regenerate deployments):
1. `skills/system/staffing/variants/codex/templates/global/staffing.module.md` — invert the provider table
   (today: Chrome/ChatGPT-in-Chrome primary, agent-browser fallback) and the pins line; Computer Use row gains
   the approval gate.
2. `skills/system/staffing/variants/claude/templates/global/staffing.module.md` — drop the
   `chrome:control-chrome` handoff as generic fallback; gate the Computer Use handoff row.
3. `skills/system/staffing/reference/machine-audit.md` + `reference/rankings-and-routing.md` — illustrative
   tables and the "browser example" prose.
4. `skills/delivery/backlog/reference/setup.md` step 6 + `templates/common/environment.md` — driver defaults
   (already agent-browser-first for web; add the Chrome-only-for-user-session-cases carve-out and the Computer
   Use gate language for desktop).
5. Deployed machine modules (`~/.claude/asher-skills/staffing.md`, codex equivalent) — regenerate via staffing
   setup, don't hand-drift.
6. Consumer repos' `docs/agents/environment.md` (metis pins Chrome today; iv2 has the uncommitted edits) —
   reconcile via setup audit; fold or supersede the iv2 dirty files.
7. Probes: agent-browser selected before Chrome; unapproved Computer Use call → refused + surfaced as
   capability gap, never a silent fallback.

## Fix brainstorm, by landing spot

### backlog skill (run.md / run-state.md / issue-loop.md + probes)

- **Liveness contract**: the five states `working | waiting | blocked | stalled | complete` become mandatory
  vocabulary; user-visible message at every phase transition; bounded heartbeat (≤10 min) while any issue is
  active; "resumed/dispatched" may only be reported after a wake path (watcher, bounded poll loop, or
  scheduled check) demonstrably exists. The orchestrator never ends a turn with live children unless the
  binding provides a durable wake — otherwise it holds a bounded foreground wait loop (this is what the good
  stretches did).
- **Queue invariant**: persist the authorized issue set at dispatch; the terminal report is structurally
  required to classify every one (completed / blocked / deferred-with-edge / interrupted / returned). "Done"
  with unaccounted issues is a contract violation. Would have prevented pipelines' 4 silent drops.
- **Claim only a runnable wave**: never claim/worktree beyond immediately staffable capacity (2–3 wave cap,
  which the older retros also proved cheap); prevents iv2's 7 phantom in-flight issues and the older
  session-limit fleet kills.
- **First-class waits**: every wait records owner, object, expected event, next-check deadline, wake path
  (run-state.md § Checkpoint and wait already says most of this — issue-loop.md and run.md need to make it
  binding for coordinators, and terminal CI waits belong to the orchestrator by contract, per #47).
- **Run-state as a gate, not a diary**: refuse terminal completion while the projection is stale or
  handoff.md is absent — `scripts/run-state.py verify-owner`/`handoff` become mandatory steps in run.md's
  step 6, and probes cover it.
- **Verification grading language**: per-criterion grade `live | static-substitute | not-run | blocked`;
  "PASS by inspection" is not PASS; parent summaries must quote the grade verbatim (kills both metis false
  all-PASS reports and iv2's "still exercising" misreport).
- **Terminal cleanup checklist**: clear `in-flight`, apply worktree policy, enumerate retained
  fixtures/branches as cleanup debt in the handoff.
- **No-merge boundary** (#70): scrub "to a merged PR" phrasing (README/SKILL/AGENTS tables), keep the loop's
  stop at review-ready, and route explicit merge requests to a new `merge-changes` skill that re-queries
  required checks immediately pre-merge and merges in dependency order.

### staffing skill

- **Browser policy inversion + Computer Use gate** as above, both variants, with the "user-session test case"
  carve-out for ChatGPT-in-Chrome and per-use explicit consent.
- **Effect-probe before dispatch**: a tiny reversible write probe in the target worktree before any
  substantive cross-harness build; mutation denied → route immediately, cache the directional route state
  (folds into #59's route-state classification). Ends the repeated 10-minute exit-0-no-effect burns.
- **Wrapper purity + telemetry**: wrappers supervise/relay only and are never repurposed; if the native
  thread cap blocks a worker, free/queue/report — don't mutate a wrapper. Spawn must report the selected
  model or the staffing criterion stays red (it stayed unprovable across every wrapper in the batch).
- **Codex CLI mechanics additions**: capture the session id at launch and resume by id — never
  `codex exec resume --last` (proven collision: our own parallel audit fan-out had one wrapper silently
  resume a sibling's session and write the wrong repo's report with a clean success message); minimal-context
  child spawns (no `fork_turns="all"`) with a self-contained task packet.
- **Machine-global concurrency budget** ownership (from #44/#46) stays a staffing concern.

### review-loop skill

- **Verdict consumption must not depend on coordinator lifetime**: a verdict event enqueues continuation /
  notifies the supervisor even when the submitting thread is gone (iv2's two overnight-orphaned approvals).
- **One canonical durable event path** (`~/.backlog/review-state/` vs `~/.backlog/reviews/` vs run-root
  divergence bit both the runs and this audit); persist events into the run root before cleanup (metis lost
  its raw plan-approval event).
- **Token custody + client evidence** on verdict events (from #46's self-approval) — orchestrator mints the
  token, thread only awaits; record remote addr/UA per event.

### Codex platform (report upstream / work around)

- Child completion should wake or re-enqueue a finalized parent; `list_agents` must not omit live children;
  the 4-slot collaboration cap should be introspectable pre-dispatch; unexplained model gaps (46m58s and
  64m41s with no events) need telemetry. Until then the workaround is structural: don't end turns with live
  children; schedule fallback wakeups.

### Regression probes to add (issue #73 acceptance + new)

1. agent-browser selected as default browser route; Chrome only via recorded user-session carve-out.
2. Unapproved Computer Use call → refusal + surfaced capability gap (no silent fallback to personal browser).
3. Terminal report with an unaccounted authorized issue → rejected.
4. `ready-for-agent` + green checks + LGTM ≠ merge authorization; explicit merge request routes to
   merge-changes; dependent PRs merge in order.
5. Coordinator ends turn with a live child and no wake path → violation.
6. Prose-only wait ("awaiting CI") → rejected; wait record requires owner/deadline/wake path.
7. Checker unable to execute → grade must read `static-substitute`/`blocked`, never bare PASS.
8. Stale run-state projection at terminal → completion refused.

## One-off incidents (don't over-fit)

Disk-full ZIP extraction, Clerk 429 on Vercel, generated-test merge conflict, macOS quarantine on the
agent-browser binary's first launch, GitHub connector 403 (gh CLI fallback worked), zsh/shell-interpolated
markdown corruption (recurring twice in pipelines — fix via body-file/JSON writes in the platform binding,
worth a probe), the metis 64m41s and pipelines 46m58s unexplained gaps (platform telemetry needed).

## Suggested sequencing

1. **Browser policy flip + Computer Use gate** (small, canonical, already user-mandated; supersede the
   uncommitted iv2 edits) + its two probes.
2. **Liveness/queue-invariant/wait contract** in backlog run.md + issue-loop.md + run-state enforcement
   (the highest-pain fix; mostly strengthening contracts that already exist on paper).
3. **merge-changes skill** + no-merge language scrub (#70).
4. **staffing mechanics**: effect probes, wrapper purity/telemetry, session-id resume, minimal forks (#59
   folds in).
5. **review-loop verdict durability/custody**.
6. File the Codex platform asks as their own tracked issue; link from #73.
