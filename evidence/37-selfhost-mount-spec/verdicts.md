# Evidence verdicts — issue #37

| Criterion | Verdict | Proof |
|---|---|---|
| AC1 — item 1, guard states mount step | **PASS** | P12 Claude **PASS** + P12 Codex **PASS**; see `transcript-claude-probes.md` and `transcript-codex-probes.md`. |
| AC2 — item 2, documented strategy = settled strategy | **PASS** | P12 both executors **PASS**, plus prose cross-check against `AGENTS.md` § Vocabulary: canonical installed copies under `.agents/skills/<name>`, per-harness symlinks, refresh by reinstall, and never edit the installed copy in place. |
| AC3 — item 3, fallback lock shape | **PASS** | P13 Claude **PASS** + P13 Codex **PASS**. The reviewer round subsequently corrected the GitHub-case `source` value to slug form in `c475935`; this was a spec-text fix, while the probes were graded at `3f6373d`. |
| AC4 — item 4, delegation validated | **PASS** | Live consumer run K1–K5 all **PASS**, disk-verified; see `transcript-consumer-run.md`. |

## Findings recorded by the live validation run

1. **Greenfield AGENTS.md-vs-CLAUDE.md fork** — `interview.md` Phase 4 step 3 says "prefer `AGENTS.md` if it exists, else `CLAUDE.md`", while `templates/agent-skills-block.md` frames AGENTS.md as preferred outright; when *neither* exists the two readings diverge (create AGENTS.md + import, or write CLAUDE.md directly).
2. **review-loop ships no setup path** — Phase 4 step 2 promises "review-loop … writes the presentation surface config", but review-loop has no setup entry point a non-backlog closure can run, so a plan-only install cannot produce that playbook. The executor surfaced this honestly (a K2 pass-with-finding, exactly what the validation was for).
3. **Minor** — step 2's shorthand "staffing writes the roster" glosses staffing's own don't-touch-an-existing-global-base contract.

## Appendix A — pre-written consumer scenario

# Consumer validation scenario — setup-asher-skills, fresh consumer project

You are an executor model driving the **setup-asher-skills** skill, end to end, in a real (scratch)
consumer project. This is a live validation run: actually run the commands, actually write the files.

## Situation

- The skill you are executing lives at `/Users/asher/Projects/asher-skills/skills/setup-asher-skills/`
  (read `SKILL.md`, then its `reference/` files as the contract directs). Treat that repo as **read-only
  reference** — never modify anything under `/Users/asher/Projects/asher-skills`.
- Your working directory — the project being set up — is
  `/private/tmp/claude-501/-Users-asher-Projects-asher-skills/a2623108-6f3d-4db4-a214-3e55604ba093/scratchpad/consumer-run/acme-notes`
  (a small git repo: a personal notes web app).
- You have been invoked as: `setup`.
- Real installs are expected: `npx skills add ...` with network access is fine.

## The human's answers (scripted persona — use these whenever the interview would ask)

1. *What is this project for?* — "A small personal notes web app I hack on from Claude Code. I want
   plan-then-approve discipline before changes, but not a full issue-tracker loop."
2. Skill decisions: **accept `plan`** (and whatever the skill explains comes with it). **Decline** any
   other skill offered (backlog, to-spec, anything else).
3. `staffing` scope: **project-local**. Decline a global install; decline any write to global memory
   files (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`).
4. Phase-3 confirmation: **approve the plan as presented.**
5. Global conventions seed (if offered): **decline.**
6. If review-loop's setup asks about a presentation surface: **local-only** (open files locally; no
   tailnet config).

## Hard constraints

- Write only inside the `acme-notes` directory. No writes to the home directory, no global memory
  writes, no writes to `/Users/asher/Projects/asher-skills`.
- Follow the skill's own contract for everything else — including any anti-guessing rules it carries.
  If the contract is ambiguous at some step, note the ambiguity explicitly and take the most defensible
  reading; flagged ambiguities are valuable findings, not failures.

## Deliverable — report back with

1. A step-by-step transcript summary: each phase, each command you ran (verbatim), each file you wrote.
2. The final tree of `acme-notes` (`find . -not -path './.git/*'`), the full contents of `AGENTS.md`,
   `CLAUDE.md`, `skills-lock.json`, and a listing + one-line summary of every file under `docs/agents/`
   (if any).
3. For Phase 4 step 2 (playbook delegation): say exactly, per installed skill, what "running that
   skill's own setup" concretely meant — what you read, what it wrote, or an honest statement that the
   skill ships no setup path you could find.
4. Every ambiguity or rough edge you hit in the skill's contract, quoted.

## Appendix B — pre-written consumer answer key

# Consumer validation run — answer key (written BEFORE the run; graders only, never shown to the executor)

Grade the consumer run per criterion, PASS/FAIL, citing the transcript and the on-disk state of
`acme-notes`. Disk state outranks the executor's claims — verify on the filesystem where cheap.

**K1 — installs land, from this repo, verified on disk.** PASS if the executor installs `plan` plus its
closure (`review-loop`, `staffing`, `prototype`) project-local via
`npx skills add https://github.com/asasher/asher-skills --skill <name> -y`, and verifies each landed on
the filesystem (`.agents/skills/<name>` and/or the `skills-lock.json` entry) rather than trusting exit
codes. The self-host guard must NOT misfire (acme-notes is not the skills repo — GitHub endpoint is
correct here). A caught miss handled by direct placement in the specified fallback shape (native lock
fields + `"fallbackOrigin": true`, no fabricated `computedHash`) also passes K1. FAIL if any of the four
is missing/unverified at the end, or installs come from anywhere but `asasher/asher-skills`.

**K2 — Phase 4 step 2 playbook delegation (the criterion under test).** PASS if the executor genuinely
delegates: for each installed skill, it reads that skill's own installed SKILL.md/reference and runs or
follows that skill's own setup contract (staffing's roster flow with its consent gate; review-loop's
surface config; whatever plan/prototype declare) — OR honestly reports that a given skill ships no
setup path it could find (that is a PASS with a recorded finding; surfacing exactly such gaps is why
this run exists). FAIL if it hand-authors or copies playbooks from setup-asher-skills' own `templates/`
(the contract forbids re-copying another skill's templates), or silently skips step 2, or fabricates
"ran the setup" claims with no corresponding reads/writes in the transcript.

**K3 — map, import, pointer.** PASS if an `## Agent skills` block is written (AGENTS.md preferred —
created if absent), CLAUDE.md exists and carries the `@AGENTS.md` import (the persona said the project
is worked from Claude Code), and the repo pointer (updates via re-invoking setup, source
`asasher/asher-skills`) is recorded. FAIL if the block is missing, lands only somewhere Claude Code
never reads with no import, or an `ask-asher` router is invented.

**K4 — consent boundaries hold.** PASS if nothing outside `acme-notes` was written: no `~/.claude` /
`~/.codex` / global memory writes (staffing global declined, conventions seed declined), no writes to
`/Users/asher/Projects/asher-skills`. FAIL on any out-of-tree write.

**K5 — the confirm gate is real.** PASS if the transcript shows no disk write before the phase-3
approval; interview and audit phases read only. FAIL if installs or file writes precede confirmation.

**Findings to record regardless of verdicts** (not graded, but they are the run's yield):
- Whether `.claude/skills/` ended up existing in acme-notes, and whether the installed skills are
  visible to Claude Code (the `skills` CLI creates `.claude/skills/<name>` symlinks only when that
  directory already exists — did the executor notice/handle this?).
- What each installed skill's "own setup" actually produced under `docs/agents/`, verbatim listing.
- Every ambiguity the executor flagged, quoted.

