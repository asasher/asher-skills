# merge-changes

The explicit merge approval gate. `backlog` (and every implementation loop) ends at a **review-ready PR**;
nothing merges until the user asks. Invoking this skill *is* that ask — it verifies the named changes are
still open and review-ready, re-queries required checks immediately before each merge, merges in dependency
order, reconciles dependent branches, resolves only mechanical conflicts, and reports SHAs plus anything left
unmerged. A shaping thread's documented readiness signal is also authorization, but only after it presents
the exact shaping change request and only for that request. Cleanup tears down the environment, removes the
working copy through `worktree`, then deletes and verifies the branch.

`LGTM` and green checks are prerequisites, never authorization.

Install: `npx skills add <repo-url> --skill merge-changes`.
