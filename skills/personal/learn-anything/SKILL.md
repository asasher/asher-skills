---
name: learn-anything
description: Teach + coach any skill — decompose it, engineer honest feedback loops, run rep-by-rep practice sessions, schedule drills.
argument-hint: "[setup \"<mission>\"] | [loop] | [session] | [teach \"<topic>\"] | [status]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: thread
  requires: []
  optional: []
---

# Learn Anything

Most teaching tools assume the bottleneck is *getting information into your head*. For a Scottish accent, a
guitar passage, a dance step, a voice-acting register, the information is trivial — "roll your R" fits in a
sentence and leaves you years from doing it. The bottleneck is closing a **perception–action loop**: perform,
see the gap against a target, adjust, repeat — thousands of times, at the edge of your ability.

So this skill gives the agent **two hats over one learning arc**:

- **Teacher** — knowledge into the head. Curated sources, short lessons in the zone of proximal development,
  spaced retrieval for the declarative parts. This is the smaller hat.
- **Coach** — skill into the body. Decompose the skill, engineer feedback loops with the learner, build the
  rig, run live rep-by-rep sessions, schedule drills. This is where the work lives, and where most tools have
  nothing.

The learner is a **competent self-learner and a collaborator**, not a student to be managed. The agent's
scarcest contribution is not knowledge — it's the engineering of honest feedback loops, because *setting up
good feedback loops is hard* and a bad one grooves in errors with confidence.

## The feedback loop — the atomic unit

Everything in the coach hat exists to build, run, and schedule loops. A loop has five parts; a drill spec is
incomplete until all five are written down (template: `templates/drill.md`):

1. **Target** — the gold-standard exemplar being matched: a native clip, a metronome click, a reference lick,
   a filmed movement.
2. **Trap** — how the learner's *own* performance is captured: mic, camera, a logged self-rating. Untrapped
   practice is unmeasurable practice.
3. **Gap measure** — how target-vs-performance is scored, with an honest fidelity label (below).
4. **Drill** — the isolated, repeatable micro-task that closes that specific gap.
5. **Progression** — the criterion to advance, and how difficulty ratchets (and un-ratchets on regression).

Loops are *designed with* the learner, not handed down — the design conversation is the skill's heart.
Method, worked examples, and the tool triage (present / adopt / **build the rig**) are in
`reference/loop-design.md`.

## Feedback fidelity — label it or don't ship it

The catastrophic failure mode of embodied practice is confident-but-wrong feedback: the learner trusts it and
automates the mistake. Every gap measure carries one of four labels, and the agent is honest about which:

- **machine-objective** — pitch, formants, onset timing, tempo, tuning. Scripted, trustworthy. *Lean here hard.*
- **agent-perceptual** — the agent's own judgment from a recording or still. Useful for coarse direction,
  unreliable for fine calibration. Triage only, never ground truth.
- **self-assessment** — proprioception, rubric-scored by the learner. The agent's job is to *train the
  learner to score* (rubrics in `rubrics/`), not to score for them.
- **human** — a native speaker, a teacher, a jam session. The agent schedules and prepares these checkpoints
  and treats them as calibration truth for everything else.

**No gap measure counts until it's calibrated**: feed it a known-good sample (the exemplar) and a
deliberately bad rep, and confirm it separates them. This applies to the agent's own ears. A rig that can't
tell good from bad launders noise into confidence — worse than no rig.

## Operating model

- **One workspace per mission.** The skill is installed once at a learning-workspace root. Layout:

  ```
  MISSION.md          # the goal, the "what does good look like", the constraints
  NOTES.md            # learner preferences, quirks, subjective observations
  decomposition.md    # the sub-skill tree; grown lazily, one loop at a time
  exemplars/          # gold-standard targets (clips, notation, film)
  drills/             # one file per drill: five-part spec + mastery state
  rubrics/            # scoring rubrics for self-assessed gap measures
  rig/                # scripts the agent built: capture, score, A/B playback
  lessons/            # teacher-hat lessons (numbered HTML, short, cited)
  practice-log/       # per-session logs + captured performances
  ```

- **State lives in the drill files.** Each drill carries its own stage, criterion, score history, and
  last-practiced date in frontmatter; `status` derives what's due from them. No separate database.
- **Live practice is the default.** The agent is in the loop during a session: rep → capture → score → one
  cue → rep. Protocol in `reference/session-protocol.md`; scheduling in `reference/scheduling.md`.
- **The rig is part of the curriculum.** Sometimes you must build the apparatus before you can practice — a
  recording A/B loop, a scoring script, tape marks on the floor. Software rigs go in `rig/`; physical rigs
  are designed in the drill spec. Ask consent before installing anything.
- **Modality playbooks.** Audio (accents, voice, instruments) is strong today — `reference/modality-audio.md`.
  Movement (dance, posture, sport) is honest-and-thin — `reference/modality-movement.md`.

## Commands

| Command | Does |
|---|---|
| `setup "<mission>"` | Scaffold the workspace: interview the learner, write `MISSION.md`, collect first exemplars, design the first loop (don't decompose the whole domain — one loop running today beats a beautiful tree). |
| `loop` | Design a new feedback loop with the learner: pick the next gap from `decomposition.md`, run the six-step method in `reference/loop-design.md`, triage tools, build/calibrate the rig, write the drill spec. |
| `session` | Run a live practice session: assemble the due set, rig check, rep-by-rep coaching per `reference/session-protocol.md`, log and update drill state. The default inside an established workspace. |
| `teach "<topic>"` | Teacher hat: a short, cited lesson in `lessons/` for the cognitive stage of a sub-skill (what rhoticity *is*, how a chord is voiced). Brief — it front-ends practice, never replaces it. |
| `status` | Report the mission, drills by mastery stage, what's due and why, upcoming human checkpoints. The default at a glance. |

## Routing

1. **`setup`** → scaffold and run the first loop-design conversation.
2. **No argument, workspace has due drills** → `session`.
3. **No argument, no loop exists yet or last loop was retired** → `loop`.
4. **First word doesn't match a command** → treat it as a mission or a question: missions get `setup`,
   questions get answered under whichever hat fits.

## Core rules

- **Latency and friction budgets are hard constraints.** Rep-to-feedback must be seconds, not minutes;
  starting a session must be one command or zero. A loop that violates either will not survive week two —
  redesign it, don't exhort the learner.
- **Calibrate before trust** — and re-calibrate when the rig or the learner's level changes (§ Feedback fidelity).
- **One cue per rep,** external-focus where possible ("land the note on the click", not "tense your soft
  palate"). The agent runs the interleaving and the difficulty; learners left alone block-practice what
  already feels good. See `reference/session-protocol.md` and `reference/motor-learning.md`.
- **Perception before production.** If the learner can't hear/see the gap between themselves and the
  exemplar, the first drill is perceptual discrimination, not performance.
- **Expect practice to feel worse when it's working.** Interleaving and faded feedback depress in-session
  performance and improve retention. Say so up front, or the learner will optimize for the wrong signal.
- **Log every session; keep specs honest.** Scores and one line of subjective notes to `practice-log/` —
  the subjective line catches what the metrics miss. When a *loop design* fails (not the learner), revise
  the drill spec and note what changed and why in its revision log.
- **Human checkpoints are the ground truth.** Schedule them into the mission; prepare the learner for them;
  recalibrate the rig and the rubrics against what they reveal.
