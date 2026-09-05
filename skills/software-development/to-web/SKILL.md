---
name: to-web
description: Upload files to the project's artifact store and return a durable URL per file. Use when evidence media needs a permanent home outside the repo, or when an HTML artifact on an artifact branch needs a viewable render.
---

# To Web

Upload one or more files to the artifact store and hand back a durable URL per file, the skill's one move. Embedding belongs to the surface that presents the file (a PR comment, an issue projection, a report), outside this skill.

Two kinds of upload, one mechanism:

- **Evidence media**: a file whose permanent home is the store.
- **Artifact renders**: a viewable render of a source that stays version-controlled on its `artifact/<issue>` branch.

## Binding

The store binding lives in `docs/agents/environment.md` § Artifact store: the bucket, the public base URL, the credential environment-variable names, and the upload command, S3-compatible with R2 as the reference example. Credentials come from the environment, never from any file in the repo. Absent the binding, state the gap and stop; media is never committed as a fallback.

## Keys and visibility

- **Visibility is public with unguessable keys.** Every key carries a random segment long enough that the URL cannot be guessed. Anyone with the URL can read the file: when the file carries a secret, personal data, or unreleased internal material, name the exposure and get the user's go-ahead before uploading.
- **Keys are immutable and carry the source's identity**: `<repo>/<issue-or-slug>/<commit-or-content-hash>-<random>/<filename>`, the source commit for artifact renders and the content hash for evidence media. A changed file is a new key, so a URL embedded in a PR or an issue projection keeps its meaning forever.

## Verify before reporting

An upload is done when the URL answers, not when the upload command exits: fetch each URL and confirm it returns the uploaded content, HTTP 200 with the file's size or hash matching, before handing it back. Report each file's URL and the key it lives under.
