# Staffing

Owns the model roster for a project and the doctrine that resolves it: **which model should run this task?** A reference skill — sibling skills cite it by name; it selects a route, and running the task stays with the caller.

## The doctrine — bars, then cheapest

The caller states the bars the task needs; resolution drops every model below them and takes the **cheapest survivor**, escalating without asking when cheaper output misses the bar. Checks are runtime-only — try, warn, fall back — with nothing about reachability ever recorded; `SKILL.md` states the rule and `reference/rankings-and-routing.md` owns the detail.

## Shape

- **One playbook, in the repo.** The project's staffing playbook under `docs/agents/` — roster table, pins, declared capability routes, repo deltas, roughly twenty lines — is the only thing read at resolution time. The bundled roster is a **seed**, read once at setup and never at runtime.
- **Capabilities are provider routes, not model traits.** Browser, computer use, and imagegen resolve through declared routes tried at use; a missing provider is a reported capability gap, never a substitution.
- **Setup is a template fill.** Seed numbers plus a short repo-deltas interview; no probes, no overlay, no machine stamps.

## Layout

`SKILL.md` is the surface (setup / route) and points into `reference/`: `setup.md` (the template fill), `rankings-and-routing.md` (bars, pins, providers, resolution order, runtime fallback), `roles-and-fallback.md` (roles as bar presets), `harness.md` (cross-harness command shapes). `templates/roster-seed.md` is the seed; `templates/instruction-trigger.md` is the § Staffing section setup reconciles into the project instruction file. `agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the pre-deployment probe eval.

Self-contained at the file level; composes by name. **Sibling dependency: none — staffing is a root reference** (cited by siblings, depends on none).

## Install

`npx skills add github:asasher/asher-skills --skill staffing`, then invoke it (`setup`) to write the playbook for your repo.

## Credits

- **Relationship:** extracted from this repository's `backlog` skill.
- **Source:** [`6412325`](https://github.com/asasher/asher-skills/commit/6412325).
- **Authority moved:** roster, role, routing, and fallback policy moved here.
- **Local changes:** bars-then-cheapest resolution, runtime-only checks, template-fill setup.
