#!/usr/bin/env python3
"""Independent native audio observations without narrative or prompt contamination."""
import asyncio
import base64
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'ajil'))
from unified_gateway.app.config import get_settings
from unified_gateway.app.providers.gemini_adapter import GeminiAdapter

OUT = ROOT / 'episodes/006-shortest-war-ever/renders/review-evidence-r006'

async def main():
    adapter = GeminiAdapter(get_settings().gemini)
    semaphore = asyncio.Semaphore(3)

    async def inspect(row):
        target = OUT / f"clip-{row['number']:03d}.audio-only.json"
        if target.exists():
            return
        path = ROOT / row['path']
        pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-vn',
                                       '-ar', '16000', '-ac', '1', '-f', 's16le', 'pipe:1'])
        import array
        samples = array.array('h', pcm)
        peak = max(map(abs, samples), default=0)
        result = dict(number=row['number'], source=row['path'], source_sha256=row['sha256'],
                      pcm_sha256=hashlib.sha256(pcm).hexdigest(), peak_pcm16=peak,
                      status='observations_pending_review')
        if peak == 0:
            result.update(status='verified_digital_silence', music=False, speech=False,
                          tonal_bed=False, heard='All decoded audio samples are zero.')
        else:
            wav = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-vn',
                                           '-ar', '16000', '-ac', '1', '-f', 'wav', 'pipe:1'])
            payload = {'contents': [{'role': 'user', 'parts': [
                {'text': 'Listen to this actual five-second audio. No story context is provided. '
                         'Describe only audible sounds. Do not invent speech. Return JSON with '
                         'heard, speech boolean, exact_words string (empty if none), music boolean, '
                         'tonal_bed boolean, continuous_ambience boolean, confidence high|medium|low. '
                         'Use under 100 words. This is observation, not approval.'},
                {'inlineData': {'mimeType': 'audio/wav', 'data': base64.b64encode(wav).decode()}}]}],
                'generationConfig': {'temperature': 0, 'responseMimeType': 'application/json',
                                     'maxOutputTokens': 1000, 'thinkingConfig': {'thinkingBudget': 0}}}
            async with semaphore:
                response = await adapter.service.proxy_call(payload, path_model=adapter.default_model)
            provider = target.with_suffix('.provider.json')
            attempt = 1
            while provider.exists():
                attempt += 1
                provider = target.with_suffix(f'.provider-r{attempt:03d}.json')
            provider.write_bytes(response.content)
            if response.status_code >= 400:
                print(f"{row['number']:03d}: HTTP {response.status_code}", flush=True)
                return
            text = ''.join(part.get('text', '') for c in response.json().get('candidates', [])
                           for part in c.get('content', {}).get('parts', []))
            try:
                result['observations'] = json.loads(text)
            except ValueError:
                print(f"{row['number']:03d}: malformed observations", flush=True)
                return
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        print(f"{row['number']:03d}: {result.get('observations', result.get('heard'))}", flush=True)

    try:
        rows = json.loads((OUT / 'baseline.json').read_text())['clips']
        await asyncio.gather(*(inspect(row) for row in rows))
    finally:
        await adapter.service.aclose()

if __name__ == '__main__':
    asyncio.run(main())
