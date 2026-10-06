from pathlib import Path
import json,time,subprocess,hashlib,datetime
from PIL import Image,ImageDraw
EP=Path('/home/mhr/Code/chronostick-studio/episodes/008-pinocchio-ww2');video=EP/'final/picture-master-1080x1920-r001.mp4';sidecar=video.with_suffix('.framewise-upscale.json')
while not sidecar.exists():time.sleep(10)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(video)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');assert int(v['nb_frames'])==773 and v['avg_frame_rate']=='24/1' and (v['width'],v['height'])==(1080,1920)
indices=[0,14,65,73,106,121,122,173,175,176,178,229,230,314,357,365,366,459,460,461,499,532,533,596,597,598,640,661,662,735,748,749,750,752,767,768,770,772];out=EP/'final/upscale-qc-r001';out.mkdir(exist_ok=False)
expr='select='+ '+'.join('eq(n\\,'+str(n)+')' for n in indices)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-vf',expr,'-vsync','0','-q:v','2',str(out/'sample-%03d.jpg')],check=True)
files=sorted(out.glob('sample-*.jpg'));assert len(files)==len(indices)
for page,start in enumerate(range(0,len(files),16),1):
 can=Image.new('RGB',(1080,2000),'white');d=ImageDraw.Draw(can)
 for i,f in enumerate(files[start:start+16]):
  im=Image.open(f);im.thumbnail((270,480));x=i%4*270;y=i//4*500;can.paste(im,(x,y+20));d.text((x+3,y+3),f'{indices[start+i]} / {indices[start+i]/24:.3f}s',fill='black')
 can.save(out/f'phone-contact-{page:02d}.jpg')
(out/'evidence.json').write_text(json.dumps(dict(created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='needs_actual_review',video=str(video.relative_to(EP)),sha256=hashlib.sha256(video.read_bytes()).hexdigest(),sample_indices=indices,files=[f.name for f in files],frames=773,fps=24,dimensions=[1080,1920]),indent=2)+'\n');print(out,flush=True)
