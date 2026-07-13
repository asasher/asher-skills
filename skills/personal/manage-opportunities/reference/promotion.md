# Promotion

Promotion creates delivery records without erasing commercial history. Treat it as a transaction whose
commit marker is the final `stage: closed-won` write.

1. Verify explicit acceptance or commercial commitment. Record it in `## Events Log` and set `outcomeDate`,
   but leave the current non-won stage in place.
2. Create each required delivery note through `manage-tasks` Project Note Shape. Set its
   `sourceOpportunity` to this Opportunity.
3. Link every Project from the Opportunity `## Projects` section and verify each Project links back. Update
   configured Company and Customer maps in both directions.
4. Move delivery tasks exactly once from the Opportunity or `TODO.md` to the appropriate Project backlog.
   Commercial follow-up may remain with the Opportunity. Clear `nextAction` when no active commercial action
   remains.
5. Assign triage ownership only through each Project's `localPath`. `workspacePath` may remain on the
   Opportunity for commercial artifacts, even when both paths point to the same physical folder.
6. Validate Project paths and links, validate task-ID uniqueness and origin, then run the Opportunity
   structural validator while the Opportunity is still not won.
7. **Final write:** set `stage: closed-won`. Make no other mutation in that write. Re-run validation.

If any step before 7 fails, leave the Opportunity at its previous stage, report the partial artifacts, and
resume from the failed step. Never write `closed-won` first and repair the transaction afterward.

Completion criterion: explicit win evidence and date exist; every delivery Project exists and links both
ways; paths and moved tasks validate; maps are current; and `closed-won` was the final write.
