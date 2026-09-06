# Local checkpoint

Store `.retro/checkpoint.json` in the primary checkout, resolved through Git's common directory and worktree registrations. All linked worktrees share it; other clones and machines keep their own. Add the root-anchored `/.retro/` rule to `.gitignore`. The checkpoint stays outside commits.

```json
{
  "last_sweep_at": "2026-09-06T12:00:00Z",
  "cursor": {
    "updated_at": "2026-09-06T11:45:00Z",
    "session_id": "harness:session-id"
  }
}
```

`last_sweep_at` records when the review finished. The cursor identifies the last reviewed session version, ordered by its latest completed-turn timestamp and harness-qualified session ID. Use session metadata to discover candidates; read transcript bodies only for the selected batch. A resumed session becomes eligible again when it has newer completed work. Active sessions wait until their work completes.

On first use, review the latest three eligible sessions in chronological order and state that older history is outside this initial scope. Thereafter, review candidates after the cursor oldest first, three at a time. Use the timestamp observed when selecting the batch so new work during the review remains eligible. If a harness cannot reliably identify completion or ordering, report the gap and leave its coverage unresolved.

Advance only through a contiguous reviewed batch; inaccessible sessions stay pending. An explicitly requested historical review preserves the normal cursor, and a broader review advances it only through covered candidates. Replace the checkpoint atomically after the discussion and selected tracker writes finish. Serialize sweeps sharing this file so one cannot overwrite another's progress. A missing or unreadable checkpoint returns to the stated first-run scope, with the loss of coverage disclosed.

## Earlier installs

The former `retro/` ledger, transcript bindings, denylists, and `docs/agents/retro.md` playbook are retired. Preserve existing records for the user's cleanup decision; the new sweep starts with recent transcripts and project issues. Existing ledger entries can be reviewed as additional input when requested. Upstream consent recorded in the old playbook grants no authority to this workflow.
