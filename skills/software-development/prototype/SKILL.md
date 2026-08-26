---
name: prototype
description: Answer one design question with a disposable artifact. Use to settle a state model, UI, document direction, or unproven mechanism claim that reasoning alone cannot settle.
metadata:
  optional: [writing-for-humans]
---

# Prototype

Build the smallest disposable artifact that answers one design question.

Use `writing-for-humans` for the artifact and returned prose.

## Gates

1. **State the question.** Record one question and what settles it with the artifact. For logic and mechanism claims, name the claim the artifact can falsify. For UI and other alternatives, name the choices and the decision they settle.
2. **Build and expose it.** Make the artifact launchable, show its relevant state, and open or drive it directly. Iterate only to settle the stated question.
3. **Return the result.** Return the artifact path, what it demonstrates, and any choice that still needs human judgment.

## Formats

- A logic question gets one double-clickable self-contained HTML file. Keep the logic under test independent from the page and use domain language for controls and displayed state. Provide free-play controls, the full relevant state after every action, and guided walkthroughs for the normal path and awkward or invalid cases that could disprove the model.
- A mechanism claim gets the smallest runtime-real probe that can make the claim fail. State the predicted observation first and run the probe before any design depends on the claim.
- A UI question gets three structurally different variants by default and no more than five, on one route with a query-parameter switcher. Prefer an existing page with its real data and surrounding UI; use a new prototype route when no page is a natural host. Vary layout, hierarchy, or primary affordance, not only color or copy.
- A document or other direction question gets comparable alternatives in the medium that makes their differences easiest to judge. A rendered document or hand-driven state table qualifies when it settles the question.

Keep the artifact effortless to launch and in memory unless persistence is the question. Add no polish or tests. Use the settled direction or validated behavior as the reference for implementation.
