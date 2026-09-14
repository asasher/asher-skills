---
name: backlog
description: Groom tickets, build frontiers or spec and milestone waves, inspect progress, recap what shipped in HTML, and run setup or retro.
disable-model-invocation: true
metadata:
  requires: [capture, shape, deliver, merge, retro, to-thread, agent-ready-codebase, to-web]
  optional: [technical-writing, writing-for-humans]
  setup: reference/setup.md
---

# Backlog

The tracker is the ledger. Groom dispatches selected shaping threads; build coordinates one owning thread per ticket. For recap, go directly to its reference below. For other verbs, read `docs/agents/environment.md` and [labels and claims](reference/labels.md); run setup if the playbook is missing. Use `technical-writing` for tracker records and reports and `writing-for-humans` for conversation when available.

The human operator controls concurrency for shaping and building. Apply a concurrency limit only when the operator specifies one.

## groom

1. Read **all open tickets** in full, including comments, labels, milestones, dependencies, and active claims. Preserve active routing and use it as context.
2. First propose duplicates and consolidations. Work that needs shaping together becomes one ticket, preserving the contributing tickets' intent and links. Related work can remain separate. Preserve batch membership and replacement links under [milestone grouping](reference/milestones.md). Include incoming and outgoing native dependencies in the consolidation plan; apply the closure gate in [labels and claims](reference/labels.md). Preserve active ownership and approved decisions.
3. Route the remaining unique tickets: clear enough to implement → `ready-for-agent`; missing product or scope decisions → `needs-shaping`; missing reporter facts → `needs-info`; human-only work → `ready-for-human`. Every ready ticket needs a work-type, observable acceptance, and a clear boundary between settled decisions and delegated choices.
4. Present one plan with each ticket's title, digest, disposition, and reason, plus any milestone changes or completed-batch closures. Apply approved changes only; existing authorization counts.
5. For each selected ticket, record its work branch and dispatch via `to-thread`, requesting a worktree and `shape <ticket>`. Set `shaping`; confirm the new thread is running. On failed spawn, confirm no worker remains, restore the prior label, and preserve any work.

## build

| Selection | Scope |
| --- | --- |
| `backlog build` | The current frontier: tickets eligible at invocation. |
| `backlog build <ids>` | The named tickets' current frontier. A single approved spec ticket selects its whole spec. |
| `backlog build spec <ticket>` | The approved spec ticket and its approved descendants, through integration and promotion. |
| `backlog build milestone <name-or-number>` | The milestone's tickets and their approved split descendants. |

1. Require a passing Agent-readiness record. Resolve the selection; the frontier contains `ready-for-agent` tickets with no open blockers. Dispatch also requires no live or uncertain owner; explicit selections pass these gates. Record the scope and initial frontier in this thread; keep undispatched tickets queued.
2. Recheck eligibility and ownership before each dispatch. Record the claim and replace `ready-for-agent` with `building`. Supply `to-thread` with the existing local or remote work branch, or its creation base: the parent spec branch for an approved split child, otherwise the configured base. Request one worktree and `deliver <ticket>`, carrying the claim deadline.
3. Confirm each launch. On failure, retain the ticket claim while liveness is uncertain. Once no worker remains, record failure, release the claim, restore readiness, and hold that ticket for recovery until its cause is resolved. Stop dispatch on a shared environment or harness failure.
4. Observe worker liveness and ticket/PR outcomes through events or bounded polling, up to their recorded deadlines or an earlier user deadline. Dispatch queued tickets as any operator-specified limit permits, rechecking eligibility and ownership. Account for each ticket as review-ready, merged, active, or blocked; report the next actor for stops. Resume existing work under `status`'s takeover rules, preserving worker deadlines and review budgets.

The default ends when each initial ticket is review-ready, merged, or stopped for a substantive blocker. At a deadline or when progress needs outside action, checkpoint the pending queue and live claims as a resumable wait. Newly unblocked tickets belong to the next invocation. For a spec or milestone, follow [successive waves](reference/build-waves.md) until completion or a recorded wait. Push, verification, and evidence belong to each ticket's owning thread.

## status

Join ticket claims, thread liveness, remote branches, worktree registrations, and PR records. Show each ticket's next action under **active**, **review-ready**, **stopped**, **abandoned**, or **merged**. Keep stalled live workers distinct from dead ones. Inspect unfinished split publications and unexplained working copies too. Report milestone progress and closure candidates under [milestone grouping](reference/milestones.md).

A takeover requires the prior worker to be stopped. Record a superseding claim, then resume from pushed commits and the ticket/PR checkpoint, preserving unresolved decisions and review bounds. Verify liveness even after claim expiry. Report cleanup candidates for a separate cleanup action.

## recap

`backlog recap [time range]` creates a standalone HTML report of what shipped, written for someone who does not read code. Accept natural ranges such as `last week`, `last month`, `last 6 months`, or explicit dates; default to the past week. Follow [recap](reference/recap.md) for time boundaries, delivery evidence, plain-language explanations, and the HTML handback. This verb reads project history and writes the report; it requires no setup or readiness certification.

## Other verbs

- **capture** → `capture` on the current conversation.
- **merge** → `merge review` for a read-only PR shortlist. Pass explicit merge selections through unchanged.
- **retro** → `retro` over recent local build and shaping sessions, proposing project issues for user selection.
- **setup** → [setup](reference/setup.md), reconciling [the environment template](templates/environment.md).
