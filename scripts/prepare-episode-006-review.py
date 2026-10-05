#!/usr/bin/env python3
"""Freeze latest per-slot candidates and prepare dense visual review evidence."""
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'episodes/006-shortest-war-ever'
OUT = EP / 'renders/review-evidence-r006'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    OUT.mkdir(exist_ok=True)
    inventory = OUT / 'baseline.json'
    if inventory.exists():
        rows = json.loads(inventory.read_text())['clips']
    else:
        rows = []
        for n in range(1, 132):
            candidates = list((EP/'renders/editorial').glob(f'clip-{n:03d}-*.mp4'))
            candidates += list((EP/'renders/controlled-maps').glob(f'clip-{n:03d}-*.mp4'))
            assert candidates, f'missing {n}'
            p = max(candidates, key=lambda p: int(re.search(r'-r(\d+)', p.name)[1]))
            side = p.with_suffix('.run.json')
            job = json.loads(side.read_text())['original_request'] if side.exists() else None
            rows.append(dict(number=n, path=str(p.relative_to(ROOT)), sha256=sha(p),
                             revision=int(re.search(r'-r(\d+)', p.name)[1]), request=job))
        inventory.write_text(json.dumps(dict(frozen_at=datetime.now(timezone.utc).isoformat(),
                           selection_policy='highest immutable revision per slot, not mtime', clips=rows),indent=2)+'\n')
    for r in rows:
        p = ROOT/r['path']
        target = OUT/f"clip-{r['number']:03d}.jpg"
        if target.exists(): continue
        # Decode every frame. Dense samples include both sides of the planned 2.30s cut.
        data = subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-an','-vf','scale=320:180',
                                        '-f','rawvideo','-pix_fmt','rgb24','-threads','1','pipe:1'])
        frames = len(data)//(320*180*3)
        samples = sorted(set(list(range(0, frames, 6))+[53,54,55,56,57,104,105,119]))
        samples = [f for f in samples if f < frames]
        tiles = []
        if r['request']:
            a = ROOT/r['request']['references'][0]['path']
            tiles.append((Image.open(a).convert('RGB').resize((320,180)), 'ANCHOR'))
        for f in samples:
            tiles.append((Image.frombytes('RGB',(320,180),data[f*172800:(f+1)*172800]),f'{f/24:.3f}s / f{f}'))
        sheet = Image.new('RGB',(1600, 32+204*((len(tiles)+4)//5)), '#18212a')
        draw = ImageDraw.Draw(sheet)
        draw.text((8,8),f"CLIP {r['number']:03d} r{r['revision']:03d} — {p.name}",fill='white')
        for i,(im,label) in enumerate(tiles):
            x=(i%5)*320;y=32+(i//5)*204
            sheet.paste(im,(x,y));draw.text((x+5,y+183),label,fill='white')
        sheet.save(target,quality=88)
        probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
        (OUT/f"clip-{r['number']:03d}.probe.json").write_text(json.dumps(probe,indent=2)+'\n')
        print(f"prepared {r['number']:03d} r{r['revision']:03d} frames={frames}",flush=True)

if __name__ == '__main__': main()
