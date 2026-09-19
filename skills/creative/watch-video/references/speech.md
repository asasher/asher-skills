# Speech and timing evidence

Probe the audio streams and choose the one carrying the relevant speaker. Record the FFmpeg stream selector. OBS recordings can contain silent tracks or a mix alongside a clean microphone track.

On Apple Silicon, local MLX Whisper is an option for word-timed transcription. Install it in a project-local environment, select an explicit model, and retain its version/model identifier. Extract the selected stream with FFmpeg to mono 16 kHz WAV, then transcribe with word timestamps. The Python API is `mlx_whisper.transcribe(path, path_or_hf_repo=MODEL, word_timestamps=True)`; check the installed package when adapting versions. A model such as `mlx-community/whisper-large-v3-turbo` may require an initial download. Use another available transcriber when the platform differs or the brief requires diarization.

Save machine-readable word/segment timings and a concise phrase view with source timestamps. If an excerpt was extracted, add its source offset to every timestamp. Preserve the source path, selected stream, extraction interval, and model in the record. Flag uncertain words and compare them with full-resolution screen evidence where relevant.

Transcription does not prove natural audio or sample-accurate boundaries. For a disputed cut, inspect dense frames and the waveform around the speech; audition when possible. Mark unverified audio, motion between samples, and exact boundary uncertainty separately. Provide observations with timestamps, not an editorial decision about what a finished video should retain.
