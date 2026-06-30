# fair-deal

A **stateful, project-scoped** skill that mediates a business deal between two partners — each represented by
their own agent. The agents privately interview their humans, research objective benchmarks, and negotiate a
fair structure with each other through a shared **private GitHub repo** (commits are the mediation channel),
filling a shared **Fair Deal Canvas** as the human review surface.

It operationalises the Fair Deal Canvas framework's three layers: a private **Solo Prep** scratchpad
(gitignored), the shared **Canvas** (committed, the review surface), and the **Agreement Memo** (the output).

## Why an agent in the mix
So two people who like each other don't have to argue across a table. Each agent draws out its human's true
goals, worries, and floor *in private*, then advocates for them like a manager or lawyer — anchoring every ask
to an objective benchmark, proposing neutral mechanisms whose honest output is already fair, and stopping to
work *with* the human (suggesting creative third options) before anything crosses their floor.

## Install (in a deal project — never global)
```bash
mkdir my-deal && cd my-deal
npx skills add <this-repo-url> --skill fair-deal -y
```
Then drive it with your agent:
```
fair-deal setup        # Party A: scaffold + create private repo + invite Party B
fair-deal join         # Party B: after cloning
fair-deal interview    # each side, privately
fair-deal negotiate    # autopilot, with a human gate only at the floor
fair-deal draft        # generate the agreement memo when ready
```

## How it works (one screen)
1. **Party A** runs `setup`: scaffolds the repo, creates a **private** GitHub repo, invites **Party B**. The
   skill is committed, so B gets it on clone. Only `private/` is gitignored.
2. Both sides run `interview`: the agent fills the private Solo Prep and seeds shareable opening positions on
   the canvas. One question at a time; honest answers stay private.
3. `negotiate` runs on **autopilot**: agents take turns (a `turn` token in `negotiation/state.json`),
   committing a proposed canvas change + a benchmark-anchored argument each move. The git log is the audit
   trail. The human is pulled in only to answer something or at a **floor gate**.
4. On convergence the canvas reads **Ready**; both humans review and accept; `draft` writes `AGREEMENT.md` for
   a lawyer. If the agents can't converge, it **escalates** to a direct human conversation with neutral
   talking points.

## Layout it scaffolds
See `reference/protocol.md`. Key point: `private/` (each side's floor/BATNA) is **never committed**; everything
else is, so the deal is fully reproducible from the repo.

## Notes
- **Not legal advice.** The converged canvas is a strongly-suggested business structure; a lawyer formalises it.
- Each partner may use a different agent (Claude, Codex, …); they coordinate only through committed files.
- Contracts live in `reference/`; scaffolded files in `templates/`; `agents/research-analyst.md` is the
  benchmark-finding subagent.
