# setup-asher-skills — probe answer key

Written before any run. Grade each probe pass/fail against its key; a probe passes only if **both** executors
(Claude in-session + gpt-5.5 via `codex exec`) satisfy it. Cited file/sentence must actually support the
answer.

**P1 — three-part audit.** PASS if the executor names **three** audit surfaces — the **repo** (remotes,
AGENTS/CLAUDE.md + existing block, installed skills project+global, docs/agents), the **machine** (reachable
models + Codex), and the **user/project** ("what is this project for?") — **and** says the machine audit is
done by **invoking the `staffing` skill by name**, not by re-deriving a roster. Cite `reference/interview.md`
§ Phase 1 (or `SKILL.md` phase 1). FAIL if it lists fewer than three surfaces, or reimplements the model probe
instead of composing staffing.

**P2 — one decision at a time + closure.** PASS if the executor installs `plan` **and** auto-pulls
**`review-loop` + `staffing`** (the closure), presents decisions **one at a time** with a **plain-language
explainer**, and **tells the user which siblings came along and why** (not a silent pull). Cite
`reference/catalog.md` § The closure rules (`plan ⇒ ensure review-loop + staffing`) and/or
`reference/interview.md` § Phase 2. FAIL if it installs `plan` alone, pulls siblings silently, or dumps the
whole catalog at once.

**P3 — pull only from this repo.** PASS if the executor **refuses to install from Matt Pocock's (or any
external) repo**, installs only from `asasher/asher-skills`, and either **offers our adapted equivalent if we
ship one or says plainly we don't ship it** — never emitting an external install command. Cite
`reference/catalog.md` § Pull only from this repo. FAIL if it emits `npx skills add mattpocock/...` or any
non-`asasher` install.

**P4 — context block + playbooks.** PASS if the executor writes the **`## Agent skills` block into
`AGENTS.md`/`CLAUDE.md`** (prefer AGENTS.md if present), **guarantees the `docs/agents/` playbooks by running
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
