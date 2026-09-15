"""Reproduce the local DeepFilterNet comparison; requires NumPy and FFmpeg."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time
import wave
import numpy as np

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--transcript', type=Path, required=True)
p.add_argument('--denoiser', type=Path, required=True)
p.add_argument('--model', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--start', type=float, default=16)
p.add_argument('--duration', type=float, default=14)
p.add_argument('--stream', default='0:a:3')
a = p.parse_args()
a.output.mkdir(parents=True, exist_ok=False)
sr = 48000

def write(path, x):
    assert np.max(np.abs(x)) < 1, 'Clipping in output'
    with wave.open(str(path), 'wb') as w:
        w.setparams((1, 2, sr, 0, 'NONE', 'not compressed'))
        w.writeframes((x * 32767).astype('<i2').tobytes())

def read(path):
    with wave.open(str(path)) as w:
        assert w.getframerate() == sr and w.getnchannels() == 1 and w.getsampwidth() == 2
        return np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float) / 32768

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

command = ['ffmpeg', '-v', 'error', '-ss', str(a.start), '-t', str(a.duration), '-i', str(a.source), '-map', a.stream, '-vn', '-ar', str(sr), '-ac', '1', '-f', 'f32le', '-']
x = np.frombuffer(subprocess.check_output(command), dtype='<f4').astype(float)
assert len(x) == round(a.duration * sr)
peak = np.max(np.abs(x))
assert peak > 0
gain = 10 ** (-6 / 20) / peak
x *= gain
# v0.5.6 compensation removes 30 ms from the tail. Supply a tail handle,
# then keep the original number of samples, preserving the end of speech.
write(a.output / 'input.wav', np.pad(x, (0, 4800)))
variants = {'original': x}
runs = []
for name, limit in [('gentle', 12), ('stronger', 24)]:
    cmd = [str(a.denoiser), '-m', str(a.model), '-D', '-a', str(limit), '-o', str(a.output / name), str(a.output / 'input.wav')]
    start = time.monotonic()
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    elapsed = time.monotonic() - start
    assert 'clipping' not in (r.stdout + r.stderr).lower(), r.stdout + r.stderr
    enhanced = read(a.output / name / 'input.wav')
    assert len(enhanced) >= len(x), 'Model truncated source speech'
    variants[name] = enhanced[:len(x)]
    runs.append({'variant': name, 'attenuation_limit_db': limit, 'elapsed_seconds': elapsed, 'command': cmd})

mask = np.zeros(len(x), dtype=bool)
words = []
for segment in json.loads(a.transcript.read_text())['segments']:
    for word in segment.get('words', []):
        begin = max(0, round((word['start'] - a.start) * sr))
        end = min(len(x), round((word['end'] - a.start) * sr))
        if end > begin:
            mask[begin:end] = True
            words.append({'start': begin / sr, 'end': end / sr, 'word': word['word']})
assert mask.sum() > sr
match = {}
for name, v in variants.items():
    rms = np.sqrt(np.mean(v[mask] ** 2))
    factor = 10 ** (-20 / 20) / rms
    variants[name] = v * factor
    match[name] = {'speech_match_gain_db': float(20 * np.log10(factor))}
# Shared final gain preserves matching while protecting all variants' peaks.
cap = min(1.0, 10 ** (-1.5 / 20) / max(np.max(np.abs(v)) for v in variants.values()))
for name, v in variants.items():
    v *= cap
    out = a.output / (name + '.wav')
    write(out, v)
    match[name].update({'sha256': sha(out), 'frames': len(v), 'peak_dbfs': float(20 * np.log10(np.max(np.abs(v)))), 'speech_rms_dbfs': float(20 * np.log10(np.sqrt(np.mean(v[mask] ** 2))))})
report = {'status': 'rendered locally; human listening verdict pending', 'source': str(a.source), 'source_sha256': sha(a.source), 'start': a.start, 'duration': a.duration, 'stream': a.stream, 'model_sha256': sha(a.model), 'binary_sha256': sha(a.denoiser), 'version': subprocess.check_output([str(a.denoiser), '-V'], text=True).strip(), 'shared_input_gain_db': float(20 * np.log10(gain)), 'tail_padding_seconds': 0.1, 'delay_compensation': True, 'sample_rate': sr, 'normalization': 'RMS on identical source-transcript word windows; linear gain only', 'common_output_gain_db': float(20 * np.log10(cap)), 'speech_windows': words, 'runs': runs, 'outputs': match}
(a.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ['status', 'version', 'outputs']}, indent=2))
