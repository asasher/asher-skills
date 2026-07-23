---
name: staffing
description: Own the model roster for a machine and its projects. Use to install or reconcile the roster, add a project override, or resolve any "which model should do this?" question — directly or from a sibling skill. Not for running the task itself.
argument-hint: "[setup | route <task> | reconcile]"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
  setup: reference/setup.md
  variants: {"claude":"variants/claude","codex":"variants/codex"}
---

# Staffing

Compiles machine-observed models into one roster of roles, pins, capability providers, rankings, reachability,
and successors. It selects a route; it does not run the task or ship a fixed machine roster.

## Commands

- **setup** — load [setup](reference/setup.md); audit reachability and reconcile only the consented base/delta layers.
- **route `<task>`** — load [rankings-and-routing](reference/rankings-and-routing.md) and, for roles or route
  loss, [roles-and-fallback](reference/roles-and-fallback.md).
- **reconcile** — load [install-and-reconcile](reference/install-and-reconcile.md) and the active provider's
  [harness mechanics](reference/harness.md); compare installed rules with the current machine and report
  drift/conflict without version stamps.

No argument runs setup.

## Resolution

Issue-coordinator callers first supply work type, surface/capabilities, coordination class/reason, and known
uncertainty. Missing fields stop dispatch; `orchestrator-required` returns the orchestrator; `routine` uses
the reachable coordinator-eligible set. Then:

1. apply a matching task/provider pin, subject to effect verification;
2. resolve any required effect to a named provider/fallback and filter to eligible executors, then apply the
   hard taste gate;
3. rank survivors by `intelligence > taste > cost`;
4. on route loss, apply the recorded successor and rerun over reachable candidates.

Never rank before gates or choose routine coordination cheapest-first. If no model is reachable, use the
current model in a subagent and report the gap; never skip the stage.

## Layers and sibling harnesses

The user chooses project-only or a consented harness-specific global base plus sparse project deltas. Existing
bases are preserved unless separately requested. Reachability is directional and effect-verified. For
cross-harness routing or delegation, load the active installed
package's `reference/harness.md`; provider compilation supplies that file without changing this shared public
contract.

## Dependency surface

- **Bundled:** setup, audit, routing, roles/fallback, install/reconcile, and compiled provider mechanics.
- **Project/global:** roster base and delta playbooks written by setup with the user's scope consent.
