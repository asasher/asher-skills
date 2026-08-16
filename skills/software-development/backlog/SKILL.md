---
name: backlog
description: Dispatch the backlog — groom routes tickets, merges fragments into shapeable subjects, and fans confirmed subjects into shaping threads; build claims ready tickets, posts each dispatch declaration as the claim, fans one build thread per ticket, and exits; status is the pure query over claims, worktrees, change requests, and deadlines. Setup binds the platform, records the choices, and certifies agent-readiness.
argument-hint: "[groom | build | status | setup] [ticket ids]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: [build-change, shape, to-subagent, to-thread, worktree]
  optional: [merge-change, retro]
  setup: reference/setup.md
---

# Backlog

A dispatcher with no supervisor. Grooming is interactive — judgment behind a confirmation gate, then human-attended shaping threads fan out. Building is pull, not push: build claims, declares, fans out, and exits; outcomes land on the tracker, and anyone reads them there. Status is the query that joins the ledger to reality. The tracker is the run ledger — claims, outcomes, reclaims: transitions, never telemetry.

Nouns are roles: _ticket_, _label_, _change request_ are bound to this repo's real tracker, review surface, and version control by `docs/agents/platform.md`; label roles, dependency edges, deadlines, and readiness by `docs/agents/backlog-policy.md`; the repo's agent-readiness answers by `docs/agents/environment.md`. Missing playbooks: run `backlog setup` first — don't improvise them.

User-facing text follows the `writing-for-humans` sibling — groom plans and status reports are its densest consumers here. Absent that sibling, write plainly and say the standard was not loaded.

**Friction is noted as it happens.** A stumble in this loop — an instruction misread, a confirmation the user had to repeat, a stale playbook row, a workaround that shouldn't have been needed — is recorded the moment it shows via the `retro` sibling's note verb, and a run's end is the sweep for anything unnoted. When the note verb reports a retro pass due, relay that report and stop — running the pass is never this dispatcher's call. Absent the `retro` sibling, friction goes unrecorded: say so once when there was something worth noting, then move on.

## groom

Sweep the tracker for tickets carrying **no readiness role** — however else they are labeled: a captured ticket arrives work-typed but unrouted — and tickets carrying the needs-shaping role, or take the ids given. Route first — as a plan, not as writes: a ticket whose decisions are already settled routes to the ready role, one owing reporter facts or human-only work to its parked role per the label roles, a duplicate or dead ticket to closure — the rest are shaping work. Two judgments shape that rest. **Merges:** many small related tickets absorb into one shapeable subject — one ticket carries the merged body; the others close as duplicates pointing at it. Absorption is safe because slicing exists: `to-slices` re-creates structure from the settled spec on the way out, informed by decisions the fragments couldn't carry. **Subjects:** what remains groups so that tickets whose decisions interlock shape together, one subject per thread.

**Confirm before anything changes — with a plan that grooms from the chat alone.** The user never needs the tracker open to follow it: every ticket the plan names — routed, merged, blocked, or proposed for closure — carries its id, its title, and a one-or-two-sentence digest drawn from its body (what it is, and why it routes where it does when the routing turns on that). Relations are said in words — "#12 blocks #14", "#7 absorbs #9 and #11" — never bare id lists; a number by itself is opaque. A body too thin to digest is presented as exactly that — thinness is a groom finding, never a licence to invent a digest. Alongside the digests: the subjects, the proposed merges, and every proposed tracker mutation (role labels, closures, merged bodies, new tickets) — and adjust to the user's edits. The confirmation is the gate for all of it: until the user approves, the tracker is untouched and no thread exists.

Then execute the approved mutations and **ask how many shaping threads to start now — default 3.** Shaping needs the user's attention, so width belongs to them; the unstarted remainder stays routed in the tracker for the next groom or a "start two more." Per started subject: mark its tickets shaping per the label roles — a ticket never gets two threads — prepare one worktree via the `worktree` skill, and spawn one thread via the `to-thread` skill in that exact directory, named for the subject, seeded with the ticket ids and the instruction to run the `shape` skill on them. Record the base, branch, path, and thread name on the subject's tickets before dispatch; that record is the worktree ownership claim. This is also the one-subject path: the dispatcher never shapes in the primary checkout. Report each thread and how to attach. Inside the thread, shaping ends with a spec on each ticket, blessed at a commit hash — readiness and teardown are the `shape` skill's endgame; no shaping branch ever merges.

Any failure between marking a subject and a successful thread spawn ends the provisional claim: restore the former roles, record the failure on the tickets, and remove a clean prepared worktree. If prepare or bootstrap left files, preserve the worktree and its ownership record for recovery while restoring the roles; surface the exact path and blocker. Never fall back into the primary checkout.

**Hygiene rides the groom: the teardown sweep** — also the action arm of `backlog status`. Every path that ends a ticket's work must also end its worktree. Merge-path teardown belongs solely to the `merge-change` skill's cleanup step, and abort-path teardown to the thread that owns the worktree — this sweep is the catch-all for what those owners missed: merges landed outside the loop, dead runners, stacks that outlived their directories. Enumerate from git's worktree listing joined with each branch's change-request state — never a directory scan. A worktree whose change request is merged or closed is a teardown candidate; detect merged squash-proof — the branch's upstream gone, or the change request's own recorded state — never a merge-base ancestor check, which squash merges defeat. A candidate with a clean tree is reaped without asking, through the `worktree` skill's Remove — the owner of the teardown order and its refusals; a dirty tree is surfaced for the user's confirmation and never silently deleted — it may hold unpushed work, the same rule the policy's orphan sweep applies on its quiet horizon. A worktree whose branch is live with its change request open is left alone. Where the environment playbook records container stacks, sweep one direction further: containers whose compose working-dir label points at a path that no longer exists are orphaned stacks — surface them for teardown too.

## build

Pull, not push. Sweep for tickets carrying the ready role whose dependency edges are clear and whose children are all closed or `delivered` (the policy's open-children rule), or take the ids given. Skip any ticket with a live claim — re-running `backlog build` is idempotent, and the claim, not a queue, is what prevents double dispatch. There is no concurrency cap and no quota gate: groom's readiness gate is the budget, and correct staffing is the cost control.

The gate is agent-readiness: the repo is certified against the `agent-ready-codebase` reference sibling's checklist, its answers recorded in `docs/agents/environment.md` § Agent-readiness — a full pass, or build does not dispatch. No serialize modes, no lanes: parallel-safe or not ready. A missing or failed certification hands the tickets back with the gap surfaced — re-run `backlog setup` to re-certify; punch-list gaps are groomable tickets.

For each ticket: post the **dispatch declaration as the claim comment** — one event, two audiences: the human reads a statement, never a question, and any later runner reads the claim. It carries the ticket digest, the branch, the worktree path, the model, the effort, the harness, the thread name, the dispatcher's identity, and the deadline as an **absolute timestamp** — any machine must be able to rule on it, and in the pull model the deadline has nowhere else to live; size it per the policy's deadline section. Then prepare the worktree via the `worktree` skill, fan one thread via the `to-thread` skill in that exact directory running the `build-change` skill, and move on. When the sweep ends, **exit** — no babysitting, no wakes, no completion relay. Outcomes land on the tracker as each build's outcome comment; `backlog status` is how anyone reads the fleet.

Never dispatch from or mutate the primary checkout. Fetch the recorded remote and resolve the playbook's base ref without checking it out; warn when the primary checkout is dirty, ahead, or behind — that affects operator expectations — but do not touch it. Work that exists only on an unpublished local base stops for publication rather than silently seeding from that checkout. One worktree carries the entire `build-change` pipeline — implementation, verification, change request, review, evidence — and downstream skills must not create another. Merging the resulting change requests stays a separate, explicit human authorization — the `merge-change` skill.

## status

A pure query — it writes nothing except through its action arm, and it never invents state. Join four sources: the tracker's claims with the deadlines read from them, live worktrees and branch tips, change-request state, and the harness's thread listing. Report, per the plan discipline groom uses — ids with titles and digests, relations in words:

- **Finished** — a claim whose change request is review-ready or merged.
- **Stalled past deadline** — a claim past its absolute deadline whose thread is still observably alive: report it, don't touch it — a slow build may still land.
- **Abandoned** — derived, never written: the building role, deadline passed, and the thread not observably alive (dead thread listing, no branch activity). Liveness decides, not the clock alone; there is no abandoned label.
- **Orphans** — worktrees and container stacks no live claim explains.

Reclaim rules: audit reality first, then adopt committed work — a reclaim resumes from the branch, never from scratch, so nothing is discarded. A reclaim is a new claim comment superseding the old; the ledger stays event-shaped: claim, outcome, reclaim. Another actor's expired claim is not this runner's to clear — leave the takeover note on the ticket per the policy's § Building hygiene. The tracker records **transitions, never telemetry** — no heartbeats, no progress comments; liveness is checked at read time. A claim that predates deadlines falls back to the policy's quiet-horizon backstop.

The action arm is the teardown sweep defined under groom — the same enumeration, the same squash-proof merged detection, the same rule that a dirty tree is surfaced and never silently deleted — run when the query surfaces candidates or on request.

## setup

Load [setup](reference/setup.md). Three jobs, and never a cache of machine state — the readiness standard lives in the `agent-ready-codebase` reference sibling:

1. **Bindings** → `docs/agents/platform.md`: tracker verbs, change-request verbs including the `delivered` mechanics, version-control conventions including feature branches and the `artifact/` prefix, and the artifact store — bucket, base URL, credential env-var names, upload command; visibility is fixed: public with unguessable keys.
2. **Choices** → `docs/agents/backlog-policy.md`: the role→label map, the work domain, readiness autonomy, deadline sizing, the quiet horizon.
3. **Certification** → `docs/agents/environment.md`: walk the `agent-ready-codebase` checklist and write the answers and the punch list; punch-list gaps are groomable tickets.
