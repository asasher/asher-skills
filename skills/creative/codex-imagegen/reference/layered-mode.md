# Asset-first layered mode

Layered mode starts from a scene plan. It does not segment or reconstruct an existing flattened image.

## Scene plan

```json
{
  "size": 1024,
  "key": "magenta",
  "art_direction": "storybook game art, warm evening light, consistent painterly edges",
  "layers": [
    {
      "name": "background",
      "role": "background",
      "subject": "a quiet forest clearing with distant trees, empty center",
      "z": 0
    },
    {
      "name": "hero",
      "role": "subject",
      "subject": "a small red-hooded traveler, full body",
      "z": 10,
      "anchor": "bottom-center",
      "x": 512,
      "y": 900
    },
    {
      "name": "foreground-fern",
      "role": "foreground",
      "subject": "one large fern cluster viewed from the front",
      "z": 20,
      "anchor": "bottom-center",
      "x": 180,
      "y": 1024
    }
  ]
}
```

`size` is a positive square canvas dimension. `art_direction` is appended to every subject to improve visual coherence. There may be at most one `background`; other roles are keyed transparent assets. Supported anchors are `bottom-center`, `center`, and `top-left`. Position defaults to bottom-center at the canvas bottom.

Each layer needs a stable `name` and a `subject`. Optional fields are `role`, `z`, `key`, `prompt`, `match`, `pad`, `anchor`, `x`, and `y`. A custom `prompt` owns the full generation instruction and therefore must preserve the flat-key constraint for non-background layers.

## Artifact

```text
forest-clearing/
├── manifest.json
├── composite.png
├── raw/
│   ├── 00-background.png
│   ├── 01-hero-keyed.png
│   └── 02-foreground-fern-keyed.png
└── layers/
    ├── 00-background.png
    ├── 01-hero.png
    └── 02-foreground-fern.png
```

The manifest records the exact prompt, raw generation, processed file, z-index, anchor, requested position, and content/canvas bounds for every layer. `composite.png` is regenerated from the listed layers in z-order.

The artifact is created before generation begins. Its status progresses from `in_progress` to `complete`; generation failure changes it to `failed` and preserves all completed layers. Never overwrite or delete the partial artifact during automatic recovery.

## Scope boundary

This first pathway guarantees independently generated assets, not pixel-perfect agreement with a previously flattened composition. Consistency comes from shared art direction and explicit placement. Segmentation, inpainting of occluded pixels, and recreation of objects from an existing composite are intentionally outside this mode.
