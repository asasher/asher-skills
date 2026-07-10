<!-- Seed for the harness's GLOBAL memory file (~/.claude/CLAUDE.md or the harness equivalent).
     Written by setup-asher-skills phase 4, with explicit consent, and only for sections not already
     present there. Any project overrides these in its own docs/agents/ playbooks. -->

## Conventions

### Presenting HTML to the human

- Author HTML deliverables — plans, reports, prototypes, review sheets — as **local files** in the repo or
  workspace.
- Present by **opening the local file** when the human is at this machine; when they are remote, serve it
  over the **tailnet presentation surface** (the project's `docs/agents/` surface config names the root URL
  and publish commands).
- **Prefer disk over harness-native surfaces, in every harness.** Do not reach for Claude artifacts, the
  ChatGPT site/canvas, or any other harness-hosted page as the presentation surface — write the HTML to
  disk and present it locally or over the tailnet. Publish to a cloud artifact (claude.ai or similar)
  **only when the human explicitly asks** — never as the default.

### Tailnet surface

- Bringing the tailnet proxy up and down is a global capability of this machine:
  `<fill at install: the serve/funnel up and down commands>`. Keep it down when nothing is being presented.
- Each project's surface config (its `docs/agents/` playbook) overrides the root URL, surface directory, and
  keep-awake choice; this global section carries only the machine-level commands and the local-first rule.
