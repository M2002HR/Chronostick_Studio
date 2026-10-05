#!/usr/bin/env python3
"""Fixed-picture finishing: actual word timing, active-word ASS and explicit stems."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from PIL import ImageFont


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)
    ]))


def resolve(root, value):
    p = Path(value).expanduser()
    return p.resolve() if p.is_absolute() else (root / p).resolve()


def finite(value, name):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f'{name} must be finite')
    return result


def default_caption_style(width, height):
    """New configurations use separate Shorts/long-form typography profiles."""
    portrait = height > width
    family = 'Montserrat' if portrait else 'Arial'
    font_path = subprocess.check_output(
        ['fc-match', '-f', '%{file}', f'{family}:style=Bold'], text=True).strip()
    return dict(profile='shorts-reference-bold' if portrait else 'longform-arial-bold',
                font_family=family, font_file=font_path,
                font_size=round(height * (104 / 1920 if portrait else 64 / 1080)),
                max_width_fraction=.8,
                bottom_margin=round(height * (300 / 1920 if portrait else 88 / 1080)),
                outline=2 if portrait else 2.5, shadow=2 if portrait else 1,
                highlight_ass_color='&H00D7FF&',
                max_words=4 if portrait else 12,
                max_cue_seconds=1.8 if portrait else 4,
                break_gap_seconds=.3 if portrait else .45, max_lines=1)


def load_words(path, offset=0, adjustments=(), boundary_repairs=()):
    words = []
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        for n, row in enumerate(csv.DictReader(f), 1):
            start, end = finite(row['start'], 'word start'), finite(row['end'], 'word end')
            if start < 0 or end <= start or not row['word'].strip():
                raise ValueError(f'Invalid timestamp row {n}')
            shift = sum(finite(a['offset_seconds'], 'timing adjustment')
                        for a in adjustments if n >= int(a['first_word_index']))
            words.append(dict(index=n, word=row['word'].strip(), source_start=start,
                              source_end=end, start=start + offset + shift,
                              end=end + offset + shift))
    if not words:
        raise ValueError('Word timing is empty')
    for repair in boundary_repairs:
        index = int(repair['word_index']) - 1
        if not 0 < index < len(words) or repair['method'] != 'previous_source_word_end':
            raise ValueError('Invalid explicit caption boundary repair')
        previous, current = words[index - 1], words[index]
        if not 0 < current['source_start'] - previous['source_start'] <= .01:
            raise ValueError('End-boundary fallback is only for near-duplicate provider starts')
        current['start'] = previous['end']
        if current['start'] >= current['end']:
            raise ValueError('Source end cannot resolve this duplicate start; re-align actual audio')
        current['display_boundary_repair'] = repair
    for a, b in zip(words, words[1:]):
        if b['start'] <= a['start']:
            raise ValueError('Word starts must be strictly increasing')
    if words[0]['start'] < 0:
        raise ValueError('Narration offset makes a word start negative')
    return words


def centiseconds(t):
    return int(math.floor(t * 100 + 0.5))


def ass_time(cs):
    return f'{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}'


def plain_time(t, separator=','):
    ms = int(math.floor(t * 1000 + 0.5))
    return f'{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02}{separator}{ms % 1000:03}'


def escape_ass(word):
    # ASS braces and slashes can inject formatting. Preserve literal typography.
    return word.replace('\\', '＼').replace('{', '｛').replace('}', '｝').replace('\n', ' ')


def split_lines(words, font, max_width, max_lines=2):
    text = ' '.join(w['word'] for w in words)
    if font.getlength(text) <= max_width:
        return [words]
    if max_lines == 1:
        return None
    candidates = []
    for n in range(1, len(words)):
        a, b = words[:n], words[n:]
        wa = font.getlength(' '.join(w['word'] for w in a))
        wb = font.getlength(' '.join(w['word'] for w in b))
        if max(wa, wb) <= max_width:
            candidates.append((abs(wa - wb), n))
    if not candidates:
        return None
    _, n = min(candidates)
    return [words[:n], words[n:]]


def make_cues(words, style, font, width):
    max_width = width * style['max_width_fraction']
    cues, group = [], []

    def finish():
        if group:
            lines = split_lines(group.copy(), font, max_width, style.get('max_lines', 2))
            if lines is None:
                raise ValueError('A single caption word is wider than the safe area')
            cues.append(dict(words=group.copy(), lines=lines,
                             start=group[0]['start'], end=group[-1]['end']))
            group.clear()

    for word in words:
        if group and (len(group) >= style['max_words']
                      or word['end'] - group[0]['start'] > style['max_cue_seconds']
                      or word['start'] - group[-1]['end'] >= style['break_gap_seconds']
                      or split_lines(group + [word], font, max_width, style.get('max_lines', 2)) is None):
            finish()
        group.append(word)
        duration = word['end'] - group[0]['start']
        if re.search(r'[.!?…]$', word['word']) or (
                re.search(r'[,;:]$', word['word']) and len(group) >= 4 and duration >= 1):
            finish()
    finish()
    # Source-provider ends occasionally overlap the next cue. The later start wins.
    for a, b in zip(cues, cues[1:]):
        a['end'] = min(a['end'], b['start'])
    return cues


def cue_text(cue, active, highlight):
    lines = []
    for line in cue['lines']:
        rendered = []
        for w in line:
            word = escape_ass(w['word'])
            if w['index'] == active:
                word = '{\\1c' + highlight + '}' + word + '{\\1c&HFFFFFF&}'
            rendered.append(word)
        lines.append(' '.join(rendered))
    return '\\N'.join(lines)


def caption_events(cues, highlight):
    events = []
    for cue in cues:
        start, end = centiseconds(cue['start']), centiseconds(cue['end'])
        boundaries = {start, end}
        for w in cue['words']:
            boundaries.update((max(start, min(end, centiseconds(w['start']))),
                               max(start, min(end, centiseconds(w['end'])))))
        times = sorted(boundaries)
        for a, b in zip(times, times[1:]):
            if b <= a:
                continue
            # A newly started word replaces an overlapping earlier word; it does
            # not reactivate the earlier word after the new one finishes.
            started = [w for w in cue['words'] if centiseconds(w['start']) <= a]
            latest = started[-1] if started else None
            active = latest['index'] if latest and a < centiseconds(latest['end']) else None
            text = cue_text(cue, active, highlight)
            if events and events[-1]['end_cs'] == a and events[-1]['text'] == text:
                events[-1]['end_cs'] = b
            else:
                events.append(dict(start_cs=a, end_cs=b, active_word_index=active, text=text))
    return events


def snap_events_to_frames(events, fps):
    result = []
    for event in events:
        start = math.floor(round(event['start_cs'] * fps / 100) / fps * 100 + 1e-7)
        end = math.floor(round(event['end_cs'] * fps / 100) / fps * 100 + 1e-7)
        if end > start:
            result.append(dict(event, unquantized_start_cs=event['start_cs'],
                               unquantized_end_cs=event['end_cs'], start_cs=start, end_cs=end))
    return result


def write_captions(folder, words, style, font_path, width, height, fps=24):
    font = ImageFont.truetype(str(font_path), style['font_size'])
    cues = make_cues(words, style, font, width)
    events = snap_events_to_frames(caption_events(cues, style['highlight_ass_color']), fps)
    margin = math.ceil(width * (1 - style['max_width_fraction']) / 2)
    header = f'''[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,{style['font_family']},{style['font_size']},&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,{style['outline']},{style['shadow']},2,{margin},{margin},{style['bottom_margin']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    ass = header + ''.join(f"Dialogue: 0,{ass_time(e['start_cs'])},{ass_time(e['end_cs'])},Caption,,0,0,0,,{e['text']}\n" for e in events)
    (folder / 'captions.ass').write_text(ass, encoding='utf-8')
    srt, vtt = [], ['WEBVTT\n']
    for i, c in enumerate(cues, 1):
        text = '\n'.join(' '.join(w['word'] for w in line) for line in c['lines'])
        srt.append(f"{i}\n{plain_time(c['start'])} --> {plain_time(c['end'])}\n{text}\n")
        vtt.append(f"{plain_time(c['start'], '.')} --> {plain_time(c['end'], '.')}\n{text}\n")
    (folder / 'captions.srt').write_text('\n'.join(srt), encoding='utf-8')
    (folder / 'captions.vtt').write_text('\n'.join(vtt), encoding='utf-8')
    report = dict(word_count=len(words), cue_count=len(cues), event_count=len(events),
                  end_seconds=words[-1]['end'], style=style, words=words, cues=cues,
                  events=events, overlap_rule='latest start wins; no cumulative highlight',
                  time_resolution_seconds=0.01, display_quantization='nearest picture frame; ASS boundary floored to centiseconds',
                  fps=fps, max_lines=style.get('max_lines', 2))
    write_json(folder / 'caption-timing.json', report)
    return report


def measure(cmd, log):
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    Path(log).write_text(result.stderr)
    if result.returncode:
        raise RuntimeError(f'FFmpeg failed; inspect {log}')
    matches = re.findall(r'\{\s*"input_i".*?\}', result.stderr, re.S)
    if not matches:
        raise RuntimeError(f'Loudness measurement missing; inspect {log}')
    data = json.loads(matches[-1])
    if not all(math.isfinite(float(data[k])) for k in ('input_i', 'input_tp', 'input_lra', 'input_thresh', 'target_offset')):
        raise ValueError('Audio is silent or has invalid loudness')
    return data


def loudness_filter(target, measured=None):
    base = f"loudnorm=I={target['integrated_lufs']}:TP={target['true_peak_dbtp']}:LRA={target['lra']}"
    if measured:
        base += (f":measured_I={measured['input_i']}:measured_TP={measured['input_tp']}"
                 f":measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}"
                 f":offset={measured['target_offset']}:linear=true")
    return base + ':print_format=json'


def run(cmd, log):
    with Path(log).open('w') as f:
        result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'Command failed; inspect {log}')


def mix_graph(tracks, duration):
    ducks = sum(bool(t.get('duck_under_narration')) for t in tracks)
    graph = [f'[0:a]apad,atrim=duration={duration},asetpts=PTS-STARTPTS[voice]']
    if ducks:
        graph.append('[voice]asplit=' + str(ducks + 1) + '[main]' + ''.join(f'[sc{i}]' for i in range(ducks)))
        mixed = ['[main]']
    else:
        mixed = ['[voice]']
    sc = 0
    for i, track in enumerate(tracks, 1):
        length = track['duration_seconds']
        chain = (f"[{i}:a]atrim=start={track.get('source_start_seconds', 0)}:duration={length},"
                 f"asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                 f"volume={track.get('gain_db', 0)}dB")
        for key, typ, st in [('fade_in_seconds', 'in', 0), ('fade_out_seconds', 'out', None)]:
            fade = track.get(key, 0)
            if fade:
                chain += f",afade=t={typ}:st={st if st is not None else length - fade}:d={fade}"
        chain += f",adelay={round(track.get('start_seconds', 0) * 48000)}S:all=1,apad,atrim=duration={duration}[t{i}]"
        graph.append(chain)
        if track.get('duck_under_narration'):
            graph.append(f'[t{i}][sc{sc}]sidechaincompress=threshold=0.025:ratio=8:attack=20:release=300[d{i}]')
            mixed.append(f'[d{i}]')
            sc += 1
        else:
            mixed.append(f'[t{i}]')
    graph.append(''.join(mixed) + f'amix=inputs={len(mixed)}:duration=longest:normalize=0,atrim=duration={duration}[mix]')
    return ';'.join(graph)


def prepare(root, config):
    if config.get('schema_version') != '1.0':
        raise ValueError('Unsupported post-production schema')
    picture = resolve(root, config['picture'])
    voice = resolve(root, config['narration']['path'])
    timing = resolve(root, config['timing']['path'])
    for path, expected in [(picture, config['picture_sha256']), (voice, config['narration']['sha256']),
                           (timing, config['timing']['sha256'])]:
        if digest(path) != expected:
            raise ValueError(f'Input hash changed: {path}')
    pp, vp = probe(picture), probe(voice)
    video = next(s for s in pp['streams'] if s['codec_type'] == 'video')
    voice_stream = next(s for s in vp['streams'] if s['codec_type'] == 'audio')
    duration = float(video['duration'])
    offset = finite(config['narration'].get('offset_seconds', 0), 'narration offset')
    if offset < 0 or float(voice_stream['duration']) + offset > duration + 0.02:
        raise ValueError('Narration exceeds the picture timeline; never truncate it')
    words = load_words(timing, offset, config['timing'].get('adjustments', []),
                       config['timing'].get('start_boundary_repairs', []))
    if words[-1]['end'] > float(voice_stream['duration']) + offset + 0.02:
        raise ValueError('Word timestamps exceed the supplied narration')
    timing_voice_hash = config['timing']['source_voice_sha256']
    if timing_voice_hash != digest(voice):
        alignment = config['timing'].get('alignment_evidence')
        if not alignment:
            raise ValueError('Timings belong to a different voice; actual alignment evidence required')
        evidence = json.loads(resolve(root, alignment).read_text())
        if (evidence['source_voice_sha256'] != timing_voice_hash or
                evidence['target_voice_sha256'] != digest(voice) or
                evidence['adjustments'] != config['timing'].get('adjustments', [])):
            raise ValueError('Voice alignment evidence does not match this configuration')
    font_path = resolve(root, config['captions']['font_file'])
    style = config['captions']
    if (not 0 < finite(style['max_width_fraction'], 'caption width') <= 1
            or not 0 < finite(style['font_size'], 'font size') < video['height']
            or not 0 <= finite(style['bottom_margin'], 'bottom margin') < video['height']
            or int(style['max_words']) < 1 or finite(style['max_cue_seconds'], 'cue duration') <= 0
            or finite(style['break_gap_seconds'], 'caption gap') < 0
            or finite(style['outline'], 'caption outline') < 0 or finite(style['shadow'], 'caption shadow') < 0
            or style.get('max_lines', 2) not in (1, 2)
            or not re.fullmatch(r'&H[0-9A-Fa-f]{6}&', style['highlight_ass_color'])):
        raise ValueError('Invalid caption typography or timing settings')
    font = ImageFont.truetype(str(font_path), style['font_size'])
    family, face = font.getname()
    if family != config['captions']['font_family'] or 'bold' not in face.lower():
        raise ValueError(f'Exact bold font required; found {family} {face}')
    cues = make_cues(words, style, font, video['width'])
    fps = float(Fraction(video['avg_frame_rate']))
    events = snap_events_to_frames(caption_events(cues, style['highlight_ass_color']), fps)
    if len({e['active_word_index'] for e in events if e['active_word_index'] is not None}) != len(words):
        raise ValueError('Some words have no visible interval; resolve provider boundary collisions explicitly')
    if config['native_audio']['mode'] not in ('mute', 'preserve'):
        raise ValueError('Native audio must explicitly be mute or preserve')
    tracks = [dict(t) for t in config.get('tracks', [])]
    if any(t['role'] == 'music' for t in tracks) and not config.get('external_music_allowed'):
        raise ValueError('External music is disabled in this finishing configuration')
    if config['native_audio']['mode'] == 'preserve':
        tracks.insert(0, dict(role='native', path=str(picture), sha256=digest(picture),
                              start_seconds=0, duration_seconds=duration,
                              gain_db=config['native_audio'].get('gain_db', -12)))
    for t in tracks:
        if t['role'] not in ('native', 'music', 'ambience', 'sfx'):
            raise ValueError('Unknown audio track role')
        t['path'] = str(resolve(root, t['path']))
        if digest(t['path']) != t['sha256']:
            raise ValueError(f"Track hash changed: {t['path']}")
        start = finite(t.get('start_seconds', 0), 'track start')
        source = finite(t.get('source_start_seconds', 0), 'source start')
        length = finite(t['duration_seconds'], 'track duration')
        if start < 0 or source < 0 or length <= 0 or start + length > duration + 0.001:
            raise ValueError('Audio track falls outside the picture timeline')
        for k in ('fade_in_seconds', 'fade_out_seconds'):
            if not 0 <= finite(t.get(k, 0), k) <= length:
                raise ValueError('Invalid track fade duration')
        finite(t.get('gain_db', 0), 'track gain')
        audio = next(s for s in probe(t['path'])['streams'] if s['codec_type'] == 'audio')
        if not t.get('loop') and source + length > float(audio['duration']) + 0.02:
            raise ValueError('Audio cue is longer than its source; declare looping explicitly')
    return picture, voice, words, font_path, video, duration, tracks


def render(root, config, output, package):
    picture, voice, words, font_path, video, duration, tracks = prepare(root, config)
    if output.exists() or package.exists() or output.with_suffix('.postproduction.json').exists():
        raise FileExistsError('Finishing outputs are immutable; choose the next revision')
    package.mkdir(parents=True)
    write_json(package / 'edit-snapshot.json', config)
    report = write_captions(package, words, config['captions'], font_path, video['width'], video['height'],
                            float(Fraction(video['avg_frame_rate'])))
    highlighted = {e['active_word_index'] for e in report['events'] if e['active_word_index'] is not None}
    if len(highlighted) != len(words):
        raise ValueError('Some words have no display interval; resolve provider boundary collisions explicitly')
    print(f"Captions: {report['word_count']} words / {report['cue_count']} cues", flush=True)
    target = config['loudness']
    voice_measure = measure(['ffmpeg', '-hide_banner', '-i', str(voice), '-map', '0:a:0', '-vn', '-sn',
                             '-af', loudness_filter(target), '-f', 'null', '-'], package / 'voice-measure.log')
    write_json(package / 'voice-loudness.json', voice_measure)
    offset = float(config['narration'].get('offset_seconds', 0))
    af = loudness_filter(target, voice_measure) + f',aresample=48000,adelay={round(offset * 48000)}S:all=1,apad,atrim=duration={duration}'
    stem = package / 'narration.flac'
    run(['ffmpeg', '-hide_banner', '-n', '-i', str(voice), '-map', '0:a:0', '-vn', '-sn', '-af', af,
         '-ar', '48000', '-ac', '2', '-c:a', 'flac', str(stem)], package / 'voice-normalize.log')
    mix = stem
    if tracks:
        mix = package / 'mix.flac'
        cmd = ['ffmpeg', '-hide_banner', '-n', '-i', str(stem)]
        for t in tracks:
            if t.get('loop'):
                cmd += ['-stream_loop', '-1']
            cmd += ['-i', t['path']]
        graph = mix_graph(tracks, duration)
        (package / 'mix-filter.txt').write_text(graph)
        cmd += ['-filter_complex', graph, '-map', '[mix]', '-ar', '48000', '-ac', '2', '-c:a', 'flac', str(mix)]
        run(cmd, package / 'mix.log')
    final_measure = measure(['ffmpeg', '-hide_banner', '-i', str(mix), '-af', loudness_filter(target),
                             '-f', 'null', '-'], package / 'mix-measure.log')
    write_json(package / 'mix-loudness.json', final_measure)
    # Copy only the exact font to a simple relative staging path. FFmpeg's filter
    # parser never sees arbitrary paths, quotes, colons or shell interpolations.
    (package / 'fonts').mkdir()
    shutil.copyfile(font_path, package / 'fonts' / 'caption.ttf')
    temporary = output.with_name('.' + output.stem + '.partial.mp4')
    if temporary.exists():
        raise FileExistsError(temporary)
    cmd = ['ffmpeg', '-hide_banner', '-n', '-threads', str(config['encoding']['threads']), '-i', str(picture),
           '-i', str(mix), '-map', '0:v:0', '-map', '1:a:0', '-map_metadata', '-1',
           '-vf', 'ass=filename=captions.ass:fontsdir=fonts',
           '-c:v', 'libx264', '-crf', str(config['encoding']['crf']), '-preset', config['encoding']['preset'],
           '-threads', str(config['encoding']['threads']), '-pix_fmt', 'yuv420p',
           '-af', loudness_filter(target, final_measure), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
           '-t', str(duration), '-metadata:s:a:0', 'language=' + config['audio_language_iso639_2'],
           '-movflags', '+faststart', str(temporary)]
    write_json(package / 'render-command.json', dict(argv=cmd, cwd=str(package)))
    print(f'Rendering {duration:.3f}s to {output.name}', flush=True)
    with (package / 'render.log').open('w') as log:
        result = subprocess.run(cmd, cwd=package, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'Render failed; inspect {package / "render.log"}')
    result_probe = probe(temporary)
    v = next(s for s in result_probe['streams'] if s['codec_type'] == 'video')
    audio = [s for s in result_probe['streams'] if s['codec_type'] == 'audio']
    if (int(v['nb_frames']) != int(video['nb_frames']) or v['width'] != video['width']
            or v['height'] != video['height'] or v['avg_frame_rate'] != video['avg_frame_rate']
            or abs(float(v['duration']) - duration) > 0.001 or len(audio) != 1):
        raise ValueError('Output changed the fixed picture timeline or stream contract')
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(temporary), '-map', '0:v:0', '-map', '0:a:0',
         '-f', 'null', '-'], package / 'decode-qc.log')
    output_loudness = measure(['ffmpeg', '-hide_banner', '-i', str(temporary), '-af', loudness_filter(target),
                               '-f', 'null', '-'], package / 'output-measure.log')
    write_json(package / 'output-loudness.json', output_loudness)
    if (abs(float(output_loudness['input_i']) - target['integrated_lufs']) > 1
            or float(output_loudness['input_tp']) > target['true_peak_dbtp'] + 0.5):
        raise ValueError('Encoded output failed loudness/peak QC')
    # Hard-link promotion atomically refuses replacement, including a racing writer.
    output.hardlink_to(temporary)
    temporary.unlink()
    manifest = dict(schema_version='1.0', completed_at=datetime.now(timezone.utc).isoformat(),
                    status='validated_needs_user_review', picture=str(picture), picture_sha256=digest(picture),
                    narration=str(voice), narration_sha256=digest(voice), native_audio=config['native_audio'],
                    tracks=tracks, captions=dict(words=report['word_count'], cues=report['cue_count'],
                    font_sha256=digest(font_path), font_file=str(font_path), style=config['captions']),
                    duration_seconds=duration, frame_count=int(v['nb_frames']), probe=result_probe,
                    output_loudness=output_loudness, output=str(output), output_sha256=digest(output),
                    package=str(package), full_decode='passed', approval=None)
    write_json(output.with_suffix('.postproduction.json'), manifest)
    write_json(package / 'manifest.json', manifest)
    print('Complete:', output, flush=True)
    return manifest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('episode', type=Path)
    ap.add_argument('--config', default='postproduction/edit.json')
    ap.add_argument('--init', action='store_true', help='Create a finishing configuration from a matching picture, voice and CSV')
    ap.add_argument('--picture', help='Episode-relative picture master for --init')
    ap.add_argument('--narration', help='Episode-relative accepted narration for --init')
    ap.add_argument('--words', help='Episode-relative actual word CSV for --init')
    ap.add_argument('--audio-language', default='spa', help='ISO639-2 code for --init')
    ap.add_argument('--check', action='store_true', help='Validate inputs without generating media')
    ap.add_argument('--background', action='store_true', help='Detach a long export and record PID/log for monitoring')
    ap.add_argument('--revision', type=int, help='Otherwise choose next unused final revision')
    args = ap.parse_args()
    root = args.episode.resolve()
    config_path = resolve(root, args.config)
    if args.init:
        if config_path.exists():
            ap.error('Finishing configuration already exists; edit its stable text file')
        if not all((args.picture, args.narration, args.words)):
            ap.error('--init requires --picture, --narration and --words from the same accepted voice')
        picture, narration, words = (resolve(root, p) for p in (args.picture, args.narration, args.words))
        video = next(s for s in probe(picture)['streams'] if s['codec_type'] == 'video')
        config = dict(schema_version='1.0', picture=args.picture, picture_sha256=digest(picture),
                      narration=dict(path=args.narration, sha256=digest(narration), offset_seconds=0),
                      timing=dict(path=args.words, sha256=digest(words), source_voice_sha256=digest(narration)),
                      native_audio=dict(mode='mute'), tracks=[], external_music_allowed=False,
                      captions=default_caption_style(video['width'], video['height']),
                      loudness=dict(integrated_lufs=-16, true_peak_dbtp=-1.5, lra=11),
                      encoding=dict(crf=16, preset='fast', threads=8), audio_language_iso639_2=args.audio_language,
                      output_stem=f"episode-{root.name}-{args.audio_language}-{video['width']}x{video['height']}",
                      review_status='needs_user_review')
        prepare(root, config)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open('x') as f:
            f.write(json.dumps(config, ensure_ascii=False, indent=2) + '\n')
        print('Finishing configuration created:', config_path)
        return
    config = json.loads(config_path.read_text())
    prepare(root, config)
    if args.check:
        print('Post-production inputs validated:', root.name)
        return
    stem = config['output_stem']
    if not re.fullmatch(r'[a-z0-9-]+', stem):
        raise ValueError('Output stem must be lowercase ASCII with hyphens')
    revisions = []
    for path in (root / 'final').glob(stem + '-r*'):
        match = re.search(r'-r(\d{3})(?:\.|$)', path.name)
        if match:
            revisions.append(int(match[1]))
    for path in (root / 'postproduction' / 'exports').glob('r*'):
        if re.fullmatch(r'r\d{3}', path.name):
            revisions.append(int(path.name[1:]))
    rev = args.revision if args.revision is not None else max(revisions, default=0) + 1
    if not 1 <= rev <= 999:
        raise ValueError('Revision must be 1..999')
    output = root / 'final' / f'{stem}-r{rev:03}.mp4'
    output.parent.mkdir(exist_ok=True)
    state_path = root / 'postproduction' / 'run-state.json'
    if args.background:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        log_path = state_path.parent / f'render-r{rev:03}.log'
        with log_path.open('x') as log:
            process = subprocess.Popen([sys.executable, '-u', str(Path(__file__).resolve()), str(root),
                                        '--config', str(config_path), '--revision', str(rev)],
                                       stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=True)
        write_json(state_path, dict(status='running', pid=process.pid, revision=rev,
                                    started_at=datetime.now(timezone.utc).isoformat(),
                                    log=str(log_path), output=str(output)))
        print('Background finishing started:', process.pid, log_path)
        return
    try:
        manifest = render(root, config, output, root / 'postproduction' / 'exports' / f'r{rev:03}')
    except Exception:
        if state_path.exists():
            state = json.loads(state_path.read_text())
            if state.get('revision') == rev:
                state.update(status='failed', next_action='Inspect the render log; retry in a new revision')
                write_json(state_path, state)
        raise
    if state_path.exists():
        state = json.loads(state_path.read_text())
        if state.get('revision') == rev:
            state.update(status=manifest['status'], completed_at=manifest['completed_at'])
            write_json(state_path, state)


if __name__ == '__main__':
    main()
