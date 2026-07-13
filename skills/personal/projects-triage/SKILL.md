---
name: projects-triage
description: Run each eligible Project repository's own backlog workflow across a workspace.
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: []
  optional: []
---

# Projects Triage

Load [triage protocol](reference/triage-protocol.md) and orchestrate one isolated worker per eligible Project.

Eligibility is deliberately narrow: scan only Project known-home notes under `Projects/` and only the
`localPath` field in their frontmatter. Never scan `Opportunities/`, never read an Opportunity `workspacePath`
as a triage target, and never infer a Project target from links or filesystem siblings.

End-state: every eligible Project `localPath` is reported as run, skipped because no local backlog skill exists,
or failed with the concrete error. Opportunity workspaces are absent from the target set.

## Dependency surface

- **Bundled reference:** target selection, dispatch, and reporting protocol.
- **Project playbooks:** each target repository's own backlog and platform instructions.
- **Sibling skills:** none. A target repository's installed `backlog` is discovered locally, not imported as a
  sibling dependency of this skill.
