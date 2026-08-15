# Staffing

Owns the model roster for a project and the doctrine that resolves it: **which model should run this task?** A reference skill — siblings like `to-subagent` cite it by name; it selects a route and never runs the task.

## The doctrine — bars, then cheapest

The caller states the intelligence bar and taste bar the task needs (coordination class and surface are the coarse inputs). Resolution filters out every model below the bars and takes the **cheapest survivor**. Quality control is escalation: when cheaper output misses the bar, a more capable route takes the retry without asking. The taste bar for user-facing UI, copy, and API design is hard — no intelligence buys past it.

This replaces the old maximize-quality rule (`intelligence > taste > cost` descending), under which cost was a dead tiebreaker and everything routed to the top model.

## Runtime-only checks

Nothing about reachability is recorded — no probes, no machine overlay, no self-heal state. A route is tried at the point of use; on failure the resolver warns the user, falls back to the next-cheapest survivor above the bars, and continues. The warning is the record; a route failing repeatedly across sessions is retro fodder. What ships as knowledge instead is the reliable cross-harness command shape (foreground CLI subprocess, stdin closed, explicit timeout, output to log) in `reference/harness.md`.

## Shape

- **One playbook, in the repo.** The project's staffing playbook under `docs/agents/` — roster table, pins, declared capability routes, repo deltas, roughly twenty lines — is the only thing read at resolution time. The bundled roster is a **seed**, read once at setup and never at runtime.
- **Capabilities are provider routes, not model traits.** Browser, computer use, and imagegen resolve through declared routes tried at use; a missing provider is a reported capability gap, never a substitution.
- **Setup is a template fill.** Seed numbers plus a short repo-deltas interview; no probes, no overlay, no machine stamps.

## Layout

`SKILL.md` is the surface (setup / route) and points into `reference/`: `setup.md` (the template fill), `rankings-and-routing.md` (bars, pins, providers, resolution order, runtime fallback), `roles-and-fallback.md` (roles as bar presets), `harness.md` (cross-harness command shapes). `templates/roster-seed.md` is the seed; `templates/instruction-trigger.md` is the § Staffing section setup reconciles into the project instruction file. `agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the pre-deployment probe eval.

Self-contained at the file level; composes by name. **Sibling dependency: none — staffing is a root reference** (cited by siblings, depends on none).

## Install

`npx github:asasher/asher-skills install --skill staffing`, then invoke it (`setup`) to write the playbook for your repo.

## Credits

- **Relationship:** extracted from this repository's `backlog` skill.
- **Source:** [`6412325`](https://github.com/asasher/asher-skills/commit/6412325).
- **Authority moved:** roster, role, routing, and fallback policy moved here.
- **Local changes:** bars-then-cheapest resolution, runtime-only checks, template-fill setup.
