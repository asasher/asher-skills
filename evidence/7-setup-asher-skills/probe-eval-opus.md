# setup-asher-skills — probe answers (Opus)

## P1 — What to audit before recommending; how to find reachable models
**ACTION:** Run Phase 1 audit of three surfaces, silently, recommending nothing yet:
1. **The repo** — `git remote -v` (also confirms the pull endpoint), read `AGENTS.md`/`CLAUDE.md` incl. any existing `## Agent skills` block, skills installed both project (`skills-lock.json`, `.claude/skills/`) and global (`~/.claude/skills/`), and the `docs/agents/` playbooks present.
2. **The machine** — determine reachable models + whether Codex CLI is installed **by invoking the `staffing` skill by name** (not re-deriving a roster). If staffing isn't reachable, say the machine audit needs it rather than inventing one.
3. **The user/project** — ask the ONE question: *what is this project for?*
**CITATION:** interview.md Phase 1: "The machine. Determine the reachable models and whether the Codex CLI is installed — the staffing probe. Do this by invoking the `staffing` skill by name, not by re-deriving a roster"; and Phase 1(1) enumerating the repo reads.
**AMBIGUITY:** None.

## P2 — Shipping web product; user accepts `plan`
**ACTION:** Install `plan` plus its auto-pulled sibling closure: **`review-loop` + `staffing`** (not full backlog machinery). Tell the user in plain language which siblings came along and why — e.g. "Adding `plan` also brings `review-loop`, which you'll use to approve the plan, and `staffing`, which picks which model writes it — they work together." (Note: for a shipping product the seed recommends `backlog`, but the user accepted `plan`, so I install `plan`'s closure, not backlog's.)
**CITATION:** catalog.md closure rules: "`plan` ⇒ ensure `review-loop` + `staffing`."; interview.md Phase 2: "Accepting a composer auto-pulls its sibling closure — and you say so … tell the user in plain language which siblings came along and why."
**AMBIGUITY:** None on closure. Minor: seed favors `backlog` for shipping web products, but the accepted decision governs.

## P3 — Mid-interview: "install the TDD skill from Matt Pocock's repo"
**ACTION:** Do NOT reach out to the external repo. Offer our adapted equivalent if this repo ships one; if not, say plainly that we don't ship it. Every install command targets `asasher/asher-skills` and nothing else.
**CITATION:** catalog.md § Pull only from this repo: "when a user asks for an external skill by name — 'install the TDD skill' — the move is: offer our adapted equivalent if we ship one, or say plainly that we don't ship it. Never reach out to the external repo."
**AMBIGUITY:** Whether we ship a TDD equivalent — I'd check the catalog before answering; absent one, the honest "we don't ship it" is correct, not a reason to break the invariant.

## P4 — Plan approved & installs run; what to write into the repo and where
**ACTION (Phase 4):**
- **`## Agent skills` block** — from `templates/agent-skills-block.md`, written into the harness memory file, **preferring `AGENTS.md` if it exists, else `CLAUDE.md`.** One row per installed skill with a one-line plain-language purpose, notes sibling relationships, links the repo pointer. No version stamp. It is the map — no `ask-asher` router.
- **Repo pointer** — from `templates/repo-pointer.md`, recording skills come from `https://github.com/asasher/asher-skills` and that updates/reconciliation run by re-invoking this skill.
- **`docs/agents/` playbooks** — NOT authored by setup. **Guaranteed by delegation**: run each installed skill's own setup (staffing writes the roster; review-loop/backlog setup writes presentation surface config; backlog setup writes its `docs/agents/` suite). setup does not re-copy any skill's templates.
**CITATION:** interview.md Phase 4 steps 2–4: "Guarantee the playbooks by delegation … setup does not re-copy any skill's templates"; "Write the `## Agent skills` block … prefer `AGENTS.md` if it exists, else `CLAUDE.md`"; "Write the repo pointer."
**AMBIGUITY:** None.

## P5 — Project already has a `## Agent skills` block from 3 months ago
**ACTION:** Existing block ⇒ run **`audit` mode** (audit-mode.md). Fetch the repo's current catalog from the public GitHub endpoint; read what's installed in both scopes plus the block and `docs/agents/`; compare and report in prose (drift, overlap, broken closure, scope conflict, new-in-repo, orphaned map entries); propose fixes one at a time, changing nothing until approved.
**Detecting drift:** reconciliation is an **LLM read** — read the installed skill's text AND the repo's current version and **judge** whether they diverge. Do **not** write or diff a version stamp / `vNN` / hash / template-version comment. (The `skills` tool's own `skills-lock.json` hashes are the tool's bookkeeping, not setup's drift mechanism.)
**CITATION:** audit-mode.md: "Drift — a skill installed here whose content diverges from the repo's current version (read both and judge; don't diff a stamp)"; and "setup writes no version stamp … If you find yourself wanting to write or diff a version token to detect drift, that is the wrong mechanism."
**AMBIGUITY:** None.

## P6 — User accepts both `staffing` and `backlog`; scope of each
**ACTION:**
- **`staffing`** — the one skill offered **global** (a reusable model roster). Offer global with a one-sentence explainer and route the global write through staffing's own consent gate. If consented: `-g -y`.
- **`backlog`** — **project-local** (default), and it pulls its full closure: ensure ALL of `staffing`, `review-loop`, `plan`, `prototype` (transitive closure adds nothing more). backlog itself and its non-staffing siblings stay project-local.
- **Ask the user:** about **scope only where it matters** — i.e. ask whether to install **`staffing` globally** (with consent). Don't ask scope for backlog or the other siblings; they're project-local by default.
**CITATION:** catalog.md § Scope: "Global only for `staffing`, only with consent … No other skill is offered global"; interview.md Phase 2: "Scope is surfaced only where it matters … the only skill offered a global install is `staffing`"; catalog closure: "`backlog` ⇒ ensure ALL of `staffing`, `review-loop`, `plan`, `prototype`."
**AMBIGUITY:** If the user wants `staffing` project-local instead of global, that's their call (project-first default still honored) — I offer global, don't force it.
