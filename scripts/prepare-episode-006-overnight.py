#!/usr/bin/env python3
"""Prepare the user-authorized input repairs and latest-revision overnight finish."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episodes/006-shortest-war-ever"
RUN = EP / "automation/overnight-finish"
CLI = Path("/home/mhr/AI/comfy-video-automation/.venv/bin/comfy-video")
POLICY = "NO BACKGROUND MUSIC. Natural diegetic sound effects only."

# These are precisely the cases in the input audit just discussed with the user.
CASES = {
    10: ("Exactly five British warships in the pictured arrangement: one large near ship on the left and four smaller ships across the middle distance. Retain the already visible tiny navy deck crew at their pictured positions and scale. Water between the vessels stays open. The intact palace, quay, palm trees, rigging and chain retain their existing shapes.", "A single small outlined ripple passes beside the near hull; the five vessels hold their positions.", "One short water slap at 1.00s, followed by silence."),
    12: ("Exactly one older white-haired, white-bearded naval officer at screen right, viewed from the pictured rear shoulder in the same navy coat and cap. His binoculars remain at their original chest-height position. His visible hands retain their simple mitten silhouettes. The existing paper, railing, distant fleet and intact palace retain their pictured positions and scale.", "The officer makes one slight head inclination toward the distant harbour, then holds; his hands and binoculars remain at rest.", "One short timber creak at 1.00s, followed by silence."),
    17: ("Exactly two seated clean-shaven officials, navy and gold at left, charcoal and ochre at right. Exactly two closed cream dispatch rolls with red wax seals lie on the desk: one in front of each official, separated by the original clear gap. Each roll stays sealed, rigid and in its own place. The two officials' simple cream mitten hands stay in their original resting positions.", "The right official gives one small head inclination toward the left official, then holds. Both sealed rolls remain motionless on the desk.", "Silence throughout."),
    19: ("An unoccupied architectural interior. Exactly one empty blue-and-gold carved throne occupies the right half of the room. The open doorway, wooden lattice, teal hangings, brass lanterns, floor and potted plants retain their pictured arrangement. The entire interior contains zero people.", "The empty room holds its quiet settled state; only one existing plant leaf makes a tiny movement and settles.", "Silence throughout."),
    35: ("An unoccupied architectural interior with exactly one empty ornate blue-and-gold throne at screen right. The open harbour doorway at screen left, patterned stone walls, wooden furniture, teal banners and brass objects retain their original arrangement. The entire interior contains zero people.", "A single existing plant leaf moves slightly and settles while the empty throne remains unchanged.", "Silence throughout."),
    58: ("Exactly one older white-haired, white-bearded Rawson at screen right, viewed from his original rear shoulder, in the same navy coat and cap. The existing cream paper stays in its pictured position on the bridge surface. Both visible hands retain the original simple mitten shapes and resting positions. The distant vessels remain background-sized in the same harbour.", "Rawson makes one small head inclination toward the existing paper, then holds. Paper and hands remain at rest.", "One short wood creak at 1.00s, followed by silence."),
    73: ("Exactly two foreground British sailors, both at screen left, in the original navy coats and white caps. The rear sailor retains his single slung long gun. The nearer sailor rests his simple black mitten hands at the original quiet cannon, on its original wooden carriage. The intact palace and tiny shore residents remain far across the water. Both sailors keep their original positions and silhouettes.", "The nearer sailor gives one tiny head inclination toward the distant palace and settles. The cannon and both sailors' hands remain motionless.", "One short timber creak at 1.00s, followed by silence."),
    93: ("One damaged black-and-ochre Glasgow vessel with its original funnel, two rigged masts and empty visible deck. Preserve the existing small empty tender at far right. The foreground consists entirely of open teal water. The damaged palace and tiny shore silhouettes stay in their original background positions. Visible people on the ship and in the foreground water: zero.", "The single Glasgow hull descends vertically by only about20pixels into the water, retaining rigid proportions and the same horizontal position. Its upper deck, funnel and masts remain visible. The small tender stays fixed at far right. The new lower waterline is held through the last frame.", "One short water slap at 3.20s, followed by silence."),
    94: ("Exactly one already tilted and partially submerged black-and-ochre Glasgow wreck with its original funnel and rigged masts. The deck and foreground water contain zero people. The damaged palace, existing residual smoke and tiny shore residents retain their pictured background positions. The blue daylight sky and bright teal water retain their exact starting brightness and palette throughout.", "One small outlined ripple crosses the hull and settles. The tilted wreck, waterline and daylight remain fixed.", "Silence throughout."),
    95: ("Exactly two cream-robed, ivory-turbaned defenders at the original screen-right arcade opening, each retaining his existing small brown satchel. Their bodies stay in the pictured bent-forward retreat stance with the same original foot positions; this is a tense paused retreat. The damaged stone arcade, palace and distant ship retain their pictured arrangement and scale. Existing background smoke and fire remain confined to their original locations.", "The smaller defender makes one slight head inclination toward his companion, then holds. Their feet, satchels, bodies and screen positions remain at rest.", "One brief distant masonry crack at 1.00s, followed by silence."),
    97: ("Exactly two cream-robed, ivory-turbaned defenders at the original screen-right doorway, each with his original small brown satchel. Preserve their pictured bent-forward retreat stance and original foot positions as a tense paused retreat. The damaged palace, distant single ship, existing splash shapes and background smoke retain their original layout. Existing fire is confined to the pictured battle locations.", "A small upper edge of the existing background smoke drifts slightly and settles. The same pair remain at rest at the doorway with unchanged feet and satchels.", "One brief distant masonry crack at 1.00s, followed by silence."),
    105: ("A full-width landscape view of the already damaged palace. One existing white surrender cloth remains on its original slender pole above the damaged roof near the centre of the picture. Keep the entire original building, roof, blue sky and residual smoke in the same horizontal composition. The cloth is clearly visible from the opening frame. All pictured architecture remains fixed.", "The single white cloth makes one small flutter on its original fixed pole and settles. Its location and the full-width landscape composition remain unchanged.", "Silence throughout."),
    110: ("Exactly two existing civilians together at screen left: the original blue-gray-shawled woman and sand-robed companion. Preserve their visible reference size and original positions, including the clear empty foreground quay to their right. One fallen wicker basket, the rope coil, bollard and masonry pieces keep their original positions. The damaged palace and low warm light remain unchanged.", "The blue-gray-shawled civilian makes one tiny head inclination toward the damaged waterfront, then holds. Both residents' bodies and feet stay at rest.", "Silence throughout."),
    126: ("Exactly two seated clean-shaven officials in the original positions: navy-and-gold official at left, charcoal-and-ochre official at right. Exactly two closed cream dispatch rolls, each with one red wax seal, remain separated on the desk in front of their respective owners. The officials' original simple cream mitten hands remain resting behind those rolls.", "The left official makes one small head inclination toward the right official, then holds. The two sealed rolls retain their exact positions, sizes and closed state.", "Silence throughout."),
}


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if RUN.exists():
        raise SystemExit(f"Already prepared: {RUN}; inspect existing receipt, never resubmit blindly")
    audit = json.loads((EP / "renders/step-comparison-r008/input-audit.json").read_text())
    assert set(CASES) == {v['number'] for v in audit['cases']}
    directions = json.loads((EP / "plan/clip-direction.json").read_text())
    states = json.loads((EP / "plan/story-state-ledger.json").read_text())
    old_batch = EP / "automation/batches/r006-same-seed-20step-r008"
    records = []
    for n, (inventory, action, sound) in sorted(CASES.items()):
        job = json.loads((old_batch / f"jobs/clip-{n:03d}.json").read_text())
        ref = ROOT / job['references'][0]['path']
        assert ref.is_file()
        geometry_style = "Use the anchor's detailed hand-inked architectural and object style, bold clean outlines, muted sand/teal/navy and soft drawn shadows."
        if n not in (19, 35, 93, 94, 105):
            geometry_style += " Preserve the pictured round cream heads, black dot eyes, period costumes and simple mitten hands exactly."
        prompt = (
            "Create exactly 5.00 seconds of landscape 16:9 animation at 1024×576 and 24 fps. "
            "<Picture 1> is the single authority for this scene's composition, visible inventory, identities, object shapes, lighting and illustrated style. "
            + inventory + " " + geometry_style + " "
            "One continuous full-frame view, using the anchor's original viewpoint and framing throughout. Camera locked at its original height and distance. "
            "The illustration fills the complete horizontal frame edge to edge. Preserve the exact pictured foreground/background separation and scale. "
            "0.00–0.80s: hold the original scene and inventory at rest. "
            "0.80–2.00s: " + action + " Complete this one small movement by 2.00s. "
            "2.00–5.00s: hold the resolved scene; objects, characters, camera and lighting remain settled through the last frame. "
            "The same composition and visible inventory persist for all five seconds. No cut, dissolve, new viewpoint, additional subject, extra prop, panel or border. "
            "Keep surfaces unlettered. No readable text, dialogue, narration, vocal reaction or lip sync. "
            "Sound: " + sound + " " + POLICY + "\n"
        )
        settle = 2.0
        if n == 93:
            settle = 4.0
            prompt = prompt.replace('0.00–0.80s:', '0.00–2.84s:').replace('0.80–2.00s:', '2.84–4.00s:').replace('by 2.00s.', 'by 4.00s.').replace('2.00–5.00s:', '4.00–5.00s:')
        assert prompt.count(POLICY) == 1
        assert prompt.count('<Picture 1>') == 1
        frozen = RUN / f"prompts/clip-{n:03d}.md"
        frozen.parent.mkdir(parents=True, exist_ok=True)
        frozen.write_text(prompt)
        (EP / f"prompts/clip-{n:03d}.md").write_text(prompt)
        current = sorted((EP / 'renders/editorial').glob(f'clip-{n:03d}-*-r*.mp4'), key=lambda p: int(re.search(r'-r(\d+)\.mp4$', p.name)[1]))[-1]
        rev = int(re.search(r'-r(\d+)\.mp4$', current.name)[1]) + 1
        prefix = f'clip-{n:03d}-shot-r{rev:03d}'
        assert not list((EP / 'renders').glob(f'*/{prefix}*'))
        seed = int.from_bytes(hashlib.sha256(f'006:input-repair:{n}:r{rev}'.encode()).digest()[:8], 'big') & ((1 << 63) - 1)
        job['prompt'] = {'file': str(frozen.relative_to(ROOT))}
        job['generation'].update(steps=20, seed=seed, seed_mode='fixed', lightning=False, scheduler='simple')
        job['output'].update(prefix=prefix, overwrite=False)
        job['job_identity'] = f'006-shortest-war-ever:clip-{n:03d}:r{rev:03d}:input-repair-20step'
        write(RUN / f'jobs/clip-{n:03d}.json', job)
        shot = dict(start=0.0, end=5.0, framing="the anchor's original continuous full-frame view", camera='locked', action=action, hold_from=settle, cut='hard cut at 5.00s only')
        direction = next(v for v in directions['slots'] if v['number'] == n)
        old = json.loads(json.dumps(direction))
        direction.update(action=action, start_inventory=inventory, end_inventory=inventory, shots=[shot])
        state = next(v for v in states['states'] if v['clip'] == n)
        state.update(allowed_change=action, subject_count_and_inventory=inventory, resolved_state=inventory + f'; camera and action settled by {settle:.2f} seconds', shots=[shot])
        records.append(dict(number=n, revision=rev, seed=seed, hold_from=settle, previous_selected_candidate=str(current.relative_to(ROOT)), previous_direction=old, inventory=inventory, action=action, sound=sound, prompt=str(frozen.relative_to(ROOT)), prompt_sha256=sha(frozen), reference=str(ref.relative_to(ROOT)), reference_sha256=sha(ref), output=str((EP / 'renders/editorial' / f'{prefix}.mp4').relative_to(ROOT)), reference_decision='Actual full-resolution anchor reviewed in the input audit; reuse unchanged and align the shot to it. No new invented angle or incompatible pose.', review_status='input_contract_reviewed_output_pending', final_approval=False))
    write(EP / 'plan/clip-direction.json', directions)
    write(EP / 'plan/story-state-ledger.json', states)
    plan = (EP / 'plan/shot-plan.md').read_text()
    for record in records:
        n = record['number']
        pattern = rf'(## Clip {n:03d} .*?)(?=\n## Clip |\Z)'
        block = re.search(pattern, plan, re.S)[0]
        block = re.sub(r'Method: .*', 'Method: h3_20_step_input_repair', block)
        block = re.sub(r'Start: .*', 'Start: ' + record['inventory'], block)
        block = re.sub(r'Action: .*', 'Action: ' + record['action'], block)
        block = re.sub(r'- 0\.00–.*?(?=\nEnd:)', '- 0.00–5.00s: original full-frame anchor viewpoint; camera locked. ' + record['action'] + f" Settle by {record['hold_from']:.2f}s and hold through the final frame.\n", block, flags=re.S)
        block = re.sub(r'End: .*?(; settled final frame\.)', 'End: ' + record['inventory'] + r'\1', block)
        plan = re.sub(pattern, lambda _: block, plan, flags=re.S)
    (EP / 'plan/shot-plan.md').write_text(plan)
    write(EP / 'plan/overnight-input-repairs.json', {'schema_version': '1.0', 'authorization': 'User explicitly requested correcting prompts and necessary inputs,20step generation, latest-revision selection, concatenation and anime6B upscale in a detached overnight pipeline.', 'scope': sorted(CASES), 'shots': records})
    settings = dict(continue_on_error=True, stop_on_error=False, max_retries=1, concat_on_complete=False, upscale_on_complete=False)
    write(RUN / 'settings.json', settings)
    final_rev = 1
    while list((EP / 'final').glob(f'*-r{final_rev:03d}*')):
        final_rev += 1
    manifest = dict(schema_version='1.0', created_at=datetime.now(timezone.utc).isoformat(), status='prepared', scope=sorted(CASES), job_count=len(CASES), steps=20, sampler='res_multistep', scheduler='simple', lightning=False, seed_policy='New fixed per-clip seeds after correcting trajectories; this is a repair batch, not a same-seed step experiment.', records=records, batch_id=None, selection_policy='User explicitly requests highest numeric completed editorial revision for every slot, not only creatively approved clips. Include controlled geographic slots014/118. Preserve all original candidates.', final_approval=None, final_revision=final_rev, outputs={'picture': f'final/picture-sfx-1024x576-r{final_rev:03d}.mp4', 'upscaled': f'final/picture-sfx-1920x1080-r{final_rev:03d}.mp4', 'distribution': f'final/episode-006-shortest-war-ever-es-1920x1080-r{final_rev:03d}.mp4'}, upscale={'model': '/home/mhr/AI/ComfyUI/models/upscale_models/RealESRGAN_x4plus_anime_6B.pth', 'width':1920, 'height':1080, 'tile':256, 'overlap':32, 'batch_size':8, 'precision':'fp16'}, audio_policy='Preserve native audio in picture/SFX master. Distribution uses accepted Spanish narration only; unreviewed generated native audio is muted to avoid the previously observed generated-speech/music contamination.', generation_failure_policy='Wait until every repair has a terminal outcome. If a new repair fails technically, keep the last existing completed revision and report that fallback; never skip a timeline slot.')
    write(RUN / 'manifest.json', manifest)
    result = subprocess.run([str(CLI), 'batch', '--folder', str(RUN / 'jobs'), '--settings', str(RUN / 'settings.json'), '--dry-run'], cwd=ROOT, capture_output=True, text=True)
    (RUN / 'dry-run.json').write_text(result.stdout)
    (RUN / 'dry-run.stderr').write_text(result.stderr)
    assert result.returncode == 0 and json.loads(result.stdout)['valid'], result.stderr[-2000:]
    manifest['status'] = 'preflight_passed'
    write(RUN / 'manifest.json', manifest)
    episode_path = EP / 'episode.json'
    episode = json.loads(episode_path.read_text())
    episode['overnight_pipeline'] = {'manifest':'automation/overnight-finish/manifest.json', 'status':'preflight_passed', 'steps':20, 'repair_slots':sorted(CASES), 'selection_policy':'highest_completed_revision_per_slot_explicit_user_override', 'final_approval':None}
    episode['next_action'] = 'Detached user-authorized20step input repairs, latest-revision assembly and anime6B1080p narrated export.'
    write(episode_path, episode)
    print(json.dumps({'prepared':len(CASES), 'manifest':str(RUN/'manifest.json')}))


if __name__ == '__main__':
    main()
