# Playbook: Research

> Project-specific delta owned by `research setup`. The installed skill owns source hierarchy, claim classes,
> fan-out, synthesis, and audit; this file binds those roles to this repo.

## Artifact routing

- Durable general research root: `research/<lowercase-hyphenated-slug>/`.
- Research directly supporting a local skill source: `<skill>-workspace/research/<slug>/`; keep author-side
  source packets and drafts there, never inside the shipped skill source.
- Temporary shard/executor material: the owning skill workspace or an isolated temporary directory; retain it
  only when it contributes cited claim packets to the dossier.
- Evidence boundary: research deliverables remain under the research route even when reviewed. `evidence/` is
  reserved for criterion-linked proof of a separate completed change, per `evidence.md`.

## Source bindings

- Primary local sources: skill sources under `skills/<category>/<name>/`, git history, checked-in playbooks,
  eval scenarios/transcripts, and the installed-package provenance in `skills-lock.json`.
- Primary external sources: upstream source repositories at pinned commits, official documentation and
  specifications, first-party APIs, and connected records the user places in scope. Search is discovery;
  inspect the owning source before recording a claim.
- Citation locators: cite repo path plus commit/line or URL plus version/section and date. For upstream skill
  research, pin the commit SHA. For mutable web material, record accessed date.
- Privacy: keep credentials and unrelated personal data out of dossiers and shard packets. Do not publish or
  send research outside the repo without explicit user authority.

## Parallelism

- Available routes: the staffing-resolved in-session agent route and the independent Codex executor described
  in `environment.md`/the global staffing base. The research coordinator chooses workers through `staffing`.
- Nested fan-out is allowed when backlog already runs issues in parallel. Preserve one slot for the research
  coordinator, size the inner fan-out from remaining capacity, and keep one canonical dossier writer.
- GitHub, rate-limited APIs, and mutable local files are serialized source surfaces unless the worker shards
  are read-only and independent. No worker edits the canonical dossier.

## Presentation

- Markdown is the default canonical dossier. When diagrams or source relationships materially improve review,
  add a self-contained `report.html` beside `findings.md` and keep both derived from the same claim ledger.
- Open the canonical file locally for Asher. When remote review is explicitly needed, use the presentation
  binding in `environment.md`; serve the committed research file in place rather than copying it to evidence.
