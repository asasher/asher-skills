# Migrations

Read by `setup` when a playbook's version stamp — the `<!-- backlog-templates: ... -->` comment on line 1 (or its retired `<!-- triage-templates: ... -->` form) — predates the current `templates/VERSION`, or is absent. Each entry says what changed and how to reconcile it without losing repo values. **Reconcile applies every entry between the stamp and current `templates/VERSION`, in order** — never just the newest. So a playbook must not be re-stamped to the current version until every intervening entry has actually been applied to it; advancing the stamp past an unabsorbed entry silently strands that entry's changes, since the stamp is what tells reconcile the entry is still pending. An entry retires once no live deployment can predate it.

## v2026-07-09.1 → v2026-07-10.1

Setup hardened for existing non-trivial code projects: the audits now bind to a real inherited codebase instead of passing trivially on a greenfield one. The playbook slots the audits write into gain structure. Apply all of, preserving every repo value:

- **verifying.md — verified checks + CI merge gate** — § Checks gains the "discovered and verified by running" discipline (record only commands seen to run; no guessed slots), and a new **§ CI merge gate** section records the host CI required-checks as a merge precondition distinct from the local checks. Keep the repo's existing recorded commands; add the CI-gate section (or "none — no CI").
- **environment.md — singleton list, drive-to-feature, verdict derivation** — § Worktree isolation's lone "shared singletons" line becomes the enumerated **shared-singleton list** table (resource · collision mode · locally-isolatable); § Seed data gains an explicit **drive-to-feature path** line; § Parallelism verdict is reworded to derive from the list and name the forcing singletons. Preserve the repo's recorded regime, seed, and verdict — reshape them into the new slots, don't blank them.
- **evidence.md — real-app evidence over probes** — § What to capture gains the leading rule that for a runnable app, evidence is real check output + artifacts driven through the app, with agent-authored probes named a greenfield-only fallback. Additive; keep the repo's per-change-type expectations.
- **platform.md — dependency-relation verbs** — the Tracker binding gains explicit blocker read/write verbs, and § Custom bindings gains the native-relation guidance (Jira/Linear) with the "verify at first use" prose-contract rule. Keep the repo's recorded verbs; add the blocker verbs (task-list/frontmatter for github/local).
- **backlog-policy.md — neutral-by-default + aliases + dependency binding** — § Label roles gains the neutral-by-default rule and an Aliases line; § Dependencies is restated per-binding (task-list / frontmatter / native relation). **Do not touch the work-type role list** during this migration beyond re-stamping — reconcile only the Neutral/Aliases and Dependencies areas, so an install that has customized work-types keeps them.
- **pr.md — CI status line** — the body outline gains a **CI status** item after Checks run (the merge-gate green/red/pending, disclosed). Additive; keep the repo's title convention and required sections.
- **setup.md / worktree-isolation.md / groom.md** — bundled references, replaced wholesale on install (not repo-authored); no per-repo reconciliation, they ship at the new version.
- **Stamp** — bump every reconciled playbook to `v2026-07-10.1`. A section verbatim-identical to the older shipped default updates to the new default; a diverged section is repo practice — leave it and flag only where a listed change touches its contract.

## v2026-07-06.1 → v2026-07-09.1

Primitives extracted to sibling skills. backlog no longer owns staffing, the review surface, planning, or prototyping — each is a standalone skill composed by name (`staffing`, `review-loop`, `plan`, `prototype`). Apply all of:

- **Setup ensures siblings, not sections** — setup no longer installs the picking-models `<!-- backlog-section: ... -->` blocks, the planning/prototyping playbooks, or the tailnet presentation surface. On reconcile, ensure the four siblings are present and let each own its playbook; leave any already-installed sections as repo practice — do NOT delete them unless the user runs the sibling's own setup/reconcile.
- **environment.md sections become sibling-owned** — § Model staffing and § Presenting are now pointers: the roster is the `staffing` skill's, and § Presenting reduces to a pointer to `review-loop`. Preserve the repo's recorded model choices and surface config.
- **Bundled machinery removed** — `reference/{staffing,presenting,plan,prototype}.md`, `scripts/review-*`, `scripts/pages/`, `templates/{plan-skeleton.html,planning.md,prototyping.md}`, and `templates/sections/` are removed from the skill; callers point at the siblings by name.
- **Stamp** — bump touched playbooks to `v2026-07-09.1`.

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
