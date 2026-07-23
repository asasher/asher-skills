# To-Spec

Turns a conversation that already reached a decision into the **spec** it earned: the high-level direction
document a long design discussion produced but never wrote down. To-spec reads the current conversation and
the codebase/project understanding built up in it, captures what was **decided**, and lands the spec **on
the subject's ticket** — body canonical, opening with a diagram, revisions as comments — creating the
ticket when none exists. Shaping's exit: every settled subject ends here; `to-tickets` splits a spec'd
ticket only when the user approves a recommended split. With no tracker bound, falls back to a
repo doc at `docs/specs/<name>.md` carrying the same diagram-first body.

## When to use

- **Closing out a design conversation** — the direction is settled; capture it durably before the thread is
  gone.
- **Feeding `to-tickets`** — produce the direction document the ticket-cutter consumes (a sibling skill
  invokes this by name; a user can run it directly).

Not for eliciting requirements. To-spec captures decisions already made — it never interviews.

## Shape

- **Pure synthesis, no interview.** To-spec mines what's already on the table; it does not re-ask what the
  conversation settled and does not stall on the user. Undecided points are **flagged in the spec's Notes**,
  not turned into questions.
- **Vendored local method.** The credits below identify its upstream adaptation.
- **Dev / non-dev gating.** The skill classifies the work. A **dev spec** keeps the dev-only sections
  (Testing decisions, Test seams) and runs the upstream "sketch the test seams, prefer the highest
  existing seam" step (see Credits); a **non-dev spec** skips both. One template serves process, content, and decision specs too.
- **Generic vocabulary.** "spec" and "ticket," never GitHub-specific "issue." The downstream unit is a ticket.
- **No stale content.** The spec carries no file paths or code snippets (they rot) — direction in prose. The
  one exception is a prototype-validated snippet that encodes a decision more precisely than prose can.

## Layout

`SKILL.md` is the command surface (`to-spec [<ticket id, or name>]`) and points into `reference/`:
`synthesis.md` (the no-interview method, the diagram-first rule, where the spec lives, gating, seams
step, no-stale-content rule, split recommendation, sign-off) and
`template-guide.md` (what each section holds).
`agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the pre-deployment probe eval.

Self-contained at the file level; composes by name. To-spec depends on no other skill.

## Install

`npx skills add <repo-url> --skill to-spec`, then invoke it (`to-spec`) at the end of a design conversation to
synthesize the decided direction into a spec.

## Credits

- **Relationship:** adapted.
- **Source:** Matt Pocock's MIT-licensed [`to-spec`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/to-spec/SKILL.md).
- **Borrowed:** conversation synthesis, decision capture, and test-seam sketching.
- **Local changes:** spec-on-ticket artifact, dev/non-dev gates, no-interview rule, and generic vocabulary.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
