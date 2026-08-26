---
name: code-review
description: Two-axis review of the changes since a base ref — Standards and Spec. Use to review a branch, a change request, or work-in-progress changes.
metadata:
  optional: [to-subagent]
---

# Code Review

Two-axis review of the diff between `HEAD` and a base ref:

- **Standards** — does the code meet the repo's documented standards and the bundled smell baseline and structural bar?
- **Spec** — does the code faithfully implement the originating ticket / spec?

## 1. Pin the base ref

A given change request's base, or whatever ref was named — a commit SHA, branch, tag, `main`. Nothing named: the current branch's merge-base with the default branch; ask only when that is ambiguous.

Capture the diff command once: `git diff <base-ref>...HEAD` (three-dot, against the merge-base) and the commit list via `git log <base-ref>..HEAD --oneline`. Confirm the ref resolves (`git rev-parse`) and the diff is non-empty before dispatching anything — a bad ref or empty diff fails here, not inside two subagents.

## 2. Identify the spec source

In order: ticket references in the commit messages or change request (fetched through the tracker binding in `docs/agents/platform.md`); a path passed as an argument; a spec matching the branch or feature at the registered specs location (named by the project instruction file's `## Context documents` index or a `docs/agents/` playbook; `docs/specs/` when neither names one); else ask. No spec at all: the Spec axis skips and the report says "no spec available".

## 3. Identify the standards sources

Anything in the repo documenting how code should be written (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `docs/agents/codebase.md`, lint configs' prose). On top of whatever the repo documents, the Standards axis always carries the **smell baseline** in [smells](reference/smells.md) and the **structural bar** in [structure](reference/structure.md). Skip anything tooling already enforces.

## 4. Dispatch both axes

Each axis goes via the `to-subagent` skill so each axis runs in its own clean context; absent it, run them yourself, Standards first, in one pass each.

**Standards brief** — the diff command and commit list; the standards files found; the smell baseline and the structural bar pasted in full (the subagent has no other access to them); report every documented-standard violation (cite the standard), every baseline smell (name it, quote the hunk), and every structural finding (name the blocker, quote the hunk, sketch the simpler reframing), hard violations distinguished from judgement calls. Under 400 words.

**Spec brief** — the diff command and commit list; the spec's path or fetched content; report (a) requirements missing or partial, (b) behavior nobody asked for (scope creep), (c) requirements implemented but wrong — quoting the spec line for each, keyed to its acceptance-criterion id (`AC-N`) where the spec carries them. Under 400 words.

## 5. Aggregate

Present the two reports verbatim under `## Standards` and `## Spec` (formatting fixes only); ranking happens only within an axis — reporting them separately stops one axis from masking the other. End with a one-line summary: total findings per axis and the worst issue within each.

One collision is surfaced instead of reported twice: a spec requirement that contradicts a documented repo standard. Neither axis outranks the other there — present it as a single open question ("the spec asks X; the repo's standard says Y") for whoever owns the review to rule on.
