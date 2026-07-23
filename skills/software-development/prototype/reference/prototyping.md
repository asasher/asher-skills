# The Prototyping Technique

Repo-specific placement (task runner, where throwaway artifacts live, the component library variants must
use) lives in the project playbook `docs/agents/prototyping.md`; read it for the "where," read this for the
"how." Absent a playbook, fall back to the defaults called out below rather than improvising repo structure.

The medium is usually code, but it need not be — a rendered document, a layout, a maquette, a driven
scenario, or a spreadsheet is a prototype when it exists only to settle a question and is discarded once it
has.

## Pick the shape

The question decides the shape:

- **"Does this logic / model / flow feel right?"** → the **behavior shape**: something you push through the
  cases that are hard to reason about on paper, one action at a time, watching what the model does.
- **"What should this look like / how should this be structured?"** → the **variants shape**: several radically
  different variations of one surface, flipped between so a human can react to real alternatives.

If the question is ambiguous, default to whichever matches the surrounding work (a state machine or backend
module → behavior; a page, a document, a layout → form) and state the assumption at the top of the prototype.

An unfamiliar mechanism claim uses the **falsification shape**: build the smallest runtime-real probe that
can make the claim fail, state the predicted observation first, and run it before dependent design. A green
mock or seam that bypasses the claimed runtime path is not evidence.

## Rules for both shapes

- **Throwaway from day one, clearly marked.** Locate the prototype near what it prototypes for, named so a
  casual reader sees it is not production. Follow the surrounding conventions (the repo's task runner, the
  project playbook's placement rule); don't invent new top-level structure. Absent a playbook: a
  self-contained file in a scratch/workspace directory, outside any shipped artifact.
- **One command to run, or one URL to open.** For code, wire it into the task runner; for a document, it is
  the file that opens.
- **No persistence.** State lives in memory unless persistence *is* the question (then a scratch store with a
  clear "PROTOTYPE — wipe me" name).
- **Skip the polish.** No tests, no error handling beyond runnable, no abstractions.
- **Surface the state** after every action or variant switch, so the human always sees what changed.

## Behavior shape

*Answers: does this model behave the way I think under the cases that are hard to hold in my head?*

- **Code:** put the logic behind a small **pure, portable module** — a reducer `(state, action) => state`, an
  explicit state machine, or a set of pure functions over a plain type, whichever fits the question (not
  whichever is easiest to wire up). No I/O inside it: the shell imports the module, never the reverse. When
  the question is answered, this module is the part worth lifting into real code. Wrap it in the smallest
  terminal shell that works: clear and re-render one stable frame per action — current state pretty-printed,
  then the keybindings (`[a] add  [t] tick  [q] quit`). The whole frame fits on one screen.
- **Non-code:** the same discipline without a program. A **hand-driven state table** — a document that lists
  the states and, for each, what each event does — walked through the awkward sequences by hand; or a
  **scenario run** where you narrate the model's response to a script of real inputs and record where it
  surprises you.
- The interesting moments are "wait, that shouldn't be possible" — those are bugs in the *idea*, which is the
  point. Add cases on request.

## Form shape

*Answers: which of several genuinely different directions is right?*

- Default to **3 structurally different variants** (cap at 5) — different layout, information hierarchy,
  primary affordance. Variants that differ only in color or copy are wallpaper, not a prototype. If two
  drafts converge, redo one with an explicit structural constraint.
- **Code (a UI surface):** host the variants in the real page whenever one plausibly exists, gated by a
  `?variant=` URL param, keeping the page's real data fetching, params, and auth — an empty standalone route
  hides design problems a populated page exposes. Add a floating switcher pill (bottom-center, visually
  distinct from the design under evaluation): prev/next plus the variant key and name; arrow keys cycle too
  (not while an input is focused); URL updates so variants are shareable and reload-stable; hidden in
  production builds. Hold every variant to the page's real purpose, its real data, and this repo's component
  library.
- **Non-code (a document, layout, slide, or doc UI):** the variants are **structurally different drafts of
  the same content** — three ways to organize the same plan, three layouts for the same one-pager — each a
  self-contained rendered artifact (a standalone HTML file, inline styles, no external assets, so it
  renders anywhere). One artifact per variant, or one artifact with a variant
  switcher.
- The best feedback is composite — "the header from B with the sidebar from C" is the design the human
  actually wants.

## Present the answer for feedback

A variants-shape prototype, and any behavior-shape prototype whose answer is a rendered document, is
presented by opening the rendered artifact / variant sheet and ending the pause with its location.
Feedback arrives in conversation. A live interactive prototype (a terminal behavior app, a running page)
is driven directly.

## Staff the build — compose `staffing`

Building the artifact — the reducer and shell, the variants, the draft sheets — is dispatched to the builder
the **`staffing`** skill resolves (by name): mechanical build-out to the pinned mechanical model, anything
with taste weight (a UI variant, a rendered document) to a taste-ranked model.

## Capture and cleanup

- **Capture the answer** — which option won and why — into the consuming plan when planning invoked this;
  standalone, into the issue or a commit message the playbook names. For variants-shape prototypes, capture each
  variant (a screenshot of a UI, the rendered sheet of a document) and embed them with the winner marked.
  The prototype itself is never the record.
- **Then delete.** Losing variants and the switcher go; a winning variant is rebuilt properly (it was written
  under prototype constraints), and a validated behavior module is lifted into real code.
