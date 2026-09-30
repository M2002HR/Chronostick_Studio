#!/usr/bin/env python3
"""Render immutable Gemini TTS WAV takes without storing an API key.

Use --text for a probe, or --segments with a localization segments.json file.
The key is requested without terminal echo if GEMINI_API_KEY is unset.
"""

import argparse
import base64
import getpass
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib import error, request


DEFAULT_STYLE = (
    "Native Iranian Persian documentary narrator. Natural, conversational and "
    "human; clear articulation, measured but flowing pace. Restrained gravity "
    "and empathy, never theatrical, breathy, shouted, or exaggerated. "
    "Read only the supplied Persian text; do not add words."
)


def safe_error(exc):
    return re.sub(r"AIza[0-9A-Za-z_-]+", "[REDACTED]", str(exc))[:1200]


def synthesize(key, model, voice, text, style):
    payload = {
        "model": model,
        "input": [{
            "type": "user_input",
            "content": [{
                "type": "text",
                "text": text,
                "annotations": [{"type": "speech_metadata", "style": style}],
            }],
        }],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": [{"voice": voice}]},
    }
    req = request.Request(
        "https://generativelanguage.googleapis.com/v1beta/interactions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=180) as response:
            result = json.load(response)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {safe_error(detail)}") from None
    blocks = [
        content
        for step in result.get("steps", [])
        if step.get("type") == "model_output"
        for content in step.get("content", [])
        if content.get("type") == "audio" and content.get("data")
    ]
    if not blocks:
        raise RuntimeError("API response did not contain audio")
    return base64.b64decode(blocks[-1]["data"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="One short probe utterance")
    source.add_argument("--segments", type=Path, help="Localization segments.json")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="gemini-3.8-flash-tts")
    parser.add_argument("--voice", default="Charon")
    parser.add_argument("--style", default=DEFAULT_STYLE)
    parser.add_argument("--revision", default="r001")
    parser.add_argument("--resume", action="store_true", help="Skip existing immutable takes")
    parser.add_argument("--cue-id", action="append", default=[],
                        help="Render only this cue ID; may be repeated")
    parser.add_argument("--interval-seconds", type=float, default=22.0,
                        help="Minimum interval between API requests (Free Tier: 3/min)")
    args = parser.parse_args()

    if args.text:
        items = [("probe", args.text, args.style)]
    else:
        plan = json.loads(args.segments.read_text(encoding="utf-8"))
        items = [
            (item["id"], item["localized_text"],
             args.style + " " + item.get("delivery_style", ""))
            for item in plan["segments"]
            if not args.cue_id or item["id"] in args.cue_id
        ]
        if args.cue_id and len(items) != len(set(args.cue_id)):
            parser.error("An --cue-id is missing or duplicated in the segment plan")
    outputs = [args.output_dir / f"{item_id}-{args.revision}.wav" for item_id, _, _ in items]
    existing = [str(path) for path in outputs if path.exists()]
    if existing and not args.resume:
        parser.error("Refusing to overwrite existing take(s): " + ", ".join(existing))

    key = os.environ.get("GEMINI_API_KEY") or getpass.getpass("Google AI Studio API key: ")
    if not key:
        parser.error("Missing API key")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    last_request_at = None
    for (item_id, text, style), path in zip(items, outputs):
        if path.exists():
            print(f"{item_id}: retained {path}", flush=True)
            continue
        try:
            for attempt in range(5):
                if last_request_at is not None:
                    delay = args.interval_seconds - (time.monotonic() - last_request_at)
                    if delay > 0:
                        time.sleep(delay)
                last_request_at = time.monotonic()
                try:
                    data = synthesize(key, args.model, args.voice, text, style)
                    break
                except RuntimeError as exc:
                    if "HTTP 429" not in str(exc) or attempt == 4:
                        raise
                    print(f"{item_id}: Free Tier rate limit; waiting before retry", flush=True)
                    time.sleep(max(30.0, args.interval_seconds))
            if data[:4] != b"RIFF":
                raise RuntimeError("Provider did not return a WAV file")
            path.write_bytes(data)
            print(f"{item_id}: wrote {path} ({len(data)} bytes)", flush=True)
        except Exception as exc:
            print(f"{item_id}: {type(exc).__name__}: {safe_error(exc)}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
