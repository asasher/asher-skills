---
name: manage-notes
description: Maintain a workspace reference wiki through Intake, Ingest, Query, and Lint. Use when captures need collecting or triage, raw material should become durable notes, a workspace question may be answered from Notes, Projects, Opportunities, or entity records, or the wiki needs a health check.
metadata:
  invocation: model
  execution: thread
  requires: [manage-tasks]
  optional: [manage-opportunities]
---

# Manage Notes

`Notes/` is durable, interlinked knowledge. Raw captures belong in `Inbox/`; cited local sources belong in
`Attachments/`; working documents belong with their Project or Opportunity. This skill owns Note Shape and
four commands. It delegates task handling and entity shapes to their owning sibling skills.

## Commands

- **Intake** - pull configured capture sources into `Inbox/`. Load [capture sources](reference/capture-sources.md).
- **Ingest** - drain every inbox item into a note, task, attachment, or `GRAVEYARD.md` decision. Load
  [ingest](reference/ingest.md).
- **Query** - answer from workspace records and cite them. Load [query and lint](reference/query-lint.md).
- **Lint** - report wiki health; mutate only after confirmation. Load [query and lint](reference/query-lint.md).

Infer the command from the request. Intake only fills the inbox; Ingest empties it. Never merge those cadences
implicitly.

## Note Shape

One note is one durable idea at `Notes/<Title>.md`:

```yaml
---
title: <human title>
type: research | idea | reference | concept | hub
source: <URL or Attachments-relative path>
created: <YYYY-MM-DD>
tags: [lowercase, topic, words]
---
```

Omit `source` only when none exists. The body has an H1, one-line framing, and useful headings. Link related
notes and entity records explicitly. A hub maps a topic with one orienting line per note; every note is
reachable from a hub within two hops.

## Boundaries

- Invoke required `manage-tasks` for task relay and Project Note Shape.
- Invoke optional `manage-opportunities` for Opportunity Note Shape or lifecycle. Query may read Opportunity
  records without it; Lint reports Opportunity shape as unchecked when the sibling is absent rather than
  inventing a schema.
- Capture mechanisms, credentials, paths, and archive behavior come only from the project's
  `docs/agents/capture-sources.md`. The bundled skill defines roles, never personal machine bindings.

## Dependency surface

- **Bundled references:** capture-source role contract, Ingest, Query, and Lint.
- **Project playbook:** optional `docs/agents/capture-sources.md` binds actual capture mechanisms and ledgers.
- **Sibling skills:** required `manage-tasks`; optional `manage-opportunities`, both invoked by name.
