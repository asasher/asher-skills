---
name: agent-ready-codebase
description: Assess whether a repository can run the lifecycle family with isolated builds, runnable checks, and a working artifact bucket.
metadata:
  requires: [to-web]
---

# Agent-ready codebase

Certify the repository by demonstrating each capability, then record commands and gaps in `docs/agents/environment.md`.

1. **Worktrees:** create, attach existing local/remote branches, and remove secondary working copies without moving the primary checkout.
2. **Stack:** bring up an isolated stack and run the project's checks in each worktree.
3. **Auth:** mint a usable session independently in each working copy.
4. **Seed:** reach the application's features with reproducible data. New features extend the seed.
5. **Artifacts:** use `to-web` to upload HTML and evidence media to the configured bucket, then fetch the resulting URLs and confirm the content. Keep screenshots, images, MP4s, and GIFs out of Git.

Pass only demonstrated items; explain genuinely inapplicable app capabilities. An absent artifact bucket is a readiness gap. Record shared singletons and what changes would collide. Issues changing shared state precede only the work that truly depends on that change.

Certification records repository capabilities, not permanent machine health. Check current access and capacity at dispatch; re-certify when setup changes.
