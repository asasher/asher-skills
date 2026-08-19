---
name: to-web
description: Upload files to the project's bound store and return a durable URL per file. Use when evidence media needs a permanent home outside the repo, or when an HTML artifact on an artifact branch needs a viewable render. Private one-off viewing is the to-tailnet sibling.
argument-hint: "<file path(s)> [ticket id]"
metadata:
  requires: [docs/agents/platform.md]
  optional: [to-tailnet]
---

# To Web

Upload one or more files to the bound store and hand back a durable URL per file — the skill's one move. Embedding belongs to the surface that presents the file (a PR, a ticket projection, a report), outside this skill.

Two kinds of upload, one mechanism:

- **Evidence media** — a file whose permanent home is the store.
- **Artifact renders** — a viewable render of a source that stays version-controlled on its `artifact/*` branch. The render is a preview deployment.

## Binding

The store binding lives in `docs/agents/platform.md`: the bucket or store, the public base URL, the credential environment-variable names, and the upload command — S3-generic, with R2 as the reference example. Credentials come from the environment, never from any file in the repo. Absent the binding, state the gap and stop; offer the `to-tailnet` sibling for a one-off private viewing. Media is never committed as a fallback.

## Keys and visibility

- **Visibility is public with unguessable keys.** Every key carries a random segment long enough that the URL cannot be guessed. Anyone with the URL can read the file — when the file carries a secret or credential, personal data, or unreleased internal material, name the exposure and get the user's go-ahead before uploading.
- **Keys are immutable and carry the source's identity**: `<repo>/<ticket-or-slug>/<commit-or-content-hash>-<random>/<filename>` — source commit for artifact renders, content hash for evidence media. A changed file is a new key — a URL embedded in a PR or a blessed projection keeps its meaning forever.

## Verify before reporting

An upload is done when the URL answers, not when the upload command exits: fetch each URL and confirm it returns the uploaded content — HTTP 200 with the file's size (or hash) matching — before handing it back. Report each file's URL and the key it lives under.
