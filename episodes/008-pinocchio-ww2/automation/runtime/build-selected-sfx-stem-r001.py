import json,hashlib,subprocess,datetime
from pathlib import Path
import numpy as np
EP=Path('/home/mhr/Code/chronostick-studio/episodes/008-pinocchio-ww2');manifest=json.loads((EP/'renders/selection-manifest.json').read_text());clips=sorted(manifest['clips'],key=lambda c:c['clip_id'])
assert [c['clip_id'] for c in clips]==[f'clip-{i:02d}' for i in range(1,7)]
assert sum(c['frames'] for c in clips)==773
parts=[];rows=[];offset=0
for c in clips:
 id=c['clip_id'];plan=EP/'plan/sfx'/f'{id}-clean-plan-r001.json'
 if plan.exists():source=EP/json.loads(plan.read_text())['stem'];gain=0;kind='lossless independent recorded fallback stem'
 elif id=='clip-01':source=EP/'audio/sfx/clip-01-silent-stem-r001.wav';gain=0;kind='explicit lossless silence'
 else:source=EP/c['source'];gain=c.get('finishing_gain_db',0);kind='reviewed native isolated physical sound'
 samples=c['frames']*2000
 cmd=['ffmpeg','-v','error','-i',str(source),'-vn','-af',f'asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={gain}dB,apad,atrim=end_sample={samples}','-ar','48000','-ac','2','-f','f32le','-']
 b=subprocess.check_output(cmd);x=np.frombuffer(b,np.float32).reshape(-1,2);assert len(x)==samples;parts.append(x)
 rows.append(dict(clip_id=id,source=str(source.relative_to(EP)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),selected_media=c['path'],selected_sha256=c['sha256'],sound_choice=kind,gain_db=gain,start_frame=offset//2000,start_sample=offset,samples=samples,command=cmd));offset+=samples
x=np.concatenate(parts);assert len(x)==1546000
out=EP/'audio/sfx/selected-full-stem-r001.wav';assert not out.exists()
cmd=['ffmpeg','-v','error','-f','f32le','-ar','48000','-ac','2','-i','-','-c:a','pcm_s24le',str(out)];subprocess.run(cmd,input=x.tobytes(),check=True)
d=dict(created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),output=str(out.relative_to(EP)),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),sample_rate=48000,channels=2,samples_per_channel=len(x),frames=773,duration_seconds=773/24,no_time_stretch=True,mute_old_concatenated_audio=True,mix_this_stem_once=True,music=False,ambience=False,clips=rows,write_command=cmd)
(EP/'audio/sfx/selected-full-stem-r001.json').write_text(json.dumps(d,indent=2)+'\n');print(out)
