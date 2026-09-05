# Shape

Shapes one GitHub issue into a blessed spec. The issue's work branch carries project context changes into the later build and its single PR. Research, prototype questions, and settled-record synthesis run in fresh subagents; `shape` commits each artifact to the issue's `artifact/<issue>` branch, publishes the render through `to-web`, and projects each revision onto the issue. Before opening additions, shaping separates the desired outcome from proposed solutions, traces claimed requirements to their sources, and subtracts unsupported steps from the current experience and system behavior. Implementation design describes the coherent target separately from migration and compatibility constraints, then uses the `principle-codebase-design` and `principle-type-system-discipline` siblings, with `typescript-best-practices` for TypeScript targets when available. When the approved spec recommends a split and the user agrees, `shape` runs `to-slices` inline at the close.

## Credits

- **Relationship:** rewritten synthesis.
- **Sources:** Jon McNeill's five-step framework in _The Algorithm_; Cursor's [`principle-subtract-before-you-add`](https://github.com/cursor/plugins/blob/45c66fde1f1681a902a30d1ae8bca1cc64465d6e/pstack/skills/principle-subtract-before-you-add/SKILL.md) and [`principle-redesign-from-first-principles`](https://github.com/cursor/plugins/blob/45c66fde1f1681a902a30d1ae8bca1cc64465d6e/pstack/skills/principle-redesign-from-first-principles/SKILL.md).
