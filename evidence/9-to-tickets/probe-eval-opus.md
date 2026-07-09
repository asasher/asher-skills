# Probe-eval transcript — Opus in-session executor (HEAD c85c6a7)

Executor: Opus subagent via the Agent tool, read-only, SKILL.md + references in context, answer key withheld.
Method: `docs/patterns/probe-evals.md` (dual-executor situated dry-run probes). Grading: correct-action-and-citation
against `skills/to-tickets/evals/probes.md` § Answer key.

---

**P1 (ac-1).** Yes on all three. Frontmatter names a `user-invocable: true` skill described as "Split a decided direction into backlog-ready tickets with blocking edges." No file imports another skill's files (SKILL.md § Dependency surface: "no file here imports or reads another skill's files. It composes siblings by name only"). Directory carries the shipped-primitive layout (SKILL.md, README.md, agents/, reference/, templates/, evals/). **PASS**

**P2 (ac-2).** Three pointer kinds: bundled references, project playbooks (dependency convention in backlog-policy.md + tracker binding in platform.md), sibling skills. Siblings: consumes `to-spec`'s output as primary, also a plan or raw conversation, composed by name, no import. `backlog` modelled as a project playbook it emits *into*, not an imported sibling ("to-tickets emits **into** backlog's convention, it does not import backlog"). **PASS**

**P3 (ac-3).** Yes — spec at `docs/specs/foo.md` is the primary input (SKILL.md § How a split happens step 1). Alternates: a plan and the raw current conversation. **PASS**

**P4 (ac-4).** No — "all the models / all the logic / all the UI" is the horizontal-layer anti-pattern (slicing.md § Draft vertical slices). Wants vertical slices (tracer bullets); three properties: narrow-but-complete path through every layer, demoable on its own, sized to one fresh context window. **PASS**

**P5 (ac-5).** No — not a single vertical slice. Wide-refactor exception: expand → migrate-in-batches → contract. Trigger is BOTH conditions: mechanical AND high blast radius. **PASS**

**P6 (ac-6).** Do not publish now — quiz the user first (the human-confirmation step): settles granularity and blocking edges, iterate until approved, nothing publishes before approval. Differs from to-spec's pure-synthesis no-interview posture. **PASS**

**P7 (ac-7) — LOAD-BEARING.** (a) Create A first, then B and C in either order — blockers created before dependents because the tracker assigns an id at creation ("a ticket can only reference its blocker once that id exists"). (b) Each dependent carries, verbatim, `- [ ] depends on #N` as a task-list line in the ticket body (N = A's id); backlog-policy.md § Dependencies. (c) `backlog run` treats any unchecked, unclosed dependency as blocked and skips it, so B and C are skipped until A closes. **PASS**

**P8 (ac-8).** Publish through the tracker binding in platform.md (GitHub via `gh`, ticket == a GitHub issue), body from templates/ticket.md. Skill's own word is generic "ticket" (never assumes GitHub vocabulary). **PASS**

**P9 (ac-9).** No — do not apply `ready-for-agent` on a fresh split. Default: leave readiness to `backlog groom`. Noted option: apply on approval — Matt Pocock's posture (the quiz is the human confirmation). **PASS**

**P10 (ac-10).** No file paths / code snippets in a ticket (they rot); single exception is a prototype-validated snippet. Separately: to-tickets never edits the source spec or parent issue ("The parent is never touched"). **PASS**

**P11 (ac-11).** openai.yaml well-formed per codex-compat.md (interface block with display_name/short_description/default_prompt + policy block); `allow_implicit_invocation: false` correct for a tracker-publishing operator skill. **PASS**

**P12 (ac-12).** N/A — the eval file was withheld by design.

---

Verdict: 11/11 answerable probes pass (P12 N/A), all with correct citations. No genuine ambiguity found across P1–P11.
