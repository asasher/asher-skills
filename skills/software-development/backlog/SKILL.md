---
name: backlog
description: The software backlog dispatcher — groom routes and fans shaping threads, build claims and fans build threads, status queries the fleet, setup binds and certifies.
disable-model-invocation: true
metadata:
  requires: [build-change, shape, to-thread, worktree]
  optional: [merge-change, writing-for-humans, technical-writing, retro, agent-ready-codebase]
  setup: reference/setup.md
---

# Backlog

A dispatcher with no supervisor; the tracker is the run ledger.

Nouns are roles: _ticket_, _label_, _change request_ are bound to this repo's real tracker, review surface, and version control by `docs/agents/platform.md`; label roles, dependency edges, deadlines, and readiness by `docs/agents/backlog-policy.md`; the repo's agent-readiness answers by `docs/agents/environment.md`. Missing playbooks: run `backlog setup` first — don't improvise them.

Chat text follows the `writing-for-humans` sibling — groom plans and status reports are its densest consumers here. Tracker writes (ticket bodies, merged bodies) follow the `technical-writing` sibling. Absent either sibling, write plainly and say the standard was not loaded.

**Friction is noted as it happens.** A stumble in this loop — an instruction misread, a confirmation the user had to repeat, a stale playbook row, a workaround that shouldn't have been needed — is recorded the moment it shows via the `retro` sibling's note verb, and a run's end is the sweep for anything unnoted. When the note verb reports a retro pass due, relay that report and stop — running the pass is never this dispatcher's call. Absent the `retro` sibling, friction goes unrecorded: say so once when there was something worth noting, then move on.

## groom

Sweep the tracker for tickets carrying **no readiness role** — however else they are labeled: a captured ticket arrives work-typed but unrouted — and tickets carrying the needs-shaping role, or take the ids given. Route first — as a plan, not as writes: a ticket whose decisions are already settled routes to `ready-for-agent`, one owing reporter facts to `needs-info`, human-only work to `ready-for-human`, per the label roles, a duplicate or dead ticket to closure — the rest are shaping work. Two judgments shape that rest. **Merges:** many small related tickets absorb into one shapeable subject — one ticket carries the merged body; the others close as duplicates pointing at it. Absorption is safe because slicing exists: `to-slices` re-creates structure from the settled spec on the way out, informed by decisions the fragments couldn't carry. **Subjects:** what remains groups so that tickets whose decisions interlock shape together, one subject per thread.

**Confirm before anything changes — with a plan that grooms from the chat alone.** The user never needs the tracker open to follow it: every swept ticket appears in the plan exactly once — routed, merged, blocked, proposed for closure, or held with the reason — each carrying its id, its title, and a one-or-two-sentence digest drawn from its body (what it is, and why it routes where it does when the routing turns on that). Relations are said in words — "#12 blocks #14", "#7 absorbs #9 and #11" — never bare id lists; a number by itself is opaque. A body too thin to digest is presented as exactly that — thinness is a groom finding, never a licence to invent a digest. Alongside the digests: the subjects, the proposed merges, and every proposed tracker mutation (role labels, closures, merged bodies, new tickets) — and adjust to the user's edits. The confirmation is the gate for all of it: until the user approves, the tracker is untouched and no thread exists.

A subject parked at `shape`'s experience handoff routes to a thread for its remaining implementation decisions. Then execute the approved mutations and **ask how many shaping threads to start now — default 3.** Shaping needs the user's attention, so width belongs to them; the unstarted remainder stays routed in the tracker for the next groom or a "start two more." Per started subject: mark its tickets shaping per the label roles — a ticket never gets two threads — prepare one worktree via the `worktree` skill **on the ticket's work branch** (created from the base ref, named per the platform binding), and spawn one thread via the `to-thread` skill in that exact directory, named for the subject, seeded with the ticket ids and the instruction to run the `shape` skill on them. Record the base, branch, path, and thread name on the subject's tickets before dispatch. This is also the one-subject path: the dispatcher never shapes in the primary checkout. Report each thread and how to attach. Inside the thread, shaping ends with a spec on each ticket, blessed at a commit hash; shaping opens no change request, and its pushed work branch, context commits included, is the handoff `build-change` later continues on.

Any failure between marking a subject and a successful thread spawn rolls the provisional dispatch back: restore the former roles, record the failure on the tickets, and remove a clean prepared worktree. If prepare or bootstrap left files, preserve the worktree and its recorded facts for recovery while restoring the roles; surface the exact path and blocker. Never fall back into the primary checkout.

**Hygiene rides the groom:** end every groom with the teardown sweep (§ teardown sweep).

## build

Pull, not push. Sweep for tickets carrying `ready-for-agent` whose dependency edges are clear and whose children are all closed or `delivered` (the policy's open-children rule), or take the ids given. Skip any ticket with a live claim — re-running `backlog build` is idempotent, and the claim, not a queue, is what prevents double dispatch. Fan-out is bounded by readiness alone — groom's gate sizes the sweep; each thread rides the dispatching session's model and effort, and staffing prices only the subagents inside a build.

The gate is agent-readiness: the repo is certified against the `agent-ready-codebase` reference sibling's checklist, its answers recorded in `docs/agents/environment.md` § Agent-readiness — a full pass, or build does not dispatch: parallel-safe or not ready. A missing or failed certification hands the tickets back with the gap surfaced — re-run `backlog setup` to re-certify; punch-list gaps are groomable tickets.

For each ticket: post the **dispatch declaration as the claim comment** — one event, two audiences: the human reads a statement, never a question, and any later runner reads the claim. It carries the declaration fields per the policy's `building` role, the deadline as an **absolute timestamp** sized per the policy's deadline section. Then materialize the worktree via the `worktree` skill **from the ticket's recorded work branch at the remote** (shaping's context commits ride it; a ticket with no recorded branch gets one from the base ref), fan one thread via the `to-thread` skill in that exact directory running the `build-change` skill, and move on. When the sweep ends, **exit** — never babysit; outcomes land on the tracker as each build's outcome comment, and `backlog status` is how anyone reads the fleet.

Never dispatch from or mutate the primary checkout. Fetch the recorded remote and resolve the playbook's base ref without checking it out; warn when the primary checkout is dirty, ahead, or behind — that affects operator expectations — but do not touch it. Work that exists only on an unpublished local base stops for publication rather than silently seeding from that checkout. One worktree carries the entire `build-change` pipeline — implementation, verification, change request, review, evidence — and downstream skills must not create another. Merging the resulting change requests stays a separate, explicit human authorization — the `merge-change` skill.

## status

The report is a pure query — it never invents state; the only writes are the teardown action arm's. Join four sources: the tracker's claims with the deadlines read from them, live worktrees and branch tips, change-request state, and the harness's thread listing. Report, per the plan discipline groom uses — ids with titles and digests, relations in words:

- **Finished** — a claim whose change request is review-ready or merged.
- **Stalled past deadline** — a claim past its absolute deadline whose thread is still observably alive: report it, don't touch it — a slow build may still land.
- **Abandoned** — derived, never written: the building role, deadline passed, and the thread not observably alive (dead thread listing, no branch activity).
- **Orphans** — worktrees and container stacks no live claim explains.

Every live claim and every listed worktree lands in exactly one bucket; anything unclassifiable is reported as such, never dropped.

Reclaim rules: audit reality first, then adopt committed work — a reclaim resumes from the branch, never from scratch, so nothing is discarded. A reclaim is a new claim comment superseding the old; the ledger stays event-shaped: claim, outcome, reclaim. Another actor's expired claim is not this runner's to clear — leave the takeover note on the ticket per the policy's § Building hygiene. The tracker records **transitions, never telemetry** — no heartbeats, no progress comments; liveness is checked at read time. A claim that predates deadlines falls back to the policy's quiet-horizon backstop.

The action arm is the teardown sweep (§ teardown sweep), run when the query surfaces candidates or on request.

## teardown sweep

Every path that ends a ticket's work must also end its worktree. Merge-path teardown belongs solely to the `merge-change` skill's cleanup step, and abort-path teardown to the thread that owns the worktree — this sweep is the catch-all for what those owners missed: merges landed outside the loop, dead runners, stacks that outlived their directories. Enumerate from git's worktree listing joined with each branch's change-request state — never a directory scan. A worktree whose change request is merged or closed is a teardown candidate; detect merged squash-proof — the branch's upstream gone, or the change request's own recorded state — never a merge-base ancestor check, which squash merges defeat. A candidate with a clean tree is reaped without asking, through the `worktree` skill's Remove — the owner of the teardown order and its refusals; a dirty tree is surfaced for the user's confirmation and never silently deleted — it may hold unpushed work, the same rule the policy's orphan sweep applies on its quiet horizon. A worktree whose branch is live with its change request open is left alone. Where the environment playbook records container stacks, sweep one direction further: containers whose compose working-dir label points at a path that no longer exists are orphaned stacks — surface them for teardown too.

## setup

Load [setup](reference/setup.md).
