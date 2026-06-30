# fair-deal eval — local protocol dry run

`protocol-dryrun.sh` exercises the whole `fair-deal` turn protocol on one machine, with **no network and no
GitHub**: a bare local repo stands in for the private remote, and two clones (`deal-A` = Ada, `deal-B` = Ben)
play the two partners. One run drives setup → join → interview → negotiate (3 rounds) → converge → draft,
asserting the protocol's invariants at every step.

```bash
bash skills/fair-deal/eval/protocol-dryrun.sh    # prints PASS/FAIL per check; exits non-zero on any FAIL
```
It scaffolds into a fresh `mktemp` dir each run and never touches this repo.

## What it asserts (35 checks)
- **The private firewall** — after every commit/push, on both clones *and* the origin, nothing under
  `private/` is ever tracked; the floor/BATNA in `solo-prep.md` stays local.
- **Clone-gets-skill** — the skill is committed, so Party B has it after a bare `git clone`.
- **Turn alternation** — each negotiate move checks the `turn` token before writing; the commit log alternates
  A, B, A, B; neither side writes the other's `from-*/` outbox.
- **Shared-state integrity** — `canvas.json` parses after every push; both sides' interview rows merge;
  `phase` advances interview → negotiate → ready; `draft` runs only once both `accepted` flags are true.
- **Memo firewall** — the generated `AGREEMENT.md` is built from `canvas.json` only and leaks no private floor.

## Findings it has caught
- **`pull --rebase` aborts on a dirty tree.** An agent following "pull before pushing" literally will edit
  `canvas.json` and then fail the pre-push pull with *"cannot pull with rebase: you have unstaged changes."*
  Fixed by making the ordering rule explicit in `reference/protocol.md`: pull on a **clean** tree first → edit
  → **commit** → then the pre-push pull → push (or `--autostash`).

The negotiated scenario is illustrative (a PlateAI-style audience-vs-build deal) and also exercises the canvas
improvements: durability tags that drive the keystone readout, hybrid Box-3 tags, and the restraint field.
