1. **P1:** Do not apply the fix. Record the off-by-one failure and its evidence for the change owner.  
   **Citation:** “**Never fix anything**: a verifier that edits the work stops being a verifier, and the fix belongs to whoever owns the changes.”

2. **P2:** No. Compilation and booting do not verify the summary-math behavior; run a behavioral check that produces a failure when the math is wrong.  
   **Citation:** “A check that cannot fail is not proof. ‘It compiles’ verifies nothing about behavior.”

3. **P3:** Write a browser-driver script, keep it where the repo stores such specs, and exercise the payout journey through empty, loading, error, and disabled states—not only the golden path.  
   **Citation:** “for UI work, a check **written as a script** with the repo's recorded driver for that surface — a browser driver for web, an emulator or app driver for mobile — walking the changed journey through the states named in the ticket (empty, loading, error, disabled), not just the golden path — and left in the tree where the repo keeps such specs.”

4. **P4:** Report the large-tenant claim as *not verified*, explicitly stating that the required fixture was absent. Do not skip or infer the result.  
   **Citation:** “A check you couldn't run (missing environment, no browser, absent fixture) is reported as *not verified*, with the reason — never silently skipped, never guessed at.”

5. **P5:** Use the authentication procedure and browser driver recorded in `docs/agents/environment.md`, rather than improvising a login flow.  
   **Citation:** “Honor it — a verifier that improvises around the recorded contract produces evidence nobody can reproduce.”

6. **P6:** Not yet. Open and inspect `summary.png` for the claimed content, legibility, sensible dimensions, and clipping; its 14KB size proves nothing.  
   **Citation:** “A check whose output is a visual artifact — a screenshot, an export, a rendered document — is judged by **looking at it**: the content the claim names, legible, at sane dimensions, without clipping. A file existing at nonzero bytes proves nothing.”

7. **P7:** Report the failure as **pre-existing**, supported by the same test failing against the base commit.  
   **Citation:** “A failure also present before the change, proven by the same check against the base commit, is reported as **pre-existing** — a distinct verdict from a failure the change caused.”

8. **P8:** No. Do not run `db:reset` against the shared development database; destructive commands may target only resources the playbook marks as per-ticket disposable.  
   **Citation:** “The contract also bounds what state is yours: create and seed what a check needs per the playbook's fixture rules, and point destructive verbs (reset, drop, wipe) only at resources the playbook marks per-ticket-disposable — a shared store is never yours to reset.”
