# Prompts for Extractable Sheets

Good extraction starts with a boring background and isolated subjects. Use this guidance both when prompting
an image model yourself and when passing `--generate`, because `--generate` forwards the subject guidance to
the bundled `codex-imagegen` generator.

## Grid Sheet Prompt

Ask for:

- A fixed grid: exact rows and columns, equal cell size, no overlaps.
- A solid flat key background covering the entire image, usually pure magenta `#FF00FF` or pure green
  `#00FF00`.
- One centered element per cell with transparent-able padding around it.
- No shadows that touch neighboring cells.
- No text, labels, checkerboard transparency, gradients, or decorative background elements.
- No subject pixels matching or nearly matching the key color.

Example subject:

```text
4 by 4 sprite sheet of isometric fantasy terrain tiles, one tile centered in each cell, consistent scale,
isolated non-touching shapes, flat pure magenta background behind every tile, no text, no checkerboard,
no pure magenta pixels inside the tiles
```

## Packed Sheet Prompt

For components mode, ask for isolated objects on one flat key background:

```text
16 separate top-down potion bottle sprites arranged with clear space between every bottle, consistent
lighting and scale, flat pure green background, no contact between objects, no labels, no shadows touching
another object, no pure green inside any bottle
```

## Key Choice

Use magenta for green/brown/gray subjects such as foliage, terrain, stone, and wood. Use green only when the
subjects contain no greens and no green fringe would be plausible. If validation reports key remnants or
keyed holes, regenerate on the other key color or pass an explicit `--key #RRGGBB`.
