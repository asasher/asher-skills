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

## Command recipes: findings for the next pass

All 47 packages were reviewed again for mechanics the agent can derive from the environment. These are identified candidates; this command-recipe pass has not yet changed the skills.

| Priority | Source | Candidate change | Essential detail to retain |
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

The export recipe illustrates why copied implementations go stale: it documents fractional scaling while its Python snippet parses scale as an integer. Its readiness recipe also treats CLI-help availability as a possible browser-presence check. These deserve outcome-based instructions and actual artifact verification.

Keep bundled tool interfaces, genuine harness traps, literal state/schema interfaces, safety-critical atomic options, and commands recorded from an actual verification run. The label table also needs a deliberate single-source change: the reconciler currently calls the Markdown table authoritative, so deleting the table alone would leave an inconsistent contract.

## Proposed staffing

This is a proposal based on the user's assessment of Astra and Fable 5.1; model assignments have not yet been changed.

| Work | Model | Effort |
| --- | --- | --- |
| Planning, shaping, orchestration, architecture | `gpt-6-astra` | High |
| Implementation, debugging, refactoring, code review | `gpt-6-astra` | High |
| Taste, front-end design and implementation, visual critique, copy | `claude-fable-5-1` | High |
| Research synthesis and difficult fact-checking | `gpt-6-astra` | High |
| Bounded source collection, browser driving and capture | `gpt-5.6-terra` | High |
| Independent behavioral verification | `gpt-6-astra`, fresh context | High |
| Image generation | `gpt-image-2` | Unchanged |

Retire `claude-fable-5`; remove Sol and Opus from default assignments. GPT workers use the Codex route; Fable uses the Claude route. User-selected models and harnesses take precedence. Independent review and high-risk verification use fresh contexts; model diversity is an optional additional check. Routine stages remain with the owner, and staffing applies when a separate worker is warranted.
