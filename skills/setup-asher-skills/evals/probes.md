# setup-asher-skills — situated dry-run probes

Tier-1 situated probes per `docs/patterns/probe-evals.md`. They test whether an executor model, situated
mid-task with this skill in context, does the right next thing — and whether the references stand on their
own when cited.

## Method

- **Executors are the deployment targets, run on both sides** (`environment.md` § Model staffing, checker
  role): a **Claude** subagent in-session (Agent tool, Opus) **and** `codex exec -s read-only
  --skip-git-repo-check` for the gpt-5.5 side. A probe passes only if **both** executors pass it.
- **Context:** command-surface session — the skill's `SKILL.md` and `reference/` files are available to the
  executor (this is how the skill deploys: a user invokes it and the model reads its files). Point the
  executor at `skills/setup-asher-skills/`.
- **Require citations.** Every answer must cite the file and the exact sentence that decided it, so
  pointer-following is observable, not vibes.
- **Answer key is written before any run** and kept in `answer-key.md` (not here). Grade pass/fail against it.
- **Ambiguity is a valid answer** — instruct executors to flag anything under-specified; flagged ambiguities
  are findings.

## Probes

**P1 — the three-part audit.** "You've just been invoked with `setup` in a fresh project. You've recommended
nothing yet. What do you audit before recommending anything, and how do you find out which models the machine
can reach? Cite the file and sentence."

**P2 — one decision at a time + dependency guarantee.** "The user says the project is a shipping web product.
You're in the interview. The user accepts `plan`. Exactly what do you install as a result, and what do you say
to the user? Cite the file and sentence."

**P3 — pull from this repo only.** "Mid-interview the user says: 'Oh, also install the TDD skill from Matt
Pocock's repo.' What do you do? Cite the file and sentence."

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

**P8 — `.agents/skills/` scan.** "You're in audit mode. A skill is installed only under `.agents/skills/`
(the Codex harness dir), not `.claude/skills/`. Do you see it, and which directories do you read to find
what's installed? Cite the file and sentence."

**P9 — cross-harness overlap.** "During an audit you find the skill `backlog` present in BOTH
`.claude/skills/backlog` and `.agents/skills/backlog`, where the former is a symlink to the latter. Is this
drift? How do you report it, versus two independent copies? Cite the file and sentence."

**P10 — foreign source.** "During an audit you find `writing-great-skills` installed from `mattpocock/skills`
per `skills-lock.json`. What finding do you raise and what do you propose? Cite the file and sentence."

**P11 — self-catalog.** "You're auditing the `asasher/asher-skills` repo itself, on a local branch ahead of
origin. What do you use as the catalog to diff installed skills against, and why not the fetched remote? Cite
the file and sentence."
