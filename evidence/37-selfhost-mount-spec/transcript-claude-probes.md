# Claude probe evidence

Claude-side executor (Opus), running probes P12 and P13 against `skills/setup-asher-skills` at commit `3f6373d`, graded against `evals/answer-key.md`.

# Claude-side executor (Opus subagent) — P12 + P13 answers

## P12 — self-host write guard

Commands emitted. For each repo-owned skill in the closure (backlog, plan, review-loop, staffing, prototype), I emit a local-source install pointed at the repo's own root, not the GitHub endpoint:

    npx skills add <repo-root> --skill backlog -y
    npx skills add <repo-root> --skill plan -y
    npx skills add <repo-root> --skill review-loop -y
    npx skills add <repo-root> --skill staffing -y
    npx skills add <repo-root> --skill prototype -y

Decided by reference/interview.md Phase 4 step 1, "Local source, not the endpoint" bullet: "Install repo-owned skills from the repo's own root as a local source — npx skills add <repo-root> --skill <name> -y — never from the https://github.com/asasher/asher-skills endpoint, which may lag the local branch." Same rule in SKILL.md: "repo-owned skills are still mounted, from the repo's own root as a local source."

That these repo-owned skills must still be mounted (source presence is not an install) is fixed by interview.md Phase 4 step 1: "In the self-host case, a repo-owned skill — one whose install source is this repo's own skills/<name>/ — still gets mounted: source presence is not an install... a register-only write (block + pointer + playbooks with nothing mounted) leaves the closure non-functional."

How each becomes loadable — paths that exist afterwards. Per interview.md Phase 4 step 1, "skills/<name>/ is never an install destination" bullet, each install produces, for <name>:
- a canonical copy at .agents/skills/<name> (a real directory copy, an "identical twin" of skills/<name>/, per the "build product" bullet),
- a per-harness symlink .claude/skills/<name> -> ../../.agents/skills/<name>,
- a skills-lock.json entry with sourceType: "local" and a tool-computed computedHash.

The harness loads from .agents/skills/ / .claude/skills/, never from skills/ — cited in the same step: "The harness loads installed skills from .agents/skills/ / .claude/skills/, never from skills/." skills/<name>/ itself is never a destination (SKILL.md: "skills/<name>/ itself is never an install destination").

One operational caveat to apply: "the tool creates the symlink only when .claude/skills/ already exists — when the project is worked from Claude Code, ensure that directory exists before installing, or add the symlink afterwards" (interview.md Phase 4 step 1). Since this repo is worked from Claude Code, I ensure .claude/skills/ exists first (or add the symlink after).

After each command I verify on the filesystem, not the exit code, and fall back to direct placement on a miss — interview.md Phase 4 step 1: "After each npx skills add, verify <name> actually landed on the filesystem... Do not trust the exit code." (This is the P13 path.)

What I still write to the repo (identical to any other install — interview.md Phase 4 step 1: "Still write the ## Agent skills block, the repo pointer, and the guaranteed playbooks, exactly as for any other install."):
1. Guaranteed docs/agents/ playbooks by delegation — run each installed skill's own setup, never re-copy templates (step 2): staffing writes the roster (global base + project delta, with consent), review-loop/backlog setup writes the presentation-surface config, backlog setup writes its docs/agents/ suite.
2. The ## Agent skills block into the harness memory file, "prefer AGENTS.md if it exists, else CLAUDE.md" (step 3). Because this repo is worked from Claude Code and the block lands in AGENTS.md, I also guarantee the @AGENTS.md import at the top of CLAUDE.md (step 3: "ensure its CLAUDE.md begins with an @AGENTS.md import... without it the map is invisible"). Here that import already exists.
3. The repo pointer from templates/repo-pointer.md (step 4).
4. Consent-gated global conventions only if phase 1 found no ## Conventions in the global memory file (step 5) — on this machine it's already present, so this is skipped.

Note on staffing scope: it's the one skill that may go global, routed through staffing's own consent gate (interview.md Phase 2, scope bullet); absent that consent it installs project-local like the rest.

## P13 — silent install miss

How I determine whether plan actually installed. I do not trust the exit code. Per interview.md Phase 4 step 1: "After each npx skills add, verify <name> actually landed on the filesystem: check the project install dir (.claude/skills/<name>/ or .agents/skills/<name>/) and/or the skills-lock.json entry for <name>. Do not trust the exit code: npx skills add can print '✖ No matching skills found' and exit 0 after installing nothing." So I check for .claude/skills/plan/ (or .agents/skills/plan/) and a plan entry in skills-lock.json. That printed message with exit 0 is exactly the documented false-success, so verification is mandatory here.

What I do if it did not install — the direct-placement fallback. Per interview.md Phase 4 step 1: "On a verified miss, place the skill's files directly instead of trusting the failed install. This is the direct-placement fallback: copy from this repo's own skills/<name>/ in the self-host case, else fetch the skill from the https://github.com/asasher/asher-skills endpoint. It never breaks pull-only-from-this-repo, and it mirrors the mount shape the tool would have produced — a canonical copy at .agents/skills/<name> plus the per-harness symlink .claude/skills/<name> where that harness is present."

So I place plan as: a canonical copy at .agents/skills/plan + the per-harness symlink .claude/skills/plan -> ../../.agents/skills/plan.

Then I hand-write the skills-lock.json entry in the specified fallback shape (interview.md Phase 4 step 1, final paragraph): the tool's native fields — source (the GitHub endpoint here / repo-root path in the self-host case), sourceType ("github" / "local"), and skillPath for github sources — plus exactly one extension field "fallbackOrigin": true, and no computedHash. "Never fabricate computedHash... and add no free-form fields." Finally I tell the user the entry is fallback-origin; audit-mode treats a fallbackOrigin/missing-computedHash entry as expected, not drift.

Ambiguity to flag. The command as written targets the GitHub endpoint (https://github.com/asasher/asher-skills), which is the non-self-host install path. The probe doesn't state which repo we're in:
- If this is a normal consumer project, the command is correct, and the fallback fetches plan from the GitHub endpoint (source https://github.com/asasher/asher-skills, sourceType: "github", with skillPath).
- If this is actually the self-host case (repo remote is asasher/asher-skills, per P12), then emitting the endpoint command is itself the bug — the guard requires npx skills add <repo-root> --skill plan -y, and the fallback must copy from this repo's own skills/plan/ with sourceType: "local". The "✖ No matching skills found" failure would be an expected symptom of using the wrong (endpoint) source in that case.

Either way the verification step and the fallback contract are the same; only the fallback source and lock-entry source/sourceType differ, keyed on whether it's the self-host case.

# Grader verdicts (checker): P12 PASS, P13 PASS (both per answer-key.md)
