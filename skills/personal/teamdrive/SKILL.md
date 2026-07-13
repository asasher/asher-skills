---
name: teamdrive
description: Set up and operate a shared Google Workspace (Drive, Docs, Sheets, Slides) for agents through the gws CLI — install/auth walkthrough, in-place editing, revision history, and managed versions.
argument-hint: "[command] [target]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: thread
  requires: []
  optional: []
  setup: reference/setup.md
---

# Teamdrive

Teamdrive lets agents work on real Google Workspace files — Docs, Sheets, Slides, Drive — in a shared team Drive, using the [`gws` CLI](https://github.com/googleworkspace/cli) as the engine. This file is the command surface; each subcommand loads its own contract from `reference/` only when it runs.

`gws` authenticates **as the signed-in user**, so an agent inherits exactly that person's existing access — no more, no less — and nothing but an encrypted local login is ever stored. No service-account keys, no shared secret files. New users start at `setup`.

## Commands

| Command | Role | Reference |
|---|---|---|
| `setup` (default) | Walk a new user through installing `gws`, authenticating, and a live check — explaining each step | [reference/setup.md](reference/setup.md) |
| `check` | Confirm install + auth + access with a real API call (status alone can lie) | [reference/check.md](reference/check.md) |
| `edit` | Edit a Doc/Sheet/Slides **in place** (same fileId), safely under concurrency | [reference/edit.md](reference/edit.md) |
| `read` | Read or export a file's content, including from a Shared Drive | [reference/read.md](reference/read.md) |
| `versions` | List revision history and upload **managed versions** of a file | [reference/versions.md](reference/versions.md) |

Background the commands draw on — the auth, access, and Shared-Drive model — lives in [reference/auth-model.md](reference/auth-model.md). Load it when a command points there or the user asks how access works.

## Routing

1. **No argument** → run `setup`. Show the command table first so the user can redirect.
2. **First word matches a command** → load that reference and follow it. Everything after is the target (a fileId, URL, or Drive name).
3. **First word does not match** → infer the closest command, state the inferred command, then load its reference and proceed. A request to install, log in, connect, or "get started" infers `setup`.

## Core rules

- **Permission before install.** Never install software or run an authenticating browser flow without the user agreeing first. State the exact command, then run it.
- **Install only `@googleworkspace/cli` via npm.** `brew install gws` is a *different, unrelated tool* (a git-workspace manager) — never use it.
- **Prove access with a real call, not `gws auth status`.** A configured client can still hold a dead token (`invalid_grant`). Only a successful API request confirms readiness.
- **Shared Drives need their flags.** Any `gws drive` call touching a Shared Drive passes `supportsAllDrives: true` (and `includeItemsFromAllDrives: true` when listing/searching), or it returns "file not found".
- **Edits act as the human.** Revision history attributes changes to the signed-in user, not the agent. For per-agent attribution, use a marker convention — see `edit`.

## Glossary

- **gws**: the Google Workspace CLI (`@googleworkspace/cli`). Raw passthrough to every Workspace API method: `gws <service> <resource> <method> --params <JSON> --json <JSON>`.
- **Managed version**: a new file content uploaded under the **same fileId** via `drive.files.update`, tracked in revision history — not a duplicate sibling file.
- **Shared Drive**: an org-owned Drive (not a My-Drive folder) — the right home for a team workspace.
