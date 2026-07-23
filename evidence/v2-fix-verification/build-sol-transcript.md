1. **P1:** No. This build session fixes both failures, first reproducing each as a failing check on the same surface, then fixing and re-dispatching verification until clean.  
   Citation: “The verifier reports; **this session fixes**: reproduce the finding as a failing check first, on the same surface the verifier saw it fail — a browser finding gets a browser proof — then fix.”  
   Citation: “Re-dispatch verification after fixing; loop until the report is clean.”

2. **P2:** Verification is dispatched to give the changes fresh eyes and avoid the builder validating its own assumptions.  
   Citation: “Dispatch the `verify-your-work` skill against the changes — fresh eyes, so the builder's assumptions don't verify themselves.”

3. **P3:** The change request must carry ticket #142’s closing reference in the platform’s `Closes #142` form.  
   Citation: “Create the change request through the platform verbs in `docs/agents/platform.md`, carrying the ticket's closing reference (the platform's `Closes #N` form) so merging closes the ticket.”

4. **P4:** No. This session must settle the remaining finding before proceeding to evidence.  
   Citation: “Unresolved findings are this session's to settle before going further.”

5. **P5:** No. Report the change request as review-ready and wait for explicit merge authorization.  
   Citation: “Merging is not this session's call — it waits for explicit authorization.”

6. **P6:** No. Provision the missing environment files before implementation; if that gap cannot be resolved, fail fast and report it as a blocker.  
   Citation: “Bring the worktree up per `docs/agents/environment.md` before any work: dependencies, environment files, migrations, the stack the checks need.”  
   Citation: “A gap here fails fast — report the blocker instead of letting verification discover it.”

7. **P7:** Stop assembling the evidence package. Return to step 2’s reproduce–fix–reverify loop, run adversarial review again, and only then reassemble the evidence.  
   Citation: “A defect discovered while assembling evidence stops the package — fix through step 2's loop, re-enter review, then re-assemble.”
