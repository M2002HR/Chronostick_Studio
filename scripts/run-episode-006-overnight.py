#!/usr/bin/env python3
"""Detached, resumable generation → latest selection → concat → anime6B → voice."""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
import traceback
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'episodes/006-shortest-war-ever'
RUN = EP / 'automation/overnight-finish'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
API = 'http://127.0.0.1:8090'
COMFY = 'http://127.0.0.1:8188'
TERMINAL = {'succeeded', 'failed', 'cancelled', 'completed'}
UPSCALE_PYTHON = '/home/mhr/AI/ComfyUI/.venv/bin/python'


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def api(path: str, payload=None, *, base=API):
    request = urllib.request.Request(base + path, data=None if payload is None else json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
    # GETs are safe to reconnect. Mutations are never blindly repeated.
    attempts = 1 if payload is not None else 120
    for attempt in range(attempts):
        try:
            with OPENER.open(request, timeout=180) as response:
                body = response.read()
                # ComfyUI /free acknowledges success with an empty HTTP body.
                if path == '/free' and not body.strip():
                    return {}
                return json.loads(body)
        except (OSError, urllib.error.URLError):
            if attempt + 1 == attempts:
                raise
            time.sleep(15)


def state(stage: str, **fields) -> None:
    path = RUN / 'status.json'
    prior = json.loads(path.read_text()) if path.exists() else {}
    prior.pop('error', None)
    prior.update(status='running', stage=stage, updated_at=now(), pid=os.getpid(), **fields)
    write(path, prior)
    print(now(), stage, json.dumps(fields, ensure_ascii=False), flush=True)
    episode_path = EP / 'episode.json'
    episode = json.loads(episode_path.read_text())
    episode['overnight_pipeline'].update(status=prior['status'], stage=stage, runtime='automation/overnight-finish/status.json', updated_at=prior['updated_at'])
    write(episode_path, episode)


def probe(path: Path, *, count=False) -> dict:
    command = ['ffprobe','-v','error'] + (['-count_frames'] if count else []) + ['-show_streams','-show_format','-of','json',str(path)]
    raw = json.loads(subprocess.check_output(command, text=True))
    video = next(v for v in raw['streams'] if v['codec_type']=='video')
    audio = next((v for v in raw['streams'] if v['codec_type']=='audio'), None)
    frames = video.get('nb_read_frames') or video.get('nb_frames')
    return dict(width=video['width'], height=video['height'], fps=float(Fraction(video['avg_frame_rate'])), frames=int(frames) if frames not in (None,'N/A') else None, duration=float(video.get('duration') or raw['format']['duration']), has_audio=audio is not None, audio_sample_rate=audio.get('sample_rate') if audio else None)


def validate_picture(path: Path, frames: int, width=1024, height=576) -> dict:
    info = probe(path, count=True)
    assert info['frames']==frames, (str(path), info)
    assert (info['width'],info['height'])==(width,height), (str(path), info)
    assert abs(info['fps']-24)<1e-6 and info['has_audio'], (str(path), info)
    assert abs(info['duration']-frames/24)<0.05, (str(path), info)
    return info


def submit_once(name: str, endpoint: str, payload: dict) -> dict:
    receipt = RUN / f'{name}-submission.json'
    if receipt.exists():
        return json.loads(receipt.read_text())
    intent = RUN / f'{name}-submission-intent.json'
    if intent.exists():
        raise RuntimeError(f'Uncertain {name} submission: inspect service state and recover receipt; no duplicate is submitted.')
    write(intent, dict(at=now(), endpoint=endpoint, payload=payload))
    value = api(endpoint,payload)
    write(receipt,value)
    return value


def wait_for_job(job_id: str, label: str) -> dict:
    while True:
        job = api('/v1/jobs/'+job_id)
        state(label, service_job_id=job_id, service_status=job['status'], service_progress=job.get('progress_percent'))
        if job['status'] in TERMINAL:
            write(RUN/f'{label}-result.json',job)
            if job['status']!='succeeded':
                raise RuntimeError(f'{label} failed: {job.get("error")}')
            return job
        time.sleep(20)


def choose_latest(slot_count: int) -> list[dict]:
    """Highest complete numeric editorial revision, with controlled maps included."""
    records=[]
    candidates=[]
    for directory in ['editorial','controlled-maps','graphics']:
        candidates.extend((EP/'renders'/directory).glob('clip-*-r*.mp4'))
    for number in range(1,slot_count+1):
        options=[]
        for path in candidates:
            match=re.fullmatch(r'clip-(\d+)-.*-r(\d+)\.mp4',path.name)
            if match and int(match[1])==number:
                options.append((int(match[2]),path))
        options.sort(key=lambda item:item[0],reverse=True)
        assert options, f'Missing timeline slot {number:03d}'
        assert len({v[0] for v in options})==len(options), f'Ambiguous same-revision candidates for slot {number:03d}'
        failures=[]
        for revision,path in options:
            try:
                info=validate_picture(path,120)
            except Exception as error:
                failures.append({'path':str(path.relative_to(ROOT)),'error':str(error)})
                continue
            records.append(dict(number=number,revision=revision,source=str(path.relative_to(ROOT)),filename=path.name,sha256=digest(path),probe=info,selection_basis='highest_numeric_completed_revision_explicit_user_instruction',creative_approval=None,rejected_incomplete_candidates=failures))
            break
        else:
            raise RuntimeError(f'No technically complete candidate for slot {number:03d}: {failures}')
    return records


def stage_selection(records: list[dict]) -> Path:
    target=EP/'renders/final-selected'
    manifest_path=EP/'renders/selection-manifest.json'
    provenance=RUN/'selection.json'
    if provenance.exists():
        previous=json.loads(provenance.read_text())
        assert [(v['source'],v['sha256']) for v in previous['clips']]==[(v['source'],v['sha256']) for v in records], 'Selection changed during resumed finish'
    elif target.exists() and any(target.iterdir()):
        archive=EP/'renders'/'selection-archives'
        archive.mkdir(exist_ok=True)
        index=1
        while (archive/f'latest-selection-r{index:03d}').exists():
            index+=1
        target.rename(archive/f'latest-selection-r{index:03d}')
        if manifest_path.exists():
            shutil.copy2(manifest_path,archive/f'latest-selection-r{index:03d}.json')
    target.mkdir(parents=True,exist_ok=True)
    for item in records:
        destination=target/item['filename']
        if destination.exists():
            assert digest(destination)==item['sha256']
        else:
            shutil.copy2(ROOT/item['source'],destination)
    assert len(list(target.glob('*.mp4')))==len(records)
    selection=dict(schema_version='1.0',selected_at=now(),policy='User-directed latest revision; overrides approval-only selection. Creative approval is not inferred.',slot_count=len(records),clips=records,final_approval=None)
    write(provenance,selection)
    write(manifest_path,selection)
    return target


def release_gpu() -> None:
    while True:
        queue=api('/queue',base=COMFY)
        if not queue['queue_running'] and not queue['queue_pending']:
            break
        state('waiting_for_gpu',comfy_running=len(queue['queue_running']),comfy_pending=len(queue['queue_pending']))
        time.sleep(20)
    api('/free',{'unload_models':True,'free_memory':True},base=COMFY)
    time.sleep(3)


def run_command(name: str, command: list[str]) -> None:
    write(RUN/f'{name}-command.json',dict(at=now(),argv=command))
    with (RUN/f'{name}.log').open('a') as log:
        # Avoid oversized CPU thread pools during framewise tile blending.
        environment = os.environ | {'OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4'}
        subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,env=environment)


def upscale_command(source: Path, output: Path, config: dict) -> list[str]:
    return [UPSCALE_PYTHON,str(ROOT/'scripts/upscale-framewise-batched-video.py'),str(source),'--output',str(output),'--model',config['model'],'--width','1920','--height','1080','--fit','cover','--tile',str(config['tile']),'--overlap',str(config['overlap']),'--batch-size',str(config['batch_size']),'--precision',config['precision'],'--crf','16','--preset','medium','--progress-every','120']


def main() -> None:
    RUN.mkdir(parents=True,exist_ok=True)
    lock=(RUN/'pipeline.lock').open('a')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    manifest=json.loads((RUN/'manifest.json').read_text())
    if (RUN/'completed.json').exists():
        print('Already completed; no outputs are overwritten.',flush=True)
        return
    write(RUN/'process.json',dict(pid=os.getpid(),started_at=now(),command=str(Path(__file__)),detached=True))
    assert Path(manifest['upscale']['model']).is_file()
    assert shutil.disk_usage(EP).free>12*1024**3, 'At least12GiB free disk required'
    for record in manifest['records']:
        assert digest(ROOT/record['prompt'])==record['prompt_sha256']
        assert digest(ROOT/record['reference'])==record['reference_sha256']
    state('generation_preflight')
    ready=api('/v1/ready')
    assert ready['ready'] and ready['h3_available'], ready
    jobs=[json.loads(p.read_text()) for p in sorted((RUN/'jobs').glob('*.json'))]
    assert len(jobs)==manifest['job_count']
    submission=submit_once('generation','/v1/batches',dict(jobs=jobs,settings=json.loads((RUN/'settings.json').read_text())))
    batch_id=submission['id']
    manifest.update(status='generation_submitted',batch_id=batch_id,job_ids=submission.get('job_ids'))
    write(RUN/'manifest.json',manifest)
    while True:
        batch=api('/v1/batches/'+batch_id)
        counts=dict(Counter(v['status'] for v in batch.get('jobs',[])))
        state('generation',batch_id=batch_id,counts=counts,job_count=len(jobs))
        write(RUN/'generation-progress.json',{'at':now(),'batch_status':batch['status'],'jobs':[{'id':v['id'],'status':v['status'],'stage':v.get('stage'),'progress_percent':v.get('progress_percent'),'error':v.get('error'),'identity':v.get('request',{}).get('job_identity')} for v in batch.get('jobs',[])]})
        if len(batch.get('jobs',[]))==len(jobs) and all(v['status'] in TERMINAL for v in batch['jobs']):
            break
        time.sleep(30)
    write(RUN/'generation-terminal.json',batch)
    failed=[dict(id=v['id'],error=v.get('error'),identity=v.get('request',{}).get('job_identity')) for v in batch['jobs'] if v['status']!='succeeded']
    write(RUN/'generation-failures.json',{'jobs':failed,'fallback_policy':manifest['generation_failure_policy']})
    slot_count=json.loads((EP/'timestamps/timing-map.json').read_text())['slot_count']
    state('selection',slot_count=slot_count,generation_failures=failed)
    selected=stage_selection(choose_latest(slot_count))
    state('concat',selected_directory=str(selected))
    picture=EP/manifest['outputs']['picture']
    if picture.exists():
        validate_picture(picture,slot_count*120)
    else:
        concat=submit_once('concat','/v1/media/concat',dict(directory=str(selected),output=str(picture),fps=24,missing_audio='fail',overwrite=False))
        wait_for_job(concat['id'],'concat')
        validate_picture(picture,slot_count*120)
    write(RUN/'picture-probe.json',probe(picture,count=True))
    upscale=EP/manifest['outputs']['upscaled']
    if not upscale.exists():
        state('upscale_prepare')
        release_gpu()
        pilot_source=RUN/manifest['upscale'].get('pilot_source','pilot-source-r002.mp4')
        pilot_output=RUN/manifest['upscale'].get('pilot_output','pilot-anime6b-fullframe-1920x1080-r002.mp4')
        if not pilot_source.exists():
            run_command('pilot-extract',['ffmpeg','-v','error','-n','-i',str(picture),'-frames:v','24','-t','1','-map','0:v:0','-map','0:a:0','-c:v','libx264','-crf','16','-preset','fast','-c:a','aac','-ar','48000','-ac','2',str(pilot_source)])
        if not pilot_output.exists():
            run_command('pilot-upscale',upscale_command(pilot_source,pilot_output,manifest['upscale']))
        pilot=validate_picture(pilot_output,24,1920,1080)
        pilot_report=json.loads(pilot_output.with_suffix('.framewise-upscale.json').read_text())
        state('upscale',pilot=pilot,processing_fps=pilot_report['processing_fps'],estimated_upscale_seconds=(slot_count*120)/pilot_report['processing_fps'])
        run_command('upscale',upscale_command(picture,upscale,manifest['upscale']))
    final_probe=validate_picture(upscale,slot_count*120,1920,1080)
    state('narration_mix')
    voice=EP/'audio/narration-es-google-vids-r001.mp4'
    voice_manifest=json.loads((EP/'audio/manifest.json').read_text())
    assert digest(voice)==voice_manifest['sha256'], 'Accepted narration changed'
    distribution=EP/manifest['outputs']['distribution']
    if not distribution.exists():
        duration=slot_count*5
        temporary=distribution.with_name('.'+distribution.stem+'.partial.mp4')
        temporary.unlink(missing_ok=True)
        run_command('narration-mix',['ffmpeg','-v','error','-n','-i',str(upscale),'-i',str(voice),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',f'apad,atrim=duration={duration}','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(duration),'-metadata:s:a:0','language=spa','-movflags','+faststart',str(temporary)])
        validate_picture(temporary,slot_count*120,1920,1080)
        temporary.replace(distribution)
    distribution_probe=validate_picture(distribution,slot_count*120,1920,1080)
    # Full decode detects truncation/corruption. It is explicitly technical QC,
    # and is never labelled a human visual or audio approval.
    state('final_technical_qc')
    run_command('final-decode',['ffmpeg','-v','error','-xerror','-i',str(distribution),'-map','0:v:0','-map','0:a:0','-f','null','-'])
    finished=dict(completed_at=now(),status='completed_with_generation_fallbacks' if failed else 'completed',slot_count=slot_count,frames=slot_count*120,duration_seconds=slot_count*5,generation_batch_id=batch_id,generation_failures=failed,outputs={key:{'path':str((EP/value).relative_to(ROOT)),'sha256':digest(EP/value)} for key,value in manifest['outputs'].items()},upscaled_probe=final_probe,distribution_probe=distribution_probe,technical_qc='Numbering,120frames per slot,24fps,dimensions,audio stream,655second picture timeline and full final decode verified.',creative_qc='User-directed latest-revision assembly. Generated replacements and other latest clips are not silently creatively approved.',native_audio_policy=manifest['audio_policy'],approval=None)
    write(distribution.with_suffix('.run.json'),finished)
    write(RUN/'completed.json',finished)
    state('complete',completion=finished)
    status=json.loads((RUN/'status.json').read_text());status['status']=finished['status'];write(RUN/'status.json',status)
    manifest.update(status=finished['status'],completed_at=finished['completed_at']);write(RUN/'manifest.json',manifest)
    episode_path=EP/'episode.json';episode=json.loads(episode_path.read_text())
    episode['picture_master']=manifest['outputs']['upscaled'];episode['distribution_master']=manifest['outputs']['distribution']
    episode['overnight_pipeline'].update(status=finished['status'],completed_at=finished['completed_at'],technical_qc='passed',creative_approval=None)
    episode['next_action']='Review the completed user-directed latest-revision picture and Spanish distribution export; technical QC passed, creative approval remains pending.'
    write(episode_path,episode)
    (EP/'final/distribution-review.md').write_text('# Overnight export technical report\n\n'+f"Completed: {finished['completed_at']}\n\n"+f"Distribution: `{manifest['outputs']['distribution']}`\n\n"+finished['technical_qc']+'\n\n'+finished['creative_qc']+'\n\n'+manifest['audio_policy']+'\n\nGeneration failures/fallbacks: '+json.dumps(failed,ensure_ascii=False)+'\n')
    print('COMPLETE',distribution,flush=True)


if __name__=='__main__':
    try:
        main()
    except Exception as error:
        traceback.print_exc()
        write(RUN/'error.json',dict(at=now(),error=str(error),traceback=traceback.format_exc()))
        if (RUN/'status.json').exists():
            value=json.loads((RUN/'status.json').read_text());value.update(status='failed',error=str(error),updated_at=now());write(RUN/'status.json',value)
        raise
