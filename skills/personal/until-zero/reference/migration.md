# Lakebed migration and retirement

Keep the Lakebed application live and readable until every cutover gate passes.

1. Freeze a source snapshot without disabling capture. Obtain a Lakebed dump through the verified deployment
   tooling; never use chat or terminal output as the data carrier.
2. Run `migrate_lakebed.py inspect --input <dump>`. Present each owner fingerprint and per-table counts. Select
   the intended owner explicitly; never infer it from order, row count, or login recency.
3. Run the explicit-owner import into an empty instance. It preserves domain IDs, converts fields to the local
   contract, copies only destination allowlisted fields, recursively excludes secret-shaped keys and raw
   ingest logs, and writes a source-hashed manifest. Review the secret scan and count reconciliation. A private
   recovery journal makes the exact source/owner import resumable; a mismatched retry stops for manual recovery.
4. At frozen dates, run the historical TypeScript oracle and Python projection over the same fixtures and
   sanitized real snapshot. Use `compare_oracles.py`; investigate every delta in opening balance, three zero
   dates, card statements, ordered timeline, amounts, or source IDs. Do not waive unexplained drift.
5. Complete a real generated report and statement proposal/apply cycle while Lakebed remains available.
6. Repoint the phone only after the dedicated API auth matrix and signed Shortcut pass. Dual-run through at
   least one live Wallet charge and one statement reconciliation; compare missing/duplicate captures,
   mappings, statements, and zero dates.
7. Rehearse rollback: restore the old Shortcut endpoint and prove the Lakebed read path. Agree the observation
   window. Then disable old Shortcut/token/runtime without deleting the export or repository.

Retirement evidence includes owner selection, sanitized manifest, parity report, Shortcut build/live Queue ID,
dual-run ledger, statement proposal/approval, rollback rehearsal, and post-retirement refresh/report smoke.
