# Relighting options for the recurring OBS setup

Status: deferred by Asher. Retained for a later version; no relighting work is required for the current voice and motion-graphics scope.

Researched September 15, 2026. This is a shortlist from primary documentation and released source, not a benchmark on Asher's footage. No footage was uploaded, models installed, or paid jobs started.

Asher wants a consistent studio-lit look and expects broadly similar recording conditions. Prefer a method with explicit light controls and reusable settings. Compare its output in motion across recordings before choosing the implementation.

## First candidate: Beeble 3D Relight

Beeble's [3D Relight product documentation](https://www.beeble.ai/features/3d-relight) describes this workflow:

1. Generate VFX passes from the video using SwitchLight 3.0, including normals, depth, and albedo.
2. Import those passes into a browser-based 3D scene.
3. Add HDRI, point, spot, area, sun, or video lights.
4. Export MP4 or a PNG sequence.

This is a good conceptual fit for a repeatable studio setup: define the lights once and evaluate the reconstruction across takes. The vendor describes browser use in Chrome or Edge with graphics acceleration. The page currently lists a free Starter allowance with VFX-pass clips limited to five seconds; verify limits before selecting the actual trial.

Beeble's [local Studio documentation](https://www.beeble.ai/beeble-studio) says Mac is not supported and specifies NVIDIA hardware. This machine is an Apple M3 Pro Mac with 36 GB of memory, so the local Studio route is not supported here. The cloud/browser route is the candidate.

The [developer site](https://developer.beeble.ai) documents a SwitchX image/video generation API with reference images and masks. It does not, on the page reviewed, establish an API for saving and rendering the 3D Relight scene. Treat the web editor and SwitchX API as separate integration candidates. Confirm scene/preset reuse and automation before making either a skill dependency.

Still to verify: account access, applicable clip length and resolution, cost for full videos, scene export/reuse, frame timing, reconstructed detail around beard and hands, and consistency at chunk boundaries. The existence of a product and API does not establish its reliability on these recordings.

## Research alternative: Light-A-Video

Reviewed the official [BCMI Light-A-Video repository](https://github.com/bcmi/Light-A-Video/tree/1b444823a725f0d5d8dc8185a4d8e1c23aea316c), revision `1b444823a725f0d5d8dc8185a4d8e1c23aea316c`.

The authors explicitly address flicker from applying an image relighting model separately to each frame. Their method adds interaction across frames and progressive blending of source and relit appearance. Released implementations include AnimateDiff, Wan2.1, and CogVideoX paths.

The inspected `lav_relight.py` selects CUDA directly. Its sample configuration is 512 × 512, and its output writer uses 8 fps. These are facts about that entrypoint, not limits established for every implementation in the repository. It is not a drop-in local renderer for these 30 fps portrait videos. A trial needs a compatible GPU and explicit preservation of source timing, aspect ratio, and delivery resolution.

The repository code has an Apache-2.0 license. Model weights have their own terms and must be reviewed if adopted. No source or weights have been copied into the skill family.

## Research alternative: RelightVid

Reviewed the official [RelightVid repository by Ye Fang and collaborators](https://github.com/Aleafy/RelightVid/tree/9faad741a0297a5e237b2bde78717b101800b278), revision `9faad741a0297a5e237b2bde78717b101800b278`.

The released example takes source video, per-frame foreground masks, and a background video that conditions the lighting. The installation instructions target CUDA 11.8. Although the introduction describes text and HDR conditions, the release checklist still leaves those inference paths unfinished. Do not assume the headline capabilities are all available in the released workflow.

The repository declares CC BY-NC-SA 4.0. That makes it unsuitable as an assumed unrestricted dependency for a reusable publishing workflow. Keep it as a research comparison until intended use and permissions are resolved.

## Local option to inspect: DaVinci Resolve

DaVinci Resolve 18.6.6 is installed in `/Applications/DaVinci Resolve/`. The app bundle does not establish whether a Studio license is active. Inspect edition, Relight availability, and automation/export controls before promising that route. Current online product features should not be assumed to exist in this installed version.

A tracked grade and selective corrections can provide a local comparison baseline. Whether Resolve's relighting tools can produce the desired look here remains untested.

## Proposed trial

Use a five-second excerpt containing head movement and a hand crossing the face for the first technical trial. The Harness source is a candidate because the inspected final frame shows hands close to the face. Select the exact interval through playback. Repeat the successful treatment on a second recording and then on a longer segment spanning processing chunks.

Compare original camera footage, natural correction, and a studio treatment with a broad soft key, gentle fill, and subtle background separation. Keep timing, crop, resolution, and sound constant. Prefer the key direction that cooperates with the recorded light.

The human judges likeness, skin and beard detail, hand occlusion, flicker, and whether the lighting looks intentional across takes. Also record render time, cost, and the steps needed to repeat the result. An attractive single frame is insufficient to accept the method.

Start with Beeble's explicit 3D lighting workflow if accessible. Inspect the installed Resolve edition as a local alternative. Evaluate an open-source diffusion route only if those fail the output or repeatability requirements. Save the accepted look as a versioned preset plus reference footage; keep per-take exposure adjustments separate from the light setup.
