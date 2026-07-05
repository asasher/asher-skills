# Playbook: Planning Enhancements

> Project playbook for this repo. The backlog `plan` subskill reads this file for the threshold, format, review conduct, and approval; the gates are in the skill's `reference/plan.md`. The plan structure below draws on Matt Pocock's `to-prd` skill (MIT) — tailor everything to this team's conventions.

## Plan-size threshold

Write a plan when any of these hold; otherwise skip planning and implement directly:

- The change touches more than one subsystem or public interface.
- It needs new data models, migrations, or external dependencies.
- It is risky, hard to reverse, or affects more than ~1 day of work.

_Adjust these triggers to this team._

## Format and location

- Plans are **HTML documents** committed to the repo: `plans/<issue-number>-<slug>.html` (or this repo's convention: _<add yours>_). HTML is the surface for both sides: Mermaid diagrams, syntax-highlighted code, embedded prototype screenshots — whatever makes the plan easiest for a human to review — and the implementing agents read the same file from disk.
- Keep the file self-contained (inline styles/scripts, no external fetches) so it renders anywhere, including a plain browser open.

## What a plan covers

- **Problem statement** — the problem from the user's perspective, and the solution the same way.
- **User stories** — a numbered, extensive list: "As an _actor_, I want _feature_, so that _benefit_." Cover the feature's full surface, not just the happy path.
- **Definition of done** — explicit, testable acceptance criteria, each checkable pass/fail against a running app. This is the contract verify and evidence consume.
- **Implementation decisions** — modules built or modified, interface changes, schema changes, API contracts, architectural calls. No file paths or code snippets — they rot. Exception: a prototype-validated snippet that encodes a decision more precisely than prose can (a state machine, reducer, schema, type shape) — inline the decision-rich part and note it came from a prototype.
- **Test seams** — the public seams the acceptance criteria will be tested at, and the surfaces deliberately left untested with why (see `implementing.md` § What deserves a test). Prefer existing seams, at the highest point possible; the fewer, the better.
- **Evidence required, risks, out of scope.**

## Prototype when paper isn't enough

Run the skill's `prototype` step (`reference/prototype.md` + `docs/agents/prototyping.md`) when a design question blocks the plan. Triggers — any one is enough:

- More than one plausible state model, data shape, or API surface survives discussion, and the choice is expensive to reverse later.
- The plan is accumulating speculative "should handle X" reasoning about state transitions that driving a real model would settle in minutes.
- The issue or the human signals visual uncertainty — no settled design, or several plausible layouts for the surface.

Don't prototype what reading the code, the spec, or existing patterns can settle — a prototype answers a question, it doesn't replace thinking. Fold the answer into the plan; for UI prototypes, embed the variant screenshots with the chosen one marked, so the decision record outlives the prototype.

_Adjust these triggers to this team._

## Review, approval, and commit

- Open the rendered HTML for the human — a browser, the harness's preview, whatever the environment offers. Who approves and how: _<add yours>_.
- If approval changes scope, update the plan before coding.
- Once approved, **commit the plan to the work branch before implementation is dispatched** — implementing agents must find it on disk.
- Posterity: after approval, comment a compact markdown digest of the plan on the issue — headings, the acceptance criteria, and Mermaid blocks where the tracker renders them (GitHub does; a local issue file holds them as source) — plus a repo link to the committed HTML. Any screenshots in the digest follow the presentation contract in `evidence.md`. On the local binding this digest is a PR-bound lifecycle write: it rides the work branch per `platform.md`. _Adjust or drop this write if this team doesn't want plans mirrored to the tracker._
