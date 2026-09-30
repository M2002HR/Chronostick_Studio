#!/usr/bin/env python3
"""Save a raw, immutable faster-whisper word-timing pass for TTS takes."""

import argparse
import hashlib
import json
from pathlib import Path

from faster_whisper import WhisperModel


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--takes-dir", type=Path)
    source.add_argument("--audio", type=Path, help="Transcribe the assembled narration master")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="small")
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite raw timestamp source")
    takes = [args.audio] if args.audio else sorted(args.takes_dir.glob("cue-*-r*.wav"))
    if not takes:
        parser.error("No WAV takes found")
    model = WhisperModel(args.model, device=args.device,
                         compute_type="float16" if args.device == "cuda" else "int8")
    result = {"provider": "faster-whisper", "model": args.model,
              "language_requested": "fa", "word_timestamps": True, "takes": []}
    for path in takes:
        segments, info = model.transcribe(str(path), language="fa", beam_size=5,
                                          word_timestamps=True, vad_filter=False)
        chunks = []
        for segment in segments:
            chunks.append({
                "start": segment.start, "end": segment.end, "text": segment.text,
                "avg_logprob": segment.avg_logprob,
                "no_speech_prob": segment.no_speech_prob,
                "words": [{"word": word.word, "start": word.start,
                           "end": word.end, "probability": word.probability}
                          for word in (segment.words or [])],
            })
        result["takes"].append({
            "path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "language_detected": info.language,
            "language_probability": info.language_probability,
            "segments": chunks,
        })
        print(f"{path.name}: {' '.join(chunk['text'] for chunk in chunks)}", flush=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(f"Saved raw STT to {args.output}")


if __name__ == "__main__":
    main()
