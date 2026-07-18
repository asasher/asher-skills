# setup-asher-skills — situated dry-run probes

Tier-1 situated probes per `docs/agents/probe-evals.md`. They test whether an executor model, situated
mid-task with this skill in context, does the right next thing — and whether the references stand on their
own when cited.

## Method

- **Executors are the deployment targets, run on both sides** (`environment.md` § Model staffing, checker
  role): a **Claude** subagent in-session (Agent tool, Opus) **and** `codex exec -s read-only
  --skip-git-repo-check` for the gpt-5.6-sol side. A probe passes only if **both** executors pass it.
- **Context:** command-surface session — the skill's `SKILL.md` and `reference/` files are available to the
  executor (this is how the skill deploys: a user invokes it and the model reads its files). Point the
  executor at `skills/system/setup-asher-skills/`.
- **Require citations.** Every answer must cite the file and the exact sentence that decided it, so
  pointer-following is observable, not vibes.
- **Answer key is written before any run** and kept in `answer-key.md` (not here). Grade pass/fail against it.
- **Ambiguity is a valid answer** — instruct executors to flag anything under-specified; flagged ambiguities
  are findings.
- These are probe specifications and prewritten keys, not claims that a live executor run has passed.

## Probes

**P1 — the three-part audit.** "You've just been invoked with `setup` in a fresh project. You've recommended
nothing yet. What do you audit before recommending anything, and how do you find out which models the machine
can reach? Cite the file and sentence."

**P2 — one decision at a time + dependency guarantee.** "The user says the project is a shipping web product.
You're in the interview. The user accepts `plan`. Exactly what do you install as a result, and what do you say
to the user? Cite the file and sentence."

**P3 — undeclared external request.** "Mid-interview the user says: 'Oh, also install the TDD skill from Matt
Pocock's repo.' No selected skill declares it in `metadata.external`. What do you do? Cite the file and
sentence."

**P4 — the context block + playbook writes.** "The user has approved the plan and the installs have run. What
do you write into the repo, and where does each thing go? Be specific about the `## Agent skills` block and the
`docs/agents/` playbooks. Cite the file and sentence."

**P5 — audit mode on re-invoke, no version stamps.** "You're invoked on a project that already has a
`## Agent skills` block; it was set up three months ago. What do you do, and specifically how do you detect
that an installed skill has drifted from the repo's current version? Cite the file and sentence."

**P6 — project-first scope.** "The user accepts both `staffing` and `backlog`. What scope does each get, and
what, if anything, do you ask the user about scope? Cite the file and sentence."

**P7 — routing paradox.** "You're invoked with no argument on a repo that HAS skills installed under
`.claude/skills/` and `.agents/skills/` but has NO `## Agent skills` block (it was set up by the old backlog).
Do you run setup or audit, and why? Cite the file and sentence."

**P8 — primary-only install.** "You're in audit mode. A skill has a real `.agents/skills/<name>` primary and
project lock provenance but no `.claude/skills/<name>` alias because Claude is not used. Is it valid, and what
do you inspect at project and global scope? Cite the file and sentence."

**P9 — alias versus independent copy.** "During an audit `.agents/skills/backlog` is a real directory. Compare
`.claude/skills/backlog` as a symlink to it versus an independent directory. Which is valid, and may reconcile
replace the independent directory? Cite the file and sentence."

**P10 — undeclared foreign provenance.** "During an audit you find `writing-great-skills` installed from
`mattpocock/skills` per `skills-lock.json`, but no active Asher skill declares it as external. What finding do
you raise and what may you do automatically? Cite the file and sentence."

**P11 — self-catalog.** "You're auditing the `asasher/asher-skills` repo itself, on a local branch ahead of
origin. What do you use as the catalog to diff installed skills against, and why not the fetched remote? Cite
the file and sentence."

**P12 — self-host write guard.** "You're invoked with `setup` on the `asasher/asher-skills` repo itself (git
remote is `asasher/asher-skills`; the closure you're installing — `backlog`, `diagnosing-bugs`,
`prototype`, `research`, `review-loop`, `staffing` — has its sources under the repo's categorized `skills/`). You've reached Phase 4 (Write); the
user approved the plan. Which install command do you emit for those repo-owned skills, how does each one end
up loadable by the harness (name the paths that exist afterwards), and what do you still write to the repo?
Cite the file and sentence."

**P13 — batch landing and silent miss.** "In Phase 4 the scope already has `staffing`; the new closure is
`review-loop`, `plan`. You run one batch add over all three names. The tool under-reports its count and `plan`
is absent afterwards despite exit 0. What do you verify, what do you preserve, and how do you repair only the
miss? Cite the file and sentence."

**P14 — optional sibling.** "The user selects `plan`; neither `prototype` nor `research` is selected or
installed. What is the closure and setup order? Repeat with both optional siblings already installed. Cite the
declarations."

**P15 — pre-write cycle.** "A local branch accidentally declares required `a → b → a`. When is this found,
what is reported, and has anything been written?"

**P16 — no setup branch.** "A selected skill installs successfully but declares no setup pointer. Is that a
failure, and what runs next?"

**P17 — partial setup failure.** "The dependency-first order is staffing → review-loop → plan. Review-loop
setup fails after staffing succeeds. What state is recorded, does plan run, and what does retry do?"

**P18 — greenfield instruction files.** "Exercise Codex-only and Claude-enabled projects where neither
AGENTS.md nor CLAUDE.md exists, then existing AGENTS-only, CLAUDE-only, and two-file layouts. What layout does
setup produce or preserve?"

**P19 — owner boundaries.** "In a plan-only closure, who writes review-loop's presentation section and
staffing's project delta? May setup-asher-skills open or copy either owner's setup reference?"

**P20 — declared external consent path.** "A selected skill declares
`[{name: browser-driver, kind: codex-plugin, source: https://github.com/acme/browser-driver, capability: Drive
an authenticated browser, version: v2}]`. Walk the pre-write validation, disclosure, consent, provider install,
capability check, and lock write. What happens if consent is declined? Cite the file and sentence."

**P21 — external compiler conflicts.** "Two skills in one closure declare the same external name but different
versions; a third skill has no external declaration. What does schema 3 emit, and when is the conflict found?"

**P22 — strict global verification.** "A global skill exists at `~/.agents/skills/staffing`, its primary is a
symlink, and no project `skills-lock.json` mentions it. Which lock supplies global provenance, is the primary
valid, and may reconciliation replace it? Cite the file and sentence."

**P23 — declared provider variant.** "`staffing` declares Codex and Claude overlays; both harnesses are
confirmed active. Which fields stay shared, which paths may overlays replace, what mount shape is published,
what provenance is locked, and what happens if publication fails after the first provider? Cite the file and
sentence."

**P24 — variant audit taxonomy.** "Audit a declared two-provider package with a missing Claude mount, Codex
bytes installed under Claude, a changed effective tree, and a provider `SKILL.md` edit. Name the distinct
findings. Contrast an unvaried skill whose Claude alias is an independent directory."

**P25 — global owner boundary.** "Both native global files already contain user, Staffing, and Presentation
sections. Global migration is approved. In what order do the two owners write modules and pointers, what does
unreadable-module behavior do, and which existing bytes may each owner change?"

**P26 — staffing pointer fire/non-fire/all triggers.** "Using the installed Codex staffing pointer, decide
whether it loads the deferred module for each isolated next action: edit a leaf file with no routing decision;
choose a model; delegate; create a child; create a worktree; use browser; use computer; use imagegen; start a
watcher; recover from route loss. State the exact trigger responsible for every load."

**P27 — staffing unreadable and project-delta order.** "A model choice is required. First the deferred
staffing module is readable and the project has a sparse staffing delta; then repeat with the module
unreadable. What is loaded, in what order, and may dispatch continue?"

**P28 — presentation pointer fire/non-fire/unreadable.** "Using the installed Claude presentation pointer,
decide whether it loads the deferred module while merely editing HTML, then before opening, serving,
publishing, and changing a presentation route. Repeat a publish attempt with the module unreadable."

**P29 — cross-owner four-module barrier.** "Presentation modules for both providers and only the Codex
Staffing module stage successfully; Claude Staffing staging fails. What exact global-file bytes may change?
After all four stage and read back, one global has an unowned `## Conventions` block. What may apply, in what
order, and how does finalize behave? What must a second successful full reconcile do?"
