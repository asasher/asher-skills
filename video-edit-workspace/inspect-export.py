#!/usr/bin/env python3
"""Record independent decode, stream, loudness, and caption-timing evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--video', required=True, type=Path)
p.add_argument('--captions', required=True, type=Path)
p.add_argument('--out', required=True, type=Path)
a = p.parse_args()
a.out.mkdir(parents=True, exist_ok=True)
probe = json.loads(subprocess.check_output([
    'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(a.video)
], text=True))
(a.out / 'ffprobe.json').write_text(json.dumps(probe, indent=2) + '\n')
command = ['ffmpeg', '-hide_banner', '-nostats', '-xerror', '-i', str(a.video),
           '-map', '0:v:0', '-map', '0:a:0',
           '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-']
decode = subprocess.run(command, capture_output=True, text=True)
(a.out / 'decode.log').write_text(decode.stderr)
measurement = re.search(r'\{\s*"input_i"[\s\S]*?\}', decode.stderr)
video = [s for s in probe['streams'] if s['codec_type'] == 'video']
audio = [s for s in probe['streams'] if s['codec_type'] == 'audio']
duration = float(probe['format']['duration'])
timing = re.compile(r'(\d{2}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}[,.]\d{3})')
def seconds(value):
    h, m, s = value.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
cues = [(seconds(start), seconds(end)) for start, end in timing.findall(a.captions.read_text())]
errors = []
for i, (start, end) in enumerate(cues):
    if not 0 <= start < end <= duration + .05:
        errors.append({'cue': i + 1, 'reason': 'out of range or nonpositive duration'})
    if i and start < cues[i - 1][1]:
        errors.append({'cue': i + 1, 'reason': 'overlaps previous cue'})
digest = hashlib.sha256()
with a.video.open('rb') as source:
    for chunk in iter(lambda: source.read(8 * 1024 * 1024), b''):
        digest.update(chunk)
report = {
    'video': str(a.video), 'video_sha256': digest.hexdigest(),
    'duration_seconds': duration,
    'decode': {'exit_code': decode.returncode, 'pass': decode.returncode == 0, 'command': command},
    'video_streams': [{k: s.get(k) for k in ['codec_name', 'width', 'height', 'pix_fmt', 'r_frame_rate', 'avg_frame_rate', 'duration']} for s in video],
    'audio_streams': [{k: s.get(k) for k in ['codec_name', 'sample_rate', 'channels', 'duration']} for s in audio],
    'loudness': json.loads(measurement.group()) if measurement else None,
    'caption_timing': {'file': str(a.captions), 'count': len(cues), 'errors': errors, 'pass': bool(cues) and not errors},
    'limits': 'Decode and timing checks do not establish natural speech, audiovisual sync, caption accuracy, motion quality, or destination UI clearance.'
}
(a.out / 'technical.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
if decode.returncode or not cues or errors:
    raise SystemExit(1)
