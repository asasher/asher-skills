---
name: to-spec
description: Turn a settled conversation or shaping record into a spec on the subject's artifact branch; the ticket gets a projection. Creates the ticket when none exists. Pure synthesis, no interview.
argument-hint: "[<ticket id, or a name for the spec>]"
metadata:
  optional: [experience-first, writing-for-humans, to-branch, to-web]
---

# To-Spec

To-spec owns one move: **take a conversation that already reached a decision and write the spec it earned** — the high-level direction document downstream work builds on. Pure synthesis, no interview: undecided points become Notes lines, never questions back (synthesis § The one rule).

User-facing text follows the `writing-for-humans` sibling; absent it, write plainly and say the standard was not loaded.

## Command surface

- **`to-spec [<ticket id, or name>]`** — the argument names the subject ticket, or supplies the slug when one is created (synthesis § Where the spec lives).

Load [synthesis](reference/synthesis.md) for the method and [template-guide](reference/template-guide.md) for what each section holds.

## How a spec gets written

The shape:

1. **Mine, don't ask.** Read the table (synthesis § The one rule). Start from the shaping record when one exists (synthesis § What to mine). Sweep every decision-informing artifact into a **Supporting artifacts** entry (synthesis § Sweep the artifacts). Done when every synthesis § What to mine category is either filled or landed as a Notes line.
2. **Classify the work — dev or non-dev** (synthesis § Classify the work); a dev spec runs the seams step below, a non-dev spec skips it.
3. **For dev specs only — sketch the test seams, declare the test split, sweep the contract surface.** Name the public seams the work would be tested at, **prefer the highest existing seam**, declare per acceptance criterion whether it lands as a durable suite test or a throwaway verification script (synthesis § The test split), and enumerate the contract decisions hiding as defaults (synthesis § Sweep the contract surface).
4. **Draft, then publish to the artifact branch** (synthesis § Where the spec lives) — one HTML document, **opening with a diagram** of the moving parts (synthesis § The diagram comes first), then the template's sections in generic vocabulary, ordered per the `experience-first` sibling where the work has both registers: experience sections (organized per affected user type) before implementation sections, implementation stated as recommendations with only genuine forks left open (absent that sibling, keep the template's own order). Draft as an untracked scratch file in the current worktree; **publish at record time** via the `to-branch` sibling — a commit on the artifact branch without any checkout, whose printed hash is the projection's hash (absent that sibling, a temporary worktree on the artifact branch is the fallback). The branch file is **canonical**. Then write the ticket's **projection** and post its change comment (synthesis § Where the spec lives). Ticket reads, comments, and creation follow the tracker bindings in `docs/agents/platform.md`. A direction too big for one build ends with a **recommended split** — a proposal only (synthesis § Recommend the split, never perform it).
5. **Classify the Notes, then audit fidelity.** Classify every Notes line — blocking, delegated, or deferred (template-guide § Notes) — then run the fidelity audit in both directions (synthesis § Sign-off). Done when every Notes line is classified and the audit passes in both directions.
6. **Sign-off — the direction's approval gate** (synthesis § Sign-off). User present: done when the approval and its commit hash are recorded. User AFK: done once the projection is posted. No tracker: done with the spec on its branch, sign-off deferred.
