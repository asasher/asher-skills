# Setup

Reconcile the consumer's control-plane bindings; sibling setup owners keep ownership of their own artifacts.

1. Verify all required siblings are installed. Invoke `capture-to-inbox setup` by name when its instance is
   absent or incomplete, and effect-verify its project-local credential source before a dry run; do not
   duplicate its materialization, secret-storage, external dependency, deployment, or smoke-test logic here.
2. Read `control-plane/config.json` and existing project instructions. Bind canonical task, Inbox, attachment,
   Opportunity, Project, Company, Customer, and People homes only from verified project facts.
3. Ask whether morning ingest is enabled, which non-capture Intake sources participate, and whether any daily,
   weekly opportunity-review, or project-triage cadence should be scheduled. Record timezone and consent.
4. Create `docs/agents/control-plane.md` only when project-specific deltas are needed. On rerun, preserve all
   consumer edits and propose factual corrections rather than replacing the file.
5. Dry-run [morning-run](morning-run.md) through the phase gates without mutating domain data, then run the
   real sequence only with approval.

Completion criterion: required siblings, the capture instance, and local credential loading are
effect-verified, project paths and cadence are explicit, optional siblings are never treated as required,
and an immediate rerun produces no unapproved changes.
