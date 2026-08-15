# Merge Change

The explicit merge approval gate, renamed from `merge-changes` — the action was always per-change: CI gated per merge, merges in dependency order, reconciliation after each; a request may still name several changes. Every implementation loop ends at a **review-ready PR**; nothing merges until the user asks. Invoking this skill _is_ that ask — it verifies the named changes are still open and review-ready, re-queries required checks immediately before each merge, merges bases before dependents, and reconciles dependent branches after each merge. Conflicts resolve on a three-rung ladder: mechanical → intent-resolvable (traced to the documented specs and tickets, never invented) → spec-versus-spec, which stops for the human. A slice merging into a feature branch gets its ticket the `delivered` label in the same act; the ticket closes natively at promotion via the `Closes` lines on the promotion PR. Cleanup tears down the environment, removes the working copy through `worktree`, then deletes and verifies the branch.

`LGTM` and green checks are prerequisites, never authorization.

Install: `npx skills add <repo-url> --skill merge-change`.
