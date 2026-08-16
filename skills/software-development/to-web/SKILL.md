---
name: to-web
description: Upload a file to the project's bound web store and return a durable URL. Use when evidence media (screenshots, video, GIFs) needs a permanent home outside the repo, or when an HTML artifact on an artifact branch needs a viewable render. Not for ephemeral or private viewing — that is the to-tailnet sibling.
argument-hint: "<file path(s)> [ticket id]"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: [to-tailnet]
---

# To Web

Upload one or more files to the bound store and hand back a durable URL per file. This skill does one move; embedding the URLs — in a PR, a ticket projection, a report — stays with the caller.

Two upload meanings, one mechanism:

- **Evidence media** — a file whose permanent home is the store: media stays out of the repo, and the surface that presents it embeds the URL.
- **Artifact renders** — a viewable render of a source that stays version-controlled on its `artifact/*` branch. The render is a preview deployment, keyed by the commit the source was rendered from — a new blessed commit means a new upload and a new URL; old URLs stay true forever.

## Binding

The store binding lives in `docs/agents/platform.md`: the bucket or store, the public base URL, the credential environment-variable names, and the upload command — S3-generic, with R2 as the reference example. Credentials come from the environment, never from any file in the repo. Absent the binding, state the gap and stop — never invent a store, and never fall back to committing media; for a one-off private viewing, offer the `to-tailnet` sibling instead.

## Keys and visibility

- **Visibility is public with unguessable keys.** Every key carries a random segment long enough that the URL cannot be guessed; the store serves it publicly. Anyone with the URL can read the file — say so when the content looks sensitive, before uploading.
- **Keys are content-addressed and immutable**: `<repo>/<ticket-or-slug>/<commit-or-content-hash>-<random>/<filename>`. Never overwrite an existing key — a URL embedded in a PR or a blessed projection must never change meaning. A changed file is a new key.

## Verify before reporting

An upload is done when the URL answers, not when the upload command exits: fetch the URL and confirm the response before handing it back. Report each file's URL and the key it lives under.
