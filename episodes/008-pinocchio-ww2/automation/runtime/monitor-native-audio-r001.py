#!/usr/bin/env python3
"""Blind audio-only supplementary review; no approval or new generation."""
import json,subprocess,time,urllib.request
from pathlib import Path
ROOT=Path('/home/mhr/Code/chronostick-studio');EP=ROOT/'episodes/008-pinocchio-ww2';BATCH='1b9e7f46-1554-4339-a91f-949e5e570baf';op=urllib.request.build_opener(urllib.request.ProxyHandler({}));done=set()
while True:
 d=json.loads(op.open('http://127.0.0.1:8090/v1/batches/'+BATCH,timeout=30).read())
 for j in d['jobs']:
  clip=j['request']['job_identity'].split('episode-008-')[1][:7];audio=EP/'renders/review-evidence'/f'{clip}-r001'/'actual-audio.wav';out=EP/'renders/machine-review'/f'{clip}-native-audio-only-r001'
  if j['status']!='succeeded' or clip in done or not audio.exists():continue
  done.add(clip)
  if out.exists():continue
  cmd=['python3','scripts/ajil-review-reference.py','--video',str(audio),'--transcript',str(EP/'script/narration-es.md'),'--output-dir',str(out),'--revision','r001','--base-url','http://127.0.0.1:8082','--env-file','.env','--instructions',str(EP/'renders/audio-only-review-instructions.txt'),'--media-only','--media-mime','audio/wav']
  with (EP/'automation/runtime'/f'{clip}-native-audio-only-r001.log').open('x') as log:r=subprocess.run(cmd,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
  print('audio-only review',clip,'exit',r.returncode,flush=True)
 if d['status'] in ('succeeded','failed','cancelled') and all(j['status']!='succeeded' or j['request']['job_identity'].split('episode-008-')[1][:7] in done for j in d['jobs']):break
 time.sleep(30)
