#!/usr/bin/env python3
"""Prepare and launch the explicitly requested same-seed r006 12→20-step comparison."""
import hashlib,json,subprocess,urllib.request
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EP=ROOT/'episodes/006-shortest-war-ever'
BATCH=EP/'automation/batches/r006-same-seed-20step-r008'
CLI=Path('/home/mhr/AI/comfy-video-automation/.venv/bin/comfy-video')
FAILURES={
2:('0.00–5.00','Warm reference palette becomes blue; hand/foot morphology changes.'),
4:('0.00–2.00','Added foreground haze obscures and changes the intact palace.'),
7:('1.75–5.00','An additional approaching hull overlays the five fixed ships.'),
10:('1.25–4.25','Invented large person at bow chain sinks into open water.'),
12:('2.00–5.00','Officer changes screen side; new close vessel/view replaces original distant fleet.'),
13:('2.30–5.00','Moored reference dhow moves and changes scale/orientation instead of static crop.'),
15:('0.00–5.00','Two new foreground people appear in the single-messenger scene.'),
17:('3.50–5.00','Three dispatches replace the exactly two closed reference dispatches; transition overlay.'),
19:('0.00–3.00','Crowd appears in the empty throne room.'),
22:('0.00–5.00','Unlisted foreground crowd appears in open harbour water.'),
25:('0.00–5.00','Two close foreground people appear in the zero-person fleet scene.'),
31:('2.00–5.00','Giant unsupported foreground hands and morphing scrolls replace the original courier crop.'),
32:('1.00–5.00','Red flare appears before battle; invented close deck crew/view follows.'),
33:('2.30–5.00','Invented white hull drawing appears on the original unmarked hull.'),
34:('0.00–5.00','Extra foreground and background people appear in the empty reference room.'),
35:('0.00–5.00','Unlisted group of people appears beside the empty throne.'),
36:('0.00–5.00','Khalid disappears at opening; changed viewpoint, fingered hand and opened scroll follow.'),
37:('2.00–5.00','An additional guard appears; reference arrangement changes.'),
45:('2.30–5.00','Giant foreground Hamoud is duplicated while original Hamoud remains by the throne.'),
47:('2.30–5.00','Unlisted cloth/head wiping action changes Hamoud turban silhouette and covers face.'),
58:('0.00–5.00','Large fingered hands replace the specified simple mitten hands in unsupported close framing.'),
62:('0.00–5.00','Added close foreground people and ship approach; more invented deck figures follow.'),
63:('2.30–5.00','Close crew and new gun dominate the required hull/funnel crop with deck excluded.'),
67:('1.00–5.00','New foreground residents appear and grow across single-messenger harbour scene.'),
70:('1.00–5.00','Premature blast/smoke in waiting beat followed by invented close cannon crew.'),
72:('0.00–2.00','Unlisted fog obscures Khalid and the clear-air palace scene.'),
73:('0.00–2.00','Additional navy gunner appears beside the existing stationary cannon crew.'),
77:('2.30–5.00','Close deck crew replaces the specified hull/waterline view with deck excluded.'),
78:('1.00–5.00','Premature burning ship and smoke replace the waiting balcony/fleet scene.'),
80:('2.00–5.00','Khalid walks out and disappears despite required unchanged still clock scene.'),
81:('2.30–5.00','Palace dissolves into fog/empty shoreline despite required unchanged intact harbour.'),
82:('2.00–5.00','Khalid obscures the required 09:00 placard; exact text no longer visible throughout.'),
93:('0.00–3.00','Large invented crowd stands and sinks in water around the Glasgow.'),
94:('2.00–5.00','Daylight wreck becomes orange sunset, breaking unchanged light/time continuity.'),
95:('2.00–3.00','Originally still crouched defenders become running close figures, followed by dissolve.'),
97:('2.30–5.00','Originally crouching defenders stand/run with altered pose instead of remaining still.'),
103:('0.00–4.00','Full-frame smoke hides the original doorway characters; dissolving scene replaces reference opening.'),
105:('2.00–5.00','Landscape scene collapses into narrow portrait insert with large black side panels.'),
110:('0.00–5.00','New foreground woman and crate appear while original two civilians remain behind.'),
126:('2.00–5.00','Closed dispatches become an unfolded sheet and oversized fingered hands; prop state changes.'),
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(timezone.utc).isoformat()
def main():
 BATCH.mkdir(parents=True,exist_ok=True)
 if (BATCH/'submission.json').exists():print('Already submitted',json.loads((BATCH/'submission.json').read_text())['id']);return
 if (BATCH/'launch-attempt.json').exists():raise SystemExit('Inspect service state before any resubmission; launch receipt missing.')
 inventory=json.loads((EP/'renders/review-evidence-20step/inventory.json').read_text())['clips'];available={r['number'] for r in inventory};assert set(FAILURES)<=available
 pairs=[];jobs=[]
 for n,(bad_times,reason) in sorted(FAILURES.items()):
  prior=EP/f'automation/retries/review-r006/clip-{n:03d}'
  j=json.loads((prior/f'jobs/clip-{n:03d}.json').read_text());source=EP/f'renders/editorial/clip-{n:03d}-shot-r006.mp4';side=json.loads(source.with_suffix('.run.json').read_text());prompt=ROOT/j['prompt']['file'];assert j['generation']['steps']==12 and side['actual_seed']==j['generation']['seed'];assert side['prompt_text'].startswith(prompt.read_text().strip())
  frozen=BATCH/f'prompts/clip-{n:03d}.md';frozen.parent.mkdir(exist_ok=True)
  if frozen.exists():assert frozen.read_bytes()==prompt.read_bytes()
  else:frozen.write_bytes(prompt.read_bytes())
  assert frozen.read_text().count('NO BACKGROUND MUSIC. Natural diegetic sound effects only.')==1
  prefix=f'clip-{n:03d}-shot-r008';assert not list((EP/'renders').glob(f'*/{prefix}*'))
  old=json.loads(json.dumps(j));j['prompt']['file']=str(frozen.relative_to(ROOT));j['generation']['steps']=20;j['output'].update(prefix=prefix,overwrite=False);j['job_identity']=f'006-shortest-war-ever:clip-{n:03d}:r008:20step-same-r006-seed'
  normalized=json.loads(json.dumps(j));normalized['prompt']=old['prompt'];normalized['output']=old['output'];normalized['job_identity']=old['job_identity'];normalized['generation']['steps']=12;assert normalized==old
  refs=[{'path':r['path'],'sha256':sha(ROOT/r['path'])} for r in j['references']]
  pairs.append(dict(number=n,decision='retry_same_prompt_seed_increase_steps',bad_times=bad_times,reason=reason,baseline=str(source.relative_to(ROOT)),baseline_sha256=sha(source),baseline_steps=12,test_steps=20,seed=side['actual_seed'],baseline_prompt=str(prompt.relative_to(ROOT)),test_prompt=str(frozen.relative_to(ROOT)),prompt_sha256=sha(frozen),effective_prompt_sha256=hashlib.sha256(side['prompt_text'].encode()).hexdigest(),references=refs,output=f'episodes/006-shortest-war-ever/renders/editorial/{prefix}.mp4',review_evidence=f'episodes/006-shortest-war-ever/renders/review-evidence-20step/overview-{next(i for i,r in enumerate(inventory) if r["number"]==n)//8+1:02d}.jpg',baseline_run_metrics_summary=side.get('run_metrics',{}).get('summary'),test_review_status='pending_generation',steps_effect_conclusion=None))
  write(BATCH/f'jobs/clip-{n:03d}.json',j);jobs.append(j)
 settings=dict(continue_on_error=True,stop_on_error=False,max_retries=1,concat_on_complete=False,upscale_on_complete=False);write(BATCH/'settings.json',settings)
 write(BATCH/'comparison.json',dict(scope='Only manually screened failed completed r006 renders. No r004/r005/r007 candidates reviewed or used.',control='Original r006 render at12steps; identical original prompt bytes, seed, references, sampler, scheduler, resolution, audio and all generation options; test changes only steps12→20. Output identity/path are new for immutability.',pairs=pairs,review_method='Rapid actual-frame/reference visual screening at0/1/2/3/4/4.958seconds plus existing dense replacement evidence. Not final all-frame motion/audio approval.',created_at=now()))
 check=subprocess.run([str(CLI),'batch','--folder',str(BATCH/'jobs'),'--settings',str(BATCH/'settings.json'),'--dry-run'],cwd=ROOT,capture_output=True,text=True);(BATCH/'dry-run.json').write_text(check.stdout);(BATCH/'dry-run.stderr').write_text(check.stderr);assert check.returncode==0 and json.loads(check.stdout)['valid'],check.stderr[-1000:]
 manifest=dict(created_at=now(),status='preflight_passed',job_count=len(jobs),steps=20,baseline_steps=12,revision=8,seed_policy='same actual r006 seed',prompt_policy='byte-identical frozen r006 prompt; active/latest prompt edits excluded',authorization='User2026-10-04 explicitly requested quick review only of round006 failures and generation/step experiment at20steps with identical prompts and seeds.',profile_exception='User override20steps applies only to this scoped experiment; episode12step default unchanged.',concat_on_complete=False,upscale_on_complete=False)
 write(BATCH/'manifest.json',manifest);write(BATCH/'launch-attempt.json',dict(at=now(),job_identities=[j['job_identity'] for j in jobs]))
 op=urllib.request.build_opener(urllib.request.ProxyHandler({}));req=urllib.request.Request('http://127.0.0.1:8090/v1/batches',data=json.dumps(dict(jobs=jobs,settings=settings)).encode(),headers={'Content-Type':'application/json'});res=json.load(op.open(req,timeout=300));write(BATCH/'submission.json',res);manifest.update(status=res['status'],batch_id=res['id'],job_ids=res.get('job_ids'),submitted_at=now());write(BATCH/'manifest.json',manifest)
 print(json.dumps({'jobs':len(jobs),'batch_id':res['id'],'status':res['status'],'steps':20,'same_r006_prompt_and_seed':True}))
if __name__=='__main__':main()
