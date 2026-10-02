#!/usr/bin/env python3
"""Submit the frozen map-redirection batch once; persist progress until terminal state."""
import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from comfy_video_service.cli import Api, main

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'episodes/006-shortest-war-ever'
BATCH = EP / 'automation/batches/map-redirection-12step-r005'

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def now(): return datetime.now(timezone.utc).isoformat()
def write(p, d):
    tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');tmp.replace(p)

manifest=read(BATCH/'manifest.json');preflight=read(BATCH/'preflight.json')
assert manifest['batch_id'] is None and manifest['status']=='prepared_not_launched'
assert preflight['valid'] and preflight['live_dry_run_passed'] and preflight['job_count']==manifest['job_count']==117
assert len(manifest['timeline_coverage'])==131 and preflight['output_collision_count']==0
assert sha(BATCH/'live-dry-run.json')==preflight['dry_run_sha256']
assert not (BATCH/'submission.json').exists()
assert sha(ROOT/manifest['settings'])==manifest['settings_sha256']
assert sha(EP/'audio/narration-es-google-vids-r001.mp4')==manifest['accepted_voice_sha256']
assert sha(EP/'timestamps/timing-map.json')==manifest['accepted_timing_sha256']
for c in manifest['timeline_coverage']:
    if c['method']=='controlled_geography': assert sha(ROOT/c['artifact'])==c['sha256']
    if c['status']=='retained_candidate_unreviewed':
        for a in c['artifacts']:assert sha(ROOT/a['path'])==a['sha256']
for r in manifest['jobs']:
    for field in ('job','prompt','production_job'):assert sha(ROOT/r[field])==r[field+'_sha256']
    for a in r['references']:assert sha(ROOT/a['path'])==a['sha256'] and '/map-' not in a['path']
    j=read(ROOT/r['job']);g=j['generation']
    assert (g['steps'],g['lightning'],g['width'],g['height'],g['fps'])==(12,False,1024,576,24)
    assert g['seed']==r['seed'] and j['output']['overwrite'] is False
    for field in ('directory','editorial_directory'):assert not list((ROOT/j['output'][field]).glob(j['output']['prefix']+'*'))

api=Api('http://127.0.0.1:8090',None)
assert api.request('GET','/v1/ready')['ready']
# Direct engine check avoids environment proxies; do not submit into an unrelated queue.
import urllib.request
op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
queue=json.load(op.open('http://127.0.0.1:8188/queue'))
assert not queue['queue_running'] and not queue['queue_pending']
with (BATCH/'launch-attempt.json').open('x') as f:
    json.dump(dict(started_at=now(),watcher_pid=os.getpid(),instruction='Do not resubmit after a connection interruption; inspect persistent service state.'),f,indent=2);f.write('\n')

original_request=Api.request
def recording_request(self,method,path,**kwargs):
    result=original_request(self,method,path,**kwargs)
    if method=='POST' and path=='/v1/batches':
        write(BATCH/'submission.json',result)
        manifest.update(batch_id=result['id'],status=result['status'],submitted_at=now(),watcher_pid=os.getpid())
        write(BATCH/'manifest.json',manifest)
        runtime=dict(schema_version='1.0',batch_id=result['id'],purpose='remaining117 twelve-step H3 candidates after map redirection',status=result['status'],manifest=str((BATCH/'manifest.json').relative_to(ROOT)),job_ids=[j['id'] for j in result['jobs']],watcher_pid=os.getpid(),retained_unreviewed_candidates=12,controlled_maps_ready=2,next_action='Let the complete batch run; then review actual candidates before selection or assembly.')
        write(EP/'automation/run-state.json',runtime)
        print('Submission receipt recorded: '+result['id'],flush=True)
    elif method=='GET' and manifest.get('batch_id') and path=='/v1/batches/'+manifest['batch_id']:
        counts=dict(Counter(j['status'] for j in result.get('jobs',[])))
        progress=dict(batch_id=result['id'],status=result['status'],checked_at=now(),child_status_counts=counts,job_count=117,retained_unreviewed_candidates=12,controlled_maps_ready=2)
        write(BATCH/'progress.json',progress)
        manifest.update(status=result['status'],last_progress_at=progress['checked_at'],child_status_counts=counts)
        write(BATCH/'manifest.json',manifest)
        runtime=read(EP/'automation/run-state.json');runtime.update(status=result['status'],child_status_counts=counts,last_progress_at=progress['checked_at']);write(EP/'automation/run-state.json',runtime)
        if result['status'] in {'succeeded','failed','cancelled'}:
            write(BATCH/'terminal-state.json',result)
            for path in [EP/'episode.json',EP/'pipeline-state.json']:
                d=read(path);d['production_batch'].update(status=result['status'],finished_at=now(),child_status_counts=counts);write(path,d)
            print('Generation terminal state recorded; actual picture and audio review still required.',flush=True)
    return result

Api.request=recording_request
main(['batch','--folder',str(BATCH/'jobs'),'--settings',str(BATCH/'settings.json'),'--watch','--poll-interval','15'])
