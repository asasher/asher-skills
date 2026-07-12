# Live consumer validation evidence

Live consumer validation run for issue item 4: a fresh scratch project, `acme-notes`, driven through the full setup flow and graded K1–K5 against the pre-written `consumer-key.md`.

# Consumer validation run — executor report (Opus subagent), setup-asher-skills on acme-notes

Checker note: on-disk end state independently verified by the checker after the run (tree, symlinks,
skills-lock.json, CLAUDE.md, docs/agents/, no AGENTS.md, ~/.claude/CLAUDE.md mtime 00:12 predates run,
asher-skills repo git-clean). Disk matched this report on every checked point.

---

## 1. Step-by-step transcript

**Routing decision.** Read SKILL.md → the routing rule: greenfield (no `## Agent skills` block, no
installed asher-skills) runs `setup`. Confirmed greenfield: no remote, no AGENTS.md/CLAUDE.md, no
skills-lock.json, no .claude/.agents/docs. Ran **setup**.

**Phase 1 — Audit (silent, three surfaces).**
- Repo: `git remote -v` → empty (no remote); no AGENTS.md, no CLAUDE.md, no block, no installed skills
  anywhere (project or global ~/.claude|.agents/skills), no docs/agents/. Not the self-host case (remote
  is not asasher/asher-skills; no local skills/ dir).
- Machine: reachable roster taken from the existing global base in ~/.claude/CLAUDE.md § Staffing
  (gpt-5.6-sol/terra, sonnet-5, opus-4.8, fable-5); `which codex` → Codex CLI present;
  `grep '^## Conventions' ~/.claude/CLAUDE.md` → `## Conventions` already present globally.
- Project: answer — "small personal notes web app… plan-then-approve discipline… not a full
  issue-tracker loop." Keys to catalog row `plan` (not `backlog`).

**Phase 2 — Interview (scripted persona).** Recommended `plan`; persona accepted. Closure computed:
plan ⇒ review-loop + staffing + prototype (told the persona which siblings came along and why). Declined
all other skills (backlog, to-spec, etc.). staffing scope → project-local; declined global install and
any global-memory write.

**Phase 3 — Confirm.** Plan (4 skills project-local; CLAUDE.md block; docs/agents/staffing.md; repo
pointer; no global write) approved as presented.

**Phase 4 — Write.** Commands run verbatim:

    mkdir -p .claude/skills   # ensure symlink target exists (worked from Claude Code)
    npx skills add https://github.com/asasher/asher-skills --skill plan -y
    npx skills add https://github.com/asasher/asher-skills --skill review-loop -y
    npx skills add https://github.com/asasher/asher-skills --skill staffing -y
    npx skills add https://github.com/asasher/asher-skills --skill prototype -y
    mkdir -p docs/agents

Every install verified on the filesystem (not by exit code): all four landed at .agents/skills/<name>
with SKILL.md present and a .claude/skills/<name> symlink; skills-lock.json has a real tool computedHash
for each → no direct-placement fallback needed, no fallbackOrigin entries.

Files written (all inside acme-notes):
- docs/agents/staffing.md — staffing project override (deltas-only).
- CLAUDE.md — `## Agent skills` block + repo pointer + scope/surface notes.

Global conventions seed (step 5): not offered — `## Conventions` already present in ~/.claude/CLAUDE.md
(only seeded when absent); persona would have declined anyway. No home-directory writes:
~/.claude/CLAUDE.md mtime (00:12) predates the run (15:5x).

## 2. Final state

Tree: .agents/skills/{plan,prototype,review-loop,staffing} (canonical copies: 7/5/13/8 files);
.claude/skills/{plan,prototype,review-loop,staffing} (symlinks -> ../../.agents/skills/<name>);
CLAUDE.md; README.md; docs/agents/staffing.md; index.html; skills-lock.json; src/app.js.

AGENTS.md — does not exist. Not created (see ambiguity #1). Pre-existing README.md, index.html,
src/app.js untouched.

CLAUDE.md carries: `## Agent skills` table (plan / review-loop / prototype / staffing, all project
scope, plain-language purposes), "How they fit together" closure note, staffing-scope note (project-local,
inherits global roster, deltas in docs/agents/staffing.md), review-surface note (local-only), and the
repo pointer (source asasher/asher-skills, updates via re-invoking setup-asher-skills; skills source
HTML comment).

skills-lock.json: four entries, each {source: "asasher/asher-skills", sourceType: "github",
skillPath: "skills/<name>/SKILL.md", computedHash: <real tool hash>}.

docs/agents/staffing.md — staffing project override for acme-notes: inherits the global base in
~/.claude/CLAUDE.md § Staffing, records zero deltas, notes the run was project-only with no global write.

## 3. Phase 4 step 2 — what "running each skill's own setup" concretely meant

- staffing → ran its setup (project-only branch). Read reference/install-and-reconcile.md +
  machine-audit.md. Since a global base already exists, staffing's scope-flow dictates "offer a project
  override (deltas), do not overwrite global." Concretely wrote docs/agents/staffing.md as a deltas-only
  override (none for this repo) and left ~/.claude/CLAUDE.md untouched. This is the one skill in the
  closure with a real setup command.
- review-loop → ships no setup path I could find. Its command surface is serve | await | sweep only —
  there is no setup/install command, and nothing in the skill writes the "presentation surface config"
  playbook that interview.md Phase 4 step 2 attributes to it (on the asher-skills repo itself that file,
  environment.md, is written by backlog setup, not review-loop). Because the persona chose local-only,
  and review-loop's documented degradation for "no surface recorded" is exactly "open the rendered file
  locally," the correct end-state needs no surface playbook — so none was written. Recorded the
  local-only choice as a note in CLAUDE.md instead. (See rough edge #2.)
- plan → ships no setup path. Thin composer, "no runtime of its own, no server, no scripts." It reads an
  optional project playbook but ships nothing that writes one. Nothing to run; nothing written.
- prototype → ships no setup path. Thin composer; it optionally reads docs/agents/prototyping.md but
  explicitly says "absent a playbook, the technique's defaults apply." Nothing to run; nothing written.

## 4. Ambiguities / rough edges in the contract (quoted)

1. AGENTS.md vs CLAUDE.md — "prefer if exists" vs "preferred." The interview says write the block into
   "the harness memory file — prefer AGENTS.md if it exists, else CLAUDE.md." (interview.md Phase 4 §3),
   but the block template's own header says "setup writes this section into the target repo's AGENTS.md
   (preferred) or CLAUDE.md" (agent-skills-block.md) — which reads as "create AGENTS.md preferentially."
   These conflict when neither file exists. Resolution: followed the interview's more specific wording —
   AGENTS.md does not exist, so wrote to CLAUDE.md and did not create an AGENTS.md. A consequence worth
   noting: the same step's @AGENTS.md-import guarantee ("ensure its CLAUDE.md begins with an @AGENTS.md
   import") is scoped "when the block lands in AGENTS.md", so with the block directly in CLAUDE.md no
   import is needed — self-consistent, but only because I took the "else CLAUDE.md" branch. A run that
   instead created AGENTS.md would have produced a different, two-file layout. This is the single most
   consequential fork in the contract for a greenfield repo.

2. review-loop's "own setup" is asserted but not shipped. interview.md Phase 4 §2 states "review-loop
   (or backlog setup, which composes it) writes the presentation surface config," and SKILL.md §"How it
   composes" says "review-loop's surface config" is guaranteed by delegation. But review-loop exposes no
   setup command and writes no surface playbook — in a plan-only closure (no backlog) there is no skill
   whose setup writes the surface-config playbook. Combined with the interview's "What this skill does
   not do: Write a docs/agents/ playbook itself," this leaves the surface decision with no
   contract-sanctioned author. Defensible outcome here (local-only == review-loop's no-surface default)
   made it harmless, but the contract over-promises: it names review-loop as the writer of a playbook
   review-loop cannot write.

3. "staffing writes the roster (global base + project delta, with consent)" vs a pre-existing global
   base + a project-local persona. interview.md Phase 4 §2 phrases staffing's output as "global base +
   project delta," implying both. But staffing's own scope-flow branches on "Global staffing rules
   already exist → … offer to add a project override," and the persona chose project-local with no
   global write. The interview's phrasing reads as though the global base is always (re)written;
   staffing's contract says don't touch an existing one. Resolution: followed staffing's contract —
   wrote only the project delta, left global untouched. The two documents are reconcilable but the
   interview's shorthand invites re-writing a global base that already exists.

4. Minor — `-y` self-reporting caveat did not bite. interview.md warns "`-y` mode can under-report the
   count (it reported 'Installed 3 skills' when 4 were requested)" and that npx skills add "can print
   '✖ No matching skills found' and exit 0." On skills v1.5.16 each single-skill install reported
   "Installed 1 skill" accurately and all four verified on disk — so the documented hazard is real
   guidance but did not manifest here. Worth noting the contract is written against v1.5.15; this
   machine has v1.5.16, and behavior matched.

Net: the skill drove cleanly end-to-end to a functional, correctly-scoped, this-repo-only install with
no home writes. The only substantive contract gaps are #1 (AGENTS.md/CLAUDE.md fork on greenfield) and
#2 (review-loop's surface-config setup is promised but not shipped for a plan-only closure).

---

# Checker grading (K1–K5, per consumer-key.md)

- K1 PASS — all four skills (plan + closure) installed project-local from asasher/asher-skills GitHub
  endpoint (correct: acme-notes is not the skills repo, self-host guard did not misfire), each verified
  on the filesystem, real tool computedHash in the lock; no fallback needed. Verified on disk by checker.
- K2 PASS — genuine delegation: staffing's own setup run (deltas-only project override written per its
  scope-flow); review-loop/plan/prototype honestly reported as shipping no setup path, with the
  review-loop over-promise recorded as a finding (exactly the yield this run exists to produce). No
  hand-authored playbooks from setup's templates; no fabricated "ran the setup" claims.
- K3 PASS with caveat — block written with pointer and plain-language purposes, directly in CLAUDE.md,
  which Claude Code reads natively (no import needed; persona works from Claude Code). No ask-asher
  router. Caveat: the key anticipated AGENTS.md created-if-absent; the executor followed interview.md's
  literal "prefer AGENTS.md if it exists, else CLAUDE.md" and created no AGENTS.md. The FAIL clause
  (block missing / invisible to Claude Code / router invented) is not triggered. The divergence is a
  contract ambiguity in the skill (interview.md vs templates/agent-skills-block.md header), recorded as
  finding #1 for the issue thread.
- K4 PASS — no writes outside acme-notes: ~/.claude/CLAUDE.md mtime predates the run; asher-skills repo
  git-status clean after the run; conventions seed not written.
- K5 PASS — transcript shows reads only through Phases 1–3; first disk write (mkdir .claude/skills)
  occurs in Phase 4 after the scripted approval. Disk mtimes (15:54–15:56) consistent with a
  single post-approval write burst.

Findings the key asked to record regardless:
- .claude/skills visibility: the executor created .claude/skills BEFORE installing (citing the Phase-4
  caveat), so the tool laid all four per-harness symlinks and the skills are visible to Claude Code —
  direct evidence the new caveat sentence in interview.md works in situ.
- docs/agents/ yield: exactly one file, staffing.md (deltas-only override); no surface playbook (see
  finding #2 — no contract-sanctioned author in a plan-only closure).
- Ambiguities: four, quoted in §4 above (greenfield AGENTS.md fork; review-loop setup over-promise;
  staffing "global base + delta" shorthand; v1.5.15-vs-v1.5.16 caveat did not bite).
