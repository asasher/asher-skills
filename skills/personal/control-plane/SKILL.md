---
name: control-plane
description: Run the personal workspace control plane to reconcile the prior day, pull and ingest intake, pulse opportunity next actions, open today's work, optionally refresh the cash runway, and report one brief.
argument-hint: "[setup | morning | runway | communications | review-opportunities | projects-triage]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: [capture-to-inbox, manage-notes, manage-opportunities, manage-tasks]
  optional: [manage-communications, projects-triage, review-opportunities, until-zero]
  setup: reference/setup.md
---

# Control Plane

Thin orchestration over workspace owners. It owns sequence, gates, cadence, and the final brief; sibling
skills retain every domain contract and mutation.

## Commands

- **No argument / `morning`** - load [morning-run](reference/morning-run.md) and run the complete sequence.
- **`setup`** - load [setup](reference/setup.md) and reconcile control-plane bindings.
- **`runway`** - explicitly invoke the optional `until-zero` sibling to refresh and report the cash runway.
- **`communications`** - explicitly invoke the optional `manage-communications` sibling for due project
  updates or the internal digest. Do not include it silently in a morning run.
- **`review-opportunities`** - explicitly invoke the optional `review-opportunities` sibling for the full
  portfolio audit. Do not substitute the daily pulse.
- **`projects-triage`** - explicitly invoke the optional `projects-triage` sibling for repository backlog
  dispatch. Do not include it silently in a morning run.

Read [cadence](reference/cadence.md) when configuring or changing scheduled runs. A missing required sibling
stops the affected phase and is reported; a missing optional sibling affects only its configured or explicit phase.

## Dependency Surface

- **Bundled:** morning sequence, setup, and cadence references.
- **Project:** consumer-owned `control-plane/config.json`, state, and optional `docs/agents/control-plane.md`
  bindings.
- **Siblings:** required `capture-to-inbox`, `manage-notes`, `manage-opportunities`, and `manage-tasks`;
  optional `manage-communications`, `projects-triage`, `review-opportunities`, and `until-zero`, all invoked by
  name without file imports.
