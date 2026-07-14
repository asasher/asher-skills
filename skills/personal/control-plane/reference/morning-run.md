# Morning Run

Run all seven phases in order. Keep a phase ledger for the final brief: `complete`, `skipped`, `blocked`, or
`failed`, with concrete effects.

1. **Close prior day.** Inspect the date open in `TODO.md`. If it predates today, invoke `manage-tasks` Stop
   Work for that date and verify its end state. If today is already open, record this phase as skipped. Do not
   commit unrelated dirty work.
2. **Pull.** Invoke `capture-to-inbox drain`, then invoke `manage-notes` Intake for every other bound source.
   If capture is also registered in the Intake roster, count the completed drain and do not pull it twice.
   Verify each source either advanced after a local write or has a named failure; remote queue deletion is not
   a substitute for local success.
3. **Ingest.** Invoke `manage-notes` Ingest as a distinct phase over the resulting Inbox. Verify its own
   completion contract rather than treating Pull as ingestion.
4. **Opportunity pulse.** Invoke `manage-opportunities` by name to query active opportunities for their one
   designated next action and due or overdue follow-ups. Surface missing or blocked next actions. Do not run
   the full portfolio audit, mutate stage, or infer progress from artifacts.
5. **Start work.** Only after Close Prior Day, Pull, and Ingest complete, invoke `manage-tasks` Start Work and
   verify today's task shape. Opportunity tasks remain owned by their Opportunity origin when inactive.
6. **Runway.** When Until Zero is configured, invoke `until-zero refresh` and then its current report. Record
   captures committed or pending, the expected zero status, first material driver, warnings, and report path.
   A missing optional skill, unavailable API, or invalid runway marks this phase skipped or failed without
   blocking unrelated phases; never present a stale runway as fresh.
7. **Brief.** Report prior-day closure, captures pulled and drained, Inbox dispositions, opportunity actions,
   today's active plan, runway status when configured, and every unresolved decision or failed effect.
   Distinguish an empty source from a source that could not be checked.

Continue independent source pulls after one source fails, and the Opportunity pulse may still run. Any
failure in Close Prior Day, Pull, or Ingest blocks Start Work; finish with the brief instead of presenting a
partial morning run as complete. A Runway failure remains visible but does not retroactively block Start Work.

Completion criterion: every phase has a ledger status, Start Work ran only after its three gates passed, and
the final brief accounts for every change and blocker.
