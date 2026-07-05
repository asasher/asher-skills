# watch-video

Video understanding for vision models that can't take video: sample frames, shrink them into a
single timestamped **contact sheet**, read temporal structure in one glance, then drill down —
dense window sheets over regions of interest, full-res "loupe" frames for text and fine detail.

## Why this shape

Validated two ways before writing the skill:

- **Literature**: [IG-VLM — "An Image Grid Can Be Worth a Video"](https://arxiv.org/abs/2403.18406)
  showed a tiled frame grid fed to an image-only VLM beats purpose-built video LLMs on 9 of 10
  zero-shot video QA benchmarks. Query-aware keyframe selection
  ([Q-Frame](https://arxiv.org/abs/2506.22139), [AKS](https://github.com/ncTimTang/AKS)) needs the
  question up front; a sheet looks at everything cheaply first, then picks.
- **Hands-on** (July 2026, Big Buck Bunny, 596s / ~14,300 frames): a 30-frame sheet (~1,475 tokens)
  recovered the full narrative arc including facial expressions; 80 frames at 153×86 tiles was
  still legible for gist; a 12-frame / 36-second window sheet read as a causal chain (bait → lure
  → trap → confrontation, motion blur visible). On-screen text died at sheet resolution and came
  back fully at one full-res frame. Same frames sent as individual images: ~17× the tokens, with
  temporal order left for the model to reconstruct.

## Contents

- `SKILL.md` — the three-pass drill-down (index → window → loupe)
- `scripts/framesheet.py` — sheet builder: uniform sampling, timestamp stamping, auto grid
  geometry sized to a ~1.15 MP / 1568 px vision budget (ffmpeg + Pillow)
