# Codex compatibility manifest

## Problem

These skills install into more than one harness. Codex reads an `agents/openai.yaml` manifest to decide
how a skill is presented (display name, description, default prompt) and whether it may be invoked
implicitly. Without one, the skill still works in Claude Code but presents poorly — or fires when it
shouldn't — in Codex.

## Shape

`agents/openai.yaml` in the skill root:

```yaml
interface:
  display_name: "Backlog"
  short_description: "Groom the backlog, then run ready-for-agent issues through the issue loop to reviewed PRs"
  default_prompt: "Use $backlog to triage the open issues in this repo."

policy:
  allow_implicit_invocation: false
```

- `short_description` should match the spirit of the SKILL.md frontmatter description, compressed to one
  line.
- `default_prompt` is what a user gets when they invoke the skill with no arguments — write it as the most
  common concrete ask.
- Default `allow_implicit_invocation` to `false` for operator-style skills that run loops or spend money;
  only lightweight advisory skills should be implicitly invocable.

## How to adopt

Copy any existing `agents/openai.yaml` (backlog's is canonical), rewrite the three interface strings,
decide the invocation policy deliberately.

Note the `agents/` directory is shared-purpose: it also holds Claude subagent definitions when a skill
ships one (fair-deal's `agents/research-analyst.md`). The yaml manifest and subagent markdown coexist.

## Instances

backlog, bare-minimum-ux, eloquent, goodwork, smallbets, teamdrive.
