---
name: prototype
description: Answer one design question with a throwaway artifact. Use to settle a state model, UI, document direction, or an unproven mechanism claim — any question paper can't settle. Not for building the real thing.
argument-hint: "<design question>"
metadata:
  optional: [writing-for-humans, to-branch, to-subagent, to-web]
---

# Prototype

Build the smallest throwaway artifact that answers one design question. The answer is durable; the artifact is not.

User-facing text follows the `writing-for-humans` sibling — ASD-STE100 plain language, `CONTEXT.md` as the dictionary, no bare ticket or PR numbers. Absent it, write plainly and say the standard was not loaded.

## Entry

Run on an explicit question; if it is vague, narrow it until it passes gate 1. Framing and interpretation stay here; build-out may be dispatched via the `to-subagent` skill (absent it, build in-session).

## Gates

1. **Question stated.** Record one question and what settles it: for logic and mechanism claims, the claim the artifact can falsify; for UI/variants, the alternatives presented and the decision they settle.
2. **Built and exposed.** Launchable per the shared rules, state visible. Open rendered artifacts; drive live ones directly. Iterate only to settle the named question. Failure to expose a falsifiable observation — or, for variants, real alternatives a human can react to — returns to gate 1.
3. **Decision captured.** Write the decision, why, and the evidence into the record of the work that raised the question — the ticket, or the raising conversation. Evidence: for logic and mechanism claims, the observed outcome against the prediction; for UI/variants, a screenshot of every variant with the winner marked. The prototype itself is never the record.
4. **Cleaned.** Build on the desk as untracked scratch; **publish at record time** — commit the artifact to its artifact branch (`artifact/<ticket>-<slug>`; `artifact/<slug>` when ticketless) via the `to-branch` sibling (absent it, a temporary worktree on that branch), with a `to-web` render link in the record (absent that sibling, link the branch file). Publish and link are one move — every commit on the branch is a revision somebody was shown. Nothing throwaway ships — the build that follows rebuilds the winner or lifts the validated logic, and the branch is deleted when spent, never in this run.

## Formats

- **A logic question** ("does this model / flow behave right?") → **one double-clickable self-contained HTML file**: plain HTML/CSS/JS, no build, no server. It carries **free-play controls** (one per action, always available) plus **tabbed guided walkthroughs** — each tab a scenario in plain words above the ordered actions to press, resetting to a known initial state — and shows the **full relevant state after every action**, in domain language.
- **A mechanism claim** (no observed evidence on this runtime) → **the smallest runtime-real probe that can make the claim fail.** State the predicted observation first; run the probe before any design that depends on the claim. A green mock or seam that bypasses the claimed runtime path is not evidence, and a failure in the probe's own scaffolding is a probe defect, not a verdict.
- **A UI or variants question** ("what should this look like / how structured?") → **multiple structurally different variants (layout, hierarchy, primary affordance) on one route with a simple switcher**; color-or-copy-only variants are wallpaper. Host in the real page where one exists (read-only over its real data; stub mutations); the switcher cycles and keeps variants shareable. An interface's non-obvious presentation choices — visual hierarchy, which actions are overt, what each journey step shows — are decisions this format settles.

The medium need not be code — a rendered document or a hand-driven state table is a prototype when it exists only to settle a question. When the question fits none of these, build one artifact that still passes the gates.

## Shared rules

- **Disposable and labeled as such** — named so a casual reader sees it is not production.
- **Effortless to launch** — a file that opens by double-click, or one URL.
- **In-memory state** — no persistence unless persistence _is_ the question.
- **No polish, no tests** — nothing beyond runnable.
