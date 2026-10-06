import json,hashlib,subprocess,datetime
from pathlib import Path
import numpy as np
EP=Path('/home/mhr/Code/chronostick-studio/episodes/008-pinocchio-ww2')
family=EP/'renders/editorial/episode-008-clip-02-families-distribution-blocked-r003.mp4';dock=EP/'renders/editorial/episode-008-clip-02-isolated-dock-r004.mp4';output=EP/'renders/editorial/episode-008-clip-02-directed-composite-r004.mp4'
assert not output.exists()
r=json.loads((EP/'renders/clip-02-isolated-dock-review-r004.json').read_text());assert r['picture_decision']=='approved_actual_dock_subtake'
assert json.loads((EP/'renders/clip-02-review-r003.json').read_text())['decision']=='reject_complete_clip_select_family_subtake_only'
cmd=['ffmpeg','-v','error','-n','-i',str(family),'-i',str(dock),'-filter_complex','[0:v:0]trim=start_frame=0:end_frame=54,setpts=PTS-STARTPTS[f];[1:v:0]trim=start_frame=0:end_frame=54,setpts=PTS-STARTPTS[d];[f][d]concat=n=2:v=1:a=0[v]','-map','[v]','-an','-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p','-r','24','-frames:v','108','-movflags','+faststart',str(output)]
subprocess.run(cmd,check=True)
def small(path):
 b=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-vf','scale=120:216','-vsync','0','-pix_fmt','gray','-f','rawvideo','-']);return np.frombuffer(b,np.uint8).reshape(-1,216,120)
a=np.concatenate([small(family)[:54],small(dock)[:54]]);b=small(output);assert a.shape==b.shape==(108,216,120);mae=abs(a.astype(np.int16)-b.astype(np.int16)).mean(axis=(1,2));assert mae.max()<5
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report=dict(created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='technical_composite_needs_actual_review',output=str(output.relative_to(EP)),sha256=sha(output),direction='plan/clip-02-direction-r004.json',sources=[dict(path=str(family.relative_to(EP)),sha256=sha(family),frames=[0,54],output_frames=[0,54],review='renders/clip-02-review-r003.json'),dict(path=str(dock.relative_to(EP)),sha256=sha(dock),frames=[0,54],output_frames=[54,108],review='renders/clip-02-isolated-dock-review-r004.json')],frames=108,fps=24,seconds=4.5,native_audio_contribution_samples=0,no_time_stretch=True,no_freeze=True,decoded_frame_correspondence=dict(compared_frames=108,method='same-index120x216decodedgrayscaleMAE',max_mae_255=float(mae.max()),mean_mae_255=float(mae.mean()),bit_exact_claim=False),command=cmd)
(EP/'renders/clip-02-composite-provenance-r004.json').write_text(json.dumps(report,indent=2)+'\n')
print(output)
