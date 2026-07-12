# Codex executor transcript — issue #35

> Provenance: raw cited executor output copied without re-running or re-grading. P1/P2 are copied verbatim from /tmp/issue35-codex-rerun.md at commit 6a0bdacb1234e877148e47299e8818ad7c750370. P3 is copied verbatim from the converged /tmp/issue35-codex-p3-converged.md at reviewed commit 001376238342bbf4559acea0cef4c4404b08a869; it supersedes the earlier P3 record after the verification-record handoff fixes.

# P1

Offer exactly these six work-domain choices:

`software` / `skill-authoring` / `writing` / `research` / `ops` / `general`

Propose `skill-authoring` because the repository contains `SKILL.md` files under `skills/<name>/`. This happens before any scaffolding.

Deciding sentences — [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:14):

> Fresh install: **before scaffolding anything**, ask the user "what kind of work does this repo track?" with exactly six options: `software` / `skill-authoring` / `writing` / `research` / `ops` / `general`.

> Default the answer from repo evidence and confirm rather than interrogate, in the same posture as step 3's binding questions: a skill-authoring repo (`SKILL.md` files under `skills/<name>/`) defaults to `skill-authoring`; a code repo (`package.json`, `src/`, a test runner) defaults to `software`; a manuscript defaults to `writing`; ambiguous evidence defaults to `software`.

After confirmation, record `skill-authoring` in the installed `docs/agents/backlog-policy.md` under `§ Work domain`.

Deciding sentence — [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:14):

> Record the answer in the installed `backlog-policy.md` § Work domain.

The resolved scaffold contains eleven counterparts.

| Installed counterpart | Source | Status |
|---|---|---|
| `backlog-policy.md` | `templates/common/backlog-policy.md` | Native common |
| `platform.md` | `templates/common/platform.md` | Native common |
| `change-description.md` | `templates/common/change-description.md` | Native common |
| `environment.md` | `templates/skill-authoring/environment.md` | Native skill-authoring; shadows common |
| `verifying.md` | `templates/skill-authoring/verifying.md` | Native skill-authoring |
| `evidence.md` | `templates/skill-authoring/evidence.md` | Native skill-authoring |
| `diagnosing-bugs.md` | `templates/skill-authoring/diagnosing-bugs.md` | Native skill-authoring |
| `implementing.md` | `templates/software/implementing.md` | Flagged software stand-in |
| `refactoring.md` | `templates/software/refactoring.md` | Flagged software stand-in |
| `change-reviewer.md` | `templates/software/change-reviewer.md` | Flagged software stand-in |
| `change-fixer.md` | `templates/software/change-fixer.md` | Flagged software stand-in |

The three directory listings establish the available filenames. The overlay and fallback decisions come from [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:16):

> Scaffolding and reconciliation draw from the **resolved scaffold set**: first overlay `templates/common/` with `templates/<domain>/`, with a same-name pack file shadowing common; then add the same-name `templates/software/` baseline as a flagged stand-in for every required step playbook absent from that overlay.

The domain-specific shadow and exact four stand-ins are decided by [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:17):

> For `skill-authoring`, its pack `environment.md` shadows common and only `implementing.md`, `refactoring.md`, `change-reviewer.md`, and `change-fixer.md` come from software as flagged stand-ins.

The total is explicitly fixed by [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:11):

> For `skill-authoring`, the full set has eleven counterparts: three unshadowed common files, four native pack files, and four flagged software stand-ins.

Each of the four stand-ins must receive a header flag identifying it as a code-flavored baseline needing tailoring, and each missing native baseline must be named in the setup report.

Deciding sentences — [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:17):

> Add one flag line to every installed stand-in's header naming it a code-flavored baseline to tailor for `<domain>`, and name every gap in the setup report.

> Never leave a required playbook uninstalled.

Setup must also report every degraded stand-in and other reconciliation result.

Deciding sentence — [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:21):

> Completion criterion: the domain is chosen and recorded, every playbook in the resolved scaffold set has a reconciled counterpart, and every change, degraded stand-in, and flagged conflict is reported.

**Ambiguity:** None. The six choices, evidence-based default, eleven-file count, shadow, four fallbacks, flagging, reporting, and domain recording are explicit.

# P2

The recorded `skill-authoring` domain remains authoritative on the re-run.

Deciding sentences — [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:15):

> Re-run: the recorded domain stands.

> Changing an installed repo's domain is a user decision, never a silent reconciliation outcome.

The skill-authoring `environment.md` wins. The common `environment.md` is shadowed and must not become the installed baseline.

Deciding sentences — [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:16):

> Scaffolding and reconciliation draw from the **resolved scaffold set**: first overlay `templates/common/` with `templates/<domain>/`, with a same-name pack file shadowing common; then add the same-name `templates/software/` baseline as a flagged stand-in for every required step playbook absent from that overlay.

And specifically, [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:17):

> For `skill-authoring`, its pack `environment.md` shadows common and only `implementing.md`, `refactoring.md`, `change-reviewer.md`, and `change-fixer.md` come from software as flagged stand-ins.

The native skill-authoring files that remain are:

- `environment.md`
- `verifying.md`
- `evidence.md`
- `diagnosing-bugs.md`

Only the four absent counterparts are repaired from their same-name software templates:

- `implementing.md`
- `refactoring.md`
- `change-reviewer.md`
- `change-fixer.md`

The rule forbidding replacement of present native files is the “only each missing” rule in [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:17):

> When a shipped pack omits a required step baseline, install only each missing same-name `templates/software/` baseline as a stand-in.

Every repaired stand-in must be header-flagged, and setup must name all four gaps in its report.

Deciding sentence — [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:17):

> Add one flag line to every installed stand-in's header naming it a code-flavored baseline to tailor for `<domain>`, and name every gap in the setup report.

`backlog run` may not pass preflight while any of those four files is absent. Its completion criterion requires every resolved counterpart, and it explicitly requires eleven for `skill-authoring`.

Deciding sentences — [run.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/run.md:11):

> Completion criterion: every playbook in the **resolved scaffold set** has its `docs/agents/` counterpart.

> The required step names are `implementing`, `verifying`, `evidence`, `diagnosing-bugs`, `refactoring`, `change-reviewer`, and `change-fixer`; for `skill-authoring`, preflight therefore requires the full eleven counterparts (three unshadowed common files, four native pack files, and four flagged software stand-ins).

After repair, the full count is eleven: three unshadowed common files, four native skill-authoring files, and four flagged software stand-ins.

Deciding sentence — [setup.md](/Users/asher/Projects/asher-skills/skills/backlog/reference/setup.md:11):

> For `skill-authoring`, the full set has eleven counterparts: three unshadowed common files, four native pack files, and four flagged software stand-ins.

**Ambiguity:** None. Shadow priority, partial fallback, reporting, preflight failure, and the repaired count are explicit.



P3:

1. Key before execution:

> “Put the scenarios in the changed skill's `evals/` directory and write their pass/fail answer key **before any executor run**.”
> — `templates/skill-authoring/verifying.md`

2. Run the identical scenario through both roles:

> “Run the same self-contained scenario through both executor roles:”
> “1. An **in-session executor** in the harness where the skill will run.”
> “2. An **independent CLI executor** in a read-only sandbox.”
> — `templates/skill-authoring/verifying.md`

3. Each run must produce cited output, with ambiguity permitted:

> “Require each answer to cite the file and exact sentence that decided it, and explicitly allow genuine ambiguity to be reported.”
> “Preserve both cited transcripts.”
> — `templates/skill-authoring/verifying.md`

4. Grade only against the prewritten criteria:

> “Grade every probe against every prewritten answer-key criterion in a pass/fail verdict table; both executor roles must meet the recorded pass bar.”
> “If wording is ambiguous or a criterion fails, revise the skill and rerun the same keyed probe rather than changing the key to fit the output.”
> — `templates/skill-authoring/verifying.md`

5. Setup provides the no-app seed and execution path:

> “For `skill-authoring`, record the checked-in probe scenarios as seed state and do not invent an app or stack.”
> — `reference/setup.md`

> “**Executor-harness skill behavior** → a fresh in-session executor plus an independent CLI executor, each able to load the skill context and answer a checked-in situated probe.”
> — `reference/setup.md`

> “Record the **exercise-to-criterion path** — after readying and seeding the surface, how the agent reaches an observable criterion: load a skill and submit the situated scenario…”
> — `reference/setup.md`

6. Verify exercises that exact surface:

> “For skill behavior this is the executor harness loaded with the skill's situated scenario, deployment context, and prewritten answer key — no app or stack is assumed.”
> — `reference/verify.md`

> “Verification produces a **verdict and its raw evidence record (the grading record)**, not presentation artifacts.”
> — `reference/verify.md`

7. Review-time changes require actual re-verification, never inferred re-grading:

> “A post-fix verdict comes only from **re-running the criterion's check against the same verification surface** — never from reasoning that the fix should work…”
> — `reference/verify.md`

8. The final evidence package deterministically consumes that record:

> “Captured once after review converges, copy the final verify step's raw transcript and verdict record into the evidence package without re-running or independently re-grading it.”
> “If review changed behavior, the affected criteria must have been re-verified first and the newest raw record replaces the stale rows.”
> — `templates/skill-authoring/evidence.md`

“Drive the app and take a screenshot” is not the seam:

> “Skill behavior is verified with **situated probes**, not quiz questions or instructions to drive an app.”
> “Executor probes replace ‘drive the app’ for skill behavior.”
> — `templates/skill-authoring/verifying.md`

> “An uncited executor summary or a screenshot without the keyed behavioral verdict is not sufficient proof of a skill decision.”
> — `templates/skill-authoring/evidence.md`

Genuine ambiguity: none. The raw verification record is the grading record; behavioral review changes require re-running affected criteria on the same surface; the evidence step copies the newest final record without re-running or independently re-grading it. This is one deterministic handoff.

PASS against P3.
