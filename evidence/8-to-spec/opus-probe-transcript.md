# to-spec probe eval — Opus in-session executor transcript

Executor: fresh Opus subagent via the Agent tool (no answer key in context; reasoned cold from the skill files at `skills/to-spec/`). Method per `docs/patterns/probe-evals.md` and `skills/to-spec/evals/probes.md`.

**P1 (ac-1).** Yes. Frontmatter has `name: to-spec`, `user-invocable: true`, and a `description` beginning "Turn the current conversation into a spec … Pure synthesis, no interview" — a user-invocable conversation→spec synthesis skill. No file imports another skill's files: the Dependency surface states it, and a grep for cross-skill paths found none. The directory carries the shipped-primitive layout: SKILL.md, README.md, agents/openai.yaml, reference/, templates/, evals/. Cite — SKILL.md:80–81 ("self-contained at the file level … no file here imports or reads another skill's files").

**P2 (ac-2).** Three pointer kinds: Bundled references (own reference/ + templates/spec.md), Project playbooks (repo spec conventions — default docs/specs/; presentation-surface config when review-loop is used), Sibling skills. Siblings: exactly one — `review-loop` — optional, not a hard dependency. Cite — SKILL.md:76–78.

**P3 (ac-3).** No — do not ask. The undecided secondary flow is recorded as a line in the spec's Notes, not bounced back. Cite — reference/synthesis.md:12–14 ("record it as a line in the spec's Notes … a question bounced back to the user is not").

**P4 (ac-4).** A spec — a repo doc at docs/specs/<name>.md — the direction document consumed by `to-tickets`; not a ticket, coarser than a plan. Cite — SKILL.md:54–55.

**P5 (ac-5).** Not right; the correct word is ticket. The skill avoids "issue" because it is GitHub's word and the pair is tracker-agnostic. Cite — reference/synthesis.md:65–66.

**P6 (ac-6).** Core (always): Problem, Solution, User stories, Implementation decisions, Out of scope, Notes. Dev-only: Testing decisions, Test seams. Guide says drop/skip the dev-only ones entirely when they don't apply; don't manufacture prose. Cite — reference/template-guide.md:26–27.

**P7a (ac-7, non-dev).** No — skip Test seams and do not run the seams step. Cite — reference/synthesis.md:52 ("For a non-dev spec this step does not run at all").

**P7b (ac-7, dev).** Yes — run it; prefer the highest existing seam (fewer the better). Adapted from Matt Pocock's `to-spec`. Cite — reference/synthesis.md:46–50.

**P8 (ac-8).** No file paths / code snippets; describe in prose. Single exception: a prototype-validated snippet encoding a decision (state machine, schema, type shape). Cite — SKILL.md:57–60.

**P9a (ac-9, AFK).** Present via optional `review-loop`, first rendering the markdown spec to a self-contained review HTML; not a hard dependency. Cite — reference/synthesis.md:79–81.

**P9b (ac-9, present).** Inline, in the conversation; a valid spec ships without review-loop. Cite — reference/synthesis.md:77 & 84.

**P10 (ac-10).** Well-formed; `allow_implicit_invocation: false` — correct for an operator-style skill per codex-compat.md. Cite — agents/openai.yaml:7 + codex-compat.md.

**P11 (ac-11).** Pre-written answer key covering ac-1..ac-10 (ac-7 both ways) + coverage map; method names both executors (Opus subagent + `codex exec --sandbox read-only`) per probe-evals.md. Cite — evals/probes.md:2–3, :9.

Verdict: 12/12 correct action + citation. No ambiguities flagged.
