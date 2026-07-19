# Raw cold-reader reports (verbatim)

Five context-free readers, 2026-07-20. Each was told only: "you are an agent who must execute this
skill cold; flag what the files can't ground" — no authoring history, no answer keys. Apply fixes
from these quotes; synthesis in `findings.md`.

---
---

# Report 1 — backlog

I read every file under `skills/delivery/backlog/` (SKILL.md, all of reference/, all of templates/) plus the pointers between them, as a cold consumer. Findings, grouped by file, most severe first. All paths are under `/Users/asher/Projects/asher-skills/skills/delivery/backlog/`.

## SKILL.md

**1. CONTRADICTION — "optional" diagnosing-bugs playbook vs. run's hard requirement.**
> `diagnose` row: "optional `docs/agents/diagnosing-bugs.md` delta + `environment.md`"

vs. `reference/run.md` step 1: "Completion criterion: every playbook in the **resolved scaffold set** … has its `docs/agents/` counterpart, **plus `docs/agents/diagnosing-bugs.md` and `docs/agents/researching.md`**." A cold reader running `run` must fail preflight on a repo the SKILL.md table told them was fine. Fix: single-home the requirement — either drop "optional" from the SKILL.md table row, or drop the two files from run's completion criterion. Which one is a behavior choice → QUESTION.

**2. CONFUSION — ambiguous routing sentence.**
> "invoke `staffing` or `review-loop` directly for their own commands."

Neither `staffing` nor `review-loop` appears in the command table, so "their own commands" has no antecedent I can resolve: does this mean the *user* should invoke them, or that I, on seeing `backlog staffing …`, should delegate to the sibling like the `prototype`/`research` case? Fix: reword to "a first word of `staffing` or `review-loop` is not a backlog command — invoke that sibling skill directly instead."

## reference/run.md and reference/run-state.md (paired findings)

**3. CONTRADICTION — `verify-terminal` is not in run-state's own subcommand list.**
`run-state.md` line 5:
> "Use `scripts/run-state.py append|project|verify-owner|handoff`; do not hand-edit streams or projections."

but `run.md` step 6 orders: "run `scripts/run-state.py verify-terminal --run-id <run>`", and `run-state.md` itself later says "`run-state.py verify-terminal` refuses a terminal report…". A cold reader auditing allowed subcommands would conclude `verify-terminal` is not one. Fix: add `verify-terminal` to the enumerated list in `run-state.md`.

**4. REDUNDANCY (drifted) — terminal status enumeration differs.**
`run.md` step 6: "**`completed | blocked(edge) | deferred(wave) | returned | interrupted`**" vs. `run-state.md`: "(`complete | blocked | deferred | returned | interrupted`)". Same enumeration, two spellings (`completed`/`complete`, with/without qualifiers) — a reader writing an event doesn't know which token the verifier expects. Fix: pick one canonical token set (single-home in `run-state.md`, since the script consumes it) and have `run.md` quote it exactly.

**5. REDUNDANCY — the verify-terminal gate is stated twice with drifted wording.**
`run.md` step 6: "a missing `handoff.md` or a non-terminal parent refuses completion; fix the state, never the report." and `run-state.md`: "refuses a terminal report while `handoff.md` is missing or any parent's latest status is non-terminal". Fix: single-home the rule in `run-state.md`; `run.md` keeps only the pointer and the "fix the state, never the report" instruction.

**6. CONFUSION — heartbeat interval wording inverts the guarantee.**
> "While any issue is active, emit a heartbeat at most every 10 minutes"

Read literally, "at most every 10 minutes" caps *frequency* (no more often than every 10 min); the evident contract is a staleness bound (no *gap* longer than 10 min). Fix: reword to "at least every 10 minutes" or "with no more than 10 minutes between heartbeats."

**7. CONFUSION / UNDEFINED TERM — "the harness's staffing module".**
> "The harness's staffing module names its native wake sources"

Everywhere else this capability is "the `staffing` skill (by name)". "Module" appears only here; a cold reader doesn't know whether this is the staffing skill, some harness component, or a playbook section. Fix: reword to "the `staffing` skill's guidance for this harness names its native wake sources."

## reference/build-loop.md

**8. CONFUSION — the draft "degeneration" of step 6 is defined only inside step 4, and only vaguely.**
> step 4: "Correspondingly, step 6 adversarial review degenerates for a pure-prose artifact (the human verdict was the review); a code-docs draft keeps a light correctness pass over the docs it touches."

Executing step 6 for a draft, I don't know what "degenerates" means operationally — skip `reference/adversarial-review.md` entirely? Run it with a reduced bar? And is the "light correctness pass" run through the Reviewer/Fixer machinery or informally by the coordinator? Fix: state it in step 6 itself ("**draft exception:** skip this step for a pure-prose draft — the step-3 review verdict stands; for a code-docs draft run one Reviewer pass limited to correctness of the touched docs" — confirm intended mechanics → QUESTION if that's not it).

**9. REDUNDANCY — the no-approval-gate rule stated twice in one bullet.**
> step 3: "…recorded in the thread and reflected in the PR body; **never a human gate**…" and, same bullet: "There is no in-run planning approval gate."

Same rule twice in one paragraph; the second sentence also reads as authoring-context reassurance (arguing against an expectation the files never set up) rather than an instruction. Fix: delete "There is no in-run planning approval gate." — "never a human gate" already binds.

## templates/common/change-description.md

**10. CONTRADICTION / QUESTION — the Plan bullet assumes an approved, committed plan that enhancements are told not to have.**
> "**Plan** (enhancements) — SHA-pinned link to the committed plan, noting where it was approved."

`build-loop.md` step 3 says the enhancement plan is "a **just-in-time tactical plan** — … recorded in the thread and reflected in the PR body; never a human gate". A JIT plan is neither committed nor approved, so a cold reader building the PR body cannot satisfy this bullet. (`implement.md` acknowledges both cases: "an approved plan artifact where one exists … otherwise the issue thread's just-in-time tactical plan".) Fix: reword the bullet to cover both — "SHA-pinned link to the committed plan artifact where one exists (noting where it was approved); otherwise the just-in-time tactical plan inline". Since this changes what the PR body must contain for JIT plans, flagging as QUESTION.

## templates/software/verifying.md

**11. CONTRADICTION — interactive criteria "written into the PR body at its start" vs. the loop's ordering.**
> "interactive chat-and-build: the criteria the build loop wrote into the PR body at its start — verify always has a target, even without a ticket."

In `reference/build-loop.md` the PR is created at step 5, *after* verify (step 4). At verify time in an interactive run there is no PR body to read criteria from. Fix requires deciding where interactive criteria actually live before the PR exists → QUESTION.

**12. UNGROUNDED POINTER + UNDEFINED TERM — the evidence-degrade rule doesn't exist where cited, and "AFK" is undefined.**
> "Evidence obligation scales with absence (`evidence.md`): an AFK run owes the full evidence package — nobody watched; interactive work may degrade to the PR body's verification grades where the playbook allows"

`templates/software/evidence.md` contains no scaling-with-absence or interactive-degrade rule, so "(`evidence.md`)" and "where the playbook allows" resolve to nothing. "AFK" is never expanded anywhere reachable. Fix: either add the degrade rule to `templates/software/evidence.md` (single-home it there and keep this as pointer) — a behavior decision → QUESTION — and spell out "unattended (AFK) run".

**13. UNDEFINED TERMS — spec/slice vocabulary from an unnamed upstream flow.**
> "a ticketed run: the ticket's acceptance block (inheriting its spec's per-slice acceptance); a spec without tickets: the spec's acceptance for the slice being built"

"Spec" and "slice" are terms from a shaping flow the skill never defines (see finding 19). Fix: one sentence defining them, or reword to tracker-neutral language ("the acceptance criteria recorded on the ticket / in its source document").

## templates/software/implementing.md

**14. UNDECLARED DEPENDENCY + UNGROUNDED — `bare-minimum-ux` is mandatory but not a declared sibling; "Asher's policy overlay" is authoring provenance.**
> "Building UI always loads the `bare-minimum-ux` skill (Asher's policy overlay — it wins on conflict)."

SKILL.md's `requires` is `[diagnosing-bugs, prototype, research, review-loop, staffing]`; `bare-minimum-ux` is nowhere declared, and no degrade is stated ("always loads"), so a cold consumer in a repo without it fails silently — exactly what the skill's own dependency-surface rules forbid. "Asher's policy overlay" is meaningless to a consumer. Same undeclared reference recurs in `templates/software/verifying.md` § UI surfaces: "per the `bare-minimum-ux` overlay". The `impeccable` external at least self-gates on `external-dependencies.lock.json`. Fix: declare the dependency or add degrade wording ("where installed; otherwise state the gap") — dependency-surface change → QUESTION.

## reference/setup.md

**15. UNGROUNDED — history-framed legacy references a cold reader cannot ground.**
> "…is a stamp from the retired versioning scheme — delete the line…" and "`<!-- backlog-section: ... -->` markers in `AGENTS.md`/`CLAUDE.md` (the old picking-models install) are the `staffing` skill's concern"

Nothing reachable establishes what "the versioning scheme" or "picking-models" were. The *operative* halves (delete the stamp line; leave the markers) survive cold, but "picking-models" is an undefined name. Fix: reword to drop the history — "a `<!-- backlog-templates: ... -->` … comment on line 1 is a legacy stamp: delete the line…"; "`<!-- backlog-section: ... -->` markers … belong to the `staffing` skill — leave them."

**16. CONTRADICTION — section-name pointers that fail on a skill-authoring install.**
Step 6: "per the driver-per-surface defaults and gates in `environment.md` § Driving the app & capturing evidence" and "fill every row of `environment.md` § Verification data". But `templates/skill-authoring/environment.md` names its section "**Driving behavior & capturing evidence**" and has **no** "Verification data" section at all. On a skill-authoring install, setup's completion criterion ("a complete verification-data inventory") cannot be satisfied against the installed playbook. Fix: rename the skill-authoring section to match common, and add a (skill-flavored) Verification data section to `templates/skill-authoring/environment.md` — or soften setup's pointer; adding a section is arguably behavior → QUESTION.

**17. CONFUSION — "migrations" appears once, undefined.**
Step 11 checklist: "…playbooks tailored to house practice where the repo has one; **migrations applied and conflicts resolved**." No earlier step performs anything called a migration (steps 1–2 call it reconciliation). A cold reader can't check this item off. Fix: reword to "reconciliations applied and flagged conflicts resolved."

**18. REDUNDANCY (drifted) — the review-loop surface-config list differs from environment.md's.**
Step 7: "(tailnet root, surface dir, publish/proxy commands, keep-awake)" vs. `templates/common/environment.md` § Presenting to the human: "(tailnet root, surface dir, publish/proxy commands, **hub**, keep-awake)". Fix: single-home the list in the environment template; setup points at the section without enumerating. (Also: setup says "§ Presenting" where the section is titled "Presenting to the human" — align the pointer.)

## reference/groom.md and templates/common/backlog-policy.md (paired)

**19. UNDEFINED TERM — "the upstream shaping flow (interview → spec → tickets)".**
`groom.md` step 3: "…routed to the upstream shaping flow (interview → spec → tickets); it re-enters grooming when that flow delivers execution-ready work." and `backlog-policy.md`: "cleared when the upstream shaping flow (interview → spec → tickets) delivers execution-ready work." No file in the skill defines this flow, names who runs it, or declares it as a sibling/external. Since `needs-spec` parks work for a human, the degrade is survivable, but a cold reader cannot tell the human *what* to run. Fix: one grounding sentence in `backlog-policy.md`'s `needs-spec` entry ("whatever process this team uses to settle product/design decisions and produce execution-ready tickets — backlog does not run it") and have groom.md point there.

**20. REDUNDANCY + LATENT CONTRADICTION — the readiness rule is hard-coded in groom.md while the policy declares it adjustable.**
`groom.md` line 7: "the agent proposes and may self-apply any role except `ready-for-agent`, which it applies only to issues the human confirms (step 5)" vs. `backlog-policy.md` § Readiness decision: same rule, plus "**Adjust this rule** if this team wants more or less agent autonomy (e.g. let the agent auto-bless low-risk bugs)." If a team adjusts the playbook, groom.md's fixed wording (and its step 5) still forbids the adjusted behavior — the playbook-overrides-skill model breaks exactly here. Fix: single-home in `backlog-policy.md`; groom.md rewords to "self-apply roles per `backlog-policy.md` § Readiness decision (default: `ready-for-agent` only on human confirmation, step 5)."

## reference/evidence.md and templates/software/change-reviewer.md (paired)

**21. REDUNDANCY (drifted) — the "exact verdict" string differs between its two homes.**
`evidence.md`: "the Reviewer records **"no product-code change; no recapture.**"" (period inside the quotes) vs. `change-reviewer.md`: "record the exact verdict **"no product-code change; no recapture"**" (no period). Both call it exact; a mechanical match against either fails the other. The styling-only reuse rule itself also appears in four places (`evidence.md`, `verify.md` line 11, `templates/software/evidence.md`, `change-reviewer.md`). The pointers are fine; the duplicated *verbatim string* is the hazard. Fix: single-home the exact string in `reference/evidence.md` (pick one punctuation); `change-reviewer.md` says "record the exact verdict quoted in the skill's `reference/evidence.md` § Styling-only reuse."

## reference/adversarial-review.md

**22. CONFUSION — dropped noun in the Fixer role definition.**
> "**Fixer** — watches for Reviewer comments and addresses the current iteration's per its playbook, pushes, and replies."

"the current iteration's" has no noun. Almost certainly "the current iteration's comments", but a cold reader is guessing at a role's core duty. Fix: insert "comments".

**23. CONFUSION — "the approved plan" in Behavior ruling.**
> "The coordinator rules inside the approved plan or escalates to the session orchestrator/human."

For the enhancement branch there is often no *approved* plan — only a just-in-time tactical plan that is "never a human gate" (`build-loop.md` step 3). What bounds the ruling then? Fix: reword to "rules inside the issue's settled or delegated authority (the approved plan where one exists)" — matches build-loop's vocabulary without changing behavior.

## reference/diagnose.md

**24. UNDEFINED TERM — "the existing prototype/approval path".**
> "If the fix exposes a contested design decision, pause the diagnosis handoff and route that question through the existing prototype/approval path before resuming it."

No file defines a "prototype/approval path". Build-loop step 3 defines two distinct routes: a `prototype` session for questions within delegated authority, and a `needs-spec` handback for strategic ones — "approval path" matches neither name. Fix: reword to "route it per `reference/build-loop.md` step 3 — a `prototype` question within delegated authority, or a `needs-spec` handback — before resuming."

## reference/verify.md

**25. CONFUSION — where substitutes get "pre-approved" is only discoverable in a template placeholder.**
> step 2: "An infeasible requirement returns to the approved substitute or ruling; do not invent one here." and step 5: "`static-substitute` (inspection or a pre-approved substitute — name it)"

Nothing in verify.md or its named playbooks says who approves a substitute or where the approval is recorded; the only trace is `templates/common/environment.md` § Verification data: "plan-approved synthetic substitutes and the criterion classes where each is/is not valid". Fix: add the pointer in verify.md step 2 — "(recorded in `environment.md` § Verification data)".

## templates/common/environment.md

**26. UNDEFINED TERMS — machine-specific tool names shipped as unexplained defaults.**
> "**agent-browser with an isolated profile** for the web app (the user's own browser only under a recorded **user-session carve-out**, with per-use consent)" and "default: agentmail for OTP/magic-link inboxes"

`agent-browser`, `agentmail`, and "user-session carve-out" are named nowhere else reachable; a consumer on a machine without these tools can't tell whether they are products to install or role nouns to bind. (They sit in tailorable placeholders, which softens this.) Fix: one clause each — "agent-browser (or this machine's equivalent isolated browser driver)", expand "carve-out" to "a recorded exception permitting use of the user's own browser session", "an email-inbox tool the agent can read (e.g. agentmail)".

## reference/worktree-isolation.md — minor

**27. UNGROUNDED (mild) — rhetorical aside.**
> "…which is the family a naive 'it's just a Node app, worktrees are free copies' read misses."

Argues with an absent interlocutor rather than instructing; harmless but cold-noisy. Fix: delete the clause (the probe list already carries the content). Same class, `run.md` step 2: "Dispatch needs no further confirmation — `ready-for-agent` *is* the human's confirmation from grooming." — kept, since it is operative.

## Files that read clean

- `reference/refactor.md`
- `reference/implement.md` (one loose thread: "e.g. a spec-derived slice" leans on the undefined spec vocabulary of finding 13/19)
- `reference/run-state.md` apart from findings 3–5
- `templates/common/platform.md` (thorough and self-grounding; the `no --bare` Codex example is unverifiable cold but is a tailorable placeholder)
- `templates/software/refactoring.md`
- `templates/software/change-fixer.md`
- `templates/software/evidence.md` (clean in itself; implicated only as the missing home in finding 12)
- `templates/skill-authoring/evidence.md`
- `templates/skill-authoring/verifying.md`
- `templates/common/backlog-policy.md` apart from findings 19–20

Overall: the skill is unusually well cross-wired — almost every pointer resolves, role nouns are defined where first used, and the local-binding contract is genuinely self-contained. The highest-value fixes are the four QUESTION-class items (findings 1, 10, 11, 14): each is a place where two files give a cold executor incompatible marching orders, not just wording drift.

---
---

# Report 2 — shaping trio (interview, domain-modeling, interview-with-docs)

Findings from a cold read of the three skills. I read all SKILL.md and reference/ files; no file in the set points at a `docs/agents/*.md` playbook, so none were pulled in. All by-name sibling references among the three (`interview` ↔ `interview-with-docs` ↔ `domain-modeling`) resolve, as do `research`, `prototype`, and `staffing`.

## skills/thinking/interview-with-docs/SKILL.md

**1. Indeterminate destination when there is no caller — Confusion (QUESTION)**
> "At exit, the interview's open-thread classification is written where the caller directs — an issue comment, a spec's Notes."

Frontmatter says `user-invocable: true`. Invoked directly by a user, there is no caller and no direction — I would not know where to write the classification. QUESTION: should the direct-invocation fallback be "ask the user for a home" or "record in conversation only"? Either fix changes behavior, so the author must pick.

**2. The degraded form is impossible for one of the two siblings — Contradiction/Confusion**
> "Absent either sibling, state the requirement and offer the degraded form — bare `interview` with the classification recorded in the conversation only — rather than failing silently."

"Either sibling" covers `domain-modeling` *and* `interview`. If `interview` is the absent one, the degraded form "bare `interview`" cannot be offered. Fix: reword to "Absent `domain-modeling`, offer the degraded form — bare `interview` with the classification recorded in the conversation only. Absent `interview`, state the requirement and stop."

**3. "a spec's Notes" — Undefined term**
> "an issue comment, a spec's Notes."

No file in this set defines a spec format or its Notes section (that presumably lives in `to-spec`, which this skill names in its description but does not declare as a sibling). Cold, "a spec's Notes" is a capitalized section of an artifact I have no schema for. Fix: reword to "a spec's notes section" (generic), or declare `to-spec` where the pointer matters.

## skills/thinking/domain-modeling/SKILL.md

**4. "groom" named alongside skills but is not a skill — Undefined term**
> "…or when another skill (interview-with-docs, groom, a spec session) needs the model maintained while it works."

The list frames all three items as skills. `interview-with-docs` resolves; `groom` does not exist as a skill anywhere in `skills/` (in this repo it is a stage inside `backlog`, which a consumer repo may not have), and "a spec session" is not a skill either. Fix: reword to "…or when another skill or workflow (e.g. `interview-with-docs`, a backlog grooming stage, a spec-writing session) needs the model maintained while it works."

**5. "Register on create" asserts a repo layout the consumer may not have — Confusion (QUESTION)**
> "add its line to the project instruction file's `## Context documents` index (`AGENTS.md`; `CLAUDE.md` reaches it via its `@AGENTS.md` import — create the section if absent)"

"Create the section if absent" is covered — but not the file. In a repo with only `CLAUDE.md` and no `@AGENTS.md` import (common), I don't know whether to create `AGENTS.md` plus wire the import into `CLAUDE.md`, or just edit `CLAUDE.md`. The parenthetical states the import as a fact about the consumer repo rather than an instruction. QUESTION: which is intended? Suggested wording if the latter: "add its line to the project instruction file's `## Context documents` section (`AGENTS.md` if the repo has one, else `CLAUDE.md`); create the section if absent."

**6. Bullet lead and body state two different rules — Confusion**
> "**Write inline, never batch.** `CONTEXT.md` is a glossary and nothing else — no implementation details, no spec content, no scratch notes."

The bold lead is a timing rule (write each entry as it resolves, not at session end — I'm guessing); the body is a content-scope rule. The timing rule is never actually explained anywhere, so cold I don't know what "batch" would even look like. Fix: split into two bullets, e.g. "**Write inline, never batch.** A term goes into `CONTEXT.md` the moment it resolves, not in an end-of-session sweep." and "**Glossary only.** No implementation details, no spec content, no scratch notes."

**7. "the *active* discipline" implies an unnamed passive counterpart — Ungrounded (minor)**
> "This is the *active* discipline: for when the model is *changing*, not merely consumed."

"The active discipline" reads as one half of a pair whose other half is never named in this file (the description's "merely reading CONTEXT.md… a one-line habit" partially grounds it, but only if the reader connects them). Fix: reword to "This skill is for when the model is *changing*, not merely consumed."

**8. Dependency-surface sentence is addressed to someone else — Confusion (minor)**
> "Callers compose this skill by name; absent it, they state the gap rather than writing glossary entries ad hoc."

This tells *callers* what to do if this skill is absent — but anyone reading this file has, by definition, the skill present. The consumer of this sentence can never act on it here. Fix: delete, or move the degrade rule to the callers (interview-with-docs already carries its own version — see finding 12).

## skills/thinking/interview/SKILL.md

**9. "a cap" has no antecedent — Ungrounded**
> "If a round balloons past comfortable answering, split it by dependency cluster and say so — a cap is manners, not a rule."

No cap (a number, a limit) is established anywhere in the file; "a cap is manners, not a rule" reads like residue of an earlier draft that had a question cap. Cold, I can't tell whether I'm being told there *is* a soft cap or that caps don't exist. Fix: reword to "…split it by dependency cluster and say so — splitting is a courtesy to the reader, not a fixed limit."

**10. "the instruction file's `## Context documents` index" — Undefined term**
> "the durable context — `PRODUCT.md`, `DESIGN.md`, `CONTEXT.md`, ADRs, prior specs — the instruction file's `## Context documents` index is the map when one exists."

"The instruction file" has no antecedent in this file, and the `## Context documents` index is defined only in `domain-modeling` — which `interview` does not declare as a sibling (its optionals are `prototype`, `research`, `staffing`). Bare `interview` in a repo without `domain-modeling` gives me no way to resolve either term. Fix: gloss inline — "the project instruction file (`AGENTS.md` / `CLAUDE.md`)" — and keep "when one exists" doing the degrade work. Related, minor: `PRODUCT.md` and `DESIGN.md` are named nowhere else in the reachable set; they pass as generic examples but are flag-worthy as conventions the file assumes.

**11. Threads classified as "settled" are called "open" — Confusion (minor)**
> "the classification of **every open thread**: *settled*, *delegated* … *deferred* … or *blocking* …"

A thread classified *settled* is by definition not open; cold, I can't tell whether "open threads" means only the unresolved ones (in which case *settled* shouldn't be a class here) or every thread raised. Fix: reword to "every thread" or "every question raised."

**12. Same routing rule in three places with drifted wording — Redundancy**
> interview description: "it writes no durable artifacts — compose `interview-with-docs` for that."
> interview § Exit: "This skill records nothing durable. When settled terms and decisions should outlive the conversation — a glossary term, an ADR, spec input — run `interview-with-docs`."
> interview-with-docs description: "use bare `interview` when nothing durable is wanted."

Three statements of one routing rule, with verb drift ("compose" vs "run") and criterion drift ("durable artifacts" / "outlive the conversation" / "nothing durable is wanted"). Not contradictory, but three homes means three places to drift further. Fix: single-home the full rule in interview § Exit; leave the descriptions as bare pointers ("use `interview-with-docs` for durable output").

**13. Later-round sentence quietly contradicts the frontier definition — Redundancy/Contradiction (minor)**
> "Work the tree in **rounds** over the **frontier** — every decision whose prerequisites are already settled." … "Ask the whole frontier in one numbered round. … Questions whose answers depend on another question still open in this round belong to a later round."

By the frontier definition, a question whose prerequisite is still open is not in the frontier — so the second sentence either restates the definition or implies the frontier can contain intra-round dependencies, contradicting "prerequisites are already settled." Fix: reword to make it a check, e.g. "(a question depending on another in the same round isn't frontier yet — push it to a later round)," or delete.

## skills/thinking/domain-modeling/reference/context-format.md

**14. Template mixes placeholder and filled example — Confusion (minor)**
> "**Order**:\n{A one or two sentence description of the term}\n_Avoid_: Purchase, transaction"

The `Order` entry has placeholder description text but concrete `_Avoid_` values, while `Invoice` and `Customer` are fully worked examples. Cold, it's ambiguous whether `_Avoid_: Purchase, transaction` is placeholder or content. Fix: make `Order` a fully worked example like the other two.

## Files that read clean

- `skills/thinking/domain-modeling/reference/adr-format.md` — self-contained; its one cross-reference ("The three gates for offering an ADR are in SKILL.md (§ ADRs — offer sparingly)") resolves exactly.
- `skills/thinking/interview-with-docs/SKILL.md` body paragraphs 1–2 (the composition statement itself is crisp; issues are confined to the exit and degrade clauses above).

One cross-cutting note rather than a finding: the frontmatter keys `metadata.invocation: model` and `metadata.execution: orchestrator` are terms of art defined nowhere in the reachable set. They are plausibly machine-read installer schema, so I flag them only as a documentation gap, not a defect in any one skill.

---
---

# Report 3 — probes (prototype, research, diagnosing-bugs)

Read as a consumer agent with no authoring context. "Resolves via sibling" was checked for `review-loop` and `staffing` (both exist); playbook pointers under `docs/agents/` all resolve in this repo.

## docs/agents/prototyping.md (reached via the prototype skill's playbook pointer) — most severe cluster

The pointer resolves, so that is not the flag; the *content* it resolves to contradicts the skill that points at it.

**1. Ungrounded / stale reference.**
> "The backlog `prototype` subskill reads this file for the technique; the gates are in the skill's `reference/prototype.md`."

- Cold-fail: `prototype` is a standalone skill (`skills/delivery/prototype/`), not a "backlog subskill" — no such subskill is established anywhere reachable. And `reference/prototype.md` does not exist; the file is `reference/prototyping.md`, and the gates actually live in `SKILL.md`, not the reference.
- Fix: reword the header to "> Project delta for the `prototype` skill. The installed skill owns the technique (`reference/prototyping.md`); keep only this repo's placement bindings here."

**2. Contradiction (with `skills/delivery/prototype/SKILL.md` line 17).**
- SKILL.md: "Use optional `docs/agents/prototyping.md` **only for repo-specific placement**."
- Playbook: "reads this file **for the technique**" — and it then ships the entire technique (shapes, rules, capture, cleanup).
- Cold-fail: two reachable files disagree about which one owns the method. A cold reader cannot tell whether the playbook's method text overrides the bundled reference.
- Fix: cut the playbook down to its "This repo" section (which is genuinely project-specific and good), matching what `research`'s and `diagnosing-bugs`'s playbooks already do.

**3. Redundancy with drifted wording (vs `reference/prototyping.md`).**
- Playbook: "**logic** shape ... **UI** shape"; reference: "**behavior shape** ... **form shape**". Also playbook: "Add **actions** on request" vs reference: "Add **cases** on request"; playbook: "screenshot each variant **via the driver in `environment.md`**" vs reference: "a screenshot of a UI".
- Cold-fail: same rules, two vocabularies; a cold reader following gate 1's "behavior/form shape" then reading the playbook meets a two-shape taxonomy under different names, with no mapping — and the playbook's copy lacks the falsification shape entirely.
- Fix: same as (2) — single-home the technique in `reference/prototyping.md`.

## skills/delivery/prototype/SKILL.md

**4. Contradiction — two shapes vs three.**
> Gate 1: "Record one question, the claim it can falsify, and **behavior/form shape**."

`reference/prototyping.md` defines a third: "An unfamiliar mechanism claim uses the **falsification shape**". The gate's enumeration excludes a shape the reference requires. Fix: reword gate 1 to "…and its shape (behavior, form, or falsification per the reference)."

**5. QUESTION — falsifiability required of every prototype?**
> Gate 1: "the claim it can falsify" and "Failure to expose a falsifiable observation returns to gate 1."

For a form-shape prototype ("which of three layouts?") there is no claim being falsified — the reference frames form work as reacting to alternatives, not testing a claim. Cold, I would not know what to record for gate 1 on a form prototype, or when gate 2's "falsifiable observation" is satisfied by a variant sheet. Clarifying this changes what the skill demands, so: question, not fix.

**6. Confusion — undefined role noun in dispatch syntax.**
> "dispatch build-out through `staffing route <prototype-builder task>`."

"prototype-builder" is not a role in the reachable `staffing` skill (its vocabulary is "mechanical/bulk", task pins, rankings). Cold, I can't tell whether `<prototype-builder task>` is a literal role name staffing knows or a placeholder for a task description. Fix: reword to "dispatch build-out via `staffing route`, describing the build task (see the reference's Staff-the-build section)."

**7. Confusion — capture target when standalone with no playbook.**
> Gate 3: "Write the decision … into **the caller's durable record**."

When run "directly on an explicit question" (no caller), the reference routes capture "into the issue or a commit message **the playbook names**" — but the playbook is optional and the skill ships no template/setup to create one, and no absent-playbook fallback is given for capture (placement gets one; capture doesn't). Cold and standalone-without-playbook, the capture destination is indeterminate. Fix: add a fallback in the reference's Capture section, e.g. "absent a playbook, capture in the commit message or a note beside the deleted artifact's former location."

**8. Redundancy/term drift — the sheet.**
- SKILL.md gate 2: "Serve rendered **answer sheets** through `review-loop`"
- reference § Present: "serve the rendered artifact / **variant sheet**"
- reference § Staff: "the **draft sheets**"

Three names, one artifact (review-loop's own reference also says "prototype's answer sheet"). Fix: pick one term ("answer sheet") and use it in all three places.

## skills/delivery/prototype/reference/prototyping.md

**9. Confusion — "end the pause" has no antecedent.**
> "serve the rendered artifact / variant sheet, and **end the pause** with its URL and the hub URL."

No pause is established anywhere in this file or SKILL.md; the pause is review-loop vocabulary (its `scripts.md` mentions a "pause message"). It resolves only if you go read review-loop's internals, which composition-by-name says you shouldn't need for this sentence. Fix: reword to "…and when review-loop pauses for the verdict, announce the artifact URL and the hub URL."

**10. Confusion — garbled parenthetical.**
> "Repo-specific placement (task runner, where throwaway artifacts live, **the component library variants must use**) lives in the project playbook"

Reads as a broken list item; means "the component library that variants must use". Fix: insert "that".

**11. Undefined term — "presentation surface" / "surface … recorded".**
> "its URL is still announced on the **presentation surface**" and "Where **no surface is recorded**, `review-loop` degrades to a local open"

"Presentation surface" is defined only inside review-loop's `reference/surface-and-hub.md`; "recorded" (where? by whom?) is never located. Passable via the sibling, but the second clause is load-bearing for degradation and cold-ambiguous. Fix: "Where the project playbooks record no presentation surface (see `review-loop`), it degrades to a local file open."

**12. Minor — "never improvise a public tunnel."** "Tunnel" is a term of art (tailnet/ngrok-style exposure) never established. Intent is guessable; fix by rewording to "never expose it on a public URL."

## skills/delivery/diagnosing-bugs/reference/diagnosis.md

**13. Redundancy/term drift — two names for an undefined record.**
> Phase 3: "Put the ranked list in the **durable work record**"
> Phase 6: "Record the confirmed hypothesis/root cause in the **durable change record**"

Neither term is defined in anything reachable from this skill (no playbook template field, no SKILL.md mention); a cold standalone invocation has no established record at all. Fix: pick one term, and define it once in SKILL.md's Contract (e.g. "the durable record: the caller's issue/PR when one exists, else the commit message or diagnosis note").

**14. Confusion — "the project's required checks" has no binding.**
> Phase 6: "Rerun the original loop and **the project's required checks**." / Done: "**required checks** have not regressed."

Neither `templates/diagnosing-bugs.md` nor the skill-authoring template has a field collecting required checks, and SKILL.md's contract item 4 says only "cleanup and **project-check results**" (a third phrasing). Cold, in a fresh repo after `setup`, I cannot learn what the required checks are. Fix: add a template line "- Required project checks before declaring done: _<verified commands, or "none">_" and align the two phrasings.

## skills/delivery/diagnosing-bugs/templates/skill-authoring/diagnosing-bugs.md

**15. Undefined terms — the probe-evals discipline is presupposed, not shipped.**
> "Regression seam: a failing **situated probe** or confirmed misbehaving transcript, run through both an **in-session executor** and an **independent CLI executor**" and "_<path to the changed skill's eval scenarios, **answer key**, and verified executor commands>_"

"Situated probe", "answer key", and the dual-executor scheme are defined only in this repo's `docs/agents/probe-evals.md` — a repo playbook, not part of the skill's install. This template ships to *any* skill-authoring repo, where none of these terms resolve. Fix: either define "situated probe" in one sentence inside the template ("a scenario prompt run against the installed skill, judged against a recorded expected outcome") or point at a bundled definition; don't rely on a consumer repo happening to have `probe-evals.md`.

## skills/thinking/research/reference/research-contract.md

**16. Ungrounded — foreign lifecycle vocabulary in a caller-neutral contract.**
> "Research does not become evidence because someone reviews it. `evidence/` is for criterion-linked proof of a separate completed change. When the research dossier itself is **the backlog deliverable**, commit it in `research/`; its citations and audit are intrinsic provenance, not a second **evidence package**."

"`evidence/`", "criterion-linked proof", "backlog deliverable", and "evidence package" belong to the `backlog` skill, which research neither requires nor names as a sibling. In a repo without backlog, this paragraph refers to a directory and a deliverable class that don't exist. (SKILL.md's Return has the same leak: "without … **copying the dossier into `evidence/`**".) Fix: generalize — "The dossier is its own provenance; do not copy it into a caller's proof/evidence area, and do not treat review of the dossier as converting it into proof of a change."

**17. Ungrounded — this repo's workspace convention in the shipped contract.**
> "If research directly supports authoring a local skill and the project routes development material through a **`<skill>-workspace/`**, follow its playbook and place the dossier under that workspace's `research/` directory."

`<skill>-workspace/` is this repo's private layout (defined in this repo's AGENTS.md, unreachable from an installed copy). It's conditionally phrased so it degrades, but it's the only sentence in the contract naming a specific foreign convention, and the template already has a generic slot ("Research supporting a local skill source: _<record the workspace path…>_"). Fix: delete the sentence; the playbook's "special workspace route" field already carries this.

**18. Minor undefined term — "execution slot".**
> "Reserve at least one **execution slot** for the coordinator/synthesizer."

Never defined; harness-dependent. Guessable (parallel-worker capacity), so minor. Fix: "reserve capacity for the coordinator: never spend every available parallel worker on shards."

## skills/thinking/research/SKILL.md

**19. Minor ungrounded — "the epistemic stage".**
> "Own **the epistemic stage**: source question → primary-source observations → traceable inferences."

"Stage" implies a pipeline established elsewhere (backlog's lifecycle); cold, there is no pipeline in view. The colon-expansion makes it survivable. Fix (optional): "Own the epistemics of a question: …"

**20. Minor confusion — "Standalone, open the canonical artifact."** Open with what, for a headless run? Research's playbook binds presentation in this repo, but absent a playbook the verb is indeterminate. Fix: "Standalone, present the dossier per the project playbook's presentation binding; absent one, return its path."

## Files that read clean

- `skills/delivery/diagnosing-bugs/SKILL.md` — tight; contract maps 1:1 onto the six phases; "red-capable" is used before definition but the reference grounds it immediately. (Only the "project-check results" phrasing drift, folded into finding 14.)
- `skills/delivery/diagnosing-bugs/reference/setup.md` — clean; the skill-authoring/plain template fork condition is explicit and checkable.
- `skills/delivery/diagnosing-bugs/templates/diagnosing-bugs.md` (plain variant) — clean placeholder seed (modulo the missing required-checks field, finding 14).
- `skills/thinking/research/reference/setup.md` — clean; completion criterion's fields match the template's sections exactly.
- `skills/thinking/research/templates/researching.md` — clean.
- `skills/thinking/research/reference/research-contract.md` is otherwise the best-written file in the set: every term of art (observation/fact/inference/unknown, claim packet, coordinator/worker/challenger) is defined before use.

## Cross-cutting note (not a source flag)

The installed copies diverge from the sources: `skills/prototype` etc. are symlinks to `.agents/skills/*`, and the installed `prototype` and `diagnosing-bugs` SKILL.md descriptions differ from source (installed prototype adds "layout," and "rather than argument"; installed diagnosing-bugs adds "broken … throwing" and "Diagnose hard bugs and performance regressions"). A consumer agent reads the installed copy, so whichever direction is current, the pair needs a reinstall/reconcile — per the repo's own rule that installed packages are build products.

---
---

# Report 4 — formation (to-spec, to-tickets, merge-changes)

Reading complete. All files under the three skills read, plus the pointers they name (`docs/agents/platform.md`, `docs/agents/backlog-policy.md`, `skills/system/review-loop/SKILL.md` + setup reference, `skills/thinking/interview/SKILL.md`). Findings below, grouped by file, most severe first.

## skills/delivery/to-tickets/reference/slicing.md

**1. Authoring-repo leakage — "this repo" has no referent for a consumer** — CONTRADICTION + UNGROUNDED

> "Where the playbook records the tracker's **native blocking relation** (this repo: GitHub `blocked_by`, written via the verified verbs in `docs/agents/platform.md`), write the native edge"

and in § Publish:

> "On this repo that binding is GitHub via `gh` (`gh issue create --title '...' --body '...'`), and a ticket is a GitHub issue."

A skill reference is shipped into arbitrary consumer repos; "this repo" resolves to nothing a cold reader can identify (the authoring repo's binding leaked into the shipped contract). Worse, the second quote directly contradicts the same file's § Vocabulary — "Never assume GitHub's 'issue' in the skill's own text; the pair is deliberately tracker-agnostic" — and to-tickets SKILL.md — "the skill's own text never assumes GitHub's vocabulary." Fix: delete both parentheticals/sentences; the concrete binding already lives in the consumer's `platform.md` (reword the first to "e.g. GitHub's native `blocked_by`").

**2. "the retired plan stage"** — UNGROUNDED

> "**A legacy plan document** — a per-ticket design doc from the retired plan stage."

No file in the skill's reach establishes what the plan stage was, that it was retired, or what a legacy plan document looks like (the only mention is this repo's own AGENTS.md, which an installed consumer never has). Fix: reword to "a standalone per-ticket design document ('plan'), if the project has one" — describes the input without the history.

**3. "carried from the plan/spec rule"** — UNGROUNDED + REDUNDANCY (drifted twin)

> "The single exception, carried from the plan/spec rule: a **prototype-validated snippet**…"

No "plan/spec rule" is reachable; and the near-verbatim twin paragraph in to-spec's synthesis.md says "carried over from the **plan/PRD** rule" — two names for a rule neither file establishes. Fix: delete the attribution clause in both files ("The single exception: a prototype-validated snippet…").

**4. "an older `.md` spec reads the same way"** — UNGROUNDED (minor)

> "(a self-contained HTML deliverable; an older `.md` spec reads the same way)"

"Older" references a format history never established. Fix: "a `.md` spec reads the same way".

**5. "the register"** — UNDEFINED TERM

> "**UX context, for UI surfaces** — the register, the key states (empty / loading / error / disabled / responsive)…"

"The register" is never defined in anything reachable — voice/tone register? A UI element? Fix: reword, e.g. "the voice and formality of user-facing text (the register)".

## skills/delivery/to-tickets/templates/tickets.md + reference/template-guide.md + SKILL.md — the dependency-edge form contradiction

**6. Marker form stated unconditionally, contradicting slicing's native-relation path** — CONTRADICTION

- tickets.md: "On publish these become `- [ ] depends on #N` lines in the recorded convention, in dependency order."
- template-guide.md: "On publish, local Tn labels become tracker ids and the edges become `- [ ] depends on #N` lines (the playbook's verbatim form)"
- template-guide.md: "**Depends on** — the blocking edges, copied verbatim from the repo's recorded dependency convention (default `- [ ] depends on #N`, per `backlog-policy.md` § Dependencies)."
- ticket.md: "(default below, per backlog-policy.md § Dependencies)" above a `- [ ] depends on #N` line.

But slicing.md § Order and wire says: "Where the playbook records the tracker's **native blocking relation** … write the native edge … Where it records a body-line marker (`- [ ] depends on #N`) or `deps:` frontmatter instead, copy the playbook's literal form." And the one reachable playbook (`docs/agents/backlog-policy.md` § Dependencies) records the **native** relation — so the "default" body-line claim is wrong for the very repo the reader can see, and tickets.md/template-guide assert the marker form unconditionally. A cold agent following the templates would emit body lines where the playbook demands native `blocked_by`. Fix: single-home the rule in slicing § Order and wire; templates and guide say only "each edge is written in the playbook's recorded convention (native relation or marker line)" with no default.

**7. Readback assumes markers** — CONTRADICTION (same cluster), SKILL.md step 6

> "every emitted `depends on #N` marker points at a real, earlier ticket id"

If the recorded convention is a native relation there are no `depends on #N` markers, and the readback as written verifies nothing. Fix: "every emitted dependency edge — native relation or marker — resolves to a real, earlier ticket id."

## skills/delivery/to-tickets/SKILL.md (further)

**8. "(from the retired plan stage)"** — UNGROUNDED — same as finding 2; appears again here: "can also take a **legacy plan document** (from the retired plan stage)". Same fix.

**9. Step numbering "3b."** — CONFUSION (minor)

> "3b. **Audit each ticket for readiness**…"

A "3b" with no "3a", visually inside item 3 but sequenced before 4 — a cold reader can't tell if the audit happens during the quiz or after approval (slicing § Audit says "Before publishing", i.e. after approval). Fix: make it step 4 ("Audit each approved ticket") and renumber.

**10. No absent-binding degradation** — CONFUSION / QUESTION

Step 5 and slicing § Publish require "the tracker binding recorded in `docs/agents/platform.md`" but neither says what to do when no `platform.md` exists — unlike merge-changes, which has an explicit "state the gap and stop", and unlike the repo convention that "absent a sibling, a skill states the requirement rather than failing silently." QUESTION: should to-tickets stop, or fall back to leaving `tickets.md` as the deliverable? Either way, one sentence is needed.

## skills/delivery/merge-changes/SKILL.md

**11. The reachable platform binding forbids the skill's core act** — CONTRADICTION / QUESTION

> "Platform verbs (merge, checks-read, PR-read, branch ops) come from the project's `docs/agents/platform.md` when present"

but `docs/agents/platform.md` § Change review records:

> "Merge: the human merges on GitHub — the loop never merges."

The pointed-at playbook records no merge verb and explicitly reserves merging for the human. A cold reader invoked as merge-changes in this repo cannot tell whether the user's request overrides "the loop never merges" (merge-changes arguably isn't "the loop") or whether the binding blocks the skill entirely. QUESTION: either `platform.md` should record merge mechanics for this gate, or merge-changes should say what to do when the binding reserves merge for the human.

**12. `ready-for-agent` listed as a merge prerequisite** — CONFUSION

> "Automated review approval, green checks, `ready-for-agent`, or a reviewer's `LGTM` are prerequisites where configured — **they are never authorization to merge**."

Per the reachable `backlog-policy.md`, `ready-for-agent` means "groomed and released: the agent may work it" — a pre-work pickup label, not a merge-readiness signal; a PR-stage reader can't act on it. Fix: drop it from the list, or generalize to "readiness labels".

**13. "keep-both provenance"** — UNDEFINED TERM (minor)

> "resolve conflicts only when the intended resolution is mechanical and unambiguous (keep-both provenance, regenerated artifacts, lockfile refresh + the project's install command)"

"Keep-both provenance" is opaque — presumably conflicts where both sides are retained (e.g. append-only lists), but a cold reader is guessing. Fix: "conflicts where both sides are simply kept (append-only additions)".

## skills/delivery/to-spec/reference/synthesis.md

**14. "carried over from the plan/PRD rule"** — UNGROUNDED — twin of finding 3.

> "The single exception, carried over from the plan/PRD rule: a **prototype-validated snippet**…"

No plan/PRD rule is reachable; drifted twin of slicing's "plan/spec rule". Fix: delete the clause.

**15. Lifecycle justification with no reachable lifecycle** — UNGROUNDED

> "The spec's approval is the **direction's gate** — the lifecycle has no separate plan stage; per-ticket tactics are made just-in-time inside execution."

"The lifecycle" is never described in the skill's files; this explains why the text is right rather than what to do. Fix: reword to instruction — "Spec approval is the only direction-level gate; do not wait for any further plan approval."

**16. "maps straight onto the Notes rule below" — but the definitions aren't below** — CONFUSION

> "the exit classification (settled / delegated / deferred / blocking) … the classification maps straight onto the Notes rule below."

Nothing below in synthesis.md defines blocking/delegated/deferred; the definitions live only in SKILL.md step 5 ("**blocking** (must be settled upstream before tickets), **delegated** (the executor may choose; boundary named), or **deferred** (parked, with a home)"). A reader deep in the reference has a dangling pointer. Fix: single-home the three definitions in synthesis § Sign-off and let SKILL.md step 5 summarize.

**17. "presentation-surface config"** — UNDEFINED TERM (shared with SKILL.md)

> "approved from the human's own device per the repo's presentation-surface config."

and to-spec SKILL.md § Project playbooks: "the repo's **presentation-surface config** (its `docs/agents/` surface playbook)". Nothing reachable is named that — the review-loop sibling calls it "the project's presentation section" under `docs/agents/` (review-loop SKILL.md: "**Project:** the presentation section under `docs/agents/`."), and no `docs/agents/` file here is a "surface playbook". Fix: adopt review-loop's term in both places — "the project's presentation section under `docs/agents/` (owned by review-loop's setup)".

**18. "the project instruction file"** — CONFUSION (minor)

> "The first spec also registers the specs location in the project instruction file's `## Context documents` index"

Which file? Repos commonly have both `AGENTS.md` and `CLAUDE.md`; the skill never says. Fix: "the project's agent instruction file (`AGENTS.md`, or `CLAUDE.md` where that is the only one)".

**19. Fidelity-audit gate stated twice with drift** — REDUNDANCY

- SKILL.md step 5: "A spec with an **unclassified material Note, or an open blocking Note**, must not feed `to-tickets`."
- synthesis.md § Sign-off: "An open **blocking** Note stops the hand-off to `to-tickets`" — the unclassified-Note condition is missing.

The method file (the stated authority) has the weaker gate. Fix: single-home the full condition in synthesis § Sign-off; SKILL.md points at it.

## skills/delivery/to-spec/SKILL.md (further)

**20. "same house style as a plan"** — UNGROUNDED

> "a self-contained HTML deliverable with stable element ids, same house style as a plan."

No plan artifact or skeleton is established anywhere in to-spec's files; the actual plan skeleton lives in the review-loop sibling (`skills/system/review-loop/templates/plan-skeleton.html`), unnamed here. Fix: either drop the comparison or point at it: "same house style as review-loop's `templates/plan-skeleton.html`".

**21. Tracking-ticket projection stated unconditionally** — REDUNDANCY (drift, minor)

Step 6: "On approval: commit and project the thin tracking ticket" — but synthesis § Sign-off conditions it: "when a live tracker is bound (`docs/agents/platform.md`) — create a **thin tracking ticket**". Fix: add "(when a tracker is bound)" to the SKILL.md summary.

## skills/delivery/to-spec/reference/template-guide.md

**22. "the retired per-ticket plan stage"** — UNGROUNDED

> "a spec is coarser than a plan (the retired per-ticket plan stage)"

Same dangling history as findings 2/8; also duplicated with drift in to-tickets' template-guide ("coarser than a plan (the retired per-ticket plan stage)"). Fix in both: "coarser than a per-ticket implementation plan".

## skills/delivery/to-spec/templates/spec-skeleton.html

**23. "the plan skeleton" / "the review surface"** — UNGROUNDED (minor, comment only)

> "Same house style as the plan skeleton, so specs and plans present identically on the review surface."

Neither artifact is locatable from this skill's files (both are review-loop concepts). Fix: "same house style as review-loop's plan-skeleton.html, so both present identically on its review surface."

## skills/delivery/merge-changes/agents/openai.yaml vs the other two

**24. Two manifest schemas** — CONTRADICTION (format drift)

to-spec and to-tickets nest the flag: `policy:\n  allow_implicit_invocation: false`; merge-changes has bare top-level `allow_implicit_invocation: false`. One shape is presumably invalid for Codex; a cold reader authoring the next skill can't tell which. Fix: align merge-changes to the `policy:` nesting (the majority form) — QUESTION only if the bare form is the correct one.

## Read clean

- `skills/delivery/to-tickets/templates/ticket.md` — clean except its share of the "default `- [ ] depends on #N`" cluster (finding 6); one nit: work-type exists only as a trailing HTML comment, with no field or placement guidance (label vs body line) — minor.
- `skills/delivery/to-tickets/templates/tickets.md` — clean apart from finding 6.
- `skills/delivery/to-spec/templates/spec-skeleton.html` — clean apart from finding 23; ids, styling, and section comments all match the template guide.
- Pointers that resolved and are **not** flags: `backlog-policy.md` § Dependencies and § Readiness decision (exist, answer the questions asked of them); `platform.md` tracker verbs; the interview skill's exit classification "*settled*, *delegated* … *deferred* … *blocking*" (defined at `skills/thinking/interview/SKILL.md`); "thin tracking ticket" (defined in synthesis § Sign-off); "tracer bullet" and "wide refactor" (defined where used); review-loop as the AFK sign-off sibling.

The dominant patterns: (a) the to-tickets edge-convention text disagrees with itself between method and templates (findings 6–7 — the one cluster that would change published output); (b) authoring-repo facts leaked into shipped reference text ("this repo", findings 1); (c) a family of dangling history references to a "retired plan stage" and a "plan/PRD|plan/spec rule" that no reachable file establishes (findings 2, 3, 8, 14, 20, 22); (d) merge-changes' one reachable playbook denying it a merge verb (finding 11).

---
---

# Report 5 — services + UX (review-loop, staffing, setup-asher-skills, bare-minimum-ux)

Below are my cold-reading findings. I read every SKILL.md, reference, and template in the four skills, plus the reachable pointers (`docs/agents/environment.md` exists with § Presenting to the human; all catalog skill names resolve under `skills/`; both `render-global.py` headers checked). Grouped by file, most severe first.

## 1. `skills/system/staffing/variants/claude/templates/global/staffing.module.md` (and the codex twin)

**1a. QUESTION — Contradiction: the shipped module templates ARE a fixed roster, which the skill's own doctrine forbids.**
`reference/machine-audit.md` opens: "The roster is **compiled from the current machine, never shipped fixed.**" and "Seed only rows for models the audit found reachable; drop any example row whose model this machine can't reach". But `variants/claude/templates/global/staffing.module.md` ships a concrete roster ("| gpt-5.6-sol | 4 | 9 | 5 |… | fable-5 | 1 | 9 | 9 |", "Coordinator-eligible: fable-5, opus-4.8, sonnet-5…"), and `reference/setup.md` step 3 says to install it byte-authoritatively: "Use `scripts/render-global.py render`/`check` for byte-authoritative previews, then `stage` each consented provider module and `apply`". The script (`payloads()`) renders the template verbatim except `{{COMMON}}`. A cold reader cannot tell whether to (a) apply the template's fixed Asher-machine roster verbatim (what setup.md + the script say) or (b) rewrite it from the audit (what machine-audit.md says) — and rewriting would fail the byte `check`. This is the load-bearing ambiguity of the whole skill. Fix requires deciding which is true, so: QUESTION.

**1b. Ungrounded — private history in a shipped template.**
- "Current machine policy (Asher, plan #73): **yolo both ways for now**, matching how the orchestrators themselves run." (both variants) — plan #73 is never established anywhere reachable; a consumer machine has no plan #73. Propose: delete the citation, keep the policy line, or move machine policy out of the shipped template.
- "(observed 2026-07-17: a wrapper silently resumed a sibling's session and wrote the wrong report with a clean success marker)" (claude variant) — incident history with no referent. Propose: reword to the rule only: "resume by id, never `resume --last`; parallel wrappers collide on `--last`."
- "Floor: sonnet-5 Claude-side / gpt-5.6-terra Codex-side; never Haiku." — "never Haiku" bans a model that appears in no roster row and is never introduced. Propose: delete "never Haiku" or add Haiku as a row with its exclusion reason.

**1c. Contradiction — the template's dispatch command disagrees with the same variant's `reference/harness.md`.**
- `variants/claude/reference/harness.md`: "it runs `codex exec` read-only for investigation or workspace-write for edits" vs. `variants/claude/templates/global/staffing.module.md`: "`codex exec --cd <worktree> --sandbox danger-full-access '<self-contained prompt>' </dev/null`". Read-only/workspace-write vs. danger-full-access are incompatible envelopes for the same dispatch.
- `variants/codex/reference/harness.md`: "`claude -p --model <verified-alias> '<self-contained prompt>' </dev/null`" vs. `variants/codex/templates/global/staffing.module.md`: "`claude -p --model <verified-alias> --dangerously-skip-permissions '<self-contained prompt>' </dev/null`". Same command, one adds a permission-bypass flag. Propose: single-home the command in `harness.md` and have the module reference it — or state explicitly that the module's yolo policy overrides harness.md's envelope.

**1d. Contradiction (cross-skill) — no "Wake paths" table where review-loop expects one.**
`review-loop/reference/watch.md`: "the machine staffing module publishes a **Wake paths** table — per harness, the cheapest wake mechanism the audit verified, and the fallback. Pick the top verified row". `machine-audit.md` step 7 also mandates writing it. But neither shipped `staffing.module.md` template contains a Wake paths table — the claude one has only prose ("Tracked background tasks, subagent completions, and Monitor conditions re-invoke the session"). A cold review-loop consumer told to "read the Floor value the roster publishes" and "pick the top verified row" finds no table. Propose: add the Wake-paths table to both module templates (shape from machine-audit's example).

**1e. Undefined terms.**
- "staffed by the cheapest Claude model allowed by the floor—`sonnet-low` on this roster" — `sonnet-low` is not a roster row; presumably sonnet-5 at low effort, but that's inference. Propose: "sonnet-5 at low effort".
- "a Claude-led run satisfies the liveness contract's 'verified wake path' natively" — "the liveness contract" is never defined in anything staffing ships (it appears to be a backlog concept). Propose: delete "the liveness contract's" or name the owning playbook.
- Codex variant: "`chrome:control-chrome`", "`computer-use:computer-use`" — provider identifiers used nowhere else and never explained (plugin? tool name? label convention?). Propose: one parenthetical each naming what kind of identifier this is.

## 2. `skills/system/staffing/reference/install-and-reconcile.md`

**2a. Contradiction + Confusion — "Setup" is an undeclared external owner in a skill that declares no siblings.**
§ Module-first owner reconciliation: "Setup starts a fresh barrier, then both owners atomically stage and read back all four Codex/Claude modules. … Setup preflights both globals and applies both Presentation sections; staffing refuses to apply until those match…". Two problems cold: (1) staffing has its own `reference/setup.md`, so "Setup" naturally reads as *staffing's* setup — but this "Setup" owns Presentation policy, which is `setup-asher-skills`. The antecedent is never disambiguated. (2) `staffing/SKILL.md` says "**Siblings:** none; staffing is a model-invoked root primitive and imports no skill files" — yet this procedure cannot run without setup-asher-skills driving the barrier. Propose: name the owner ("the `setup-asher-skills` installer") on first use, and either declare it an optional sibling or state the degraded path when it is absent (can staffing reconcile its module alone?). If the latter changes behavior: QUESTION.

**2b. Undefined term — "all four Codex/Claude modules."**
Nothing in staffing's reachable files enumerates the four (Presentation×2 + Staffing×2 — that enumeration lives in `setup-asher-skills/reference/interview.md` Phase 4 step 6, which staffing never points at; only the script source's `REQUIRED_BARRIER` set reveals it). Propose: one sentence: "the four modules are the Presentation and Staffing modules for each of Claude Code and Codex."

**2c. Redundancy (cross-skill, drifted wording) — the barrier procedure is specified twice.**
Here: "No pointer applies until all four verify. … Setup verifies all four final sections and removes the barrier. Never use an eager import." And `setup-asher-skills/reference/interview.md` Phase 4 step 6: "Apply no pointer until the barrier verifies all four current module paths and hashes; any staging failure leaves both global files byte-for-byte untouched. … Finally setup runs `finalize`, verifies all four final pointer sections, and removes the transaction barrier. Never use an eager import." Same protocol, two homes, different vocabulary (`verify` vs `paths and hashes`; no `begin/stage/preflight/finalize` verbs on the staffing side). Propose: single-home the protocol in one file (interview.md step 6 is the fuller one) and have the other say "per the installer's barrier protocol" in one line.

## 3. `skills/system/review-loop/reference/review-loop.md`

**3a. Contradiction — the canonical state dir vs. the bundled example.**
"Durable state lives in **one canonical place per review**: `~/.backlog/reviews/<repo>/<scope>/state` (never a session scratchpad, never an ad-hoc `review-state/` sibling)." But `reference/scripts.md` documents `--state` default `state` and its Typical invocation uses "`--state ./run/state`" — exactly the ad-hoc sibling the rule bans. A cold reader following scripts.md verbatim violates review-loop.md. Propose: make the example use the canonical path, or scope the canonical-place rule ("when no owning workflow supplies a state dir…").

**3b. Ungrounded — backlog coupling in a skill whose only declared sibling is optional `staffing`.**
"`~/.backlog/reviews/…`" and "When the owning workflow keeps a durable run root (backlog's `<git-common-dir>/backlog/runs/<run-id>/`), copy `events.jsonl` and `ledger.json` into it before `--stop`", and "an audited backlog resume". SKILL.md declares "**Sibling:** optional `staffing`" only; a consumer who installed review-loop via `prototype` or `to-spec` has no backlog and cannot ground `<scope>`, `~/.backlog/`, or "run root". Propose: reword generically ("the owning workflow's durable run root, when it keeps one") and let backlog's own docs name its paths; `<scope>` needs a definition wherever the path stays.

**3c. Confusion — "These checks are the guard."**
"Audit heuristics for a suspect approval: a verdict seconds after server start, a loopback/CLI client where a human browser is expected, or an approval on a route that was never published are grounds to void and re-present. These checks are the guard." "The guard" (definite article) against what, run by whom, when? No trigger, no owner, no procedure is established. Propose: reword: "Whoever consumes an approval applies these heuristics before trusting it; a hit voids the approval and the artifact is re-presented."

**3d. Ungrounded — negation of an unestablished mechanism.**
"Reconciliation is LLM audit over this event log and the ledger; there are no version stamps." Nothing in review-loop introduces "reconciliation" or version stamps (the no-version-stamp posture lives in setup-asher-skills/staffing, unreachable from here). Propose: delete the sentence or expand: "A later audit of the review reads `events.jsonl` and `ledger.json`; the skill writes no separate version marker to compare."

## 4. `skills/system/setup-asher-skills/templates/global/presentation.common.md`

**4a. QUESTION — a "common" template shipped to any consumer hardcodes one person's machine.**
"When Asher is at this machine, open the local file." / "This machine's tailnet root is `https://ashers-macbook-pro.tail045dd5.ts.net`; Funnel stays off." `interview.md` Phase 4 step 6 offers this module verbatim ("the deferred module from `templates/global/presentation.common.md`", staged byte-atomically) to "each confirmed harness" on whatever machine setup runs on. On any machine but Asher's MacBook the installed global policy names the wrong human and a wrong hostname. Same tension as finding 1a. Fix (placeholders filled at install, or an explicit "personal template — rewrite the host line at install" instruction) changes behavior: QUESTION.

**4b. Redundancy (drifted) — tailnet bring-up rules duplicated against review-loop.**
This template: "Before publishing, run `tailscale status`. Run `tailscale up` only when the node is down and something is being published now. Never cycle a healthy connection. If authentication or startup fails, report it and open locally; never enable Funnel or improvise a public tunnel." `review-loop/reference/surface-and-hub.md` § Bringing the tailnet up: "Run `tailscale up` only when all three hold: (a) the surface is a tailnet, (b) a review is actually being published right now, and (c) the check shows the node down or logged out. … never `tailscale down` then `up` as a 'reset.' … fall back to the local-only review". Two owners (setup's global module vs review-loop's bundled reference) will drift — the template already lacks condition (a). Propose: single-home the rule in surface-and-hub.md; the global module keeps only the machine facts (hostname, serve/teardown commands) and points at the skill for procedure.

## 5. `skills/system/review-loop/reference/watch.md`

**5a. Ungrounded — appeal to unshown history.**
"Parking the orchestrator on that wait has two failure modes, both observed in practice:" — "observed in practice" cites nothing reachable; it justifies rather than instructs. Propose: delete the clause ("…has two failure modes:").

**5b. Undefined term — "the platform binding."**
"**The PR-merge watch** — the watcher holds the merge poll (the `ScheduleWakeup` / `Monitor` loop named in the platform binding) and wakes the parent when the PR merges." Neither "platform binding" nor `ScheduleWakeup` is defined in anything review-loop ships or declares (it's a backlog/`docs/agents/platform.md` concept; review-loop's declared project surface is only "the presentation section under `docs/agents/`"). Propose: "the merge poll named in the owning workflow's platform playbook, where one exists."

**5c. Confusion — PR-merge scope vs. SKILL.md scope.**
SKILL.md scopes the skill: "Owns rendered-HTML sign-off … It never authors the artifact." watch.md § Both gates extends the contract to "The PR-merge watch", which involves no rendered HTML, no verdict codes, no `review-await.py`. A cold reader can't tell whether review-loop owns merge watches or is merely being cited as a pattern. Propose: one sentence in watch.md: "The merge watch belongs to the owning workflow; it reuses this watch *shape*, not these scripts." (If review-loop genuinely owns it: QUESTION.)

## 6. `skills/system/staffing/reference/rankings-and-routing.md`

**6a. Ungrounded/undefined — "Terra" in the machine-generic contract.**
"For example, ChatGPT-in-Chrome and Computer Use are Codex harness/tool providers, not Terra capabilities". "Terra" is never introduced in this file; it's a model nickname from the *illustrative* audit example in machine-audit.md. In the normative contract it reads as an unknown proper noun. Propose: "…not capabilities of any model" (the sentence's actual point).

**6b. Confusion — "on this machine" inside a shipped generic reference.**
"Resolve `browser-use` to its named primary provider — on this machine an isolated-profile `agent-browser`, never the user's own browser session. … the only recorded fallback is the user-session carve-out". machine-audit.md insists the roster is "compiled from the current machine, never shipped fixed", yet this section states one machine's providers as fact with no "example" framing until you notice the heading "### Browser example". Which machine is "this machine" for a consumer? Propose: open the section with "Illustration from one machine's roster:" and swap "on this machine" → "on the example machine".

## 7. `skills/system/setup-asher-skills/reference/interview.md`

**7a. Undefined term — the legacy `## Conventions` migration is unactionable.**
Phase 4 step 6: "A legacy `## Conventions` block is replaced only when its seeded setup-asher-skills marker is present; an unowned block stops for review. The migration also replaces setup's legacy seeded header with the compact native header." (Phase 1 similarly: "setup's legacy seeded `## Conventions` block".) Nothing reachable says what the "seeded setup-asher-skills marker" looks like, what the "legacy seeded header" was, or which text is "the compact native header" (the templates ship only `# Global CLAUDE.md` / `# Global AGENTS.md`). A cold reader cannot execute the gate that decides whether replacing a user's block is allowed. Propose: quote the marker string and the legacy header verbatim in this step, or delete the migration path if the legacy form no longer exists in the wild (QUESTION if the latter).

**7b. Redundancy — barrier protocol duplicated with staffing** (see 2c; drifted wording quoted there).

**7c. Redundancy (minor, consistent) — the self-host detection is defined in two places.**
`audit-mode.md` step 1: "This is the single shared **repo is the source** detection consumed by both the READ path here … and the WRITE path in [interview](interview.md) Phase 4 … so the two cannot diverge." Yet interview.md Phase 4 step 1 restates the criteria inline: "(the repo's git remote is `asasher/asher-skills`, or a local `skills/` dir holds these skills)". The restatement is what lets them diverge. Propose: drop the inline parenthetical, keep the pointer.

## 8. `skills/system/setup-asher-skills/SKILL.md`

**Undefined term — "internal holds."**
"The read-only compiler validates public identities, invocation/execution policy, sibling closure, external declarations, internal holds, setup pointers, provider overlays, and dependency order". No reachable file defines a "hold"; the nearest concept is catalog.md's "Internal roots are cataloged for audit but cannot be selected or required by a public skill" — different noun, and a reader can't confirm they're the same thing. Propose: "internal-root exclusions (internal roots cannot be selected or required)".

## 9. `skills/creative/bare-minimum-ux/SKILL.md`

**9a. Undefined term — "`## Context documents` index."**
"register both files in the project instruction file's `## Context documents` index when it does." No reachable file (including the `agent-skills-block.md` template that defines what setup writes into instruction files) establishes a `## Context documents` section or its format. Propose: either define the one-line format here or reword: "list both files in the project instruction file so sessions load them."

**9b. Confusion — "shaping (the interview)" with no declared sibling.**
"A rule's non-obvious case … is settled with the user during shaping (the interview), never invented during implementation." The skill declares `requires: []`, `optional: []`, and catalog.md says single-purpose skills "carry no sibling closure" — so "the interview" resolves to nothing for a consumer without the `interview` skill. Propose: "…settled with the user before implementation — during shaping where the project runs an interview/spec stage, otherwise by asking directly."

**9c. QUESTION — `"version":"latest"` vs. the catalog's version semantics.**
This skill declares `"version":"latest"` for `impeccable`, but catalog.md says "`version` is optional" and interview.md Phase 4 step 2 branches on "resolve the declared `version` when present (otherwise disclose that it is unpinned)". "latest" is present-but-unresolvable: the installer would try to resolve a tag named `latest` rather than disclosing unpinned. Whether to omit the field or teach the installer "latest" changes install behavior: QUESTION.

## 10. `skills/system/setup-asher-skills/reference/catalog.md`

**Ungrounded — retired-stage history in the recommendation table.**
"`interview-with-docs` → `to-spec` (review-loop for the gate) | Elicit and crystallise the decisions, then write the spec; the spec's review gate replaced the retired plan stage". "The retired plan stage" is never established in anything this skill ships — it's repo history. A cold installer gains nothing and may hunt for a `plan` skill that doesn't exist. Propose: delete "; the spec's review gate replaced the retired plan stage".

## 11. `skills/system/setup-asher-skills/templates/agent-skills-block.md`

**Ungrounded — negation of a never-established referent.**
"It is a map, not a router: there is no `ask-asher` dispatcher skill." `ask-asher` appears nowhere else in anything reachable; the denial only makes sense to someone who remembers a design that was rejected. Propose: "It is a map, not a router: skills are invoked by their own names."

## 12. `skills/system/review-loop/SKILL.md` + `reference/surface-and-hub.md` + `reference/setup.md`

**12a. Contradiction (mild) — is the playbook name fixed or repo-variable?**
`reference/setup.md`: "Reconcile only `docs/agents/environment.md` § **Presenting to the human**." (fixed filename). `surface-and-hub.md`: "lives in a `docs/agents/` surface-config playbook (on this repo, `environment.md` § Presenting to the human)" (variable, with an ambiguous "this repo" — in an installed copy, does "this repo" mean asher-skills or the consumer repo?). SKILL.md says only "**Project:** the presentation section under `docs/agents/`." Three generality levels for one pointer. Propose: pick one: "the project's surface-config playbook — by convention `docs/agents/environment.md` § Presenting to the human" — and use it in all three files; drop "on this repo".

**12b. Redundancy (drifted) — the wake-path summary in SKILL.md restates watch.md.**
SKILL.md: "a tracked background await where the harness wakes on completion, else a pure wait-and-relay watcher at the roster's published Floor — it only runs the await script and relays the verdict and comments, no synthesis." watch.md roster: three rungs (tracked wake / Floor-staffed watcher / degrade). The SKILL.md inline shows two rungs with the degrade rule in a separate paragraph ("Missing staffing runs the watcher on the current model…"), so the two summaries can drift. Low severity — the pointer is present. Propose: trim SKILL.md to "Hold the wait on the harness's cheapest verified wake path per [watch] § The wake-path roster" and let watch.md own the rungs.

## 13. `skills/system/staffing/reference/machine-audit.md`

**Confusion (minor) — "it ships no scripts."**
"This is an agent-driven procedure; **it ships no scripts.**" The skill's own `scripts/render-global.py` sits one directory over; the antecedent "it" (the audit, not the skill) is easy to misread as a claim about the skill. Propose: "the audit is performed by the agent directly; no audit script is bundled."

## 14. `skills/system/setup-asher-skills/reference/audit-mode.md`

**Ungrounded (light) — "This is the shared posture across this repo's operator skills."** "Operator skills" is a category never defined anywhere reachable, and the sentence justifies rather than instructs. Propose: delete the sentence; the rule stands alone.

## Files that read clean

- `skills/system/review-loop/templates/plan-skeleton.html` — exemplary cold artifact: self-describing header, explicitly framed as one example, id contract restated locally and consistently with `review-loop.md`.
- `skills/system/review-loop/reference/scripts.md` — internally clean and precise (its only defect is being the other half of contradiction 3a).
- `skills/system/review-loop/reference/setup.md` — clean, crisp completion criterion.
- `skills/creative/bare-minimum-ux/references/notifications.md` — fully self-contained; every rule actionable cold.
- `skills/system/staffing/SKILL.md`, `reference/roles-and-fallback.md`, `reference/harness.md` (placeholder — the fail-safe wording is exactly right), `templates/global/staffing.common.md`, both `staffing-pointer.md`, `provider.txt`, `global-header.txt`.
- `skills/system/setup-asher-skills/templates/repo-pointer.md` and both `presentation-pointer.*.md` — self-contained and consistent with each other.

**Overall pattern worth relaying:** the recurring severe fault is one design tension appearing in three places — the skills preach "compiled from the machine / no shipped fixed values" (machine-audit.md, audit-mode.md) while shipping byte-authoritative templates full of one specific machine's values and private history (staffing modules, presentation.common.md). Every finding marked QUESTION traces to that tension; the rest are local deletions/rewords.
