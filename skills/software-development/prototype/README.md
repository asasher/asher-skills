# Prototype

Answers **one design question with a throwaway artifact**, then throws it away — the answer is the only
deliverable. Usable anywhere, not only in dev: settle a state model, a layout, a UI, or a document
direction with real alternatives instead of argument. Keep the answer, delete the artifact.

## When to use

- **A design question blocks progress** — more than one plausible state model, data shape, or layout
  survives discussion and the choice is expensive to reverse; or there is visual uncertainty with no
  settled design.
- **You need to see alternatives, not describe them** — three structurally different variants a human can
  react to beats a paragraph of trade-offs.
- **Not for building the real thing** — a prototype answers the question that unblocks the build; it is
  not the build.

## Shape

- **A throwaway artifact, not only code.** Scaffolding built to reach an answer and torn down after — a
  reducer with a terminal shell, a page with `?variant=`, a rendered document, a driven scenario.
- **Question-driven shapes.** *Behavior* drives the idea through the awkward cases one action at a time;
  *variants* puts structurally different alternatives side by side; *falsification* exposes the claim an
  artifact can break. An interface's non-obvious presentation choices are decisions a variants prototype
  settles — implementation never invents them.
- **Four gates.** Question stated → built & exposed → answer captured → cleaned up. The prototype is
  never the record, and nothing throwaway ships.

## Dependency surface

- **Bundled:** `reference/prototyping.md` — the authoritative technique.
- **Project:** optional placement delta `docs/agents/prototyping.md` (task runner, routing, where
  throwaway artifacts live); absent it, a self-contained artifact in a scratch dir.
- **Siblings (optional, by name):** `serve-via-tailnet` (present answer sheets to a user not at this
  machine; degrades to opening locally), `to-subagent` (build-out dispatch; degrades to building
  in-session).

## Credits

- **Relationship:** extracted from this repository's earlier `backlog` skill
  ([`7f8ca23`](https://github.com/asasher/asher-skills/commit/7f8ca23)).
- **Technique source:** the two core prototype shapes (logic-probe terminal app, UI variants on one
  route) are adapted from Matt Pocock's MIT-licensed
  [`prototype`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/prototype/SKILL.md).
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
