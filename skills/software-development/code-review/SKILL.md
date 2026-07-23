---
name: code-review
description: Review the changes since a fixed point (commit, branch, tag, or change request base) along two axes — Standards (does the code follow this repo's documented standards?) and Spec (does the code match what the originating ticket or spec asked for?). Use to review a branch, a change request, or work-in-progress changes.
argument-hint: "<fixed point, change request, or nothing for the current branch>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [to-subagent]
---

# Code Review

Two-axis review of the diff between `HEAD` and a fixed point:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating ticket / spec?

Run each axis via the `to-subagent` skill so they don't pollute each other's context (absent it, run
them yourself, Standards first, in one pass each), then aggregate.

## 1. Pin the fixed point

A given change request's base, or whatever ref was named — a commit SHA, branch, tag, `main`. Nothing
named: the current branch's merge-base with the default branch; ask only when that is ambiguous.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, against the merge-base) and
the commit list via `git log <fixed-point>..HEAD --oneline`. Confirm the ref resolves
(`git rev-parse`) and the diff is non-empty before dispatching anything — a bad ref or empty diff fails
here, not inside two subagents.

## 2. Identify the spec source

In order: ticket references in the commit messages or change request (fetched through the tracker
binding in `docs/agents/platform.md`); a path passed as an argument; a spec under `docs/specs/` (or the
repo's recorded specs location) matching the branch or feature; else ask. No spec at all: the Spec axis
skips and the report says "no spec available".

## 3. Identify the standards sources

Anything in the repo documenting how code should be written (`CODING_STANDARDS.md`, `CONTRIBUTING.md`,
lint configs' prose). On top of whatever the repo documents, the Standards axis always carries the
**smell baseline** in [smells](reference/smells.md) and the **structural bar** in
[structure](reference/structure.md). Two rules bind both:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the
  baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a
  hard violation — and, like any standard here, skip anything tooling already enforces.

## 4. Dispatch both axes

**Standards brief** — the diff command and commit list; the standards files found; the smell baseline
and the structural bar pasted in full (the subagent has no other access to them); report every
documented-standard violation (cite the standard), every baseline smell (name it, quote the hunk), and
every structural finding (name the blocker, quote the hunk, sketch the simpler reframing), hard
violations distinguished from judgement calls. Under 400 words.

**Spec brief** — the diff command and commit list; the spec's path or fetched content; report (a)
requirements missing or partial, (b) behavior nobody asked for (scope creep), (c) requirements
implemented but wrong — quoting the spec line for each. Under 400 words.

## 5. Aggregate

Present the two reports under `## Standards` and `## Spec`, verbatim or lightly cleaned. Do **not**
merge or rerank findings across axes. End with a one-line summary: total findings per axis and the worst
issue within each. Don't pick a single winner across axes — that reranking is what the separation
exists to prevent.

## Why two axes

Code that follows every standard but implements the wrong thing → Standards pass, Spec fail. Code that
does exactly what the ticket asked but breaks the project's conventions → Spec pass, Standards fail.
Reporting them separately stops one axis from masking the other.
