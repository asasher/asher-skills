# Staffing

Owns the model roster for a machine and its projects: **which model should run this task?** The roles,
rankings, capabilities, task-pins, and fallback ladder live in one primitive so the same answer serves any
workflow skill, an ad-hoc session, and any harness — not just one dev loop.

## When to use

- **Setting up a machine or project** — audit reachable models and write the roster.
- **Routing a task** — resolve who staffs it (a sibling skill like prototype/backlog invokes this by
  name; a user can ask directly).
- **Staffing an issue before dispatch** — route groomed routine work over the coordinator-eligible set, while
  named judgment/design/hard-diagnosis work goes to the orchestrator with an upward successor recorded.
- **Reconciling** — check a drifted install against the skill and report conflicts.

## Shape

- **Compiled, not hardcoded.** A machine audit probes native models plus each installed sibling harness CLI
  in each direction, then classifies each direction — effect-verified, intentionally disabled by the owner,
  or unavailable with its failure class — with the probe evidence behind it; only effect-verified directions
  back dispatch. The example table in `machine-audit.md` exists
  only as a *labeled example of audit output*, never as the shipped roster. Cost/intelligence/taste are
  seeded and user-tuned.
- **Three separate structures.** A rankings table (cost/intelligence/taste), a named harness/tool
  capability-provider registry, and a pin list. Provider reachability gates the executor set before model
  ranking, so a model name never invents browser, computer, or image access.
- **One resolution order.** After any issue-coordination pre-gate: pin → provider/fallback → eligible
  executor → taste gate → `intelligence > taste > cost`. Routine coordination is never cheapest-first.
- **Directional sibling harness dispatch.** The active harness's effect-verified sibling route is tracked
  independently; a failed direction falls back asymmetrically.
  Each external CLI runs inside a cheap, named, watched native relay; provider compilation keeps only the
  active harness mechanics in the installed tree.
- **One layer, in the repo.** The project's staffing playbook under `docs/agents/` carries the complete
  roster and is the only thing read at resolution time. The skill's bundled roster is a **seed**, read once
  at setup and never at runtime. No home-directory module, no base-plus-delta overlay — two layers were the
  previous shape and the reason this one exists.
- **The playbook records its own machine.** Judgment numbers travel between machines; reachability, aliases,
  and CLI versions do not, so a probe record at its head says where the rows came from. A playbook naming a
  different machine is stale, and stale is worse than absent: it resolves cleanly and fails at the point of
  use.
- **Reconcile by LLM audit** — the shared posture across this repo's operator skills.

## Layout

`SKILL.md` is the command surface (setup / route / reconcile) and points into `reference/`. `setup.md` owns
the setup branch; the other references hold the reusable audit and routing rules:
`roles-and-fallback.md`, `rankings-and-routing.md`, `machine-audit.md`, `install-and-reconcile.md`.
Declared `variants/{codex,claude}` overlays supply one active-harness `reference/harness.md` without
duplicating the public identity, dependencies, invocation policy, or setup owner.
`agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the pre-deployment probe eval.
`variants/*/templates/seed/roster-seed.md` is the per-provider roster seed setup reads when writing a
project's playbook — data only; the doctrine lives in the references.

Self-contained at the file level; composes by name. **Sibling dependency: none — staffing is a root
primitive** (invoked by siblings, depends on none).

## Install

`npx github:asasher/asher-skills install --skill staffing`, then invoke it (`setup`) to run the audit and write the roster
for your machine.

## Credits

- **Relationship:** extracted from this repository's `backlog` skill.
- **Source:** [`6412325`](https://github.com/asasher/asher-skills/commit/6412325).
- **Authority moved:** roster, role, routing, and fallback policy moved here.
- **Local changes:** added machine/project layers, coordinator routing, and directional sibling-harness dispatch.
