# Playbook: Environment

> Project playbook for a skill-authoring repo. Shared — read by any backlog subskill that builds, runs, or verifies a skill. There is no assumed app or software stack: exercising a skill means running a situated probe through an executor harness. `setup` fills the agent-readiness section from its certification. Repo facts accrete here; machine state is never recorded — a capability is checked at use, and a failed check warns and names its fallback.

## Branching & deploys

- Base branch: _<e.g. main>_ — create worktrees and work branches from it, and target change review at it.
- Branch naming: _<e.g. `<issue-number>-<slug>`>_.
- What a change review produces: _<e.g. a merged skill-source change, or nothing until release>_.
- What a merge produces: _<e.g. a published skill release, an installer refresh, or no automatic deployment>_.

## Running locally

- Skill source layout: _<e.g. `skills/<name>/SKILL.md` with bundled references, scripts, and evals>_.
- How to exercise a skill: _<executor-harness command or dispatch that runs one situated probe>_.
- App / stack: **none assumed** — the runtime surface is the executor harness loading the skill and responding to a probe.

## Agent-readiness

> The standard lives in the `agent-ready-codebase` reference skill; this section records this repo's **answers**. `backlog setup` certifies against the checklist — pass, or a punch list of gaps — and `backlog build` dispatches only on a full pass. Working copies always go through the project-owned `worktree` skill; dispatch receives the prepared directory and never asks a harness for native isolation. For a skill-authoring repo, checked-in skill files and stdlib-only scripts are worktree-local by construction — the items below mostly pass for free.

1. **Worktrees** — the `worktree` skill can create, inspect, and remove working copies here: _<pass | gap>_.
2. **Stack per worktree** — an isolated skill run per worktree: _<pass — run the executor with that worktree's skill source and eval scenario | gap>_.
3. **Auth per worktree** — an agent can mint an executor session in each copy independently: _<pass | gap>_.
4. **Seed** — the `evals/` probe scenarios cover what the skills offer, including new behavior: _<pass | gap>_.

**Shared singletons — use ≠ change.** _<external executor session, cache, publishing target, or account; otherwise "none — files and scripts are worktree-local">_. Most rows collide only on change: a ticket that changes a shared resource is marked at the tracker.

| Singleton          | Collides on     | Notes         |
| ------------------ | --------------- | ------------- |
| _<row, or "none">_ | _<change only>_ | _<add yours>_ |

**Punch list** — the gaps certification found, each groomable as its own ticket: _<the list, or "none — certified <date>">_.

## Seed data

- Seed regime: **the skill's `evals/` situated probe scenarios**.
- Command: _<command that selects or materializes a probe fixture, or “none — scenarios are checked in”>_.
- What a fresh probe run contains: _<the scenario, deployment-context files, and prewritten answer key>_.
- Exercise-to-criterion path: load the skill in its real executor context, submit the situated scenario, preserve the cited transcript, and grade it against the prewritten key. _<add any skill-specific entrypoint or prerequisite>_.

## Authenticating for testing

- Auth model: _<executor login or token, or “none”>_.
- How an agent mints an executor session: _<start a fresh in-session or CLI executor without sharing mutable context>_.
- Test accounts / where credentials live: _<environment or secrets store; never hardcode or echo secrets>_.
- Record here only the liveness probe — never an observed identity; who is authed is checked at use, not written down.

## Driving behavior & capturing evidence

- Form factor(s): **executor-harness skill behavior**, plus _<CLI scripts or a visual artifact surface, if the skill has them>_.
- Driver per surface: _<in-session executor; independent CLI executor; direct shell invocation for scripts>_.
- Independent runtime verification: _<independent CLI executor with a self-contained prompt, selected through staffing>_.
- Evidence capture per surface: **cited executor transcripts and a per-criterion pass/fail verdict table**; _<rendered screenshots or a short flow artifact when the skill produces a visual surface>_.
- Gaps: _<surfaces the agent cannot drive or capture, and the fallback; or “none”>_.

## Presenting to the human

> No standing presentation surface is bound here. Review happens on the change request bound in `platform.md` § Change review; evidence media uploads via the `to-web` sibling and embeds by URL per `evidence.md`. Where the `to-tailnet` skill is installed, it may be invoked on demand when the human needs an artifact on another device without publishing it.

## Model staffing

> Owned by the `staffing` skill. Do not bake named models into this baseline.
