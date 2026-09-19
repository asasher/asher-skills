# Short-video captions and safe zones

Research reviewed September 18, 2026. This is an authoring reference for the accepted lean family: `watch-video`, `motion-graphics`, and `edit-video`. Voice cleanup, captions, and destination delivery belong inside `edit-video` for the first pass. No new skill packages ship with this research.

## Preserve the portrait composition

Resolve landscape or Short, then the destination and placement: YouTube Shorts, Instagram Reels, TikTok, or multiple destinations. Record organic or paid delivery, target locale, and extra UI such as anchors, links, or disclaimers. Use known brief details; ask only for missing decisions that affect the composition.

Use `safe-zone-profiles.json` for the measured reference geometry and source provenance. The supplied coordinates describe official **ad** templates. They are provisional layout references for organic delivery, not verified organic app profiles. YouTube's organic Shorts editor provides dynamic visual guides; use them when checking that destination.

Record a profile ID, revision, canvas, exclusion masks, caption lane, and verification status with each export. Recheck the current reference when starting delivery. When the app preview differs, update that delivery's profile and retain the evidence. Do not silently overwrite profiles used by earlier eval runs.

## Findings from official sources

| Destination | What the source establishes | Consequence |
| --- | --- | --- |
| YouTube Shorts | The organic editor's visual guides indicate potential overlap with likes, comments, and descriptions. White edge guides mark content that may be hidden on some devices. | Check the actual editor guides. Google does not give a fixed organic pixel rectangle in this article. |
| YouTube ads | Google supplies a vertical safe-zone PNG covering varying ad formats and screens. Its transparent rectangle is x=48–888, y=288–1248 on 1080 × 1920. | Useful broad ad reference; label the scope when applying it to organic Shorts. |
| Instagram Reels | Meta's current 9:16 ad diagram reserves 14% at the top, 35% at the bottom, and 6% on both sides. Its lower-right inset reaches 21% of width over the bottom 40%. | Preserve the inset, not just a rectangular top/bottom margin. Reels ads with disclaimers reserve the full bottom 40%. |
| TikTok | The standard LTR ad template labels a 720 × 1280 canvas: top 160, bottom 440, sides 80; an extra 120-wide right inset spans the bottom 720. | At 1080 × 1920 these become top 240, bottom 660, sides 120, and a 180-wide inset starting at y=840. |

TikTok supplies separate anchor and Arabic-region RTL templates. Its article says safe zones vary with dimensions, ad caption length, and additional formats. It also says device-independent previews can differ from live placement. Here, TikTok's term "ad captions" describes post/ad copy, not the burned-in speech subtitles we create.

Meta describes either zooming/cropping or adding a black background on screens taller than 9:16. Keep important content comfortably inside the reference boundary. Neither the frame edge nor a guessed action-rail position guarantees visibility on every device.

The proposed shared inset was rejected in human review on September 19: it shrank the edit into a landscape strip with excessive empty space. The accepted default is graphics above and portrait camera below, filling the canvas. Keep these ad measurements as diagnostic evidence, not a house composition. Apply organic control reservations locally to important text, faces, and captions.

## Compose graphics and captions together

Pass the canvas, chosen exclusion masks, and reserved caption lane to `motion-graphics` before scene construction. The scene should work with those inputs without depending on another skill's private files.

Keep complete labels, equations, meaningful pointer movements, faces, and caption plates clear of controls appropriate to the actual placement. Ad masks are advisory for organic exports. Decorative imagery can extend beyond them. Include padding and outlines in collision bounds. Check moving objects throughout their path, not only at their resting positions.

Start portrait speech captions at the project's 48 px sans-serif size and 58 px line height. Use sentence case, short phrases, and normally one or two lines. Rebreak phrases or split a beat before shrinking the type. Keep speaker names, technical terms, negations, and qualifications correct.

Align cues to the final edited speech. Use meaningful phrase boundaries and sufficient reading time; avoid forcing every cue into a fixed two-word or fixed-duration template. Prevent stale words persisting across cuts, gaps that omit speech, and overlaps between adjacent cues. Correct transcription against the audio.

Use a contrasting monochrome plate over variable footage. Keep the full plate inside the usable area and away from faces, diagrams, and demonstrations. Keep caption position stable within a shot. Move to another planned lane at a scene boundary when the explanation needs the space.

Export a clean master and a timed sidecar, plus a burned-in version when requested. Shorts default to a burned-in version in this project. A sidecar is a portable deliverable; it does not imply every platform uploader accepts it. Check the destination's supported subtitle path and review automatic captions where used. Avoid unintentionally showing two copies of the same subtitles while preserving an accessible caption option.

## Review the delivered composition

1. Render an overlay preview with the chosen exclusions and caption lane. Keep guide layers out of the delivered video.
2. Check the longest caption, a two-line caption, each scene change, and the widest or lowest graphic. Inspect full motion for path collisions.
3. Watch at phone playback size. A coordinate check cannot establish legibility or whether captions compete with the explanation.
4. In the destination app's draft/editor preview, check the actual description, controls, native captions, links, and expected locale. Check paid placement in its corresponding ad preview.
5. Record device, app/version when available, placement, date, and screenshot or review evidence. If app access is unavailable, mark platform verification pending; do not claim the layout passed. This review does not authorize public posting.
6. Inspect cover, profile-grid, and feed crops separately. Playback safety does not imply a cover title survives a different crop.

For a shared organic export, preserve the project’s full-frame stacked composition and accommodate relevant UI locally. Use verified destination differences to decide whether separate layouts are necessary. The union of ad templates is not an organic layout requirement.

Add caption accuracy, plate/UI overlap, important-content overlap, phone-size legibility, and duplicate native captions to human eval. Pin the destination-profile revision with each known-footage run. A changed layout profile is an eval input change.

## Landscape treatment

Keep the project's normal 64 px edge padding at 1920 × 1080. Prefer timed sidecar captions unless the brief asks for burned-in text. Reserve space when captions are visible, and avoid essential information at the extreme bottom edge. Check temporary playback controls, native subtitles, and any requested end-screen elements. The large persistent Short-feed exclusion masks are not the landscape default.

## Sources and scope

- [YouTube: Enhance your Shorts, Use visual guides](https://support.google.com/youtube/answer/16215842?hl=en). Organic guidance, read in full relevant section.
- [Google Ads: About video ad specs](https://support.google.com/google-ads/answer/13547298?hl=en), with its [vertical PNG template](https://services.google.com/fh/files/misc/youtubesafezoneoverlay_vertical_final.png). Downloaded and measured the transparent rectangle.
- [Meta: About text overlays and safe zones](https://www.facebook.com/business/help/980593475366490?locale=en_US). Read public embedded article content and inspected its current diagram, including the lower-right inset.
- [TikTok: Auction In-Feed Ads](https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads?lang=en). Article updated June 2026. Downloaded and inspected its Standard LTR archive; other variants remain separate inputs.

Source asset URLs and SHA-256 hashes are recorded in `safe-zone-profiles.json`. The HTML draws our own monochrome geometry from these references. No platform UI screenshots or downloaded templates are committed to Git. No organic device tests or new rendered-video evals have been run for this research.
