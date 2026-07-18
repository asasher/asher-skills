# Prototype

Answers **one design question with a throwaway artifact**, then throws it away — the answer is the only
deliverable. A thin composer usable anywhere, not only in dev: settle a state model, a layout, a UI, or a
document direction with real alternatives instead of argument. Keep the answer, delete the artifact.

## When to use

- **A design question blocks progress** — more than one plausible state model, data shape, or layout survives
  discussion and the choice is expensive to reverse; a plan is accumulating speculative "should handle X"
  reasoning that driving a real model would settle in minutes; or there is visual uncertainty with no settled
  design (a sibling like `plan`/`backlog` hands the question over by name; a user can ask directly).
- **You need to see alternatives, not describe them** — three structurally different variants a human can
  react to beats a paragraph of trade-offs.
- **Not for building the real thing** — a prototype answers the question that unblocks the build; it is not
  the build.

## Shape

- **A throwaway artifact, not only code.** A prototype is scaffolding built to reach an answer and torn down
  after. The medium is usually code (a reducer + terminal shell, a page with `?variant=`) but can be a
  rendered document, a layout, a driven scenario — anything that exists only to settle the question.
- **Two shapes, question-driven.** *Behavior* — "does this model/flow feel right under real cases?" — drives
  the idea through the awkward cases one action at a time. *Form* — "what should this look like / how
  structured?" — puts 3 structurally different variants side by side. Getting the shape wrong wastes the
  whole prototype.
- **Composes, doesn't fork.** Presenting the answer is the `review-loop` skill's job; staffing the build is
  the `staffing` skill's job. Prototype invokes both **by name** and owns neither's machinery.
- **Four gates.** Question stated → built & handed over → answer captured → cleaned up. The prototype is never
  the record, and nothing throwaway ships.

## Layout

`SKILL.md` is the gate-driven flow, entry points (direct or handed over by a sibling), how it composes
review-loop + staffing, and the three-part dependency surface. `reference/prototyping.md` is the authoritative
technique — the two shapes, the throwaway rules, capture and cleanup — written to stand alone so the skill
works outside dev. `agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the pre-deployment probe
eval.

Self-contained at the file level; composes by name. **Sibling dependency: `review-loop` + `staffing` —
`prototype` is a composer, not a root primitive** (it depends on those two by name and imports none of their
files). Repo-specific placement lives in the project playbook `docs/agents/prototyping.md`.

## Install

`npx skills add <repo-url> --skill prototype`, then hand it a design question. On a fresh repo it uses a
`docs/agents/prototyping.md` playbook for idiomatic placement (task runner, routing, where throwaway artifacts
live); absent one it degrades to the technique's defaults — a self-contained artifact in a scratch/workspace
dir. Presenting an answer for feedback needs the `review-loop` skill installed; staffing the build needs the
`staffing` skill installed.

## Credits

- **Relationship:** extracted from this repository's `backlog` skill.
- **Source:** [`7f8ca23`](https://github.com/asasher/asher-skills/commit/7f8ca23).
- **Authority moved:** throwaway design-question technique and cleanup gates moved here.
- **Local changes:** made it usable outside development and composed review-loop/staffing by name.
- **Technique source:** the two prototype shapes (logic-probe terminal app, UI variants on one route) are adapted from Matt Pocock's MIT-licensed [`prototype`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/prototype/SKILL.md).
