#!/usr/bin/env python3
"""Render pure video prompts from explicitly reviewed dynamic shot direction."""

import argparse
import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
POLICY = "NO BACKGROUND MUSIC. Natural diegetic sound effects only."


def render(slot, clip):
    fps = 24
    lines = [
        POLICY,
        "MANDATORY AUDIO: an otherwise completely silent soundtrack with ONLY the specifically listed tiny dry physical SFX. Each SFX is one short isolated event, followed immediately by absolute silence. ZERO MUSIC during the opening, action, cuts, ending and raw tail. Never fill quiet sections with sound. No score, soundtrack, musical transition, beat, melody, tonal drone, pulse, riser, sting, sustained texture, room tone or ambience. No speech or human vocal sound. Silence is the required default, including every shot without an explicit SFX cue.",
        f"Create one detailed cinematic ChronoStick vertical 9:16 sequence at 24 fps. Engine request {slot['generation_request_seconds']:.6f} seconds; H3 output {slot['expected_raw_frame_count']} frames / {slot['expected_raw_duration_seconds']:.6f} seconds. The authored picture is frames 0–{slot['frame_count'] - 1}, ending at {slot['duration_seconds']:.6f} seconds. Deliver {len(clip['shots'])} materially distinct shots joined by instantaneous hard cuts, then the specified resolved raw-tail hold. Pacing idea: {clip['arc']}.",
        "Every visible pixel belongs to the approved illustrated stick-world: round off-white heads, sparse dot eyes/brows/closed mouths, narrow simplified bodies and limbs with detailed muted period/modern clothing, simple pale drawn hands, strong controlled dark contours, matte simplified surfaces and cinematic drawn shadows. Standard bodies retain roughly 5.0–5.8 head diameters; never broad realistic human anatomy. Architecture, water, stone, timber, wax, metal, foliage, clothes and smoke share that drawn rendering. No live action, photographic skin/textures/backgrounds, glossy 3D, anime or mixed style. No panels, grids, sheets, borders or inset views.",
        "Binding ordered reference roles; the first scene anchor supplies rendering authority for every pixel, and the remaining reviewed anchors supply only their explicit scene/identity/prop states in the same style:"
    ]
    for index, ref in enumerate(clip["reference_ids"], 1):
        lines.append(f"<Picture {index}> is the {ref} anchor. {clip['anchor_locks'][ref]}")
    lines.append("Keep exact scene-specific counts, colors, head/hair/headwear silhouettes, costume cuts, owners and object shapes. Crops exclude other anchored subjects instead of duplicating or transforming them. Preserve screen placement within each setting and advance only through the explicit phases below. One primary action, at most one simple camera move and no more than the stated low-amplitude secondary motion per shot; never frantic motion or choreography. The era/location changes only on the listed hard cuts. Empty object inserts contain only their explicit inventory.")
    for shot in clip["shots"]:
        ref = ", ".join(shot["reference_ids"])
        lines += [f"HARD CUT — {shot['id']}: {shot['start_seconds_local']:.6f}–{shot['end_seconds_local']:.6f} s; frames {shot['start_frame_local']}–{shot['end_frame_local'] - 1}. {ref} scene/crop.",
                  f"Framing: {shot['framing']}. Visible inventory: {shot['inventory']}. Light/palette: {shot['light_and_palette']}",
                  f"Primary action: {shot['primary_action']}. Camera: {shot['camera']}. Resolved end: {shot['resolved_end_state']}"]
        cue = shot.get("sfx")
        if cue:
            lines.append(f"Only one quiet dry cue: {cue['description']}, local {cue['onset_frame_local'] / fps:.6f}–{cue['end_frame_local'] / fps:.6f} s; stop completely at the cue endpoint. Silence throughout the rest of this shot.")
        else:
            lines.append("Silence in this shot; do not invent a cue, voice or ambience bed.")
    lines += ["", f"Resolved raw tail: local {slot['duration_seconds']:.6f}–{slot['expected_raw_duration_seconds']:.6f} s, frames {slot['frame_count']}–{slot['expected_raw_frame_count'] - 1} inclusive. {clip['raw_tail_hold']['instruction']}",
              "Every cut is instantaneous and exact; no dissolve, temporal morph, whip-pan masking, speed ramp or unplanned scene. Zero dialogue, narration, lip sync, subtitles, readable writing, numbers, labels or buttons. Painted mask features remain fixed. Never add an unlisted person, hand, animal, prop or background event; no duplicated characters, costume/prop swaps, multiplying objects or unresolved action.",
              "FINAL AUDIO CHECK: absolutely zero background music throughout. Only listed brief dry non-tonal physical cues; silence between events and in the entire raw tail. Never add an atmospheric or musical bed. No singing, speech, whispers, human vocalization or voices."]
    text = "\n\n".join(lines).strip() + "\n"
    if text.count(POLICY) != 1 or any(text.count(f"<Picture {i}>") != 1 for i in range(1, len(clip["reference_ids"]) + 1)):
        raise ValueError("Prompt policy/reference mapping error")
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path)
    args = parser.parse_args()
    ep = args.episode.resolve()
    state = json.loads((ep / "pipeline-state.json").read_text())
    stages = {s["id"]: s for s in state["stages"]}
    if any(stages[i]["status"] != "approved" for i in ("timed-direction", "references")):
        raise ValueError("Pure prompts require reviewed direction and references")
    spec = importlib.util.spec_from_file_location("short_plan", REPO / "scripts/validate-short-plan.py")
    check = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check)
    errors = check.validate(ep, REPO)
    if errors:
        raise ValueError("; ".join(errors))
    timing = json.loads((ep / "timestamps/timing-map.json").read_text())
    direction = json.loads((ep / "plan/clip-direction.json").read_text())
    outputs = []
    for slot, clip in zip(timing["clips"], direction["clips"], strict=True):
        if slot['id'] != clip['id']:
            raise ValueError('Timing and directing clip IDs must match in order')
        path = (ep / slot["prompt_path"]).resolve()
        if not path.is_relative_to(ep / "prompts") or path.exists():
            raise ValueError("Prompt path escaped or already exists; invalidate/review text revision explicitly")
        outputs.append((path, render(slot, clip)))
    for path, prompt in outputs:
        with path.open("x") as stream:
            stream.write(prompt)
    print(f"{len(outputs)} pure prompts authored from reviewed explicit shots")


if __name__ == "__main__":
    main()
