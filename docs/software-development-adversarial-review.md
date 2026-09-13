# Adversarial review and evaluation plan

Original review: revision **7fc50c1**, September 13, 2026. **The approved corrections and pruning are now applied on PR #201.** Four Astra reviewers and three Fable 5.1 reviewers examined the family independently. Two additional Astra analysts designed evals and inspected the five proposed pilot repositories. All three Fable runs reported `claude-fable-5-1`, completed successfully, and had no tool-permission denials.

The patch repairs dispatch, dependency, integration, and evidence failures. Pruning removes duplicated authority and arbitrary process while retaining standalone worktree protection, independent review, bounded recovery, and human merge selection.

This is a static adversarial review with focused offline reproductions, not a lifecycle certification. Diagram Design's 210-file package was sampled. The complete reviewer reports retain coverage limits and proposals I rejected or downgraded.

## Applied changes

| Contract | What changed | Evidence still needed |
| --- | --- | --- |
| Tickets and shaping | Consolidation transfers native prerequisites and dependents before closure. Shape claims its ticket, holds affected split work during revisions, and releases only a reconciled approved graph. Capture recovery preserves advanced owners. | Agent fixtures for concurrent claims, partial publication, and re-approval. |
| Build and merge | Deliver accepts its own launch reservation and records stopped outcomes. Checks identify the tested integration tree. Merge requires applicable server protection, current authority, and risk-appropriate independent proof. | Conflict-free integration failure and a disposable GitHub test of base movement during merge. |
| Runtime recovery | Artifact publication rejects occupied and symbolic target refs. T3 preserves identity and unknown liveness through ambiguous responses or failed credential cleanup. Naming and authentication waits are bounded. | Live harness compatibility and failure injection. |
| Image provenance | Native output belongs to the returned session and a completed typed image result. Sprite generation and extraction share one resolved chroma key. | Live native-format compatibility; unsupported formats stop safely. |
| Retro | Save the selected session versions before discussion. Resume that batch without advancing completed coverage; historical reviews preserve normal progress. | Interrupted sweep with new arrivals and selected tracker-write recovery. |
| Simpler instructions | Six diagram output checks replace the duplicated checklist. Resolved project tokens govern visuals. Diagnosis uses a trustworthy bounded reproduction. Interview and TDD reuse settled decisions. Specs show approval deltas; published reports own detailed proof. | Human comparison of clarity, question quality, diagrams, and proof on the same fixtures. |

Embedded motion figures share one canonical controller in the host; isolated checker fixtures include that controller once. The fixes include direct approval propagation for ticket-based splits, inspectable prototype comparisons, context-document registration, and explicit human waiver provenance. Routine verification may reuse matching recorded checks; an independent verifier runs its own checks. No automatic review-budget reset was added.

### Validation status

The final offline suites pass: **6 artifact-branch tests, 32 dispatch/naming tests, and 34 image-backend tests (72 total)**. Sprite acceptance covers 14 criteria plus bounds sanity; the versioning dry run passes. New regressions were demonstrated failing against the prior helpers. Nine offline diagram cases cover valid fragments, host separation, rejected unsafe fragments, and shipped templates. A headless browser check confirms two motion figures step independently with one shared controller.

Three fresh independent review contexts found and closed additional gaps: symbolic target refs, malformed T3/auth responses, merge during shaping holds, publication ownership for unchanged builders, and repeated embedded motion initialization. These follow-up reviews used source inspection and focused reproductions.

Structural checks pass for 46 authored skills and the 36-skill install closure, with no runtime cross-package file links. The mobile reader exposes all 385 family package files; 2,034 local links and anchors resolve. Mobile and desktop rendering checks found no page overflow or browser errors. These checks establish narrower facts than a lifecycle run.

**Synthetic agent runs are no longer the rollout gate.** The user selected real repository work as the behavioral assessment. Helper regressions remain. Pilot installation, reconciliation, and ordinary work are the next steps; no pilot build is claimed here.

The following findings describe the **original reviewed revision**. Their line numbers and failure descriptions are historical; source links open the corrected files. Original reviewer reports remain unchanged.

## First fixes to review

### F1. Consolidation can unblock unfinished work

**High confidence, source-traced.** [Backlog line 18](../skills/software-development/backlog/SKILL.md) preserves intent and links when consolidating tickets. Its [label contract](../skills/software-development/backlog/reference/labels.md) closes duplicates and treats a closed blocker as satisfied. No step transfers native dependencies.

If A blocks C and groom merges A into B, closing A makes C eligible before B delivers the prerequisite. A prose replacement link does not preserve the gate.

**Smallest change:** transfer the approved true prerequisite/dependent edges to the survivor and read them back before closing the source ticket. **Eval:** assert C remains blocked after consolidation, including incoming and outgoing edges.

### F2. A dispatched build no longer has the label its worker requires

**High-confidence instruction gap; runtime frequency unmeasured.** [Backlog line 27](../skills/software-development/backlog/SKILL.md) sets `building` before dispatch. [Deliver line 15](../skills/software-development/deliver/SKILL.md) requires `ready-for-agent` for a new build, or an ownership checkpoint and stopped prior worker for a resume. It does not distinguish a newly reserved launch from a resumed worker.

A literal worker rejects its valid preclaimed ticket; another guesses that this is a resume. Fable found this handoff mismatch independently of the runtime helper review.

**Smallest change:** explicitly accept a newly dispatched `building` claim belonging to this launch, while rejecting another live owner's claim. **Eval:** run the same worker input with its own reservation, another live reservation, and an expired claim whose worker is still running.

### F3. T3 failure handling can lose or misdescribe a live worker

**High confidence, source-traced; no live T3 failure injection.** Two paths in the [T3 helper](../skills/system/to-thread/scripts/t3-thread.py) break the recovery contract:

- Lines 487–495 treat an ambiguous turn-start failure as grounds for deletion. If deletion fails, line 363 describes a thread “without a running turn,” although the server may have accepted the start before the response was lost.
- Lines 554–570 suppress a successful launch result if temporary-session revocation fails. The caller receives an error without the launched thread's UUID.

Both can undermine liveness checks and duplicate-worker prevention.

**Smallest change:** preserve the known thread identity in every outcome; separate launch state from credential cleanup. Ambiguous start means unknown liveness and retained ownership until confirmed stopped. **Eval:** fake an accepted start with a lost acknowledgement, failed deletion, and successful launch followed by failed revocation. Assert identity and uncertainty survive every path.

### F4. Current head/base labels do not prove the integrated change

**High confidence, source-traced.** [Verification line 14](../skills/software-development/verify-your-work/SKILL.md) records the target base but runs the requested head. A head based on B0 can be tested again while the report names B1, without ever running H combined with B1. Conflict-free API changes can break only after integration.

There is also a separate race in [merge lines 20–21](../skills/software-development/merge/SKILL.md): `--match-head-commit` guards the head, not a base that moves after the final client read.

**Smallest change:** identify and test the intended integration tree, then use server-enforced up-to-date/merge-queue checks appropriate to the repository. State exactly what the protection guarantees. Another client-side read cannot make the base check atomic. **Evals:** incompatible but conflict-free branches; base movement between final read and merge. A mock can check intended parameters, but only a disposable GitHub trial establishes the configured server gate.

### F5. Artifact publication can invalidate another worktree

**Reproduced in a disposable Git repository.** [To-branch line 59](../skills/software-development/to-branch/scripts/to-branch.py) updates a target ref without checking whether a registered worktree has it checked out.

The helper exited successfully and advanced the other worktree's HEAD, while `spec.html` remained absent. Git status reported `D  spec.html`: its unchanged index now described a deletion relative to the advanced HEAD.

**Smallest change:** refuse a target checked out in any registered worktree. Preserve the temporary index and expected-old-ref guard. **Eval:** compare both worktrees' refs, index, files, and status before and after a refused publication; include the current checkout as a target.

### F6. Native imagegen can claim an unrelated image as its result

**Reproduced with an offline mock.** [Native extraction lines 94–125](../skills/creative/codex-imagegen/scripts/codex_imagegen.py) searches recent transcripts and accepts the best candidate without binding it to the launched session or requiring a successful process result.

A mocked failed “robot” request returned an unrelated “sunset landscape” image from another transcript, with `matched_kw=0`. This is false evidence, not merely an image-quality issue.

**Smallest change:** accept generated-image output only from the launched session with attributable provenance; report missing or ambiguous output as failure. **Eval:** overlapping sessions, failed subprocess, unrelated image, and zero keyword matches. Keyword similarity alone must never establish ownership.

## Further corrections

These corrections are applied alongside F1–F6. The table preserves the original finding and proposed test; source-traced scenarios still need behavioral tests where noted.

| Area | Finding and smallest proposed correction | Targeted eval |
| --- | --- | --- |
| [Shape intake, line 13](../skills/software-development/shape/SKILL.md) | Standalone shape does not establish `shaping` or revoke readiness before reopening decisions. Establish ownership and active state at intake. | Reopen a ready ticket from its correct worktree while a build sweep runs; no build admission. |
| [Split source, lines 7–12](../skills/software-development/to-slices/reference/slicing.md) | Later “refinements” can contradict the approved hash while the source spec must stay verbatim. Separate split-boundary edits from requirement changes; revised direction needs an approved source. | H1 says 30-day retention; later ruling says seven. Children and parent must share the same approved authority. |
| [Capture recovery, line 16](../skills/software-development/capture/SKILL.md) | Readback requires no readiness label even on an adopted uncertain create. Preserve labels/claims advanced by another owner. | Lose create acknowledgement, advance issue to `building`, then resume capture without creating or resetting it. |
| [Merge gate, line 19](../skills/software-development/merge/SKILL.md) | It accepts LGTM and verification without checking the recorded risk's independence requirements. Require reports satisfying those requirements; clarify that a waiver comes from explicit human authorization, including recorded chat approval. | Auth PR with only builder-produced reports; unverified claim with an agent-authored waiver. Both remain blocked. |
| [Deliver stops, lines 30–42](../skills/software-development/deliver/SKILL.md) | The label reference names `ready-for-human` for environment/cap stops, but the standalone owner only records a stop. Make the verb own the terminal state transition. | Exhaust the review bound; status must report stopped work consistently rather than leave an ambiguous active claim. |
| [Retro checkpoint, lines 17–19](../skills/software-development/retro/reference/checkpoint.md) | An interrupted first sweep has no durable pending selection. New sessions can replace its original latest-three batch. Persist the selected versions before discussion without advancing completed coverage. | Interrupt A/B/C, add D/E/F, resume in fresh context; A/B/C stay pending. |
| [Protocol waits](../skills/system/to-thread/scripts/name-codex-thread.py) | Naming waits on an unbounded `readline`; T3 auth subprocesses also lack a timeout. Bound waits and return known identity. | Fake a silent server/auth CLI; require a bounded, recoverable stop and reaped subprocess. |
| [Embedded diagrams, line 24](../skills/creative/diagram-design/references/embedded-output.md) | Applying the standalone checker to the whole host rejects required research citations and ordinary host scripts. Validate the figure's policy locally; validate host rendering/integration separately. **Offline reproduced.** | Valid diagram inside a cited research dossier and an interactive host. Both remain publishable. |
| [Spritesheet key, line 596](../skills/creative/codex-imagegen/scripts/extract_spritesheet.py) | Generation always requests magenta while extraction can select green. Resolve one key and use it in both stages. **Offline reproduced.** | Request a green key; assert generated prompt, extraction color, and retained subject pixels agree. |
| [Diagnosis, lines 11–13](../skills/software-development/diagnosing-bugs/reference/diagnosis.md) | A mandatory seconds-long reproducer blocks inherently slow leaks or performance regressions. Require the fastest trustworthy reproducer with a measured bound. | A slower deterministic reproduction fails while every reduced fixture passes. |
| [Context ownership](../skills/software-development/domain-modeling/SKILL.md) | Context/product owners omit the index registration required by CONTEXT.md; shape reads DESIGN.md without naming its creation owner. Restore owner-level discovery/creation contracts. | Fresh project acquires one glossary term, user type, and durable visual decision; each document gets one usable pointer. |
| [Split-parent delivery, line 31](../skills/software-development/deliver/SKILL.md) | Other packages describe coverage-gap child creation, but deliver only specifies small integration fixes and broader stops. Clarify whole-spec coverage and propose missing slice work through the approved capture path. | All children closed but one AC missing: report the gap and obtain the required tracker decision; no silent feature expansion. |

## Applied pruning

| Candidate | Suggested simplification | What must survive |
| --- | --- | --- |
| Interview and TDD | Ask about material unresolved choices; use settled decisions and delegated authority. Remove blanket “every assumption” and seam reconfirmation wording. | Material product questions still reach the human. Measure omissions and re-asks, not just question count. |
| Re-approval and split approval | Show the delta from the approved spec, including changed ACs. Let concrete split approval live in to-slices; carry prior approval forward when it already covers that plan. | Approval remains bound to the actual revision and graph. Three distinct pauses are a risk in the text, not a measured inevitability. |
| Evidence surfaces | PR body: summary, checkpoint, current evidence link. Published report: per-claim detail. Ticket: pointer and outcome. | A reviewer can find current evidence without guessing which copy is authoritative. |
| Diagram rules | Delete the universal grid/last-digit tests and hardcoded font/color overrides. Use resolved project tokens. Let evidence determine fishbone causes. | Legibility, correct semantics, accessible output, and the user's design. A style budget cannot invent or merge root causes. |
| Diagnosis quotas and duplicate policy | Drop the fixed 3–5 hypothesis minimum. Keep one ADR qualification gate. Remove the stale staffing README preference for model diversity. | Ranked falsifiable explanations where uncertainty exists; the actual ADR gate; independent review context. |
| Parentless slicing | Prefer limiting to-slices to approved spec tickets, matching the ticket-based lifecycle, instead of maintaining contradictory parentless and unconditional spec-branch paths. | Applied after approval: slicing starts from an approved spec ticket. |
| Repeated test runs | Evaluate reuse of captured normal-risk implementation checks when code, integration tree, environment, and fixtures match. | Independent checks where required, claim-specific runtime proof, invalidation on changed inputs. Measure reuse on the real repositories before claiming a speed improvement. |
| UI prototype comparison | Publish an inspectable comparison when alternatives need human judgment; screenshots or a reachable preview can replace a launch recipe alone. | The prototype answers its question. Avoid adding a screenshot quota when an already-published artifact is sufficient. |

I rejected automatic review-budget resets after sibling merges, removal of standalone worktree guards, removal of media rules from every pre-publication stage, and replacing prelaunch reservations with a single postlaunch record. These would weaken bounded recovery, independent invocation, or concurrency protection. I also would not add an instruction merely to teach an agent that “accept these recommendations” counts as an answer.

## A small evaluation sequence

### 1. Keep the quick checks cheap

Run metadata/dependency/package-link checks and retained helper tests. Add deterministic regression cases for the demonstrated helper defects. They run without an agent and belong beside the helper they exercise. Keep the skill instruction tests separate: valid packaging is not evidence of correct execution.

Original review evidence: structural checks had passed at the reviewed revision; the initial review ran 14 existing image backend-selection/native tests offline. Four defect classes were reproduced with disposable Git or mocks: artifact ref movement, image provenance, spritesheet key mismatch, and embedded-host checking. No live image service, T3 failure injection, or lifecycle agent eval was run.

### 2. Judge behavior during real repository work

The user chose actual repository work as the behavioral assessment. The proposed synthetic agent fixtures are retired as a rollout gate: an agent recognizing an evaluation can behave differently from ordinary work. The earlier plan remains in Git history and the original reviewer reports.

Observe normal groom, shape, build, merge, and retro sessions in the pilot. Use their actual tracker mutations, commits, CI, app behavior, evidence, and recovery outcomes. Capture failures through retro and offer project issues for user selection. Keep helper regression tests for concrete code defects.

Start with installation and reconciliation: inspect installed skills, tracked and ignored playbooks, instruction pointers, worktree assumptions, and machine-local configuration. Preserve project knowledge while replacing obsolete family policy. Reuse the established skill installer; add a small repeatable checkout migration only where ignored or local files need it. Show the change and its preserved/removed material in a PR.

Then select real work. Observe whether default build drains exactly the ready-for-agent tickets with no open blockers, whether spec waves respect merge and shaping decisions, and whether milestone waves preserve scope and report waits truthfully. A real interruption or failure becomes evidence to improve the skills; simulated agent scores are not a prerequisite.

### 3. Pilot the actual repositories in stages

Repository inspection was read-only: the commands and capabilities below have not been run or certified here. Each pilot pins both repository and skill revisions and uses disposable resources plus human merge selection.

| Order | Repository | First exercise | Why / constraints |
| --- | --- | --- | --- |
| Quick smoke | `integrations-v2` | One export-core formatting/filename boundary case, chosen after reading its test imports. | Small Node/Vitest seam, before browser/auth work. Respect this repo's pnpm contract. |
| First full lifecycle | `pipelines` | One synthetic inbound-validation bug, then a browser-visible result with inspected proof. Add a planned checkpoint/resume. | Bun/TypeScript; worktree-aware Postgres, MinIO, SFTP, noop OTP, and batch fixtures. Some tests hardcode DB addresses; choose the lane deliberately. Real providers remain a separate serialized lane. |
| Second full lifecycle | `integrations-v2` | One local-Convex UI/export journey, then an approved split with partial-publication recovery. | Next.js/Convex/Clerk. Local backend isolation exists; Clerk presets remain shared. Fresh browser state per run; no shared reset-and-seed for the trial. |
| Serialized pilot | `metis` | Task-date or CLI validation case, then a bounded full-stack check in its exclusive lane. | Next.js/tRPC/Yjs/Hono with shared DB/Clerk/Drive/queues. Target is staging. CI has no test job; a green CI result must not stand in for behavior. Preserve the task-test timezone. |
| Readiness pilot first | `zyngo` | Reconcile setup facts; then an isolated convex-test case. Add mobile proof only for demonstrated surfaces. | Environment docs claim no scaffold, while Expo/Convex code and tests exist. Web evidence cannot establish native behavior. Shared Clerk/Convex and external fixture provisioning need explicit isolation. |
| Pending location | `millwright-agent` | Locate the requested checkout before choosing a case. | Exact path absent. The nearby Millwright collateral project is not a substitute. |

These are proposed ticket types, not discovered product defects. Begin with a disposable clone and selected low-risk work. Introduce real tracker writes and artifact publication only in the chosen pilot scope. Do not make the first confidence exercise a production-auth or destructive-data change.

### 4. Review actual outcomes

Lost work, duplicate live writers, unapproved changes, stale or false proof, released incomplete graphs, and reset review budgets require correction. Use real evidence to distinguish a skill defect, missing repository setup, a tool failure, and an ordinary implementation bug.

During human review, assess whether intent survived, decisions were understandable, proof supports the claims, questions respected settled choices, and another session could resume. Review context cost only alongside these outcomes. Retro keeps findings on the current project's backlog after the user's selection.

## Decision for this review

The approved correction and pruning batch is applied. Review and merge the candidate, then reconcile the selected pilot repository and judge the family through real work. Expand to other repositories after resolving the setup and behavior problems the pilot exposes.

[Read the complete reviewer reports](software-development-reviewer-reports.md). Those reports contain additional suggestions, exact source citations, reproduction details, and each reviewer's coverage limits. The original recommendations were adjudicated before implementation; the applied-status section above describes the resulting patch.
