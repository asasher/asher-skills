# Local media tools

- FFmpeg and FFprobe are on PATH.
- Python dependencies are in `.venv`; use `.venv/bin/python`. NumPy, Pillow, and MLX Whisper are available there.
- DeepFilterNet executable: `.tools/deep-filter` (v0.5.6). Model: `.tools/DeepFilterNet3_onnx.tar.gz`.
- Playwright is installed in this project. Chrome is at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. Set `CHROME_PATH` to this path when using a renderer that accepts it.
- Local transcription can use `mlx-community/whisper-large-v3-turbo`; record the actual model/version selected. Model downloads use the local Hugging Face cache.

`raw/` contains independent read-only copies of the selected OBS recording group. Determine each file's actual usable content, quality, audio stream, and sync from the recordings. Generated media belongs in `work/` or `output/`.
