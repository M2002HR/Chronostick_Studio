#!/usr/bin/env python3
"""Observe the submitted batch, archive real media review evidence; never approve."""
import json,subprocess,time,urllib.request
from pathlib import Path
ROOT=Path('/home/mhr/Code/chronostick-studio');EP=ROOT/'episodes/008-pinocchio-ww2';BATCH='1b9e7f46-1554-4339-a91f-949e5e570baf';op=urllib.request.build_opener(urllib.request.ProxyHandler({}));done=set()
while True:
 raw=op.open('http://127.0.0.1:8090/v1/batches/'+BATCH,timeout=30).read();d=json.loads(raw)
 print(d['status'],[(j['request']['job_identity'],j['status'],j.get('progress_percent')) for j in d['jobs']],flush=True)
 for job in d['jobs']:
  identity=job['request']['job_identity'];clip=identity.split('episode-008-')[1][:7]
  if job['status']!='succeeded' or clip in done:continue
  done.add(clip);media=EP/'renders/editorial'/f'{identity}.mp4';evidence=EP/'renders/review-evidence'/f'{clip}-r001';machine=EP/'renders/machine-review'/f'{clip}-r001'
  commands=[]
  if not evidence.exists():commands.append(['python3','scripts/prepare-short-review.py',str(EP),'--clip',clip,'--media',str(media),'--revision','r001'])
  if not machine.exists():commands.append(['python3','scripts/ajil-review-reference.py','--video',str(media),'--transcript',str(EP/'script/narration-es.md'),'--output-dir',str(machine),'--revision','r001','--base-url','http://127.0.0.1:8082','--env-file','.env','--instructions',str(EP/'renders/machine-review-instructions.txt'),'--media-only'])
  for i,cmd in enumerate(commands):
   log=EP/'automation/runtime'/f'{clip}-review-command-{i}-r001.log'
   with log.open('x') as stream:result=subprocess.run(cmd,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
   print('prepared',clip,'command',i,'exit',result.returncode,flush=True)
 if d['status'] in ('succeeded','failed','cancelled'):
  p=EP/'automation/batches/native-16step-remaining-r001/terminal-response-r001.json'
  if not p.exists():p.write_bytes(raw)
  print('TERMINAL',d['status'],flush=True);break
 time.sleep(30)
