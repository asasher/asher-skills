# Software development family: full manual review

The full review covers **36 skills and all 385 files in their packages**, matching the README install set. Start with [the visual guide](software-development.html#review). The complete file inventory below includes conditional references, templates, scripts, existing tests, sidecars, and credits. See the [simplification review](skill-instruction-review.md#simplification-review) for the applied setup, dispatch, diagram, and browser changes and Relay retirement.

The accepted September 13 [adversarial corrections](software-development-adversarial-review.md) are applied. Review ownership and dependency recovery, approval-bound revisions, tested integration trees and server merge gates, attributable runtime results, and the reduced interview, testing, diagram, and evidence ceremony. Focused helper regressions and offline checks are separate from behavioral assessment through real repository work, which follows installation and reconciliation. The original findings and evaluation plan remain available for comparison.

Read each entrypoint, then finish its package inventory before marking that skill reviewed. Diagram Design has 210 files; inspect its type references and rendered examples in their own review sitting. Existing tests are evidence to assess, not an instruction to run live services.

For each skill, record **accept**, **change**, or **needs behavioral evidence**, with the exact source sentence or file. Check the trigger, inputs, owner, approval boundary, output, recovery, and whether each instruction adds useful guidance. Sibling composition uses skill names; runtime file references stay inside the owning package. The source links in this review inventory are for human inspection. A linked file is inventoried; it is not yet manually approved.

## 1. Intake and grooming

Check how findings become tickets, how milestones survive consolidation, and who decides readiness.

- [ ] **01. [capture](../skills/software-development/capture/SKILL.md)**: One ticket per finding; confirmed publication; recovery preserves advanced labels and claims; milestone grouping and spec-parent gaps.
- [ ] **02. [backlog](../skills/software-development/backlog/SKILL.md)**: All open issues read; native dependencies preserved through consolidation; initial frontier draining and spec/milestone waves with human merge waits.

For build, trace three scopes: a frontier larger than capacity, a spec that needs a human merge between waves, and a milestone with independent and blocked work. Check selection, truthful waits, completion, and resume from tracker state.

## 2. Shaping and splitting

Follow one ticket from unsettled intent to an approved, recoverable build brief.

- [ ] **03. [shape](../skills/software-development/shape/SKILL.md)**: One ticket and worktree; shaping ownership, held children during revisions, approval deltas, artifacts, and release.
- [ ] **04. [interview](../skills/software-development/interview/SKILL.md)**: Material unresolved questions, carried answers, delegated choices, and when the conversation is complete.
- [ ] **05. [research](../skills/software-development/research/SKILL.md)**: Bounded fact questions, sources, uncertainty, and reusable results.
- [ ] **06. [prototype](../skills/software-development/prototype/SKILL.md)**: Which uncertainty an experiment resolves; inspectable alternatives when human judgment is needed; evidence on the ticket.
- [ ] **07. [domain-modeling](../skills/software-development/domain-modeling/SKILL.md)**: Consistent vocabulary, context-document discovery, and one qualification gate for architecture decisions.
- [ ] **08. [to-spec](../skills/software-development/to-spec/SKILL.md)**: Observable acceptance, delegated choices, verification risk, and deltas from the approved revision.
- [ ] **09. [to-slices](../skills/software-development/to-slices/SKILL.md)**: An approved ticket-bound spec, concrete split approval, vertical coverage, and graph readback before readiness.
- [ ] **10. [to-branch](../skills/software-development/to-branch/SKILL.md)**: Artifact commits, refusal of checked-out or symbolic target branches, preserved checkout state, remote history, and pushed revisions.

## 3. Building and proving

Check who owns the build, what independent checks establish, and when the PR is ready. For UI verification, review headless defaults, isolated alternatives, parallel sessions, user-desktop protection, and temporary-check retention.

- [ ] **11. [deliver](../skills/software-development/deliver/SKILL.md)**: The owner adopts its launch reservation; whole-spec coverage, checkpointed stops, correct targets, and finish gates.
- [ ] **12. [implement](../skills/software-development/implement/SKILL.md)**: Implementation scope, project conventions, and appropriate tests.
- [ ] **13. [adversarial-review](../skills/software-development/adversarial-review/SKILL.md)**: Independent verdicts, bounded fixes, refreshed evidence, and explicit stops.
- [ ] **14. [code-review](../skills/software-development/code-review/SKILL.md)**: Pinned inputs, review scope, actionable findings, and approval criteria.
- [ ] **15. [verify-your-work](../skills/software-development/verify-your-work/SKILL.md)**: Checks on the intended integration tree, risk-appropriate independence, valid normal-risk reuse, and truthful claim evidence.
- [ ] **16. [prove-your-work](../skills/software-development/prove-your-work/SKILL.md)**: One published report owns per-claim evidence; inspected visuals, revision identity, and current PR/ticket links.

## 4. Merging and learning

Check human selection, cleanup, interrupted work, and proposed issues from recent runs.

- [ ] **17. [merge](../skills/software-development/merge/SKILL.md)**: Shaping holds, risk and waiver authority, verified integration, server-enforced freshness, dependent branches, and safe cleanup.
- [ ] **18. [retro](../skills/software-development/retro/SKILL.md)**: Persisted pending transcript versions, bounded sweeps, selected tracker writes, and completed checkpoint coverage.
- [ ] **19. [handoff](../skills/software-development/handoff/SKILL.md)**: Enough durable context for another session to resume without losing decisions or unfinished work.

## 5. Setup and dispatch

Check the infrastructure that makes the lifecycle possible in a fresh repository or on another machine.

- [ ] **20. [agent-ready-codebase](../skills/software-development/agent-ready-codebase/SKILL.md)**: Demonstrated capability to run, seed, authenticate, isolate concurrent browser checks on the execution host, and publish.
- [ ] **21. [to-web](../skills/software-development/to-web/SKILL.md)**: Artifact destinations, immutable uploads, verified reachability, and media outside Git.
- [ ] **22. [to-thread](../skills/system/to-thread/SKILL.md)**: Worktree preparation, bounded protocol waits, preserved thread identity, and explicit uncertain liveness.
- [ ] **23. [to-subagent](../skills/system/to-subagent/SKILL.md)**: Bounded assignments, fresh context, deadlines, recovery, and returned results.
- [ ] **24. [staffing](../skills/system/staffing/SKILL.md)**: Astra, Fable, Terra, and image model assignments; owner stages and independent contexts.

## 6. Supporting standards

Review every supporting skill, including its conditional branches and packaged tooling.

- [ ] **25. [diagnosing-bugs](../skills/software-development/diagnosing-bugs/SKILL.md)**: The fastest trustworthy bounded reproduction, falsifiable candidates without a quota, and evidence before a fix.
- [ ] **26. [tdd](../skills/software-development/tdd/SKILL.md)**: Meaningful red/green checks at settled or delegated seams, with appropriate mocking.
- [ ] **27. [principle-codebase-design](../skills/software-development/principle-codebase-design/SKILL.md)**: Ownership boundaries, interfaces, and maintenance cost.
- [ ] **28. [principle-experience-first](../skills/software-development/principle-experience-first/SKILL.md)**: User journeys, questioned assumptions, and necessary behavior.
- [ ] **29. [principle-type-system-discipline](../skills/software-development/principle-type-system-discipline/SKILL.md)**: Domain states, impossible states, and type boundaries.
- [ ] **30. [typescript-best-practices](../skills/software-development/typescript-best-practices/SKILL.md)**: Project-compatible TypeScript rules that improve implementation choices.
- [ ] **31. [bare-minimum-design](../skills/creative/bare-minimum-design/SKILL.md)**: Product visual defaults, notifications, and the DESIGN.md template.
- [ ] **32. [diagram-design](../skills/creative/diagram-design/SKILL.md)**: Project-token precedence, fragment safety and host integration, evidence-based semantics, imports, exports, motion, and examples.
- [ ] **33. [codex-imagegen](../skills/creative/codex-imagegen/SKILL.md)**: Backend priority, attributable native results, consistent spritesheet keys, dimensions, versioned assets, and recovery.
- [ ] **34. [technical-writing](../skills/software-development/technical-writing/SKILL.md)**: Readable durable tickets, specs, reports, and PR descriptions.
- [ ] **35. [writing-for-humans](../skills/software-development/writing-for-humans/SKILL.md)**: Clear conversation and review communication.
- [ ] **36. [unslop](../skills/software-development/unslop/SKILL.md)**: Concrete language and retained useful instructions, including standards shared across projects.

## Full package inventory

Expand each package and account for every file. The checklist above records the human verdict; this inventory makes omissions visible.

<details>
<summary>01. capture: 3 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/capture/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/capture/README.md)
- [agents/openai.yaml](../skills/software-development/capture/agents/openai.yaml)

</details>

<details>
<summary>02. backlog: 8 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/backlog/SKILL.md)

### Instructional references

- [reference/build-waves.md](../skills/software-development/backlog/reference/build-waves.md)
- [reference/labels.md](../skills/software-development/backlog/reference/labels.md)
- [reference/milestones.md](../skills/software-development/backlog/reference/milestones.md)
- [reference/setup.md](../skills/software-development/backlog/reference/setup.md)

### Templates and visual assets

- [templates/environment.md](../skills/software-development/backlog/templates/environment.md)

### Packaging and provenance

- [README.md](../skills/software-development/backlog/README.md)
- [agents/openai.yaml](../skills/software-development/backlog/agents/openai.yaml)

</details>

<details>
<summary>03. shape: 5 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/shape/SKILL.md)

### Instructional references

- [PRODUCT-FORMAT.md](../skills/software-development/shape/PRODUCT-FORMAT.md)
- [reference/revisions.md](../skills/software-development/shape/reference/revisions.md)

### Packaging and provenance

- [README.md](../skills/software-development/shape/README.md)
- [agents/openai.yaml](../skills/software-development/shape/agents/openai.yaml)

</details>

<details>
<summary>04. interview: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/interview/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/interview/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/interview/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/interview/agents/openai.yaml)

</details>

<details>
<summary>05. research: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/research/SKILL.md)

### Instructional references

- [reference/research-contract.md](../skills/software-development/research/reference/research-contract.md)

### Packaging and provenance

- [README.md](../skills/software-development/research/README.md)
- [agents/openai.yaml](../skills/software-development/research/agents/openai.yaml)

</details>

<details>
<summary>06. prototype: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/prototype/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/prototype/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/prototype/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/prototype/agents/openai.yaml)

</details>

<details>
<summary>07. domain-modeling: 6 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/domain-modeling/SKILL.md)

### Instructional references

- [ADR-FORMAT.md](../skills/software-development/domain-modeling/ADR-FORMAT.md)
- [CONTEXT-FORMAT.md](../skills/software-development/domain-modeling/CONTEXT-FORMAT.md)

### Packaging and provenance

- [README.md](../skills/software-development/domain-modeling/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/domain-modeling/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/domain-modeling/agents/openai.yaml)

</details>

<details>
<summary>08. to-spec: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/to-spec/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/to-spec/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/to-spec/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/to-spec/agents/openai.yaml)

</details>

<details>
<summary>09. to-slices: 6 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/to-slices/SKILL.md)

### Instructional references

- [reference/slicing.md](../skills/software-development/to-slices/reference/slicing.md)
- [reference/template-guide.md](../skills/software-development/to-slices/reference/template-guide.md)

### Packaging and provenance

- [README.md](../skills/software-development/to-slices/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/to-slices/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/to-slices/agents/openai.yaml)

</details>

<details>
<summary>10. to-branch: 5 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/to-branch/SKILL.md)

### Executable helpers

- [scripts/to-branch.py](../skills/software-development/to-branch/scripts/to-branch.py)

### Existing tests and fixtures

- [tests/test_to_branch.py](../skills/software-development/to-branch/tests/test_to_branch.py)

### Packaging and provenance

- [README.md](../skills/software-development/to-branch/README.md)
- [agents/openai.yaml](../skills/software-development/to-branch/agents/openai.yaml)

</details>

<details>
<summary>11. deliver: 3 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/deliver/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/deliver/README.md)
- [agents/openai.yaml](../skills/software-development/deliver/agents/openai.yaml)

</details>

<details>
<summary>12. implement: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/implement/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/implement/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/implement/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/implement/agents/openai.yaml)

</details>

<details>
<summary>13. adversarial-review: 5 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/adversarial-review/SKILL.md)

### Instructional references

- [reference/conduct.md](../skills/software-development/adversarial-review/reference/conduct.md)

### Packaging and provenance

- [README.md](../skills/software-development/adversarial-review/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/adversarial-review/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/adversarial-review/agents/openai.yaml)

</details>

<details>
<summary>14. code-review: 6 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/code-review/SKILL.md)

### Instructional references

- [reference/smells.md](../skills/software-development/code-review/reference/smells.md)
- [reference/structure.md](../skills/software-development/code-review/reference/structure.md)

### Packaging and provenance

- [README.md](../skills/software-development/code-review/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/code-review/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/code-review/agents/openai.yaml)

</details>

<details>
<summary>15. verify-your-work: 3 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/verify-your-work/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/verify-your-work/README.md)
- [agents/openai.yaml](../skills/software-development/verify-your-work/agents/openai.yaml)

</details>

<details>
<summary>16. prove-your-work: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/prove-your-work/SKILL.md)

### Instructional references

- [reference/media.md](../skills/software-development/prove-your-work/reference/media.md)

### Packaging and provenance

- [README.md](../skills/software-development/prove-your-work/README.md)
- [agents/openai.yaml](../skills/software-development/prove-your-work/agents/openai.yaml)

</details>

<details>
<summary>17. merge: 3 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/merge/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/merge/README.md)
- [agents/openai.yaml](../skills/software-development/merge/agents/openai.yaml)

</details>

<details>
<summary>18. retro: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/retro/SKILL.md)

### Instructional references

- [reference/checkpoint.md](../skills/software-development/retro/reference/checkpoint.md)

### Packaging and provenance

- [README.md](../skills/software-development/retro/README.md)
- [agents/openai.yaml](../skills/software-development/retro/agents/openai.yaml)

</details>

<details>
<summary>19. handoff: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/handoff/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/handoff/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/handoff/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/handoff/agents/openai.yaml)

</details>

<details>
<summary>20. agent-ready-codebase: 3 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/agent-ready-codebase/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/agent-ready-codebase/README.md)
- [agents/openai.yaml](../skills/software-development/agent-ready-codebase/agents/openai.yaml)

</details>

<details>
<summary>21. to-web: 3 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/to-web/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/to-web/README.md)
- [agents/openai.yaml](../skills/software-development/to-web/agents/openai.yaml)

</details>

<details>
<summary>22. to-thread: 13 files</summary>

### Entrypoint

- [SKILL.md](../skills/system/to-thread/SKILL.md)

### Instructional references

- [reference/claude-cli.md](../skills/system/to-thread/reference/claude-cli.md)
- [reference/claude-desktop.md](../skills/system/to-thread/reference/claude-desktop.md)
- [reference/codex-cli.md](../skills/system/to-thread/reference/codex-cli.md)
- [reference/codex-desktop.md](../skills/system/to-thread/reference/codex-desktop.md)
- [reference/t3.md](../skills/system/to-thread/reference/t3.md)
- [reference/worktrees.md](../skills/system/to-thread/reference/worktrees.md)

### Executable helpers

- [scripts/name-codex-thread.py](../skills/system/to-thread/scripts/name-codex-thread.py)
- [scripts/t3-thread.py](../skills/system/to-thread/scripts/t3-thread.py)

### Existing tests and fixtures

- [evals/test_name_codex_thread.py](../skills/system/to-thread/evals/test_name_codex_thread.py)
- [evals/test_t3_thread.py](../skills/system/to-thread/evals/test_t3_thread.py)

### Packaging and provenance

- [README.md](../skills/system/to-thread/README.md)
- [agents/openai.yaml](../skills/system/to-thread/agents/openai.yaml)

</details>

<details>
<summary>23. to-subagent: 3 files</summary>

### Entrypoint

- [SKILL.md](../skills/system/to-subagent/SKILL.md)

### Packaging and provenance

- [README.md](../skills/system/to-subagent/README.md)
- [agents/openai.yaml](../skills/system/to-subagent/agents/openai.yaml)

</details>

<details>
<summary>24. staffing: 3 files</summary>

### Entrypoint

- [SKILL.md](../skills/system/staffing/SKILL.md)

### Packaging and provenance

- [README.md](../skills/system/staffing/README.md)
- [agents/openai.yaml](../skills/system/staffing/agents/openai.yaml)

</details>

<details>
<summary>25. diagnosing-bugs: 5 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/diagnosing-bugs/SKILL.md)

### Instructional references

- [reference/diagnosis.md](../skills/software-development/diagnosing-bugs/reference/diagnosis.md)

### Packaging and provenance

- [LICENSE](../skills/software-development/diagnosing-bugs/LICENSE)
- [README.md](../skills/software-development/diagnosing-bugs/README.md)
- [agents/openai.yaml](../skills/software-development/diagnosing-bugs/agents/openai.yaml)

</details>

<details>
<summary>26. tdd: 6 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/tdd/SKILL.md)

### Instructional references

- [reference/mocking.md](../skills/software-development/tdd/reference/mocking.md)
- [reference/tests.md](../skills/software-development/tdd/reference/tests.md)

### Packaging and provenance

- [README.md](../skills/software-development/tdd/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/tdd/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/tdd/agents/openai.yaml)

</details>

<details>
<summary>27. principle-codebase-design: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/principle-codebase-design/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/principle-codebase-design/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/principle-codebase-design/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/principle-codebase-design/agents/openai.yaml)

</details>

<details>
<summary>28. principle-experience-first: 3 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/principle-experience-first/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/principle-experience-first/README.md)
- [agents/openai.yaml](../skills/software-development/principle-experience-first/agents/openai.yaml)

</details>

<details>
<summary>29. principle-type-system-discipline: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/principle-type-system-discipline/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/principle-type-system-discipline/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/principle-type-system-discipline/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/principle-type-system-discipline/agents/openai.yaml)

</details>

<details>
<summary>30. typescript-best-practices: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/typescript-best-practices/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/typescript-best-practices/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/typescript-best-practices/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/typescript-best-practices/agents/openai.yaml)

</details>

<details>
<summary>31. bare-minimum-design: 5 files</summary>

### Entrypoint

- [SKILL.md](../skills/creative/bare-minimum-design/SKILL.md)

### Instructional references

- [references/notifications.md](../skills/creative/bare-minimum-design/references/notifications.md)

### Templates and visual assets

- [templates/DESIGN.md](../skills/creative/bare-minimum-design/templates/DESIGN.md)

### Packaging and provenance

- [README.md](../skills/creative/bare-minimum-design/README.md)
- [agents/openai.yaml](../skills/creative/bare-minimum-design/agents/openai.yaml)

</details>

<details>
<summary>32. diagram-design: 210 files</summary>

### Entrypoint

- [SKILL.md](../skills/creative/diagram-design/SKILL.md)

### Instructional references

- [references/animation.md](../skills/creative/diagram-design/references/animation.md)
- [references/doctor.md](../skills/creative/diagram-design/references/doctor.md)
- [references/embedded-output.md](../skills/creative/diagram-design/references/embedded-output.md)
- [references/export.md](../skills/creative/diagram-design/references/export.md)
- [references/import-drawio.md](../skills/creative/diagram-design/references/import-drawio.md)
- [references/import-mermaid.md](../skills/creative/diagram-design/references/import-mermaid.md)
- [references/output-spec.md](../skills/creative/diagram-design/references/output-spec.md)
- [references/primitive-annotation.md](../skills/creative/diagram-design/references/primitive-annotation.md)
- [references/primitive-icons.md](../skills/creative/diagram-design/references/primitive-icons.md)
- [references/primitive-sketchy.md](../skills/creative/diagram-design/references/primitive-sketchy.md)
- [references/primitive-terminal.md](../skills/creative/diagram-design/references/primitive-terminal.md)
- [references/project-design.md](../skills/creative/diagram-design/references/project-design.md)
- [references/semantic-patterns.md](../skills/creative/diagram-design/references/semantic-patterns.md)
- [references/style-guide.md](../skills/creative/diagram-design/references/style-guide.md)
- [references/type-architecture.md](../skills/creative/diagram-design/references/type-architecture.md)
- [references/type-bar.md](../skills/creative/diagram-design/references/type-bar.md)
- [references/type-data-flow.md](../skills/creative/diagram-design/references/type-data-flow.md)
- [references/type-db-schema.md](../skills/creative/diagram-design/references/type-db-schema.md)
- [references/type-dependency.md](../skills/creative/diagram-design/references/type-dependency.md)
- [references/type-deployment.md](../skills/creative/diagram-design/references/type-deployment.md)
- [references/type-dp-integration.md](../skills/creative/diagram-design/references/type-dp-integration.md)
- [references/type-dp-security-matrix.md](../skills/creative/diagram-design/references/type-dp-security-matrix.md)
- [references/type-er.md](../skills/creative/diagram-design/references/type-er.md)
- [references/type-fishbone.md](../skills/creative/diagram-design/references/type-fishbone.md)
- [references/type-flowchart.md](../skills/creative/diagram-design/references/type-flowchart.md)
- [references/type-gantt.md](../skills/creative/diagram-design/references/type-gantt.md)
- [references/type-high-level.md](../skills/creative/diagram-design/references/type-high-level.md)
- [references/type-it-state.md](../skills/creative/diagram-design/references/type-it-state.md)
- [references/type-journey.md](../skills/creative/diagram-design/references/type-journey.md)
- [references/type-kanban.md](../skills/creative/diagram-design/references/type-kanban.md)
- [references/type-layers.md](../skills/creative/diagram-design/references/type-layers.md)
- [references/type-line.md](../skills/creative/diagram-design/references/type-line.md)
- [references/type-loop.md](../skills/creative/diagram-design/references/type-loop.md)
- [references/type-medallion.md](../skills/creative/diagram-design/references/type-medallion.md)
- [references/type-nested.md](../skills/creative/diagram-design/references/type-nested.md)
- [references/type-org-chart.md](../skills/creative/diagram-design/references/type-org-chart.md)
- [references/type-polar.md](../skills/creative/diagram-design/references/type-polar.md)
- [references/type-process.md](../skills/creative/diagram-design/references/type-process.md)
- [references/type-pyramid.md](../skills/creative/diagram-design/references/type-pyramid.md)
- [references/type-quadrant.md](../skills/creative/diagram-design/references/type-quadrant.md)
- [references/type-radar.md](../skills/creative/diagram-design/references/type-radar.md)
- [references/type-sankey.md](../skills/creative/diagram-design/references/type-sankey.md)
- [references/type-scatter.md](../skills/creative/diagram-design/references/type-scatter.md)
- [references/type-sequence.md](../skills/creative/diagram-design/references/type-sequence.md)
- [references/type-state.md](../skills/creative/diagram-design/references/type-state.md)
- [references/type-story-map.md](../skills/creative/diagram-design/references/type-story-map.md)
- [references/type-swimlane.md](../skills/creative/diagram-design/references/type-swimlane.md)
- [references/type-timeline.md](../skills/creative/diagram-design/references/type-timeline.md)
- [references/type-tree.md](../skills/creative/diagram-design/references/type-tree.md)
- [references/type-treemap.md](../skills/creative/diagram-design/references/type-treemap.md)
- [references/type-uml-class.md](../skills/creative/diagram-design/references/type-uml-class.md)
- [references/type-venn.md](../skills/creative/diagram-design/references/type-venn.md)
- [references/type-wardley.md](../skills/creative/diagram-design/references/type-wardley.md)

### Templates and visual assets

- [assets/example-architecture-dark.html](../skills/creative/diagram-design/assets/example-architecture-dark.html)
- [assets/example-architecture-full.html](../skills/creative/diagram-design/assets/example-architecture-full.html)
- [assets/example-architecture.html](../skills/creative/diagram-design/assets/example-architecture.html)
- [assets/example-bar-dark.html](../skills/creative/diagram-design/assets/example-bar-dark.html)
- [assets/example-bar-full.html](../skills/creative/diagram-design/assets/example-bar-full.html)
- [assets/example-bar.html](../skills/creative/diagram-design/assets/example-bar.html)
- [assets/example-bubble-dark.html](../skills/creative/diagram-design/assets/example-bubble-dark.html)
- [assets/example-bubble-full.html](../skills/creative/diagram-design/assets/example-bubble-full.html)
- [assets/example-bubble.html](../skills/creative/diagram-design/assets/example-bubble.html)
- [assets/example-data-flow-dark.html](../skills/creative/diagram-design/assets/example-data-flow-dark.html)
- [assets/example-data-flow-full.html](../skills/creative/diagram-design/assets/example-data-flow-full.html)
- [assets/example-data-flow.html](../skills/creative/diagram-design/assets/example-data-flow.html)
- [assets/example-datalake-dark.html](../skills/creative/diagram-design/assets/example-datalake-dark.html)
- [assets/example-datalake-full.html](../skills/creative/diagram-design/assets/example-datalake-full.html)
- [assets/example-datalake.html](../skills/creative/diagram-design/assets/example-datalake.html)
- [assets/example-db-schema-dark.html](../skills/creative/diagram-design/assets/example-db-schema-dark.html)
- [assets/example-db-schema-full.html](../skills/creative/diagram-design/assets/example-db-schema-full.html)
- [assets/example-db-schema.html](../skills/creative/diagram-design/assets/example-db-schema.html)
- [assets/example-dependency-dark.html](../skills/creative/diagram-design/assets/example-dependency-dark.html)
- [assets/example-dependency-full.html](../skills/creative/diagram-design/assets/example-dependency-full.html)
- [assets/example-dependency.html](../skills/creative/diagram-design/assets/example-dependency.html)
- [assets/example-deployment-dark.html](../skills/creative/diagram-design/assets/example-deployment-dark.html)
- [assets/example-deployment-full.html](../skills/creative/diagram-design/assets/example-deployment-full.html)
- [assets/example-deployment.html](../skills/creative/diagram-design/assets/example-deployment.html)
- [assets/example-dp-integration-dark.html](../skills/creative/diagram-design/assets/example-dp-integration-dark.html)
- [assets/example-dp-integration-full.html](../skills/creative/diagram-design/assets/example-dp-integration-full.html)
- [assets/example-dp-integration.html](../skills/creative/diagram-design/assets/example-dp-integration.html)
- [assets/example-dp-security-matrix-dark.html](../skills/creative/diagram-design/assets/example-dp-security-matrix-dark.html)
- [assets/example-dp-security-matrix-full.html](../skills/creative/diagram-design/assets/example-dp-security-matrix-full.html)
- [assets/example-dp-security-matrix.html](../skills/creative/diagram-design/assets/example-dp-security-matrix.html)
- [assets/example-er-dark.html](../skills/creative/diagram-design/assets/example-er-dark.html)
- [assets/example-er-full.html](../skills/creative/diagram-design/assets/example-er-full.html)
- [assets/example-er.html](../skills/creative/diagram-design/assets/example-er.html)
- [assets/example-fishbone-dark.html](../skills/creative/diagram-design/assets/example-fishbone-dark.html)
- [assets/example-fishbone-full.html](../skills/creative/diagram-design/assets/example-fishbone-full.html)
- [assets/example-fishbone.html](../skills/creative/diagram-design/assets/example-fishbone.html)
- [assets/example-flowchart-dark.html](../skills/creative/diagram-design/assets/example-flowchart-dark.html)
- [assets/example-flowchart-full.html](../skills/creative/diagram-design/assets/example-flowchart-full.html)
- [assets/example-flowchart.html](../skills/creative/diagram-design/assets/example-flowchart.html)
- [assets/example-gantt-dark.html](../skills/creative/diagram-design/assets/example-gantt-dark.html)
- [assets/example-gantt-full.html](../skills/creative/diagram-design/assets/example-gantt-full.html)
- [assets/example-gantt.html](../skills/creative/diagram-design/assets/example-gantt.html)
- [assets/example-high-level-dark.html](../skills/creative/diagram-design/assets/example-high-level-dark.html)
- [assets/example-high-level-full.html](../skills/creative/diagram-design/assets/example-high-level-full.html)
- [assets/example-high-level-vertical-dark.html](../skills/creative/diagram-design/assets/example-high-level-vertical-dark.html)
- [assets/example-high-level-vertical-full.html](../skills/creative/diagram-design/assets/example-high-level-vertical-full.html)
- [assets/example-high-level-vertical.html](../skills/creative/diagram-design/assets/example-high-level-vertical.html)
- [assets/example-high-level.html](../skills/creative/diagram-design/assets/example-high-level.html)
- [assets/example-import-drawio.html](../skills/creative/diagram-design/assets/example-import-drawio.html)
- [assets/example-import-mermaid.html](../skills/creative/diagram-design/assets/example-import-mermaid.html)
- [assets/example-it-state-dark.html](../skills/creative/diagram-design/assets/example-it-state-dark.html)
- [assets/example-it-state-full.html](../skills/creative/diagram-design/assets/example-it-state-full.html)
- [assets/example-it-state.html](../skills/creative/diagram-design/assets/example-it-state.html)
- [assets/example-journey-dark.html](../skills/creative/diagram-design/assets/example-journey-dark.html)
- [assets/example-journey-full.html](../skills/creative/diagram-design/assets/example-journey-full.html)
- [assets/example-journey.html](../skills/creative/diagram-design/assets/example-journey.html)
- [assets/example-kanban-dark.html](../skills/creative/diagram-design/assets/example-kanban-dark.html)
- [assets/example-kanban-full.html](../skills/creative/diagram-design/assets/example-kanban-full.html)
- [assets/example-kanban.html](../skills/creative/diagram-design/assets/example-kanban.html)
- [assets/example-layers-dark.html](../skills/creative/diagram-design/assets/example-layers-dark.html)
- [assets/example-layers-full.html](../skills/creative/diagram-design/assets/example-layers-full.html)
- [assets/example-layers.html](../skills/creative/diagram-design/assets/example-layers.html)
- [assets/example-line-dark.html](../skills/creative/diagram-design/assets/example-line-dark.html)
- [assets/example-line-full.html](../skills/creative/diagram-design/assets/example-line-full.html)
- [assets/example-line.html](../skills/creative/diagram-design/assets/example-line.html)
- [assets/example-loop-dark.html](../skills/creative/diagram-design/assets/example-loop-dark.html)
- [assets/example-loop-full.html](../skills/creative/diagram-design/assets/example-loop-full.html)
- [assets/example-loop-terminal.html](../skills/creative/diagram-design/assets/example-loop-terminal.html)
- [assets/example-loop.html](../skills/creative/diagram-design/assets/example-loop.html)
- [assets/example-medallion-dark.html](../skills/creative/diagram-design/assets/example-medallion-dark.html)
- [assets/example-medallion-full.html](../skills/creative/diagram-design/assets/example-medallion-full.html)
- [assets/example-medallion.html](../skills/creative/diagram-design/assets/example-medallion.html)
- [assets/example-nested-dark.html](../skills/creative/diagram-design/assets/example-nested-dark.html)
- [assets/example-nested-full.html](../skills/creative/diagram-design/assets/example-nested-full.html)
- [assets/example-nested.html](../skills/creative/diagram-design/assets/example-nested.html)
- [assets/example-org-chart-dark.html](../skills/creative/diagram-design/assets/example-org-chart-dark.html)
- [assets/example-org-chart-full.html](../skills/creative/diagram-design/assets/example-org-chart-full.html)
- [assets/example-org-chart.html](../skills/creative/diagram-design/assets/example-org-chart.html)
- [assets/example-paved-road-animated.html](../skills/creative/diagram-design/assets/example-paved-road-animated.html)
- [assets/example-polar-dark.html](../skills/creative/diagram-design/assets/example-polar-dark.html)
- [assets/example-polar-full.html](../skills/creative/diagram-design/assets/example-polar-full.html)
- [assets/example-polar.html](../skills/creative/diagram-design/assets/example-polar.html)
- [assets/example-policy-trace-animated.html](../skills/creative/diagram-design/assets/example-policy-trace-animated.html)
- [assets/example-process-dark.html](../skills/creative/diagram-design/assets/example-process-dark.html)
- [assets/example-process-full.html](../skills/creative/diagram-design/assets/example-process-full.html)
- [assets/example-process.html](../skills/creative/diagram-design/assets/example-process.html)
- [assets/example-pyramid-dark.html](../skills/creative/diagram-design/assets/example-pyramid-dark.html)
- [assets/example-pyramid-full.html](../skills/creative/diagram-design/assets/example-pyramid-full.html)
- [assets/example-pyramid.html](../skills/creative/diagram-design/assets/example-pyramid.html)
- [assets/example-quadrant-consultant.html](../skills/creative/diagram-design/assets/example-quadrant-consultant.html)
- [assets/example-quadrant-dark.html](../skills/creative/diagram-design/assets/example-quadrant-dark.html)
- [assets/example-quadrant-full.html](../skills/creative/diagram-design/assets/example-quadrant-full.html)
- [assets/example-quadrant.html](../skills/creative/diagram-design/assets/example-quadrant.html)
- [assets/example-queue-animated.html](../skills/creative/diagram-design/assets/example-queue-animated.html)
- [assets/example-radar-dark.html](../skills/creative/diagram-design/assets/example-radar-dark.html)
- [assets/example-radar-full.html](../skills/creative/diagram-design/assets/example-radar-full.html)
- [assets/example-radar.html](../skills/creative/diagram-design/assets/example-radar.html)
- [assets/example-ridgeline-dark.html](../skills/creative/diagram-design/assets/example-ridgeline-dark.html)
- [assets/example-ridgeline-full.html](../skills/creative/diagram-design/assets/example-ridgeline-full.html)
- [assets/example-ridgeline.html](../skills/creative/diagram-design/assets/example-ridgeline.html)
- [assets/example-sankey-dark.html](../skills/creative/diagram-design/assets/example-sankey-dark.html)
- [assets/example-sankey-full.html](../skills/creative/diagram-design/assets/example-sankey-full.html)
- [assets/example-sankey.html](../skills/creative/diagram-design/assets/example-sankey.html)
- [assets/example-scatter-dark.html](../skills/creative/diagram-design/assets/example-scatter-dark.html)
- [assets/example-scatter-full.html](../skills/creative/diagram-design/assets/example-scatter-full.html)
- [assets/example-scatter.html](../skills/creative/diagram-design/assets/example-scatter.html)
- [assets/example-sequence-dark.html](../skills/creative/diagram-design/assets/example-sequence-dark.html)
- [assets/example-sequence-full.html](../skills/creative/diagram-design/assets/example-sequence-full.html)
- [assets/example-sequence-oauth-dark.html](../skills/creative/diagram-design/assets/example-sequence-oauth-dark.html)
- [assets/example-sequence-oauth-full.html](../skills/creative/diagram-design/assets/example-sequence-oauth-full.html)
- [assets/example-sequence-oauth.html](../skills/creative/diagram-design/assets/example-sequence-oauth.html)
- [assets/example-sequence.html](../skills/creative/diagram-design/assets/example-sequence.html)
- [assets/example-slopegraph-dark.html](../skills/creative/diagram-design/assets/example-slopegraph-dark.html)
- [assets/example-slopegraph-full.html](../skills/creative/diagram-design/assets/example-slopegraph-full.html)
- [assets/example-slopegraph.html](../skills/creative/diagram-design/assets/example-slopegraph.html)
- [assets/example-state-dark.html](../skills/creative/diagram-design/assets/example-state-dark.html)
- [assets/example-state-full.html](../skills/creative/diagram-design/assets/example-state-full.html)
- [assets/example-state.html](../skills/creative/diagram-design/assets/example-state.html)
- [assets/example-story-map-dark.html](../skills/creative/diagram-design/assets/example-story-map-dark.html)
- [assets/example-story-map-full.html](../skills/creative/diagram-design/assets/example-story-map-full.html)
- [assets/example-story-map.html](../skills/creative/diagram-design/assets/example-story-map.html)
- [assets/example-swimlane-dark.html](../skills/creative/diagram-design/assets/example-swimlane-dark.html)
- [assets/example-swimlane-full.html](../skills/creative/diagram-design/assets/example-swimlane-full.html)
- [assets/example-swimlane.html](../skills/creative/diagram-design/assets/example-swimlane.html)
- [assets/example-timeline-dark.html](../skills/creative/diagram-design/assets/example-timeline-dark.html)
- [assets/example-timeline-full.html](../skills/creative/diagram-design/assets/example-timeline-full.html)
- [assets/example-timeline.html](../skills/creative/diagram-design/assets/example-timeline.html)
- [assets/example-tree-dark.html](../skills/creative/diagram-design/assets/example-tree-dark.html)
- [assets/example-tree-full.html](../skills/creative/diagram-design/assets/example-tree-full.html)
- [assets/example-tree.html](../skills/creative/diagram-design/assets/example-tree.html)
- [assets/example-treemap-dark.html](../skills/creative/diagram-design/assets/example-treemap-dark.html)
- [assets/example-treemap-full.html](../skills/creative/diagram-design/assets/example-treemap-full.html)
- [assets/example-treemap.html](../skills/creative/diagram-design/assets/example-treemap.html)
- [assets/example-uml-class-dark.html](../skills/creative/diagram-design/assets/example-uml-class-dark.html)
- [assets/example-uml-class-full.html](../skills/creative/diagram-design/assets/example-uml-class-full.html)
- [assets/example-uml-class.html](../skills/creative/diagram-design/assets/example-uml-class.html)
- [assets/example-venn-dark.html](../skills/creative/diagram-design/assets/example-venn-dark.html)
- [assets/example-venn-full.html](../skills/creative/diagram-design/assets/example-venn-full.html)
- [assets/example-venn.html](../skills/creative/diagram-design/assets/example-venn.html)
- [assets/example-wardley-dark.html](../skills/creative/diagram-design/assets/example-wardley-dark.html)
- [assets/example-wardley-full.html](../skills/creative/diagram-design/assets/example-wardley-full.html)
- [assets/example-wardley.html](../skills/creative/diagram-design/assets/example-wardley.html)
- [assets/icons.html](../skills/creative/diagram-design/assets/icons.html)
- [assets/index.html](../skills/creative/diagram-design/assets/index.html)
- [assets/template-full.html](../skills/creative/diagram-design/assets/template-full.html)
- [assets/template-light.html](../skills/creative/diagram-design/assets/template-light.html)
- [assets/template-motion.html](../skills/creative/diagram-design/assets/template-motion.html)
- [assets/template-terminal.html](../skills/creative/diagram-design/assets/template-terminal.html)
- [assets/template.html](../skills/creative/diagram-design/assets/template.html)

### Executable helpers

- [scripts/drawio_extract.py](../skills/creative/diagram-design/scripts/drawio_extract.py)
- [scripts/mermaid_extract.py](../skills/creative/diagram-design/scripts/mermaid_extract.py)
- [scripts/self_check.py](../skills/creative/diagram-design/scripts/self_check.py)

### Packaging and provenance

- [LICENSE](../skills/creative/diagram-design/LICENSE)
- [README.md](../skills/creative/diagram-design/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/creative/diagram-design/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/creative/diagram-design/agents/openai.yaml)

</details>

<details>
<summary>33. codex-imagegen: 22 files</summary>

### Entrypoint

- [SKILL.md](../skills/creative/codex-imagegen/SKILL.md)

### Instructional references

- [reference/api-key-path.md](../skills/creative/codex-imagegen/reference/api-key-path.md)
- [reference/backends.md](../skills/creative/codex-imagegen/reference/backends.md)
- [reference/layered-mode.md](../skills/creative/codex-imagegen/reference/layered-mode.md)
- [reference/spritesheet-manifest.md](../skills/creative/codex-imagegen/reference/spritesheet-manifest.md)
- [reference/spritesheet-prompts.md](../skills/creative/codex-imagegen/reference/spritesheet-prompts.md)
- [reference/spritesheet-slicing.md](../skills/creative/codex-imagegen/reference/spritesheet-slicing.md)
- [reference/spritesheet-validation.md](../skills/creative/codex-imagegen/reference/spritesheet-validation.md)

### Executable helpers

- [scripts/chroma_key.py](../skills/creative/codex-imagegen/scripts/chroma_key.py)
- [scripts/codex_imagegen.py](../skills/creative/codex-imagegen/scripts/codex_imagegen.py)
- [scripts/extract_spritesheet.py](../skills/creative/codex-imagegen/scripts/extract_spritesheet.py)
- [scripts/image_backends.py](../skills/creative/codex-imagegen/scripts/image_backends.py)
- [scripts/image_key.py](../skills/creative/codex-imagegen/scripts/image_key.py)
- [scripts/output_paths.py](../skills/creative/codex-imagegen/scripts/output_paths.py)

### Existing tests and fixtures

- [evals/spritesheet-fixtures/iso-4x4.png](../skills/creative/codex-imagegen/evals/spritesheet-fixtures/iso-4x4.png)
- [evals/spritesheet_make_fixture.py](../skills/creative/codex-imagegen/evals/spritesheet_make_fixture.py)
- [evals/spritesheet_selfcheck.py](../skills/creative/codex-imagegen/evals/spritesheet_selfcheck.py)
- [evals/versioning_dryrun.py](../skills/creative/codex-imagegen/evals/versioning_dryrun.py)
- [tests/test_backends.py](../skills/creative/codex-imagegen/tests/test_backends.py)

### Packaging and provenance

- [README.md](../skills/creative/codex-imagegen/README.md)
- [agents/openai.yaml](../skills/creative/codex-imagegen/agents/openai.yaml)
- [requirements.txt](../skills/creative/codex-imagegen/requirements.txt)

</details>

<details>
<summary>34. technical-writing: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/technical-writing/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/technical-writing/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/technical-writing/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/technical-writing/agents/openai.yaml)

</details>

<details>
<summary>35. writing-for-humans: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/writing-for-humans/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/writing-for-humans/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/writing-for-humans/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/writing-for-humans/agents/openai.yaml)

</details>

<details>
<summary>36. unslop: 4 files</summary>

### Entrypoint

- [SKILL.md](../skills/software-development/unslop/SKILL.md)

### Packaging and provenance

- [README.md](../skills/software-development/unslop/README.md)
- [THIRD_PARTY_LICENSES.md](../skills/software-development/unslop/THIRD_PARTY_LICENSES.md)
- [agents/openai.yaml](../skills/software-development/unslop/agents/openai.yaml)

</details>

## Cross-skill review

After the package review, trace these journeys through the sources. Record contradictions or missing ownership at each handoff.

- A user-testing batch becomes milestone issues; duplicates consolidate across batches; a shaped issue splits and retains its milestone.
- A clear bug skips shaping, is built and verified in its worktree, and reaches an ordinary PR for human selection.
- Shaping pauses on one machine and resumes on another from the pushed branch, ticket, and published artifacts.
- A spec splits into blocked and independent children, integrates their PRs, passes whole-spec verification, and promotes to base.
- A high-risk build receives independent verification, encounters a defect, refreshes both verdicts, and preserves its remaining review budget.
- A worker fails during dispatch; later status recovers ownership without duplicating a live build or moving the primary checkout.
- A reviewed merge cleans up finished branches and worktrees while preserving active work and published artifacts.
- Retro revisits updated sessions, matches existing issues, accepts user dismissals, and advances only through reviewed work.

## Evidence and sign-off

**Manual review is pending.** Completion means all 36 skills and their package files have a recorded verdict, cross-skill gaps have an owner, and required changes are resolved or explicitly deferred.

Packaging, dependency closure, links, formatting, and rendered-guide checks establish structural consistency. They do not establish lifecycle behavior. The image backend has 22 passing implementation tests and a visually inspected live proxy smoke, recorded in [the instruction review](skill-instruction-review.md). Other tests listed in the inventory are existing assets; inclusion does not claim a current passing run.

The user selected real repository work for behavioral assessment. Observe actual lifecycle outcomes after installation and reconciliation; synthetic agent fixtures are no longer a rollout gate. Helper regressions remain useful for concrete code defects.

The September 5 rewrite snapshot fell from 24,788 to 15,492 o200k_base tokens (37.5%) against 516f0c6. That historical entrypoint measurement excludes references and design siblings; the current review covers the full packages.

Family scope comes from the [README install set](../README.md#install). Authoring-only `skill-loop` and unrelated creative, thinking, and personal packages are outside this family. [Writing for Agents](../.agents/skills/writing-for-agents/SKILL.md) remains guidance for reviewing instruction quality.
