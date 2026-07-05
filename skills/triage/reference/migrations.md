# Migrations

Read by `setup` when a playbook's version stamp — the `<!-- triage-templates: ... -->` comment on line 1 — predates the current `templates/VERSION`, or is absent. Each entry says what changed and how to reconcile it without losing repo values. An entry retires once no live deployment can predate it.

## unstamped → v2026-07-05

Playbooks scaffolded before version stamps existed. Apply all of:

- **Missing playbooks** — `evidence.md`, `prototyping.md`, and `pr.md` did not ship as templates; scaffold any that are missing.
- **Staffing roles renamed** — rosters written as lead / delegate / floor become orchestrator / builder (backend | ui | mixed) / checker / floor plus a succession line; rewrite the Model staffing section to the current template shape, preserving the repo's model choices. A hand-rolled "work-surface routing" subsection, if present, is absorbed by the builder/checker split.
- **Evidence presentation modes removed** — the `public-inline` / `private-links` split is gone; the single contract is wrapped `blob/<sha>/…?raw=1` embeds. Replace any mode line or camo-proxy workaround guidance with the current template's Presentation section, keeping the repo's capture expectations.
- **Plans are HTML** — a plan location ending `.md` becomes `.html`; keep the repo's directory and naming convention.
- **PR body outline moved** — if a PR body outline lives anywhere other than `pr.md`, `pr.md` is now its home; point the old site at it.
- **Presenting section added** — `environment.md` gains a Presenting section; the surface step of setup fills it.
- **Serialized exception lane added** — the Parallelism verdict section gains an exception-lane line; fill it from any equivalent caveat the repo already recorded, else "none".
- **Stamp** — add the current version stamp to every playbook this pass touches or confirms current.
