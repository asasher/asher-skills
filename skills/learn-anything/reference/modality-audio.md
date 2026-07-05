# Modality playbook — audio

Accents, voice acting, singing, instruments. This is the **strong** playbook: capture is trivial, analysis
tooling is mature, and machine-objective gap measures genuinely exist. Lean on it.

## Capture (the trap)

- `sox -d rep.wav trim 0 5` or `ffmpeg -f avfoundation -i ":0" -t 5 rep.wav` (macOS) — wrap in a one-keypress
  `rig/rec.sh`. Fixed short durations keep the latency budget; size them to the drill (pilot sessions
  routinely reveal truncation — see the worked example in `reference/loop-design.md`).
- Name captures `<drill>-<date>-<n>.wav` into `practice-log/` so score history stays attached to audio.
  Keep the best rep and the exemplar adjacent — future perception drills need both.

## Gap measures, by trust

**Machine-objective (build these first):**

- **Pitch / intonation contour** — `librosa.pyin` or `parselmouth` (Praat's Python binding). Plot learner F0
  over exemplar F0, or score contour correlation. Covers singing pitch, intonation for accents, vocal
  registers for voice acting.
- **Timing / rhythm** — onset detection (`librosa.onset`) against a click track or exemplar onsets → mean
  absolute deviation in ms. Covers instrument timing, syllable rhythm and stress-timing for accents.
- **Tempo stability, tuning** — trivial with `librosa`; a guitar drill's "did the tempo drift" is one script.
- **Formants / vowel quality** — `parselmouth` F1/F2 at the vowel midpoint, plotted against the exemplar's.
  Real signal for vowel-shift work (e.g. Scottish vowel length, French rounded vowels), but sensitive to
  recording setup — calibrate per loop-design step 5 and re-calibrate when the mic or room changes.

**Agent-perceptual (triage only):** the agent can reliably judge *transcription-level* properties (which
word, roughly which vowel, obvious tap vs approximant) and coarse direction ("closer than last block").
It cannot be trusted for fine phonetic calibration — blind-test yourself against exemplar/bad-rep pairs and
write the result in the drill spec. When machine and agent disagree, the machine wins; when both are blind,
schedule the human.

**Self-assessment:** the A/B loopback (below) turns the learner's own ears into the measure — for audio this
is the workhorse, because trained perception transfers directly back into production.

## Rigs worth building

- **A/B loopback** — `rig/ab.sh`: play exemplar, then last rep, back to back, instantly. One afternoon to
  build, devastatingly effective for accents and voice; the contrast does the teaching. This is usually the
  first rig any audio workspace gets.
- **Capture-and-score** — record, run the drill's objective measure, print one number and one sentence.
  Rep-to-feedback in under five seconds.
- **Slow-downer** — `sox tempo 0.6` (or `rubberband`) on the exemplar for part-practice at correct-speed-zero;
  also for perceptual drills (differences are audible at 60% that vanish at 100%).
- **Click/drone generator** — `sox synth` covers metronomes and drone notes; no adoption needed.

## Exemplar generation (adopt tier)

- **ElevenLabs** (or equivalent TTS with accent/voice control) can synthesize exemplars on demand: the same
  sentence in the target accent, a voice-acting register at three intensities, minimal pairs that no
  recording of a real speaker happens to contain. Powerful for coverage; **verify authenticity before
  trusting** — synthesized "Scottish" can be stage-Scottish. Prefer real speakers for the gold standard and
  synthesis for volume; when they conflict, the human recording wins.
- Real-speaker sources: film/interview clips, accent archives (e.g. IDEA), instructional recordings.
  Clip the exact phrase into `exemplars/`, don't cite a 40-minute video.

## Protocols that earn their keep

- **Shadowing** (accents, voice): play a phrase, speak along/immediately after, capture, A/B. It compresses
  perceive→produce→compare into one rep and naturally hits the latency budget.
- **Minimal pairs** (perception drills): same/different and which-one identification against exemplar pairs
  before production drills on the contrast.
- **Register laddering** (voice acting): same line at 3–5 marked intensities, exemplar per rung — turns a
  vague "more menacing" into a scored progression.
