---
name: edit-video
description: Edit recorded explanations or assemble narrated educational videos. Choose the story and cuts, clean voice, compose footage and motion graphics, time captions, and export landscape or short-video layouts.
metadata:
  requires: [watch-video]
  optional: [motion-graphics, writing-for-humans]
---

# Edit video

Deliver an editable project and a coherent rendered video. Keep raw sources intact. Read the brief and the project's `DESIGN.md` before making editorial or visual choices.

## Resolve the delivery

Use the requested format and destination. If neither the brief nor project context settles the format, ask "Landscape video or Short?" Resolve duration separately. A landscape explanation can need several portrait beats; render each composition intentionally.

For Shorts, Reels, or TikTok, read [portrait delivery](references/portrait.md) before designing scenes. Preserve the project’s portrait composition, then accommodate destination controls within it. For landscape, use normal project margins, reserve caption clearance, and account for temporary player controls and requested end-screen elements.

## Understand the sources

Use `watch-video` to build a timestamped scene map and inspect details. If it is unavailable, report the missing dependency; probe streams and inspect frames directly, marking coverage gaps. Speech-led editing also needs a transcript tied to the selected audio stream. Silent contact sheets cannot settle wording or natural audio.

Probe every source's streams, duration, frame rate, and dimensions. OBS filenames indicate intended roles, not quality or synchronization. Inspect the actual camera, screen, and program recordings. Select the microphone by comparing tracks rather than assuming the first track carries speech. Check usable coverage: companion recordings can end before the program.

Measure camera/screen/audio offsets from shared events or audio where available, and check alignment again near the end. Keep those offsets per take. Preserve the program crop as a fallback when a separate screen track is damaged or incomplete.

## Build the story and timeline

Choose one complete explanation, retain qualifications, and remove failed starts, redundant takes, and distracting dead time. A Short needs a self-contained takeaway with its setup and ending. Fit duration by narrowing the takeaway before cutting the words or example that make it understandable.

Write an edit decision list before expensive rendering. Record source file and stream, in/out times, output times, synchronization offsets, and why a take was chosen. Word timings locate candidate cuts; inspect the waveform and surrounding speech to retain consonants, breaths, and natural pacing. Fade only when a boundary needs it; choose the fade from that boundary, not a universal duration.

Before rendering graphics, assemble a paper edit: the actual retained spoken words in output order, with source ranges and output times. Read it without the source context or diagrams. Check every join for a completed thought, a clear referent, and the connection to the next sentence. A setup must reach its answer; pronouns and summaries must refer to information established in the cut. Restore context, use a complete alternate take, or drop an incomplete beat. Preserve natural speech while resolving abandoned clauses and missing explanations. Captions, punctuation, or graphic labels cannot supply words missing from the narration. Record any unresolved source gap rather than inventing speech.

Proceed when the assembled narration explains the selected takeaway on its own, every setup reaches its payoff, and each cut preserves the speaker's meaning. Keep this paper edit with the timeline and revisit it after trims.

Use the final timeline for audio, camera, graphics, and captions. A trim or speed change must update all affected tracks. Keep the timeline and rendering commands reproducible in the project.

## Treat sound and explanatory scenes

For recorded speech, read [voice cleanup](references/voice.md). Start with the project's accepted treatment and keep an untreated comparison. Apply final level control after editorial assembly and measure the encoded export.

When a transformation or diagram would teach the idea, use `motion-graphics` with the concept, narration cues, exact canvas, usable regions, and caption lane. Request editable scenes and rendered clips. If absent, keep real footage or create a simpler visual and disclose that limitation. Motion should clarify the explanation, not fill every pause.

## Caption and assemble

Read [captions and export](references/delivery.md). Derive captions from the final cut, correct technical terms against speech, and check the complete caption plate against both the scene and destination overlays. Reflow graphics around captions before shrinking labels.

Assemble with a local renderer such as FFmpeg, retaining the source timeline and graphics. Use explicit stream maps. Match output frame rate, pixel format, audio rate, and dimensions across clips; verify joins after encoding.

## Review the result

Use `watch-video` on the rendered video, not just the sources. Inspect titles and captions at full resolution, dense windows around joins and animation beats, and phone-size playback for portrait output. Decode the whole export, compare expected duration, and check sync near the start and end.

Compare the rendered narration with the paper edit, checking every join and the final sentence for missing words or unfinished thoughts. Audition processed speech and cut boundaries when playback is available. Measurements and transcripts do not establish voice naturalness; name any unverified listening or motion review. Deliver the video, clean/captioned variants as requested, timed captions, editable scene sources, edit list, and a concise review note with remaining uncertainties. Use `writing-for-humans` when available for the handoff. Publish only when the brief requests publication.
