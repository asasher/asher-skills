# Modality playbook — movement

Dance, posture, sport technique, stagecraft. This is the **honest-and-thin** playbook: machine-objective
measures are scarce and high-friction, so the center of gravity shifts to *trained self-assessment*,
*physical rigs*, and *human checkpoints*. Say that plainly in loop design rather than promising precision
the tooling can't deliver.

## Capture (the trap)

- **Phone on a tripod, one tap** — the entire trap for most drills. Fixed camera position and framing per
  drill (mark the tripod spot with tape) so films are comparable across sessions.
- **Per-rep video review violates the latency budget.** Use body tests per rep (below) and video per block:
  film the block, review once every N reps, sample stills for the agent.
- **Delayed mirror** — a laptop webcam looping video at a 2–4 second delay lets the learner perform, then
  watch themselves, without touching anything. One small script; the closest movement gets to A/B loopback.

## Gap measures, by trust

**Self-assessment (the workhorse):** proprioceptive **body tests** — binary, per-rep, no equipment:
"could I lift the free foot right now?" (weight transfer), "did my heel touch first?", "did the balance
survive the freeze?". A good body test is the movement equivalent of a machine measure: instant, objective
to the performer, hard to fake. Designing one per drill is the main loop-design craft here. Back them with
two-line rubrics in `rubrics/`, and calibrate per loop-design step 5: the learner films a deliberately bad
and a careful rep, scores them blind a day later, and must separate them.

**Agent-perceptual (gross triage):** the agent reviewing stills or short clips catches *gross* posture and
shape errors — a dropped frame, a bent support leg, arms dead. It cannot judge timing feel, weight, or flow
from stills. Label accordingly; when the learner's rubric and the agent's stills disagree on anything
subtle, trust the rubric and queue the question for the human checkpoint.

**Machine-objective (rare, sometimes worth it):**

- **Timing against music** is the exception — feet or claps landing on the beat can be scored from the
  film's audio track with onset detection, same tooling as the audio playbook. If the drill has a rhythmic
  spine, this is the measure to build.
- **Pose estimation** (MediaPipe et al.) can score joint angles and positions, but the friction cost —
  setup, lighting sensitivity, calibration drift — usually exceeds what a good body test can't already
  catch. Default: **defer, and write the deferral in the drill spec** with the condition that would revisit
  it (e.g. "rubric stops discriminating on knee angle").

**Human:** teachers, classes, socials, film review by a practitioner. For movement these aren't occasional
calibration — they're load-bearing. Schedule them into `MISSION.md`, prepare specific questions for them
("watch my weight transfer, not my arms"), and treat what they say as re-calibration input for every rubric.

## Physical rigs (the build tier is mostly physical here)

- **Floor tape** — step width, turn spots, travel lines. The cheapest constraint that makes an error
  self-announcing.
- **Freeze protocol** — stop on a count and hold; balance failure reveals what continuous movement hides.
  A protocol is a rig.
- **Slow-motion practice** — the universal part-practice; slowed music (audio playbook's slow-downer) keeps
  it musical.
- **Constraint props** — a book balanced for posture, hands clasped to silence arms while feet learn, eyes
  closed to force proprioception. Choose the prop that makes the *target* error impossible or obvious.

## Protocols that earn their keep

- **Perception first, here too:** learners often can't *see* the gap between their film and the exemplar.
  Half-speed side-by-side viewing with a "name one difference" prompt is a real drill, not a warm-up.
- **Film the checkpoint:** record the human teacher demonstrating the correction on you — that clip becomes
  the exemplar for the next loop.
- **Context laddering:** no music → slow music → tempo → different song → eyes off the floor → a partner →
  a crowd. Variable practice is the progression axis movement gives you for free.
