#!/usr/bin/env python3
"""Place immutable narration takes on a fixed picture timeline without stretching."""

import argparse
import json
from pathlib import Path

import numpy as np
import soundfile as sf


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assembly", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite immutable narration master")
    plan = json.loads(args.assembly.read_text(encoding="utf-8"))
    if "base_plan" in plan:
        base = json.loads((args.assembly.parent / plan["base_plan"]).read_text(encoding="utf-8"))
        for change in plan.get("changes", []):
            matches = [item for item in base["takes"] if item["id"] == change["id"]]
            if len(matches) != 1:
                parser.error(f"Unknown or duplicate cue in changes: {change['id']}")
            matches[0].update({key: value for key, value in change.items() if key != "id"})
        plan = base
    sample_rate = int(plan["sample_rate"])
    total = round(float(plan["picture_duration_seconds"]) * sample_rate)
    mix = np.zeros(total, dtype=np.float64)
    for item in plan["takes"]:
        path = args.assembly.parent / item["file"]
        audio, rate = sf.read(path, dtype="float64")
        if rate != sample_rate or audio.ndim != 1:
            parser.error(f"Expected mono {sample_rate} Hz WAV: {path}")
        pauses = item.get("pause_insertions", [])
        if pauses:
            pieces = []
            cursor = 0
            for pause in sorted(pauses, key=lambda value: value["at_seconds"]):
                at = round(float(pause["at_seconds"]) * sample_rate)
                if at < cursor or at > len(audio):
                    parser.error(f"Invalid pause point in {path}")
                pieces.extend((audio[cursor:at],
                               np.zeros(round(float(pause["duration_seconds"]) * sample_rate))))
                cursor = at
            pieces.append(audio[cursor:])
            audio = np.concatenate(pieces)
        start = round(float(item["start"]) * sample_rate)
        end = start + len(audio)
        if start < 0 or end > total:
            parser.error(f"Take extends outside picture: {path}")
        fade = min(round(0.010 * sample_rate), len(audio) // 2)
        audio[:fade] *= np.linspace(0, 1, fade, endpoint=False)
        audio[-fade:] *= np.linspace(1, 0, fade, endpoint=False)
        audio *= 10 ** (float(item["gain_db"]) / 20)
        mix[start:end] += audio
        print(f"{item['id']}: {item['start']:.2f}–{end / sample_rate:.2f} s, {item['gain_db']:+.1f} dB")
    peak = float(np.max(np.abs(mix)))
    if peak > 0.98:
        parser.error(f"Composite peak {peak:.3f} exceeds safe PCM headroom")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(args.output, mix, sample_rate, subtype="PCM_24")
    print(f"Saved {args.output}: {total / sample_rate:.6f} s, peak {peak:.3f}")


if __name__ == "__main__":
    main()
