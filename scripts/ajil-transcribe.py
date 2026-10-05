#!/usr/bin/env python3
"""Extract audio and preserve Ajil word/segment STT in immutable revisions."""

import argparse
import csv
from datetime import datetime, timezone
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata

from dotenv import dotenv_values
import httpx


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def tokens(text):
    return re.findall(r"[^\W_]+", unicodedata.normalize("NFC", text).casefold())


def unpack_response(response):
    """Ajil -> provider payload -> original verbose_json. Never alter raw bytes."""
    if not isinstance(response, dict) or response.get("ok") is False:
        raise ValueError("Ajil reported a failed transcription")
    provider = response.get("payload", response)
    if not isinstance(provider, dict) or provider.get("ok") is False:
        raise ValueError("STT provider reported a failed transcription")
    raw = provider.get("raw", provider)
    if not isinstance(raw, dict):
        raise ValueError("Missing verbose STT object")
    return raw


def validate_words(raw, duration, expected=None):
    words = raw.get("words")
    segments = raw.get("segments")
    text = raw.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("No transcript text")
    if not isinstance(words, list) or not words:
        raise ValueError("Word timestamps missing; enable UAG_GROQ_STT_TIMESTAMP_GRANULARITIES=word,segment")
    if not isinstance(segments, list) or not segments:
        raise ValueError("Segment timestamps missing")
    overlaps = []
    regressions = []
    previous_start = previous_end = -1
    for index, word in enumerate(words):
        if not isinstance(word, dict) or not isinstance(word.get("word"), str) or not word["word"].strip():
            raise ValueError(f"Invalid token at word {index + 1}")
        start, end = word.get("start"), word.get("end")
        if (not isinstance(start, (float, int)) or isinstance(start, bool)
                or not isinstance(end, (float, int)) or isinstance(end, bool)
                or not math.isfinite(start) or not math.isfinite(end)
                or start < 0 or end < start or end > duration + 0.25):
            raise ValueError(f"Invalid time bounds at word {index + 1}")
        if start < previous_start:
            regressions.append(index + 1)
        if start < previous_end:
            overlaps.append(index + 1)
        previous_start, previous_end = start, end
    previous_start = -1
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict) or not isinstance(segment.get("text"), str):
            raise ValueError(f"Invalid segment {index + 1}")
        start, end = segment.get("start"), segment.get("end")
        if (not isinstance(start, (int, float)) or isinstance(start, bool)
                or not isinstance(end, (int, float)) or isinstance(end, bool)
                or not math.isfinite(start) or not math.isfinite(end)
                or start < 0 or end < start or end > duration + 0.25 or start < previous_start):
            raise ValueError(f"Invalid segment time {index + 1}")
        previous_start = start
    reconstructed = " ".join(w["word"] for w in words)
    expected_changes = []
    if expected is not None:
        before, after = tokens(expected), tokens(reconstructed)
        matcher = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
        expected_changes = [dict(operation=op, expected=before[i:j], observed=after[k:l])
                            for op, i, j, k, l in matcher.get_opcodes() if op != "equal"]
    return {
        "word_count": len(words), "segment_count": len(segments),
        "first_word_start": words[0]["start"], "last_word_end": words[-1]["end"],
        "overlapping_word_rows": overlaps,
        "nonmonotonic_word_rows": regressions,
        "text_vs_words_match": tokens(text) == tokens(reconstructed),
        "expected_script_changes": expected_changes,
        "status": "needs_review", "normalization": "none; provider times preserved",
        "timing_limit": "STT estimates; accepted voice and perceptual review are required",
    }


def save_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--purpose", required=True, choices=("reference", "voice"))
    parser.add_argument("--revision", required=True)
    parser.add_argument("--language", default="auto")
    parser.add_argument("--expected-script", type=Path)
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--timeout", type=float, default=240)
    parser.add_argument("--audio-format", choices=("flac", "wav", "mp3"), default="flac")
    parser.add_argument("--from-response", type=Path, help="Derive a new revision from preserved response bytes; no API call")
    parser.add_argument("--audio-derivative", type=Path, help="Exact derivative used for --from-response")
    parser.add_argument("--source-provenance", type=Path, help="Provenance binding the preserved response, derivative and original")
    args = parser.parse_args()
    if not re.fullmatch(r"r\d{3,}", args.revision):
        parser.error("Use an immutable rNNN revision")
    if not args.input.is_file() or (args.expected_script and not args.expected_script.is_file()):
        parser.error("Input or expected script does not exist")
    if args.purpose == "voice" and (not args.expected_script or args.language == "auto"):
        parser.error("Voice mode requires --expected-script and an explicit --language")
    if any((args.from_response, args.audio_derivative, args.source_provenance)):
        if not all(p and p.is_file() for p in (args.from_response, args.audio_derivative, args.source_provenance)):
            parser.error("Derivation requires existing --from-response, --audio-derivative and --source-provenance")
        prior = json.loads(args.source_provenance.read_text())
        for p, key in ((args.input, "input_sha256"), (args.audio_derivative, "audio_sha256"), (args.from_response, "raw_response_sha256")):
            if digest(p) != prior.get(key):
                parser.error("Preserved response provenance does not match original/audio/response")
        if args.audio_derivative.suffix != "." + args.audio_format:
            parser.error("--audio-format must match the preserved derivative")
    names = {key: args.output_dir / f"{args.purpose}-{name}-{args.revision}.{extension}"
             for key, name, extension in (
                 ("audio", "audio", args.audio_format), ("raw", "response", "json"),
                 ("words", "words", "csv"), ("segments", "segments", "json"),
                 ("text", "transcript", "md"), ("report", "validation", "json"),
                 ("provenance", "provenance", "json"))}
    if any(path.exists() for path in names.values()):
        parser.error("Revision already has artifacts; inspect it and choose a new revision")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    input_hash = digest(args.input)
    # Explicit mono audio derivative; original video/audio is never rewritten.
    codec_args = {
        "flac": ["-c:a", "flac", "-sample_fmt", "s16"],
        "wav": ["-c:a", "pcm_s16le"],
        "mp3": ["-c:a", "libmp3lame", "-b:a", "48k"],
    }[args.audio_format]
    if args.from_response:
        with args.audio_derivative.open("rb") as source, names["audio"].open("xb") as target:
            shutil.copyfileobj(source, target)
    else:
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-i", str(args.input),
            "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000",
            *codec_args, str(names["audio"])
        ], check=True)
    duration = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(names["audio"])
    ]))
    if names["audio"].stat().st_size > 24 * 1024 * 1024:
        parser.error("Audio exceeds this helper's 24 MiB limit; implement offset-preserving chunking before retrying")
    env = dotenv_values(args.env_file)
    token = os.getenv("UAG_AUTH_TOKEN") or env.get("UAG_AUTH_TOKEN") or ""
    header = os.getenv("UAG_AUTH_HEADER_NAME") or env.get("UAG_AUTH_HEADER_NAME") or "x-api-token"
    params = {} if args.language == "auto" else {"language": args.language}
    provenance = {
        "purpose": args.purpose, "revision": args.revision,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_path": str(args.input.resolve()), "input_sha256": input_hash,
        "audio_path": names["audio"].name, "audio_sha256": digest(names["audio"]),
        "audio_duration_seconds": duration, "language_requested": args.language,
        "endpoint": "/v1/audio/transcriptions", "status": "pending",
        "derivative_format": args.audio_format,
        "derivative_lossy": args.audio_format == "mp3",
    }
    try:
        if args.from_response:
            raw_response = args.from_response.read_bytes()
            http_status = prior.get("http_status")
            provenance["derived_from_response"] = str(args.from_response.resolve())
            provenance["api_request_made"] = False
        else:
            with httpx.Client(trust_env=False, timeout=args.timeout) as client, names["audio"].open("rb") as audio:
                response = client.post(args.base_url.rstrip("/") + provenance["endpoint"],
                                       headers={header: token}, params=params,
                                       files={"file": (names["audio"].name, audio,
                                                       {"flac": "audio/flac", "wav": "audio/wav", "mp3": "audio/mpeg"}[args.audio_format])})
            raw_response = response.content
            http_status = response.status_code
            provenance["api_request_made"] = True
        with names["raw"].open("xb") as stream:
            stream.write(raw_response)
        provenance.update(http_status=http_status, raw_response_path=names["raw"].name,
                          raw_response_sha256=digest(names["raw"]))
        if http_status != 200:
            raise ValueError(f"Ajil returned HTTP {http_status}; raw response retained")
        envelope = json.loads(raw_response)
        raw = unpack_response(envelope)
        report = validate_words(raw, duration, args.expected_script.read_text() if args.expected_script else None)
        provenance.update(provider=envelope.get("provider"), model=envelope.get("model"),
                          language_detected=raw.get("language"), status="needs_review")
        save_json(names["report"], report)
        save_json(names["segments"], {"segments": raw["segments"], "source_response": names["raw"].name})
        with names["words"].open("x", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=("word", "start", "end"))
            writer.writeheader()
            writer.writerows({key: word[key] for key in writer.fieldnames} for word in raw["words"])
        with names["text"].open("x", encoding="utf-8") as stream:
            stream.write(raw["text"].strip() + "\n")
        save_json(names["provenance"], provenance)
        print(f"Saved {report['word_count']} words and {report['segment_count']} segments; status needs_review: {args.output_dir}")
        return 0
    except (ValueError, httpx.HTTPError) as exc:
        provenance["status"] = "failed"
        save_json(names["provenance"], provenance)
        # Avoid echoing provider errors or transport URLs that could contain credentials.
        print(f"Transcription failed ({type(exc).__name__}); inspect local raw response/provenance and use a new revision.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
