# Video editing skill: shaping draft

Status: shaping draft, September 15, 2026. Asher chose to refine the existing visual style and focus on voice quality and motion graphics. Relighting is deferred. The conversation review and fixture inventory are complete. The skill is not implemented. A monochrome Harness specimen and two local DeepFilterNet voice treatments are ready; human verdicts are pending. The exact visual tokens and voice treatment remain to be established through examples. Landscape and Short are explicit format choices.

## What we are making

An agent edits Asher's recorded explanations into coherent videos, with clear natural speech, readable composition, and diagrams that explain the spoken idea. The human judges whether changes improve the finished video.

Start with one creative skill, tentatively `video-edit`. Its main instructions own source selection, the edit timeline, treatment selection, and review. Disclose audio and motion guidance in separate references when those passes apply. Split into independent skills only when another workflow needs one of those capabilities directly.

The first scope is voice quality and the visual language for diagrams and motion graphics, with landscape and Short output modes. Relighting is outside this version. Existing editorial work supplies the surrounding workflow and comparison material. Publishing is a separate requested action; eval runs end at local review artifacts.

Keep reusable instructions in the eventual skill source. Keep Asher's chosen palette, typography, camera layout, and approved visual examples in the video project's editable style document. Keep this research and the skill regression suite in `video-edit-workspace/`. A reusable skill must work without these local paths.

## What the conversations establish

Reviewed five editing threads dated September 7, 8, 9, 10, and 15, 2026. Local artifacts live under `~/Projects/random`, and raw recordings under `~/Movies/OBS`. The requested `~/Project/random` path does not exist.

| Evidence | Consequence for the skill |
| --- | --- |
| September 7: remove filler and duplicate takes; use the screen or appropriate animations; crop the camera. | Preserve a coherent explanation and choose the visual that makes each passage understandable. |
| September 7: rejected the pastel-cloud portrait thumbnail, returned to the original concept, then explicitly selected Photo Booth variation 03, "My AI coding workflow." | Use the approved dark thumbnail as one visual reference. The rejection applies to that execution; it does not establish a universal ban on light backgrounds or serif type. |
| September 8: explicitly requested screen above camera and approved the resulting Harness short. Later corrected the landscape thumbnail supplied for a Short. | Preserve the requested layout and make covers for the delivery format. Screen-above-camera is an approved option, not a universal layout. |
| September 9: requested a Short under one minute and a tasteful animation for "unrolling the video." | Motion should explain the operation as it is spoken. The one-minute limit belongs to that brief. |
| September 10 and 15: requested combining interrupted recordings. | Select retakes across recordings and measure synchronization independently for each take. |
| Current request: improve voice, remove background noise, investigate relighting, establish visual language, compare skill revisions on known raw footage. | These are new quality goals. Previous publication does not prove the existing sound or lighting is the desired standard. |
| Latest shaping decision: defer relighting; focus on voice quality and the visual language; choose landscape or Short. | Make format an intake decision and evaluate sound and graphics independently. Keep relighting research parked. |

Conversation identifiers are in [fixtures.json](fixtures.json). Specific preference evidence: SDLC thread user messages at rollout lines 583 and 744; Harness thread lines 226 and 416; Unroll thread line 9. These are historical statements, not fresh posting authorization.

## What the artifacts establish

The five project READMEs, edit lists, and render scripts were inspected. Visual inspection covered the Unroll review grid, the selected SDLC thumbnail, the Harness frame at 23.5 seconds, and the Recap frame at 24 seconds. This review did not include continuous listening or motion playback.

- The SDLC render uses a high-pass filter, mild FFT denoising, and two-pass loudness normalization. Most shorts use high-pass filtering and normalization without dedicated denoising. Recap adds gain and compression. There is no consistent voice-quality assessment.
- Recap's microphone is on the fourth Program audio track, represented as zero-based index 3. The project notes report a nearly silent default track. Audio selection must precede processing; these indices are fixture facts, not defaults.
- Several edits report a distorted separate Screen recording and use a clean Program crop instead. The skill should compare actual source quality before choosing a recording by its filename.
- Recorded camera offsets vary between one frame and half a frame. They must be measured per take, including drift over longer recordings.
- Existing camera adjustments are small contrast and saturation changes. They are not evidence that directional relighting works on this footage.
- The Unroll animation uses actual sampled frames: stack, fan out, settle into a contact sheet, select, enlarge. This is a useful semantic sequence to retain in the first motion comparison.
- Existing designs vary between mint and amber accents, dark graphic panels, a light captured whiteboard, and different camera placements. A stable visual language has not yet been explicitly chosen.
- The Harness edit has a second pacing edit list after its initial edit list. Reusing only the initial list would compare different timing to the finished export.
- The prior sessions report sampled-frame inspection, transcripts, full decoding, and loudness measurements. Those checks leave natural voice quality and animation timing for perceptual review.

## Proposed workflow contract

### Choose the format

Resolve the format before selecting the story length or designing the layout. Use the format already named in the brief. If it is missing, ask one question: "Landscape video or Short?" Do not infer the answer from the raw recording's aspect ratio. A request for both produces two intentional compositions with one shared visual language.

| Decision | Landscape | Short |
| --- | --- | --- |
| Canvas | 16:9, normally 1920 × 1080. | 9:16, normally 1080 × 1920. |
| Story | Room for a complete explanation, examples, and chapter structure. | One focused takeaway, with a hook and a complete ending. |
| Composition | Give the screen or diagram most of the width; place the camera beside it or use a purposeful inset. | Stack camera and graphics. Use the approved screen-above-camera layout for demos; a camera-above-graphics layout also exists in the references. |
| Diagram layout | Reveal relationships across the available width. | Reflow into fewer elements per beat; split a dense diagram into a sequence. |
| Captions | Provide a timed sidecar; burn in captions when the brief calls for them. | Start with readable phrase captions burned in, plus a timed sidecar. Reserve room for platform overlays and the speaker's face. |
| Cover | A landscape thumbnail when requested. | A portrait cover when requested. |

Agree on target duration separately from format. A Short does not imply the one-minute constraint from the Unroll brief. Check current destination limits when preparing delivery. Render graphics for the chosen canvas rather than cropping a finished landscape graphic into portrait.

For the first voice and motion comparisons, choose **Short**: the existing Unroll and Recap edits provide compact, familiar review material. Keep the SDLC landscape fixture in the regression set so the skill's other format is covered.

### Intake and edit

Read the brief and any existing style decisions. Identify the actual take group, source roles, audio tracks, duration, aspect ratio, and intended output. For multiple takes, select the best complete explanation and preserve qualifications that change its meaning.

Record source intervals, selected tracks, camera offsets, screen substitutions, and output timing in an edit decision list. Keep speech, camera, captions, and animation attached to that timeline. Preserve word endings and natural breaths at cuts. Derive caption timing from the final cut.

Validate source quality before expensive treatment. The raw recordings remain the inputs for every revision; each render writes a new artifact.

### Voice and background noise

Aim for recognizably Asher's voice with intelligible consonants, natural breaths, steady level, and less distracting noise.

Start with DeepFilterNet 3 as the local neural denoising candidate. The native Apple Silicon v0.5.6 executable has rendered two strengths on Recap; the human listening verdict is pending. The trial source and hashes are in `voice-trial.json`, and its repeatable script is `scripts/voice-trial.py`. Keep FFmpeg for extraction, timing, loudness, and export.

Choose the microphone track by inspecting and auditioning available tracks. Assess noise during speech as well as pauses. Apply processing to the observed problem: rumble, steady hiss, hum, room reverb, or transient noise need different treatment. Preserve a bypass version.

Try the lightest effective treatment on a representative passage before processing the whole edit. Compare untreated and processed speech at matched speech loudness. Listen for metallic texture, missing consonants, pumping, and abrupt changes in the noise floor at cuts. A quieter waveform or a correct transcript cannot establish natural sound.

The existing -16 LUFS / -1.5 dBTP settings are a candidate delivery starting point. Measure the encoded export because encoding can change peaks. Select the final loudness target for the delivery brief. Apply the same preprocessing in both normalization passes.

Completion: the chosen track is documented, technical measurements are recorded, and a human can audition matched versions. If listening is unavailable to the agent, label naturalness unverified and retain that review item.

### Diagrams and motion graphics

Use [DESIGN.md](DESIGN.md) for the current visual proposal: monochrome light and dark, with an optional blue comparison from diagram-design. Asher rejected the previous teal direction. The interactive reference is `visual-reference.html`.

The visual language must define more than colours:

- Typography and information density that remain readable at phone playback size.
- Camera, screen, caption, and graphic regions for portrait and landscape compositions. Reserve delivery-specific overlay space.
- A small vocabulary: entity, group/container, connection, sequence, selected item, and detail view. Use containment for the Harness/model relationship and frame selection for Unroll.
- Motion that reveals an entity, establishes a relationship, or directs attention. Time the reveal to the spoken concept and allow reading time before the next change.
- Stable identities and positions across beats so an object remains recognizable while the explanation advances.

The first motion specimen should redraw the Unroll passage using the same source frames and spoken timing. The first diagram specimen should redraw the Harness/model relationship. Compare them at actual phone size, including captions and camera.

The existing `diagram-design` skill is a candidate dependency for diagram semantics and styling. Its interactive HTML controls and static fallbacks do not define a rendered video timeline. The eventual video skill must own time-based composition. `watch-video` is a candidate dependency for sampled inspection, with audio and continuous motion explicitly covered elsewhere. If adopted, declare dependencies and missing-skill behavior in the shipped skill.

Completion: the human can compare specimens against the old edit, judge whether the explanation is clearer, and choose a visual direction. Only then record exact style tokens as approved defaults.

## Human eval

[fixtures.json](fixtures.json) fingerprints the current raw recordings, old exports, edit lists, and render scripts. It records local file references and SHA-256 hashes, not copies of the media. Check hashes before a run; a mismatch requires recovery of the recorded version or an explicitly new fixture revision.

The exports are historical ad hoc baselines. They include iterative feedback and some skill/tool use, so they are not a controlled "no skills" experiment. They remain the right practical reference for "is this better than what I have?"

| Case | First use | Later coverage |
| --- | --- | --- |
| `recap` | Voice treatment, using take 1 at 16.8–27.1333 seconds plus handles. | Two takes, fourth audio track, demo substitution, intact final word. |
| `unroll` | Motion specimen: source 65.6667–82.8667 seconds, corresponding to the old edit at 17.1333–34.3333 seconds. | Selection and enlargement later in the explanation; full 53-second story. |
| `harness` | Diagram specimen and approved screen-above-camera layout. | Separate pacing pass, camera/gesture framing, usable portrait cover. |
| `terms` | Regression after choosing treatments. | Longer Short, all 11 terms, interruption and take transition. |
| `sdlc` | Long-form regression. | Landscape composition, chapter transitions, repeated graphics. |

The candidate voice passage still needs listening before it becomes the locked review excerpt. Include speech, a pause, and a cut boundary. Add a passage with confirmed noise if this one lacks it. None of these familiar recordings is an unseen holdout; reserve a new recording for a later generalization check.

### Compare one change at a time

1. Copy the baseline files and run inputs into a versioned local run directory, or use immutable storage. Record hashes before rendering.
2. Pin the brief, raw media, edit timeline, model/effort, loaded skill revisions, render tools, fonts, settings, and any seeds. For a treatment comparison, hold editorial timing and all other treatments fixed. Reconstruct the final Harness timing from both edit lists.
3. Render the baseline treatment and candidate from the raw footage using that same timeline. An encoded historical export is a viewing reference, not input media for the new treatment.
4. Present neutral A/B labels with randomized order and a stored reveal key. For audio, match active-speech loudness using gain only and disable player enhancement where possible. For graphics, use the same speech, scene timing, camera treatment, and output format.
5. Let the reviewer replay a short interval, switch versions, and choose A, B, tie, or neither. Record a timestamp and reason for defects. Keep the verdict independent for voice, graphic clarity, and pacing.
6. After the focused comparisons, run the complete candidate skill on the known raw set. Compare the full edit for coherence, cut damage, sync, caption accuracy, legibility, and treatment continuity.

A controlled claim about the instructions needs a fresh baseline run without the candidate skill and a candidate run with it, using the same brief and environment. Record the other loaded skills. Historical improvement alone cannot isolate the effect of instructions from a model or tool change.

### Review artifact and decision

The intended review page has synchronized playback, A/B switching, a replay range, a view at the selected format's intended playback size, and a downloadable verdict record. Only one audio source plays at a time. Stop playback when leaving the comparison. Stills support inspection but do not substitute for listening or motion review.

Each verdict records the case and run IDs, anonymous labels, choice, defect timestamp, reason, reviewer, and date. The run record holds the hypothesis, exact instruction diff, source hashes, configuration, output hashes, validation results, and label mapping.

Promote a treatment only after the human records an improvement or accepts a stated tradeoff. Clipped words, lost meaning, wrong captions, unreadable graphics, or broken synchronization must be resolved. A tie provides no evidence of improvement; retain the current accepted version unless the human has another reason to change it.

Whenever instructions or rendering code change, rerun the affected comparisons and the complete known-footage regression set before accepting the revision. Keep prior accepted outputs and decisions so later changes can be compared against them. Human review is part of acceptance, not a score inferred from loudness or decode success.

## Settled direction and next decisions

1. Focus this version on voice quality and diagrams/motion graphics.
2. Refine the existing visual style.
3. Resolve landscape or Short at intake; use Short for the first treatment specimens.
4. Keep human A/B review on known raw footage as the acceptance step for instruction changes.
5. Defer relighting. The [research notes](relighting-research.md) remain available for a later version and do not create current implementation or eval requirements.

Next, review the monochrome Harness specimen and the original/gentle/stronger Recap voice samples in `visual-reference.html`. Record the human choices in DESIGN.md and the trial record. Apply those choices to an Unroll motion specimen and then exercise both output formats on the known-footage suite. Successful rendering alone does not establish perceptual improvement.
