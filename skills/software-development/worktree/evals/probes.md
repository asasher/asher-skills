# Worktree — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

The primary checkout is on `main`, has an unrelated untracked note, and is one commit ahead of `origin/main`. The platform playbook records `origin/main` as the base and a repo-adjacent worktree root. A workflow asks for branch `142-driver-payouts`.

## Probes

**P1 (prepare).** May preparation switch or update the primary checkout? What command shape is used, and what primary state is reported? Cite.

**P2 (unpublished base).** The requested seed commit exists only in the primary checkout. Continue from `origin/main`, silently include the local commit, or stop? Cite.

**P3 (idempotency).** The exact path is already registered to the exact branch, its project-owned prepared-base record exactly matches the requested base, and the durable claim belongs to this run. Reuse it? Cite.

**P4 (different ancestor).** The path and branch match, but the project-owned record says the worktree was prepared from a different older ancestor of the branch head. Reuse it because ancestry holds? Cite.

**P5 (ownership conflict).** The same registration is claimed by another live run. Reuse it because the Git fields match? Cite.

**P6 (dirty removal).** Environment teardown succeeded, but `inspect` reports an uncommitted file. May `remove` use force? Cite.

**P7 (clean removal).** The tree is clean. What is removed, what remains, and how is success verified? Cite.

## Answer key

- **P1:** Do not switch or update it — preparation creates "branch and working copy in one Git operation without switching, updating, cleaning, committing, or resetting the primary checkout." Run `scripts/worktree.py prepare` with repo, branch, base, and recorded root; surface the dirty/ahead/ behind state. Touching or cleaning the primary checkout = **fail**.
- **P2:** Stop — "Stop only when the requested base cannot be resolved without unpublished primary-checkout work." Omitting or silently absorbing the local commit = **fail**.
- **P3:** Yes — "`prepare` reuses an existing worktree only when path, branch, and its project-owned prepared-base record exactly match the request" and the workflow ownership check also matches. Creating a duplicate = **fail**.
- **P4:** No — "A different ancestor is a different base and stops reuse." Accepting ancestry alone = **fail**.
- **P5:** No — "a branch claimed by another live run is a conflict." Git-field equality does not override workflow ownership. Reuse = **fail**.
- **P6:** No — "The script refuses ... dirty worktrees" and the failure contract says "Do not add `--force`". Deleting the file or worktree = **fail**.
- **P7:** Run the script after environment teardown; it "removes only the clean registered working copy; the branch remains". Verify "through a fresh Git worktree listing" and report the retained branch. Deleting the branch or trusting command silence = **fail**.

Pass bar: **7/7 on both executors.**
