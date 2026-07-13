---
name: staffing
description: Own the model roster for a machine and its projects — who staffs which task. Use to install or reconcile the roster, add a project override, or resolve any "which model should do this?" question — directly or from a sibling skill. Not for running the task itself.
argument-hint: "[setup | route <task> | reconcile]"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
  setup: reference/setup.md
---

# Staffing

Compiles machine-observed models into one roster of roles, pins, capability gates, rankings, reachability,
and successors. It selects a route; it does not run the task or ship a fixed machine roster.

## Commands

- **setup** — load [setup](reference/setup.md); audit reachability and reconcile only the consented base/delta layers.
- **route `<task>`** — load [rankings-and-routing](reference/rankings-and-routing.md) and, for roles or route
  loss, [roles-and-fallback](reference/roles-and-fallback.md).
- **reconcile** — load [install-and-reconcile](reference/install-and-reconcile.md); compare installed rules
  with the current machine and report drift/conflict without version stamps.

No argument runs setup.

## Resolution

Issue-coordinator callers first supply work type, surface/capabilities, coordination class/reason, and known
uncertainty. Missing fields stop dispatch; `orchestrator-required` returns the orchestrator; `routine` uses
the reachable coordinator-eligible set. Then:

1. apply matching task/capability pin and stop;
2. filter hard capability and taste gates;
3. rank survivors by `intelligence > taste > cost`;
4. on route loss, apply the recorded successor and rerun over reachable candidates.

Never rank before gates or choose routine coordination cheapest-first. If no model is reachable, use the
current model in a subagent and report the gap; never skip the stage.

## Layers and sibling harnesses

The user chooses project-only or a consented harness-specific global base plus sparse project deltas. Existing
bases are preserved unless separately requested. Reachability is directional and effect-verified:
Claude→Codex may use tracked `codex exec`; Codex→Claude may use bounded `claude -p` with closed stdin and no
`--bare`. One failed direction produces an asymmetric graph; no policy monitor gates either route.

## Dependency surface

- **Bundled:** setup, audit, routing, roles/fallback, and install/reconcile references.
- **Project/global:** roster base and delta playbooks written by setup with the user's scope consent.
- **Siblings:** none; staffing is a model-invoked root primitive and imports no skill files.
