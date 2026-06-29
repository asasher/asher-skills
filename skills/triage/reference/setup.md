# Setup

Prepares a repo for the loop. It scaffolds the project playbooks, provisions the GitHub labels the role model needs, decides whether work runs in parallel or sequentially (and prepares worktree isolation when parallel), identifies the seed and check commands, and confirms the repo is actually ready. Run once per repo, and again to fill a gap.

## Steps

1. Scaffold the playbooks.
   - For each file in this skill's `templates/`, write it to `docs/agents/<name>.md` in the target repo.
   - Skip any playbook that already exists. Never overwrite without explicit confirmation.
   - Completion criterion: every template exists at `docs/agents/`, either freshly written or already present and left untouched.

2. Provision GitHub labels.
   - Reconcile the role→label mapping in `docs/agents/triage-policy.md` with the repo's actual GitHub labels: list the existing labels, map each role (readiness: `ready-for-agent`, `ready-for-human`, `needs-info`; work-type: `bug`, `enhancement`, `refactor`; exclusions) to an existing label where one already fits, and create the missing ones — with a clear name and description — on the user's approval.
   - Write the final mapping back into `triage-policy.md` so the skill's roles resolve to real labels.
   - When GitHub tools are unavailable, list the labels the user must create and the role each fills, and record it as a blocker.
   - Completion criterion: every role resolves to a label that exists in the repo, or the missing labels are listed as an explicit blocker.

3. Choose parallel or sequential, and prepare isolation.
   - Ask the user whether issue work should run in parallel (many worktrees standing up the stack at once) or sequentially (one at a time). This intent, crossed with what the repo can support, sets the parallelism verdict.
   - **Sequential** → record `serialize-verification`; no isolation work is needed.
   - **Parallel** → follow `reference/worktree-isolation.md`: classify the regime, run the collision probes, and detect any isolation the repo already has.
     - Already isolated → `parallel-safe`; defer to it.
     - Local-isolatable but not isolated → offer to scaffold the isolation layer. Write isolation code only with explicit approval; approved → `parallel-safe`, declined → `serialize-verification`.
     - Cloud-singleton with no per-worktree cloud envs → local isolation can't make it safe; explain why, record `serialize-verification`, and note the manual path to true parallel (per-worktree deployment + auth tenant).
   - Completion criterion: the parallelism verdict is set, matches what the repo can actually support, and any approved isolation scaffolding is in place.

4. Identify seed and checks.
   - Determine how an empty stack is brought to a state that exercises the product's features: a real seed command, a load-from-checked-in-dataset command, or none (state is produced by driving the app). Do not assume a `db:seed` exists — most repos lack one.
   - Read an existing machine-readable command catalog if present (e.g. `.intent/`) to populate the check commands rather than asking.
   - Completion criterion: the seed regime and command (or "none — drive the app") and the check commands are identified.

5. Write the contracts into the playbooks.
   - Record the results in `docs/agents/environment.md`: dev-stack startup, isolation regime and how to bring up an isolated stack, seed regime and command, auth/session minting, and the parallelism verdict. Record the check commands in `verifying.md`.
   - Offer to fill the remaining baselines — the dependency convention in `triage-policy.md`, branch conventions, plan format, review criteria — with this repo's real values. The templates are baselines, not the contract.
   - Completion criterion: `environment.md` states the isolation, seed, and parallelism contracts the loop reads, or the user has chosen to keep a baseline section.

6. Offer external skills.
   - The playbooks may defer to installed skills. Offer to install the matching ones and tell the user the exact command, e.g.:
     - `diagnosing-bugs`, `tdd` — `npx skills@latest add mattpocock/skills --skill diagnosing-bugs tdd`
   - Prefer composing with an in-repo dev-loop skill (`diagnose`, `diagnosing-bugs`, `tdd`) already present rather than duplicating it. Install only what the user approves.
   - Completion criterion: the user has chosen which external skills to install, and approved installs have run.

7. Verify readiness and confirm.
   - Offer a smoke test of the recorded commands — bring up the stack, seed it, and run the check gate once — so a wrong command surfaces now, not mid-loop. When the verdict is `parallel-safe`, run it in a throwaway worktree to confirm isolation actually holds; tear the worktree down after.
   - Report a readiness checklist: playbooks present; GitHub labels provisioned; dependency convention set; seed and checks identified (and smoke-tested if run); parallelism verdict; external skills installed.
   - Completion criterion: the user has a clear ready / not-ready verdict for each item and knows whether `triage` will verify in parallel or serialized.
