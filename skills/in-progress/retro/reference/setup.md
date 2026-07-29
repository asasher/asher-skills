# Setup — consent, targets, and the denylist

Install or reconcile `docs/agents/retro.md` from [templates/retro.md](../templates/retro.md) — a
repo-owned playbook is edited, never blindly overwritten — and seed the skill instance. Steps, in
order:

1. **Ask the consent question, plainly.** "May retro passes in this repo *propose* upstream feedback
   — sanitized issues on the skill source repo, each one still requiring your approval of the exact
   text before it is filed from your own GitHub account?" Record the answer and who gave it when in
   the playbook's consent row. **Default is disabled**: an unanswered or skipped question records
   disabled, and a fresh install must never surprise anyone with a submission proposal. Make the
   pseudonymity part of the ask, not a footnote: content is sanitized, authorship is not.

2. **Record the upstream target.** Repo (default `asasher/asher-skills`), label (default
   `feedback`), verb (`gh issue create`). When consent is enabled, verify the route with a cheap
   read (`gh repo view <target>`); a dead route is recorded as a gap in the playbook, not silently
   dropped.

3. **Bind the transcripts.** For each harness this repo actually runs under, record where it keeps
   session transcripts for this project (e.g. Claude Code's project transcript directory, Codex's
   session logs — verify the path exists rather than guessing it). The retro pass reads only runs
   since the last pass.

4. **Seed the denylist.** Create `retro/denylist.txt` with the terms a leak would carry: the repo
   and org names, git remote slugs, the user's email domain, tracker project keys, product and
   internal codenames, the machine's hostname and username. Derive candidates from the repo itself
   (`git remote -v`, `git config user.email`, the repo directory name) and show the user the seeded
   list for additions — they know their sensitive vocabulary better than the repo does.

5. **Record the pass-due threshold.** Default: 5 open entries, or 3 entries in one visible cluster.
   The note verb reports against whatever is recorded.

6. **Create the instance if absent.** `retro/ledger.md` with empty `## Open` and `## Triaged`
   sections, next to the denylist.

Reconciling an existing playbook re-asks nothing that is already answered — consent especially: an
existing decision row stands until the user themselves changes it.
