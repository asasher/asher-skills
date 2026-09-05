---
name: code-review
description: Review changes against documented standards and their issue or spec. Use for a branch, PR, or work-in-progress diff.
metadata:
  optional: [to-subagent]
---

# Code review

Read the change on two axes: **Standards**, whether it meets documented repo rules and the bundled structural guidance; and **Spec**, whether it implements the requested behavior. This is one read-only pass. Return findings; leave fixes to the owner.

## 1. Pin the inputs

Resolve the named PR base or supplied base ref to a SHA, and record the head SHA. Without a named base, use the default branch; ask only when that is ambiguous. Use immutable refs in `git diff <base-sha>...<head-sha>` and `git log <base-sha>..<head-sha> --oneline`. Confirm refs resolve and the diff is nonempty before starting. When reviewing uncommitted work, capture the staged and unstaged diff too, identify that snapshot in the report, and return findings without granting a committed-head approval.

Read the issue referenced by the PR or commits with `gh issue view <n> --comments`. When it names a blessed spec, read that revision; for a child, retain its narrower acceptance criteria and their parent mapping. Otherwise use the issue text or the supplied spec. With no source, report the Spec axis as unavailable instead of inventing requirements.

## 2. Read the standards

Read the repo's documented standards and the bundled [smells](reference/smells.md) and [structural bar](reference/structure.md). Skip rules already enforced by tooling. Apply the guidance to changed behavior and structure, respecting the issue's settled decisions and delegated scope.

## 3. Size the pass

For a coherent change that fits one context, review both axes here. Split the axes into concurrent read-only passes via `to-subagent` only when their context or reasoning load warrants it. Absent that sibling, cover both axes in this context and state any coverage limitation. File count alone is not a reason to split. When another worker owns runtime verification, neither this pass nor its axis workers runs tests or mutates fixtures.

Each axis receives the pinned refs, relevant source material, and the required report format. A Standards worker also receives the bundled guidance; a Spec worker receives the actual spec and slice scope. Keep the briefs self-contained.

## 4. Report

Under **Standards**, report documented-standard violations and structural problems with the rule, quoted hunk, and concrete failure scenario or maintenance cost. Under **Spec**, report missing, partial, incorrect, or unrequested behavior, quoting the requirement and its `AC-N` where present.

Distinguish **blocking findings** from **optional suggestions**. A preference or alternate design without a demonstrated cost is optional. Do not demand a redesign of settled intent; a contradiction between the spec and a repo standard is one product question for a ruling. Unrelated pre-existing cleanup stays outside the change.

Keep each axis concise without dropping actionable findings. Preserve separately dispatched reports under their own headings, formatting fixes only. End with blocking and optional counts per axis, any missing review coverage, and the input head and base. Recheck refs before returning; input movement makes the report stale and requires a new pass before approval.
