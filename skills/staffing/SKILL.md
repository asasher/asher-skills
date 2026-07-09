---
name: staffing
description: Own the model roster for a machine and its projects — who staffs which task. A global-capable primitive that audits which models the current harness can reach, writes a rankings table, a separate capability matrix, and a task-pin list, then resolves any "which model should do this?" question by a fixed order (pin → capability gate → intelligence>taste>cost tie-break → fallback ladder). Invoked by name by sibling skills (plan, prototype, backlog) and directly by a user setting up or asking a staffing question. Use to install the roster, add a project override, resolve a routing question, or reconcile a drifted install. Not for writing the task itself — only for deciding who runs it.
argument-hint: "[setup | route <task> | reconcile]"
user-invocable: true
---

# Staffing

Staffing owns the machinery that answers one question consistently everywhere: **given a task, which model
should run it?** The rules that answer it — roles, a rankings table, a capability matrix, task-pins, and a
fallback ladder — live in one place so the same roster serves any workflow skill, an ad-hoc session, any
harness, and anyone who installs from the public repo. It is a configuration/operator primitive, not advice:
it writes roster rules into harness memory (with consent) and resolves routing questions against them.

The roster is **compiled from a machine audit, never hardcoded.** What models exist and what they cost/are
worth differs per machine and per person, so the skill probes the current environment at install time and
writes the table from that. No fixed machine-specific roster ships as authoritative.

## Command surface

- **`setup`** — audit the environment, decide scope (global base vs project override), and write the roster.
  Load [install-and-reconcile](reference/install-and-reconcile.md) and [machine-audit](reference/machine-audit.md).
- **`route <task>`** — resolve who should run a task against the installed roster. Load
  [rankings-and-routing](reference/rankings-and-routing.md) (and [roles-and-fallback](reference/roles-and-fallback.md)
  when the question is role- or reachability-shaped).
- **`reconcile`** — re-audit the installed base + overrides against this skill's definition and report
  drift or conflict in prose. Load [install-and-reconcile](reference/install-and-reconcile.md).

Invoked with no argument, run `setup`.

## How a staffing question resolves

The full contract is in [rankings-and-routing](reference/rankings-and-routing.md); the order is:

1. **Task-type pin?** If the task matches a named pin (e.g. bulk/mechanical → the pinned model), that model
   wins and ranking is skipped.
2. **Capability gate.** Filter the candidate models to those with any required capability (browser-use,
   computer-use) from the capability matrix — a boolean filter, not a ranking input.
3. **Rank the survivors** by the tie-break `intelligence > taste > cost`.
4. **Fallback ladder.** If the chosen model is unreachable, the next most capable reachable model succeeds
   into the role; if none is reachable, run on the current model in a subagent — never skip the step.

Pins and capabilities are checked *before* the ranking tie-break because they are gates, not rows in the
rankings table. See [roles-and-fallback](reference/roles-and-fallback.md) for roles and succession.

## Two-layer install

The audited roster is written once as a **global base**, harness-coupled (Claude Code: `~/.claude/CLAUDE.md`;
Codex: the global AGENTS layer, e.g. `~/.codex/AGENTS.md`). A project that differs records **only its deltas**
in `docs/agents/` — never a re-copy of the base. A resolver reads the base, then applies the project deltas
on top. Details, the scope-decision flow, and reconciliation-by-audit (no version stamps) are in
[install-and-reconcile](reference/install-and-reconcile.md).

Global writes touch home-directory memory, so the skill writes them **only with user consent** via the
scope-decision flow — never silently.

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory under `reference/`:
  `roles-and-fallback.md`, `rankings-and-routing.md`, `machine-audit.md`, `install-and-reconcile.md`. These
  are the authority; the reference files import no other skill's files.
- **Project playbooks** — what `setup` installs into the target repo's `docs/agents/`: a project staffing
  override (the delta-only playbook). It holds only what differs from the global base.
- **Sibling skills** — **none. `staffing` is a root primitive.** It is invoked *by* siblings (plan,
  prototype, backlog) but depends on no other skill and imports no other skill's files.
