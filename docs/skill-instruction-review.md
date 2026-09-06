# Skill instruction review

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
