# Playbook: Prototyping

> Project delta for the `prototype` skill. The installed skill owns the technique (`reference/prototyping.md`: the behavior, variants, and falsification shapes, rules, capture, cleanup); this file keeps only this repo's placement bindings.

## This repo

- Task runner and how to register a script: **none** — no build/task system. A prototype here is a throwaway artifact answering a design question about a skill: a standalone HTML file (does this rendered plan/prototype read well?), a scratch scenario run (does this SKILL routing resolve? does this prompt shape produce the intended decision?), or a stdlib-Python spike.
- Routing convention and where shared UI lives: n/a — no app routing. If a prototype needs a rendered HTML surface, use a self-contained single file (inline CSS/JS) so it renders on the tailnet surface with no external assets.
- Component library / styling system variants must use: none. Keep prototypes **outside** any skill directory — under the relevant `<skill>-workspace/` at the repo root or the session scratchpad — so throwaway code never ships inside a self-contained skill.
