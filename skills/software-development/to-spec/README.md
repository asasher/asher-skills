# To-Spec

Turns a conversation that already reached a decision into the **spec** it earned: the high-level direction document a long design discussion produced but never wrote down. To-spec reads what's on the table, captures what was **decided**, and writes the spec as an **HTML document on the subject's artifact branch** — canonical, opening with a diagram, revisions as branch commits. The ticket gets the **projection**: a writing-for-humans summary, the `to-web` render URL, and the commit hash it was rendered from — to-spec creates the ticket when none exists; with no tracker bound, the projection lands in the raising conversation. A settled subject ends here: the spec is the record a decided direction earns, and a spec'd ticket is split only when the user approves a recommended split.

## When to use

- **Closing out a design conversation** — the direction is settled; capture it durably before the thread is gone.
- **Feeding a split** — produce the direction document a later decomposition step consumes (a sibling skill invokes this by name; a user can run it directly).

Not for eliciting requirements. To-spec captures decisions already made — it never interviews.

## Shape

- **Pure synthesis, no interview.** To-spec mines what's already on the table; it does not re-ask what the conversation settled and does not stall on the user. Undecided points are **flagged in the spec's Notes**, not turned into questions.
- **Branch file canonical, ticket projection.** The spec lives on the subject's artifact branch; the ticket carries summary, render URL, and hash — a stale projection is visible by its hash. Sign-off binds to the hash: a later commit past an approval invalidates it.
- **The test split.** Per acceptance criterion: durable suite test vs throwaway verification script — a shaping decision verification executes. (Terms and ADRs need no declaration: shaping commits them on the ticket's work branch.)
- **Dev / non-dev gating.** The skill classifies the work. A **dev spec** keeps the dev-only sections (Testing decisions, Test split, Test seams) and runs the borrowed "sketch the test seams, prefer the highest existing seam" step (see Credits); a **non-dev spec** skips them. One template serves process, content, and decision specs too.
- **Generic vocabulary.** "spec" and "ticket," never GitHub-specific "issue." The downstream unit is a ticket.
- **No stale content.** The spec carries no file paths or code snippets (they rot) — direction in prose. Two narrow exceptions: a prototype-validated snippet that encodes a decision more precisely than prose can, and the durable pointers in the spec's **Supporting artifacts** section — the evidence trail swept onto the spec at crystallise time, omitted when nothing was generated.

## Layout

`SKILL.md` is the command surface (`to-spec [<ticket id, or name>]`) and points into `reference/`: `synthesis.md` (the method) and `template-guide.md` (what each section holds). `agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the pre-deployment probe eval.

Self-contained at the file level; composes by name — `to-web` deploys the render, `writing-for-humans` sets the register; both degrade.

## Install

`npx skills add <repo-url> --skill to-spec`, then invoke it (`to-spec`) at the end of a design conversation to synthesize the decided direction into a spec.

## Credits

- **Relationship:** adapted.
- **Source:** Matt Pocock's MIT-licensed [`to-spec`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/to-spec/SKILL.md).
- **Borrowed:** conversation synthesis, decision capture, and test-seam sketching.
- **Local changes:** artifact-branch spec with ticket projection, dev/non-dev gates, the two declarations, no-interview rule, and generic vocabulary.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
