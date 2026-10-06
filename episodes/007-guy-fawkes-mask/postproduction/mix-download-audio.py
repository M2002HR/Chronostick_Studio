#!/usr/bin/env python3
"""Episode-specific audio overlay; reuse the local finishing helpers."""
import argparse
import importlib.util
import json
import shutil
import subprocess
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
spec = importlib.util.spec_from_file_location('postproduction', REPO / 'scripts/postproduce-episode.py')
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)


def video_hash(path):
    result = subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
        '-c:v', 'copy', '-f', 'hash', '-hash', 'sha256', '-'
    ], text=True)
    return result.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default='postproduction/audio-overlay.json')
    args = parser.parse_args()
    config = json.loads(pp.resolve(ROOT, args.config).read_text())
    picture = ROOT / config['picture']
    source = ROOT / config['source_audio']['path']
    for path, expected in [(picture, config['picture_sha256']),
                           (source, config['source_audio']['sha256'])]:
        if pp.digest(path) != expected:
            raise ValueError(f'Input hash changed: {path}')
    if config['native_audio'] != {'mode': 'preserve', 'gain_db': 0}:
        raise ValueError('This requested overlay preserves native audio at unity gain')
    original = pp.probe(picture)
    video = next(s for s in original['streams'] if s['codec_type'] == 'video')
    duration = float(video['duration'])
    source_stream = next(s for s in pp.probe(source)['streams'] if s['codec_type'] == 'audio')
    if float(source_stream['duration']) > duration:
        raise ValueError('Supplied audio would be truncated')
    captioned = config.get('captions', {}).get('enabled', False)
    words = font = None
    caption_inputs = []
    if captioned:
        timing = config['timing']
        timing_path = ROOT / timing['path']
        timing_voice = ROOT / timing['source_voice_path']
        ingestion_path = ROOT / timing['ingestion_provenance']
        caption_inputs = [(timing_path, timing['sha256']),
                          (timing_voice, timing['source_voice_sha256']),
                          (ingestion_path, timing['ingestion_provenance_sha256'])]
        for path, expected in caption_inputs:
            if pp.digest(path) != expected:
                raise ValueError(f'Caption input hash changed: {path}')
        ingestion = json.loads(ingestion_path.read_text())
        if (ingestion['incoming_sha256'] != config['source_audio']['sha256'] or
                ingestion['artifacts']['wav']['sha256'] != timing['source_voice_sha256']):
            raise ValueError('Caption timing voice is not derived from the supplied export')
        words = pp.load_words(timing_path, boundary_repairs=timing.get('start_boundary_repairs', []))
        if words[-1]['end'] > float(source_stream['duration']) + 0.02:
            raise ValueError('Captions exceed actual supplied voice')
        font = pp.resolve(ROOT, config['captions']['font_file'])
        family, face = pp.ImageFont.truetype(str(font), config['captions']['font_size']).getname()
        if family != config['captions']['font_family'] or 'bold' not in face.lower():
            raise ValueError('Exact configured bold font is required')
    revision = 1
    while True:
        output = ROOT / 'final' / f"{config['output_stem']}-r{revision:03}.mp4"
        package = ROOT / 'postproduction/exports' / f'audio-overlay-r{revision:03}'
        if not (output.exists() or package.exists() or output.with_suffix('.postproduction.json').exists()):
            break
        revision += 1
    package.mkdir(parents=True)
    pp.write_json(package / 'edit-snapshot.json', config)
    caption_report = None
    if captioned:
        caption_report = pp.write_captions(package, words, config['captions'], font,
                                          video['width'], video['height'],
                                          float(Fraction(video['avg_frame_rate'])))
        highlighted = {e['active_word_index'] for e in caption_report['events']
                       if e['active_word_index'] is not None}
        if len(highlighted) != len(words):
            raise ValueError('Some words have no visible highlight interval')
        (package / 'fonts').mkdir()
        shutil.copyfile(font, package / 'fonts/caption.ttf')
    # Source audio starts at zero and is silence-padded only after its endpoint.
    # Native audio remains unity; only the supplied voice has explicit headroom.
    # No normalization, ducking or time stretch affects the original soundtrack.
    graph = pp.mix_graph([dict(duration_seconds=duration, start_seconds=0, gain_db=0)], duration)
    graph = graph.replace('[0:a]apad', f"[0:a]volume={config['source_audio']['gain_db']}dB,apad", 1)
    target = dict(integrated_lufs=-16, true_peak_dbtp=-1.5, lra=11)
    measurement = pp.measure([
        'ffmpeg', '-hide_banner', '-i', str(source), '-i', str(picture),
        '-filter_complex', graph + ';[mix]' + pp.loudness_filter(target) + '[measured]',
        '-map', '[measured]', '-f', 'null', '-'
    ], package / 'mix-measure.log')
    pp.write_json(package / 'mix-loudness.json', measurement)
    if float(measurement['input_tp']) > 0:
        raise ValueError('Unity-gain mix would clip; review source levels before encoding')
    temporary = output.with_name('.' + output.stem + '.partial.mp4')
    command = [
        'ffmpeg', '-hide_banner', '-n', '-i', str(source), '-i', str(picture),
        '-filter_complex', graph, '-map', '1:v:0', '-map', '[mix]',
    ]
    if captioned:
        command += ['-vf', 'ass=filename=captions.ass:fontsdir=fonts',
                    '-c:v', 'libx264', '-crf', str(config['encoding']['crf']),
                    '-preset', config['encoding']['preset'],
                    '-threads', str(config['encoding']['threads']), '-pix_fmt', 'yuv420p']
    else:
        command += ['-c:v', 'copy']
    command += [
        '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
        '-t', str(duration), '-metadata:s:a:0', 'language=spa',
        '-movflags', '+faststart', str(temporary)
    ]
    pp.write_json(package / 'render-command.json', dict(argv=command, cwd=str(package)))
    with (package / 'render.log').open('w') as log:
        subprocess.run(command, cwd=package, stdout=log, stderr=subprocess.STDOUT, check=True)
    result = pp.probe(temporary)
    out_video = next(s for s in result['streams'] if s['codec_type'] == 'video')
    for key in ('nb_frames', 'width', 'height', 'avg_frame_rate', 'duration'):
        if out_video[key] != video[key]:
            raise ValueError(f'Picture timeline changed: {key}')
    if len(result['streams']) != 2:
        raise ValueError('Expected exactly picture and mixed audio')
    source_video_hash = video_hash(picture)
    if not captioned and video_hash(temporary) != source_video_hash:
        raise ValueError('Encoded picture changed')
    pp.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(temporary),
            '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'], package / 'decode-qc.log')
    loudness = pp.measure(['ffmpeg', '-hide_banner', '-i', str(temporary),
                          '-af', pp.loudness_filter(target), '-f', 'null', '-'],
                         package / 'output-measure.log')
    if float(loudness['input_tp']) > 0:
        raise ValueError('Encoded audio exceeds 0 dBTP')
    for path, expected in [(picture, config['picture_sha256']),
                           (source, config['source_audio']['sha256']), *caption_inputs]:
        if pp.digest(path) != expected:
            raise ValueError(f'Input changed during finishing: {path}')
    output.hardlink_to(temporary)
    temporary.unlink()
    manifest = dict(
        schema_version='1.0', completed_at=datetime.now(timezone.utc).isoformat(),
        status='validated_needs_user_review', approval=None, config=config,
        picture=str(picture), picture_sha256=pp.digest(picture),
        source_audio=str(source), source_audio_sha256=pp.digest(source),
        native_audio=config['native_audio'],
        captions=dict(config['captions'], words=caption_report['word_count'],
                      cues=caption_report['cue_count'], font_sha256=pp.digest(font))
                 if captioned else {'enabled': False},
        timing=config['timing'],
        source_video_bitstream_sha256=source_video_hash, video_bitstream_unchanged=not captioned,
        picture_processing='caption burn-in only' if captioned else 'stream copy',
        frame_count=int(video['nb_frames']), duration_seconds=duration,
        full_decode='passed', output_loudness=loudness, probe=result,
        output=str(output), output_sha256=pp.digest(output), package=str(package)
    )
    pp.write_json(package / 'manifest.json', manifest)
    pp.write_json(output.with_suffix('.postproduction.json'), manifest)
    print('Complete:', output)


if __name__ == '__main__':
    main()
