---
name: manage-tasks
description: Reconcile workspace tasks and the daily Start Work / Stop Work lifecycle. Use when a task is created, completed, deferred, blocked, scheduled, or moved in TODO.md, a Project, or an Opportunity, when opening or closing a work day, or when another skill needs task vocabulary or the Project Note Shape.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: [manage-opportunities]
---

# Manage Tasks

Own task vocabulary, task movement, the daily lifecycle, and the Project Note Shape. A task has one stable
`🆔` and one origin: either a Project or an Opportunity. Load [task contract](reference/task-contract.md)
before changing tasks and [Project Note Shape](reference/project-note-shape.md) when creating or validating a
Project.

## Commands

- **Start Work** - open today's `TODO.md` and activate due, planned, or named tasks.
- **Stop Work** - close the open day and return unfinished work to its origin.
- **task change** (default) - create, move, complete, cancel, schedule, or update one task under the same
  contract.

If `TODO.md` opens on a date older than today, run Stop Work for that date before Start Work for today.

## Start Work

1. Move completed and elapsed scheduled tasks from `TODO.md` to the `## Done` section of their recorded
   Project or Opportunity origin. Preserve identity and metadata.
2. Set the first level-two heading to today's ISO date.
3. For every Project and Opportunity backlog, move each unblocked task due or planned today or earlier, plus
   every task named by the user, into the matching origin heading in `TODO.md`.
4. Pull repo-owned issue reminders only for Projects whose Project note and repo playbook bind that tracker.
5. Audit all moved IDs. Each occurs in exactly one task location and every blocker resolves.

Completion criterion: today's file is open; every due, planned, or named unblocked task is active; and each
moved task exists once under its original Project or Opportunity.

## Stop Work

1. Move every deferred task from `TODO.md` back to its origin `## Backlog` as open. A Project task returns to
   its Project; an Opportunity task returns to its Opportunity.
2. Ensure in-progress, done, and cancelled tasks carry their required dates.
3. Move done and cancelled tasks into the origin `## Done`, grouped by completion date newest first.
4. Resolve implicit dependencies to stable IDs and attach findable calendar links to scheduled tasks.
5. Audit all touched IDs across `TODO.md`, Project backlogs, and Opportunity backlogs/done sections.

Completion criterion: no deferred task remains in `TODO.md`; every task is in exactly one valid location;
and every active heading resolves to one origin note.

## Boundaries

- `manage-opportunities` owns Opportunity Note Shape, stages, and next-action designation. When installed,
  invoke it by name for those mutations; when absent, move existing Opportunity tasks but do not invent or
  reshape Opportunity records.
- Project repositories own their issue status when their local `backlog` skill and platform playbook say so.
  Workspace copies are daily reminders, not a second tracker.
- Do not commit a dirty workspace as a lifecycle precondition. Commit only when the user or the surrounding
  repository workflow requests one, and never absorb unrelated changes.

## Dependency surface

- **Bundled references:** task vocabulary/movement and Project Note Shape.
- **Project playbooks:** repository tracker bindings named by each Project's local repository.
- **Sibling skills:** optional `manage-opportunities`, invoked by name for Opportunity shape and lifecycle.
