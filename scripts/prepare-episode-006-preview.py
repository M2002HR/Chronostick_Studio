#!/usr/bin/env python3
"""Freeze and audit the user-authorized four-step concept batch. Never submits."""
import copy
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'episodes/006-shortest-war-ever'
BATCH = EP / 'automation/batches/preview-4step-r001'
POLICY = 'NO BACKGROUND MUSIC. Natural diegetic sound effects only.'


def load(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-unsubmitted', action='store_true')
    args = parser.parse_args()
    if BATCH.exists():
        prior = load(BATCH / 'manifest.json')
        if not args.refresh_unsubmitted or prior['batch_id'] or prior['status'] != 'prepared_not_launched' or (BATCH / 'submission.json').exists():
            raise ValueError('Submitted/frozen preview cannot be rewritten; increment revision')
    assets = {a['path']: a for a in load(EP / 'plan/reference-manifest.json')['assets']}
    directions = load(EP / 'plan/clip-direction.json')['slots']
    assert len(directions) == 131
    records = []
    seeds = set()
    for n, direction in enumerate(directions, 1):
        assert direction['number'] == n
        shots = direction['shots']
        assert shots[0]['start'] == 0 and shots[-1]['end'] == 5
        assert all(a['end'] == b['start'] for a, b in zip(shots, shots[1:]))
        assert all(s['start'] <= s['hold_from'] < s['end'] for s in shots)
        original = EP / f'automation/jobs/clip-{n:03d}.json'
        job = copy.deepcopy(load(original))
        assert job['generation']['steps'] == 12 and job['generation']['lightning'] is False
        source_prompt = ROOT / job['prompt']['file']
        text = source_prompt.read_text()
        assert text.count(POLICY) == 1 and text.startswith('Create exactly 5.00 seconds')
        assert not re.search(r'(?m)^---|^#|^status:|^approved:', text)
        assert {int(v) for v in re.findall(r'<Picture (\d+)>', text)} == set(range(1, len(job['references']) + 1))
        assert [r['path'] for r in job['references']] == direction['references']
        assert 1 <= len(job['references']) <= 2
        references = []
        for reference in job['references']:
            path = ROOT / reference['path']
            asset = assets[reference['path']]
            assert asset['status'] == 'approved' and asset['approved_by']
            assert sha(path) == asset['sha256']
            references.append({'path': reference['path'], 'sha256': asset['sha256']})
        seed = job['generation']['seed']
        assert seed not in seeds
        seeds.add(seed)
        prompt = BATCH / f'prompts/clip-{n:03d}.md'
        prompt.parent.mkdir(parents=True, exist_ok=True)
        prompt.write_bytes(source_prompt.read_bytes())
        job['prompt']['file'] = str(prompt.relative_to(ROOT))
        job['profile'] = 'draft'
        job['job_identity'] = f'{EP.name}:clip-{n:03d}:preview-4step-r001'
        job['generation'].update(steps=4, lightning=True, megapixel=0.6, width=1024, height=576)
        prefix = f'clip-{n:03d}-preview-4step-r001'
        job['output'].update(directory=str(EP.relative_to(ROOT) / 'renders/preview-4step/raw'),
                             editorial_directory=str(EP.relative_to(ROOT) / 'renders/preview-4step/editorial'), prefix=prefix)
        assert job['output']['overwrite'] is False
        assert job['audio']['enabled'] and job['audio']['mode'] == 'sfx_only'
        assert job['postprocess'] == {'concat': False, 'upscale': False}
        for field in ('directory', 'editorial_directory'):
            assert not list((ROOT / job['output'][field]).glob(prefix + '*'))
        path = BATCH / f'jobs/clip-{n:03d}.json'
        save(path, job)
        records.append({'number': n, 'job': str(path.relative_to(ROOT)), 'job_sha256': sha(path),
                        'prompt': str(prompt.relative_to(ROOT)), 'prompt_sha256': sha(prompt),
                        'production_job': str(original.relative_to(ROOT)), 'production_job_sha256': sha(original),
                        'seed': seed, 'references': references, 'output_prefix': prefix})
    settings = load(EP / 'automation/batch-settings.json')
    assert settings['concat_on_complete'] is False and settings['upscale_on_complete'] is False
    save(BATCH / 'settings.json', settings)
    manifest = {'schema_version': '1.0', 'episode_id': EP.name, 'revision': 1,
                'authorization': 'User explicitly requested all clips as a background 4-step preview on 2026-10-02; stop after verifying start. Later 12-step production requires preview review.',
                'purpose': 'concept and major prompt/reference defect review; no production-quality approval',
                'status': 'prepared_not_launched', 'batch_id': None, 'job_count': 131,
                'generation': {'steps': 4, 'lightning': True, 'width': 1024, 'height': 576, 'fps': 24,
                               'raw_frames': 124, 'editorial_frames': 120, 'editorial_seconds': 5},
                'final_production': {'steps': 12, 'lightning': False, 'revision': 4, 'status': 'prepared_not_launched'},
                'settings': str((BATCH / 'settings.json').relative_to(ROOT)),
                'settings_sha256': sha(BATCH / 'settings.json'),
                'accepted_voice_sha256': sha(EP / 'audio/narration-es-google-vids-r001.mp4'),
                'accepted_timing_sha256': sha(EP / 'timestamps/timing-map.json'), 'jobs': records}
    save(BATCH / 'manifest.json', manifest)
    execution = {'schema_version': '2.1', 'episode_id': EP.name, 'slot_count': 131,
                 'h3_12step_count': 131, 'h3_preview_4step_count': 131, 'other_video_methods_count': 0,
                 'note': 'All picture remains H3-only. New four-step concept package is isolated and frozen. Revised 12-step jobs have not been launched.',
                 'production_gate': 'awaiting_full_preview_review', 'preview_manifest': str((BATCH / 'manifest.json').relative_to(ROOT)),
                 'superseded_pilot_batch': 'a8fd33bf-eb25-4f44-b36f-b18b6c8e0a7b',
                 'slots': [{'number': r['number'], 'method': 'h3_12_step', 'job': r['production_job'],
                            'job_sha256': r['production_job_sha256'], 'status': 'prepared_not_launched',
                            'preview_job': r['job']} for r in records]}
    save(EP / 'automation/execution-plan.json', execution)
    print(f'Frozen and statically audited {len(records)} preview jobs: {BATCH}')


if __name__ == '__main__':
    main()
