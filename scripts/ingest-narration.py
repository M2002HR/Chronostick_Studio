#!/usr/bin/env python3
"""Archive a supplied voice/export and extract a full-length assembly WAV."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def probe(path):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--language", default="es")
    parser.add_argument("--revision", required=True)
    parser.add_argument("--audio-stream", type=int, default=0, help="Zero-based audio stream number")
    args = parser.parse_args()
    if not re.fullmatch(r"r\d{3,}", args.revision) or not re.fullmatch(r"[a-z]{2,3}(?:-[a-z0-9]+)*", args.language):
        parser.error("Use rNNN and a lowercase language tag")
    if not args.input.is_file() or not (args.episode / "episode.json").is_file():
        parser.error("Input and episode manifest must exist")
    source = args.input.resolve()
    root = args.episode.resolve()
    source_probe = probe(source)
    audio = [s for s in source_probe["streams"] if s.get("codec_type") == "audio"]
    if not 0 <= args.audio_stream < len(audio):
        parser.error("Selected audio stream does not exist")
    stream = audio[args.audio_stream]
    paths = {
        "source": root / f"audio/source/voice-export-{args.language}-{args.revision}{source.suffix.lower()}",
        "wav": root / f"audio/narration-{args.language}-{args.revision}.wav",
        "provenance": root / f"audio/narration-provenance-{args.language}-{args.revision}.json",
        "probe": root / f"audio/narration-probe-{args.language}-{args.revision}.json",
    }
    if stream.get("codec_name") == "aac":
        paths["native"] = root / f"audio/narration-{args.language}-{args.revision}.m4a"
    if any(p.exists() for p in paths.values()):
        parser.error("Refusing to overwrite an existing narration revision")
    for p in paths.values():
        p.parent.mkdir(parents=True, exist_ok=True)
    source_hash = digest(source)
    with source.open("rb") as original, paths["source"].open("xb") as archived:
        shutil.copyfileobj(original, archived)
    if digest(paths["source"]) != source_hash:
        raise RuntimeError("Input archive hash mismatch")
    mapping = f"0:a:{args.audio_stream}"
    provenance = {
        "created_at": datetime.now(timezone.utc).isoformat(), "status": "pending",
        "original_name": source.name, "incoming_sha256": source_hash,
        "source_path": paths["source"].relative_to(root).as_posix(),
        "selected_audio_stream": args.audio_stream, "source_audio_start_seconds": float(stream.get("start_time", 0)),
        "source_probe": source_probe, "purpose": "separate narration track for final assembly",
        "processing": "full selected audio; no silence trim, gain, filtering, time stretch or resampling",
        "wav_encoding": "pcm_s24le; native sample rate and channel count",
        "creative_approval": None,
    }
    try:
        commands = [["ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-i", str(paths["source"]),
                     "-map", mapping, "-vn", "-c:a", "pcm_s24le", str(paths["wav"])]]
        if "native" in paths:
            commands.append(["ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-i", str(paths["source"]),
                             "-map", mapping, "-vn", "-c:a", "copy", str(paths["native"])])
        for command in commands:
            subprocess.run(command, check=True)
        out_probe = probe(paths["wav"])
        out_stream = out_probe["streams"][0]
        if out_stream["sample_rate"] != stream["sample_rate"] or out_stream["channels"] != stream["channels"]:
            raise RuntimeError("Sample rate/channel count changed")
        with paths["probe"].open("x") as f:
            json.dump(out_probe, f, indent=2)
            f.write("\n")
        provenance.update(status="needs_review", duration_seconds=float(out_probe["format"]["duration"]),
                          sample_rate=int(out_stream["sample_rate"]), channels=out_stream["channels"],
                          artifacts={k: {"path": p.relative_to(root).as_posix(), "sha256": digest(p)}
                                     for k, p in paths.items() if k != "provenance"})
    except (subprocess.CalledProcessError, RuntimeError):
        provenance["status"] = "failed"
        raise
    finally:
        with paths["provenance"].open("x") as f:
            json.dump(provenance, f, ensure_ascii=False, indent=2)
            f.write("\n")
    print(f"Assembly narration saved: {paths['wav']} ({provenance['duration_seconds']:.3f} s)")


if __name__ == "__main__":
    main()
