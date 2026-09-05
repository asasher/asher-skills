---
name: backlog
description: The software backlog dispatcher for a GitHub repo — capture, groom, build, retro, status, setup. Each verb sweeps the issues, confirms a plan, and fans one run of a skill per unit of work.
disable-model-invocation: true
metadata:
  requires: [capture, shape, deliver, retro, to-thread, worktree]
  optional: [merge, agent-ready-codebase, writing-for-humans, technical-writing]
  setup: reference/setup.md
---

# Backlog

A dispatcher with no supervisor. GitHub issues are the run ledger: every claim, outcome, and reclaim is a comment on the issue, and liveness is derived at read time, never recorded.

Every verb does the same three things: sweep the issues for the units it applies to, confirm the plan with the user, then fan one run of a skill per unit and exit. The verb skill (`capture`, `shape`, `deliver`, `retro`) works on exactly one unit and runs on its own without this dispatcher; this skill decides only which units and when.

Labels, claims, deadlines, and branch names are fixed by this skill: [labels](reference/labels.md). The repo's environment is read from `docs/agents/environment.md`; when it is missing, run `backlog setup` first instead of improvising it.

Chat text follows the `writing-for-humans` sibling; issue bodies and comments follow `technical-writing`. Absent either, write plainly and say the standard was not loaded. A stumble in any verb (an instruction misread, a confirmation repeated, a stale playbook row) is recorded the moment it shows via `retro note`; absent the `retro` sibling, say so once and move on.

## capture

Run the `capture` skill on the current conversation. There is nothing to sweep: the conversation is the unit.

## groom

1. **Sweep.** Every open issue carrying no readiness label, plus every `needs-shaping` issue, or the ids given. Done when each swept issue has been read in full: title, body, comments, labels, blockers.
2. **Route, as a plan.** An issue whose decisions are already settled routes to `ready-for-agent` and builds from its own text. One owing the reporter facts routes to `needs-info`, human-only work to `ready-for-human`, a duplicate or dead issue to closure. The rest is shaping work, and two judgments shape it. **Merges**: many small related issues absorb into one shapeable subject; one issue carries the merged body and the others close as duplicates pointing at it. **Subjects**: each shaping thread owns one canonical issue. When decisions interlock, propose consolidating their context and scope into that issue; identify every absorbed issue and its disposition in the plan. Issues whose independent scope remains valuable stay separate. The approved canonical issue owns the work branch, spec, and blessing.
3. **Confirm.** Present a plan the user can follow from chat alone. Every swept issue appears exactly once (routed, merged, proposed for closure, or held with the reason) with its id, title, and a one-or-two-sentence digest drawn from its body. Relations are words, never bare id lists: "#12 blocks #14", "#7 absorbs #9 and #11". A body too thin to digest is reported as thin, never invented. Until the user approves, no issue changes and no thread exists.
4. **Apply the routing.** Labels, closures, merged bodies, exactly as approved.
5. **Fan shaping threads.** Ask how many to start now, default three; the unstarted remainder stays routed for the next groom. Per started subject: label its canonical issue `shaping`, prepare one worktree via the `worktree` skill on the work branch (labels § Branches) from the base branch, and spawn one thread via the `to-thread` skill in that exact directory, named for the subject, seeded with the canonical issue id and the instruction to run `shape` on that issue. Record branch, path, and thread name on the canonical issue before the spawn. A failure between labeling and a verified spawn rolls the subject back: restore the labels, comment the failure, remove a clean worktree, preserve a dirty one and surface its path. Never shape in the primary checkout.
6. **Teardown sweep** (§ teardown sweep). Done when each candidate is reaped or surfaced.

## build

1. **Gate.** `docs/agents/environment.md` § Agent-readiness records a full pass against the `agent-ready-codebase` checklist. A missing or failed certification hands every issue back with the gap surfaced; re-run `backlog setup` to re-certify.
2. **Sweep.** Every `ready-for-agent` issue with no open blocker (labels § Dependencies) and no live claim, or the ids given. A spec issue appears here only once every child is closed, because each child blocks it. Re-running `backlog build` is idempotent: the claim, not a queue, prevents double dispatch.
3. **Size the wave.** Read the concurrent-build limit in § Agent-readiness, default three. Count existing live builds and unresolved spawn reservations against it, including stalled threads until confirmed stopped. Available slots are the limit minus occupied slots. Confirm the selected issue list within those slots; existing approval covering that list is sufficient. Leave the rest ready for the next sweep. Recheck eligibility and available capacity immediately before each claim. Concurrent dispatchers must serialize capacity admission; issue comments alone do not enforce a machine-wide limit.
4. **Claim and fan.** Per admitted issue, post the dispatch declaration as a provisional claim and swap `ready-for-agent` for `building`. Inspect an existing worktree before preparing another; a shaped issue keeps its context commits, a child branches from the spec branch, and unshaped work branches from the base. Use `worktree` for the exact directory, then spawn `deliver` there via `to-thread`, carrying the claim's absolute deadline. Confirm liveness and record the thread id before the next claim.
5. **Recover failed dispatch.** If provisioning or spawn fails, first establish whether a worker started. Stop it and confirm it is stopped before releasing the reservation. If liveness remains uncertain, retain the reservation and report it. Once stopped or confirmed never started, post a failed-dispatch outcome, restore `ready-for-agent`, and remove only a newly created clean worktree through `worktree`. Preserve reused or dirty worktrees and report their paths. Stop this sweep when the failure indicates a shared capacity or harness problem.
6. **Exit** when the admitted wave ends. Outcomes land on each issue as the build's outcome comment; `backlog status` is how anyone reads the fleet. Never dispatch from or mutate the primary checkout: fetch the remote and resolve the base without checking it out; warn when the primary checkout is dirty, ahead, or behind. Merging stays the `merge` skill's human authorization.

## retro

Run the `retro` skill's pass over the friction ledger.

## status

A pure query that writes nothing except through the teardown sweep. Join four sources: the claims and their deadlines, live worktrees and branch tips, PR state, and the harness's thread listing. Report ids with titles and digests, relations in words, every live claim and every listed worktree in exactly one bucket:

- **Finished**: a claim whose PR is review-ready or merged.
- **Active**: a live build before its deadline, or a provisional spawn whose liveness is still being resolved.
- **Stopped**: a recorded bound, product question, incomplete verification, or failed dispatch with no live worker. Show its next action and any retained worktree.
- **Stalled past deadline**: past its absolute deadline, thread still observably alive. Report it, leave it.
- **Abandoned**: `building`, deadline passed, thread not observably alive, and no recorded stop or completion. Derived, never written.
- **Orphans**: worktrees, artifact branches, or container stacks no active or stopped work record explains.

Reclaim rules: audit reality first, then adopt committed work. A reclaim resumes from the branch and the delivery checkpoint on the issue or PR. Preserve consumed review passes and any unresolved stop condition. Record a new claim comment superseding the old (labels § Claims); a new claim deadline does not erase a stopped convergence bound. Another actor's expired claim is not yours to clear: leave a takeover note. The issue records transitions, never telemetry.

## teardown sweep

Every path that finishes or abandons an issue's work must account for its worktree; the `merge` skill owns the merge path and the owning thread owns the abort path. A stopped run retains its worktree and checkpoint for recovery; a stop is not permission to delete it. This sweep catches what they missed. Enumerate from git's worktree listing joined with each branch's PR state, never a directory scan. A worktree whose PR is merged or closed is a candidate: a clean tree is reaped through the `worktree` skill's Remove without asking; a dirty tree is surfaced for the user's confirmation and never silently deleted. Detect merged from PR state, never a merge-base check, which squash merges defeat. An `artifact/<issue>` branch whose issue is closed is deleted. Where `environment.md` records container stacks, containers whose compose working-dir label points at a path that no longer exists are orphaned stacks: surface them.

## setup

Load [setup](reference/setup.md) and reconcile the project against [the environment template](templates/environment.md).
