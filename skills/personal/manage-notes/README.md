# Manage Notes

Maintains a plain-markdown reference wiki through capture Intake, inbox Ingest, workspace Query, and health
Lint. Capture sources are roles bound by `docs/agents/capture-sources.md`, so the published skill contains no
personal paths or service assumptions.

The skill reads Projects and Opportunities during Query/Lint while delegating their shapes to `manage-tasks`
and optional `manage-opportunities`.

## Source

Adapted from the installed `manage-notes` workspace skill and generalized into a project-playbook-driven source.
