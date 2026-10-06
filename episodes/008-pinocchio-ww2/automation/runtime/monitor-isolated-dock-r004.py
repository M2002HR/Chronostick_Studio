import json,subprocess,time,urllib.request
from pathlib import Path
ROOT=Path('/home/mhr/Code/chronostick-studio');EP=ROOT/'episodes/008-pinocchio-ww2';op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
while True:
 raw=op.open('http://127.0.0.1:8090/v1/batches/89060dd7-85b6-4791-8248-2e1b1c60c516',timeout=30).read();d=json.loads(raw)
 print(d['status'],[(j['stage'],j['progress_percent']) for j in d['jobs']],flush=True)
 if d['status'] in ('succeeded','failed','cancelled'):break
 time.sleep(20)
(EP/'automation/retries/isolated-dock-r004/terminal-response-r004.json').write_bytes(raw)
if d['status']!='succeeded':raise RuntimeError(d['status'])
media=EP/'renders/editorial/episode-008-clip-02-isolated-dock-r004.mp4'
cmd=['python3','scripts/prepare-short-review.py',str(EP),'--clip','clip-02','--media',str(media),'--revision','r004']
with (EP/'automation/runtime/repair-frame-evidence-r004.log').open('x') as f:subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
for label,target,mime,ins in [('picture',media,'video/mp4','machine-review-instructions.txt'),('native-audio-only',EP/'renders/review-evidence/clip-02-r004/actual-audio.wav','audio/wav','audio-only-review-instructions.txt')]:
 cmd=['python3','scripts/ajil-review-reference.py','--video',str(target),'--transcript',str(EP/'script/narration-es.md'),'--output-dir',str(EP/'renders/machine-review'/('clip-02-'+label+'-r004')),'--revision','r004','--base-url','http://127.0.0.1:8082','--env-file','.env','--instructions',str(EP/'renders'/ins),'--media-only','--media-mime',mime]
 with (EP/'automation/runtime'/('repair-'+label+'-r004.log')).open('x') as f:subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True)
print('actual repair evidence and machine supplements archived',flush=True)
