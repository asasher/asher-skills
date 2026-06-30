---
name: fair-deal
description: Stateful, project-scoped mediation for a business deal between two partners. Each partner runs their own agent; the agents privately interview their human, research objective benchmarks, and negotiate a fair structure with each other through a shared PRIVATE GitHub repo — commits are the mediation channel — filling a shared Fair Deal Canvas as the human review surface. Use to set up or run a partnership, co-founder, JV, advisory, or revenue-share deal. Must be installed inside a deal project; never global.
argument-hint: "[setup|join|interview|negotiate|status|draft|research] [args]"
user-invocable: true
disable-model-invocation: true
---

# Fair Deal

Two people want to do a deal and like each other. Most such deals go wrong not from bad faith but from
**things left unsaid** — who gets paid and when, who owns what, who decides, what happens if it ends. This
skill makes an agent each partner's **representative** (like a manager or a lawyer): it draws out that
partner's true goals, reservations, and floor *in private*, then negotiates a fair structure with the other
partner's agent — so the two humans never have to sit across a table and argue. The agents do the admin and
the back-and-forth; the humans just answer questions honestly and review the result.

This skill is the operational engine for the **Fair Deal Canvas** framework. It maps onto the framework's
three layers exactly:

| Framework layer | Here |
|---|---|
| **Solo Prep Sheet** — private floor, BATNA, benchmarks | `private/solo-prep.md` — **gitignored, never pushed** |
| **The Canvas** — the shared, fair structure filled together | `canvas.json` (+ `canvas.html` to view) — the **committed human review surface** |
| **Agreement Memo** — the output | `AGREEMENT.md` — generated when the canvas is *Ready* |

The mediation channel is the **git history of a private GitHub repo**: each agent takes turns committing its
move (a proposed change to the canvas + a benchmark-anchored argument). The commit log becomes the deal's
audit trail — *why* every term was agreed.

## References

`reference/` holds the contracts; `templates/` holds the files `setup` scaffolds into the deal repo. A
subcommand's reference is its contract — follow it; don't improvise. `reference/protocol.md` is the shared
source of truth for the file layout and the turn/state machine; every subcommand reads it.

## Commands

| Command | Role | Reference |
|---|---|---|
| `setup` | **Party A:** scaffold the deal repo (canvas, negotiation files, gitignored scratchpad), create a **private** GitHub repo, invite Party B, record your identity | `reference/setup.md` · `reference/protocol.md` |
| `join` | **Party B:** after cloning, create your own gitignored scratchpad and record your identity | `reference/join.md` · `reference/protocol.md` |
| `interview` | Privately interview your human one question at a time (canvas-box order); fill the private Solo Prep, derive shareable opening positions onto the canvas | `reference/interview.md` |
| `negotiate` | The **autopilot** turn loop: pull, take your turn (counter / accept / hold), push; pause only to ask the human something or to run a **floor gate** | `reference/negotiate.md` · `reference/protocol.md` · `reference/floor-gate.md` · `reference/monitor.md` |
| `research` | Pull objective benchmarks (salaries, margins, royalty ranges, comparable terms) via subagents into the canvas/log, with sources | `reference/research.md` |
| `status` | Show the canvas state, phase, whose turn it is, and the open items | `reference/protocol.md` |
| `draft` | When *Ready* and both humans have accepted, generate the Agreement Memo | `reference/draft.md` |

## Routing

1. **No argument** → if no deal repo is initialised here, route to `setup`. If one exists, run `status`, then
   continue the natural next step (`interview` if your side hasn't finished; otherwise `negotiate`).
2. **First word matches a command** → load that reference and follow it.
3. **First word doesn't match** → infer the closest command, state it, then proceed.

## Core rules

- **Project-scoped, never global.** This skill must run inside a deal project that is a git repo. If invoked
  globally or with no repo, stop and tell the user to make a directory and run `fair-deal setup`.
- **Autopilot.** The agent owns all admin and the negotiation back-and-forth. Never make the human do git,
  turn-taking, or file bookkeeping. The human has exactly two jobs: answer interview questions, and decide at
  a floor gate. Drive everything else yourself.
- **The private firewall.** `private/` is gitignored and must never be committed or pushed. **Never copy
  private content — a floor, a BATNA, a raw reservation — into any committed file.** Positions you commit are
  *derived* (an anchored ask), never the underlying secret. `setup` configures `.gitignore` so this holds by
  construction; still, never write secrets outside `private/`.
- **The floor gate (the one place autopilot yields).** Before you propose, accept, or even *discuss* a
  concession at or below your human's stated floor, STOP and follow `reference/floor-gate.md`: bring it to
  your human in plain language and proactively offer a **creative third option** (restructure the deal so
  nobody has to cross a floor) — the way a good manager or lawyer would. Only proceed with their decision.
- **Not the final agreement.** Whatever the two agents converge on is a **strongly-suggested mediation
  outcome**, not a binding deal. Both humans must explicitly review and accept it, and a lawyer must formalise
  it. Say this whenever you present a converged result.
- **Turn protocol.** Negotiation strictly alternates via the `turn` token in `negotiation/state.json`. Only
  the side whose turn it is writes shared files. Always `git pull --rebase` before acting and before pushing;
  if a push is rejected, rebase and retry. Full rules in `reference/protocol.md`.
- **Escalate, don't loop.** If you hit the round cap or a genuine values impasse, set the phase to
  `escalated`, write a neutral talking-points summary of the open items and each side's position, and tell
  both humans to have a direct conversation. Don't burn rounds in a stalemate.
- **The other side may be a different agent.** Each human uses whatever agent they like (Claude, Codex, …).
  Communicate *only* through committed files; never assume the other side reasons or formats like you.
