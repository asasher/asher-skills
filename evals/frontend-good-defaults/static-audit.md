# Static Baseline Audit

This is a source-level audit of `skills/frontend-good-defaults/SKILL.md` against the two baselines. It does not replace output-quality evals; use `evals.json` and `runbook.md` for iteration runs.

## Baseline Summary

Uncodixfy is strongest as a reset. It aggressively blocks common AI UI failure modes: floating cards, oversized radii, glass panels, decorative labels, generic dark SaaS composition, fake charts, gradient-heavy dashboards, and ornamental copy. Its weakness is that it mostly says what not to do; it gives fewer constructive mechanics for hierarchy, typography, layout, imagery, states, and verification.

OpenAI's frontend skill is strongest for visually led work. It emphasizes composition, full-bleed heroes, brand-first hierarchy, image-led storytelling, section narrative, restrained copy, and intentional motion. Its weakness for this use case is that it is less of a hard reset for internal product UI and gives fewer low-level mechanics for app surfaces, data layout, typography, color systems, empty states, and anti-Codex defaults.

Frontend Good Defaults intentionally merges both roles: reset first, then constructive defaults.

## Coverage Matrix

| Dimension | Uncodixfy | OpenAI frontend skill | Frontend Good Defaults |
|---|---:|---:|---:|
| Anti-AI UI reset | Strong | Medium | Strong |
| Normal app/workspace defaults | Strong | Medium | Strong |
| Landing page composition | Medium | Strong | Strong |
| Image-led hierarchy | Low | Strong | Strong |
| Product utility copy | Medium | Strong | Strong |
| Refactoring UI mechanics | Low | Low | Strong |
| Typography specifics | Medium | Low | Strong |
| Spacing/layout systems | Medium | Medium | Strong |
| Color/shade systems | Medium | Medium | Strong |
| Component-level defaults | Strong | Low | Strong |
| Empty/loading/error states | Low | Low | Strong |
| Verification discipline | Low | Low | Strong |
| Concision/token cost | Medium | Strong | Medium |

## Current Strengths

- Keeps Uncodixfy's core reset while making it less rant-like and more operational.
- Preserves OpenAI's full-bleed, image-led landing guidance without making every task a landing page.
- Adds Refactoring UI-derived mechanics agents can execute: constrained scales, hierarchy by de-emphasis, label/value treatment, right-aligned numbers, fixed/max widths, color shade systems, image contrast, intended media sizes, and fewer borders.
- Makes app UI and landing pages take different paths.
- Includes verification checks that should reduce visually broken outputs.
- Keeps references out of the shipped skill.

## Risks To Test Empirically

- The skill may be too long for a reset. Check whether agents follow the high-priority bans or diffuse attention across too many rules.
- The fallback palettes may still bias outputs toward preselected colors instead of project tokens. The existing-design-system eval should catch this.
- "Visual thesis" could lead some agents to print process notes unless they respect "internally" and product-copy rules.
- The landing page instructions may be less expressive than OpenAI's skill because the reset intentionally discourages decorative moves.
- The bans may be too strict for playful products, games, or highly branded marketing pages. Eval outputs should reveal whether the skill over-constrains.

## Expected Comparative Outcomes

- `frontend_good_defaults` should beat Uncodixfy on landing pages, imagery, states, and design-system mechanics.
- `frontend_good_defaults` should beat OpenAI frontend skill on internal apps, dashboard anti-pattern avoidance, data density, and fake-content suppression.
- OpenAI frontend skill may still beat it on bold art-directed landing pages if "delight" matters more than restraint.
- Uncodixfy may still beat it on pure anti-pattern suppression if our constructive guidance weakens the reset signal.

## Suggested Improvement Criteria

Only revise the skill after output runs show repeated failures. Prefer changes that generalize:

- If AI patterns still appear, move the relevant ban earlier or make it more concrete.
- If outputs are bland, strengthen image/composition guidance for landing pages without weakening app restraint.
- If agents expose internal design notes, tighten the "internal only" wording.
- If outputs ignore existing tokens, move token adherence into the reset section.
- If outputs are over-constrained for games or playful brands, add a short exception rule for intentional product personality.
