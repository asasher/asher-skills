# Local checkpoint

Store `.retro/checkpoint.json` in the primary checkout, resolved through Git's common directory and worktree registrations. All linked worktrees share it; other clones and machines keep their own. Add the root-anchored `/.retro/` rule to `.gitignore`. The checkpoint stays outside commits.

```json
{
  "last_sweep_at": "2026-09-06T12:00:00Z",
  "cursor": {
    "updated_at": "2026-09-06T11:45:00Z",
    "session_id": "harness:session-id"
  },
  "pending": {
    "scope": "incremental",
    "sessions": [
      { "updated_at": "2026-09-07T09:00:00Z", "session_id": "harness:next-session" }
    ]
  }
}
```

`last_sweep_at` records completed review time. The cursor identifies the last reviewed session version, ordered by latest completed-turn timestamp and harness-qualified session ID. `pending` holds only the selected batch and its scope (`initial`, `incremental`, or `historical`); omit it after completion. Before any completed sweep, the time and cursor are null. Use metadata to select versions; read transcript bodies only for that batch. Active sessions wait until their work completes.

On first use, select the latest three eligible sessions in chronological order and state that older history is outside this initial scope. Thereafter select candidates after the cursor oldest first, three at a time. Atomically persist `pending` before reading or discussing the batch, preserving the completed cursor. On resume, use those saved versions before selecting new sessions. Read only through each selected completed-turn boundary; newer completed work remains eligible. If completion, ordering, or the saved version cannot be recovered reliably, report the gap and keep it pending.

Advance only through contiguous reviewed versions whose discussion and selected tracker writes have finished, including dismissals. Atomically update the cursor and remove only that completed prefix from `pending`; inaccessible versions and unfinished writes retain the remainder. Check existing tracker records before retrying selected writes. A historical review preserves the normal cursor. When a normal selection is already pending, leave that checkpoint unchanged and report historical coverage separately. Otherwise a historical selection may use `pending` and clear it without advancing the normal cursor. A broader scope advances only through covered candidates and retains unresolved normal coverage.

Serialize sweeps sharing this file so one cannot overwrite another's selection or progress. A missing or unreadable checkpoint returns to the stated first-run scope, with the loss of coverage disclosed. The checkpoint holds a cursor and pending selection; accepted findings remain on project issues.

## Earlier installs

The former `retro/` ledger, transcript bindings, denylists, and `docs/agents/retro.md` playbook are retired. Preserve existing records for the user's cleanup decision; the new sweep starts with recent transcripts and project issues. Existing ledger entries can be reviewed as additional input when requested. Upstream consent recorded in the old playbook grants no authority to this workflow.
