#!/usr/bin/env python3
"""Render immutable cue-level WAV takes through the local Ajil TTS API."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.request
import wave

from dotenv import dotenv_values


SAFE_HEADERS = (
    "x-router-provider", "x-proxy-served-via", "x-proxy-key-slot",
    "x-proxy-key-pool-size", "x-proxy-key-rotated", "x-proxy-attempts",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--segments", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--revision", required=True, help="New immutable revision, e.g. r003")
    parser.add_argument("--cue-id", action="append", default=[], help="Only this cue; repeat as needed")
    parser.add_argument("--voice", help="Overrides UAG_GEMINI_TTS_DEFAULT_VOICE")
    parser.add_argument("--model", default="gemini-3.8-flash-tts")
    parser.add_argument("--style", default="Natural conversational Iranian Persian; calm, restrained storytelling.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--interval-seconds", type=float, default=22.0)
    parser.add_argument("--resume", action="store_true", help="Skip complete take-and-metadata pairs")
    args = parser.parse_args()

    if not re.fullmatch(r"r\d{3,}", args.revision):
        parser.error("--revision must be rNNN")
    env = dotenv_values(args.env_file)
    voice = (args.voice or os.getenv("UAG_GEMINI_TTS_DEFAULT_VOICE") or
             env.get("UAG_GEMINI_TTS_DEFAULT_VOICE") or "").strip()
    if not voice:
        parser.error("Choose --voice or configure UAG_GEMINI_TTS_DEFAULT_VOICE")
    token = os.getenv("UAG_AUTH_TOKEN") or env.get("UAG_AUTH_TOKEN") or ""
    plan = json.loads(args.segments.read_text(encoding="utf-8"))
    segments = plan.get("segments", [])
    if not isinstance(segments, list) or not segments:
        parser.error("segments.json has no segments")
    selected = [s for s in segments if not args.cue_id or s.get("id") in args.cue_id]
    if args.cue_id and set(args.cue_id) != {s.get("id") for s in selected}:
        parser.error("An --cue-id was not found in segments.json")
    if len({s.get("id") for s in selected}) != len(selected):
        parser.error("Duplicate cue ID in segments.json")

    outputs = []
    for seg in selected:
        cue_id = str(seg.get("id") or "")
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", cue_id):
            parser.error(f"Unsafe cue ID: {cue_id!r}")
        wav = args.output_dir / f"{cue_id}-{args.revision}.wav"
        meta = args.output_dir / f"{cue_id}-{args.revision}.json"
        if wav.exists() != meta.exists():
            parser.error(f"Incomplete prior take; inspect before retrying: {wav}")
        if wav.exists() and not args.resume:
            parser.error(f"Refusing to overwrite immutable take: {wav}")
        outputs.append((seg, wav, meta))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    last_request_at = None
    for seg, wav, meta in outputs:
        spoken = str(seg.get("localized_text") or "").strip()
        if not spoken:
            parser.error(f"Empty localized_text for {seg['id']}")
        style = " ".join(filter(None, [args.style.strip(), str(seg.get("delivery_style") or "").strip()]))
        if wav.exists():
            prior = json.loads(meta.read_text(encoding="utf-8"))
            if (prior.get("spoken_text") != spoken or prior.get("voice") != voice or
                    prior.get("model") != args.model or prior.get("style") != style or
                    prior.get("wav_sha256") != hashlib.sha256(wav.read_bytes()).hexdigest()):
                parser.error(f"Existing take or provenance differs from this request: {wav}")
            print(f"{seg['id']}: retained {wav}", flush=True)
            continue
        if last_request_at is not None:
            time.sleep(max(0.0, args.interval_seconds - (time.monotonic() - last_request_at)))
        body = {
            "model": f"gemini/{args.model}", "voice": voice, "input": spoken,
            "style": style, "response_format": "wav",
            "x_router": {"providers": ["gemini"], "timeout_sec": 90, "max_attempts": 1},
        }
        request = urllib.request.Request(
            args.base_url.rstrip("/") + "/v1/audio/speech",
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={"content-type": "application/json", "x-api-token": token},
            method="POST",
        )
        last_request_at = time.monotonic()
        try:
            with opener.open(request, timeout=120) as response:
                raw_wav = response.read()
                safe_headers = {k: response.headers.get(k, "") for k in SAFE_HEADERS}
        except urllib.error.HTTPError as exc:
            print(f"{seg['id']}: Ajil returned HTTP {exc.code}; take not written", file=sys.stderr)
            return 1
        except urllib.error.URLError:
            print(f"{seg['id']}: Ajil is unreachable; take not written", file=sys.stderr)
            return 1
        if not raw_wav.startswith(b"RIFF"):
            print(f"{seg['id']}: Ajil response is not WAV; take not written", file=sys.stderr)
            return 1
        with wav.open("xb") as out:
            out.write(raw_wav)
        with wave.open(str(wav), "rb") as sound:
            duration = sound.getnframes() / sound.getframerate()
        provenance = {
            "cue_id": seg["id"], "revision": args.revision, "created_at": datetime.now(timezone.utc).isoformat(),
            "model": args.model, "voice": voice, "style": style,
            "spoken_text": spoken, "spoken_text_sha256": hashlib.sha256(spoken.encode()).hexdigest(),
            "wav_sha256": hashlib.sha256(raw_wav).hexdigest(), "duration_seconds": duration,
            "target_start": seg.get("start"), "target_end": seg.get("end"),
            "response_headers": safe_headers,
        }
        with meta.open("x", encoding="utf-8") as out:
            json.dump(provenance, out, ensure_ascii=False, indent=2)
            out.write("\n")
        print(f"{seg['id']}: {duration:.2f}s {wav} (key slot {safe_headers['x-proxy-key-slot']})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
