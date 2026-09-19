#!/usr/bin/env python3
"""Run explicit local DFN3 treatment while preserving the decoded sample count."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import wave

import numpy as np


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_wav(path, audio):
    if not np.isfinite(audio).all() or np.max(np.abs(audio)) >= 1:
        raise ValueError('Audio is nonfinite or would clip')
    with wave.open(str(path), 'wb') as f:
        f.setparams((1, 2, 48000, 0, 'NONE', 'not compressed'))
        f.writeframes(np.rint(audio * 32767).astype('<i2').tobytes())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--stream', required=True, help='Explicit ffmpeg selector, e.g. 0:a:3')
    p.add_argument('--denoiser', type=Path, required=True)
    p.add_argument('--model', type=Path, required=True)
    p.add_argument('--attenuation-db', type=float, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--start', type=float, default=0)
    p.add_argument('--duration', type=float)
    a = p.parse_args()
    if a.start < 0 or (a.duration is not None and a.duration <= 0) or not 0 <= a.attenuation_db <= 100:
        p.error('Use a nonnegative start, positive duration, and attenuation between 0 and 100 dB')
    for f in [a.source, a.denoiser, a.model]:
        if not f.is_file():
            p.error(f'File not found: {f}')
    version = subprocess.check_output([str(a.denoiser.resolve()), '-V'], text=True).strip()
    if version != 'deep_filter 0.5.6':
        p.error(f'Helper validated for deep_filter 0.5.6; inspect/adapt the delay path for {version}')
    a.output.mkdir(parents=True, exist_ok=False)
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(a.start), '-i', str(a.source.resolve())]
    if a.duration is not None:
        cmd += ['-t', str(a.duration)]
    cmd += ['-map', a.stream, '-vn', '-ar', '48000', '-ac', '1', '-f', 'f32le', '-']
    audio = np.frombuffer(subprocess.check_output(cmd), dtype='<f4').astype(np.float64)
    if not len(audio) or not np.isfinite(audio).all():
        raise ValueError('Selected stream is empty or nonfinite')
    peak = float(np.max(np.abs(audio)))
    if peak < 1e-7:
        raise ValueError('Selected stream is effectively silent; inspect track selection')
    # Keep headroom for conversion and neural processing, without boosting quiet inputs.
    input_gain = min(1.0, 10 ** (-6 / 20) / peak)
    audio *= input_gain
    # v0.5.6 -D consumes 30 ms at the tail; a 100 ms handle protects retained samples.
    model_input = a.output / 'model-input.wav'
    write_wav(model_input, np.pad(audio, (0, 4800)))
    command = [str(a.denoiser.resolve()), '-m', str(a.model.resolve()), '-D', '-a', str(a.attenuation_db), '-o', str((a.output / 'model-output').resolve()), str(model_input.resolve())]
    result = subprocess.run(command, capture_output=True, text=True)
    (a.output / 'denoiser.log').write_text(result.stdout + result.stderr)
    result.check_returncode()
    if 'clipping' in (result.stdout + result.stderr).lower():
        raise ValueError('Denoiser reported clipping; inspect the saved log and reduce input gain')
    with wave.open(str(a.output / 'model-output/model-input.wav'), 'rb') as f:
        if (f.getnchannels(), f.getsampwidth(), f.getframerate()) != (1, 2, 48000):
            raise ValueError('Unexpected denoiser output format')
        wet = np.frombuffer(f.readframes(f.getnframes()), dtype='<i2').astype(np.float64) / 32768
    if len(wet) < len(audio):
        raise ValueError('Denoiser output shortened source speech despite the handle')
    wet = wet[:len(audio)]
    if not np.isfinite(wet).all():
        raise ValueError('Nonfinite denoiser output')
    common_gain = min(1.0, 10 ** (-1.5 / 20) / max(float(np.max(np.abs(wet))), float(np.max(np.abs(audio)))))
    paths = {'dry': a.output / 'dry.wav', 'processed': a.output / 'processed.wav'}
    write_wav(paths['dry'], audio * common_gain)
    write_wav(paths['processed'], wet * common_gain)
    report = {
        'source': str(a.source.resolve()), 'source_sha256': sha(a.source),
        'stream': a.stream, 'start_seconds': a.start, 'requested_duration_seconds': a.duration,
        'sample_rate': 48000, 'channels': 1, 'frames': len(audio),
        'duration_seconds': len(audio) / 48000, 'denoiser_version': version,
        'denoiser_sha256': sha(a.denoiser), 'model_sha256': sha(a.model),
        'attenuation_limit_db': a.attenuation_db, 'delay_compensation': True,
        'tail_handle_seconds': 0.1, 'input_gain_db': float(20 * np.log10(input_gain)),
        'common_output_gain_db': float(20 * np.log10(common_gain)),
        'perceptually_loudness_matched': False, 'naturalness': 'requires listening',
        'command': command,
        'outputs': {k: {'path': str(v.resolve()), 'sha256': sha(v)} for k, v in paths.items()},
    }
    (a.output / 'treatment.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'frames': len(audio), 'output': str(a.output.resolve())}))


if __name__ == '__main__':
    main()
