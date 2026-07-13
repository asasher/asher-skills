# Teamdrive

A user-invoked router skill for operating a shared Google Workspace (Drive, Docs, Sheets, Slides) as an agent workspace, built on the [`gws` CLI](https://github.com/googleworkspace/cli) (`@googleworkspace/cli`).

Start with `teamdrive setup` — it installs `gws` (after permission), authenticates via the browser, and runs a live check. `gws` signs in **as the user**, so agents inherit exactly that person's existing Google access and nothing but an encrypted local login is stored.

Commands: `setup`, `check`, `edit` (in-place, same fileId), `read`, `versions` (revision history + managed versions). See `SKILL.md` for the command surface and `reference/auth-model.md` for the access model.

## Notes

- Install the real tool with `npm install -g @googleworkspace/cli`. **Not** `brew install gws` — that is an unrelated git-workspace manager.
- `gws` is community-published by Google's Workspace team and pre-1.0 ("not an officially supported Google product"); pin a version for load-bearing use.
