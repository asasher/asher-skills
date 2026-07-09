**P1 (ac-1):** Yes. Frontmatter has `user-invocable: true`, and its description says, “Pure synthesis, no interview: it mines what's already on the table … and writes a repo doc at docs/specs/<name>.md…” [SKILL.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/SKILL.md:3). No cross-skill file import/read is intended: “To-spec is **self-contained at the file level** … and no file here imports or reads another skill's files.” [SKILL.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/SKILL.md:80). Directory listing showed the shipped layout: `SKILL.md`, `README.md`, `agents/`, `reference/`, `templates/`, `evals/`.

**P2 (ac-2):** The three dependency pointer kinds are bundled references, project playbooks, and sibling skills. For siblings: “**Sibling skills** — **optional `review-loop` only**,” and “This is the sole sibling and it is **not** a hard dependency: skipping review-loop still produces a valid, committed spec.” [SKILL.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/SKILL.md:75).

**P3 (ac-3):** No, do not stop and ask. “Anything left undecided becomes a line in **Notes**, never a question back to the user.” [SKILL.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/SKILL.md:37).

**P4 (ac-4):** It produces a spec repo doc at `docs/specs/<name>.md`; it is not a ticket. “**The artifact is a repo doc** at `docs/specs/<name>.md` — the direction document `to-tickets` consumes.” [SKILL.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/SKILL.md:54).

**P5 (ac-5):** No, “issues” is wrong; the correct word is “tickets.” “Say "spec" and "ticket" — never GitHub-specific "issue." The unit of downstream work is a ticket.” [SKILL.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/SKILL.md:52).

**P6 (ac-6):** Always-present core sections: Problem, Solution, User stories, Implementation decisions, Out of scope, Notes. Dev-only sections: Testing decisions, Test seams. The guide says, “Two groups: **core** sections appear in every spec; **dev-only** sections are kept for dev specs and **skipped when they don't apply**,” and “Don't manufacture prose to fill a heading that doesn't apply.” [template-guide.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/reference/template-guide.md:4).

**P7a (ac-7, non-dev):** No, skip Test seams and do not run the seams step. “**Non-dev spec** … **Skip** the dev-only sections entirely,” and “For a non-dev spec this step does not run at all.” [synthesis.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/reference/synthesis.md:37).

**P7b (ac-7, dev):** Yes, run the seams step. It says to “name the **public seams** the work would be tested at, and **prefer the highest existing seam**,” and the step is “Adapted from Matt Pocock's `to-spec`, shipped as our own.” [synthesis.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/reference/synthesis.md:46).

**P8 (ac-8):** No file paths or ordinary code snippets. The exception is a prototype-validated snippet that encodes a decision more precisely than prose; otherwise, “Everything else is prose.” [SKILL.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/SKILL.md:57).

**P9a (ac-9, AFK):** Use optional `review-loop` sign-off, but first render the markdown spec to self-contained review HTML. “If they're AFK, present the spec for sign-off through the optional `review-loop` sibling (render the markdown to a self-contained review HTML first).” [SKILL.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/SKILL.md:46). It is not hard: “This is the sole sibling and it is **not** a hard dependency…” [SKILL.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/SKILL.md:77).

**P9b (ac-9, present):** Approve inline in the conversation. “When the user is present, approval is inline,” and “skipping review-loop still produces a valid, committed spec.” [SKILL.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/SKILL.md:77).

**P10 (ac-10):** Yes, `agents/openai.yaml` is well-formed for the expected manifest shape, and `allow_implicit_invocation` is correctly `false`. The manifest contains `display_name`, `short_description`, `default_prompt`, and `allow_implicit_invocation: false` [openai.yaml](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/agents/openai.yaml:1). The policy fits because “Default `allow_implicit_invocation` to `false` for operator-style skills …; only lightweight advisory skills should be implicitly invocable.” [codex-compat.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/docs/patterns/codex-compat.md:28).

**P11 (ac-11):** Yes, the eval file declares a pre-written key and dual executors. It says, “**The answer key is written before any runs**,” and “Between them the 12 probes cover ac-1..ac-11.” [probes.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/evals/probes.md:8). The method is dual-executor: “Method: situated probes against the actual deployment targets — an Opus subagent … and `codex exec --sandbox read-only`…” [probes.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/skills/to-spec/evals/probes.md:3), matching the pattern sentence “Executors are the actual deployment targets.” [probe-evals.md](/Users/asher/Projects/asher-skills-wt/8-to-spec/docs/patterns/probe-evals.md:30).

| Probe | Answer | File cited |
|---|---:|---|
| P1 | Yes | `SKILL.md` |
| P2 | Optional | `SKILL.md` |
| P3 | No | `SKILL.md` |
| P4 | Spec | `SKILL.md` |
| P5 | Ticket | `SKILL.md` |
| P6 | Split | `template-guide.md` |
| P7a | Skip | `synthesis.md` |
| P7b | Run | `synthesis.md` |
| P8 | No | `SKILL.md` |
| P9a | Optional | `SKILL.md` |
| P9b | Inline | `SKILL.md` |
| P10 | False | `openai.yaml` |
| P11 | Yes | `probes.md` |