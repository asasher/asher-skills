---
name: backlog
description: Groom all open tickets, dispatch ready builds, inspect progress, and run setup or retro for a GitHub repository.
disable-model-invocation: true
metadata:
  requires: [capture, shape, deliver, merge, retro, to-thread, agent-ready-codebase, to-web]
  optional: [technical-writing, writing-for-humans]
  setup: reference/setup.md
---

# Backlog

The tracker is the ledger. This dispatcher selects tickets, starts one thread per ticket, then exits. Read `docs/agents/environment.md` and [labels and claims](reference/labels.md); run setup if the playbook is missing. Use `technical-writing` for tracker records and `writing-for-humans` for conversation when available.

## groom

1. Read **all open tickets** in full, including comments, labels, dependencies, and active claims. Already-routed work is context, not permission to reset it.
2. First propose duplicates and consolidations. Work that needs shaping together becomes one ticket, preserving the contributing tickets' intent and links. Related work can remain separate. Protect active work and approved decisions.
3. Route the remaining unique tickets: clear enough to implement → `ready-for-agent`; missing product or scope decisions → `needs-shaping`; missing reporter facts → `needs-info`; human-only work → `ready-for-human`. Every ready ticket needs a work-type, observable acceptance, and a clear boundary between settled decisions and delegated choices.
4. Present one plan with each ticket's title, digest, disposition, and reason. Apply approved changes only; existing authorization counts. Offer how many shaping threads to start, default three.
5. For each selected ticket, record its work branch and dispatch via `to-thread`, requesting a worktree and `shape <ticket>`. Set `shaping`; confirm the new thread is running. On failed spawn, confirm no worker remains, restore the prior label, and preserve any work.

## build

1. Require a passing Agent-readiness record. Select `ready-for-agent` tickets with no open blocker or live owner. Explicit IDs still pass these gates.
2. Read the concurrent-build limit, default three. Count live builds and uncertain spawns; admit only available slots. Use one dispatch owner or the playbook's shared admission lock. Recheck before each claim.
3. Record the claim and replace `ready-for-agent` with `building`. Supply `to-thread` with the ticket's existing local or remote work branch, or its creation base: a child's spec branch, otherwise the configured base. Request one worktree and `deliver <ticket>`, carrying the claim deadline.
4. Confirm the thread is running before admitting another. If spawn fails, retain the reservation while liveness is uncertain. Once no worker remains, record failure, restore readiness, and retain committed or dirty work for recovery. Stop the wave on a shared environment or harness failure.

Push and readback belong to each ticket's owning thread. Another sweep handles work beyond this wave; no supervising session waits here.

## status

Join ticket claims, thread liveness, remote branches, worktree registrations, and PR records. Show each ticket's next action under **active**, **review-ready**, **stopped**, **abandoned**, or **merged**. Keep stalled live workers distinct from dead ones. Inspect unfinished split publications and unexplained working copies too.

A takeover requires the prior worker to be stopped. Record a superseding claim, then resume from pushed commits and the ticket/PR checkpoint, preserving unresolved decisions and review bounds. Expiry alone does not prove a worker stopped. Surface cleanup candidates; status itself deletes nothing.

## Other verbs

- **capture** → `capture` on the current conversation.
- **merge** → `merge review` for a read-only PR shortlist. Pass explicit merge selections through unchanged.
- **retro** → `retro` on the local friction ledger.
- **setup** → [setup](reference/setup.md), reconciling [the environment template](templates/environment.md).
