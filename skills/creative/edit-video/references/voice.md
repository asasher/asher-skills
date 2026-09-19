# Voice cleanup

Select the actual microphone stream before denoising. Compare noise during speech and pauses. Preserve wording, voice identity, breaths, synchronization, and duration. Neural noise reduction is not a reliable repair for clipping or a substitute for a better take.

## Local model path

DeepFilterNet 3 is a local starting option for hiss and background noise. Use a supported native executable or a project-local environment; keep the executable and weights explicit. Record their versions and hashes. The reviewed native CLI is DeepFilterNet v0.5.6 with DFN3 ONNX weights. It accepts `-m MODEL -D -a LIMIT_DB -o DIRECTORY INPUT.wav`; check the installed CLI before adapting another version.

On Apple Silicon, the pinned executable is `https://github.com/Rikorose/DeepFilterNet/releases/download/v0.5.6/deep-filter-0.5.6-aarch64-apple-darwin` (SHA-256 `4601e7f4e4c03e59a4c5b5000216ef3add3e808799cfccd95e14e83ea4611081`). Weights: `https://raw.githubusercontent.com/Rikorose/DeepFilterNet/v0.5.6/models/DeepFilterNet3_onnx.tar.gz` (SHA-256 `c94d91f70911001c946e0fabb4aa9adc37045f45a03b56008cb0c8244cb63616`). Verify downloads before executing. Other architectures require their matching build.

Use `scripts/clean_voice.py` from this skill with explicit source, stream, denoiser, model, attenuation, and a fresh output directory. It needs FFmpeg and NumPy. The helper converts the selected track to 48 kHz mono, supplies a tail handle for native v0.5.6 delay compensation, and retains the decoded source sample count. It writes dry and processed audio plus a treatment record. Example arguments:

```text
--source recording.mp4 --stream 0:a:3 --denoiser /path/to/deep-filter
--model /path/to/DeepFilterNet3_onnx.tar.gz --attenuation-db 24 --output audio/pass-1
```

`0:a:3` is an example of the fourth audio stream, not a default microphone choice. Use the stream selected from this recording. The 24 dB attenuation limit is a stronger candidate; use the project's preference or compare against a gentler candidate such as 12 dB. Keep postfilter off unless separately justified.

## Listen, then commit the treatment

Try a representative passage before processing all takes. Include speech, pauses, and a boundary. Match versions on the same active-speech windows with linear gain for listening; silence-heavy whole-file averages can make the noisier version seem louder. The helper preserves common input gain but does not perform perceptual loudness matching.

Listen for missing consonants, metallic texture, pumping, excessive breath removal, and changes in the noise floor at joins. If the stronger pass harms speech, reduce treatment or retain the source. Carry handles when cleaning individual selected clips, then trim to the intended boundaries. Prefer treating a continuous take before making its editorial cuts.

Measure loudness and true peak after assembly and again on the encoded result. Use the delivery brief's target; -16 LUFS and -1.5 dBTP are reasonable initial project choices, not universal platform requirements. Keep two-pass normalization preprocessing identical. Record any EQ, gain, or compression separately from neural denoising so their effects remain distinguishable.
