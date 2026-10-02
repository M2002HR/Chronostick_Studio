#!/usr/bin/env python3
"""Rebuild Episode 006 direction from explicit reviewed anchors, without launching H3."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episodes/006-shortest-war-ever"
REF = ROOT / "assets/episodes/006-shortest-war-ever/references"
POLICY = "NO BACKGROUND MUSIC. Natural diegetic sound effects only."


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


BASE = module("episode_direction_base", "build-episode-006-production.py")
JOBS = module("episode_job_builder", "build-longform-jobs.py")

REPLACEMENTS = {
    2: ("shoe-foot-insert", "The held brown shoe lowers toward the unshod foot, then stops while the other shoe stays worn."),
    15: ("dhow-trade-cargo", "The one quay worker lowers his hand onto the existing timber crate beside the tied dhow."),
    23: ("market-basket-close", "The cream-robed trader lowers the existing large shared basket a few centimeters; the other two residents remain sober and still."),
    24: ("dhow-trade-cargo", "The crate, tied dhow and cargo barrels remain at their existing positions as one rope end shifts slightly."),
    26: ("dhow-trade-cargo", "The one quay worker turns his head toward the intact palace beyond the tied dhow."),
    29: ("market-basket-close", "The navy-robed shopper rests one mitten hand on the large basket; the trader and red-shawled resident keep their positions."),
    49: ("messenger-scroll-quay", "The one messenger turns his head toward the intact palace while holding the single closed scroll."),
    52: ("khalid-scroll-insert", "Khalid draws the single closed scroll a little closer to his chest; the one guard remains still behind."),
    57: ("messenger-scroll-quay", "The messenger holds the one closed scroll at chest height and gives the intact palace one expectant glance."),
    65: ("shore-defenders-cannon", "The defender nearest the small shore cannon gives one restrained nod while the second defender and cannon remain still."),
    71: ("khalid-scroll-insert", "Khalid lowers his gaze to the single closed scroll while the one guard remains still."),
    91: ("glasgow-afloat-battle", "The single Glasgow's pictured forward deck gun gives one brief muzzle flash and short recoil; the five existing crew figures remain at their stations."),
    92: ("glasgow-quarter-battle", "The single Glasgow remains afloat in the exact supplied low three-quarter view; the already damaged palace and all five crew remain unchanged."),
    94: ("glasgow-sunken-close", "The already partially submerged Glasgow holds its tilted wreck state as one small outlined water ripple crosses its hull."),
    96: ("glasgow-sunken-close", "The already sunken Glasgow, damaged palace and quiet water remain in their established aftermath state."),
    99: ("map-harbour-table-refuge", "Only the tiny maroon Khalid token slides from the damaged palace up and slightly right along the existing city route to the inland consulate position."),
    100: ("consulate-street-approach", "Khalid takes two short steps screen-right along the pictured approach and stops one pace before the guard at the already open consulate doorway."),
    105: ("map-harbour-table-surrender", "Only the one small plain white surrender cloth rises at the damaged palace; Khalid is already at the inland refuge and every ship stays fixed."),
    110: ("aftermath-quay-detail", "The fallen basket and masonry stay still; the same two distant civilians quietly lower their heads once."),
    114: ("aftermath-quay-detail", "Hold the fallen basket, damaged palace and existing submerged Glasgow in one respectful quiet scene."),
    116: ("harbour-after-arch", "The same two quiet civilians hold beneath the arch while the damaged palace and submerged Glasgow remain unchanged."),
    117: ("hamoud-enthroned", "Hamoud sits on the same throne with his green sash visible and a restrained serious expression."),
    118: ("map-world-khalid-mainland", "Only the existing small maroon Khalid token moves from beside Zanzibar to the adjacent East African mainland shown in the second reference."),
    119: ("hamoud-enthroned", "Hamoud remains seated in the occupied throne, grounding the political result without a new journey."),
    120: ("aftermath-civilians-close", "The same three blue-gray, sand and ochre-clothed residents look quietly toward the damaged waterfront, representing the affected population without depicting an invented abolition ceremony."),
    123: ("shoe-foot-insert", "The one held brown shoe slides onto the unshod foot and settles; both shoes are then worn and no loose shoe remains."),
    127: ("map-harbour-table-surrender", "The resolved surrender chart holds five British ships, sunken Glasgow, damaged palace, one white cloth and Khalid already at inland refuge."),
}
TRANSITIONS = {
    99: ("map-harbour-table-aftermath", "map-harbour-table-refuge", 0.80, 3.80),
    105: ("map-harbour-table-refuge", "map-harbour-table-surrender", 0.80, 3.80),
    118: ("map-world-khalid", "map-world-khalid-mainland", 1.72, 4.35),
}
ACTION_FIXES = {
    1: "The one shoe-searcher takes one startled step toward the doorway, holding one loose brown shoe; his other shoe remains worn.",
    5: "Khalid glances at the existing brass clock once; its blank placard and hand angles stay unchanged.",
    7: "One narrow daylight glint crosses the existing five navy ship tokens; every ship, miniature and coastline stays fixed.",
    13: "One narrow daylight glint catches the existing Zanzibar ring; the entire uncovered chart stays still.",
    16: "One existing dashed Indian Ocean trade route briefly catches a light glint; route geometry remains fixed.",
    17: "The fixed Germany pin catches one brief light glint while the Zanzibar ring and all existing trade paths stay unchanged.",
    22: "The nearest of the five already positioned British hulls rocks once by a few centimeters; the other four retain their positions.",
    30: "The existing Germany pin catches a brief light glint; all diplomatic tokens and other map marks stay fixed.",
    31: "The existing Britain pin catches a brief light glint; the Zanzibar ring and coastline remain fixed.",
    41: "Rawson lowers his gaze to the one paper already in his hands; the same intact shore remains beyond.",
    53: "Khalid steadies the already closed scroll against his chest; its closed physical state stays unchanged.",
    58: "Rawson folds the existing paper once and keeps it in his hand, with no prop transfer to the rail.",
    59: "Khalid gives the existing 08:00 placard one focused glance; both clock hands and every digit remain fixed.",
    61: "The shoe-searcher pauses his existing missing-shoe action and gives his pictured blank wall clock one quick glance.",
    66: "Khalid holds his tense posture beside the brass clock; its blank placard and hand angles remain unchanged.",
    74: "The same blank clock holds its exact existing hand angles while Khalid remains in place.",
    75: "Khalid makes one small hand squeeze; the exact 08:59 placard, clock hands, clear sky and intact harbour stay unchanged.",
    77: "The nearest of the five stationary British bows makes one slight waterline bob, then settles; all five positions remain fixed.",
    79: "The one quay messenger waits beside the existing dhow, looking toward the intact palace; every background silhouette remains unchanged.",
    80: "The clock and Khalid remain still while one isolated tick is heard; the placard stays blank.",
    83: "One localized impact dislodges a small chip from the already damaged palace frontage; the two pictured defenders remain at their positions.",
    84: "The two pictured defenders take one short retreating step together along the already damaged outer arcade.",
    85: "One daylight glint crosses the five existing navy ship miniatures; the already damaged palace and still-afloat Glasgow stay unchanged.",
    86: "The two pictured defenders withdraw one short step along the already damaged wall; existing rubble stays rubble.",
    90: "Khalid turns his head toward the existing harbour once; the exact 09:05 placard and established early-battle background remain unchanged.",
    91: "The single Glasgow's pictured forward deck gun gives one brief muzzle flash and short recoil; the five existing crew figures remain at their stations.",
    93: "The already sunken Glasgow miniature holds its exact tilted state; five navy ship miniatures remain fixed.",
    95: "One small loose stone falls a short distance down the already damaged wall; the two defenders remain still.",
    97: "The existing thin residual plume drifts a few centimeters above the already damaged palace; no new damage occurs.",
    98: "The nearer of the two defenders glances toward the pictured arcade doorway while the second defender remains still.",
    102: "The one neutral guard takes one small step aside at the already open consulate doorway; Khalid waits at the threshold and does not cross during this clip.",
    103: "Khalid stands already inside the consulate doorway and settles his shoulders; the same one guard remains beside him.",
    121: "One short water ripple passes the quiet damaged waterfront; the existing Glasgow wreck and distant British vessel remain unchanged.",
    122: "The shoe-searcher pauses near the doorway with one shoe worn and the matching loose shoe in his hand.",
    125: "The shoe-searcher makes one small eyebrow lift while the exact 38 MINUTOS placard remains steady.",
    130: "The fully shod shoe-searcher stands calmly at the open doorway, holding the existing gentle smile.",
    131: "The fully shod shoe-searcher and the entire doorway composition remain still for the full clip.",
}


def close_crop(key):
    if key == "khalid-balcony-fleet": return "a tighter crop of the same Khalid profile and five distant ships from the same balcony axis; the one guard stays at his established world position outside this crop"
    if key == "hook-shoe-resolved": return "a tighter crop of the same fully shod shoe-searcher at the doorway, both existing shoes worn and no loose shoe"
    if key.startswith("khalid"): return "a tighter crop of the same visible turban, minimal face and scroll; the one background guard may leave the crop but stays at his established world position"
    if key == "rawson-bridge-over-shoulder": return "a tighter crop of the same officer's cap, white beard and single paper already held in the anchor"
    if key == "rawson-bridge": return "a tighter crop of the same officer's cap, white beard and existing binoculars"
    if key.startswith("hamoud"): return "a tighter crop of the same ivory turban, green sash and existing throne arm"
    if key.startswith("market"): return "a closer crop of the same three residents and the large existing basket, keeping all three identities distinguishable"
    if key.startswith("hook-shoe"): return "a closer crop of the same shoe-searcher, his held shoe and doorway; do not show a second copy of him"
    if key == "shoe-foot-insert": return "a closer crop of the same two legs and existing shoe pair, without adding a face outside the anchor"
    if key == "shore-defenders-cannon": return "a closer crop of the same cannon carriage and the nearer pictured defender; the second defender stays at his established world position"
    if key.startswith("glasgow"): return "a tighter crop of the same existing hull, funnel and rigging; vessel geometry and crew/wreck state carry through the cut"
    if key.startswith("fleet"): return "a closer crop of the nearest existing bow and the same shore beyond; other fleet vessels merely leave the crop, never disappear from the harbour"
    if key.startswith("palace-battle"): return "a closer crop of the already pictured damaged arcade and two defenders; existing damage and figure count carry through"
    if key.startswith("consulate"): return "a closer crop of the same Khalid and carved doorway; the one guard keeps his established position"
    if key == "dhow-trade-cargo": return "a closer crop of the existing crate, rope and same worker's stylized hands; preserve the tied dhow and cargo state"
    if key == "messenger-scroll-quay": return "a closer crop of the same messenger's head and single closed scroll, with the same intact palace beyond"
    if key.startswith("empty-throne"): return "a closer crop of the same empty throne back and arm, with exactly zero people"
    return "a closer crop inside the existing anchor, emphasizing its already visible quay, architecture or civilian detail; introduce no unseen object or viewpoint"


def shots(number, key, action):
    if key.startswith(("map-", "clock-")) or number in {94, 96, 110, 111, 113, 131}:
        return [{"start": 0.0, "end": 5.0, "framing": "the exact full-frame anchor viewpoint", "camera": "locked",
                 "action": action, "hold_from": 1.2 if number == 131 else 4.35, "cut": "hard cut at 5.00 only"}]
    split = 2.05 if 82 < number < 99 else 2.30
    return [{"start": 0.0, "end": split, "framing": "the anchor's original composition", "camera": "locked",
             "action": action + f" Complete and settle this single action by {split - 0.20:.2f}s.", "hold_from": split - 0.20, "cut": f"hard cut at {split:.2f}s"},
            {"start": split, "end": 5.0, "framing": close_crop(key), "camera": "locked",
             "action": "Show the already completed action's resulting state; only a tiny eyebrow, cloth or water adjustment already supported by the anchor is allowed.",
             "hold_from": 4.35, "cut": "hard cut at 5.00s"}]


def claim(number):
    return {117: "C019", 118: "C017", 119: "C019"}.get(number, BASE.claim(number))


def main():
    registry = dict(BASE.ASSETS)
    registry["khalid-balcony-fleet"] = ("khalid-balcony-fleet-r001.png", "scene", "exactly one ivory-turbaned maroon Khalid foreground left and one cream-robed guard with maroon fez and one spear at right; exactly five distant British ships, intact harbour and existing small dhows", "palace balcony before the battle")
    for key in ["prebattle", "early-battle", "aftermath", "refuge"]:
        name = "map-harbour-table-" + key
        old = registry[name]
        registry[name] = (f"{name}-r002.png", *old[1:])
    for key, (filename, inventory, phase) in read(EP / "plan/preview-asset-registry.json")["assets"].items():
        registry[key] = (filename, "scene", inventory, phase)
    old_manifest = read(EP / "plan/reference-manifest.json")
    old_plan = read(EP / "automation/job-plan.json")
    reviewed = {(a["id"], a["path"], a["sha256"]): a for a in old_manifest["assets"] if a["status"] == "approved"}
    for a in read(EP / "plan/reference-preview-review.json")["assets"]:
        if a["status"] != "approved" or not a.get("approved_by"):
            raise ValueError("new references require actual review")
        reviewed[(a["id"], a["path"], a["sha256"])] = a
    timing = read(EP / "timestamps/timing-map.json")
    beats = []
    for line in (EP / "plan/beat-cards.tsv").read_text().splitlines():
        n, key, action = line.split("|", 2); n = int(n)
        if n in REPLACEMENTS: key, action = REPLACEMENTS[n]
        elif n in ACTION_FIXES: action = ACTION_FIXES[n]
        beats.append((n, key, action))
    assert [n for n, _, _ in beats] == list(range(1, timing["slot_count"] + 1))
    support = defaultdict(list); coverage = []; states = []; directions = []; jobslots = []
    plan = ["# Episode 006 — revised five-second direction", "", "131 slots, 655.000 seconds; accepted Spanish voice and working word timings remain unchanged. Ordinary scenes use two simple shots in five seconds; maps, exact clock text, quiet human-cost moments and the final settled frame use one continuous shot. The 4-step Lightning preview is a concept review pass; final 12-step rendering remains a later decision.", ""]
    for (n, key, action), slot in zip(beats, timing["slots"], strict=True):
        keys = list(TRANSITIONS[n][:2]) if n in TRANSITIONS else [key]
        refs = [str((REF / registry[k][0]).relative_to(ROOT)) for k in keys]
        for k in keys: support[k].append(n)
        filename, kind, inventory, phase = registry[key]
        start_inventory = registry[keys[0]][2]
        local_shots = shots(n, key, action)
        direction = {"number": n, "start": slot["start"], "end": slot["end"], "chapter_id": slot["chapter_id"],
                     "narration": slot["spoken_text"], "action": action, "asset_ids": keys, "references": refs,
                     "start_inventory": start_inventory, "end_inventory": inventory, "shots": local_shots,
                     "source_claim": claim(n), "reference_analysis_id": BASE.ref_analysis(n)}
        directions.append(direction)
        coverage.append({"shot_id": f"clip-{n:03d}", "asset_ids": keys, "unsupported_elements": []})
        states.append({"shot_id": f"clip-{n:03d}", "clip": n, "global_start": slot["start"], "global_end": slot["end"],
                       "narration_word_ids": slot["word_ids"], "chapter_id": slot["chapter_id"], "source_claim": claim(n),
                       "reference_analysis_id": BASE.ref_analysis(n), "identity_authority": refs,
                       "inherited_state": registry[keys[0]][3], "allowed_change": action,
                       "resolved_state": inventory + "; action and camera settled by 4.35 seconds",
                       "subject_count_and_inventory": start_inventory, "reference_asset_id": key, "shots": local_shots})
        role = " ".join(f"<Picture {i}> controls {'the exact starting scene' if i == 1 else 'only the declared final state'}: {registry[k][2]}." for i, k in enumerate(keys, 1))
        text = (f"Create exactly 5.00 seconds of landscape 16:9, 1024×576 animation at 24 fps. {role} "
                "Use the pictured scene as the literal first frame. Keep every pixel in the same detailed hand-inked ChronoStick world: round off-white heads, black dot eyes, spare stick limbs and mitten hands, bold clean dark outlines, period clothing, muted sand/teal/navy/maroon, soft drawn shadows. "
                f"Initial inventory: {start_inventory}. Preserve visible identities, costume colours, existing props and left/right relationships; a closer crop never creates a new person or removes one from the world. ")
        if key.startswith("map-"):
            text += "The uncovered parchment chart and carved table fill the whole frame continuously. Camera locked at the supplied chart angle; no uncovering reveal, covering fabric, surrounding full-size person or foreground hand. Only a specifically declared route or surrender-flag change is allowed; otherwise every existing map mark stays fixed. Geography, table, compass, pin positions and miniature scale stay exactly as pictured. "
            if key.startswith("map-harbour"):
                text += "Exactly FIVE navy British ship miniatures remain fixed west/left and ONE ochre Glasgow remains east/right in its pictured afloat or sunken state. Rawson remains the one tiny navy figure west. Palace remains east/right in its pictured damage state. "
            else:
                text += "Britain navy pin stays on the British Isles northwest of Europe; Germany ochre pin stays central Europe; Zanzibar maroon ring stays off eastern Africa. No political colour fill or modern border is added. "
            if n in TRANSITIONS:
                _, _, onset, end = TRANSITIONS[n]
                text += f"From 0.00 to {onset:.2f}s hold Picture 1 unchanged. From {onset:.2f} to {end:.2f}s {action} Picture 2 is the destination evidence, not another scene or a duplicate token. Every element except that single declared token/cloth stays fixed. From {end:.2f} to 5.00s hold the exact resulting state, with no additional event. "
                if n == 99:
                    text = text.replace("Every element except that single declared token/cloth stays fixed.", "The only secondary change is revealing Picture 2's already designed short dotted city route directly behind the moving token; no invented route or destination. All ships, geography, Rawson, palace and table stay fixed.")
            else:
                text += f"0.00–0.80s: hold the literal anchor. 0.80–3.50s: {action} 3.50–5.00s: hold the unchanged resolved chart. All character miniatures, vessels and location marks stay fixed. "
        elif key.startswith("clock-"):
            text += "One continuous locked shot, with the same clock left, the same pictured figure or empty floor right, the same room and harbour beyond. The brass clock's existing hand angles and dial marks stay fixed. "
            text += f"0.00–0.80s establish the unchanged scene. 0.80–3.50s: {action} 3.50–5.00s hold the resolved scene. "
        else:
            for s in local_shots:
                text += f"{s['start']:.2f}–{s['end']:.2f}s: {s['framing']}; camera {s['camera']}. {s['action']} Hold settled from {s['hold_from']:.2f}s; {s['cut']}. "
        if n <= 81 and not key.startswith("map-"):
            text += "The pictured clear blue sky, golden cloud shapes, clear air, calm water and intact shore silhouettes remain identical from first to last frame. Only the declared small foreground action changes. "
        elif 82 < n < 106 and not key.startswith("map-"):
            text += "Carry the anchor's exact existing damage, haze and vessel state across every cut; no reversal to an earlier state. "
        if n in BASE.TEXT:
            exact = BASE.TEXT[n][0]
            text += f'The only readable text is exactly "{exact}" on the existing ivory enamel placard, visible from frame one to the final cut. Its letter/digit shapes, colon, spacing, size and placement remain stable in every frame. '
        else:
            text += "All surfaces remain unlettered; no readable letters, digits, labels, captions or added writing. "
        sound = BASE.sfx(key, n)
        if key in {"shoe-foot-insert", "messenger-scroll-quay", "khalid-scroll-insert"}: sound = "one brief shoe or cloth touch tied to the declared action, then silence"
        if key in {"dhow-trade-cargo", "market-basket-close"}: sound = "one brief literal wicker, rope or wood touch, then silence"
        text += f"Sound: {sound}. Keep silence between isolated effects; no sustained ambience or tonal bed. Mouths stay closed and no generated voice, dialogue, narration, vocal reaction, lip sync, photographic surface, montage panel or extra subject appears. {POLICY}\n"
        if text.count(POLICY) != 1: raise ValueError("audio policy repetition")
        (EP / f"prompts/clip-{n:03d}.md").write_text(text)
        previous = old_plan["slots"][n - 1]
        seed = previous.get("seed", read(EP / f"automation/jobs/clip-{n:03d}.json")["generation"]["seed"])
        jobslots.append({"number": n, "revision": 4, "seed": seed, "references": refs})
        plan += [f"## Clip {n:03d} · {slot['start']:.2f}–{slot['end']:.2f}s · {slot['chapter_id']}", "", f"Narration: {slot['spoken_text']}", "", f"Start: {registry[keys[0]][3]}; {start_inventory}.", f"Action: {action}", f"References in order: {', '.join(refs)}."]
        for s in local_shots: plan.append(f"- {s['start']:.2f}–{s['end']:.2f}s: {s['framing']}; {s['action']} Camera {s['camera']}; hold from {s['hold_from']:.2f}s.")
        plan += [f"End: {inventory}; settled final frame. Source claim {claim(n)}; adaptation {BASE.ref_analysis(n)}.", ""]
    assets = []
    for key in sorted(support):
        filename, kind, inventory, phase = registry[key]; path = REF / filename
        signature = (key, str(path.relative_to(ROOT)), digest(path))
        decision = reviewed.get(signature)
        if decision is None: raise ValueError(f"unreviewed current reference: {key}")
        assets.append({"id": key, "type": kind, "path": signature[1], "sha256": signature[2], "status": "approved",
                       "approved_by": decision["approved_by"], "provenance": "built-in imagegen; reviewed immutable full-frame scene",
                       "aspect": "16:9", "subject_inventory": inventory, "story_phase": phase,
                       "supported_shot_ids": [f"clip-{n:03d}" for n in support[key]], "authority_sources": BASE.MAP_SOURCES if key.startswith("map-") else []})
    retired = old_manifest.get("retired_assets", []) + [a for a in old_manifest["assets"] if a["status"] == "rejected"]
    write(EP / "plan/reference-manifest.json", {"schema_version": "1.0", "assets": assets, "coverage": coverage, "retired_assets": retired})
    write(EP / "plan/clip-direction.json", {"schema_version": "1.0", "slots": directions})
    write(EP / "plan/story-state-ledger.json", {"schema_version": "1.0", "states": states})
    (EP / "plan/beat-cards.tsv").write_text("\n".join(f"{n:03d}|{key}|{action}" for n, key, action in beats) + "\n")
    (EP / "plan/shot-plan.md").write_text("\n".join(plan).rstrip() + "\n")
    jobplan = {"schema_version": "1.0", "project_seed": old_plan["project_seed"], "slots": jobslots}
    write(EP / "automation/job-plan.json", jobplan)
    for path, job in JOBS.build(EP, jobplan): write(path, job)
    text_events = read(EP / "plan/text-events.json")
    for event in text_events["events"]: event["reference_asset"] = str((REF / registry[BASE.TEXT[event["clip"]][2]][0]).relative_to(ROOT))
    write(EP / "plan/text-events.json", text_events)
    maps = read(EP / "plan/map-manifest.json")
    maps["render_method"] = "H3-only picture; full 4-step Lightning concept pass before reviewed 12-step production. Stills are generation inputs only."
    existing = {m["id"]: m for m in maps["maps"]}
    new_maps = []
    for key in sorted(k for k in support if k.startswith("map-")):
        item = dict(existing.get(key, existing["map-world-khalid"] if key.startswith("map-world") else existing["map-harbour-table-refuge"]))
        item.update(id=key, asset_path=str((REF / registry[key][0]).relative_to(ROOT)), supported_shots=[f"clip-{n:03d}" for n in support[key]], exact_inventory=registry[key][2])
        if key in {"map-world-khalid", "map-world-khalid-mainland"}: item["depicted_date_or_interval"] = "1893 succession context or later postwar departure, according to the exact slot; mainland departure is broad explanatory geography without exact itinerary"
        new_maps.append(item)
    maps["maps"] = new_maps; write(EP / "plan/map-manifest.json", maps)
    usage = Counter(k for _, k, _ in beats)
    run = best = 0; prior = None
    for _, key, _ in beats: run = run + 1 if key == prior else 1; best = max(best, run); prior = key
    metrics = {"active_anchor_count": len(assets), "primary_anchor_count": len(usage), "max_primary_reuse": max(usage.values()),
               "max_consecutive_primary_slots": best, "unique_primary_anchors_per_60s": [len({k for _, k, _ in beats[i:i+12]}) for i in range(0, len(beats), 12)],
               "shot_count": sum(len(d["shots"]) for d in directions), "per_anchor_slots": {k: sorted(v) for k, v in support.items()}}
    write(EP / "plan/visual-variety-audit.json", metrics)
    print(json.dumps({k: v for k, v in metrics.items() if k != "per_anchor_slots"}))


if __name__ == "__main__":
    main()
