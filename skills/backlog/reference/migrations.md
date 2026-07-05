# Migrations

Read by `setup` when a playbook's version stamp — the `<!-- backlog-templates: ... -->` comment on line 1 (or its retired `<!-- triage-templates: ... -->` form) — predates the current `templates/VERSION`, or is absent. Each entry says what changed and how to reconcile it without losing repo values. An entry retires once no live deployment can predate it.

## v2026-07-05 → v2026-07-05.1

The skill was renamed `triage` → `backlog` and made platform-agnostic. Apply all of:

- **Stamp form renamed** — `<!-- triage-templates: ... -->` becomes `<!-- backlog-templates: ... -->` on every playbook this pass touches or confirms current.
- **Policy playbook renamed** — `docs/agents/triage-policy.md` → `docs/agents/backlog-policy.md`, as a tracked rename (`git mv`); update any repo references to the old path, and "run `triage <cmd>`" mentions to `backlog <cmd>`.
- **Platform bindings playbook added** — scaffold `docs/agents/platform.md` and fill it from current practice: a GitHub remote with a `gh`-based flow fills the github defaults for tracker and change review, git fills version control, the harness running setup fills harness dispatch. Verify the verbs per setup step 3 rather than assuming.
- **`in-flight` role added** — the readiness axis gains `in-flight` (claim marker set by `run` at dispatch, replacing `ready-for-agent`; records branch and dispatch date; groom sweeps orphans). Add the role and its hygiene section to `backlog-policy.md` and map or create its label on the tracker.
- **Evidence presentation is per-binding** — the GitHub blob-URL/camo contract moves under a "GitHub binding" heading of `evidence.md` § Presentation, joined by the local and custom binding sections; the repo's capture expectations stay untouched.
- **PR close linkage is bound** — `pr.md`'s hardcoded `Closes #<issue-number>` line becomes "the close linkage per `platform.md`"; a repo staying on GitHub keeps `Closes #<n>` as the recorded value.
- **Stamp** — add the current version stamp to every playbook this pass touches or confirms current.

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
