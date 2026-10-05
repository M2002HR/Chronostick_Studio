#!/usr/bin/env python3
"""Track the persisted repair queue and prepare new media for actual review."""
import argparse
import concurrent.futures
import json
import os
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'episodes/006-shortest-war-ever'
QUEUE = EP / 'automation/retries/review-r006'
OUT = EP / 'renders/review-evidence-r006'

def fetch(path):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return json.load(opener.open('http://127.0.0.1:8090/v1/' + path, timeout=30))

def inspect_receipt(receipt):
    response = json.loads(receipt.read_text())
    batch = fetch('batches/' + response['id'])
    children = [fetch('jobs/' + ident) for ident in batch.get('job_ids', [])]
    return dict(number=int(receipt.parent.name[-3:]), batch_id=batch['id'],
                manifest=str(receipt.parent/'manifest.json'),
                batch_status=batch['status'], jobs=[dict(id=j['id'], status=j['status'],
                error=j.get('error'), progress=j.get('progress')) for j in children])

def prepare(row):
    n = row['number']
    record = json.loads(Path(row['manifest']).read_text())
    rev = record['revision']
    path = EP / f'renders/editorial/clip-{n:03d}-shot-r{rev:03d}.mp4'
    target = OUT / f'clip-{n:03d}-r{rev:03d}.jpg'
    if target.exists() or not path.exists():
        return
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-an',
        '-vf', 'scale=320:180', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-threads', '1', 'pipe:1'])
    count = len(raw) // 172800
    samples = sorted(set(range(0, count, 6)) | {48,49,50,51,53,54,55,56,57,104,105,119})
    anchor = ROOT / record['references'][0]['path']
    tiles = [(Image.open(anchor).convert('RGB').resize((320,180)), 'ANCHOR')]
    for k in samples:
        if k < count:
            tiles.append((Image.frombytes('RGB', (320,180), raw[k*172800:(k+1)*172800]), f'{k/24:.3f}s / f{k}'))
    sheet = Image.new('RGB', (1600, 32+204*((len(tiles)+4)//5)), '#18212a')
    draw = ImageDraw.Draw(sheet)
    draw.text((8,8), f'{path.name} — replacement, NOT APPROVED', fill='white')
    for i,(im,label) in enumerate(tiles):
        x=i%5*320;y=32+i//5*204
        sheet.paste(im,(x,y));draw.text((x+5,y+183),label,fill='white')
    sheet.save(target, quality=90)
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    target.with_suffix('.probe.json').write_text(json.dumps(probe,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--watch',action='store_true')
    args=parser.parse_args()
    while True:
        receipts=sorted((EP/'automation/retries').glob('review-r*/clip-*/submission.json'))
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            rows=list(pool.map(inspect_receipt,receipts))
        counts={}
        for row in rows:
            for job in row['jobs']:
                counts[job['status']]=counts.get(job['status'],0)+1
            if row['batch_status']=='succeeded':
                prepare(row)
        snapshot=dict(checked_at=datetime.now(timezone.utc).isoformat(), counts=counts,
                      submitted_jobs=len(rows), submitted_slots=len({r['number'] for r in rows}),
                      replacements_require_actual_review=True, clips=rows)
        temp=QUEUE/f'status.json.{os.getpid()}.tmp';temp.write_text(json.dumps(snapshot,indent=2)+'\n');temp.replace(QUEUE/'status.json')
        print(snapshot['checked_at'], counts, flush=True)
        if not args.watch or all(r['batch_status'] in ['succeeded','failed','cancelled'] for r in rows):
            return
        time.sleep(30)

if __name__=='__main__':
    main()
