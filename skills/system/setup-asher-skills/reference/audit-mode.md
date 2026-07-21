# Audit mode — reconcile an existing install

Routing into `audit` is per SKILL.md; this mode also handles the populated-but-no-map state and repairs it
through the **Missing map** finding. Compare what's installed against this repo's current
catalog and report what drifted, overlaps, or broke — then propose fixes one at a time.

## Reconciliation is an LLM audit — no version stamps

**Reconciliation is the model reading the live repo against what's installed and judging it — not a number
comparison.** setup writes **no version stamp, no `vNN` marker, no content hash, and no template-version
comment** as the drift-detection mechanism, and it does not look for one. This is the shared posture across
this repo's operator skills. If you find yourself wanting to write or diff a version token to detect
drift, that is the wrong mechanism for this skill: read the installed text and the repo, and judge.

(The provider maintains project `skills-lock.json` and global `~/.agents/.skill-lock.json` records for install
provenance — setup reads their source/scope fields but does not use their hashes as its drift judgment. Declared
externals have a separate consumer-owned `external-dependencies.lock.json`; setup adds no version stamp to the
skill payload. Declared provider variants additionally use `variant-lock.json` effective-tree hashes to verify
the installed build product; those hashes prove provider bytes/provenance, not semantic policy freshness.)

## What the audit does

1. **Compile the repo's current catalog.** Fetch the repo (the public GitHub endpoint
   `https://github.com/asasher/asher-skills`) and compile the catalog fresh from its `skills/` sources
   (`python3 skills/system/setup-asher-skills/scripts/catalog.py compile --root <checkout>`) — each skill's
   frontmatter is the source of truth for names, invocation/execution axes, required/optional sibling edges,
   merged external requirements, setup branches, and declared provider variants; **no stored snapshot
   exists to read or to drift**. If the
   repo being audited is the source itself (git remote is `asasher/asher-skills`, or a local `skills/` dir
   holds these skills), use the local `skills/` working tree as the catalog instead of the fetched remote, and
   state the branch-vs-origin relationship (for example, "local is ahead of origin"), compile the local
   declarations, and fail on duplicate names, broken setup pointers, missing dependencies, or required cycles
   so local work does not look like fleet-wide drift. This is the single shared **repo is the source**
   detection consumed by both the
   READ path here (which catalog to diff) and the WRITE path in [interview](interview.md) Phase 4 (the install
   guard), so the two cannot diverge.
2. **Read what's installed and classify every mount.** At project scope read `skills-lock.json`, primary
   `.agents/skills/` mounts, alias mounts such as `.claude/skills/`,
   `external-dependencies.lock.json`, and `.agents/asher-skills/variant-lock.json`. At global scope read `~/.agents/.skill-lock.json` for provenance,
   primary `~/.agents/skills/` mounts, aliases such as `~/.claude/skills/`, and
   `~/.agents/external-dependencies.lock.json`. Also read the `## Agent skills` block and `docs/agents/`
   playbooks. Run `scripts/install.py inspect` for each installed Asher-authored skill: resolving symlinks is
   not enough, because it can hide a primary symlink or independent alias directory. An unvaried package must
   have a real `.agents/skills/<name>` primary and zero or more aliases that symlink to it. A declared variant
   instead has one self-contained real directory per confirmed active provider; run
   `scripts/install.py audit-variant` because comparing those trees to each other misclassifies intentional
   divergence as drift.
   Do not classify consumer-owned skill instance directories such as `control-plane/` as package mounts or
   drift; their editable scaffold/configuration/state/artifacts survive package reconciliation.
3. **Compare and report — in prose.** Describe each finding and what to do about it:
   - **Drift** — a skill installed here whose content diverges from the repo's current version. A
     fallback-origin `skills-lock.json` entry (`"fallbackOrigin": true`, no
     `computedHash` — the shape specified in [interview](interview.md) Phase 4), hand-placed because the tool
     could not install the skill, is expected, not drift: its `computedHash` is intentionally uncomputed, so
     do not flag it as drifted.
   - **Mount shape** — a missing/regular-file/symlink primary, or an alias that is dangling, targets another
     installed package, is a regular file, or is an independent directory. Missing/dangling/wrong symlink aliases may be
     reconciled with `scripts/install.py reconcile` after approval. A primary symlink or independent alias
     directory is unsafe and must be refused, not replaced automatically.
   - **Provider variant** — report separately: `missing-provider-mount`; `wrong-provider` (including a
     provider symlink where a real tree is declared); `altered-tree-hash`; `undeclared-independent-copy` for
     a real alias directory on an unvaried skill; and `shared-contract-drift` when provider trees disagree on
     protected `SKILL.md`, `agents/openai.yaml`, or setup ownership. Also report missing/stale provider-lock
     provenance. Valid declared divergence with matching source revision, provider identity, effective hash,
     and mount type passes.
   - **Overlap** — a skill installed both project and global, or listed twice; say which scope should win
     (project-first: keep local, drop the redundant global unless it is `staffing`). A
     `.claude/skills/<name>` alias symlinked to the primary is the expected mount shape, not overlap; an
     independent alias directory is a Mount-shape finding, not overlap.
   - **Broken closure** — a composer installed without its required sibling closure; name the missing
     siblings from the generated catalog. Optional siblings are findings only when explicitly selected or
     previously installed; never silently promote one to required.
   - **Scope conflict** — something global that should be project-local, or a project-local `staffing` that
     the user might want global; state the project-first default and let the user decide.
   - **Provenance mismatch** — an Asher-authored skill whose project `skills-lock.json` or global
     `~/.agents/.skill-lock.json` source is not `asasher/asher-skills` (or the self-host root), a mount with no
     lock entry, or a lock entry with no mount. Offer the canonical Asher source after consent. A foreign skill
     or Codex plugin is valid only when it exactly matches an active skill source's `metadata.external` and the
     consumer's `external-dependencies.lock.json`; otherwise surface it as undeclared and advise only, never
     auto-install or auto-remove it.
   - **External requirement** — a selected closure's declared external is missing, unverified, or differs in
     name/kind/source/version/capability from `external-dependencies.lock.json`, or a locked external is no
     longer declared. Re-run the provenance disclosure, consent, provider install, and capability check for a
     required repair; stale undeclared entries are removal proposals, not automatic removals.
   - **New in the repo** — a skill the repo now ships that fits this project and isn't installed; offer it.
   - **Orphaned map entry** — a `## Agent skills` line for a skill no longer installed; propose removing it.
   - **Missing map** — installed asher-skills are present but there is no `## Agent skills` block; propose
     writing the block, then continue the same one-fix-at-a-time audit discipline.
   - **Global owner drift** — setup audits only its Presentation pointer/module and leaves Staffing bytes
     untouched. A missing module blocks publishing but preserves local opening. Pointer migration is proposed
     through the per-owner global apply ([interview](interview.md) Phase 4 step 6).
   - **Cross-harness wrapper drift** — a sibling CLI invoked directly, an unbounded or interactive command, a
     wrapper that synthesizes/judges, a label missing external model/task, or absent wrapper-model evidence.
     If spawn cannot select or report the assigned native model, observability may pass but cheapest-floor
     compliance remains unproven; never upgrade that finding from the command's exit status.
4. **Propose fixes one at a time.** Same discipline as `setup`: present each proposed change with a
   plain-language reason, one decision at a time, and change nothing until the user approves — then apply and
   refresh the `## Agent skills` block.

Completion criterion: every content, closure, mount-shape, scope, and provenance divergence between the
installed set and the current catalog is reported, and the user has decided on each proposed fix.
