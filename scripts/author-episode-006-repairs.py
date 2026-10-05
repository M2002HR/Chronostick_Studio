#!/usr/bin/env python3
"""Apply manually reviewed clip-specific direction to the active pure prompts."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EP=ROOT/'episodes/006-shortest-war-ever'

def author(n,lock,crop=None,action=None):
    p=EP/f'prompts/clip-{n:03d}.md';s=p.read_text()
    i=s.index('Keep every pixel') if 'Keep every pixel' in s else s.index('Keep the pictured') if 'Keep the pictured' in s else s.index('Preserve the reference')
    s=s[:i]+lock+' '+s[i:]
    if crop and ("2.30–5.00s:" in s or "2.05–5.00s:" in s):
        cut='2.30–5.00s:' if '2.30–5.00s:' in s else '2.05–5.00s:'
        b=s.index(cut);e=s.index('camera locked.',b)
        s=s[:b]+cut+' '+crop+'; camera locked.'+s[e+len('camera locked.'):]
    if action:
        b=s.index('camera locked.',s.index('0.00–'));e=s.index('Complete',b)
        s=s[:b+len('camera locked.')]+ ' '+action+' '+s[e:]
    s=s.replace(' This is before first fire: no cannon flash, blast, battle smoke, damage or firing order.','')
    s=s.replace('Existing damage stays fixed except the one explicitly permitted tiny change.','The current reference scene stays unchanged except the declared small action.')
    s=s.replace('only a tiny eyebrow, cloth or water adjustment already supported by the anchor is allowed.','hold the completed action and current props entirely still.')
    s=s.replace('Hold settled from 4.35s;', 'Camera and main action are entirely still for the last second. Hold settled from 4.35s;')
    s=s.replace('Hold the resolved state from 4.35s;', 'Camera and main action are entirely still for the last second. Hold the resolved state from 4.35s;')
    assert s.count('NO BACKGROUND MUSIC. Natural diegetic sound effects only.')==1
    p.write_text(s)

def main():
    directives=json.loads((EP/'plan/repair-directives.json').read_text())
    for r in directives['clips']:
        if (EP/f"automation/retries/review-r006/clip-{r['number']:03d}/submission.json").exists():continue
        author(r['number'],r['lock'],r.get('crop'),r.get('action'))
        print(f"authored {r['number']:03d}")

if __name__=='__main__':main()
