# Playbook: Environment

> Project playbook for a skill-authoring repo. Shared — read by any backlog subskill that builds, runs, or
> verifies a skill. There is no assumed app or software stack: exercising a skill means running a situated
> probe through an executor harness. `setup` fills the isolation, seed, and parallelism sections from its audit.

## Branching & deploys

- Base branch: _<e.g. main>_ — create worktrees and work branches from it, and target change review at it.
- Branch naming: _<e.g. `<issue-number>-<slug>`>_.
- What a change review produces: _<e.g. a merged skill-source change, or nothing until release>_.
- What a merge produces: _<e.g. a published skill release, an installer refresh, or no automatic deployment>_.

## Running locally

- Skill source layout: _<e.g. `skills/<name>/SKILL.md` with bundled references, scripts, and evals>_.
- How to exercise a skill: _<executor-harness command or dispatch that runs one situated probe>_.
- App / stack: **none assumed** — the runtime surface is the executor harness loading the skill and responding to a probe.

## Worktree isolation

- Regime: **local-isolatable** — checked-in skill files and stdlib-only scripts are isolated by the worktree unless the repository records an external shared resource below.
- How to create an isolated skill run for one worktree: _<run the executor with that worktree's skill source and eval scenario>_.
- Shared-singleton list: _<external executor session, cache, publishing target, or account; otherwise “none — files and scripts are worktree-local”>_.

## Seed data

- Seed regime: **the skill's `evals/` situated probe scenarios**.
- Command: _<command that selects or materializes a probe fixture, or “none — scenarios are checked in”>_.
- What a fresh probe run contains: _<the scenario, deployment-context files, and prewritten answer key>_.
- Exercise-to-criterion path: load the skill in its real executor context, submit the situated scenario, preserve the cited transcript, and grade it against the prewritten key. _<add any skill-specific entrypoint or prerequisite>_.

## Authenticating for testing

- Auth model: _<executor login or token, or “none”>_.
- How an agent mints an executor session: _<start a fresh in-session or CLI executor without sharing mutable context>_.
- Test accounts / where credentials live: _<environment or secrets store; never hardcode or echo secrets>_.

## Driving behavior & capturing evidence

- Form factor(s): **executor-harness skill behavior**, plus _<CLI scripts or a visual artifact surface, if the skill has them>_.
- Driver per surface: _<in-session executor; independent CLI executor; direct shell invocation for scripts>_.
- Independent runtime verification: _<independent CLI executor with a self-contained prompt, selected through staffing>_.
- Evidence capture per surface: **cited executor transcripts and a per-criterion pass/fail verdict table**; _<rendered screenshots or a short flow artifact when the skill produces a visual surface>_.
- Gaps: _<surfaces the agent cannot drive or capture, and the fallback; or “none”>_.

## Presenting to the human

> Owned by the `review-loop` skill. Its setup records this repo's surface configuration here.

## Model staffing

> Owned by the `staffing` skill. Do not bake named models into this baseline.

## Parallelism verdict

- Verdict: _<parallel-safe | serialize-verification>_.
- If serialized, why: _<user preference or the external singleton that forces it>_.
- Serialized exception lane: _<shared publishing, mutable external accounts, or “none”>_.
