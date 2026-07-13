# setup-asher-skills — probe answer key

Written before any run. Grade each probe pass/fail against its key; a probe passes only if **both** executors
(Claude in-session + gpt-5.6-sol via `codex exec`) satisfy it. Cited file/sentence must actually support the
answer.

**P1 — three-part audit.** PASS if the executor names **three** audit surfaces — the **repo** (remotes,
AGENTS/CLAUDE.md + existing block, installed skills project+global, docs/agents), the **machine** (reachable
models + Codex), and the **user/project** ("what is this project for?") — **and** says the machine audit is
done by **invoking the `staffing` skill by name**, not by re-deriving a roster. Cite `reference/interview.md`
§ Phase 1 (or `SKILL.md` phase 1). FAIL if it lists fewer than three surfaces, or reimplements the model probe
instead of composing staffing.

**P2 — one decision at a time + closure.** PASS if the executor installs `plan` **and** its required
**`review-loop` + `staffing`** closure, offers `prototype` only when selected/already present, presents decisions **one at a time** with a
**plain-language explainer**, and **tells the user which siblings came along and why** (not a silent pull).
Cite `reference/catalog.md` § The closure rules and/or
`reference/interview.md` § Phase 2. FAIL if it installs `plan` alone, pulls siblings silently, or dumps the
whole catalog at once.

**P3 — pull only from this repo.** PASS if the executor **refuses to install from Matt Pocock's (or any
external) repo**, installs only from `asasher/asher-skills`, and either **offers our adapted equivalent if we
ship one or says plainly we don't ship it** — never emitting an external install command. Cite
`reference/catalog.md` § Pull only from this repo. FAIL if it emits `npx skills add mattpocock/...` or any
non-`asasher` install.

**P4 — context block + playbooks.** PASS if the executor writes the **`## Agent skills` block into the
reconciled instruction layout** (greenfield creates canonical AGENTS.md and a Claude import when needed), **guarantees the `docs/agents/` playbooks by running
each installed skill's own setup** (not by authoring/copying them itself), and writes the **repo pointer** —
and does **not** create an `ask-asher` router. Cite `reference/interview.md` § Phase 4 (steps 2–4) and/or
`SKILL.md` § How it composes. FAIL if it hand-writes the playbooks, or invents a router.

**P5 — audit mode, no version stamps.** PASS if the executor **fetches the repo's current catalog**, **diffs
it against what's installed** (project + global), **reports drift/overlap/broken-closure/scope-conflict in
prose**, proposes fixes **one at a time**, and detects drift by **reading the installed skill against the
repo's current version — explicitly NOT by comparing a version stamp / vNN / hash marker.** Cite
`reference/audit-mode.md` § Reconciliation is an LLM audit — no version stamps. FAIL if it introduces or
compares a version stamp as the drift mechanism.

**P6 — project-first scope.** PASS if the executor scopes **everything project-local by default**, keeping
`backlog` (and its closure) project-local, and offers **`staffing` a global install only, with consent** (via
staffing's consent gate), asking about scope only for staffing. Cite `reference/catalog.md` § Scope —
project-first and/or `reference/interview.md` § Phase 2. FAIL if it offers `backlog` global, installs staffing
global without consent, or makes everything global.

**P7 — routing paradox.** PASS if the executor routes to **audit** (not setup) because installed asher-skills
are prior-install evidence even without a `## Agent skills` block, and notes that audit's Missing-map finding
writes the block. Cite `SKILL.md` routing. FAIL if it routes to setup.

**P8 — `.agents/skills/` scan.** PASS if the executor reads both `.claude/skills/` and `.agents/skills/` at
project scope and both `~/.claude/skills/` and `~/.agents/skills/` at global scope, and therefore reports the
`.agents`-only skill as installed. Cite `reference/audit-mode.md` step 2 and/or `reference/interview.md`
Phase 1. FAIL if it reads only `.claude/skills/` and misses it.

**P9 — cross-harness overlap.** PASS if the executor names the cross-harness-duplication category and
classifies the symlinked pair as benign/note-only (one underlying skill), distinct from independent copies
(flag + consolidate). Cite `reference/audit-mode.md` step 3 Overlap. FAIL if it reports the symlinked pair as
drift, or has no cross-harness category.

**P10 — foreign source.** PASS if the executor raises a Foreign-source finding, honors pull-only by offering
our equivalent or saying we don't ship it, never reinstalls from `mattpocock/skills`, and treats it as
advise-only with no auto-remove. Cite `reference/audit-mode.md` step 3 Foreign source and
`reference/catalog.md` § Pull only from this repo. FAIL if it proposes a `mattpocock` reinstall or auto-removes
the skill.

**P11 — self-catalog.** PASS if the executor uses the local `skills/` working tree as the catalog, not the
fetched remote, because the repo is the source and a local branch ahead of origin would disagree; it must also
state branch-vs-origin. Cite `reference/audit-mode.md` step 1 self-host. FAIL if it diffs against the fetched
remote and reports the local branch's skills as drift.

**P12 — self-host write guard.** PASS if the executor recognizes the self-host case via the repo-is-the-source
detection shared with `reference/audit-mode.md` step 1 and **still mounts** the repo-owned skills — source
presence is not an install: it emits one `npx skills add <repo-root> --skill <ordered closure names...> -y`
(the repo's own root as a **local source**), not the GitHub endpoint, and states the resulting mounts — canonical copies at
`.agents/skills/<name>`, per-harness symlink at `.claude/skills/<name>`, tool-written `skills-lock.json` entry
— while never treating the catalog-resolved source as an install destination; and still writes the `## Agent skills`
block, repo pointer, and guaranteed playbooks. Cite `reference/interview.md` § Phase 4 (self-host mount) and/or
`reference/audit-mode.md` step 1. FAIL if it stops at register-only (writes the block/pointer but mounts
nothing, leaving the closure non-functional), emits the GitHub endpoint for repo-owned skills, targets
the source directory as a destination, or moves/symlinks the source dirs themselves.

**P13 — silent install miss.** PASS if the executor batches the scope's existing public asher-skills plus the
new closure in one command, then verifies every landing on the filesystem/lock rather than trusting the exit code — knowing `npx skills add` exits 0
on a no-match — detects that `plan` did not land, and falls back to direct placement (place `plan`'s files
from the `asasher/asher-skills` endpoint, pull-only preserved) with the lock entry in the **specified fallback
shape**: the tool's native fields (`source`, `sourceType`, `skillPath` for github sources) plus
`"fallbackOrigin": true`, and **no `computedHash`** — never a fabricated hash, no free-form extras. Cite
`reference/interview.md` § Phase 4 (landing verification + direct-placement fallback). FAIL if it trusts exit
0 / the "No matching" message as success-enough, ships the broken closure, fabricates a `computedHash`, or
invents unspecified lock fields.

**P14 — optional sibling.** PASS if plan alone resolves `review-loop → staffing → plan` in a deterministic
dependency-first order (the relative order of the two roots follows the compiler output); when prototype is
present it joins and brings its required closure. Optional never silently becomes required. Cite
`catalog.json` and `reference/catalog.md`.

**P15 — pre-write cycle.** PASS if the compiler rejects the full `a → b → a` cycle before confirmation or
writes and reports the path. Cite `reference/interview.md` Phase 4 and the catalog compiler contract.

**P16 — no setup branch.** PASS if it is a valid no-op and the next owner in dependency order runs; absence
is not failure.

**P17 — partial setup failure.** PASS if staffing's completion and owned writes plus review-loop's failure are
atomically recorded, plan is not invoked, dependants stop, and retry recompiles then idempotently resumes at
the failed owner without undoing staffing.

**P18 — greenfield instruction files.** PASS if Codex-only creates canonical AGENTS.md; Claude-enabled adds a
minimal CLAUDE.md beginning `@AGENTS.md`; deliberate existing one- and two-file layouts are reconciled rather
than replaced.

**P19 — owner boundaries.** PASS if review-loop's public setup writes only its presentation section and
staffing's public setup preserves the base/reconciles the delta; setup-asher-skills invokes both by public
name and never reads or copies their reference bodies.
