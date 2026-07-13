# Staffing

Owns the model roster for a machine and its projects: **which model should run this task?** The roles,
rankings, capabilities, task-pins, and fallback ladder live in one primitive so the same answer serves any
workflow skill, an ad-hoc session, and any harness — not just one dev loop.

## When to use

- **Setting up a machine or project** — audit reachable models and write the roster.
- **Routing a task** — resolve who staffs it (a sibling skill like plan/prototype/backlog invokes this by
  name; a user can ask directly).
- **Staffing an issue before dispatch** — route groomed routine work over the coordinator-eligible set, while
  named judgment/design/hard-diagnosis work goes to the orchestrator with an upward successor recorded.
- **Reconciling** — check a drifted install against the skill and report conflicts.

## Shape

- **Compiled, not hardcoded.** A machine audit probes native models plus each installed sibling harness CLI
  in each direction, then writes only effect-verified routes. The example table in `machine-audit.md` exists
  only as a *labeled example of audit output*, never as the shipped roster. Cost/intelligence/taste are
  seeded and user-tuned.
- **Three separate structures.** A rankings table (cost/intelligence/taste, higher = better), a distinct
  capability matrix (browser-use/computer-use booleans), and a first-class pin list (task-type and
  capability pins). They stay apart so the `intelligence > taste > cost` tie-break isn't corrupted by mixing
  a boolean into a ranked axis.
- **One resolution order.** After any issue-coordination pre-gate: pin → capability/taste gates →
  `intelligence > taste > cost` → fallback. Routine coordination is never cheapest-first.
- **Directional sibling harness dispatch.** Effect-verified `codex exec` and bounded `claude -p` routes are
  tracked independently; a failed direction falls back asymmetrically and no vendor-policy monitor gates it.
- **Scope is the human's choice.** Project-only (one project playbook, no global write) or
  global-with-overrides: a global base (harness-coupled: `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`, each
  filtered to the models that harness can reach) plus sparse project overrides in `docs/agents/` that carry
  only deltas. A resolver reads base, then applies deltas.
- **Reconcile by LLM audit, no version stamps** — the shared posture across this repo's operator skills.
- **Global writes are consent-gated** via a scope-decision flow.

## Layout

`SKILL.md` is the command surface (setup / route / reconcile) and points into `reference/`. `setup.md` owns
the setup branch; the other references hold the reusable audit and routing rules:
`roles-and-fallback.md`, `rankings-and-routing.md`, `machine-audit.md`, `install-and-reconcile.md`.
`agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the pre-deployment probe eval.

Self-contained at the file level; composes by name. **Sibling dependency: none — staffing is a root
primitive** (invoked by siblings, depends on none).

## Install

`npx skills add <repo-url> --skill staffing`, then invoke it (`setup`) to run the audit and write the roster
for your machine.

## Credits

- **Relationship:** extracted from this repository's `backlog` skill.
- **Source:** [`6412325`](https://github.com/asasher/asher-skills/commit/6412325).
- **Authority moved:** roster, role, routing, and fallback policy moved here.
- **Local changes:** added machine/project layers, coordinator routing, and directional sibling-harness dispatch.
