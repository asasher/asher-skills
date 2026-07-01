# Skill Loop

`skill-loop` runs a target skill through an eval-backed improvement loop:

1. Read the current `SKILL.md` and latest eval signals.
2. Ask a fresh LLM reviewer for evidence-backed edits.
3. Apply only gated skill-text changes.
4. Run all test cases into a new `iteration-N/` directory.
5. Grade, aggregate, compare, and review with a human.
6. Repeat until no evaluation-backed edits remain.

## Usage

```bash
npx skills add <repo-url> --skill skill-loop
```

Invoke it with a skill and eval target:

```text
skill-loop skills/shadixfy/SKILL.md shadixfy-workspace
skill-loop shadixfy "cd shadixfy-workspace && bash scripts/run_all.sh <N>"
```

The eval target must document how to run every test case into `iteration-N/`, then grade and aggregate that
iteration. If the eval command is ambiguous, the skill stops and asks for the exact command rather than
guessing.
