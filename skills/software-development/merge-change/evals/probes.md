# Merge Change — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

The user says "merge #51." PR #51 is review-ready with LGTM; its stack-mate #52 is also green and LGTM'd. #51's checks passed forty minutes ago. The environment playbook records a per-change container teardown. Each PR was built in its own worktree, still present at merge time, and the platform's merge command offers a flag that also deletes the branch.

## Probes

**P1 (authorization and scope).** #52 is green too. Merge both? And would #52's LGTM alone have authorized anything? Cite both halves.

**P2 (CI timing).** The forty-minute-old green run — good enough? Cite.

**P3 (conflict).** Post-merge reconciliation of a dependent branch hits a non-mechanical conflict: the two sides changed the same surface differently, each matching its own ticket's spec, and the documented intents do not contradict. Abort, invent a compromise, or what? Cite.

**P4 (cleanup).** After #51 merges, what beyond the merge itself gets cleaned up, in what order, from where is the teardown run, and how do you know the branch is gone? Cite.

**P5 (order).** If the user had said "merge #51 and #52" (stacked, #51 base), what order and why? Cite.

**P6 (merge verb).** At step 4, about to merge #51 — its build worktree still holds the branch, and the merge command's branch-deleting flag would save a cleanup step. Use it? Cite.

**P7 (slice into a feature branch).** The user also named PR #53, a slice whose PR targets the feature branch `payments-rework`, not main. After merging it, what happens to the slice's ticket — and when does it close? Cite.

## Answer key

- **P1:** Merge only #51 — "'merge #51' does not license merging its stack-mates." And no: an LGTM is a prerequisite, "**they are never authorization to merge**." Merging #52 = **fail**.
- **P2:** No — "re-query the required checks on the current head — only its own completed checks count; a local run, an earlier head's green, or timing inferred from another change never stands in for them." Trusting the old run = **fail**.
- **P3:** Resolve at rung 2 — "Trace both sides to their specs and tickets — intent is addressable by construction: spec projections, blessed hashes, change descriptions. Resolve by the documented intent, never by inventing behavior neither side documents, and record the trade-off on the change request." Stopping belongs only to rung 3, where "Two blessed intents genuinely contradict." Aborting here, inventing a third behavior, or resolving without recording the trade-off = **fail**.
- **P4:** Working copy through the owner — "remove each merged change's working copy through the `worktree` skill — its Remove owns the teardown order (environment torn down from inside the working copy, then the copy itself)" — and "Only then delete each merged branch, local and remote" — known gone because the answer "verif[ies] both are gone by querying them" (`git branch --list` / `git ls-remote --heads origin`, both returning nothing), "never by trusting the delete commands' own output." Leaving the container = **fail**; removing the working copy before the environment, or tearing down by hand instead of through the `worktree` skill = **fail**; deleting the branch (or claiming it deleted) before the working copy is gone = **fail**; reporting the branch gone on the delete command's say-so, without the queries = **fail**.
- **P5:** "bases before dependents" — #51 then #52, with the CI gate re-checked "per merge, at merge time." Dependents first = **fail**.
- **P6:** No — "Branch deletion stays out of the merge verb": the working copy still holds the branch, so the bundled delete "fails on the local branch — and can abort before the remote branch is touched. Branch cleanup is step 7's, downstream of working-copy teardown." Using the flag = **fail**.
- **P7:** The ticket gets "the `delivered` label role in the same act as the merge" and stays open — "`Closes #n` fires only on default-branch merges, so the slice ticket does not close here — it stays open and `delivered`, awaiting promotion, and closes natively when the promotion change request (the spec ticket's PR into main, carrying one `Closes` line per slice) merges." Closing the ticket at the feature-branch merge, or skipping the label, = **fail**.

Pass bar: **7/7 on both executors.**
