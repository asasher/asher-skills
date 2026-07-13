# Capture Source Bindings

A capture source is a project-bound role with up to three operations:

- **Pull** - read new items into `Inbox/`; transcribe or extract enough raw content to preserve meaning.
- **Bookkeep** - record source item IDs and cursor only after a successful pull so Intake is idempotent.
- **Archive** - optionally clear processed items at the source after Ingest, only on explicit request.

Read `docs/agents/capture-sources.md` when present. Each binding must name the source, pull mechanism, provenance
tag, bookkeeping location/key, archive mechanism or `none`, required capability/auth, and failure behavior.
Treat paths and commands there as project facts. Do not substitute remembered personal paths, browser profiles,
services, or credentials.

If the playbook is absent, or one source lacks a complete binding, do not guess. Report the unbound role and
the one setup fact needed. Other fully bound sources may still run.

## Intake contract

1. Pull every bound source from its recorded cursor to now.
2. Append text captures to `Inbox/INBOX.md` or place files in `Inbox/`, carrying provenance and source ID.
3. Advance bookkeeping only after the inbox write succeeds; retries must not duplicate an existing source ID.
4. Report each source as pulled, unchanged, or failed with the concrete reason.
5. Do not distill or perform post-Ingest archive during Intake.

Completion criterion: every bound source was attempted, successful writes are idempotently ledgered, failures
are visible, and no source item was archived.
