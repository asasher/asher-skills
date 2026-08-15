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
   `feedback`, color `#BFD4F2` where the tracker carries label colors — retro mints this label
   itself, outside the backlog skill's role axes, so it ships the color too), verb
   (`gh issue create`). When consent is enabled, verify the route with a cheap read
   (`gh repo view <target>`); a dead route is recorded as a gap in the playbook, not silently
   dropped.

3. **Bind the transcripts.** For each harness this repo actually runs under, derive where it keeps
   session transcripts from the playbook's how-to-find notes, verify the location resolves rather
   than guessing it, and write the verified locations to `retro/transcripts.md` in the untracked
   instance — never into the tracked playbook, which keeps only the derivations and the names of
   the harnesses bound. Record no transient evidence (a file count decays the moment another
   session runs); the durable guard is verify-at-use, and this step is what a pass re-runs when
   `retro/transcripts.md` is missing or stale.

4. **Seed the denylist halves.** Two files, split by who should see the terms:
   - `retro/denylist.txt` — the machine-local half, untracked with the instance: the machine's
     hostname and username, the user's email fragments, employer and person terms.
   - `docs/agents/retro-denylist.txt` — the repo-shareable half, tracked: the repo and org names,
     git remote slugs, tracker project keys, product and internal codenames — terms every clone
     of the repo wants scrubbed.

   Derive candidates from the repo itself (`git remote -v`, `git config user.email`, `hostname`,
   the repo directory name) and show the user the two seeded lists side by side for edits — they
   know their sensitive vocabulary, and which terms are shareable, better than the repo does.

5. **Record the pass-due threshold.** Default: 5 open entries, or 3 entries in one visible cluster.
   The note verb reports against whatever is recorded.

6. **Create the instance if absent, and keep it untracked.** `retro/ledger.md` with empty `## Open`
   and `## Triaged` sections, next to the local denylist half and `retro/transcripts.md`. Write the
   root-anchored `/retro/` entry into the repo's `.gitignore` (idempotently — add the line only
   when it is not already covered; the anchor keeps deeper directories that happen to be named
   `retro` trackable): the instance is machine-local, and nothing in it belongs in the repo's
   history.

Reconciling an existing playbook re-asks nothing that is already answered — consent especially: an
existing decision row stands until the user themselves changes it.

## Migration — the instance is already tracked

When `git ls-files retro/` is non-empty, the instance predates machine-locality. Migrate it forward
in one commit:

1. Untrack going forward: `git rm -r --cached retro/` — the working-tree files stay in place,
   about to become ignored.
2. Write the root-anchored `/retro/` entry into `.gitignore`.
3. Split the existing `retro/denylist.txt` into the two halves of step 4, showing the user the
   split for edits.
4. Move any concrete transcript locations out of `docs/agents/retro.md` into `retro/transcripts.md`,
   leaving the playbook the how-to-find derivations and the staleness clause per step 3 — and drop
   any transient evidence (file counts) on the way. When `retro/transcripts.md` does not exist yet
   and the playbook records no locations, run step 3's binding to create it fresh.
5. Commit the untracking, the `.gitignore` entry, the shared denylist half, and the playbook edit.

A migration run in a **linked worktree** untracks for every checkout but migrates only that
worktree's working files — and the instance resolves against the repo's main working tree, per the
skill. Before the worktree is cleaned up, copy the migrated instance (`ledger.md`, the local
denylist half, `transcripts.md`) into the main working tree, or restore there from the
pre-untracking commit and re-run steps 3–4.

Two warnings the user hears before the commit lands:

- **Other clones and machines pulling the untracking commit will have git delete their unmodified
  `retro/` working files.** Each machine restores its instance from the pre-untracking commit
  (e.g. `git show <sha>:retro/ledger.md > retro/ledger.md`) or from a backup taken before pulling.
- **History rewrite is out of scope.** Previously tracked values — hostnames, denylist terms —
  remain reachable in git history. Accepted; the migration stops the bleeding, it does not
  launder the past.
