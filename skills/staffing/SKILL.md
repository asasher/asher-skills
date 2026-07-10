---
name: staffing
description: Own the model roster for a machine and its projects — who staffs which task. Use to install or reconcile the roster, add a project override, or resolve any "which model should do this?" question — directly or from a sibling skill. Not for running the task itself.
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

- **`setup`** — audit the environment, decide scope (global-with-overrides vs project-only), and write the roster.
  Load [install-and-reconcile](reference/install-and-reconcile.md) and [machine-audit](reference/machine-audit.md).
- **`route <task>`** — resolve who should run a task against the installed roster. Load
  [rankings-and-routing](reference/rankings-and-routing.md) (and [roles-and-fallback](reference/roles-and-fallback.md)
  when the question is role- or reachability-shaped).
- **`reconcile`** — re-audit the installed base + overrides against this skill's definition and report
  drift or conflict in prose. Load [install-and-reconcile](reference/install-and-reconcile.md).

Invoked with no argument, run `setup`.

## How a staffing question resolves

The full contract is in [rankings-and-routing](reference/rankings-and-routing.md); the order is:

1. **Pin?** If the task matches a task-type pin (e.g. bulk/mechanical → the pinned model) or requires a
   capability that carries a capability pin (e.g. browser-use → the pinned browser model), that model wins
   and ranking is skipped.
2. **Capability gate.** For a required capability with no pin, filter the candidate models to those the
   capability matrix marks true — a boolean filter, not a ranking input.
3. **Rank the survivors** by the tie-break `intelligence > taste > cost`.
4. **Fallback ladder.** If the chosen model is unreachable, the next most capable reachable model succeeds
   into the role; if none is reachable, run on the current model in a subagent — never skip the step.

Pins and capabilities are checked *before* the ranking tie-break because they are gates, not rows in the
rankings table. See [roles-and-fallback](reference/roles-and-fallback.md) for roles and succession.

## Two-layer install

**One roster, every harness.** The rankings (cost/intelligence/taste) are harness-independent; what changes
per harness is **reachability**, so each harness's file lists only the models that harness can reach — the
Codex layer (AGENTS) omits Claude models, while the Claude layer (CLAUDE.md) includes OpenAI models, since
Claude Code reaches them through the Codex CLI.

**Where the base lives is the human's scope decision at setup**: hoist it global — harness-coupled
(Claude Code: `~/.claude/CLAUDE.md`; Codex: the global AGENTS layer, e.g. `~/.codex/AGENTS.md`) — or keep a
single project-level source; both are legitimate. A project that differs from a global base records **only
its deltas** in `docs/agents/` — never a re-copy of the base. A resolver reads the base, then applies the
project deltas on top. Details, the scope-decision flow, and reconciliation-by-audit (no version stamps) are
in [install-and-reconcile](reference/install-and-reconcile.md).

Global writes touch home-directory memory, so the skill writes them **only with user consent** via the
scope-decision flow — never silently.

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory under `reference/`:
  `roles-and-fallback.md`, `rankings-and-routing.md`, `machine-audit.md`, `install-and-reconcile.md`. These
  are the authority; the reference files import no other skill's files.
- **Project playbooks** — what `setup` installs into the target repo's `docs/agents/`: a project staffing
  playbook. Under global-with-overrides it is **delta-only** (only what differs from the global base); under
  the project-only shape it carries the whole roster for this repo.
- **Sibling skills** — **none. `staffing` is a root primitive.** It is invoked *by* siblings (plan,
  prototype, backlog) but depends on no other skill and imports no other skill's files.
