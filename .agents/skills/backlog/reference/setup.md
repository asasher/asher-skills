# Setup

Prepares a repo for the loop — and reconciles a repo an earlier version already prepared. It inventories any prior installation, scaffolds or upgrades the project playbooks, binds the platforms (tracker, change review, version control, harness) and provisions the tracker's role labels, decides parallelism (preparing worktree isolation when parallel), identifies the seed and check commands, confirms app access, ensures the sibling skills it composes (`staffing`, `review-loop`, `plan`, `prototype`) are present, and verifies the repo is actually ready. Safe to re-run at any time: reconciliation never overwrites repo practice.

## Steps

1. Inventory the installation.
   - List `docs/agents/`: which playbooks exist, which of this skill's `templates/*.md` lack a counterpart, and each playbook's version stamp — the `<!-- backlog-templates: ... -->` comment on line 1. Compare stamps against this skill's `templates/VERSION`. This is the playbook-stamp inventory for the DEV playbooks backlog still owns.
   - A legacy install may still carry `<!-- backlog-section: ... -->` markers in `AGENTS.md`/`CLAUDE.md` (the old picking-models install). Setup no longer installs or owns those — the `staffing` skill does; on reconcile, leave any already-installed sections as repo practice (do NOT delete them) and ensure the siblings per steps 7–8 instead.
   - No playbooks → fresh install: scaffold in step 2 and skip reconciliation. Stamp current → leave untouched. Stamp older or absent (including the retired `<!-- triage-templates: ... -->` form) → mark for reconciliation and read `reference/migrations.md` for the changes between that vintage and now.
   - Completion criterion: every playbook is classified fresh-scaffold, current, or needs-reconciliation, with its applicable migrations listed.

2. Scaffold and reconcile the playbooks.
   - Missing → write it from this skill's `templates/`, prepending the stamp line with the version from `templates/VERSION`.
   - Needs-reconciliation → work section by section: a section verbatim-identical to an older shipped default updates to the current default; a section that diverges is repo practice — leave it, and flag it only where a listed migration changed the contract around it. Apply the listed migrations mechanically; they preserve repo values (a roster rewrite keeps the repo's model choices, a plan-format change keeps its directory and naming). Re-stamp each reconciled playbook.
   - Never delete repo-authored content. Where a migration and repo practice genuinely conflict, show the conflict and let the user decide.
   - Completion criterion: every template has a current-stamped counterpart, and every applied migration or flagged conflict is reported.

3. Bind the platforms.
   - Walk the user through the four ports in `docs/agents/platform.md`, one question each: where issues are tracked (GitHub, a local on-disk tracker, GitLab, other), where changes are reviewed (usually the same host; local otherwise), which version control (git, jj colocated or native), and which harness dispatches threads. Default each answer to what the repo already shows — a `github.com` remote, an existing `.backlog/` directory, a `.jj/` — and confirm rather than interrogate.
   - For a platform with a shipped default (GitHub, local), fill the binding's verb slots from it, adjusted to this repo. For anything else, derive the binding with the user: name the tool or API, exercise every verb live against the real platform, and record only commands that worked; record any verb the platform cannot express as a gap with its fallback, per `platform.md` § Custom bindings.
   - Provision the tracker's role labels: reconcile the role→label mapping in `docs/agents/backlog-policy.md` with the tracker's actual labels — list what exists, map each role (readiness: `ready-for-agent`, `in-flight`, `ready-for-human`, `needs-info`; work-type: `bug`, `enhancement`, `refactor`; exclusions) to an existing label where one fits, and create the missing ones with a clear name and description. Label creation is an upsert, not an approval gate — creating a label is cheap and reversible; report what was created. On the local binding there is nothing to provision — roles are frontmatter values; scaffold `.backlog/issues/` instead and offer to import any backlog the user has elsewhere.
   - Write the final mapping back into `backlog-policy.md` and the verified verbs into `platform.md` so the skill's roles resolve to real mechanics.
   - When the tracker's tools are unavailable, list the labels the user must create and the role each fills, and record it as a blocker.
   - Completion criterion: all four bindings are recorded with verified verbs (or explicit gaps), and every role resolves on the tracker — or the missing pieces are listed as an explicit blocker.

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
   - On a re-run, verify every previously recorded command still exists — a recorded check, seed, or platform-binding command missing from the repo or the machine is drift; update it.
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

7. Ensure the review-loop skill (presentation & review).
   - The presentation surface and the interactive review loop are owned by the **`review-loop`** skill (composed by name). Ensure it is present: the `setup-asher-skills` installer guarantees the siblings; absent it, tell the user to install `review-loop`.
   - review-loop's own setup records this repo's surface config (tailnet root, surface dir, publish/proxy commands, keep-awake) into `environment.md` § Presenting. backlog does not install the surface itself.
   - Degrade note: absent `review-loop`, presentation falls back to a local open of the rendered document.
   - Completion criterion: `review-loop` is present and its surface config resolves, or the gap is reported.

8. Ensure the staffing skill (model roster).
   - The model roster (rankings, roles, capability matrix, task-pins, fallback ladder) is owned by the **`staffing`** skill (composed by name). Ensure it is present; staffing's own setup writes the roster — global base plus this project's delta — with user consent, probing what this machine can actually staff. backlog does not install the picking-models sections.
   - The enhancement and diagnose branches also compose the **`plan`** and **`prototype`** siblings by name — ensure those are present too; each installs its own `docs/agents/` playbook (planning, prototyping).
   - Completion criterion: the four siblings (`staffing`, `review-loop`, `plan`, `prototype`) resolve, or the gaps are reported.

9. Write the contracts into the playbooks.
   - Record the results in `docs/agents/environment.md`: dev-stack startup, isolation regime and how to bring up an isolated stack, seed regime and command, auth/session minting, the app drivers and evidence-capture tooling from the access audit, and the parallelism verdict with its serialized exception lane. `environment.md` § Presenting is a pointer the `review-loop` skill fills (its setup records the surface config); § Model staffing is the `staffing` skill's roster (its setup writes it) — backlog does not write either here. The platform bindings live in `platform.md` from step 3. Record the check commands in `verifying.md` and the repo's evidence expectations — including the presentation contract for the bound review surface — in `evidence.md`.
   - Offer to fill the remaining baselines — the dependency convention in `backlog-policy.md`, branch conventions, plan format, review criteria — with this repo's real values. The templates are baselines, not the contract.
   - Completion criterion: `environment.md` states the isolation, seed, and parallelism contracts (its § Presenting and § Model staffing being sibling-owned pointers) and `platform.md` the bindings the loop reads, or the user has chosen to keep a baseline section.

10. Fold in existing repo practice.
   - The scaffolded playbooks are self-contained: the debugging discipline, test-first build technique, and review standards ship inlined, so nothing external is required. But a repo may already have its own practice — a dev-loop skill, a testing guide, debugging docs, review checklists.
   - Where one exists, offer to fold it into (or substitute it for) the matching playbook section, so the loop follows house practice instead of the shipped default. Edit only with the user's approval.
   - Completion criterion: each playbook either keeps its inlined default or records the repo's own practice, per the user's choice.

11. Verify readiness and confirm.
   - Offer a smoke test of the recorded contracts — bring up the stack, seed it, mint a session, drive one interaction through the recorded driver, capture one throwaway artifact, round-trip the tracker binding (create a throwaway issue, label it, comment, close it — or the local-file equivalent), verify an artifact renders inline on the bound review surface per `evidence.md`'s presentation contract, publish a throwaway page to the presentation surface and confirm it resolves, and run the check gate once — so a wrong command or a broken binding surfaces now, not mid-loop. When the verdict is `parallel-safe`, run it in a throwaway worktree to confirm isolation actually holds; tear the worktree down after. On a re-run, also sweep orphaned surface path handlers whose worktrees are gone, and sweep the review hub registry via the **`review-loop`** skill's sweep.
   - Report a readiness checklist: playbooks present and current-stamped; platform bindings verified per verb; tracker roles provisioned; dependency convention set; seed and checks identified and real; app driver, evidence capture, and auth confirmed per surface (and smoke-tested if run); the four sibling skills (`staffing`, `review-loop`, `plan`, `prototype`) present and their playbooks/surface-config resolving; parallelism verdict and exception lane; playbooks tailored to house practice where the repo has one; migrations applied and conflicts resolved.
   - Completion criterion: the user has a clear ready / not-ready verdict for each item and knows whether `backlog` will verify in parallel or serialized.
