---
name: staffing
description: Own the model roster for a project. Use to write or reconcile the project's staffing playbook, re-probe reachability after a CLI or machine change, or resolve any "which model should do this?" question — directly or from a sibling skill. Not for running the task itself.
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

- **setup** — load [setup](reference/setup.md); audit reachability and write or reconcile the project's staffing playbook.
- **route `<task>`** — load [rankings-and-routing](reference/rankings-and-routing.md) and, for roles or route
  loss, [roles-and-fallback](reference/roles-and-fallback.md).
- **reconcile** — load [install-and-reconcile](reference/install-and-reconcile.md) and the active provider's
  [harness mechanics](reference/harness.md); compare installed rules with the current machine and report
  drift/conflict in prose.

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

## Where the roster lives

**The project's staffing playbook is the sole authority.** Resolution reads it and nothing else. There is one
layer, not two: no machine-level module, and no bundled roster consulted at runtime.

The bundled roster is a **seed** — setup reads it once, when writing the playbook, and never again. A seed
value that survives into the playbook does so because the audit verified it, not because it shipped.

Absent a project playbook, **never resolve from the seed** and never reach for a home-directory path: its rows
are unverified defaults, and staffing from them asserts a reachability nobody checked. That is a bar on
*fabricating* a roster, not a hard stop on the work — degrade as
[roles-and-fallback](reference/roles-and-fallback.md) directs, running the delegated step on the current model
in a subagent and reporting the staffing gap. Run `staffing setup` to close it.

The playbook carries **data**: model rows, per-harness eligibility and capability bindings, pins, floor,
succession, probed reachability, and the machine the probes ran on. It never carries doctrine. Ranking and
succession rules live in [rankings-and-routing](reference/rankings-and-routing.md) and
[roles-and-fallback](reference/roles-and-fallback.md); harness command shapes, wrapper discipline, and wake
mechanics live in the compiled provider's [harness mechanics](reference/harness.md). Those are identical on
every machine, so they ship with the skill and are reviewed with it.

One playbook serves every harness — a Codex session and a Claude session read the same file, and facts that
differ between them are a column, not a second file. Reachability is directional and effect-verified: a
failure removes one direction, never both.

A playbook whose recorded machine is not this machine is stale. Re-run setup before dispatching rather than
trusting rows probed elsewhere.

## Dependency surface

- **Bundled:** setup, audit, routing, roles/fallback, install/reconcile, compiled provider mechanics, and the
  roster seed.
- **Project playbooks:** the staffing playbook under the repo's agent-docs directory — the sole runtime
  authority, written by setup.
- **Sibling skills:** none — `staffing` is a root primitive. Siblings invoke it; it invokes none, so there is
  no closure to carry and nothing to degrade when a sibling is absent.
