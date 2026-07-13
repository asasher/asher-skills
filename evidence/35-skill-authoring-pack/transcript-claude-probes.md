# Claude executor transcript — issue #35

> Provenance: raw cited executor output copied without re-running or re-grading. P1/P2 are copied verbatim from Claude subagent agent-a660a3447973e8c10 at commit 6a0bdacb1234e877148e47299e8818ad7c750370. P3 is copied verbatim from the converged Claude subagent agent-a55efa89e8d6d4096 at reviewed commit 001376238342bbf4559acea0cef4c4404b08a869; it supersedes the earlier P3 record after the verification-record handoff fixes.

**P1 — Fresh registration and install**

**The domain question.** This is a fresh install (no `docs/agents/` playbooks), so setup must ask before scaffolding. `setup.md` step 2: "Fresh install: **before scaffolding anything**, ask the user 'what kind of work does this repo track?' with exactly six options: `software` / `skill-authoring` / `writing` / `research` / `ops` / `general`." So I offer exactly those six choices.

**The proposed default.** The repo has `skills/formatter/SKILL.md` and `skills/linter/SKILL.md` and no app stack, source tree, or test runner. `setup.md` step 2: "Default the answer from repo evidence and confirm rather than interrogate … a skill-authoring repo (`SKILL.md` files under `skills/<name>/`) defaults to `skill-authoring`; a code repo (`package.json`, `src/`, a test runner) defaults to `software`; a manuscript defaults to `writing`; ambiguous evidence defaults to `software`." The evidence here is not ambiguous — SKILL.md files under `skills/<name>/` with no code-repo markers — so I propose **`skill-authoring`** and ask the user to confirm.

**Resolution after confirmation.** `setup.md` step 2: "first overlay `templates/common/` with `templates/<domain>/`, with a same-name pack file shadowing common; then add the same-name `templates/software/` baseline as a flagged stand-in for every required step playbook absent from that overlay. The required step names are `implementing`, `verifying`, `evidence`, `diagnosing-bugs`, `refactoring`, `change-reviewer`, and `change-fixer`." Applying that to the given template listing:

Eleven files resolve into `docs/agents/` — per `setup.md` step 2's completion criterion: "For `skill-authoring`, require all eleven counterparts: three unshadowed common files, four native pack files, and four flagged software stand-ins."

- **Three unshadowed common files (native from `templates/common/`):** `backlog-policy.md`, `change-description.md`, `platform.md`.
- **Four native pack files (from `templates/skill-authoring/`):** `environment.md` (shadowing `common/environment.md`), `diagnosing-bugs.md`, `evidence.md`, `verifying.md`. Deciding sentence, `setup.md` step 2: "For `skill-authoring`, its pack `environment.md` shadows common and only `implementing.md`, `refactoring.md`, `change-reviewer.md`, and `change-fixer.md` come from software as flagged stand-ins." So `common/environment.md` does **not** install — the pack file wins.
- **Four flagged stand-ins (from `templates/software/`):** `implementing.md`, `refactoring.md`, `change-reviewer.md`, `change-fixer.md` — the required steps the skill-authoring pack omits.

**Flagged / reported / recorded:**
- Flagged: each stand-in gets a header flag — `setup.md` step 2: "Add one flag line to every installed stand-in's header naming it a code-flavored baseline to tailor for `<domain>`, and name every gap in the setup report. Never leave a required playbook uninstalled." (Mirrored in `templates/common/backlog-policy.md` § Work domain: "those step playbooks are `software` baselines standing in, each flagged in its own header as a code-flavored stand-in to tailor.")
- Reported: the four gaps are named in the setup report — same sentence ("name every gap in the setup report"), plus the step-2 completion criterion: "every change, degraded stand-in, and flagged conflict is reported."
- Recorded: the domain — `setup.md` step 2: "Record the answer in the installed `backlog-policy.md` § Work domain."

(Note: since this is fresh scaffolding, reconciliation is skipped — `setup.md` step 1: "No playbooks → fresh install: scaffold in step 2 and skip reconciliation." Later steps also record seed as the checked-in probes without inventing a stack — step 5: "For `skill-authoring`, record the checked-in probe scenarios as seed state and do not invent an app or stack.")

**P2 — Re-run, shadow, and partial resolution**

**Domain stands.** `setup.md` step 2: "Re-run: the recorded domain stands. … Changing an installed repo's domain is a user decision, never a silent reconciliation outcome." Domain remains `skill-authoring`.

**Environment baseline.** The pack file wins over common. `setup.md` step 2: "For `skill-authoring`, its pack `environment.md` shadows common" (general rule, step 2: "with a same-name pack file shadowing common"). So `templates/skill-authoring/environment.md` is the baseline the installed `environment.md` reconciles against; `templates/common/environment.md` plays no role.

**Native skill-authoring files.** The four pack files: `environment.md`, `diagnosing-bugs.md`, `evidence.md`, `verifying.md` — per the same step-2 sentence, only the other four come from software.

**Missing files reconciled from software.** The four absent counterparts are exactly the four required steps the pack omits: `implementing.md`, `refactoring.md`, `change-reviewer.md`, `change-fixer.md`. `setup.md` step 2: "Missing → write it from the resolved scaffold set, including any required flagged stand-in" — each written from its `templates/software/` baseline with the stand-in flag line ("Add one flag line to every installed stand-in's header naming it a code-flavored baseline to tailor for `<domain>`"). One procedural caveat before declaring them absent: `setup.md` step 1 requires "**Match installed playbooks to templates by content, not filename alone** — a template the skill has since renamed (e.g. `pr-reviewer.md` → `change-reviewer.md`) reconciles as a rename of the installed file, carrying every repo-tuned line over verbatim." So setup must first confirm no installed file is a renamed counterpart of, say, `change-reviewer.md`; the probe stipulates true absence, so stand-ins are written.

**What setup must report.** The gaps and stand-ins: "name every gap in the setup report" and the step-2 completion criterion: "every playbook in the resolved scaffold set has a reconciled counterpart, and every change, degraded stand-in, and flagged conflict is reported." The present playbooks get the LLM-audit reconciliation (step 2: "read the installed playbook against the current template, section by section … a section that diverges is repo practice — leave it"), with any conflicts shown rather than resolved silently (step 2: "Where a template change and repo practice genuinely conflict, show the conflict and let the user decide").

**May `run` pass preflight before those four exist? No.** `run.md` step 1 completion criterion: "every playbook in the **resolved scaffold set** has its `docs/agents/` counterpart … for `skill-authoring`, preflight therefore requires the full eleven counterparts (three unshadowed common files, four native pack files, and four flagged software stand-ins)." With four absent, preflight fails and run must "tell the user to run setup."

**Full counterpart count after repair: eleven** — `setup.md` step 1: "For `skill-authoring`, the full set has eleven counterparts: three unshadowed common files, four native pack files, and four flagged software stand-ins."



# P3 — Verifying a behavior change with only probe scenarios (no key, no answer key run, no app/stack)

**Order and executor roles, per `verify.md` and `verifying.md`:**

1. **Write the pass/fail answer key first — before any run.** `verifying.md`: "Put the scenarios in the changed skill's `evals/` directory and write their pass/fail answer key **before any executor run**." This is a hard precondition, not optional groundwork — the scenario existing without a key isn't yet verifiable.

2. **State explicit criteria** (`verify.md` step 1): "explicit, testable criteria derived from the issue and, for an enhancement, the approved plan's definition of done... Each criterion independently checkable as pass or fail."

3. **Run any existing checks** (`verify.md` step 2): "every check the PR will claim, per `verifying.md`, with its result known." (For a pure skill-behavior change this may be minimal/none beyond the probes.)

4. **Ready the surface — no app assumed.** `verify.md` step 3: "For skill behavior this is the executor harness loaded with the skill's situated scenario, deployment context, and prewritten answer key — **no app or stack is assumed**." This is exactly the no-app path the shared playbooks exist to support: `environment.md` § Running locally states "App / stack: **none assumed** — the runtime surface is the executor harness loading the skill and responding to a probe," and § Seed data names the "Drive-to-feature path" as: "load the skill in its real executor context, submit the situated scenario, preserve the cited transcript, and grade it against the prewritten key." `setup.md` step 5 backs this for skill-authoring specifically: "For `skill-authoring`, record the checked-in probe scenarios as seed state and do not invent an app or stack," and step 6 names the confirmed driver: "**Executor-harness skill behavior** → a fresh in-session executor plus an independent CLI executor, each able to load the skill context and answer a checked-in situated probe."

5. **Run through both executor roles, each producing a cited transcript.** `verifying.md`: "Run the same self-contained scenario through both executor roles: 1. An **in-session executor** in the harness where the skill will run. 2. An **independent CLI executor** in a read-only sandbox... Require each answer to cite the file and exact sentence that decided it, and explicitly allow genuine ambiguity to be reported. Preserve both cited transcripts." Who staffs the independent role is resolved by the `staffing` skill, per `environment.md` § Driving the app: "Independent runtime verification: independent CLI executor with a self-contained prompt, selected through the staffing skill/playbook," and `verify.md` § Staffing: "this whole loop runs in a delegated subagent filling the **checker** role — the role and its fallback ladder are resolved by the `staffing` skill."

6. **Grade against the key in a verdict table.** `verifying.md`: "Grade every probe against every prewritten answer-key criterion in a pass/fail verdict table; both executor roles must meet the recorded pass bar. If wording is ambiguous or a criterion fails, revise the skill and rerun the same keyed probe rather than changing the key to fit the output."

7. **Record the verdict per criterion in `verify.md`'s own loop** (step 4): "exercise each criterion against that ready surface and record a pass or fail, naming the gap on any fail... Record *how* each criterion was actually exercised" (caveat discipline for any forced workaround).

8. **Loop-or-report** (`verify.md` step 5): failed criteria go back to the relevant builder role via `staffing`; "A post-fix verdict comes only from **re-running the criterion's check against the same verification surface** — never from reasoning that the fix should work... an inferred pass is the one self-grading failure this loop's design permits, so it is banned outright." Cap at five iterations or a blocker escalates to the issue thread instead of continuing.

**What's retained as evidence at this stage:** `verify.md` § Staffing: "Verification produces a **verdict and its raw evidence record (the grading record)**, not presentation artifacts. Preserve the check output, cited executor transcripts, and per-criterion results needed to substantiate that verdict" — this raw record is what the later, separate `evidence.md` step packages; `verify.md` explicitly forbids doing that packaging here: "Do not render, commit, publish, or attach the evidence package here."

**On the teammate's "drive the app and take a screenshot" proposal:** that is **not** the skill-behavior verification seam here, and the playbooks are explicit about it. `verifying.md`: "Skill behavior is verified with **situated probes**, not quiz questions or instructions to drive an app... **Executor probes replace "drive the app" for skill behavior.**" `evidence.md` reinforces that a screenshot cannot substitute for the graded transcript: "An uncited executor summary or a screenshot without the keyed behavioral verdict is not sufficient proof of a skill decision." A screenshot is only ever *additive*, and only when the skill produces a visual artifact (`diagnosing-bugs.md`: "If the skill produces a visual surface, the regression proof also includes the relevant rendered artifact; a screenshot alone does not replace the behavioral probe"). Since the repo here "has no app or stack" (given), there is no app to drive in the first place — the seam is the executor-harness probe run through both roles and graded against the prewritten key, per the citations above.

---

## (a) Copy-not-regrade check

**Settled: yes, verified as a straight copy with no independent re-grading (as of the final verify record captured at evidence time).**

`evidence.md`: "Captured once after review converges, **copy the final verify step's raw transcript and verdict record into the evidence package without re-running or independently re-grading it.**"

This is unambiguous: the evidence-package step is a carry-over of verify's raw grading record, not a re-derivation.

## (b) Review-triggers-reverification check

**Settled: yes — review changes must be re-verified before evidence captures anything, and the fresh record (not the stale one) is what gets carried forward.**

Same sentence in `evidence.md`, immediately following the copy clause: "**If review changed behavior, the affected criteria must have been re-verified first and the newest raw record replaces the stale rows.**"

So the two halves of that one sentence in `evidence.md` jointly settle both (a) and (b): copy-without-regrading is the default action, but it operates only on the record as of the *latest* verify run — and review changes are explicitly required to trigger that re-verify before the evidence step runs. `verify.md` corroborates the ordering from the other side: "the separate, terminal `reference/evidence.md` step packages that raw record and captures any additional human-facing proof **against the final reviewed HEAD**" — i.e., evidence targets the post-review HEAD, and the record it copies must therefore already reflect any review-triggered re-verification, not a pre-review snapshot.

## Ambiguities flagged

- None of substance in these six files for (a) and (b) — the single sentence in `evidence.md` (§ What to capture) resolves both cleanly.
- Minor: none of the six files define "review" as specifically "the adversarial review / fixer loop" in so many words — `evidence.md` just says "after review converges" / "if review changed behavior." `setup.md` names the relevant step playbooks as `change-reviewer` and `change-fixer`, which is consistent with reading "review" that way, but the identification is inferential rather than a verbatim definition within the six files read.
- P3's "no app or stack" framing is fully corroborated by name across `setup.md`, `verify.md`, and `environment.md`, with no conflicting language found.
