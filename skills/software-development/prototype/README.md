# Prototype

Answers **one design question with a throwaway artifact**, then throws it away — the answer is the only deliverable. Usable anywhere, not only in dev: settle a state model, a layout, a UI, or a document direction with real alternatives instead of argument. Keep the answer, delete the artifact.

## When to use

- **A design question blocks progress** — more than one plausible state model, data shape, or layout survives discussion and the choice is expensive to reverse; or there is visual uncertainty with no settled design.
- **You need to see alternatives, not describe them** — genuinely different variants a human can react to beats a paragraph of trade-offs.
- **Not for building the real thing** — a prototype answers the question that unblocks the build; it is not the build.

## Shape

- **Two default formats.** A _logic_ question gets one double-clickable self-contained HTML file — free-play controls plus tabbed guided walkthroughs, full relevant state visible after every action. A _UI/variants_ question gets multiple genuinely different variants on one route with a simple switcher. A _falsification_ entry probes an unfamiliar mechanism claim on the real runtime path.
- **Shared rules.** Disposable and labeled as such; effortless to launch; in-memory state; no polish, no tests.
- **Four gates.** Question stated → built & exposed → answer captured → cleaned. The validated decision is absorbed into the record (ticket or conversation); the artifact parks on its artifact branch with a render link; the prototype is never the record and nothing throwaway ships.

## Dependency surface

Composes with the optional `to-subagent`, `to-web`, and `writing-for-humans` siblings.

## Credits

- **Relationship:** extracted from this repository's earlier `backlog` skill ([`7f8ca23`](https://github.com/asasher/asher-skills/commit/7f8ca23)).
- **Technique source:** the two default formats (double-clickable logic demo with free-play plus guided walkthroughs; UI variants on one route with a switcher) are adapted from Matt Pocock's MIT-licensed [`prototype`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/prototype/SKILL.md).
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
