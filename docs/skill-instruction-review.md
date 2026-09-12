# Skill instruction review

## Simplification review

Reviewed the shipped helper inventory and the setup, dispatch, verification, and diagram instructions that use it. This is an editorial assessment; these recommendations have no behavioral eval results yet. Prefer a compact instruction for occasional work the agent can derive from available tools. A helper earns its maintenance when it handles a repeated transformation, fragile protocol, or exact state transition.

### Applied: label setup

Removed the 102-line label reconciler, including its rename, color, and description override interface. The fixed nine-label scheme is now a [table](../skills/software-development/backlog/reference/labels.md#label-appearance). [Setup](../skills/software-development/backlog/reference/setup.md) compares repository labels, presents changes, applies the approved plan, and reads back the result while preserving unrelated labels. Names, colors, and workflow meanings remain; descriptions are shorter. No live tracker labels were changed.

### Further candidates, in review order

| Where | Unnecessary machinery | Proposed replacement |
| --- | --- | --- |
| [Environment template](../skills/software-development/backlog/templates/environment.md) | Copies family policy into every consumer repo: PR rules, continuity, the five readiness definitions, verification categories, and media rules. Each copy can drift as skills change. | Keep project facts, capability results, exceptions, and command/configuration pointers. Let the skills own the general workflow. Retain headings consumed by the family and evidence that readiness was demonstrated. |
| [UI verification](../skills/software-development/verify-your-work/SKILL.md#check-each-claim) and the environment template | Every UI journey requires a script, and the template fixes Playwright driving Chrome. This forces temporary code even when a browser tool can directly exercise a small change. | Let the agent choose the available browser driver. Require reproducible steps, fixtures, observed results, and captures. Use scripts for repetition, complex setup, or durable regression coverage; preserve any scripts used. This changes the verification contract, so review it explicitly. |
| [T3 dispatch reference](../skills/system/to-thread/reference/t3.md) | Narrates helper internals: runtime discovery, payload creation, error formatting, and compensating deletion. The implementation already owns those mechanics. | Keep the invocation, inputs the agent must resolve, known provider traps, observed liveness, model/effort confirmation, and recovery obligations. Let helper errors describe failed operations and orphan IDs. Keep the protocol helper. |
| [Diagram description](../skills/creative/diagram-design/SKILL.md) | Lists all 39 visual types in the always-loaded description, then repeats the catalog in the body. Every session pays for the full enumeration. | Use a short trigger covering diagrams, charts, visual explanations, and redraws of Mermaid/draw.io sources. Keep detailed selection in the body. Check invocation coverage when evals begin. |
| [Diagram planning pause](../skills/creative/diagram-design/SKILL.md#confirm-before-drawing) | Requires a plan and an opportunity to redirect unless type, mode, size, and content are all specified. Routine visual work inherits another interaction step. | Choose reasonable defaults and draw. Ask when a missing decision materially affects the result. Preserve the user's chosen design, size, and content. |
| [Relay setup discovery](../skills/personal/relay/scripts/setup_instance.py), outside the family | A one-time discovery engine guesses source files from filename keywords, caps traversal and results, and writes a discovery report. The agent still has to interpret the guesses. | Let the agent inspect the repo and propose explicit bindings. Retain consumer-edit preservation, credential handling, validation, and exact delivery approval. Evaluate the discovery portion separately from the rest of the 220-line setup helper. |

The strongest next edits are the environment template, T3 narration, and diagram description. Browser verification and the diagram pause change how work runs; the table makes those choices visible for manual review. Relay is a separate package and a lower priority for this family.

### Helpers that earn their place

- [to-branch](../skills/software-development/to-branch/scripts/to-branch.py): isolates Git's index and checks the expected ref while publishing artifact history. That supports the stable-checkout contract.
- [T3 dispatch](../skills/system/to-thread/scripts/t3-thread.py) and [Codex naming](../skills/system/to-thread/scripts/name-codex-thread.py): implement protocol handshakes and process handling. Occasional use alone is insufficient reason to replace fragile protocol code with prose.
- Image decoding, sprite extraction, chroma keying, diagram import parsers, and video contact sheets: perform transformations the agent would otherwise have to reimplement.
- Relay approval hashes, validation, and delivery state: bind approval to exact recipients and content and support delivery recovery. Keep those guarantees.

Retro's small local cursor and dispatch ownership also have concrete jobs: bounded coverage and avoiding duplicate workers. Neither needs a new framework. The diagram checker had one stale docstring naming unshipped tools; that text was corrected in this pass.

## Skill boundaries: cross-package paths removed

A scan of all 47 authored skill packages found five runtime cross-package file links: three in capture's entrypoint and README, and two in to-slices' slicing reference. Each reached into backlog's internal milestone or dependency references. The steps now state their own publication outcomes, preserving native relationships, milestone inheritance, conflicting-assignment approval, and migration readback.

Sibling composition uses skill names. Each skill owns access to its internal files. Local package references and provenance citations remain; the full review inventory links source files for human inspection. The boundary is recorded in SKILL-MECHANICS.md.

## Milestones: testing batches

Requested testing batches now use milestones. Capture keeps one issue per finding; groom preserves membership during consolidation and checks linked replacement work before proposing closure. Approved splits inherit the milestone while retaining their spec integration branches. [The milestone contract](../skills/software-development/backlog/reference/milestones.md) owns the rules, including migration from organizational parents.

## Retro: updated after review

Retro now sweeps recent local build and shaping transcripts and offers project issues or comments for user selection. An ignored `.retro/checkpoint.json` in the primary checkout tracks coverage. The ledger, upstream workflow, denylists, and setup playbook are retired. The earlier pass descriptions below record the contracts reviewed at that time; [retro](../skills/software-development/retro/SKILL.md) and its [checkpoint reference](../skills/software-development/retro/reference/checkpoint.md) describe the current behavior.

## Negations: applied

Four reviewers and the owning session reviewed all 47 authored skills and their instructional references. The pass changed 43 packages, removing about 3,400 o200k_base tokens across Markdown sources. The comparison starts from the working files at the beginning of this pass, preserving the existing user edit to `to-web`.

| Before | Result |
| --- | --- |
| “Re-ask nothing it settles” | “Carry settled answers forward” |
| “Never modify the spec text” | “Preserve the source spec verbatim” |
| “Compilation alone proves no behavior” | “Use runtime checks for behavioral claims” |
| Enumerate decorative ideas, then forbid them | Removed from shadixfy and maquette |
| Require verified upload, then warn that command success is insufficient | Kept the positive verification requirement |
| Repeated bans on upstream submission | Kept exact-text approval for each submission and setup consent for proposals |

Concrete boundaries remain: ordinary PRs, fixed revisions during checking, truthful verification verdicts, evidence media outside Git, stable primary checkouts, confirmed worker stops, bounded review loops, human merge selection, and private/approved external feedback. Useful counterexamples and programming-language `never` also remain.

A second review checked the lifecycle and system/support edits for changed behavior. It caught and corrected a verification-model routing contradiction and an unnecessary new file-count check. Packaging, invocation metadata, dependency closure, local links, and formatting were checked. This is an editorial review, not a behavioral eval.

## Command recipes: applied

All 47 packages were reviewed again for mechanics the agent can derive from the environment. The approved pass replaces ordinary command recipes with completion criteria and pointers to the environment.

| Priority | Source | Applied change | Essential detail to retain |
| --- | --- | --- | --- |
| High | [merge](../skills/software-development/merge/SKILL.md) | Replace the check-watching command sequence with a required-check outcome | All required checks pass, bounded waiting, current head/base, atomic expected-head merge |
| High | [capture](../skills/software-development/capture/SKILL.md), [slicing](../skills/software-development/to-slices/reference/slicing.md), [labels](../skills/software-development/backlog/reference/labels.md) | Remove repeated GitHub API and POST recipes | Sub-issue navigation and blocking are separate native relations; verify both |
| High | [code review](../skills/software-development/code-review/SKILL.md) | Replace generic diff, log, and issue-read commands with review inputs | Pinned revisions, merge-base comparison, comments, approved spec, uncommitted snapshot handling |
| High | [worktree preparation](../skills/system/to-thread/reference/worktrees.md) | Let the agent choose native Git commands | Reuse local or remote history before creating a branch; preserve primary checkout and existing work |
| High | [diagram export](../skills/creative/diagram-design/references/export.md) | Replace copied rasterization and regex-extraction recipes with export criteria | Font/static-frame readiness, valid standalone SVG, accessible metadata, measured dimensions, inspected output |
| Medium | [maquette architecture](../skills/creative/maquette/references/architecture.md) | Remove generic scaffolding recipes and copied implementation code | Approved stack, shared demo state, typed mutation boundary, acknowledged agent actions |
| Medium | [to-branch](../skills/software-development/to-branch/SKILL.md) | Remove narration of the bundled script's Git algorithm | Helper pointer, inputs/output, unchanged checkout/index/files, remote-history prerequisite |
| Medium | [TDD](../skills/software-development/tdd/SKILL.md) | Replace prescribed stashing with a red/green outcome | Same regression check fails before the change and passes after; preserve existing work |
| Medium | [relay runtime](../skills/personal/relay/reference/rich-email-contract.md), [learning schedule](../skills/personal/learn-anything/reference/scheduling.md) | Point to canonical manifests/templates instead of copying versions or schemas | Runtime readiness and scheduling semantics |

The old export recipe described fractional scaling but parsed it as an integer. It now requires measured output dimensions. Browser readiness now requires a launch and capture probe.

Keep bundled tool interfaces, genuine harness traps, literal state/schema interfaces, safety-critical atomic options, and commands recorded from an actual verification run. Label colors and descriptions now live in the reconciler; the Markdown reference owns lifecycle semantics and native relationships.

## Staffing: applied

The approved roster follows the user's assessment of Astra and Fable 5.1. The canonical assignments live in [staffing](../skills/system/staffing/SKILL.md).

| Work | Model | Effort |
| --- | --- | --- |
| Planning, shaping, orchestration, architecture | `gpt-6-astra` | High |
| Implementation, debugging, refactoring, code review | `gpt-6-astra` | High |
| Taste, front-end design and implementation, visual critique, copy | `claude-fable-5-1` | High |
| Research synthesis and difficult fact-checking | `gpt-6-astra` | High |
| Bounded source collection, browser driving and capture | `gpt-5.6-terra` | High |
| Independent behavioral verification | `gpt-6-astra`, fresh context | High |
| Image generation | `gpt-image-2` | Unchanged |

`claude-fable-5` is retired; Sol and Opus are removed from default assignments. GPT workers use the Codex route; Fable uses the Claude route. User-selected models and harnesses take precedence. Independent review and high-risk verification use fresh contexts; model diversity is an optional additional check. Routine stages remain with the owner, and staffing applies when a separate worker is warranted.

## Image backend: implemented and checked

[Issue #208](https://github.com/asasher/asher-skills/issues/208) adds CLIProxyAPI Images API support to the shipped `codex-imagegen` scripts. Backend priority is configured CLIProxyAPI, native Codex, then direct OpenAI API with an available Platform key and explicit user permission. Selection happens before generation; failures stop the run.

Flat, batch, layered, and generated spritesheet modes share the backend. Output versions and partial layers survive failures. Inferred credentials stay bound to their configured endpoint, redirects are rejected, and errors omit secrets. The native route uses the bundled adapter; the external system-skill CLI dependency is removed.

Validation on September 6:

- All 22 local backend tests pass, covering credential routing, direct-API permission, malformed responses, fail-stop batches, dimensions, immutable versions, partial layers, sprites, and native extraction.
- A live CLIProxyAPI request used `gpt-image-2`, low quality, and requested 1024 × 1024. The decoded image was 1254 × 1254; the adapter reported the mismatch and preserved those dimensions.
- Visual inspection confirmed the requested blue ceramic robot holding an orange flower, fully framed on the magenta key background. The raw smoke artifact stays outside Git. Transparency removal was outside this smoke's scope.
- Live native and direct-API requests were not run. Their local tests do not establish service availability. No new behavioral skill evals were added.

Review found and fixed two bugs before the live request: inferred keys could cross endpoint boundaries, and trailing-dot Platform hostnames could bypass gateway classification. Regression tests cover both.
