#!/usr/bin/env python3
"""Archive live dynamic-Short validation; this command never queues generation."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import urllib.request

REPO = Path(__file__).resolve().parents[1]
POLICY = 'NO BACKGROUND MUSIC. Natural diegetic sound effects only.'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('episode', type=Path)
    parser.add_argument('--service-root', type=Path, required=True)
    parser.add_argument('--api', default='http://127.0.0.1:8090')
    parser.add_argument('--comfy', default='http://127.0.0.1:8188')
    parser.add_argument('--revision', default='r001')
    args = parser.parse_args()
    ep = args.episode.resolve()
    if not ep.is_relative_to(REPO / 'episodes') or not re.fullmatch(r'r\d{3}', args.revision):
        raise ValueError('Episode must be beneath repository episodes')
    target = ep / 'automation/preflight.json'
    if target.exists():
        raise FileExistsError('Preserve the previous preflight and choose a reviewed new revision')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    def request(url, body=None):
        req = urllib.request.Request(url, data=body, headers={'Content-Type':'application/json'})
        return opener.open(req, timeout=120).read()
    plan = json.loads((ep / 'automation/job-plan.json').read_text())
    bindings = [(ep/'timestamps/timing-map.json', plan['timing_sha256']),
                (ep/'plan/clip-direction.json', plan['direction_sha256']),
                (ep/'plan/reference-manifest.json', plan['reference_manifest_sha256'])]
    bindings += [(ep/e['path'], e['sha256']) for e in plan['job_hashes']]
    bindings += [(Path(e['path']), e['sha256']) for e in plan['service_sources']]
    for path, digest in bindings:
        if sha(path) != digest:
            raise ValueError(f'Stale job binding: {path}')
    ready = json.loads(request(args.api + '/v1/ready'))
    queue = json.loads(request(args.comfy + '/queue'))
    if not ready.get('ready') or queue.get('queue_running') or queue.get('queue_pending'):
        raise ValueError('Services unavailable or GPU queue occupied')
    evidence = ep / f'automation/live-validation-{args.revision}'
    evidence.mkdir(exist_ok=False)
    rows = []
    for entry in plan['jobs']:
        job_path = ep / entry['job_path']
        job = json.loads(job_path.read_text())
        if sha(ep/entry['prompt_path']) != entry['prompt_sha256']:
            raise ValueError('Prompt changed after job preparation')
        for ref, digest in zip(job['references'], entry['reference_hashes'], strict=True):
            if sha(REPO/ref['path']) != digest:
                raise ValueError('Reference changed after job preparation')
        raw = request(args.api+'/v1/validate?dump_graph=false', job_path.read_bytes())
        response_path = evidence/(entry['clip_id']+'.json')
        response_path.write_bytes(raw)
        response = json.loads(raw)
        resolved = response.get('resolved_config', {})
        if not response.get('valid') or response.get('errors') or response.get('warnings'):
            raise ValueError(f'Live validation failed: {entry["clip_id"]}')
        if (resolved['frame_count'] != entry['expected_raw_frames'] or resolved['steps'] != 16
                or resolved['lightning'] or (resolved['width'], resolved['height']) != (480,864)
                or resolved['prompt_text'].count(POLICY) != 1 or resolved['seed'] != entry['seed']
                or resolved['reference_paths'] != [str(REPO/r['path']) for r in job['references']]):
            raise ValueError('Live engine configuration disagrees with reviewed job plan')
        rows.append({'clip_id':entry['clip_id'], 'valid':True, 'steps':16,
                     'raw_frames':resolved['frame_count'], 'editorial_frames':entry['editorial_frames'],
                     'response_path':response_path.relative_to(ep).as_posix(), 'sha256':sha(response_path)})
    env = dict(os.environ, NO_PROXY='127.0.0.1,localhost')
    command = ['uv','run','comfy-video','batch','--service-url',args.api,'--folder',str(ep/'automation/jobs'),
               '--settings',str(ep/'automation/batch-settings.json'),'--dry-run']
    result = subprocess.run(command, cwd=args.service_root, env=env, capture_output=True, text=True)
    (evidence/'batch.stdout').write_text(result.stdout)
    (evidence/'batch.stderr').write_text(result.stderr)
    if result.returncode:
        raise RuntimeError('Full batch dry-run failed; inspect archived stdout/stderr')
    gpu = subprocess.run(['nvidia-smi','--query-gpu=name,memory.used,memory.free,utilization.gpu,temperature.gpu',
                          '--format=csv,noheader'],capture_output=True,text=True,check=True).stdout.strip()
    report = {'schema_version':'1.0','created_at':datetime.now(timezone.utc).isoformat(),
              'status':'validated_not_submitted','episode_id':ep.name,'job_plan_sha256':sha(ep/'automation/job-plan.json'),
              'ready':ready,'comfy_queue':queue,'free_disk_bytes':shutil.disk_usage(ep).free,'gpu':gpu,
              'jobs':rows,'dry_run':{'command':command,'exit_code':result.returncode,
              'stdout':str((evidence/'batch.stdout').relative_to(ep)),
              'stderr':str((evidence/'batch.stderr').relative_to(ep))},
              'quality_limit':'Native 16-step pilot and actual motion/audio review still required.'}
    with target.open('x') as stream:
        json.dump(report,stream,ensure_ascii=False,indent=2)
        stream.write('\n')
    print(f'Validated {len(rows)} jobs; archived preflight, no generation submitted.')

if __name__ == '__main__':
    main()
