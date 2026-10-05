#!/usr/bin/env python3
"""Freeze, preflight and submit one reviewed repair as a persistent mini-batch."""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EP=ROOT/'episodes/006-shortest-war-ever'
QUEUE=EP/'automation/retries/review-r006'
CLI=Path('/home/mhr/AI/comfy-video-automation/.venv/bin/comfy-video')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def write(p,d):
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');tmp.replace(p)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('number',type=int);ap.add_argument('--reason',required=True)
    ap.add_argument('--evidence',required=True);ap.add_argument('--decision',default='revise_prompt',choices=['retry','revise_prompt'])
    ap.add_argument('--revision',type=int,default=6)
    args=ap.parse_args()
    evidence=Path(args.evidence)
    if not evidence.is_absolute() and not (ROOT/evidence).is_file():
        evidence=EP/evidence
    if not evidence.is_absolute():
        evidence=ROOT/evidence
    assert evidence.is_file(),f'Missing actual review evidence: {evidence}'
    rows=json.loads((EP/'renders/review-evidence-r006/baseline.json').read_text())['clips']
    baseline=next(r for r in rows if r['number']==args.number)
    global QUEUE
    QUEUE=EP/f'automation/retries/review-r{args.revision:03d}'
    if args.revision>6:
        candidates=sorted((EP/'renders/editorial').glob(f'clip-{args.number:03d}-shot-r*.mp4'))
        latest=candidates[-1]
        baseline=dict(baseline,path=str(latest.relative_to(ROOT)),sha256=sha(latest),revision=int(latest.stem[-3:]))
        prior=EP/f"automation/retries/review-r{baseline['revision']:03d}/clip-{args.number:03d}/jobs/clip-{args.number:03d}.json"
        if prior.exists():
            baseline['request']=json.loads(prior.read_text())
    assert sha(ROOT/baseline['path'])==baseline['sha256']
    folder=QUEUE/f'clip-{args.number:03d}'
    folder.mkdir(parents=True,exist_ok=True)
    receipt=folder/'submission.json'
    if receipt.exists():
        print('Already submitted: '+json.loads(receipt.read_text())['id']);return
    if (folder/'launch-attempt.json').exists():
        raise SystemExit('Uncertain submission: inspect service state; never resubmit blindly')
    j=json.loads(json.dumps(baseline['request']))
    assert j is not None
    rev=max(args.revision,baseline['revision']+1)
    prefix=f'clip-{args.number:03d}-shot-r{rev:03d}'
    for field in ['directory','editorial_directory']:
        assert not list((ROOT/j['output'][field]).glob(prefix+'*'))
    prompt=EP/f'prompts/clip-{args.number:03d}.md'
    frozen=folder/'prompts'/prompt.name;frozen.parent.mkdir(exist_ok=True)
    text=prompt.read_text()
    assert text.count('NO BACKGROUND MUSIC. Natural diegetic sound effects only.')==1
    assert text.count('<Picture 1>')==1 and len(j['references'])<=2
    if frozen.exists():assert frozen.read_text()==text
    else:frozen.write_text(text)
    j['prompt']={'file':str(frozen.relative_to(ROOT))}
    seed=int.from_bytes(hashlib.sha256(f"006:review:r{rev}:{args.number}".encode()).digest()[:8],'big')&((1<<63)-1)
    j['generation'].update(seed=seed,seed_mode='fixed',steps=12,lightning=False)
    assert (j['generation']['width'],j['generation']['height'],j['generation']['fps'])==(1024,576,24)
    j['output'].update(prefix=prefix,overwrite=False)
    j['job_identity']=f'006-shortest-war-ever:clip-{args.number:03d}:r{rev:03d}'
    jobs=folder/'jobs';jobs.mkdir(exist_ok=True)
    write(jobs/f'clip-{args.number:03d}.json',j)
    settings=folder/'settings.json'
    write(settings,dict(continue_on_error=True,stop_on_error=False,max_retries=1,concat_on_complete=False,upscale_on_complete=False))
    check=subprocess.run([str(CLI),'batch','--folder',str(jobs),'--settings',str(settings),'--dry-run'],cwd=ROOT,capture_output=True,text=True)
    (folder/'dry-run.json').write_text(check.stdout)
    (folder/'dry-run.stderr').write_text(check.stderr)
    assert check.returncode==0 and json.loads(check.stdout)['valid'],check.stderr[-1000:]
    record=dict(number=args.number,decision=args.decision,reason=args.reason,evidence=str(evidence.relative_to(ROOT)),
                baseline=baseline['path'],baseline_sha256=baseline['sha256'],reviewed_at=now(),
                reviewer='Codex visual review; automated audio evidence tracked separately',
                seed=seed,previous_seed=baseline['request']['generation']['seed'],revision=rev,
                prompt=str(frozen.relative_to(ROOT)),prompt_sha256=sha(frozen),job=j['job_identity'],
                references=[dict(path=r['path'],sha256=sha(ROOT/r['path'])) for r in j['references']],
                status='preflight_passed',authorization='User explicitly requested reviewing all latest clips, fixing failed prompts and regenerating incrementally while review continues.')
    write(folder/'manifest.json',record)
    write(folder/'launch-attempt.json',dict(at=now(),job_identity=j['job_identity'],instruction='Inspect persisted service state if receipt is missing; do not blindly resubmit.'))
    # Submit as a fully preflighted single-child batch; service provides the shared GPU queue.
    import urllib.request
    op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    req=urllib.request.Request('http://127.0.0.1:8090/v1/batches',data=json.dumps(dict(jobs=[j],settings=json.loads(settings.read_text()))).encode(),headers={'Content-Type':'application/json'})
    response=json.load(op.open(req,timeout=300))
    write(receipt,response)
    record.update(status=response['status'],batch_id=response['id'],job_ids=response.get('job_ids'),submitted_at=now())
    write(folder/'manifest.json',record)
    # One shared detached monitor tracks all revisions; submitted GPU work is
    # persisted in the service independently of any progress display.
    import os
    monitor_dir=EP/'automation/retries/review-r006'
    monitor_dir.mkdir(parents=True,exist_ok=True)
    pidfile=monitor_dir/'monitor-process.json'
    alive=False
    if pidfile.exists():
        try:
            pid=json.loads(pidfile.read_text())['pid']
            os.kill(pid,0)
            alive='monitor-episode-006-repairs.py' in Path(f'/proc/{pid}/cmdline').read_text()
        except (OSError,ValueError,KeyError):
            pass
    if not alive:
        log=(monitor_dir/'monitor.log').open('a')
        proc=subprocess.Popen(['python',str(ROOT/'scripts/monitor-episode-006-repairs.py'),'--watch'],cwd=ROOT,stdout=log,stderr=log,start_new_session=True)
        write(pidfile,dict(pid=proc.pid,command='python scripts/monitor-episode-006-repairs.py --watch',scope='all review revisions; evidence only, never automatic approval'))
    print(json.dumps(dict(number=args.number,batch_id=response['id'],status=response['status'],revision=rev)))

if __name__=='__main__':main()
