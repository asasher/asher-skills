---
name: prototype
description: Answer one design question with a throwaway artifact. Use to settle a state model, UI, document direction, or unproven mechanism claim that reasoning alone cannot settle. Not for building the real thing.
argument-hint: "<design question>"
metadata:
  optional: [writing-for-humans]
---

# Prototype

Build the smallest throwaway artifact that answers one design question. The answer is durable; the artifact is not.

Use `writing-for-humans` for the artifact and returned prose.

## Gates

1. **State the question.** Record one question and what settles it. For logic and mechanism claims, name the claim the artifact can falsify. For UI and variants, name the alternatives and the decision they settle.
2. **Build and expose it.** Make the artifact launchable, show its relevant state, and open or drive it directly. Iterate only to settle the stated question.
3. **Return the result.** Return the artifact path, what it demonstrates, and any choice that still needs human judgment.

## Formats

- A logic question gets one double-clickable self-contained HTML file with free-play controls, tabbed guided walkthroughs, and the full relevant state after every action.
- A mechanism claim gets the smallest runtime-real probe that can make the claim fail. State the predicted observation first and run the probe before any design depends on the claim.
- A UI or variants question gets multiple structurally different variants on one route with a simple switcher. Vary layout, hierarchy, or primary affordance, not only color or copy.

The medium need not be code. A rendered document or hand-driven state table qualifies when it settles the question.

Keep the artifact disposable, effortless to launch, and in memory unless persistence is the question. Add no polish or tests. Implementation rebuilds the chosen experience or lifts the validated logic; the prototype itself never ships.
