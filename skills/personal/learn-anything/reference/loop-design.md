# Designing a feedback loop

Read this when running `loop` (or the first loop inside `setup`). The output of one pass is a complete drill
spec in `drills/`, a calibrated gap measure, and — when needed — a rig in `rig/` or a physical-rig design in
the spec. This is a **conversation with the learner**, not a form to fill; they know things about their body,
their gear, and their tolerance for friction that you don't.

## The six steps

### 1. Elicit the target

"What does good look/sound like — show me." Force exemplars into `exemplars/` *before* any drilling: a native
clip, a recording of the passage at tempo, film of the movement. If the learner can't point at one, finding it
is the first task (and often a `teach` moment).

Then run the perception check: can the learner *perceive* the difference between the exemplar and their own
attempt? Play/show them both. If they can't hear or see the gap, **the first drill is perceptual
discrimination** (same/different judgments, A/B identification), not production — you can't hit a target you
can't perceive. *Output:* exemplars filed, plus one sentence naming the observable difference in plain words.

### 2. Pick one gap

Decompose *just enough* to isolate a single measurable sub-skill, and add only that node to
`decomposition.md`. "Sound Scottish" is not a gap; "produce a tapped /r/ between vowels" is. Resist mapping
the whole domain up front — that's planning-as-procrastination, and the map will be wrong anyway until a few
loops have run. One loop running today beats a beautiful tree.

### 3. Design the loop

Write the five parts — target, trap, gap measure, drill, progression — against two hard budgets:

- **Latency budget:** rep → feedback in seconds. Every extra second is multiplied by a thousand reps. This
  constraint drives most rig-building decisions.
- **Friction budget:** session start in one command or zero. Gear to plug in, apps to arrange, folders to
  clear — each is a reason the loop dies in week two.

The drill itself should be *smaller than feels dignified*: one sound in one word-position, two bars at half
tempo, one step-pattern without music. Small drills close; big drills blur.

### 4. Triage tools

For each of trap and gap measure, walk the three tiers **in order** — build only what the first two tiers
can't cover:

- **Present** — already on the machine or in the room: mic, camera, `ffmpeg`/`sox`, timers, the filesystem,
  the agent's own perception (with its fidelity label worn honestly).
- **Adopt** — third-party tools worth installing: `parselmouth`/Praat and `librosa` for phonetics and pitch,
  a metronome, a slow-downer, ElevenLabs for generating exemplar audio, pose estimation if the movement
  playbook justifies it. Ask consent before installing; note each adoption in the drill spec.
- **Build** — the rig tier. Software rigs live in `rig/`: an A/B loopback player (record a rep, instantly
  hear target-then-you back to back — cheap to build, devastatingly effective), a one-command
  capture-and-score script, a rubric logger. **Physical rigs count too** — tape marks on the floor, a mirror
  placement, a cork-between-teeth articulation setup, a capo scheme that makes a passage practicable. The
  agent designs these even though the learner builds them; the design goes in the drill spec.

Sometimes you must build the rig before you can practice at all. That's not a detour from learning — it *is*
the loop-design work, and it's why this skill exists.

### 5. Calibrate before trusting

The step everyone skips, and the reason most self-built feedback loops silently fail. Before the loop counts:

1. Feed the gap measure the **exemplar itself** — it must score at or near ceiling.
2. Feed it a **deliberately bad rep** (the learner hams up the error) — it must score clearly lower.
3. If the measure is agent-perceptual: run the same test on your own judgment, blind if possible. If you
   can't reliably separate them, **downgrade your role** in this loop to coarse triage and say so in the spec.

A measure that can't tell good from bad launders noise into confidence — worse than no measure. Record the
calibration result in the drill spec; re-run it when the rig, the recording setup, or the learner's level
changes.

### 6. Pilot for one session, then revise

The spec is a draft until it survives real reps. Run one session; the first one always exposes something —
latency too high, rubric ambiguous, drill too big, criterion miscalibrated. Revise the spec, and if the
*design* was wrong (not just the learner unpracticed), add a line to the spec's revision log saying what
changed and why — future loops for this learner should inherit the lesson.

## Worked example — audio (Scottish accent: the tapped /r/)

1. **Target:** three clips of a Glaswegian speaker saying "very", "sorry", "tomorrow" → `exemplars/tapped-r/`.
   Perception check: learner A/B's their own "very" against the clip — hears the difference. Proceed.
2. **Gap:** intervocalic /r/ realized as an alveolar tap, not an English approximant. One node added to
   `decomposition.md` under prosody-untouched.
3. **Loop:** trap = `rig/rec.sh` (one keypress, 3-second capture). Gap measure = A/B loopback (target then
   self, instantly) scored by learner against a 3-point rubric, plus agent-perceptual triage per 5 reps.
   Drill = the three words, isolated, 10 reps each. Progression = when 8/10 self-score at 3, move the tap
   into short phrases.
4. **Triage:** present — mic, `sox`. Build — `rec.sh` and `ab.sh` (playback exemplar + last rep back to
   back). Adopt — nothing yet; Praat waits until the rubric stops discriminating.
5. **Calibrate:** exemplar scores 3 on the rubric trivially; learner's deliberate English /r/ scores 1;
   agent blind-tests 5 pairs and separates them 5/5 at this coarse grain → agent-perceptual approved for
   triage only.
6. **Pilot:** first session shows 3-second capture truncates "tomorrow" — bump to 5 seconds. Rubric point 2
   ("somewhere between") never used — collapse to pass/fail. Both noted in the spec's revision log.

## Worked example — movement (dance: weight transfer in a basic step)

1. **Target:** 20 seconds of an instructor's basic, filmed from the front → `exemplars/basic-step/`.
   Perception check: learner watches self-film vs exemplar and *can't* name the difference → first drill is
   perceptual: watch both at half speed, three times, and say what differs (answer: weight arrives late).
2. **Gap:** weight fully transferred before the next step starts.
3. **Loop:** trap = phone on a tripod, one tap to film 30 seconds. Gap measure = self-assessment against a
   two-line rubric ("could I lift the free foot at any moment?") — labeled self-assessment; agent reviews
   stills only for gross posture triage. Drill = step-pattern without music, freeze on each count, lift the
   free foot to prove the transfer. Progression = add music at 60%, then full tempo, then eyes off the floor.
4. **Triage:** present — phone, tripod. Build (physical rig) — two tape marks on the floor at step width;
   the freeze-and-lift protocol *is* the rig. Adopt — pose estimation explicitly deferred: friction cost
   exceeds what the rubric can't already catch.
5. **Calibrate:** learner films a deliberately lazy transfer and a careful one, scores them blind a day
   later — separates them. Rubric approved.
6. **Pilot:** freeze-drill works but 30-second films are too long to review between reps → review every 5
   reps instead; per-rep feedback is the proprioceptive lift-test. Latency budget met by moving the trap to
   a sampling role. Revision log: *per-rep video review violates the latency budget; use body tests per
   rep, video per block.*

## Failure patterns

- **The loop nobody runs** — latency or friction budget violated. Redesign; never exhort.
- **The confident bad judge** — an uncalibrated measure (often the agent's ears) grooving in errors. Step 5
  exists for this; when in doubt, downgrade the label.
- **The beautiful tree** — a full decomposition and zero reps. Cap decomposition at the node you're looping.
- **The dignified drill** — too big to close a gap ("practice the song"). Shrink until a single rep can fail
  for exactly one reason.
- **Rubric drift** — self-assessment scores inflate over weeks. Human checkpoints and periodic re-calibration
  against the exemplar are the correction.
