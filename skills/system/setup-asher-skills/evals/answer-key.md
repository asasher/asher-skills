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

**P2 — one decision at a time + closure.** PASS if the executor installs `prototype` **and** its required
**`review-loop` + `staffing`** closure, presents decisions **one at a time** with a
**plain-language explainer**, and **tells the user which siblings came along and why** (not a silent pull).
Cite `reference/catalog.md` § The closure rules and/or
`reference/interview.md` § Phase 2. FAIL if it installs `prototype` alone, pulls siblings silently, or dumps the
whole catalog at once.

**P3 — undeclared external request.** PASS if the executor does **not auto-install** the TDD skill or add it to
this setup run, offers an Asher-authored equivalent if one exists, or says it needs a separate deliberate
install. Cite `reference/catalog.md` § Canonical source and declared externals. FAIL if a user mention is
treated as a declaration or consent and an external install command is emitted automatically.

**P4 — context block + playbooks.** PASS if the executor writes the **`## Agent skills` block into the
reconciled instruction layout** (greenfield creates canonical AGENTS.md and a Claude import when needed), **guarantees the `docs/agents/` playbooks by running
each installed skill's own setup** (not by authoring/copying them itself), and writes the **repo pointer** —
and does **not** create an `ask-asher` router. Cite `reference/interview.md` § Phase 4 (steps 3–5) and/or
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

**P8 — primary-only install.** PASS if the executor recognizes one real `.agents/skills/<name>` primary plus
zero aliases as valid, reads project `skills-lock.json`, and at global scope reads
`~/.agents/.skill-lock.json` plus primary/alias mounts and external locks. Cite `reference/audit-mode.md` step
2 and/or `reference/interview.md` Phase 1. FAIL if it requires a Claude alias when that harness is absent,
misses the primary, or uses project `skills-lock.json` as global provenance.

**P9 — alias versus independent copy.** PASS if the symlink to the real primary is the expected alias for one
installed package, while an independent `.claude` directory is an unsafe mount-shape failure that reconcile refuses to
replace. Cite `reference/audit-mode.md` step 3 Mount shape/Overlap. FAIL if it counts the symlink as a second
installed package or automatically deletes/replaces the independent directory.

**P10 — undeclared foreign provenance.** PASS if the executor reports an undeclared external/provenance
finding and treats it as advise-only: it neither legitimizes the install without an active declaration and
external lock nor auto-removes/reinstalls it. Cite `reference/audit-mode.md` step 3 Provenance mismatch. FAIL
if the foreign project lock alone is accepted as declaration or triggers an automatic write.

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
on a no-match — detects that `prototype` did not land, and falls back to direct placement (place `prototype`'s files
from the `asasher/asher-skills` endpoint, canonical-source provenance preserved) with the lock entry in the **specified fallback
shape**: the tool's native fields (`source`, `sourceType`, `skillPath` for github sources) plus
`"fallbackOrigin": true`, and **no `computedHash`** — never a fabricated hash, no free-form extras. Cite
`reference/interview.md` § Phase 4 (landing verification + direct-placement fallback). FAIL if it trusts exit
0 / the "No matching" message as success-enough, ships the broken closure, fabricates a `computedHash`, or
invents unspecified lock fields.

**P14 — optional sibling.** PASS if `interview` alone resolves only `interview` (it requires nothing) in the
compiler's deterministic dependency-first order; when `research` and `prototype` are already present, both
join and bring their required closure (`review-loop`/`staffing` deduplicated). Optional never silently
becomes required. Cite the skills' frontmatter declarations and `reference/catalog.md`.

**P15 — pre-write cycle.** PASS if the compiler rejects the full `a → b → a` cycle before confirmation or
writes and reports the path. Cite `reference/interview.md` Phase 4 and the catalog compiler contract.

**P16 — no setup branch.** PASS if it is a valid no-op and the next owner in dependency order runs; absence
is not failure.

**P17 — partial setup failure.** PASS if staffing's completion and owned writes plus review-loop's failure are
atomically recorded, prototype is not invoked, dependants stop, and retry recompiles then idempotently resumes at
the failed owner without undoing staffing.

**P18 — greenfield instruction files.** PASS if Codex-only creates canonical AGENTS.md; Claude-enabled adds a
minimal CLAUDE.md beginning `@AGENTS.md`; deliberate existing one- and two-file layouts are reconciled rather
than replaced.

**P19 — owner boundaries.** PASS if review-loop's public setup writes only its presentation section and
staffing's public setup preserves the base/reconciles the delta; setup-asher-skills invokes both by public
name and never reads or copies their reference bodies.

**P20 — declared external consent path.** PASS if the executor validates the exact GitHub source and declared
fields, resolves/discloses version or commit, inherited scope, capability, and every discovered hook, obtains
explicit consent before writes, uses the Codex plugin provider, verifies the browser capability rather than
trusting exit zero, and records provider/provenance/requirements/verification in the scope's separate
`external-dependencies.lock.json`. Declined consent means no install and the requiring skill remains
non-operational or is removed from the plan. Cite `reference/interview.md` Phase 4 step 2.

**P21 — external compiler conflicts.** PASS if schema 3 emits `external: []` for the third skill, includes a
sorted merged external list in closure output, and rejects the same-name/different-version declarations before
writes with a conflict naming the declarers. Cite `reference/catalog.md` and `scripts/catalog.py`.

**P22 — strict global verification.** PASS if the executor reads global provenance from
`~/.agents/.skill-lock.json`, rejects the symlink primary even if its target exists, and states reconcile must
not replace it automatically. The absence of a project lock entry is irrelevant to global provenance. Cite
`reference/audit-mode.md` step 2/3 and `reference/interview.md` Phase 4 step 1.

**P23 — declared provider variant.** PASS if root `SKILL.md` owns identity, invocation/execution, siblings,
externals, and setup once; overlays cannot contain `SKILL.md`, `agents/openai.yaml`, or `reference/setup.md`;
both active harness mounts become self-contained real directories; the provider lock records shared-source
revision, provider identity/mount, and effective hash; and all destinations plus the lock are preflighted so
failure restores every old tree and leaves the old lock unchanged. Cite `reference/catalog.md` and
`reference/interview.md` Phase 4.

**P24 — variant audit taxonomy.** PASS only for distinct `missing-provider-mount`, `wrong-provider`,
`altered-tree-hash`, and `shared-contract-drift` findings; the unvaried independent Claude directory is
`undeclared-independent-copy`. It must not flag valid declared divergence merely because hashes differ.

**P25 — global owner boundary.** PASS if the executor requires both providers' Presentation and Staffing
modules to stage and read back into the shared barrier before any pointer application. After the barrier
passes, both globals preflight; setup applies both `## Presentation` sections before staffing applies either
`## Staffing` section, then finalize verifies all four and removes the barrier. User and sibling-owner bytes
are preserved exactly. A missing/unreadable/changed module or failed preflight leaves both globals untouched, local
opening remains available, publish/dispatch is blocked as applicable, no eager import is used, consent is
required, and a second reconcile changes zero bytes.

**P26 — staffing pointer fire/non-fire/all triggers.** PASS if the leaf edit does **not** load staffing and
every other case **does** load it before acting, mapped respectively to the pointer's model choice,
delegation, child/worktree creation, browser/computer/imagegen work, watcher, and route-loss fallback
triggers. FAIL if it eagerly loads on the leaf edit or misses any named trigger. Cite the installed provider
pointer, not a source placeholder or the other provider.

**P27 — staffing unreadable and project-delta order.** PASS if a routing trigger loads the global deferred
module fully, then applies the sparse project delta, then resolves; when the module is unreadable it reports
the gap and does **not dispatch**. The project delta does not replace, precede, or rescue an unreadable global
base. Cite the installed staffing pointer and module resolution rule.

**P28 — presentation pointer fire/non-fire/unreadable.** PASS if merely editing HTML does not load the module,
while opening, serving, publishing, and changing a presentation route each load it before the action. With an
unreadable module, open locally and do not publish. Cite the installed Claude pointer. FAIL for eager loading,
a missed named trigger, or an improvised public fallback.

**P29 — cross-owner four-module barrier.** PASS if the failed fourth stage means **neither global file changes
at all**. Once all four current paths/hashes verify, both globals preflight; setup applies both Presentation
sections before staffing applies either Staffing section, preserving every other byte. Finalize verifies all
four sections and removes the barrier. Repeating the full reconcile leaves module/global bytes and inodes
unchanged and again leaves no barrier. Cite `reference/interview.md` Phase 4 and the checked-in barrier test.
FAIL if an owner applies early, a failed preflight permits either global to change, or one owner rewrites the
other's section.
