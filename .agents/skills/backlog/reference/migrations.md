# Migrations

Read by `setup` when a playbook's version stamp — the `<!-- backlog-templates: ... -->` comment on line 1 (or its retired `<!-- triage-templates: ... -->` form) — predates the current `templates/VERSION`, or is absent. Each entry says what changed and how to reconcile it without losing repo values. An entry retires once no live deployment can predate it.

## v2026-07-06 → v2026-07-06.1

Model-picking guidance moved out of the roster into the repo's memory files. Apply all of:

- **Picking-models sections added** — setup now installs stamped `<!-- backlog-section: ... -->` blocks from `templates/sections/` into the repo's `AGENTS.md` (rankings table + routing rules + Codex CLI mechanics, harness-neutral) and `CLAUDE.md` (Claude-specific mechanics overlay). Install both per setup step 8; where the repo's existing Model staffing section recorded model choices that diverge from the shipped defaults, seed the table and rules from them.
- **Model staffing section slimmed** — `environment.md` § Model staffing becomes the compiled roster (floor, per-harness role→model mapping, succession) deriving from `AGENTS.md` § Picking models; move any general rules or rationale prose out of the roster into the AGENTS.md section, preserving the repo's model choices.
- **Driving-the-app defaults gain codex** — `environment.md` § Driving the app gains an "Independent runtime verification" line (default: delegate to `codex exec`), and `verifying.md` § Checks a matching second-opinion line; keep the repo's recorded drivers and checks.
- **Stamp** — add the current version stamp to every playbook this pass touches or confirms current.

## v2026-07-05.1 → v2026-07-06

The interactive review loop shipped (`reference/presenting.md` § Review loop and § Hub; assets under the skill's `scripts/`). Apply all of:

- **planning.md format section** — gains the visual-first rules (diagram-first sections, pre-rendered inline SVG, `templates/plan-skeleton.html` as the starting point) and the stable-anchor conventions (section ids, `<li id="ac-N" data-criterion>` criteria). Keep the repo's plan directory and naming.
- **planning.md review section** — "open the rendered HTML" becomes the review-loop presentation: serve via `scripts/review-server.py`, both links in the pause message, ledger dispositions on every revision, approval as the hash-bound approve event. Keep the repo's approver line; the local fallback remains for repos without a surface.
- **environment.md Presenting section** — gains the "Review server" and "Hub" lines; setup step 7 fills them (surface directory, public-URL proxying, sweep command).
- **Stamp** — add the current version stamp to every playbook this pass touches or confirms current.

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
