#!/usr/bin/env python3
"""Save automated audiovisual observations; these never confer approval."""
import asyncio
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'ajil'))
from unified_gateway.app.config import get_settings
from unified_gateway.app.providers.gemini_adapter import GeminiAdapter

EP = ROOT/'episodes/006-shortest-war-ever'
OUT = EP/'renders/review-evidence-r006'
RULES = """Analyze the actual five-second animation WITH AUDIO, comparing the reference image,
the intended local shot plan and the generator prompt. Return JSON only:
{visual_observations: [{start: seconds, end: seconds, issue: string, severity: major|minor}],
audio: {heard: string, music: boolean|null, speech: boolean|null, tonal_bed: boolean|null,
events: [{start: seconds, end: seconds, description: string}], confidence: high|medium|low},
action_matches: boolean, cut_times: [seconds], final_resolved: boolean,
exact_text_seen: [string], summary: string}.
Keep the entire response under 450 words, with AT MOST THREE visual observations.
Only report major actionable defects; combine related times rather than listing each frame.
The style is drawn stick figures with round off-white heads, dot eyes, thin limbs,
bold dark contours and drawn period backgrounds throughout. Report only observable defects:
identity/prop duplication, anatomical or rigid-object morphing, impossible motion, mismatched
story state, photographic drift, unauthorized writing, unreadable action. A planned hard cut
is not a teleportation defect. Preserve distinctions between a protectorate and annexation.
Sound must be brief isolated natural diegetic effects with silence, no continuous ambience,
music, tonal drones, speech, vocal reactions or lip sync. Listen: do not infer audio compliance
from the prompt. Do not invent issues. Minimal mouths can change expression without speech.
Automated observations are evidence for further review, not approval. No other tasks."""

async def main():
    a = GeminiAdapter(get_settings().gemini)
    rows=json.loads((OUT/'baseline.json').read_text())['clips']
    plan=(EP/'plan/shot-plan.md').read_text()
    try:
        for r in rows:
            n=r['number'];dest=OUT/f'clip-{n:03d}.av-observations.json'
            if dest.exists():continue
            section=plan.split(f'## Clip {n:03d} ')[1].split('\n## Clip ')[0]
            section='\n'.join(line for line in section.splitlines() if not line.startswith('Narration:'))
            parts=[{'text':RULES+'\nSHOT PLAN:\n'+section}]
            if r['request']:
                j=r['request'];prompt=(ROOT/j['prompt']['file']).read_text()
                parts.append({'text':'GENERATOR PROMPT:\n'+prompt+'\nREFERENCE IMAGE:'})
                for ref in j['references']:
                    parts.append({'inlineData':{'mimeType':'image/png','data':base64.b64encode((ROOT/ref['path']).read_bytes()).decode()}})
            parts.extend([{'text':'ACTUAL CANDIDATE VIDEO WITH AUDIO:'},
                          {'inlineData':{'mimeType':'video/mp4','data':base64.b64encode((ROOT/r['path']).read_bytes()).decode()},
                           'videoMetadata':{'fps':12}}])
            payload={'contents':[{'role':'user','parts':parts}],
                     'generationConfig':{'temperature':0,'responseMimeType':'application/json','maxOutputTokens':4096,
                                         'thinkingConfig':{'thinkingBudget':0}}}
            response=await a.service.proxy_call(payload,path_model=a.default_model)
            raw=response.content
            if response.status_code>=400:
                print(f'clip {n:03d}: upstream HTTP {response.status_code}; stopping, no approval',flush=True)
                (OUT/f'clip-{n:03d}.av-error.json').write_bytes(raw)
                break
            provider=OUT/f'clip-{n:03d}.av-provider.json'
            attempt=1
            while provider.exists():
                attempt+=1;provider=OUT/f'clip-{n:03d}.av-provider-r{attempt:03d}.json'
            provider.write_bytes(raw)
            result=response.json()
            result_text=''.join(p.get('text','') for c in result.get('candidates',[]) for p in c.get('content',{}).get('parts',[]))
            try: obs=json.loads(result_text)
            except ValueError:
                print(f'clip {n:03d}: malformed observations; remains unreviewed',flush=True);continue
            dest.write_text(json.dumps(dict(number=n,source=r['path'],source_sha256=r['sha256'],
                              reviewer='automated Gemini audiovisual observations; pending Codex review',
                              model=a.default_model,observations=obs),ensure_ascii=False,indent=2)+'\n')
            print(f"clip {n:03d}: {obs.get('summary','')} audio={obs.get('audio',{})}",flush=True)
    finally:await a.service.aclose()

if __name__=='__main__':asyncio.run(main())
