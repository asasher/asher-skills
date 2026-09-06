# Software development family: manual review

Start with [the visual guide](software-development.html). The sources below are the rewritten contracts, not evaluated behavior. Review each group in order; note the skill and exact sentence you would change.

## 1. Groom and route

Does groom read everything, consolidate deliberately, and send only clear work straight to ready?

[backlog](../skills/software-development/backlog/SKILL.md) → [capture](../skills/software-development/capture/SKILL.md)

## 2. Prepare and dispatch

Can a new machine attach existing work without disturbing the primary checkout? Is the bucket a real readiness requirement?

[agent-ready-codebase](../skills/software-development/agent-ready-codebase/SKILL.md) → [to-web](../skills/software-development/to-web/SKILL.md) → [to-thread](../skills/system/to-thread/SKILL.md) → [to-subagent](../skills/system/to-subagent/SKILL.md) → [staffing](../skills/system/staffing/SKILL.md)

## 3. Shape one ticket

Are decisions, artifacts, approval, context commits, and split release each owned by one place?

[shape](../skills/software-development/shape/SKILL.md) → [interview](../skills/software-development/interview/SKILL.md) → [research](../skills/software-development/research/SKILL.md) → [prototype](../skills/software-development/prototype/SKILL.md) → [domain-modeling](../skills/software-development/domain-modeling/SKILL.md) → [to-spec](../skills/software-development/to-spec/SKILL.md) → [to-branch](../skills/software-development/to-branch/SKILL.md) → [to-slices](../skills/software-development/to-slices/SKILL.md)

## 4. Build and prove

Can the owner finish routine work while independent checks and current evidence still gate readiness?

[deliver](../skills/software-development/deliver/SKILL.md) → [implement](../skills/software-development/implement/SKILL.md) → [adversarial-review](../skills/software-development/adversarial-review/SKILL.md) → [code-review](../skills/software-development/code-review/SKILL.md) → [verify-your-work](../skills/software-development/verify-your-work/SKILL.md) → [prove-your-work](../skills/software-development/prove-your-work/SKILL.md)

## 5. Merge and learn

Are merge selection, safe cleanup, recovery, and user-selected retro issues clear? Handoff supports a pause when a context transfer is needed.

[merge](../skills/software-development/merge/SKILL.md) → [retro](../skills/software-development/retro/SKILL.md) → [handoff](../skills/software-development/handoff/SKILL.md)

## 6. Supporting standards

Do the reusable standards add guidance without duplicating the lifecycle? Review the positive instructions alongside the concrete safeguards that remain.

[diagnosing-bugs](../skills/software-development/diagnosing-bugs/SKILL.md) → [tdd](../skills/software-development/tdd/SKILL.md) → [principle-codebase-design](../skills/software-development/principle-codebase-design/SKILL.md) → [principle-experience-first](../skills/software-development/principle-experience-first/SKILL.md) → [principle-type-system-discipline](../skills/software-development/principle-type-system-discipline/SKILL.md) → [typescript-best-practices](../skills/software-development/typescript-best-practices/SKILL.md) → [bare-minimum-design](../skills/creative/bare-minimum-design/SKILL.md) → [diagram-design](../skills/creative/diagram-design/SKILL.md) → [codex-imagegen](../skills/creative/codex-imagegen/SKILL.md) → [technical-writing](../skills/software-development/technical-writing/SKILL.md) → [writing-for-humans](../skills/software-development/writing-for-humans/SKILL.md) → [unslop](../skills/software-development/unslop/SKILL.md)

## References worth reading

- Setup: [environment template](../skills/software-development/backlog/templates/environment.md), [labels and claims](../skills/software-development/backlog/reference/labels.md).
- Images: [backend selection and credentials](../skills/creative/codex-imagegen/reference/backends.md).
- Dispatch: [native worktree preparation](../skills/system/to-thread/reference/worktrees.md), then only the harness route you use.
- Splits: [publication and readback](../skills/software-development/to-slices/reference/slicing.md).
- Retro: [local checkpoint and bounded coverage](../skills/software-development/retro/reference/checkpoint.md).

## Validation boundary

The September 5 rewrite snapshot fell from 24,788 to 15,492 o200k_base tokens (37.5%) against 516f0c6. Scope: 34 prior SDLC/system entrypoints versus 33 current, full SKILL.md including frontmatter; excludes references and design siblings. Some conditional detail moved into references, so this measures entrypoint load, not every possible execution path.

Packaging, dependency closure, local links, formatting, and rendered-document checks establish structural consistency. No skill evals were added for this rewrite. The image backend has 22 implementation tests and a visually inspected live proxy smoke; see the instruction review for scope and limits. The visual guide lists candidate fixtures and human judgments for evaluation design during this review.

## September 6 instruction review

See [the instruction review](skill-instruction-review.md) for the completed negation cleanup, applied command simplifications, image backend routing, and current staffing roster. The six review groups above still follow the current lifecycle contracts.
