import json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
root=Path('/home/mhr/Code/chronostick-studio');ep=root/'episodes/006-shortest-war-ever';tmp=Path('/tmp/chronostick-006-animatic-r007');tmp.mkdir(exist_ok=True)
slots=json.loads((ep/'plan/clip-direction.json').read_text())['slots'];frames={};rows=[];lines=['ffconcat version 1.0'];out=ep/'plan/animatic-r007.mp4';assert not out.exists()
def frame(ref,close=False,key=''):
 signature=(ref,close)
 if signature not in frames:
  p=tmp/f'frame-{len(frames):03d}.jpg'
  filt='scale=640:360'
  if close:
   x='.08';y='.08'
   if key.startswith('rawson'):x='.01'
   if key.startswith('hook-shoe'):x='.15'
   if key=='shoe-foot-insert':x='.20';y='.16'
   filt=f'crop=iw*.8:ih*.8:iw*{x}:ih*{y},scale=640:360'
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(root/ref),'-vf',filt,'-frames:v','1','-threads','1',str(p)],check=True)
  frames[signature]=p
 return frames[signature]
for s in slots:
 refs=s['references'];key=s['asset_ids'][-1];parts=[]
 if len(refs)==2:
  onset={99:0.8,105:0.8,118:1.72}[s['number']];end={99:3.8,105:3.8,118:4.35}[s['number']]
  split=(onset+end)/2
  parts=[(frame(refs[0]),split),(frame(refs[1]),5-split)]
 else:
  parts=[(frame(refs[0],i>0,key),sh['end']-sh['start']) for i,sh in enumerate(s['shots'])]
  if s['number']==105:
   p=tmp/'surrender-initial.jpg'
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(root/refs[0]),'-vf','crop=iw*.42:ih*.30:iw*.48:ih*.65,scale=640:360','-frames:v','1',str(p)],check=True)
   parts=[(p,.68),(frame(refs[0]),4.32)]
 for f,d in parts:lines.extend([f"file '{f}'",f'duration {d:.6f}'])
 rows.append((s,parts))
lines.append(f"file '{parts[-1][0]}'")
concat=ep/'plan/animatic-r007.ffconcat';concat.write_text('\n'.join(lines)+'\n')
for index in range(0,len(rows),16):
 sheet=Image.new('RGB',(1280,16//4*208),'#181818');draw=ImageDraw.Draw(sheet)
 for j,(s,parts) in enumerate(rows[index:index+16]):
  x=(j%4)*320;y=(j//4)*208
  im=Image.open(parts[0][0]).resize((320,180));sheet.paste(im,(x,y));draw.text((x+3,y+182),f"{s['number']:03d} {s['start']:g}s {s['asset_ids'][-1][:30]}",fill='white')
 sheet.save(tmp/f'sheet-{index//16+1}.jpg')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-f','concat','-safe','0','-i',str(concat),'-i',str(ep/'audio/narration-es-google-vids-r001.mp4'),'-i',str(ep/'renders/controlled-maps/clip-014-map-r005.mp4'),'-i',str(ep/'renders/controlled-maps/clip-118-map-r005.mp4'),'-filter_complex','[0:v]fps=12[base];[2:v]scale=640:360,fps=12,setpts=PTS+65/TB[m14];[base][m14]overlay=eof_action=pass:enable=between(t\,65\,70)[mid];[3:v]scale=640:360,fps=12,setpts=PTS+585/TB[m118];[mid][m118]overlay=eof_action=pass:enable=between(t\,585\,590)[v]','-map','[v]','-map','1:a:0','-c:v','libx264','-preset','veryfast','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-af','apad','-t','655','-movflags','+faststart',str(out)],check=True)
print('Animatic r007 complete:131 slots with actual controlled map inserts; other motion represented by planning stills.')
