---
colors:
  primary: "#171717"
  surface: "#FAFAFA"
  text: "#171717"
typography:
  family: "Arial, Helvetica, sans-serif"
  scale: [12, 14, 16, 20, 24, 32, 48, 64]
spacing:
  scale: [4, 8, 12, 16, 24, 32, 48, 64]
radii:
  scale: [0, 4, 8]
---

# Educational video style

Use light or dark monochrome consistently across an edit. Light: paper #FAFAFA, ink #171717, secondary text #666666, decorative rules #D4D4D4. Dark: paper #0A0A0A, ink #EDEDED, secondary text #A1A1A1, decorative rules #333333. Use stronger outlines or inverted fills for emphasis. No blue, teal, green, gradients, or glow. Captured footage keeps its natural colours.

Use Arial/Helvetica for captions, titles, and labels; monospace for technical metadata. Preserve readable text at normal playback size. Start titles at 64 px, node names at 44 px, secondary labels at 32 px, and portrait captions at 48 px on a 1080-wide canvas. Reflow or split a scene before shrinking its labels. These are starting sizes, not a reason to crowd a scene.

Landscape output is 1920 × 1080 with 64 px outer padding. Make the screen or explanation dominant and use camera framing deliberately.

Portrait output is 1080 × 1920. Default to motion graphics in the upper panel and portrait camera footage in the lower panel, visible together. Fill the canvas with two substantial panels, starting near an equal-height split. Adjust the seam to suit the explanation and face framing. Crop the camera to fill its panel without stretching, using a prominent head-and-shoulders view with natural headroom. Keep the speaker present through the explanation; change the arrangement only for a deliberate teaching beat.

Compose graphics for the upper panel. Place readable captions near the seam or in another planned lane that clears the face and graphics. Avoid platform controls through local text placement and camera framing. Ad-reference masks do not define this organic-video composition: keep the full frame and both panels rather than shrinking them into a shared inset or adding an empty footer. Use modest project-owned reservations when actual app previews are unavailable, and record that verification as pending.

Graphics are flat and restrained: thin boundaries, clear grouping, one focal event at a time. Use inversion as strong emphasis. Retain object identity across beats and animate a meaningful transformation, then hold its result. Project background knowledge should be taught through the explanation rather than assumed from decorative labels.

Speech captions use sentence-case phrases, normally one or two lines, with a contrasting plate over variable footage. Keep their position stable within a shot. Preserve the actual words and timing. Landscape normally uses a timed sidecar; portrait normally has a burned-in version plus a clean master and sidecar.

For voice, start with local DeepFilterNet 3, 24 dB attenuation limit, postfilter off. Preserve voice identity and compare a representative dry/processed passage. Aim initially for -16 LUFS and at most -1.5 dBTP on the encoded output, adjusting when delivery requires it. Keep relighting out of this edit.
