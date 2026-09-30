#!/usr/bin/env python3
"""Request a blind audio-only Persian transcript/QC and save the raw response."""

import argparse
import base64
import getpass
import json
import os
from pathlib import Path
import re
from urllib import error, request


PROMPT = (
    "Listen to this Persian narration without a reference script. Return JSON "
    "with keys transcript_fa and audible_issues. Transcribe the words actually "
    "heard in colloquial Persian, including numbers as spoken. In audible_issues, "
    "list only clearly audible missing words, mispronunciations, clipped joins, "
    "abrupt voice changes, unnatural pauses, or unnatural delivery, with approximate "
    "MM:SS location and a short explanation in Persian. Do not invent issues, "
    "infer from historical facts, or claim perfect audio if unsure."
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="gemini-3.8-flash")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite raw provider response")
    key = os.environ.get("GEMINI_API_KEY") or getpass.getpass("Google AI Studio API key: ")
    if not key:
        parser.error("Missing API key")
    audio_data = base64.b64encode(args.audio.read_bytes()).decode("ascii")
    payload = {"model": args.model, "input": [
        {"type": "text", "text": PROMPT},
        {"type": "audio", "data": audio_data, "mime_type": "audio/wav"},
    ]}
    req = request.Request(
        "https://generativelanguage.googleapis.com/v1beta/interactions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=180) as response:
            raw = response.read()
    except error.HTTPError as exc:
        detail = re.sub(r"AIza[0-9A-Za-z_-]+", "[REDACTED]",
                        exc.read().decode("utf-8", errors="replace"))
        raise SystemExit(f"HTTP {exc.code}: {detail[:1200]}") from None
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    result = json.loads(raw)
    for step in result.get("steps", []):
        if step.get("type") == "model_output":
            for part in step.get("content", []):
                if part.get("type") == "text":
                    print(part.get("text", ""))
    print(f"Saved raw response to {args.output}")


if __name__ == "__main__":
    main()
