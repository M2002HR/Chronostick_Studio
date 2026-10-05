#!/usr/bin/env python3
"""Derive voice-led dynamic Short slots; preserve provider bytes and estimates."""

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derive(rows, boundaries, fps, audio_duration):
    if (isinstance(fps, bool) or not isinstance(fps, int) or fps <= 0
            or isinstance(audio_duration, bool) or not math.isfinite(audio_duration) or audio_duration <= 0):
        raise ValueError("Valid integer FPS and actual positive audio duration required")
    if (len(boundaries) < 2 or boundaries[0] != 0
            or any(isinstance(b, bool) or not isinstance(b, int) for b in boundaries)
            or any(b <= a for a, b in zip(boundaries, boundaries[1:]))):
        raise ValueError("Slots require increasing integer frame boundaries starting at zero")
    if boundaries[-1] != math.ceil(audio_duration * fps - 1e-8):
        raise ValueError("Picture endpoint must cover complete accepted audio on the next frame, without padding extra slots")
    slots = []
    for index, (start, end) in enumerate(zip(boundaries, boundaries[1:]), 1):
        duration = (end - start) / fps
        if not 4 <= duration <= 7:
            raise ValueError("Every editorial clip must be 4–7 seconds")
        request = max(5, duration)
        raw = round(request * fps)
        raw += (5 - raw % 17) % 17
        slots.append({"id": f"clip-{index:02d}", "start_frame": start, "end_frame": end,
                      "frame_count": end - start, "start_seconds": start / fps,
                      "end_seconds": end / fps, "duration_seconds": duration,
                      "generation_request_seconds": request, "expected_raw_frame_count": raw,
                      "expected_raw_duration_seconds": raw / fps, "trim_raw_tail_frames": raw - (end - start),
                      "owned_word_indexes": [], "overlapping_word_indexes": []})
    if not rows:
        raise ValueError("Real provider word timestamps required")
    normalized, changes = [], []
    previous_end = 0.0
    for number, row in enumerate(rows, 1):
        start, end = row["start"], row["end"]
        if (not str(row.get("word", "")).strip() or any(isinstance(t, bool) or not isinstance(t, (int, float))
                or not math.isfinite(t) for t in (start, end)) or start < 0 or end <= start or end > audio_duration):
            raise ValueError(f"Invalid provider word interval: {number}")
        adjusted = max(start, previous_end)
        if adjusted >= end:
            raise ValueError(f"Overlap leaves no supported positive word interval: {number}; review provider data")
        if adjusted != start:
            changes.append({"word_index": number, "word": row["word"], "provider_start": start,
                            "derived_start": adjusted, "provider_end_unchanged": end,
                            "start_shift_seconds": adjusted - start})
        normalized.append({"word_index": number, "word": row["word"], "start": adjusted, "end": end,
                           "provider_start": start, "provider_end": end})
        previous_end = end
        midpoint = (adjusted + end) / 2
        owners = [s for s in slots if s["start_seconds"] <= midpoint < s["end_seconds"]]
        if len(owners) != 1:
            raise ValueError(f"Word does not have exactly one slot owner: {number}")
        owners[0]["owned_word_indexes"].append(number)
        for slot in slots:
            if adjusted < slot["end_seconds"] and end > slot["start_seconds"]:
                slot["overlapping_word_indexes"].append(number)
    return {"fps": fps, "audio_duration_seconds": audio_duration,
            "picture_duration_seconds": boundaries[-1] / fps, "picture_frame_count": boundaries[-1],
            "audio_tail_padding_seconds": boundaries[-1] / fps - audio_duration,
            "word_count": len(rows), "normalized_words": normalized,
            "normalization": {"method": "start=max(provider_start,previous_derived_end); original ends unchanged",
                              "status": "derived visual/caption intervals, not new measured timestamps",
                              "changes": changes},
            "word_ownership": "Unique midpoint owner; overlapping-word lists separately describe boundary-spanning speech",
            "clips": slots}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--slot-decisions", type=Path, required=True)
    args = parser.parse_args()
    ep = args.episode.resolve()
    manifest = json.loads((ep / "episode.json").read_text())
    state = json.loads((ep / "pipeline-state.json").read_text())
    if next(s for s in state["stages"] if s["id"] == "voice")["status"] != "approved":
        raise ValueError("Timing requires the accepted user voice")
    decision = json.loads(args.slot_decisions.read_text())
    audio = ep / manifest["accepted_voice"]
    source = ep / decision["word_source_path"]
    response = ep / decision["raw_response_path"]
    for key, path in (("voice_sha256", audio), ("word_source_sha256", source), ("raw_response_sha256", response)):
        if sha(path) != decision[key]:
            raise ValueError(f"Changed timing input: {key}")
    probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_format", "-of", "json", str(audio)]))
    duration = float(probe["format"]["duration"])
    with source.open(newline="") as stream:
        rows = [{"word": r["word"], "start": float(r["start"]), "end": float(r["end"])} for r in csv.DictReader(stream)]
    result = derive(rows, decision["frame_boundaries"], decision["fps"], duration)
    result.update({"created_at": datetime.now(timezone.utc).isoformat(), "status": "needs_review",
                   "source": {"path": "timestamps/word-timestamps-source.csv", "sha256": sha(source),
                              "provider_path": decision["word_source_path"], "raw_response_path": decision["raw_response_path"],
                              "raw_response_sha256": sha(response)},
                   "accepted_voice": {"path": manifest["accepted_voice"], "sha256": sha(audio)},
                   "slot_decisions_path": str(args.slot_decisions.resolve().relative_to(ep)),
                   "slot_decisions_sha256": sha(args.slot_decisions),
                   "text_aliases": decision.get("text_aliases", []),
                   "timing_precision": "Actual Ajil STT estimates; normalization is explicit. Numeric aliases stay aggregate intervals, never interpolated word timings."})
    outputs = {ep / "timestamps/word-timestamps-source.csv": source.read_bytes(),
               ep / "timestamps/timing-map.json": (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()}
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(["word", "start", "end"])
    for row in result["normalized_words"]:
        writer.writerow([row["word"], f"{row['start']:.6f}", f"{row['end']:.6f}"])
    outputs[ep / "timestamps/word-timestamps-normalized.csv"] = stream.getvalue().encode()
    if any(path.exists() for path in outputs):
        raise FileExistsError("Timing output already exists; review/invalidate it explicitly instead of replacing source evidence")
    for path, data in outputs.items():
        with path.open("xb") as f:
            f.write(data)
    print(f"{len(result['clips'])} dynamic slots; {result['picture_frame_count']} frames; {len(result['normalization']['changes'])} documented overlap adjustments")


if __name__ == "__main__":
    main()
