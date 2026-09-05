# Upstream feedback


The privacy discipline for anything that leaves the repo. Every layer applies, in order:

- **Written from scratch, in skill vocabulary.** The draft is composed generatively — skill names,
  verbs, phases, role nouns, and the abstract shape of the stumble — never by redacting a transcript
  or ledger entry. You cannot leak what you never included. No repo or product names, no file paths,
  no code, no ticket ids or titles, no business terms. Reproduction steps reference the skill's own
  abstractions ("a spec-typed ticket with one open child"), never this repo's instances.
- **Scrubbed mechanically.** Run
  `scripts/scrub.py <draft> retro/denylist.txt docs/agents/retro-denylist.txt` — both denylist
  halves, the machine-local and the repo-shareable — flagging denylist terms, email addresses,
  absolute filesystem paths, and URLs outside the upstream repo. `retro/denylist.txt` is instance
  state, so it resolves like the instance — against the repo's main working tree, never a linked
  worktree's cwd. A half counts as absent only when it is missing from its resolved location; then
  run with the one that exists and say so. A finding means rewrite and re-run. A clean exit is
  necessary, never sufficient.
- **Approved verbatim, per issue.** Show the user the exact final text — title, body, label — and
  submit nothing without their explicit approval of that text. Consent recorded at setup means the
  pass may *draft and propose*; it never means submit. **There is no auto-submit, ever.**
- **Pseudonymity stated honestly.** The issue is filed from the user's own GitHub account — content
  is sanitized, authorship is not. Say so in the approval ask; it is part of what they are
  approving.

An approved draft is filed with `gh issue create` against the playbook's upstream target, carrying
its recorded label (`feedback`). If `gh` is missing or unauthenticated, state the gap and hand the
user the ready-to-file draft instead of improvising another channel.
