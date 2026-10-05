#!/usr/bin/env python3
"""Audit actual H3 request/graph, decoded frames and editorial timing; never approve cuts."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess

REPO = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def presentation_errors(stream, frames, expected, fps):
    errors = []
    if len(frames) != expected:
        errors.append(f"decoded {len(frames)} frames, expected {expected}")
    if Fraction(stream['avg_frame_rate']) != fps:
        errors.append('wrong average frame rate')
    tick = Fraction(stream['time_base'])
    for i, frame in enumerate(frames):
        pts = int(frame['best_effort_timestamp']) * tick
        if abs(pts - Fraction(i, fps)) > tick:
            errors.append(f'frame {i}: non-CFR or shifted presentation time {float(pts):.9f}')
            break
    # MP4/AAC muxing may round the final packet endpoint to milliseconds.
    # The frame count and every PTS above remain the timing authority.
    if abs(float(stream['duration']) - expected / fps) > 0.001:
        errors.append('video endpoint differs from frame-derived duration by over 1 ms')
    return errors


def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_streams',
        '-show_frames', '-show_entries',
        'stream=width,height,avg_frame_rate,time_base,duration,nb_frames:'
        'frame=best_effort_timestamp', '-of', 'json', str(path)]))


def small_frames(path):
    return subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
        '-vf', 'scale=120:216', '-vsync', '0', '-pix_fmt', 'gray',
        '-f', 'rawvideo', '-'])


def audit(ep, revision, job_plan=None):
    timing_path = ep / 'timestamps/timing-map.json'
    plan_path = job_plan or ep / 'automation/job-plan.json'
    timing = json.loads(timing_path.read_text())
    plan = json.loads(plan_path.read_text())
    slots = {c['id']: c for c in timing['clips']}
    fps = timing['fps']
    rows = []
    for entry in plan['jobs']:
        slot = slots[entry['clip_id']]
        job_path = ep / entry['job_path']
        job = json.loads(job_path.read_text())
        output = job['output']
        raw = REPO / output['directory'] / (output['prefix'] + '.mp4')
        editorial = REPO / output['editorial_directory'] / (output['prefix'] + '.mp4')
        row = {'clip_id': slot['id'], 'job_identity': job['job_identity'],
               'json_request_seconds': job['generation']['duration_seconds'],
               'expected_raw_frames': slot['expected_raw_frame_count'],
               'expected_editorial_frames': slot['frame_count'],
               'editorial_seconds': slot['frame_count'] / fps,
               'global_start_frame': slot['start_frame'], 'global_end_frame': slot['end_frame'],
               'planned_tail_trim_frames': slot['trim_raw_tail_frames'],
               'job_sha256': sha(job_path), 'errors': []}
        rows.append(row)
        run_path = raw.with_suffix('.run.json')
        if not all(p.exists() for p in (raw, editorial, run_path, editorial.with_suffix('.run.json'))):
            row['status'] = 'pending_media'
            continue
        run = json.loads(run_path.read_text())
        row['run_sha256'] = sha(run_path)
        actual = run['original_request']
        for key in ['duration_seconds', 'fps', 'steps', 'seed']:
            if actual['generation'][key] != job['generation'][key]:
                row['errors'].append(f'executed request differs from job JSON: {key}')
        if actual['output']['editorial_duration_seconds'] != slot['duration_seconds']:
            row['errors'].append('executed editorial duration differs from timing map')
        if job['generation']['duration_seconds'] != slot['generation_request_seconds']:
            row['errors'].append('job request differs from approved timing map')
        nodes = list(run['compiled_graph'].values())
        h3 = next(n['inputs'] for n in nodes if n['class_type'] == 'MiniMaxH3ReferenceToVideo')
        scheduler = next(n['inputs'] for n in nodes if n['class_type'] == 'BasicScheduler')
        create = next(n['inputs'] for n in nodes if n['class_type'] == 'CreateVideo')
        noise = next(n['inputs'] for n in nodes if n['class_type'] == 'RandomNoise')
        row['executed_graph'] = {'frames': h3['length'], 'steps': scheduler['steps'], 'fps': create['fps']}
        if h3['length'] != slot['expected_raw_frame_count']:
            row['errors'].append('compiled H3 frame count differs from approved raw grid')
        if scheduler['steps'] != job['generation']['steps'] or create['fps'] != fps:
            row['errors'].append('compiled scheduler steps/fps differ from job JSON')
        if noise['noise_seed'] != job['generation']['seed'] or run['actual_seed'] != job['generation']['seed']:
            row['errors'].append('executed seed differs from job JSON')
        for label, path, expected in [('raw', raw, slot['expected_raw_frame_count']),
                                      ('editorial', editorial, slot['frame_count'])]:
            data = probe(path)
            stream = data['streams'][0]
            problems = presentation_errors(stream, data['frames'], expected, fps)
            if (stream['width'], stream['height']) != (job['generation']['width'], job['generation']['height']):
                problems.append('resolution differs from job JSON')
            row['errors'].extend(f'{label}: {x}' for x in problems)
            row[label] = {'path': str(path.relative_to(ep)), 'sha256': sha(path),
                          'decoded_frames': len(data['frames']), 'video_stream_seconds': float(stream['duration']),
                          'frame_derived_seconds': len(data['frames']) / fps,
                          'endpoint_rounding_seconds': float(stream['duration']) - len(data['frames']) / fps,
                          'pts_checked_for_every_frame': True}
        # Editorial normalization re-encodes video: hashes cannot prove a byte-copy.
        # Check that every retained decoded frame corresponds to its raw prefix.
        a, b = small_frames(raw), small_frames(editorial)
        size = 120 * 216
        maes = [sum(abs(x-y) for x,y in zip(a[i:i+size], b[i:i+size])) / size
                for i in range(0, min(len(a), len(b)), size)]
        row['raw_prefix_correspondence'] = {'method': 'same-index 120x216 grayscale decoded-frame MAE (lossy re-encode)',
                                           'compared_frames': len(maes), 'max_mae_255': max(maes),
                                           'mean_mae_255': sum(maes) / len(maes),
                                           'bit_exact_claim': False}
        if len(maes) != slot['frame_count'] or max(maes) > 5:
            row['errors'].append('raw/editorial prefix correspondence needs inspection')
        row['actual_tail_trim_frames'] = row['raw']['decoded_frames'] - row['editorial']['decoded_frames']
        if row['actual_tail_trim_frames'] != slot['trim_raw_tail_frames']:
            row['errors'].append('incorrect raw-tail trim')
        row['status'] = 'failed' if row['errors'] else 'technical_timing_pass'
    covered_frames = sum(r['expected_editorial_frames'] for r in rows)
    result = {'created_at': datetime.now(timezone.utc).isoformat(), 'timing_sha256': sha(timing_path),
              'job_plan_path': str(plan_path), 'job_plan_sha256': sha(plan_path), 'fps': fps,
              'expected_episode_frames': timing['picture_frame_count'],
              'expected_total_frames': covered_frames, 'expected_total_seconds': covered_frames / fps, 'clips': rows,
              'complete': all(r['status'] != 'pending_media' for r in rows),
              'status': 'failed' if any(r['errors'] for r in rows) else
                        ('technical_timing_pass' if all(r['status'] == 'technical_timing_pass' for r in rows) else 'pending_remaining_media'),
              'limitations': 'A technical duration pass does not approve actual shot timing, story, audio or tail stability. Review actual cuts and voice sync separately.'}
    out = ep / 'renders' / f'timing-audit-{revision}.json'
    with out.open('x') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    for row in rows:
        print(row['clip_id'], row['status'], 'request', row['json_request_seconds'],
              'editorial', row['editorial_seconds'], row['errors'])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('episode', type=Path)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--job-plan', type=Path, help='Reviewed current job map, including individually selected repair revisions')
    args = parser.parse_args()
    if not __import__('re').fullmatch(r'r\d{3}', args.revision):
        parser.error('Use an unused rNNN audit revision')
    result = audit(args.episode.resolve(), args.revision, args.job_plan.resolve() if args.job_plan else None)
    raise SystemExit(1 if result['status'] == 'failed' else 0)


if __name__ == '__main__':
    main()
