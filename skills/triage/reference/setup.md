# Setup

Prepares a repo for the loop — and reconciles a repo an earlier version already prepared. It inventories any prior installation, scaffolds or upgrades the project playbooks, provisions the GitHub labels, decides parallelism (preparing worktree isolation when parallel), identifies the seed and check commands, confirms app access, sets the presentation surface, and verifies the repo is actually ready. Safe to re-run at any time: reconciliation never overwrites repo practice.

## Steps

1. Inventory the installation.
   - List `docs/agents/`: which playbooks exist, which of this skill's `templates/*.md` lack a counterpart, and each playbook's version stamp — the `<!-- triage-templates: ... -->` comment on line 1. Compare stamps against this skill's `templates/VERSION`.
   - No playbooks → fresh install: scaffold in step 2 and skip reconciliation. Stamp current → leave untouched. Stamp older or absent → mark for reconciliation and read `reference/migrations.md` for the changes between that vintage and now.
   - Completion criterion: every playbook is classified fresh-scaffold, current, or needs-reconciliation, with its applicable migrations listed.

2. Scaffold and reconcile the playbooks.
   - Missing → write it from this skill's `templates/`, prepending the stamp line with the version from `templates/VERSION`.
   - Needs-reconciliation → work section by section: a section verbatim-identical to an older shipped default updates to the current default; a section that diverges is repo practice — leave it, and flag it only where a listed migration changed the contract around it. Apply the listed migrations mechanically; they preserve repo values (a roster rewrite keeps the repo's model choices, a plan-format change keeps its directory and naming). Re-stamp each reconciled playbook.
   - Never delete repo-authored content. Where a migration and repo practice genuinely conflict, show the conflict and let the user decide.
   - Completion criterion: every template has a current-stamped counterpart, and every applied migration or flagged conflict is reported.

3. Provision GitHub labels.
   - Reconcile the role→label mapping in `docs/agents/triage-policy.md` with the repo's actual GitHub labels: list the existing labels, map each role (readiness: `ready-for-agent`, `ready-for-human`, `needs-info`; work-type: `bug`, `enhancement`, `refactor`; exclusions) to an existing label where one already fits, and create the missing ones with a clear name and description. Label creation is an upsert, not an approval gate — creating a label is cheap and reversible; report what was created.
   - Write the final mapping back into `triage-policy.md` so the skill's roles resolve to real labels.
   - When GitHub tools are unavailable, list the labels the user must create and the role each fills, and record it as a blocker.
   - Completion criterion: every role resolves to a label that exists in the repo, or the missing labels are listed as an explicit blocker.

4. Choose parallel or sequential, and prepare isolation.
   - Ask the user whether issue work should run in parallel (many worktrees standing up the stack at once) or sequentially (one at a time). This intent, crossed with what the repo can support, sets the parallelism verdict.
   - **Sequential** → record `serialize-verification`; no isolation work is needed.
   - **Parallel** → follow `reference/worktree-isolation.md`: classify the regime, run the collision probes, and detect any isolation the repo already has.
     - Already isolated → `parallel-safe`; defer to it.
     - Local-isolatable but not isolated → offer to scaffold the isolation layer. Write isolation code only with explicit approval; approved → `parallel-safe`, declined → `serialize-verification`.
     - Cloud-singleton with no per-worktree cloud envs → local isolation can't make it safe; explain why, record `serialize-verification`, and note the manual path to true parallel (per-worktree deployment + auth tenant).
   - Even when `parallel-safe`, agree with the user which classes of issues must still serialize — destructive operations on a shared tenant, real third-party endpoints without per-worktree credentials, features needing deliberately distinct users — and record them as the **serialized exception lane**.
   - Completion criterion: the parallelism verdict and its exception lane are set, match what the repo can actually support, and any approved isolation scaffolding is in place.

5. Identify seed and checks.
   - Determine how an empty stack is brought to a state that exercises the product's features: a real seed command, a load-from-checked-in-dataset command, or none (state is produced by driving the app). Do not assume a `db:seed` exists — most repos lack one.
   - Read an existing machine-readable command catalog if present (e.g. `.intent/`) to populate the check commands rather than asking.
   - On a re-run, verify every previously recorded command still exists — a recorded check or seed command missing from the repo's scripts is drift; update it.
   - Completion criterion: the seed regime and command (or "none — drive the app") and the check commands are identified and still real.

6. Confirm app access.
   - Verification and evidence capture only work if the agent can actually exercise the app. Identify the app's form factor(s) and confirm a working **driver** for every surface the loop will verify:
     - **CLI** → shell access and the command entrypoint.
     - **Web** → a browser the agent can drive (e.g. agent-browser, a Playwright MCP, or the harness's built-in browser).
     - **Mobile** → an emulator/simulator the agent can boot, plus a driver that installs the build and interacts with it.
     - **Desktop** → a windowed environment the agent can control (computer-use tooling or an OS automation driver).
   - Confirm an **evidence path** for the same surfaces: screenshots for static states, screen recordings (convertible to GIF) for flows, terminal transcripts for CLI output.
   - Confirm the agent can **mint a session unattended**, matching the app's auth model: a test account, an OTP/magic-link inbox the agent can read, a token in the environment — whatever the model needs.
   - Where a driver, capture path, or auth path is missing, help set it up — install the tool, create the test account, wire the inbox — with the user's approval. Anything that cannot be set up is a blocker for the surfaces it covers, and `verify`/`evidence` will inherit it.
   - Completion criterion: every app surface the loop will verify has a named driver, capture method, and auth path — or an explicit blocker.

7. Set the presentation surface.
   - Present the shipped default from `reference/presenting.md` — a singular tailnet surface (`tailscale serve`): one stable URL root private to the user's devices, documents as static paths, live prototypes as port proxies, Funnel off. Ask whether the user wants the default, local-only, or something else — and design the alternative with them if so.
   - For the tailnet default: confirm `tailscale` is installed and logged in, capture the machine's URL root, and record the publish / expose / reap commands verified against the installed version.
   - Ask whether the machine should stay awake for review pauses the harness isn't covering — including lid-closed on battery, which needs more than `caffeinate` — or whether "the surface is up when the machine is" is fine. Record the choice as the keep-awake line; no keep-awake machinery is part of the default path.
   - Completion criterion: the Presenting section of `environment.md` records a working surface or an explicit local-only choice.

8. Write the contracts into the playbooks.
   - Record the results in `docs/agents/environment.md`: dev-stack startup, isolation regime and how to bring up an isolated stack, seed regime and command, auth/session minting, the app drivers and evidence-capture tooling from the access audit, the presentation surface, the parallelism verdict with its serialized exception lane, and the model-staffing roster (orchestrator / builder by surface / checker / floor, per harness the loop runs from, plus the succession line — per `reference/staffing.md`). Record the check commands in `verifying.md` and the repo's evidence expectations in `evidence.md`.
   - Offer to fill the remaining baselines — the dependency convention in `triage-policy.md`, branch conventions, plan format, review criteria — with this repo's real values. The templates are baselines, not the contract.
   - Completion criterion: `environment.md` states the isolation, seed, parallelism, staffing, and presenting contracts the loop reads, or the user has chosen to keep a baseline section.

9. Fold in existing repo practice.
   - The scaffolded playbooks are self-contained: the debugging discipline, test-first build technique, and review standards ship inlined, so nothing external is required. But a repo may already have its own practice — a dev-loop skill, a testing guide, debugging docs, review checklists.
   - Where one exists, offer to fold it into (or substitute it for) the matching playbook section, so the loop follows house practice instead of the shipped default. Edit only with the user's approval.
   - Completion criterion: each playbook either keeps its inlined default or records the repo's own practice, per the user's choice.

10. Verify readiness and confirm.
   - Offer a smoke test of the recorded contracts — bring up the stack, seed it, mint a session, drive one interaction through the recorded driver, capture one throwaway artifact, publish a throwaway page to the presentation surface and confirm it resolves, and run the check gate once — so a wrong command or a broken driver surfaces now, not mid-loop. When the verdict is `parallel-safe`, run it in a throwaway worktree to confirm isolation actually holds; tear the worktree down after. On a re-run, also sweep orphaned surface path handlers whose worktrees are gone.
   - Report a readiness checklist: playbooks present and current-stamped; GitHub labels provisioned; dependency convention set; seed and checks identified and real; app driver, evidence capture, and auth confirmed per surface (and smoke-tested if run); presentation surface working; parallelism verdict and exception lane; playbooks tailored to house practice where the repo has one; migrations applied and conflicts resolved.
   - Completion criterion: the user has a clear ready / not-ready verdict for each item and knows whether `triage` will verify in parallel or serialized.
