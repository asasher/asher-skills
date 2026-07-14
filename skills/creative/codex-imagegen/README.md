# Codex Imagegen

One raster-asset skill with three immutable artifact modes:

- flat image generation and chroma-key transparency;
- asset-first layered generation with independent layer PNGs plus a derived composite;
- keyed sprite-sheet generation/extraction with named assets and a manifest.

Flat files and directory artifacts share one monotonic version family, so iterating among modes never destroys an earlier generation.

## Credits

- **Relationship:** the Codex image-generation integration is an original empirical recipe.
- **Consolidation:** the sprite extraction implementation formerly shipped in this repository as `to-sprites`; it now shares keying, generation, and versioning with `codex-imagegen`.
- **Internal compatibility:** follows the local OpenAI image-generation helper's output conventions without copying or owning that system skill.
