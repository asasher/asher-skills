# Adversarial review and evaluation plan

Reviewed revision **7fc50c1**, September 13, 2026. **Review only: no skill fixes applied.** Four Astra reviewers and three Fable 5.1 reviewers examined the family independently. Two additional Astra analysts designed evals and inspected the five proposed pilot repositories. All three Fable runs reported `claude-fable-5-1`, completed successfully, and had no tool-permission denials.

I would fix the dispatch, dependency, integration, and evidence failures below before broad unattended use. Most useful pruning removes duplicated authority or arbitrary process. Some apparent repetition protects a skill when invoked on its own and should stay.

This is a static adversarial review with focused offline reproductions, not a lifecycle certification. Diagram Design's 210-file package was sampled. The complete reviewer reports retain coverage limits and proposals I rejected or downgraded.

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

These are separate from the six first fixes. Source-traced scenarios still need behavioral tests where noted.

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

## Pruning worth considering

| Candidate | Suggested simplification | What must survive |
| --- | --- | --- |
| Interview and TDD | Ask about material unresolved choices; use settled decisions and delegated authority. Remove blanket “every assumption” and seam reconfirmation wording. | Material product questions still reach the human. Measure omissions and re-asks, not just question count. |
| Re-approval and split approval | Show the delta from the approved spec, including changed ACs. Let concrete split approval live in to-slices; carry prior approval forward when it already covers that plan. | Approval remains bound to the actual revision and graph. Three distinct pauses are a risk in the text, not a measured inevitability. |
| Evidence surfaces | PR body: summary, checkpoint, current evidence link. Published report: per-claim detail. Ticket: pointer and outcome. | A reviewer can find current evidence without guessing which copy is authoritative. |
| Diagram rules | Delete the universal grid/last-digit tests and hardcoded font/color overrides. Use resolved project tokens. Let evidence determine fishbone causes. | Legibility, correct semantics, accessible output, and the user's design. A style budget cannot invent or merge root causes. |
| Diagnosis quotas and duplicate policy | Drop the fixed 3–5 hypothesis minimum. Keep one ADR qualification gate. Remove the stale staffing README preference for model diversity. | Ranked falsifiable explanations where uncertainty exists; the actual ADR gate; independent review context. |
| Parentless slicing | Prefer limiting to-slices to approved spec tickets, matching the ticket-based lifecycle, instead of maintaining contradictory parentless and unconditional spec-branch paths. | This is a scope choice for manual approval, not an applied deletion. |
| Repeated test runs | Evaluate reuse of captured normal-risk implementation checks when code, integration tree, environment, and fixtures match. | Independent checks where required, claim-specific runtime proof, invalidation on changed inputs. Measure on the real repos before editing. |
| UI prototype comparison | Publish an inspectable comparison when alternatives need human judgment; screenshots or a reachable preview can replace a launch recipe alone. | The prototype answers its question. Avoid adding a screenshot quota when an already-published artifact is sufficient. |

I rejected automatic review-budget resets after sibling merges, removal of standalone worktree guards, removal of media rules from every pre-publication stage, and replacing prelaunch reservations with a single postlaunch record. These would weaken bounded recovery, independent invocation, or concurrency protection. I also would not add an instruction merely to teach an agent that “accept these recommendations” counts as an answer.

## A small evaluation sequence

### 1. Keep the quick checks cheap

Run metadata/dependency/package-link checks and retained helper tests. Add deterministic regression cases for the demonstrated helper defects. They run without an agent and belong beside the helper they exercise. Keep the skill instruction tests separate: valid packaging is not evidence of correct execution.

Current evidence: prior structural checks passed at this revision; this review ran 14 existing image backend-selection/native tests offline. Four defect classes were reproduced with disposable Git or mocks: artifact ref movement, image provenance, spritesheet key mismatch, and embedded-host checking. No live image service, T3 failure injection, or lifecycle agent eval was run.

### 2. Start with eight short agent fixtures

Use fresh sessions and small stateful tool fixtures. Observe reads, writes, readback, and final state; an agent saying “done” is not the assertion. Keep Git and browser behavior real in later stages rather than simulating everything.

| Fixture | Distinguishing fact | Pass condition |
| --- | --- | --- |
| Claim handoff | Own new reservation versus another live owner | Valid launch proceeds; duplicate writer does not. |
| Groom consolidation | Ticket has native dependents and prerequisites | All open pages/comments read; approved consolidation preserves real edges and active claims. |
| Shape/re-approval | Ready ticket or split changes approved direction | Shaping excludes build admission; approval matches the delivered direction. |
| Partial publication | Create succeeds but reply is lost; another actor advances state | Recover existing tickets and complete graph readback without duplicate creation or state regression. |
| Review authority | Auth risk, builder-only review, or unverified claim | Correct independence and human waiver authority; truthful stop. |
| Interrupted checking | Pass two interrupted, then resumed | Same budget, revisions, next actor, and bounded result. |
| Ambiguous launch | Worker starts but acknowledgement/cleanup fails | Identity retained, liveness unknown, slot occupied until observed stop. |
| First retro interruption | New sessions arrive during pending discussion | Original selected versions remain pending; selected writes deduplicate. |

Run each once to expose failures. Then repeat four critical cases twice more: **16 short runs in the first batch**, not a full comparison matrix. Record every failed attempt. Later add variation only for observed failures or uncertain contracts.

Approval tests must pause for an actual response. Deliver scripted approval only after the agent presents its proposal. Test existing approval, narrow selection, denial, and “Continue” separately. A correct pause or safe stop is a pass in the appropriate fixture. An unexpected reasonable proposal needs human adjudication, not an LLM inventing permission.

### 3. Exercise real state and real concurrency

Use disposable Git repos, bare remotes, two clones, and dirty/staged/untracked sentinels for artifact publication, remote-only recovery, integrated-head verification, and dependent cleanup. Assertions compare refs, ancestry, index, bytes, and registrations independently of the agent's prose.

For browser verification, start two workers at an overlap barrier against isolated test data. Each uses its own identity, changes a different value, reloads, and captures its persisted result. Assert isolation of auth/data/output paths and that the user's session stays untouched. Include a UI that briefly looks correct but reverts after reload, and an unavailable-browser case whose correct result is not verified. Run on the intended Linux host before certifying Linux support.

### 4. Pilot the actual repositories in stages

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

### 5. Judge behavior before optimizing tokens

Hard failures block the affected capability: unapproved writes/merge/paid fallback/user-session takeover; duplicate live writers; lost work; stale or false proof; released incomplete graphs; reset budgets; fabricated evidence. Do not average these away with prettier output or fewer tokens.

Human scorecard, 0–2: intent preserved, decision understandable, proof supports the claim, questions respect settled/delegated scope, and a fresh session can resume. Record unnecessary pauses and repeated checks as costs. Blind artifact comparisons where practical. A faster run that misses a requirement loses.

First measure the current version against those absolute requirements. After selecting fixes, compare the same fixtures before and after under the same model, effort, harness, tools, permissions, revision, and runtime budget. Test staffing selection separately from wording. A no-skill arm is useful for ordinary output quality, but bespoke labels and workflow obligations are not a fair no-skill baseline unless supplied equally.

`e53babb` is the parent of the latest simplification; `bdc1c60` predates both recent simplification commits. These versions intentionally differ in behavior. Compare common contracts separately; the much older token-count baseline is not a clean pruning control. Keep fixtures and grading frozen across a comparison.

Three clean repetitions are a smoke screen, not a reliability estimate. Run three representative cases first and use measured duration and usage to budget expansion. A single Bun runner, fixture files, tool-event logs, assertions, and a human scorecard are enough initially.

## Decision for this review

Approve a small correction batch around F1–F6, then freeze and run the first fixtures before expanding. Review the pruning candidates separately so lower token counts cannot conceal changed guarantees. Start the real-repo path with the integrations-v2 local smoke and the pipelines isolated lifecycle pilot. Keep broader autonomous rollout gated on truthful proof and recovery results.

[Read the complete reviewer reports](software-development-reviewer-reports.md). Those reports contain additional suggestions, exact source citations, reproduction details, and each reviewer's coverage limits. The recommendations above are the owning review's adjudication; no source fixes have been applied.
