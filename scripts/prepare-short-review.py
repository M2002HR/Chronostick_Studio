#!/usr/bin/env python3
"""Archive actual Short frames/probes/audio evidence without approving a render."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone
from PIL import Image, ImageDraw

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
                     '-show_format','-of','json',str(path)]))

def prepare(ep, clip_id, media, revision):
    if not re.fullmatch(r'r\d{3}',revision):
        raise ValueError('Use an unused rNNN evidence revision')
    timing = json.loads((ep/'timestamps/timing-map.json').read_text())
    direction = json.loads((ep/'plan/clip-direction.json').read_text())
    slot = next(c for c in timing['clips'] if c['id']==clip_id)
    clip = next(c for c in direction['clips'] if c['id']==clip_id)
    media = media.resolve()
    if not media.is_relative_to(ep/'renders') or not media.is_file():
        raise ValueError('Review an actual immutable episode render')
    out = ep/'renders/review-evidence'/f'{clip_id}-{revision}'
    out.mkdir(parents=True,exist_ok=False)
    data = probe(media)
    (out/'probe.json').write_text(json.dumps(data,indent=2)+'\n')
    video = next(s for s in data['streams'] if s['codec_type']=='video')
    if video['avg_frame_rate']!='24/1':
        raise ValueError('Review expects the declared 24fps Short')
    subprocess.run(['ffmpeg','-v','error','-i',str(media),'-vsync','0','-q:v','2',
                    str(out/'frame-%03d.jpg')],check=True)
    files = sorted(out.glob('frame-*.jpg'))
    for page,start in enumerate(range(0,len(files),30),1):
        canvas=Image.new('RGB',(900,2070),(235,235,235));draw=ImageDraw.Draw(canvas)
        for index,path in enumerate(files[start:start+30]):
            x=index%5*180;y=index//5*345
            with Image.open(path) as source:
                image=source.copy();image.thumbnail((180,324));canvas.paste(image,(x,y+20))
            draw.text((x+3,y+3),f'{start+index:03d} {(start+index)/24:.3f}s',fill='black')
        canvas.save(out/f'all-frames-{page:02d}.jpg')
    audio = [s for s in data['streams'] if s['codec_type']=='audio']
    if audio:
        subprocess.run(['ffmpeg','-v','error','-i',str(media),'-vn','-c:a','pcm_s24le',
                       str(out/'actual-audio.wav')],check=True)
        subprocess.run(['ffmpeg','-v','error','-i',str(media),'-filter_complex',
                        'aformat=channel_layouts=mono,showwavespic=s=1200x240:colors=black',
                        '-frames:v','1',str(out/'audio-waveform.png')],check=True)
    boundaries=[s['start_frame_local'] for s in clip['shots']][1:]
    review = {'created_at':datetime.now(timezone.utc).isoformat(),'status':'needs_actual_review',
              'clip_id':clip_id,'media':str(media.relative_to(ep)),
              'media_sha256':hashlib.sha256(media.read_bytes()).hexdigest(),
              'actual_frames':len(files),'expected_frames':slot['frame_count'],
              'frame_count_matches':len(files)==slot['frame_count'],'audio_stream_present':bool(audio),
              'planned_shot_count':len(clip['shots']),'planned_cut_frames':boundaries,
              'cut_inspection_frames':sorted({f for b in boundaries for f in (b-1,b,b+1) if 0<=f<len(files)}),
              'limitations':'Frames, waveform and job flags do not prove silence/no music. Actual sound review is required. No creative approval inferred.'}
    (out/'evidence.json').write_text(json.dumps(review,indent=2)+'\n')
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('episode',type=Path)
    parser.add_argument('--clip',required=True)
    parser.add_argument('--media',type=Path,required=True)
    parser.add_argument('--revision',required=True)
    args=parser.parse_args()
    print(prepare(args.episode.resolve(),args.clip,args.media,args.revision))

if __name__=='__main__':
    main()
