# The debate

The default way to dissolve: **two minds on one page.** A lone reasoner smuggles in its own assumptions — it
taboos the words it already finds suspicious, splits the bundle along cuts it already sees, and calls the value
strand "deserved" without noticing it chose a side. A second agent, reasoning differently, catches exactly those
blind spots. Read this when running `debate`.

## The set-up

Two agents dissolve one question into **one shared** `dissolution.html`. The second agent is a *different* mind —
a different model or CLI, or a subagent you spawn. You communicate only through two files in the dissolution
folder:

- `dissolution.html` — the joint artifact, the five-move page. **The single source of truth.**
- `discussion.md` — the turn log. **Scratch, not state.** Each move, append one dated block: what you changed
  and *why*, what in your partner's work you're **challenging**, and the open question you hand back.

## The stance

A debate in service of a dissolution, not a fight to win a side. Each turn:

- **Build on** what your partner got right — don't restate it.
- **Challenge** the weakest point. The recurring three, worth checking every turn:
  - a **strand assumed as a premise** — a sub-question stated as a background fact ("drinks *despite harm*")
    instead of split out and tested (see `method.md`, move 3);
  - a **"value" that's really empirical**, or an empirical strand that smuggles a metaphysical residue (e.g.
    "loss of control" hiding "could not have done otherwise");
  - a **resolution leaning on desert** — settling a value strand by what's *deserved* rather than by which
    stance produces better outcomes (see `method.md`, move 5).
- **Converge honestly.** Don't rubber-stamp. If you still feel a pull, say so in `discussion.md`.

## Turn discipline

- Act only on your turn. Before editing, **read the whole `dissolution.html` and all of `discussion.md`** — your
  partner may have moved things.
- Make real edits to the page, then append your `discussion.md` block. Keep the page the source of truth; keep
  `discussion.md` to moves and challenges, not a copy of the page.
- Your partner is a different mind — don't assume they reason or format like you. Be explicit.

## Convergence & the gate

Converge when **neither agent can sharpen the cut further**. Then the gate (move 5):

- **Debate + human in the loop:** the human owns the gate. The two agents present the settled decomposition and
  ask the human to reread the original — *any lingering pull?* Only they can close it.
- **Unattended debate:** the gate is the two agents' **explicit** agreement, each stated in `discussion.md`,
  that the original has stopped being a question. One agent's say-so is not a gate; a bare "looks good" is not
  agreement — each must confirm no residual pull reopens the decomposition.

Only then set the resolution section `done` and `overall` to `dissolved`.
