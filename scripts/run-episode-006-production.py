#!/usr/bin/env python3
"""Submit the reviewed Episode 006 12-step production once with the CLI watcher and receipt."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from comfy_video_service.cli import Api, main

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'episodes/006-shortest-war-ever'
BATCH = EP / 'automation/batches/production-12step-r004'


def read(p):
    return json.loads(p.read_text())


def write(p, data):
    temporary = p.with_suffix(p.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(p)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


manifest = read(BATCH / 'manifest.json')
preflight = read(BATCH / 'preflight.json')
assert manifest['batch_id'] is None and manifest['status'] == 'prepared_not_launched'
assert preflight['valid'] and preflight['job_count'] == manifest['job_count'] == 131
assert not (BATCH / 'submission.json').exists()
assert sha(ROOT / manifest['settings']) == manifest['settings_sha256']
assert sha(EP / 'audio/narration-es-google-vids-r001.mp4') == manifest['accepted_voice_sha256']
assert sha(EP / 'timestamps/timing-map.json') == manifest['accepted_timing_sha256']
for record in manifest['jobs']:
    for field in ('job', 'prompt', 'production_job'):
        assert sha(ROOT / record[field]) == record[field + '_sha256']
    for ref in record['references']:
        assert sha(ROOT / ref['path']) == ref['sha256']
    job = read(ROOT / record['job'])
    assert (job['generation']['steps'], job['generation']['lightning'], job['generation']['width'], job['generation']['height']) == (12, False, 1024, 576)
    assert job['generation']['seed'] == record['seed']
    assert job['output']['overwrite'] is False
    for field in ('directory', 'editorial_directory'):
        assert not list((ROOT / job['output'][field]).glob(job['output']['prefix'] + '*'))

# Exclusive marker prevents a second submission even if a response is interrupted.
attempt = BATCH / 'launch-attempt.json'
with attempt.open('x') as stream:
    json.dump({'started_at': datetime.now(timezone.utc).isoformat(), 'watcher_pid': os.getpid(),
               'instruction': 'Do not resubmit after an interruption; inspect persisted service state.'}, stream, indent=2)
    stream.write('\n')

original_request = Api.request


def recording_request(self, method, path, **kwargs):
    result = original_request(self, method, path, **kwargs)
    if method == 'POST' and path == '/v1/batches':
        write(BATCH / 'submission.json', result)
        manifest.update(batch_id=result['id'], status=result['status'],
                        submitted_at=datetime.now(timezone.utc).isoformat(), watcher_pid=os.getpid())
        write(BATCH / 'manifest.json', manifest)
        write(EP / 'automation/run-state.json', {'schema_version': '1.0', 'batch_id': result['id'],
              'purpose': 'full 12-step production', 'status': result['status'],
              'manifest': str((BATCH / 'manifest.json').relative_to(ROOT)),
              'job_ids': [j['id'] for j in result.get('jobs', [])], 'watcher_pid': os.getpid(),
              'next_action': 'Review all 131 twelve-step candidates for picture, motion, exact text and native SFX before assembly.'})
        print('Submission receipt recorded: ' + result['id'], flush=True)
    return result


Api.request = recording_request
main(['batch', '--folder', str(BATCH / 'jobs'), '--settings', str(BATCH / 'settings.json'),
      '--watch', '--poll-interval', '15'])
