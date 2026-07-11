# Playbook: Environment

> Project playbook for this repo. Shared — read by any backlog subskill that builds a branch, runs, or verifies a skill (`implement`, `verify`, `evidence`, `diagnose`, the PR step, the review fixer) and by `run` for the parallelism verdict. There is no assumed app or software stack: exercising a skill means running a situated probe through an executor harness. `setup` fills the isolation, seed, and parallelism sections from its audit.

## Branching & deploys

- Base branch: _<e.g. main>_ — create worktrees and work branches from it, and target change review at it. Sync it per `platform.md` § Version control before branching (on the local tracker binding, `run`'s claim commit is the fork point).
- Branch naming: _<e.g. `<issue-number>-<slug>`>_.
- What a change review produces: _<e.g. a merged skill-source change, or nothing until release>_.
- What a merge produces: _<e.g. a published skill release, an installer refresh, or no automatic deployment>_.

## Running locally

- Skill source layout: _<e.g. `skills/<name>/SKILL.md` with bundled references, scripts, and evals>_.
- How to exercise a skill: _<executor-harness command or dispatch that runs one situated probe>_.
- App / stack: **none assumed** — the runtime surface is the executor harness loading the skill and responding to a probe.

## Worktree isolation

> Set by `setup` per `reference/worktree-isolation.md`.

- Regime: **local-isolatable** — checked-in skill files and stdlib-only scripts are completely isolated by the worktree unless the repository records an external shared resource below.
- How to create an isolated skill run for one worktree: _<run the executor with that worktree's skill source and eval scenario>_.
- **Shared-singleton list** — every resource two concurrent worktrees would contend for. Files and stdlib scripts inside each worktree are not shared singletons. _<Fill the table for any external executor session, cache, publishing target, or account; otherwise "none — files and scripts are worktree-local".>_

  | Singleton | Collision mode | Locally isolatable? |
  |-----------|----------------|---------------------|
  | _<e.g. one mutable executor session>_ | _<one run can change the context observed by another>_ | _<yes — fresh session / no>_ |
  | _<e.g. one publishing target>_ | _<concurrent releases overwrite the same destination>_ | _<yes — namespaced preview / no>_ |

## Seed data

- Seed regime: **the skill's `evals/` situated probe scenarios**.
- Command (if any): _<command that selects or materializes a probe fixture, or "none — scenarios are checked in">_.
- What a fresh probe run contains: _<the scenario, deployment-context files, and prewritten answer key>_.
- **Drive-to-feature path** — load the skill in its real executor context, submit the situated scenario, preserve the cited transcript, and grade it against the prewritten key. _<add any skill-specific entrypoint or prerequisite>_.

## Authenticating for testing

- Auth model: _<executor login or token, or "none">_.
- How an agent mints an executor session: _<start a fresh in-session or CLI executor without sharing mutable context>_.
- Test accounts / where credentials live: _<environment or secrets store; never hardcode or echo secrets>_.

## Driving the app & capturing evidence

> For this domain, “driving” means running a probe through the executor harness. Set by `setup`'s access audit; read by `verify` and `evidence`.

- Form factor(s): **executor-harness skill behavior**, plus _<CLI scripts or a visual artifact surface, if the skill has them>_.
- Driver per surface: _<in-session executor; independent CLI executor; direct shell invocation for scripts>_.
- Independent runtime verification: _<independent CLI executor with a self-contained prompt, selected through the staffing skill/playbook>_.
- Evidence capture per surface: **cited executor transcripts and a per-criterion pass/fail verdict table**; _<rendered screenshots or a short flow artifact when the skill produces a visual surface>_.
- Supporting tools: _<transcript capture, renderer, or "none">_.
- Gaps: _<surfaces the agent cannot drive or capture, and the fallback; or "none">_.

## Presenting to the human

> Owned by the **`review-loop`** skill (composed by name): the presentation surface and interactive review. Its setup records this repo's surface configuration here; backlog does not install that surface.

## Model staffing

> Owned by the **`staffing`** skill (composed by name): executor roles, rankings, capability pins, and fallback order. `run` and every reference that spawns work resolve staffing questions against that playbook; do not bake named models into this baseline.

## Parallelism verdict

> Read by `run` before dispatch.

- Verdict: _<parallel-safe | serialize-verification>_ — files plus stdlib scripts are worktree-isolated; any stricter result must name an external shared singleton or a user preference.
- If serialized, why: _<either "user preference — sequential by choice" or the external shared singleton that forces it>_.
- Serialized exception lane: _<issue classes that must serialize even when parallel-safe — shared publishing, mutable external accounts, or "none">_.
