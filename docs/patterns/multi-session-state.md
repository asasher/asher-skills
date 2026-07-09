# Multi-session state and resume

## Problem

Several skills here are natively multi-session — a Bayesian question updates over weeks, a career campaign
runs for months, a backlog loop spans many working sessions. Chat context does not survive sessions;
memory files are point-in-time observations, not live state. The skill needs a state artifact such that a
bare invocation (`/bayes`, `/goodwork`) reads it and proposes the correct next step with no human recap.

## When to use

Any skill whose output of one session is the input to the next. Not needed for one-shot skills.

## Shape

- **A workspace directory owns all state.** The skill is installed into (or creates) a dedicated workspace;
  in this repo those live at the root as `<skill>-workspace/` (goodwork-workspace, dissolve-workspace,
  constraints-research, …).
- **State is a self-contained artifact, not scattered notes.** bayes goes furthest: the *entire* state —
  question card, hypothesis board, priors, every update — lives in one self-contained HTML page
  (`question.html`, scaffolded from `skills/bayes/templates/question.html`). The page doubles as the human
  review surface.
- **Bare command = resume.** The no-argument invocation always works: read the state, report where things
  stand, propose the next step. The user never needs to remember subcommands.
- **Append-only history.** Updates append; past records are never rewritten. This is what makes the state
  trustworthy after a gap.
- **The agent is the sole writer.** Same invariant as the review surface: humans and servers may request,
  only the agent writes state (goodwork SKILL.md states this explicitly).
- **Re-read the method each session.** State survives; agent comprehension doesn't. bayes: "if you haven't
  read reference/method.md this session, read it before running any command."
- **Absolute dates only.** "Last Tuesday" is meaningless at resume time.

## Canonical implementation

- **bayes** — single-artifact state: `question.html` holds everything; every session ends with beliefs
  updated and one concrete thing to observe; the dashboard and `Updated` stamps are refreshed every session
  so staleness is visible on the page itself.
- **goodwork** — directory-workspace state: `goodwork/` workspace files, agent-sole-writer invariant,
  server appends request events only.

Start from bayes when state fits one document a human will actually read; start from goodwork when state
is a working directory of many files.

## How to adopt

1. Decide the workspace location and say so in SKILL.md ("Install once in a <skill> workspace; resumable
   across sessions").
2. Ship a state template in `templates/` and scaffold it on first run.
3. Make the bare command a resume: read state → summarize position → propose next step.
4. End every session by writing the resume point *into the state artifact* — not only into memory files.
   A memory entry may point at the workspace, but the workspace is the source of truth.

## Gotchas

- State that only the agent can parse is a bug — the human should be able to open the artifact and see
  where things stand (bayes's HTML page is the strongest version of this).
- Forgetting the "re-read the method" rule produces confident wrong resumes: the agent remembers *that*
  there is a protocol but not its details.

## Instances

bayes, goodwork, backlog (`docs/agents/` environment files written by setup), dissolve and constraints
(workspace dirs in this repo); the session-memory "state" files (`*-skill-state.md`) are pointers into
these workspaces, not replacements for them.
