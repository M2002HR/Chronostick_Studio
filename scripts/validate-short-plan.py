#!/usr/bin/env python3
"""Validate dynamic Short cuts, storyboard coverage and immutable timing inputs."""

import argparse
import hashlib
import json
from pathlib import Path


def interval_errors(timing, direction, panel_ids, references):
    errors = []
    fps = timing.get("fps")
    if fps != 24:
        return ["Dynamic Short direction requires 24 fps"]
    clips = timing.get("clips", [])
    directed = direction.get("clips", [])
    if not clips or [c.get("id") for c in clips] != [c.get("id") for c in directed]:
        return ["Directed clip IDs must exactly match timing slots in order"]
    owners, covered, previous = [], set(), 0
    for slot, clip in zip(clips, directed):
        start, end = slot.get("start_frame"), slot.get("end_frame")
        if (isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, int)
                or not isinstance(end, int) or start != previous or end <= start):
            errors.append(f"Slot gap/overlap or invalid frame interval: {slot.get('id')}")
            continue
        previous = end
        frames = end - start
        if not 4 <= frames / fps <= 7 or abs(slot.get("duration_seconds", 0) - frames / fps) > 1e-6:
            errors.append(f"Slot duration/frame mismatch: {slot['id']}")
        raw = slot.get("expected_raw_frame_count", 0)
        if not isinstance(raw, int) or not 124 <= raw <= 362 or raw % 17 != 5 or raw < frames:
            errors.append(f"Unsupported H3 raw grid: {slot['id']}")
        ref_ids = clip.get("reference_ids", [])
        if not 1 <= len(ref_ids) <= 9 or len(set(ref_ids)) != len(ref_ids) or any(i not in references for i in ref_ids):
            errors.append(f"Invalid clip references: {slot['id']}")
        shot_end = 0
        for shot in clip.get("shots", []):
            a, b = shot.get("start_frame_local"), shot.get("end_frame_local")
            if (isinstance(a, bool) or isinstance(b, bool) or not isinstance(a, int) or not isinstance(b, int)
                    or a != shot_end or b <= a or b > frames):
                errors.append(f"Shot gap/overlap or boundary overflow: {shot.get('id')}")
                continue
            shot_end = b
            panels = shot.get("storyboard_panel_ids", [])
            refs = shot.get("reference_ids", [])
            if not panels or any(p not in panel_ids for p in panels):
                errors.append(f"Shot lacks known storyboard panel: {shot.get('id')}")
            covered.update(panels)
            if not refs or any(r not in ref_ids for r in refs):
                errors.append(f"Shot lacks ordered clip reference: {shot.get('id')}")
            for r in refs:
                if r not in references:
                    continue
                if any(p not in references[r].get("storyboard_panel_ids", []) for p in panels):
                    errors.append(f"Shot reference does not cover its panel: {shot.get('id')}/{r}")
            if not shot.get("primary_action") or not shot.get("inventory") or not shot.get("resolved_end_state"):
                errors.append(f"Shot lacks action/inventory/end state: {shot.get('id')}")
            sfx = shot.get("sfx")
            if sfx and (sfx.get("onset_frame_local", -1) < a
                        or sfx.get("end_frame_local", frames + 1) > b
                        or sfx["end_frame_local"] <= sfx["onset_frame_local"]):
                errors.append(f"SFX crosses its shot: {shot.get('id')}")
        if shot_end != frames:
            errors.append(f"Shots do not cover complete editorial slot: {slot['id']}")
        owners.extend(slot.get("owned_word_indexes", []))
        if clip.get("raw_tail_hold", {}).get("start_frame_local") != frames or clip.get("raw_tail_hold", {}).get("end_frame_local") != raw:
            errors.append(f"Missing resolved raw-tail hold: {slot['id']}")
    if previous != timing.get("picture_frame_count"):
        errors.append("Slots do not cover the exact picture frame count")
    if sorted(owners) != list(range(1, timing.get("word_count", 0) + 1)):
        errors.append("Every provider word must have exactly one clip owner")
    omissions = direction.get("omitted_panels", [])
    if any(not isinstance(o, dict) or o.get("id") not in panel_ids or not o.get("reason") for o in omissions):
        errors.append("Panel omissions require known IDs and reasons")
    if panel_ids - covered - {o.get("id") for o in omissions if isinstance(o, dict)}:
        errors.append("Storyboard panels absent from final direction without reasons")
    return errors


def validate(ep, repo):
    errors = []
    try:
        timing = json.loads((ep / "timestamps/timing-map.json").read_text())
        direction = json.loads((ep / "plan/clip-direction.json").read_text())
        panels = json.loads((ep / "plan/storyboard/shot-list.json").read_text())["shots"]
        refs = json.loads((ep / "plan/reference-manifest.json").read_text())["entries"]
        manifest = json.loads((ep / "episode.json").read_text())
        for record in [timing["source"], timing["accepted_voice"]]:
            path = (ep / record["path"]).resolve()
            if not path.is_relative_to(ep.resolve()) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
                errors.append("Timing source/accepted voice changed or escaped")
        if timing["accepted_voice"]["path"] != manifest.get("accepted_voice"):
            errors.append("Timing map uses a different accepted voice")
        if abs(timing["picture_duration_seconds"] - manifest["target_seconds"]) > 1e-6:
            errors.append("Timing map picture duration differs from reviewed episode target")
        raw = ep / timing["source"]["raw_response_path"]
        if hashlib.sha256(raw.read_bytes()).hexdigest() != timing["source"]["raw_response_sha256"]:
            errors.append("Raw provider response changed")
        for ref in refs:
            if ref["id"] not in {r for c in direction["clips"] for r in c["reference_ids"]}:
                continue
            image = (repo / ref["selected_path"]).resolve()
            if ref.get("review_status") != "approved" or hashlib.sha256(image.read_bytes()).hexdigest() != ref["sha256"]:
                errors.append(f"Direction uses an unreviewed/changed reference: {ref['id']}")
        errors.extend(interval_errors(timing, direction, {p["id"] for p in panels}, {r["id"]: r for r in refs}))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid or missing direction artifact: {type(exc).__name__}: {exc}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path)
    args = parser.parse_args()
    issues = validate(args.episode.resolve(), Path(__file__).resolve().parents[1])
    for issue in issues:
        print("FAIL", issue)
    if not issues:
        print("Dynamic Short direction validation passed")
    raise SystemExit(bool(issues))
