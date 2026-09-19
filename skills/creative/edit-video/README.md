# Edit video

Compose `watch-video` and, when scenes need animation, `motion-graphics` into a finished educational video. Voice treatment, captions, editorial timing, and delivery geometry remain inside this skill. `writing-for-humans` is an optional handoff reference.

Requires FFmpeg/FFprobe. Local neural voice cleanup uses a separately installed DeepFilterNet executable and model plus NumPy. Projects own their style choices, media, timelines, and output artifacts.

## Sources

- [browser-use/video-use](https://github.com/browser-use/video-use/tree/9575612f066aa517354790a645fd90f9f95a743b), reviewed at that commit. Its word-timed transcript, timeline-view, and rendered-cut inspection approach informed the workflow. Instructions and helpers here were written independently; no upstream skill or code is bundled.
- [DeepFilterNet v0.5.6](https://github.com/Rikorose/DeepFilterNet/tree/v0.5.6), Hendrik Schröter and contributors. Neural denoising runs through its separately downloaded CLI/model; those artifacts are not vendored.
- Safe-zone geometry derives from official Google, Meta, and TikTok references. URLs, retrieval date, scope, and asset hashes are included in `references/safe-zone-profiles.json`. The measurements are ad references, not a guarantee about organic app UI.
