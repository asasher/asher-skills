# Upstream feedback


The privacy discipline for anything that leaves the repo. Every layer applies, in order:

- **Written from scratch, in skill vocabulary.** Compose a fresh draft using skill names, verbs,
  phases, roles, and abstract failure scenarios. Keep transcripts, ledger text, repo or product
  names, paths, code, ticket identifiers, and business terms private. Reproduce through skill
  abstractions, such as "a spec-typed ticket with one open child."
- **Scrubbed mechanically.** Run
  `scripts/scrub.py <draft> retro/denylist.txt docs/agents/retro-denylist.txt` — both denylist
  halves, the machine-local and the repo-shareable — flagging denylist terms, email addresses,
  absolute filesystem paths, and URLs outside the upstream repo. `retro/denylist.txt` is instance
  state, so resolve it against the repo's primary working tree. A half counts as absent only when it is missing from its resolved location; then
  run with the one that exists and say so. A finding means rewrite and re-run. Require both a clean exit and the human approval below.
- **Approved verbatim, per issue.** Show the user the exact final title, body, and label.
  Submit each issue only after their explicit approval of that text. Setup consent authorizes
  drafting and proposing; submission requires this separate approval.
- **Pseudonymity stated honestly.** The sanitized issue is attributed to the user's own GitHub
  account. Say so in the approval ask; it is part of what they are
  approving.

An approved draft is filed with `gh issue create` against the playbook's upstream target, carrying
its recorded label (`feedback`). If `gh` is missing or unauthenticated, state the gap and hand the
user the ready-to-file draft.
