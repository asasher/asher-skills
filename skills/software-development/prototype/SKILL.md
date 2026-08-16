---
name: prototype
description: Answer one design question with a throwaway artifact — keep the answer, delete the scaffolding. Usable anywhere, not only dev. Use to settle a state model, UI, or document direction with real alternatives — any question paper can't settle. Not for building the real thing.
argument-hint: "<design question>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [writing-for-humans, to-subagent, to-web]
---

# Prototype

Build the smallest throwaway artifact that answers one design question. The answer is durable; the artifact is not.

User-facing text follows the `writing-for-humans` sibling — ASD-STE100 plain language, `CONTEXT.md` as the dictionary, no bare ticket or PR numbers. Absent it, write plainly and say the standard was not loaded.

## Entry

Run on an explicit question; if it is vague, narrow it before building. Framing and interpretation stay here; build-out may be dispatched via the `to-subagent` skill (absent it, build in-session). An unfamiliar **mechanism claim** takes the falsification entry: build the smallest runtime-real probe that can make the claim fail, state the predicted observation first, and run it before dependent design — a green mock or seam that bypasses the claimed runtime path is not evidence, and a failure in the probe's own scaffolding is a probe defect, not a verdict.

## Gates

1. **Question stated.** Record one question and its shape: for logic/falsification, the claim the artifact can falsify; for UI/variants, the alternatives presented and the decision they settle.
2. **Built and exposed.** Provide one file or URL and visible state. Open rendered artifacts; drive live ones directly. Iterate only to settle the named question.
3. **Answer captured.** Write the decision, why, and relevant variant captures into the record of the work that raised the question — the ticket, or the raising conversation.
4. **Cleaned.** Absorb only the validated decision into the record; park the artifact on its artifact branch (`artifact/<ticket>-<slug>`; `artifact/<slug>` when ticketless) with a `to-web` render link in the record (absent that sibling, link the branch file), and record the verdict. Nothing throwaway ships.

Failure to expose a falsifiable observation — or, for variants, real alternatives a human can react to — returns to gate 1.

## The two default formats

- **A logic question** ("does this model / flow behave right?") → **one double-clickable self-contained HTML file**: plain HTML/CSS/JS, no build, no server. It carries **free-play controls** (one per action, always available) plus **tabbed guided walkthroughs** — each tab a scenario in plain words above the ordered actions to press, resetting to a known initial state — and shows the **full relevant state after every action**, in domain language.
- **A UI or variants question** ("what should this look like / how structured?") → **multiple genuinely different variants on one route with a simple switcher.** Structurally different — layout, hierarchy, primary affordance; variants differing only in color or copy are wallpaper. Host in the real page where one exists (read-only over its real data; stub mutations); the switcher cycles and keeps variants shareable. An interface's non-obvious presentation choices — visual hierarchy, which actions are overt, what each journey step shows — are decisions this format settles; implementation never invents them.

The medium need not be code — a rendered document or a hand-driven state table is a prototype when it exists only to settle a question. When the question fits neither format, keep the format's discipline: one artifact, real alternatives or a falsifiable observation, state visible.

## Shared rules

- **Disposable and labeled as such** — named so a casual reader sees it is not production.
- **Effortless to launch** — a file that opens by double-click, or one URL.
- **In-memory state** — no persistence unless persistence _is_ the question.
- **No polish, no tests** — nothing beyond runnable.

## Afterward

The validated decision is absorbed into the record — which option won and why, variant captures embedded with the winner marked; the prototype itself is never the record. The artifact is parked on its artifact branch, its `to-web` link in the record, the verdict recorded. A winning variant is rebuilt properly; a validated logic module is lifted into real code; the branch is deleted when spent.
