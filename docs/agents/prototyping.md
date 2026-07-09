<!-- backlog-templates: v2026-07-06.1 -->

# Playbook: Prototyping

> Project playbook for this repo. The backlog `prototype` subskill reads this file for the technique; the gates are in the skill's `reference/prototype.md`. The two shapes below are the shipped default (adapted from Matt Pocock's `prototype` skill, MIT) — tailor the **This repo** section; replace the technique if this team prototypes differently.

## Pick the shape

The question decides the shape — getting this wrong wastes the whole prototype:

- **"Does this logic / state model feel right?"** → the **logic** shape: a tiny interactive terminal app that pushes the model through cases that are hard to reason about on paper.
- **"What should this look like?"** → the **UI** shape: several radically different variations of one surface, flipped between in the browser.

If the question is ambiguous, default to whichever matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

## Rules for both shapes

- **Throwaway from day one, clearly marked.** Locate the prototype near the code it's prototyping for, named so a casual reader sees it's not production. Follow the repo's existing routing/task-runner conventions; don't invent new top-level structure.
- **One command to run** — wired into the repo's task runner so nobody remembers a path.
- **No persistence.** State lives in memory unless persistence *is* the question (then a scratch store with a clear "PROTOTYPE — wipe me" name).
- **Skip the polish.** No tests, no error handling beyond runnable, no abstractions. Learn fast, then delete.
- **Surface the state** after every action or variant switch, so the human always sees what changed.

## Logic shape

- Put the logic being tested behind a small **pure, portable module** — a reducer `(state, action) => state`, an explicit state machine, or a set of pure functions over a plain type, whichever fits the question (not whichever is easiest to wire up). No I/O, no terminal code inside it: the shell imports the module, never the reverse. When the question is answered, this module is the part worth lifting into real code.
- Wrap it in the smallest terminal shell that works: clear and re-render one stable frame per action — current state pretty-printed, then the keybindings (`[a] add  [t] tick  [q] quit`). The whole frame fits on one screen.
- The interesting moments are "wait, that shouldn't be possible" — those are bugs in the *idea*, which is the point. Add actions on request.

## UI shape

- Default to **3 structurally different variants** (cap at 5) — different layout, information hierarchy, primary affordance. Variants that differ only in color or copy are wallpaper, not a prototype. If two drafts converge, redo one with an explicit structural constraint.
- **Host the variants in the real page whenever one plausibly exists**, gated by a `?variant=` URL param, keeping the page's real data fetching, params, and auth — an empty standalone route hides design problems a populated page exposes. Only when the surface genuinely has no home: a clearly named throwaway route under the repo's routing convention.
- Add a floating switcher pill (bottom-center, visually distinct from the design under evaluation): prev/next arrows plus the variant key and name; arrow keys cycle too (not while an input is focused); URL updates via the router so variants are shareable and reload-stable; hidden in production builds.
- Hold every variant to the page's real purpose, its real data, and this repo's component library.
- The best feedback is composite — "the header from B with the sidebar from C" is the design the human actually wants.

## Capture and cleanup

- Capture the answer — which option won and why — into the consuming plan when planning invoked this; standalone, into the issue or a commit message. For UI shapes, screenshot each variant via the driver in `environment.md` and embed them in the plan with the winner marked.
- Then delete: losing variants and the switcher go; the winning variant is rebuilt properly (it was written under prototype constraints), and a validated logic module is lifted into real code. Nothing throwaway stays.

## This repo

- Task runner and how to register a script: **none** — no build/task system. A prototype here is a throwaway artifact answering a design question about a skill: a standalone HTML file (does this rendered plan/prototype read well?), a scratch scenario run (does this SKILL routing resolve? does this prompt shape produce the intended decision?), or a stdlib-Python spike.
- Routing convention and where shared UI lives: n/a — no app routing. If a prototype needs a rendered HTML surface, use a self-contained single file (inline CSS/JS) so it renders on the tailnet surface with no external assets.
- Component library / styling system variants must use: none. Keep prototypes **outside** any skill directory — under the relevant `<skill>-workspace/` at the repo root or the session scratchpad — so throwaway code never ships inside a self-contained skill.
