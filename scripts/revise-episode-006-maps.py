#!/usr/bin/env python3
"""Freeze Episode 006's reviewed map redirection and remaining 12-step batch.

Preparation only. The once-only launcher performs the live preflight gate.
"""
import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'episodes/006-shortest-war-ever'
BATCH = EP / 'automation/batches/map-redirection-12step-r005'
POLICY = 'NO BACKGROUND MUSIC. Natural diegetic sound effects only.'
AUTHORITY = 'User explicitly requested a better map method with no people on maps and continuation of the entire remaining batch at the previously requested 12 steps.'
NOW = datetime.now(timezone.utc).isoformat()

def read(p): return json.loads(p.read_text())
def rel(p): return str(p.relative_to(ROOT))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

# Each scene is drawn from a reviewed full-frame physical anchor; no map tokens.
CHANGES = {
 4: ('harbour-intact', 'The cream-robed messenger gives the intact waterfront palace one small glance.', 'a closer crop of the same intact waterfront palace and calm sea'),
 7: ('fleet-quay-five', 'The five existing British hulls stay at their fixed stations, with one restrained water slap at the nearest bow.', 'a closer crop of the nearest existing bow; the other four remain at their original stations outside the crop'),
 12: ('rawson-bridge-over-shoulder', 'Rawson lowers his already pictured binoculars slightly while the intact palace remains quiet across the water.', 'a closer crop of the same officer and intact shore'),
 13: ('harbour-messenger-quay', 'The existing messenger quietly faces the intact shore as the narration introduces its earlier history.', 'a closer crop of the same quay and dhow'),
 16: ('dhow-trade-cargo', 'The existing cargo handler rests one mitten on the already pictured crate, completing one small placement.', 'a closer crop of the same crate and existing rope'),
 17: ('diplomatic-dispatches', 'The navy-coated anonymous official rests one mitten beside his own sealed dispatch; the other official stays seated.', 'a closer crop of the two separate closed dispatches on the same desk'),
 20: ('harbour-intact', 'The messenger remains quietly in place while one small ripple reaches the existing dhow.', 'a closer crop of the same palace with broad water still visible'),
 21: ('british-gun-deck', 'The nearer sailor tightens his existing resting grip on the cannon carriage once; the loaded gun remains completely quiet.', 'a closer crop of the existing cannon barrel and intact palace across water'),
 28: ('market-basket-close', 'The already pictured basket holder makes one small adjustment to the existing basket.', 'a closer crop of the same basket and its holder, preserving the other people outside the crop'),
 30: ('diplomatic-dispatches', 'The charcoal-coated anonymous official nudges his own closed sealed dispatch a few centimetres, then stops; this generic illustration is not a specific treaty meeting.', 'a closer crop of the same two separate sealed dispatches; neither is opened or signed'),
 31: ('messenger-scroll-quay', 'The existing cream-robed messenger steadies his one closed blank scroll while the intact palace stays visible behind him.', 'a closer crop of the closed scroll and same intact palace beyond'),
 33: ('fleet-prebattle', 'All five existing British ships remain at their fixed stations; one small wave meets the nearest bow.', 'a closer crop inside the same composition showing a British hull and intact palace beyond'),
 38: ('khalid-throne-close', 'Khalid turns his head once toward the already pictured throne while holding his same closed scroll; this is the earlier 1893 succession flashback.', 'a closer crop of the same Khalid, closed scroll and throne; intact palace only'),
 40: ('khalid-palace', 'Khalid draws his already held closed scroll a little closer to his chest while the guard stays in place.', 'a closer crop of the same face and closed scroll; the guard remains outside the crop'),
 55: ('rawson-bridge-over-shoulder', 'Rawson looks steadily across the existing open water toward the intact palace without issuing a firing order.', 'a closer crop of the same officer silhouette and visible water gap to the intact palace'),
 64: ('british-gun-deck', 'The nearer sailor rests his mitten on the existing cannon carriage once; its barrel already points toward the intact palace.', 'a closer crop of the existing quiet barrel and the same intact palace beyond'),
 73: ('british-gun-deck', 'The nearer sailor gives one restrained glance across the water, then waits beside the quiet cannon; no fire or signal occurs.', 'a closer crop of the same sailor and loaded but quiet cannon'),
 76: ('rawson-bridge-over-shoulder', 'Rawson watches the intact palace once across the same water, completing one small head turn without a firing signal.', 'a closer crop of the same officer and intact palace; no new viewpoint'),
 85: ('palace-battle', 'One tiny chip drops from an already damaged stone edge; the existing damage and defender identities remain fixed.', 'a closer crop of the same existing damaged masonry'),
 88: ('palace-battle-arcade', 'One existing defender makes one small flinch beside the already chipped arcade, then settles.', 'a closer crop of the same chipped stone and defender; no diagram or projectile path'),
 93: ('glasgow-sinking-start', 'Keep the Glasgow hull afloat without additional settling through 2.84s. From 2.84–4.35s its one existing hull settles modestly lower into the same water, leaving its damaged upper structure visible; hold the resolved lower waterline through 5.00s.', 'one continuous close waterline view with the empty tender at the far right excluded by the initial crop; no crew or drowning people'),
 99: ('khalid-damaged-palace-exit', 'Through 1.18s Khalid holds his closed scroll in place. At 1.18s he makes one restrained head turn toward the right-hand exit, completing by 2.10s. His feet stay INSIDE the palace through the final frame; physical departure belongs to the following clip.', 'one continuous medium view inside the damaged arch; keep the existing two distant defenders and two distant British hulls at their world positions'),
 101: ('consulate-street-approach', 'The existing consulate guard glances once toward Khalid, who waits outside the already open doorway with his same closed scroll.', 'a closer crop of the same open doorway, guard and Khalid; no door-opening action'),
 105: ('palace-surrender-cloth', 'The existing small plain white surrender cloth makes one tiny natural flutter and then settles; it is already attached and is never manufactured, raised or detached.', 'Begin on a tight crop of the existing lower damaged masonry with the white cloth entirely outside the crop. At 0.68s begin one gentle pull-back, finish by 3.50s to reveal the existing white cloth and short pole, then hold through the narrated silence and final frame.'),
 126: ('diplomatic-dispatches', 'Both anonymous officials hold their separate closed dispatches in a quiet earlier-context callback; no new agreement or annexation occurs.', 'a closer crop of the same two closed dispatches, seals and desk as the narration explains accumulated decisions'),
 127: ('harbour-after-arch', 'The two already pictured civilians hold a quiet settled stance as one small water ripple passes the existing wreck.', 'a closer crop of the existing wreck and damaged palace; the civilians stay in their same positions outside the crop'),
}

def main():
    assert not BATCH.exists(), 'A frozen package already exists; do not rebuild after submission.'
    BATCH.mkdir(parents=True)
    direction = read(EP / 'plan/clip-direction.json')
    ledger = read(EP / 'plan/story-state-ledger.json')
    refs = read(EP / 'plan/reference-manifest.json')
    assets = {a['id']: a for a in refs['assets']}
    inventories = {
      'diplomatic-dispatches': 'exactly two anonymous clean-shaven stick officials, navy/gold coat left and charcoal/ochre coat right; exactly two separate closed cream wax-sealed dispatches on a wood desk; background dhows and tiny occupants remain distant',
      'british-gun-deck': 'exactly two foreground British stick sailors in navy coats and white caps, one quiet cannon and timber carriage; the rear sailor has an existing slung long gun; intact palace and tiny distant shore residents; zero other visible warships',
      'glasgow-sinking-start': 'one still-afloat black-and-ochre Glasgow hull, mast, funnel and superstructure; no visible human; already damaged palace and residual smoke; an empty pale tender at the far-right edge stays outside the planned crop',
      'khalid-damaged-palace-exit': 'one foreground Khalid with ivory turban, black beard, maroon/gold robe and one closed scroll inside a damaged palace arch; two small cream-robed defenders behind; two distant British hulls; same damaged palace, existing rubble and smoke',
      'palace-surrender-cloth': 'one damaged palace frontage, one short pole and one existing small plain white cloth tied partway along it; exactly zero people and no ships in the crop; fixed existing roof damage and residual smoke',
    }
    review = []
    for key, inventory in inventories.items():
        path = ROOT / f'assets/episodes/{EP.name}/references/{key}-r001.png'
        item = dict(id=key, type='scene', path=rel(path), sha256=sha(path), status='approved',
                    approved_by='Codex actual full-resolution input-reference review '+NOW,
                    provenance='built-in imagegen; immutable original copied into repository', aspect='16:9',
                    subject_inventory=inventory, story_phase='clip-specific physical scene; see continuity ledger',
                    supported_shot_ids=[], authority_sources=[])
        assets[key] = item
        review.append(dict(asset_id=key, path=rel(path), sha256=sha(path), decision='approved',
                           review_scope='actual scene-anchor pixels, not future H3 motion or SFX', actual_inventory=inventory))
    write(EP / 'plan/map-free-reference-review.json', dict(reviewed_at=NOW, reviewed_by='Codex', assets=review,
          deviations_handled={'gun_deck':'Two foreground sailors plus tiny distant shore residents and one slung gun retained; no firing.',
           'glasgow':'Empty tender at right is excluded by a starting crop; deck crew not visible.',
           'surrender':'White cloth is already attached partway up pole. Use timed camera reveal, not an invented hoist.'}))

    maps = read(EP / 'renders/controlled-maps/manifest-r005.json')
    for m in maps['clips']:
        m.update(review_status='approved', approved_by='Codex actual review of all 120 frames and full-size ending '+NOW,
                 review_scope='zero people, stable geography, frame count, route timing and resolved ending; silent audio verified')
    write(EP / 'renders/controlled-maps/manifest-r005.json', maps)
    write(EP / 'plan/controlled-map-review.json', dict(reviewed_at=NOW, decision='approved', reviewed_by='Codex',
          frames_reviewed=240, evidence='All 120 frames per clip in contact sheets plus full-size ending frames; decoded output and ffprobe streams.',
          people=0, clips=maps['clips']))

    jobplan = read(EP / 'automation/job-plan.json')
    old = read(Path('/tmp/episode006-old-terminal.json'))
    assert all(j['status'] in {'succeeded','cancelled','failed'} for j in old['jobs'])
    succeeded = {int(re.search(r'clip-(\d{3})', j['request']['job_identity']).group(1)): j for j in old['jobs'] if j['status']=='succeeded'}
    retained = set(succeeded) - set(CHANGES) - {14,118}
    assert retained == {1,2,3,5,6,8,9,10,11,15,18,19}
    controlled = {m['number']: m for m in maps['clips']}
    for s in direction['slots']:
        n=s['number']; jp=jobplan['slots'][n-1]; state=ledger['states'][n-1]
        assert n == jp['number'] == state['clip']
        if n in CHANGES:
            key, action, close = CHANGES[n]; a=assets[key]
            s.update(asset_ids=[key], references=[a['path']], action=action,
                     start_inventory=a['subject_inventory'], end_inventory=a['subject_inventory'], method='h3_12_step')
            if n in {93,99,105}:
                s['shots']=[dict(start=0.0,end=5.0,framing=close,camera='one timed pull-back' if n==105 else 'locked',action=action,hold_from=4.35,cut='hard cut at 5.00s')]
            else:
                s['shots']=[dict(start=0.0,end=2.3,framing="the anchor's original composition",camera='locked',action=action+' Complete by 2.10s.',hold_from=2.10,cut='hard cut at 2.30s'),
                             dict(start=2.3,end=5.0,framing=close,camera='locked',action='Hold the already completed action and existing world state; no second action.',hold_from=4.35,cut='hard cut at 5.00s')]
            phase=a['story_phase']
            if n==38: phase='1893 succession flashback; intact palace and no 1896 combat damage'
            if n==126: phase='earlier imperial-context callback; illustrative anonymous officials, not a new postbattle meeting'
            state.update(identity_authority=s['references'], inherited_state=phase, allowed_change=action,
                         resolved_state=a['subject_inventory']+'; action and camera settled by4.35s',
                         subject_count_and_inventory=a['subject_inventory'], reference_asset_id=key, shots=s['shots'])
            jp.update(revision=5, references=s['references'], method='h3_12_step')
            special = ''
            if n in {7,33}:special='Exactly the five pictured British ships stay at their world stations; cropping is not a change in fleet count.'
            if n in {21,64,73,76,55,12}:special+=' This is before first fire: no cannon flash, blast, battle smoke, damage or firing order.'
            if n in {17,30,126}:special+=' Anonymous illustrative officials only; no named historical meeting is asserted and neither scroll is opened or signed.'
            if n==93:special+=' Begin on the specified crop excluding the empty tender. No visible crew, falling people, drowning, new vessel or new explosion. Do not finish fully submerged: clip094 owns the final wreck state.'
            if n==99:special+=' Khalid stays inside the palace until the next clip; do not cross the threshold or show a consulate here.'
            if n==105:special+=' Use the specified tighter starting crop, not the whole reference as the initial framing. The white cloth must remain outside the visible crop until the timed reveal starts; no people enter.'
            timing=' '.join(f"{sh['start']:.2f}–{sh['end']:.2f}s: {sh['framing']}; camera {sh['camera']}. {sh['action']} Hold the resolved state from {sh['hold_from']:.2f}s; {sh['cut']}." for sh in s['shots'])
            sound='one short hull creak, then silence' if key in {'fleet-quay-five','fleet-prebattle','british-gun-deck','glasgow-sinking-start'} else 'one small cloth, water or masonry sound appropriate to the single declared action, then silence'
            if key=='diplomatic-dispatches':sound='one short dry parchment scuff, then silence'
            prompt=f"Create exactly 5.00 seconds of landscape 16:9, 1024×576 animation at 24 fps. <Picture 1> controls the exact scene, identities, props and world positions: {a['subject_inventory']}. Keep the pictured detailed hand-inked ChronoStick world: round off-white heads, black dot eyes, minimal faces, thin dark limbs, mitten hands, bold dark outlines, period clothes and architecture, muted sand/teal/navy/maroon and soft drawn shadows. Preserve all existing subjects and costume cues, coastline, buildings, vessels and their relative positions. A tighter crop leaves subjects in their world positions outside the frame; it never creates, deletes or duplicates them. {timing} {special} Existing weather and lighting remain steady. Existing damage stays fixed except the one explicitly permitted tiny change. All surfaces stay unlettered: no readable words, numbers, labels, maps, chart, captions or added writing. Sound: {sound}. Keep silence between isolated short effects, no sustained ambience or tonal bed. No generated speech, dialogue, narration, vocal reaction, lip sync, photographic surface, collage or new subject. Mouths stay closed. {POLICY}\n"
            assert prompt.count(POLICY)==1
            (EP / f'prompts/clip-{n:03d}.md').write_text(prompt)
            jobpath=EP / f'automation/jobs/clip-{n:03d}.json'; j=read(jobpath)
            j.update(job_identity=f'{EP.name}:clip-{n:03d}:r005', references=[dict(path=a['path'],role='scene',name='Picture 1')])
            j['output']['prefix']=f'clip-{n:03d}-shot-r005'
            write(jobpath,j)
        elif n in controlled:
            m=controlled[n]; a=assets['map-world-blank']
            s.update(method='controlled_geography', asset_ids=['map-world-blank'], references=[a['path']],
                     start_inventory='one fixed empty world chart; exactly zero people, tokens or new labels',
                     end_inventory='same fixed empty chart; zero people; existing pins and Zanzibar ring unchanged',
                     action='Native affine zoom settles by3.50s; hold through5.00s.' if n==14 else 'Broad illustrative Zanzibar-to-nearby-mainland dotted line starts at frame50 and finishes at104; hold through119.')
            s['shots']=[dict(start=0.0,end=5.0,framing='fixed reviewed zero-person chart',camera='native affine zoom' if n==14 else 'locked',action=s['action'],hold_from=3.5 if n==14 else 104/24,cut='hard cut at5.00s')]
            state.update(identity_authority=s['references'],inherited_state=s['start_inventory'],allowed_change=s['action'],resolved_state=s['end_inventory'],subject_count_and_inventory=s['start_inventory'],reference_asset_id='map-world-blank',shots=s['shots'],method='controlled_geography')
            jp.update(revision=5, references=s['references'], method='controlled_geography', artifact=m['path'])
            for p in [EP/f'prompts/clip-{n:03d}.md',EP/f'automation/jobs/clip-{n:03d}.json']:p.unlink()
    # Keep active references and coverage in exact agreement; retire obsolete map-token inputs.
    used={k for s in direction['slots'] for k in s['asset_ids']}
    refs['retired_assets'] += [dict(a,retirement_reason='Map-redirection r005; obsolete anchor preserved immutably') for k,a in assets.items() if k not in used]
    refs['assets']=[assets[k] for k in sorted(used)]
    for a in refs['assets']:a['supported_shot_ids']=[f"clip-{s['number']:03d}" for s in direction['slots'] if a['id'] in s['asset_ids']]
    refs['coverage']=[dict(shot_id=f"clip-{s['number']:03d}",asset_ids=s['asset_ids'],unsupported_elements=[]) for s in direction['slots']]
    for p,d in [('plan/clip-direction.json',direction),('plan/story-state-ledger.json',ledger),('plan/reference-manifest.json',refs),('automation/job-plan.json',jobplan)]:write(EP/p,d)
    previous=read(EP/'plan/map-manifest.json')
    world=next(m for m in previous['maps'] if m['id']=='map-world-blank')
    world.update(supported_shots=['clip-014','clip-118'],render_method='controlled_geography',legend='existing navy/ochre Europe pins and maroon Zanzibar ring only; zero people or character tokens',route_and_arrows='Only118: broad illustrative Zanzibar-to-adjacent-mainland dotted line, not a surveyed itinerary or particular landing port.',zoom_handoff_sequence='014 world-to-East-Africa affine crop; 118 fixed East-Africa crop and one timed dotted line')
    write(EP/'plan/map-manifest.json',dict(schema_version='1.0',family='reviewed-zero-person-parchment',render_method='Bounded Episode006 controlled-map exception only014/118; remaining129 slots are H3 at12steps.',maps=[world],retired_maps=previous['maps'],decision_record=rel(EP/'plan/map-method-decision.md')))
    lines=['# Episode 006 — active map-free direction r005','', '131 five-second slots; 655.000 seconds. Accepted Spanish voice and word timing unchanged. 129 H3 slots at12steps, two controlled geographic inserts with zero people. Ordinary action uses two simple shots; sinking, decision to leave, timed surrender reveal, clocks and quiet passages retain continuous comprehension. See map-method-decision.md.','']
    for s,state in zip(direction['slots'],ledger['states']):
        lines += [f"## Clip {s['number']:03d} · {s['start']:.2f}–{s['end']:.2f}s · {s['chapter_id']}",'',f"Narration: {s['narration']}",'',f"Method: {s.get('method','h3_12_step')}",f"Start: {state['inherited_state']}; {s['start_inventory']}.",f"Action: {s['action']}",f"References in order: {', '.join(s['references'])}."]
        lines += [f"- {sh['start']:.2f}–{sh['end']:.2f}s: {sh['framing']}; {sh['action']} Camera {sh['camera']}; hold from {sh['hold_from']:.2f}s." for sh in s['shots']]
        lines += [f"End: {s['end_inventory']}; settled final frame. Source claim {s['source_claim']}; adaptation {s['reference_analysis_id']}.",'']
    (EP/'plan/shot-plan.md').write_text('\n'.join(lines).rstrip()+'\n')
    episode=read(EP/'episode.json')
    episode.update(active_revision=5,next_action='Run all117 remaining H3 candidates at12steps, then review actual renders before picture selection.',
                   picture_method_exceptions=[dict(number=m['number'],method='controlled_geography',authority=AUTHORITY,
                    decision_record=rel(EP/'plan/map-method-decision.md'),source_reference=m['source_reference'],source_reference_sha256=m['source_sha256'],artifact=m['path'],artifact_sha256=m['sha256'],people=0,review_status='approved',approved_by=m['approved_by']) for m in maps['clips']])
    episode['previous_production_batch']=episode.pop('production_batch')
    episode['production_batch']=dict(steps=12,lightning=False,job_count=117,revision=5,manifest=rel(BATCH/'manifest.json'),status='prepared_not_launched',batch_id=None)
    write(EP/'episode.json',episode)
    settings=read(EP/'automation/batches/production-12step-r004/settings.json');write(BATCH/'settings.json',settings)
    records=[];coverage=[]
    for s in direction['slots']:
        n=s['number']
        if n in controlled:
            coverage.append(dict(number=n,method='controlled_geography',status='reviewed_ready',artifact=controlled[n]['path'],sha256=controlled[n]['sha256']))
            continue
        production=EP/f'automation/jobs/clip-{n:03d}.json';j=read(production)
        if n in retained:
            artifacts=[Path(p) for p in succeeded[n]['output_files'] if p.endswith('.mp4')]
            assert len(artifacts)==2 and all(p.is_file() and p.stat().st_size for p in artifacts)
            coverage.append(dict(number=n,method='h3_12_step',status='retained_candidate_unreviewed',job_id=succeeded[n]['id'],source_batch=old['id'],artifacts=[dict(path=rel(p),sha256=sha(p)) for p in artifacts]))
            continue
        # Cancelled running job may leave an immutable partial output; select another revision.
        revision=jobplan['slots'][n-1]['revision']
        while any(list((ROOT/j['output'][field]).glob(j['output']['prefix']+'*')) for field in ('directory','editorial_directory')):
            revision+=1;j['output']['prefix']=f'clip-{n:03d}-shot-r{revision:03d}';j['job_identity']=f'{EP.name}:clip-{n:03d}:r{revision:03d}'
        jobplan['slots'][n-1]['revision']=revision;write(production,j)
        pp=EP/f'prompts/clip-{n:03d}.md';frozenp=BATCH/f'prompts/clip-{n:03d}.md';frozenp.parent.mkdir(exist_ok=True);frozenp.write_bytes(pp.read_bytes())
        frozenj=BATCH/f'jobs/clip-{n:03d}.json';j['prompt']['file']=rel(frozenp);write(frozenj,j)
        rec=dict(number=n,job=rel(frozenj),job_sha256=sha(frozenj),prompt=rel(frozenp),prompt_sha256=sha(frozenp),production_job=rel(production),production_job_sha256=sha(production),seed=j['generation']['seed'],references=[dict(path=r['path'],sha256=sha(ROOT/r['path'])) for r in j['references']],output_prefix=j['output']['prefix'])
        records.append(rec);coverage.append(dict(number=n,method='h3_12_step',status='prepared_not_launched',job=rec['job'],job_sha256=rec['job_sha256']))
    assert len(records)==117 and len(coverage)==131
    write(EP/'automation/job-plan.json',jobplan)
    manifest=dict(schema_version='1.0',episode_id=EP.name,revision=5,authorization=AUTHORITY,purpose='Complete remaining12-step generation with26 physical map replacements and2 pre-rendered controlled maps',status='prepared_not_launched',batch_id=None,job_count=117,
      generation=dict(steps=12,lightning=False,width=1024,height=576,fps=24,raw_frames=124,editorial_frames=120,editorial_seconds=5),settings=rel(BATCH/'settings.json'),settings_sha256=sha(BATCH/'settings.json'),accepted_voice_sha256=sha(EP/'audio/narration-es-google-vids-r001.mp4'),accepted_timing_sha256=sha(EP/'timestamps/timing-map.json'),jobs=records,timeline_coverage=coverage,retained_candidate_count=12,controlled_map_count=2,final_picture_approved=False)
    write(BATCH/'manifest.json',manifest)
    write(EP/'automation/execution-plan.json',dict(schema_version='2.1',episode_id=EP.name,slot_count=131,h3_12step_count=129,h3_preview_4step_count=0,other_video_methods_count=2,note='User requested12steps without4step pass. Retain12 completed non-map candidates; render117 remaining. Only014/118 use controlled geography with zero people.',production_gate='complete_remaining_live_preflight_required',production_manifest=rel(BATCH/'manifest.json'),production_batch_id=None,production_status='prepared_not_launched',slots=coverage))
    pipe=read(EP/'pipeline-state.json')
    for st in pipe['stages']:
        if st['id'] in {'05','06'}:
            st.update(status='approved',approved_by='Codex actual revised plan and input-reference review '+NOW,decision_notes='Map redirection implemented; all131 timed slots covered with reviewed inputs,26 physical replacements and2 frame-reviewed controlled inserts. User authorized method change and full remaining generation.',next_action='Generate remaining117 clips and review actual motion and SFX.')
        if st['id'] in {'07','08','09'}:
            st.update(status='validated' if st['id'] in {'08','09'} else 'needs_review',approved_by=None,decision_notes='Generation candidates authorized by user before pilot/final-picture approval; revised full planning and live preflight records are required. Actual H3 candidates remain unreviewed.',next_action='Complete remaining generation and actual clip QC.')
        if st['id']=='10':st.update(status='needs_review',approved_by=None,next_action='Review actual clips and approve one immutable candidate per131 slots before assembly.')
    pipe['production_batch']=episode['production_batch'];write(EP/'pipeline-state.json',pipe)
    print(f'Prepared {len(records)} remaining H3 jobs;12 retained candidates and2 controlled maps; {len(refs["assets"])} active reviewed scene references.')

if __name__ == '__main__': main()
