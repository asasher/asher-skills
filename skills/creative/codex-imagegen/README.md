# Codex Imagegen

Generate immutable raster assets in three modes: flat images with chroma-key transparency, independently generated scene layers with a derived composite, and named sprites extracted from a generated or supplied sheet.

Backend priority is configured CLIProxyAPI, then native Codex, then an available direct OpenAI Platform key with explicit user permission. The proxy client uses an existing gateway bearer key and the Images API; it works independently of native image-tool availability. All implementation ships here, using stdlib HTTP plus the existing Pillow/NumPy dependencies.

See [backend configuration](reference/backends.md) for URL/key discovery, explicit selection, native requirements, and [direct API permission](reference/api-key-path.md). Configuration is read-only. Requests are sequential; failures preserve completed artifacts and stop without retries or provider switching.

Files and directories share a monotonic version family. Outputs report actual decoded dimensions; flat generation preserves them, and layered manifests make composition resizing explicit. Size and quality control depend on the selected provider.

## Validation

Run `python3 -m unittest discover -s skills/creative/codex-imagegen/tests -v` from this repository. Tests use a local HTTP server, cover all generated artifact modes and the native adapter, and require no live credentials. A live smoke also needs visual inspection; record its requested model/size, actual dimensions, and artifact path.

## Credits

- The native Codex adapter is an original empirical integration recipe; the Images API client is an original stdlib implementation.
- Sprite extraction formerly shipped here as `to-sprites`; it shares keying, generation, and versioning with this package.
