#!/usr/bin/env python3
"""Replace failed native audio with reviewed recorded or declared procedural cues.

No video edit, no music separation, no source-audio excerpts. Review the actual
picture first and declare observed physical cue times in a separate JSON plan.
"""
import argparse
from array import array
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import wave

RATE=48000
KINDS={'paper','cloth','metal','wood'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dry_cue(kind,duration,seed,peak_db):
    if kind not in KINDS or not 0<duration<=0.15 or not -48<=peak_db<=-18:
        raise ValueError('Use a supported dry physical cue, <=150ms and restrained peak')
    rng=random.Random(seed);count=round(duration*RATE);amplitude=10**(peak_db/20)
    samples=[];previous=0;filtered=0
    for index in range(count):
        noise=rng.uniform(-1,1)
        if kind in ('paper','metal'):
            value=(noise-previous)*.5
        else:
            filtered=.7*filtered+.3*noise;value=filtered
        previous=noise
        position=index/max(1,count-1)
        envelope=math.sin(math.pi*position)**2
        if kind in ('metal','wood'):
            envelope*=math.exp(-8*position)
        samples.append(round(value*envelope*amplitude*32767))
    return samples

def write_wave(path,samples):
    values=array('h',samples)
    if sys.byteorder!='little':values.byteswap()
    with wave.open(str(path),'wb') as target:
        target.setnchannels(1);target.setsampwidth(2);target.setframerate(RATE);target.writeframes(values.tobytes())

def recorded_cue(ep,cue,preview=False):
    path=(ep/cue['asset_path']).resolve()
    if not path.is_relative_to(ep/'audio/sfx') or sha(path)!=cue['asset_sha256']:
        raise ValueError('Bind an unchanged separately reviewed physical SFX asset')
    allowed=('approved','needs_actual_sound_review') if preview else ('approved',)
    if cue.get('review_status') not in allowed or not cue.get('review_evidence'):
        raise ValueError('An unreviewed sound candidate cannot enter the final mix')
    with wave.open(str(path),'rb') as source:
        if (source.getnchannels(),source.getsampwidth(),source.getframerate())!=(1,2,RATE):
            raise ValueError('Reviewed cue must be48k mono PCM16')
        samples=array('h');samples.frombytes(source.readframes(source.getnframes()))
    if sys.byteorder!='little':samples.byteswap()
    if not 0<len(samples)<=RATE*.15:
        raise ValueError('Keep each physical one-shot <=150ms')
    gain=cue.get('gain_db',0)
    if isinstance(gain,bool) or not isinstance(gain,(int,float)) or not math.isfinite(gain) or not -24<=gain<=0:
        raise ValueError('Cue gain must remain restrained, -24..0dB')
    return [round(v*10**(gain/20)) for v in samples]

def video_hashes(path):
    output=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-an','-f','framemd5','-']).decode()
    return [line.rsplit(',',1)[-1].strip() for line in output.splitlines() if not line.startswith('#')]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('episode',type=Path)
    parser.add_argument('--plan',type=Path,required=True)
    parser.add_argument('--preview',action='store_true',help='Create a clearly unapproved listening candidate')
    args=parser.parse_args();ep=args.episode.resolve();plan_path=args.plan.resolve();plan=json.loads(plan_path.read_text())
    source=(ep/plan['source']).resolve();output=(ep/plan['output']).resolve()
    if not source.is_relative_to(ep/'renders') or not output.is_relative_to(ep/'renders'):
        raise ValueError('Media must stay under episode renders')
    if args.preview and output.is_relative_to(ep/'renders/final-selected'):
        raise ValueError('An unreviewed listening preview cannot become a finalselection')
    if plan.get('source_sha256')!=sha(source) or plan.get('native_audio')!='exclude_completely':
        raise ValueError('Bind actual sourcehash and explicitly exclude entire nativeaudio')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(source)]))
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    if video['avg_frame_rate']!='24/1':raise ValueError('Declared Short must be24fps')
    frames=int(video['nb_frames']);count=frames*RATE//24
    stem=(ep/plan['stem']).resolve();report=output.with_suffix('.clean-sfx.json')
    if not stem.is_relative_to(ep/'audio') or any(p.exists() for p in (output,stem,report)):
        raise FileExistsError('Use unused immutable output/stem paths')
    samples=[0]*count;events=[];last_end=0
    for cue in plan['cues']:
        values=recorded_cue(ep,cue,args.preview) if 'asset_path' in cue else dry_cue(cue['kind'],cue['duration_seconds'],cue['seed'],cue['peak_db'])
        start=round(cue['start_seconds']*RATE);end=start+len(values)
        if start<last_end or end>count or not cue.get('observed_action'):
            raise ValueError('Cues must be sorted, non-overlapping, inside actualtake and action-reviewed')
        samples[start:end]=values;last_end=end
        events.append(dict(cue,start_sample=start,end_sample=end))
    output.parent.mkdir(parents=True,exist_ok=True);stem.parent.mkdir(parents=True,exist_ok=True)
    write_wave(stem,samples)
    # Only source VIDEO is retained. Input1 supplies the separate physical cue stem.
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(source),'-i',str(stem),'-map','0:v:0','-map','1:a:0',
                    '-c:v','copy','-c:a','aac','-b:a','128k','-ar',str(RATE),'-ac','2','-map_metadata','-1',
                    '-metadata','comment=Native soundtrack completely excluded; isolated dry SFX only.',
                    '-movflags','+faststart',str(output)],check=True)
    original=video_hashes(source);result=video_hashes(output)
    if original!=result or len(result)!=frames:raise ValueError('Pictureframe preservation failed')
    silence=[];position=0
    for cue in events:
        silence.append([position,cue['start_sample']]);position=cue['end_sample']
    silence.append([position,count])
    if any(any(samples[start:end]) for start,end in silence):raise ValueError('Nonzero audio outside declaredcues')
    evidence={'created_at':datetime.now(timezone.utc).isoformat(),'status':'technical_clean_sfx_derivative_needs_release_review',
              'source':plan['source'],'source_sha256':sha(source),'output':plan['output'],'output_sha256':sha(output),
              'plan_sha256':sha(plan_path),'stem':plan['stem'],'stem_sha256':sha(stem),'sample_rate':RATE,
              'stem_sample_count':count,'native_audio_contribution_samples':0,'decoded_video_frames_identical':True,
              'video_frames':frames,'cue_generation':'Explicit recorded physical one-shots when asset_path is set; seeded non-periodic procedural transients only when separately declared. No native soundtrack/music separation, looping or sustained bed.',
              'cues':events,'exact_zero_silence_sample_intervals':silence,
              'personal_listening_claimed':False,'unapproved_preview':args.preview,
              'limits':'This proves source exclusion and declared silent PCM regions; actual encoded audiovisual release review remains separate.'}
    with report.open('x') as stream:json.dump(evidence,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print(output)

if __name__=='__main__':main()
