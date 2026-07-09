# Manifest

`spritesheet.json` is one JSON object per extraction.

```json
{
  "source": "/abs/path/sheet.png",
  "sheet": { "width": 1024, "height": 1024 },
  "slicing": {
    "mode": "grid",
    "cols": 4,
    "rows": 4,
    "tile": [256, 256],
    "margin": [0, 0],
    "spacing": [0, 0]
  },
  "key": { "color": "#00FF00", "method": "border-sample" },
  "elements": [
    {
      "name": "tile_01_grass",
      "index": 0,
      "row": 0,
      "col": 0,
      "sheet_rect": { "x": 48, "y": 56, "w": 160, "h": 145 },
      "trimmed_bounds": { "x": 48, "y": 56, "w": 160, "h": 145 },
      "asset": "assets/tile_01_grass.png",
      "size": [160, 145],
      "anchor": [80, 145],
      "pivot": [0.5, 1.0],
      "css": { "background-position": "-48px -56px", "width": 160, "height": 145 },
      "frame": { "x": 48, "y": 56, "w": 160, "h": 145 }
    }
  ]
}
```

When `--generate` is used, `source` is an object:

```json
{
  "path": "/tmp/to-sprites-.../generated-source.png",
  "generated": true,
  "subject": "4x4 isometric terrain tiles..."
}
```

## Element Fields

- `name` is the deterministic base filename without extension.
- `index` is zero-based extraction order.
- `row` and `col` are grid coordinates or component row/column assignments.
- `sheet_rect` is the exported frame rectangle in original-sheet pixels, after padding.
- `trimmed_bounds` is the opaque content rectangle in original-sheet pixels, before padding.
- `asset` is relative to the output directory.
- `size` is the exported asset size in pixels.
- `anchor` is a pixel coordinate in the exported asset; `pivot` is normalized engine-friendly form.
- `css.background-position` is `-sheet_rect.x px -sheet_rect.y px` for using the original sheet as a CSS
  sprite with `width` and `height`.
- `frame` mirrors `sheet_rect` for TexturePacker/Phaser-style atlas consumers.

For `--format both`, the manifest's `asset` points at the PNG and the WebP sibling is written beside it.
