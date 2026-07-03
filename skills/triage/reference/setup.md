# Setup

Prepares a repo for the loop. It scaffolds the project playbooks, provisions the GitHub labels the role model needs, decides whether work runs in parallel or sequentially (and prepares worktree isolation when parallel), identifies the seed and check commands, confirms the agent can drive, authenticate to, and capture evidence from the app, and confirms the repo is actually ready. Run once per repo, and again to fill a gap.

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

5. Confirm app access.
   - Verification and evidence capture only work if the agent can actually exercise the app. Identify the app's form factor(s) and confirm a working **driver** for every surface the loop will verify:
     - **CLI** → shell access and the command entrypoint.
     - **Web** → a browser the agent can drive (e.g. agent-browser, a Playwright MCP, or the harness's built-in browser).
     - **Mobile** → an emulator/simulator the agent can boot, plus a driver that installs the build and interacts with it.
     - **Desktop** → a windowed environment the agent can control (computer-use tooling or an OS automation driver).
   - Confirm an **evidence path** for the same surfaces: screenshots for static states, screen recordings (convertible to GIF) for flows, terminal transcripts for CLI output.
   - Confirm the agent can **mint a session unattended**, matching the app's auth model: a test account, an OTP/magic-link inbox the agent can read, a token in the environment — whatever the model needs.
   - Where a driver, capture path, or auth path is missing, help set it up — install the tool, create the test account, wire the inbox — with the user's approval. Anything that cannot be set up is a blocker for the surfaces it covers, and `verify`/`evidence` will inherit it.
   - Completion criterion: every app surface the loop will verify has a named driver, capture method, and auth path — or an explicit blocker.

6. Write the contracts into the playbooks.
   - Record the results in `docs/agents/environment.md`: dev-stack startup, isolation regime and how to bring up an isolated stack, seed regime and command, auth/session minting, the app drivers and evidence-capture tooling from the access audit, the parallelism verdict, and the model-staffing roster (lead/delegate/floor per harness the loop runs from). Record the check commands in `verifying.md`, and set the **presentation mode** in `evidence.md` from the repo's visibility: `public-inline` for a public repo, `private-links` for a private one (GitHub's image proxy cannot render committed images inline in private-repo PR bodies).
   - Offer to fill the remaining baselines — the dependency convention in `triage-policy.md`, branch conventions, plan format, review criteria — with this repo's real values. The templates are baselines, not the contract.
   - Completion criterion: `environment.md` states the isolation, seed, and parallelism contracts the loop reads, or the user has chosen to keep a baseline section.

7. Fold in existing repo practice.
   - The scaffolded playbooks are self-contained: the debugging discipline, test-first build technique, and review standards ship inlined, so nothing external is required. But a repo may already have its own practice — a dev-loop skill, a testing guide, debugging docs, review checklists.
   - Where one exists, offer to fold it into (or substitute it for) the matching playbook section, so the loop follows house practice instead of the shipped default. Edit only with the user's approval.
   - Completion criterion: each playbook either keeps its inlined default or records the repo's own practice, per the user's choice.

8. Verify readiness and confirm.
   - Offer a smoke test of the recorded contracts — bring up the stack, seed it, mint a session, drive one interaction through the recorded driver, capture one throwaway artifact, and run the check gate once — so a wrong command or a broken driver surfaces now, not mid-loop. When the verdict is `parallel-safe`, run it in a throwaway worktree to confirm isolation actually holds; tear the worktree down after.
   - Report a readiness checklist: playbooks present; GitHub labels provisioned; dependency convention set; seed and checks identified; app driver, evidence capture, and auth confirmed per surface (and smoke-tested if run); parallelism verdict; playbooks tailored to house practice where the repo has one.
   - Completion criterion: the user has a clear ready / not-ready verdict for each item and knows whether `triage` will verify in parallel or serialized.
