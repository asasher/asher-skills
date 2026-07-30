---
name: backlog
description: Dispatch the backlog — groom sweeps tickets carrying no readiness role and needs-shaping tickets into user-confirmed batches, fans them into shaping threads, and sweeps finished tickets' worktrees for teardown; build fans ready, unblocked tickets with no open children into worktree-isolated subagents it supervises. Setup installs the playbooks.
argument-hint: "[groom | build | setup] [ticket ids]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: [build, shape, to-subagent, to-thread, worktree]
  optional: [merge-changes, retro]
  setup: reference/setup.md
---

# Backlog

A dispatcher with two dispatch shapes. Grooming is interactive — human-in-the-loop work fans out as
threads the user attends, and no result flows back. Building is autonomous — it fans out as subagents
this session supervises to completion.

Nouns are roles: *ticket*, *label*, *change request* are bound to this repo's real tracker, review
surface, and version control by `docs/agents/platform.md`; label roles, dependency edges, and readiness
by `docs/agents/backlog-policy.md`. Missing playbooks: run `backlog setup` first — don't improvise them.

**Friction is noted as it happens.** A stumble in this loop — an instruction misread, a confirmation
the user had to repeat, a stale playbook row, a workaround that shouldn't have been needed — is
recorded the moment it shows via the `retro` sibling's note verb, and a run's end is the sweep for
anything unnoted, stumbles relayed in build outcomes included. When the note verb reports a retro pass
due, relay that report and stop — running the pass is never this dispatcher's call. Absent the `retro`
sibling, friction goes unrecorded: say so once when there was something worth noting, then move on.

## groom

Sweep the tracker for tickets carrying **no readiness role** — however else they are labeled: a
captured ticket arrives work-typed but unrouted — and tickets carrying the needs-shaping role, or take
the ids given. Route first — as a plan, not as writes: a ticket whose decisions are already settled routes to
the ready role, one owing reporter facts or human-only work to its parked role per the label roles, a
duplicate or dead ticket to closure — the rest are shaping work. Group that rest twice: tickets whose
decisions interlock form one **subject**; subjects that belong together (same subsystem, same domain
area) form one **batch**, sized to what one thread can hold.

**Confirm before anything changes — with a plan that grooms from the chat alone.** The user never
needs the tracker open to follow it: every ticket the plan names — routed, batched, blocked, or
proposed for closure — carries its id, its title, and a one-or-two-sentence digest drawn from its
body (what it is, and why it routes where it does when the routing turns on that). Relations are
said in words — "#12 blocks #14", "#7 is #5's last open child" — never bare id lists; a number by
itself is opaque. A body too thin to digest is presented as exactly that — thinness is a groom
finding, never a licence to invent a digest. Alongside the digests: the batches, and every proposed
tracker mutation (role labels, closures, new tickets, body rewrites) — and adjust to the user's
edits. Status reports carry the same discipline. The confirmation is the gate for all of it: until they approve, the tracker
is untouched and no thread exists. Then execute the approved mutations and, per approved batch: mark
its tickets shaping per the label roles — a ticket never gets two threads — prepare one batch worktree
via the `worktree` skill, and spawn one thread via the `to-thread` skill in that exact directory, named
for the batch, seeded with the ticket ids (subjects marked), the batch membership, and the instruction
to run the `shape` skill on them. This is also the one-batch path: the dispatcher never shapes in the
primary checkout. Record the batch id, base, branch, path, and intended thread owner on every ticket
before dispatch; that tracker record is the worktree ownership claim.

Report each thread and how to attach; status on request comes from the tracker and the harness's thread
listing. Inside the thread, shaping ends with a spec on each ticket. Readiness is batch-atomic and that
endgame belongs to the `shape` skill: a clean shaping worktree is removed, its branch is cleaned up,
and the whole batch becomes ready; a changed branch is committed and proposed as a shaping change
request and its exact head is presented before readiness is requested. The user's later readiness
blessing authorizes merging that shaping change only. The batch becomes ready only after that merge is
verified and its worktree is removed.

Any failure between marking the batch and a successful thread spawn ends the provisional claim: restore
the batch's former roles, record the failure on its tickets, and remove a clean prepared worktree. If
prepare or bootstrap left files, preserve the worktree and its ownership record for recovery while
restoring the roles; surface the exact path and blocker. Never fall back into the primary checkout.

**Hygiene rides the groom: the teardown sweep.** Every path that ends a ticket's work must also end its
worktree. Merge-path teardown belongs solely to the `merge-changes` skill's cleanup step, and abort-path
teardown to `backlog build` as it clears a claim — this sweep is the catch-all for what those owners
missed: merges landed outside the loop, dead runners, stacks that outlived their directories. Enumerate
from git's worktree listing joined with each branch's change-request state — never a directory scan. A
worktree whose change request is merged or closed is a teardown candidate; detect merged squash-proof —
the branch's upstream gone, or the change request's own recorded state — never a merge-base ancestor
check, which squash merges defeat. A candidate with a clean tree is reaped without asking, environment
before working copy per the environment playbook's teardown row; a dirty tree is surfaced for the user's
confirmation and never silently deleted — it may hold unpushed work, the same rule the policy's
branch-gone orphan sweep applies, and that sweep runs alongside this direction on its own quiet horizon. A
worktree whose branch is live with its change request open is left alone. Where the environment playbook
records container stacks, sweep one direction further: containers whose compose working-dir label points
at a path that no longer exists are orphaned stacks — surface them for teardown too.

## build

Sweep for tickets carrying the ready role whose dependency edges are clear **and that have no open
children** (the policy's open-children rule: a parent — a capstone over its slices — is dispatchable
only once every child is closed; the relation itself is the block, no wired edges needed), or take the
ids given.
Preflight once per run: the platform verbs and credentials the builds will lean on answer a cheap live
read — a dead one is drift, fixed by re-running `backlog setup` before any dispatch spends a build
discovering it. The preflight also runs this skill's `scripts/check-machine-facts.py` against the
repo — a stale stamped record or a missing declared overlay is the same drift, fixed by re-running
the owning setup before dispatch. For each ticket: mark it building per the label roles — a dispatched ticket must never
dispatch twice, and the claim comment carries this runner's identity per the policy's § Building
hygiene — prepare its worktree via the `worktree` skill, update the claim with its base, branch, path,
and this dispatcher as cleanup owner, then dispatch the `build` skill on it via the `to-subagent`
skill with that exact directory.
Isolation and concurrency follow the environment playbook's verdicts (`docs/agents/environment.md`
§ Worktree isolation, § Parallelism): under `serialize-verification`, parallel builds share the
serialized singleton through the playbook's lane mechanics; a repo that cannot provide worktree
isolation does not dispatch builds and hands the claim back with the capability gap surfaced. A spawn
the harness refuses queues its ticket for the next freed slot — the claim stands, the
spawn is not busy-retried.

The project owns isolation; harness-native worktrees are not requested. The primary checkout is never
switched, updated, or used for dispatched work. Fetch the recorded remote and resolve the playbook's
base ref without checking it out. Warn when the primary checkout is dirty, ahead, or behind because
that affects operator expectations, but do not mutate it. If the work exists only on an unpublished
local base, stop and ask for publication instead of silently seeding from that checkout. One build
worktree carries the entire `build` pipeline — implementation, verification, change request,
adversarial review, fixes, and evidence — and downstream skills must not create another worktree.

This session babysits the fleet: each build's completion wakes it, and it relays the outcome — the
review-ready change request, or the failure, with a died-silent build reported, never dropped. Each
dispatch also gets a deadline sized to the expected build — hours, far tighter than the multi-day
quiet horizon the orphan sweep uses: a build past it with no completion is checked — worktree, branch
tip, process — and respawned or reported, so a wedged build surfaces instead of sitting silent. **The tracker is the run ledger**: the claim comment and the
outcome comment are its events, so a dispatcher that dies or compacts mid-fleet reconstructs from
there — on resume, reconcile the claims this runner owns against live worktrees and branch tips before
dispatching anything new. Merging the resulting change requests waits for explicit authorization.

An abort ends the worktree with the claim: clearing a claim without a merge — a handback, a failed
build, a withdrawn dispatch — also removes that ticket's worktree through the `worktree` skill,
environment before working copy per the environment playbook's teardown row, so nothing the dispatch
created outlives it. Merge-path
teardown stays with the `merge-changes` skill; what both paths miss, groom's teardown sweep catches.

## setup

Load [setup](reference/setup.md): install or reconcile the project playbooks from `templates/`, then
verify the label roles exist in the tracker.
