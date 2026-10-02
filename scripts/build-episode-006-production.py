#!/usr/bin/env python3
"""Materialize the reviewed Episode 006 beat cards into production ledgers and H3 prompts."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episodes/006-shortest-war-ever"
REFDIR = ROOT / "assets/episodes/006-shortest-war-ever/references"
POLICY = "NO BACKGROUND MUSIC. Natural diegetic sound effects only."
GEO = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson"
MAP_SOURCES = [
    GEO,
    "https://www.loc.gov/resource/g8440.ct003505/",
    "https://germanhistorydocs.org/en/wilhelmine-germany-and-the-first-world-war-1890-1918/ghdi%3Adocument-782",
    "https://brema.suub.uni-bremen.de/dsdk/content/pagetext/1788980",
    "https://whc.unesco.org/en/list/173",
]

# Foreground inventory is descriptive rather than a request for new people.
ASSETS = {
    # All selected map and clock references are full-frame physical scenes.
    # H3 generates every moving frame; these stills are input anchors only.
    "map-world-blank": ("map-world-blank-r001.png", "scene", "one physical illustrated world chart; Britain navy pin, Germany ochre pin, Zanzibar maroon ring; zero people", "1890–1896 world geography before Khalid enters the story"),
    "map-world-oblique": ("map-world-oblique-r001.png", "scene", "same physical illustrated world chart from a lower table angle; Britain navy pin, Germany ochre pin, Zanzibar maroon ring off northern Tanzania; zero people", "1890–1896 world geography before Khalid enters the story"),
    "map-world-trade-blank": ("map-world-trade-blank-r001.png", "scene", "same world chart and pins; three dashed Indian Ocean routes ending at Zanzibar; zero people", "1890–1896 Indian Ocean trade context"),
    "map-world-khalid": ("map-world-table-r001.png", "scene", "same world chart and pins; one tiny maroon Khalid token beside Zanzibar", "world geography after Khalid is introduced"),
    "map-harbour-table-prebattle": ("map-harbour-table-prebattle-r001.png", "scene", "same physical harbour chart; five navy British ship tokens west/left, one ochre Glasgow east/right, Rawson west, Khalid at intact palace east", "27 August 1896 before 09:00"),
    "map-harbour-table-early-battle": ("map-harbour-table-early-battle-r001.png", "scene", "same harbour chart; five British ships west/left, Glasgow still afloat east/right, damaged palace east/right", "27 August 1896 after first fire but before Glasgow sinks"),
    "map-harbour-table-aftermath": ("map-harbour-table-aftermath-r001.png", "scene", "same harbour chart; five British ships in fixed west/left positions, tilted sunken Glasgow, damaged palace east/right, Khalid token at palace until refuge", "27 August 1896 after Glasgow sinks"),
    "map-harbour-table-refuge": ("map-harbour-table-refuge-r001.png", "scene", "same harbour chart; five British ships west/left, sunken Glasgow, damaged palace east/right, maroon Khalid token at inland consular refuge gate", "27 August 1896 after Khalid leaves the palace"),
    "clock-palace-blank": ("clock-palace-blank-r001.png", "scene", "one large brass analog clock with blank ivory placard; one Khalid in maroon; intact harbour beyond", "before battle, without duration reveal"),
    "clock-aftermath-blank": ("clock-aftermath-blank-r002.png", "scene", "one large brass analog clock with blank ivory placard; zero people; damaged harbour beyond", "sober human-cost passage after battle, before duration reveal"),
    "clock-palace-0800": ("clock-palace-0800-r001.png", "scene", "one clock and exact enamel text 08:00; one Khalid; intact harbour", "08:00 ultimatum in physical palace scene"),
    "clock-palace-0859": ("clock-palace-0859-r001.png", "scene", "one clock and exact enamel text 08:59; one Khalid; intact harbour", "08:59 final prebattle minute in physical palace scene"),
    "clock-palace-0900": ("clock-palace-0900-r001.png", "scene", "one clock and exact enamel text 09:00; one Khalid; intact harbour at firing onset", "09:00 first fire in physical palace scene"),
    "clock-palace-0905": ("clock-palace-0905-r002.png", "scene", "one clock and exact enamel text 09:05; one Khalid; early battle smoke beyond; Glasgow afloat", "09:05 Glasgow beat in physical palace scene"),
    "clock-aftermath-0938": ("clock-aftermath-0938-r001.png", "scene", "one clock and exact enamel text 09:38; one shoe-searcher; damaged palace and sunken Glasgow beyond", "09:38 delayed answer after battle"),
    "clock-aftermath-38-minutos": ("clock-aftermath-38-minutos-r001.png", "scene", "one clock and exact enamel text 38 MINUTOS; one shoe-searcher; damaged palace and sunken Glasgow beyond", "duration reveal after battle"),
    "hook-shoe": ("hook-shoe-r001.png", "scene", "one foreground shoe-searcher in brown jacket and cream trousers; one bedroom, one missing shoe", "comic Zanzibar morning"),
    "hook-shoe-resolved": ("hook-shoe-resolved-r001.png", "scene", "the same one foreground shoe-searcher in brown jacket and cream trousers, now wearing both brown shoes; the same bedroom and doorway", "comic settled closing state"),
    "harbour-intact": ("harbour-intact-r001.png", "world", "one foreground cream-robed messenger; one intact Sultan's waterfront palace; one dhow; tiny distant residents", "intact western Stone Town waterfront"),
    "khalid-palace": ("khalid-palace-focused-r001.png", "scene", "one foreground Khalid with ivory turban, black beard and maroon gold-trimmed robe; one secondary guard; one throne and scroll", "intact palace chamber before battle"),
    "rawson-bridge": ("rawson-bridge-focused-r001.png", "scene", "one foreground older Rawson with white beard, dark navy officer coat, gold shoulder boards, peaked cap and binoculars", "British ship bridge facing intact palace"),
    "hamoud-council": ("hamoud-council-r001.png", "scene", "one foreground Hamoud with dark beard, ivory turban and deep-green sash; one ornate throne", "Zanzibari council chamber"),
    "hamoud-enthroned": ("hamoud-enthroned-r001.png", "scene", "one foreground Hamoud with dark beard, ivory turban and deep-green sash seated on the ornate throne", "postbattle Zanzibari council chamber"),
    "empty-throne": ("empty-throne-r001.png", "scene", "one empty ornate blue-and-gold throne in the same council chamber; exactly zero people", "Zanzibari council chamber before successor is named"),
    "market": ("market-r001.png", "world", "three prominent local stick-figure residents, wicker baskets, shaded market stalls, one distant dhow", "Stone Town market before battle"),
    "fleet-prebattle": ("fleet-prebattle-r001.png", "vessel", "exactly five distinct British warships across the water; intact palace in distance", "prebattle harbour, fleet west of palace"),
    "glasgow-afloat": ("glasgow-afloat-r002.png", "vessel", "one intact Glasgow warship with a few tiny cream-robed Zanzibar crew figures and no flags; intact shore", "Zanzibar harbour before sinking"),
    "palace-battle": ("palace-battle-r001.png", "scene", "one damaged Sultan's waterfront palace, controlled smoke, two retreating stick defenders, one distant British warship", "battle already in progress"),
    "consulate-refuge": ("consulate-refuge-r001.png", "scene", "one Khalid in ivory turban and maroon robe, one neutral consular guard, one consulate gate", "Stone Town German consulate refuge"),
    "harbour-after": ("harbour-after-r001.png", "scene", "two quiet foreground civilians, damaged palace, one partially submerged Glasgow and one distant British ship", "settled aftermath"),
    "aftermath-civilians": ("aftermath-civilians-r001.png", "scene", "exactly three local stick civilians: older woman in blue-gray shawl left, young man in sand robe center, woman in ochre shawl right; damaged palace behind", "human aftermath on the Stone Town quay"),
    "khalid-throne-close": ("khalid-throne-close-r001.png", "scene", "one Khalid in ivory turban and maroon gold-trimmed robe, one guard, same throne and scroll in closer palace view", "intact palace chamber before battle"),
    "khalid-balcony-fleet": ("khalid-balcony-fleet-r001.png", "scene", "one Khalid viewed from palace balcony, exactly five British ships offshore; intact prebattle harbour", "27 August 1896 before 09:00"),
    "market-quay": ("market-quay-r001.png", "scene", "same three prominent local residents as market, baskets and quay from a different eye-level angle", "Stone Town market before or after battle, with matching palace state"),
    "empty-throne-door": ("empty-throne-door-r001.png", "scene", "same empty ornate throne seen through council-room doorway; zero people", "Zanzibari council chamber before successor is named"),
    "map-world-diplomacy": ("map-world-diplomacy-r001.png", "scene", "same physical world chart and fixed Britain, Germany, Zanzibar locations; two small neutral diplomat tokens in Europe; no Khalid token", "1890s British-German diplomatic context, not human travel"),
    "fleet-quay-five": ("fleet-quay-five-r001.png", "scene", "exactly five British ships in a low quay-level view and intact distant palace", "prebattle harbour, five British ships west of palace"),
    "palace-battle-arcade": ("palace-battle-arcade-r001.png", "scene", "damaged palace side arcade, two retreating defenders, one distant British ship", "27 August 1896 battle in progress"),
    "harbour-messenger-quay": ("harbour-messenger-quay-r001.png", "scene", "one cream-robed messenger by the intact waterfront palace and one dhow, seen from quay level", "intact Stone Town waterfront before battle"),
    "harbour-after-arch": ("harbour-after-arch-r001.png", "scene", "two quiet civilians beneath Stone Town arch, damaged palace and sunken Glasgow beyond", "settled aftermath"),
    "rawson-bridge-over-shoulder": ("rawson-bridge-over-shoulder-r001.png", "scene", "same older white-bearded Rawson in dark navy uniform on ship bridge seen over his shoulder; prebattle fleet and intact palace", "British ship bridge before 09:00"),
    "glasgow-stern": ("glasgow-stern-r001.png", "scene", "one intact Glasgow ship with few cream-robed crew, seen from low stern-quarter angle; no other warship", "pre-sinking Zanzibar harbour"),
    "consulate-inside": ("consulate-inside-r001.png", "scene", "same maroon-robed Khalid and one neutral guard inside consulate doorway; damaged palace visible outside", "Khalid safely inside Stone Town German consulate after escape"),
    "aftermath-civilians-close": ("aftermath-civilians-close-r001.png", "scene", "same three Zanzibari residents in blue-gray, sand and ochre clothing, closer quay view, damaged palace and sunken Glasgow", "respectful human aftermath"),
    "map-east-africa": ("map-east-africa-r001.png", "map", "fixed East African coastline, Indian Ocean, Zanzibar marker; zero people", "regional geographic map"),
    "map-trade-routes": ("map-trade-routes-r001.png", "map", "same coastline and Zanzibar marker with three pale converging routes; zero people", "regional trade-route map"),
    "map-zanzibar-coast": ("map-zanzibar-coast-r001.png", "map", "same mainland and Unguja coast; one tiny stick figure near the Zanzibar marker", "coastal map"),
    "map-zanzibar-island": ("map-zanzibar-island-r001.png", "map", "Unguja island silhouette and Zanzibar marker; zero people", "island map"),
    "map-harbour-prebattle": ("map-harbour-prebattle-r001.png", "map", "schematic west/left water, east/right palace, exactly five British ship icons and one separate Glasgow icon", "intact harbour tactical diagram"),
    "map-harbour-first-fire": ("map-harbour-first-fire-r001.png", "map", "same fixed six ship icons and palace, one British-to-shore trajectory", "first-fire tactical diagram"),
    "map-harbour-glasgow-sunk": ("map-harbour-glasgow-sunk-r001.png", "map", "same five British icons, one submerged Glasgow icon, damaged-palace direction", "Glasgow-sunk tactical diagram"),
    "map-harbour-refuge": ("map-harbour-refuge-r001.png", "map", "same six ship icons and palace; one tiny maroon stick icon and inland refuge arrow", "Khalid refuge tactical diagram"),
    "map-harbour-surrender": ("map-harbour-surrender-r001.png", "map", "same fixed ship positions, one white surrender signal at palace", "surrender tactical diagram"),
    "clock-0800": ("clock-0800-r001.png", "text", "one analog clock and exact text 08:00", "08:00 ultimatum card"),
    "clock-0859": ("clock-0859-r001.png", "text", "one analog clock and exact text 08:59", "08:59 suspense card"),
    "clock-0900": ("clock-0900-r001.png", "text", "one analog clock and exact text 09:00", "09:00 first-fire card"),
    "clock-0905": ("clock-0905-r001.png", "text", "one analog clock and exact text 09:05", "09:05 Glasgow card"),
    "clock-0938": ("clock-0938-r001.png", "text", "one analog clock and exact text 09:38", "09:38 reveal card"),
    "clock-38-minutos": ("clock-38-minutos-r002.png", "text", "one analog clock and exact text 38 MINUTOS", "duration reveal card"),
    "clock-face-0859": ("clock-face-0859-r001.png", "clock", "one analog clock with hands at 08:59 and no readable numerals or letters", "unlabelled pre-deadline clock"),
    "clock-face-0800": ("clock-face-0800-r001.png", "clock", "one analog clock with hands at 08:00 and no readable numerals or letters", "unlabelled ultimatum clock"),
    "clock-face-0900": ("clock-face-0900-r001.png", "clock", "one analog clock with hands at 09:00 and no readable numerals or letters", "unlabelled first-fire clock"),
    "clock-face-0905": ("clock-face-0905-r001.png", "clock", "one analog clock with hands at 09:05 and no readable numerals or letters", "unlabelled Glasgow clock"),
    "clock-face-0938": ("clock-face-0938-r001.png", "clock", "one analog clock with hands at 09:38 and no readable numerals or letters", "unlabelled reflective clock"),
}

TEXT = {
    8: ("08:59", "C012", "clock-palace-0859", 0.0, 4.8),
    59: ("08:00", "C012", "clock-palace-0800", 0.0, 4.8),
    60: ("08:00", "C012", "clock-palace-0800", 0.0, 4.8),
    75: ("08:59", "C012", "clock-palace-0859", 0.0, 4.8),
    82: ("09:00", "C012", "clock-palace-0900", 0.0, 4.8),
    90: ("09:05", "C014", "clock-palace-0905", 0.0, 4.8),
    124: ("09:38", "C015", "clock-aftermath-0938", 0.0, 4.8),
    125: ("38 MINUTOS", "C015", "clock-aftermath-38-minutos", 0.0, 4.8),
}
TEXT_START = {}
MAP_TRANSITIONS = {}


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phase(n: int):
    if n <= 13: return "1896 opening flash-forward; palace and Glasgow intact"
    if n <= 35: return "background geography and imperial context before 1896 battle"
    if n <= 43: return "1893 succession flashback; no 1896 combat damage"
    if n <= 74: return "27 August 1896 before 09:00; palace and Glasgow intact"
    if n <= 81: return "27 August 1896 final prefire minute; all ships and palace intact"
    if n == 82: return "27 August 1896 at exactly 09:00; first fire begins after the intact prebattle minute"
    if n <= 92: return "27 August 1896 bombardment under way; palace smoke accumulates, Glasgow afloat until its sinking"
    if n <= 96: return "27 August 1896 after Glasgow sinks; palace damaged"
    if n <= 105: return "27 August 1896 battle end; Khalid reaches consulate before surrender"
    if n <= 121: return "settled aftermath and political consequences"
    return "comic framing and final 38-minute payoff after the human-cost passage"


def claim(n: int):
    if n <= 13: return "C012"
    if n <= 16: return "C003"
    if n <= 35: return "C007"
    if n <= 51: return "C010"
    if n <= 81: return "C012"
    if n <= 96: return "C014"
    if n <= 109: return "C017"
    if n <= 117: return "C016"
    if n <= 121: return "C019"
    return "C015"


def ref_analysis(n: int):
    if n <= 13: return "RV01" if n <= 3 else "RV07"
    if n <= 21: return "RV02"
    if n <= 35: return "RV03"
    if n <= 51: return "RV06"
    if n <= 58: return "RV05"
    if n <= 74: return "RV07"
    if n <= 81: return "RV07"
    if n <= 96: return "RV08"
    if n <= 105: return "RV09"
    if n <= 121: return "RV08"
    return "RV10"


def sfx(key: str, n: int):
    if n == 82: return "one distant isolated cannon crack at 2.70 seconds, then silence"
    if key.startswith("map-"): return "one dry paper/map rustle, then silence"
    if key.startswith("clock-"): return "one isolated mechanical tick, then silence"
    if key == "hook-shoe": return "one light shoe scuff or jacket swish, then silence"
    if key in {"khalid-palace", "khalid-throne-close", "khalid-balcony-fleet", "hamoud-council"}: return "one soft cloth or parchment movement, then silence"
    if key in {"market", "market-quay"}: return "one basket or footstep sound, then silence"
    if key in {"fleet-prebattle", "fleet-quay-five", "glasgow-afloat", "glasgow-stern", "rawson-bridge", "rawson-bridge-over-shoulder"}: return "one short hull creak or water slap, then silence"
    if key in {"palace-battle", "palace-battle-arcade"}: return "one distant cannon crack or masonry impact, then silence"
    if key in {"consulate-refuge", "consulate-inside"}: return "one stone footstep or wooden gate click, then silence"
    if key in {"harbour-after", "harbour-after-arch"}: return "one quiet water lap, then silence"
    if key in {"aftermath-civilians", "aftermath-civilians-close"}: return "one soft cloth movement or harbour water lap, then silence"
    return "silence"


def framing(key: str, n: int):
    if key.startswith("map-"): return "near-top-down view of one physical parchment chart on the same carved table; coastline and pin or token positions remain fixed"
    if key == "clock-aftermath-blank": return "one continuous quiet room, ornate brass clock left, empty floor right, damaged harbour visible beyond"
    if key.startswith("clock-"): return "one continuous palace room, ornate brass clock left and one stick character right, harbour visible beyond"
    if key == "khalid-palace": return "medium palace interior from eye height, Khalid foreground left and one guard behind center"
    if key == "khalid-throne-close": return "tight palace interior from eye height, Khalid foreground with scroll and one guard behind beside the throne"
    if key == "khalid-balcony-fleet": return "over-the-shoulder palace balcony view, Khalid foreground and five intact British ships across water"
    if key == "rawson-bridge": return "medium ship-bridge view from eye height, Rawson foreground left, intact palace across water right"
    if key == "rawson-bridge-over-shoulder": return "over-the-shoulder ship-bridge view, Rawson foreground right, intact palace across water left"
    if key == "hamoud-council": return "medium wide council room from eye height, Hamoud left of the carved throne"
    if key == "hamoud-enthroned": return "medium wide council room from eye height, Hamoud seated centrally on the carved throne"
    if key == "empty-throne": return "medium wide council room from eye height, one empty carved throne center-right and no person"
    if key == "empty-throne-door": return "medium wide view through the council-room doorway, same empty carved throne deeper in frame and no person"
    if key == "market": return "wide market view from eye height, three foreground residents separated across the quay"
    if key == "market-quay": return "lower eye-level quay market view, three familiar residents and baskets in a new depth arrangement"
    if key in {"hook-shoe", "hook-shoe-resolved"}: return "medium wide bedroom doorway view from eye height, one shoe-searcher at frame right"
    if key == "harbour-intact": return "wide harbour-level view, intact palace center-right, teal water foreground, messenger at left"
    if key == "harbour-messenger-quay": return "eye-level quay view, intact palace beyond and one cream-robed messenger foreground"
    if key == "fleet-prebattle": return "wide harbour-level view, five ships spaced left-to-right with palace beyond"
    if key == "fleet-quay-five": return "low quay-level diagonal view, exactly five British ships at distinct distances and intact palace beyond"
    if key == "glasgow-afloat": return "medium wide harbour-level view, one Glasgow vessel clearly separated from the distant fleet"
    if key == "glasgow-stern": return "low stern-quarter harbour view, one intact Glasgow vessel isolated against the intact Stone Town shore"
    if key == "palace-battle": return "wide harbour-level view, damaged palace center-right and retreating defenders at safe distance"
    if key == "palace-battle-arcade": return "medium side-arcade view of damaged palace, two defenders retreating along the wall"
    if key == "consulate-refuge": return "medium street-height view, Khalid left approaching the consulate gate right"
    if key == "consulate-inside": return "medium interior consulate view, Khalid and one guard under the arched gateway, damaged harbour outside"
    if key == "aftermath-civilians": return "medium wide eye-height quay view, three distinct civilians left, center and right against the damaged palace"
    if key == "aftermath-civilians-close": return "medium close eye-height quay view, same three civilians gathered by a fallen basket with distant damage"
    if key == "harbour-after-arch": return "quiet medium wide view through Stone Town arch, two civilians and damaged harbour beyond"
    return "wide quiet harbour-level view, damage and the submerged Glasgow remain in their aftermath positions"


def make():
    timing = json.loads((EP / "timestamps/timing-map.json").read_text())
    previous_manifest = EP / "plan/reference-manifest.json"
    reviewed = {}
    if previous_manifest.is_file():
        for item in json.loads(previous_manifest.read_text()).get("assets", []):
            if item.get("status") == "approved" and item.get("approved_by"):
                reviewed[(item.get("id"), item.get("path"), item.get("sha256"))] = item["approved_by"]
    beats = []
    for line in (EP / "plan/beat-cards.tsv").read_text().splitlines():
        n, key, action = line.split("|", 2)
        beats.append((int(n), key, action))
    if len(beats) != timing["slot_count"] or [b[0] for b in beats] != list(range(1, timing["slot_count"] + 1)):
        raise ValueError("beat cards must cover exactly the 131 ordered slots")
    used = {b[1] for b in beats} | set(TEXT_START.values()) | {value[0] for value in MAP_TRANSITIONS.values()}
    missing = [ASSETS[key][0] for key in used if not (REFDIR / ASSETS[key][0]).is_file()]
    if missing:
        raise FileNotFoundError("Missing scene anchors: " + ", ".join(missing))
    for n, (text, _, key, _, _) in TEXT.items():
        if beats[n-1][1] != key: raise ValueError(f"clip {n} text anchor mismatch")
    assets = []
    coverage = []
    byasset = defaultdict(list)
    for n, key, _ in beats:
        byasset[key].append(n)
        if n in TEXT_START: byasset[TEXT_START[n]].append(n)
        if n in MAP_TRANSITIONS: byasset[MAP_TRANSITIONS[n][0]].append(n)
    for key in sorted(used):
        filename, kind, inventory, phase_desc = ASSETS[key]
        path = REFDIR / filename
        approval = reviewed.get((key, str(path.relative_to(ROOT)), sha(path)))
        assets.append({"id": key, "type": kind, "path": str(path.relative_to(ROOT)), "sha256": sha(path),
                       "status": "approved" if approval else "visual_review_required", "approved_by": approval,
                       "provenance": "built-in image_gen full-frame physical scene anchor" if key.startswith(("map-", "clock-")) else "built-in image_gen artwork or reviewed crop",
                       "aspect": "16:9", "subject_inventory": inventory, "story_phase": phase_desc,
                       "supported_shot_ids": [f"clip-{n:03d}" for n in byasset[key]],
                       "authority_sources": MAP_SOURCES if key.startswith("map-") else []})
    text_events=[]
    for n, (label, cid, key, on, hold) in sorted(TEXT.items()):
        text_events.append({"clip":n,"exact_text":label,"claim_id":cid,
                            "source":"source/reference-video/the-shortest-war-ever-transcript.txt; user-authorized source-assumption basis in source/research-waiver.json",
                            "onset_seconds":on,"hold_until_seconds":hold,"exit_seconds":5.0,
                            "placement":"one large enamel placard beneath the physical brass clock inside the continuous illustrated scene; visible from frame one",
                            "reference_asset":str((REFDIR/ASSETS[key][0]).relative_to(ROOT)),
                            "status":"requested_by_user_pending_render_review","approved_by":"user for concept and source-assumption basis",
                            "failure_conditions":["wrong digit or accent", "flicker or morph", "extra readable text", "unreadable at phone size"]})
    write_json(EP/"plan/text-events.json",{"schema_version":"1.0","events":text_events})
    maps=[]
    for key in sorted(k for k in used if k.startswith("map-")):
        filename, _, inventory, phase_desc=ASSETS[key]
        is_world=key.startswith("map-world")
        maps.append({"id":key,"depicted_date_or_interval":"1890–1896 context" if is_world else "27 August 1896",
                     "extent_and_scale":"whole world from British Isles and Germany to eastern Africa, Indian Ocean and Zanzibar" if is_world else "schematic Stone Town west waterfront and Zanzibar harbour on a physical chart table",
                     "political_status":"Zanzibar shown as a British protectorate with a local sultan; pins indicate influence, never annexation, colony fill or modern borders",
                     "source_urls":MAP_SOURCES,"coastline_authority":GEO if is_world else "schematic tactical layout informed by contemporary Zanzibar map; ship bearings and consulate path are explanatory, not surveyed coordinates",
                     "legend":"teal sea; sand land; navy Britain and five British vessels; ochre Germany or Glasgow; maroon Zanzibar focus and Khalid token; white surrender cloth only after battle",
                     "route_and_arrows":"world trade routes are broad Indian Ocean exchange corridors, not individual documented voyages; Khalid moves only Zanzibar-to-nearby refuge and later Zanzibar-to-mainland German East Africa; no London-to-Zanzibar character journey",
                     "allowed_labels":[],"zoom_handoff_sequence":"world geography and Britain/Germany/Zanzibar pins → physical harbour tactical chart → world summary; stable table, palette and character token design",
                     "supported_shots":[f"clip-{n:03d}" for n in byasset[key]],
                     "asset_path":str((REFDIR/filename).relative_to(ROOT)),
                     "failure_conditions":["Britain, Germany or Zanzibar moves to a wrong continent", "world coastline changes between shots", "harbour east/west flips", "a sixth British ship appears", "Glasgow sinks before 09:05 or resurrects afterward", "Khalid returns to palace after refuge", "unlisted writing appears"]})
    write_json(EP/"plan/map-manifest.json",{"schema_version":"1.0","family":"physical-ink-sand-teal-world-to-harbour-1896","render_method":"Every five-second map clip is generated entirely by H3 at 12 steps; still charts are reference images only.","maps":maps})
    plan=["# Episode 006 — exact five-second shot plan", "", "Source of time: accepted 651.389388-second Spanish Google Vids audio and corrected provider working CSV. Picture runs to 655.00 seconds. The last 3.68 seconds are a resolved silent hold. Every shot uses one full-frame anchor and one principal action. `beat-cards.tsv` is the concise editable source; this file expands it with timing and production state.", "", "## Sequence grammar", "", "C01 question → C02 place → C03 succession → C04 ultimatum → C05 battle → C06 surrender → C07 cost and delayed 38-minute answer. The reference-video adaptation IDs below refer to `reference-video-analysis.md`. Map geometry, ship count and cardinal layout never flip. All generated writing is restricted to `text-events.json`.", ""]
    states=[]; jobslots=[]
    for (n,key,action),slot in zip(beats,timing["slots"],strict=True):
        filename,kind,inventory,assetphase=ASSETS[key]
        refpath=REFDIR/filename
        local_state=phase(n)
        view=framing(key,n)
        sound=sfx(key,n)
        maplock=("The illustrated chart is a physical object on the same carved table in every harbour map clip. Keep western water at screen left, palace on eastern screen right, and five British ship tokens in their fixed positions. Preserve the Glasgow state and Khalid token location shown in the selected reference. " if key.startswith("map-harbour") else "The illustrated world chart is a physical object on the same carved table. Keep the British Isles northwest of continental Europe, Germany in central Europe, Zanzibar just off eastern Africa, and every coastline and pin fixed; no modern border colouring. " if key.startswith("map-world") else "")
        textevent=TEXT.get(n)
        textline=(f'The only readable text is exactly "{textevent[0]}". It appears at {textevent[3]:.2f}s, remains steady through {textevent[4]:.2f}s and exits with the final cut. Preserve all digits, colon and spacing precisely. ' if textevent else "No readable letters, digits, labels, dates or captions appear anywhere in this clip. ")
        if textevent and n not in TEXT_START:
            textline=f'The only readable text is exactly "{textevent[0]}" and is present from frame one, steady through {textevent[4]:.2f}s. Preserve all digits, colon and spacing precisely. '
        move="one restrained slow push of less than five percent, completed by 4.20s" if n%5==0 and kind not in {"map","text","clock"} else "locked camera with no zoom, pan or roll"
        map_inventory=inventory.replace("exactly ","")
        if n in TEXT_START:
            map_inventory="one analog clock with no readable characters; the matching exact text card exists only in Picture 2"
        if n in MAP_TRANSITIONS:
            map_inventory=ASSETS[MAP_TRANSITIONS[n][0]][2] + "; Picture 2 supplies only the permitted later map state"
        state={"shot_id":f"clip-{n:03d}","clip":n,"global_start":slot["start"],"global_end":slot["end"],
               "narration_word_ids":slot["word_ids"],"chapter_id":slot["chapter_id"],"source_claim":claim(n),
               "reference_analysis_id":ref_analysis(n),"story_time_and_phase":local_state,
               "subject_id":key,"identity_authority":str(refpath.relative_to(ROOT)),"inherited_state":assetphase,
               "allowed_change":action,"resolved_state":"single action ends; no new event begins in final 0.40 seconds",
               "subject_count_and_inventory":inventory,"screen_placement_and_camera":view,
               "prop_ownership":"as pictured in selected single-scene anchor; no duplicated scroll, shoe, throne or ship",
               "injury_and_emotion":"serious and quiet after casualties; warm comic only for shoe character",
               "light_and_environment":"soft daylight with muted parchment, teal and ochre ink illustration",
               "reference_asset_id":key}
        states.append(state)
        shot_assets=([TEXT_START[n],key] if n in TEXT_START else
                     [MAP_TRANSITIONS[n][0],key] if n in MAP_TRANSITIONS else [key])
        coverage.append({"shot_id":state["shot_id"],"asset_ids":shot_assets,"unsupported_elements":[]})
        plan.extend([f"## Clip {n:03d} · {slot['start']:.2f}–{slot['end']:.2f}s · {slot['chapter_id']}","",
                     f"Narration overlap: {slot['spoken_text']}","",
                     f"Purpose and action: {action} Source claim {claim(n)}; adapted reference beat {ref_analysis(n)}.","",
                     f"Anchor and inventory: {', '.join('`'+a+'`' for a in shot_assets)} — {inventory}. Start state: {assetphase}. Story phase: {local_state}.","",
                     f"Frame and motion: {view}; {move}. 0.00–0.80 establishes the anchor, 0.80–3.80 performs the one action, 3.80–4.60 settles it, 4.60–5.00 holds a resolved frame. Sound: {sound}. Cut only at 5.00s.","",
                     f"Map/text contract: {maplock}{textline}Keep the illustrated stick world across every pixel.",""])
        ref_intro=(f"<Picture 1> is the blank analog-clock start frame with no readable characters. <Picture 2> is the exact final text-card frame; it controls the clock design and only permitted letters/digits. Transition once at {textevent[3]:.2f}s, then hold the second image without morphing or flicker. " if n in TEXT_START else
                   f"<Picture 1> is the exact current harbour map state. <Picture 2> is the same fixed map after the one allowed story change. Keep coastline, five British ship positions, palace side and colours identical; transition once at {MAP_TRANSITIONS[n][1]:.2f}s and hold the second state. " if n in MAP_TRANSITIONS else
                   "<Picture 1> is the sole full-frame scene reference and controls exact setting, figure silhouettes, illustrated surface, object count and placement. ")
        prompt=(
            f"Create exactly 5.00 seconds of landscape 16:9 animation at 24 fps, composed for 1024×576. "
            f"{ref_intro}"
            f"Render every pixel as one cohesive detailed hand-inked ChronoStick world: round off-white heads, tiny black dot eyes, spare stick limbs, bold clean dark contours, period-grounded clothing and vessels, muted sand, parchment, teal and navy, soft drawn shadows. "
            f"The immediate story phase is {local_state}. The visible starting inventory is {map_inventory}. "
            f"Keep the composition {view}. The camera is {move}. "
            f"From 0.00 to 0.80 seconds, establish the reference's existing physical arrangement, steady light, subject count and object condition. "
            f"From 0.80 to 3.80 seconds, perform exactly this one primary visible action: {action} "
            f"Limit background activity to at most a slight cloth, water or smoke movement already present in the reference. "
            f"From 3.80 to 4.60 seconds, stop the primary action and preserve its resulting positions and damage state. "
            f"From 4.60 to 5.00 seconds, hold a fully resolved final frame with no new event, jump, duplication or camera movement. "
            f"{maplock}{textline}"
            f"Sound: {sound}; leave silence between isolated effects. No speech, generated narration, vocal reactions, mouth movement tied to speech, subtitles, lyric text, montage panels, alternate views, extra foreground people, extra ships or photorealistic pixels. "
            f"{POLICY}\n"
        )
        if key.startswith("map-") and kind == "scene":
            permitted_tokens = ("The miniature character tokens already pictured in <Picture 1> remain at their original tiny chart scale. "
                                if key in {"map-world-khalid", "map-world-diplomacy"} or key.startswith("map-harbour")
                                else "The pictured coloured location pins and parchment marks are the only chart symbols. ")
            prompt=(
                "Create exactly 5.00 seconds of 16:9 1024×576, 24 fps animation from <Picture 1>, the single complete physical illustrated chart on its carved wooden table. "
                "Use the reference as the literal first frame. The parchment chart and table fill the frame from beginning to end; preserve its world or harbour coastline, compass, folds, pin colours, symbol count and scale. "
                "This is a continuous in-world scene, rendered wholly by H3, with the same rich hand-inked ChronoStick texture as the reference. It is never a floating map graphic or editorial overlay. "
                f"The story phase is {local_state}. The visible inventory is {inventory}. {permitted_tokens}"
                "Keep the camera locked at the reference angle for the full clip. The chart, compass, map pins, tiny pictured tokens and carved table are the complete visible world; maintain their reference scale and clear sightlines. "
                f"From 0.00 to 0.80 seconds hold the unchanged reference; from 0.80 to 3.80 seconds perform only this subtle chart action: {action} "
                "From 3.80 to 5.00 seconds hold the resulting chart still and fully resolved. All other pins, ships, tokens, coastlines and the table stay fixed, with no geography morphing or extra visual event. "
                f"{maplock}{textline}"
                f"Sound: {sound}; otherwise silence. No speech, narration, singing, music, lip sync, subtitles or photorealistic elements. {POLICY}\n"
            )
        elif kind in {"clock", "text"}:
            graphic_start=(f"<Picture 1> is the exact blank starting clock graphic. <Picture 2> is the matching graphic with the exact final label. " if n in TEXT_START else
                           "<Picture 1> is the only clock graphic and defines the entire frame. ")
            graphic_action=(f'At {textevent[3]:.2f}–{min(textevent[3]+0.25,4.85):.2f} seconds reveal the one cream label box with exact text "{textevent[0]}" as a clean flat graphic change; then hold it unchanged to 5.00. ' if n in TEXT_START else
                            f'Keep the existing exact text "{textevent[0]}" on its cream card visible and unchanged from frame one to the final frame. ' if textevent else
                            "Keep the blank clock face and unlettered parchment visible for all five seconds; the minute hand may move at most one tiny tick. ")
            prompt=(f"Create exactly 5.00 seconds at 24 fps in landscape 16:9, 1024×576. This is ONLY a flat hand-drawn 2D analog-clock card on warm beige parchment. {graphic_start}"
                    "The full-screen faint square ink grid, double dark-ink border, left black-outlined clock, hand angles, cream card geometry if present, and empty paper stay in the same fixed orthographic plane and palette. "
                    f"{graphic_action}"
                    "At 0.00–1.00 establish the unchanging graphic. At 1.00–4.60 allow only the single specified clock/card action. At 4.60–5.00 hold a completely settled final frame. "
                    "Only the referenced clock, paper grid, border and permitted exact text box exist in the frame; no environmental scene, depth, figures, symbols or any other writing. "
                    f"Sound: {sound}; silence otherwise. No speech, narration, dialogue, lip sync or subtitles. {POLICY}\n")
        elif kind == "map":
            map_ref=(f"<Picture 1> is the exact starting illustrated map. <Picture 2> is the same map after the single permitted event change; transfer only that one change at {MAP_TRANSITIONS[n][1]:.2f} seconds. " if n in MAP_TRANSITIONS else
                     "<Picture 1> is the sole complete illustrated map reference and defines the entire frame. ")
            prompt=(f"Create exactly 5.00 seconds at 24 fps in landscape 16:9, 1024×576. This is a flat hand-inked ChronoStick map motion graphic, with no scene depth. {map_ref}"
                    f"The story phase is {local_state}. The fixed starting inventory is {map_inventory}. "
                    "Preserve the original coastline trace, island shape, sea-left/land-right orientation when showing the harbour, all palette colours, border, compass, icon identities and ship count from the reference. "
                    "At 0.00–0.80 establish the unchanged map. At 0.80–3.80 perform only this restrained graphic action: "
                    f"{action} At 3.80–4.60 settle the one changed symbol or focus; at 4.60–5.00 hold the resolved map with no new event. "
                    "The camera remains top-down, locked and orthographic; only map ink and simple stick icons from the reference exist. No extra geographical features, new borders, labels, writing, photographs, 3D terrain or environmental scene. "
                    f"Sound: {sound}; silence otherwise. No speech, narration, dialogue, lip sync or subtitles. {POLICY}\n")
        p=EP/f"prompts/clip-{n:03d}.md"
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(prompt,encoding="utf-8")
        refs=[str((REFDIR/ASSETS[a][0]).relative_to(ROOT)) for a in shot_assets]
        jobslots.append({"number":n,"revision":3,"references":refs})
    write_json(EP/"plan/story-state-ledger.json",{"schema_version":"1.0","states":states})
    write_json(EP/"plan/reference-manifest.json",{"schema_version":"1.0","assets":assets,"coverage":coverage})
    (EP/"plan/shot-plan.md").write_text("\n".join(plan)+"\n",encoding="utf-8")
    write_json(EP/"automation/job-plan.json",{"schema_version":"1.0","project_seed":18960827,"slots":jobslots})
    write_json(EP/"automation/batch-settings.json",{"continue_on_error":True,"stop_on_error":False,"max_retries":1,"concat_on_complete":False,"upscale_on_complete":False})
    print(f"Wrote {len(beats)} shot descriptions, reference coverage rows, prompts and job-plan slots")


if __name__=="__main__":make()
