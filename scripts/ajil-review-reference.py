#!/usr/bin/env python3
"""Archive an Ajil/Gemini review of actual video beside its real transcript."""

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re

from dotenv import dotenv_values
import httpx


REQUEST = """Review the complete attached reference video alongside the supplied
STT transcript as a director, editor and audio reviewer. Return a JSON object
with: coverage_method, source_language, audible_delivery_and_sound,
timecoded_sequences, transcript_mismatches, visual_story_mechanisms,
historical_claims_needing_verification, generation_feasibility, and uncertainty.
In each timecoded sequence give approximate start/end, observable people/props,
action, camera/edit technique, visible text and narrative function. Distinguish
what you actually observe/hear from interpretation. Do not invent exact cut
times, hidden actions or perfect timing. Call out STT mistakes only if audible.
Evaluate the hook, joke labels, religious-context section, cellar/barrels gag,
arrest reveal and ending. Suggest how to compress to a 30-second original
Spanish short in a detailed stick-world with very fast purposeful cuts, one
main action and at most one camera move per shot, and no separately authored
editing pass. Do not copy dialogue, creator art or the final film quotation.
Generated production clips must have no music or speech, only small isolated
natural SFX; the Spanish narration will be supplied separately. A source's
music is observation, never permission for production music. Treat historical
claims as unverified and mark unknowns. This response is machine-review evidence,
not a production approval.\n\nActual STT transcript follows:\n"""


def save_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def candidate_text(value):
    if isinstance(value, dict):
        if isinstance(value.get("candidates"), list):
            return "\n".join(p.get("text", "") for c in value["candidates"]
                             for p in c.get("content", {}).get("parts", []) if "text" in p)
        if isinstance(value.get("choices"), list):
            return "\n".join(c.get("message", {}).get("content", "") for c in value["choices"])
        for child in value.values():
            found = candidate_text(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = candidate_text(child)
            if found:
                return found
    return ""


def genuine_review(response):
    if response.get("model", "").startswith("local/") or response.get("router", {}).get("provider") == "local-fallback":
        raise ValueError("Ajil local fallback contains no video analysis")
    text = candidate_text(response)
    parsed = json.loads(text)
    if not isinstance(parsed, dict) or not parsed.get("timecoded_sequences"):
        raise ValueError("Missing structured actual-video review")
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--transcript", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--model", default="gemini-2.5-flash")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--instructions", type=Path, help="Explicit source/render review questions; never an approval")
    parser.add_argument("--media-only", action="store_true", help="Review without a supplied script or intended shot contract")
    parser.add_argument("--media-mime", default="video/mp4", choices=["video/mp4", "audio/mpeg", "audio/wav", "audio/mp4"])
    args = parser.parse_args()
    if not re.fullmatch(r"r\d{3,}", args.revision):
        parser.error("Use rNNN revision")
    if not args.video.is_file() or not args.transcript.is_file():
        parser.error("Video and transcript must exist")
    paths = {name: args.output_dir / f"video-review-{name}-{args.revision}.{ext}"
             for name, ext in (("request", "txt"), ("response", "json"), ("text", "md"), ("provenance", "json"))}
    if any(p.exists() for p in paths.values()):
        parser.error("Refusing to overwrite a review revision")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    instructions = args.instructions.read_text() if args.instructions else REQUEST
    text = instructions if args.media_only else instructions + '\n\nAttached timing/story contract:\n' + args.transcript.read_text()
    with paths["request"].open("x") as stream:
        stream.write(text)
    video_bytes = args.video.read_bytes()
    body = {
        "model": [{"provider": "gemini", "model": args.model, "priority": 0}],
        "contents": [{"role": "user", "parts": [
            {"inlineData": {"mimeType": args.media_mime, "data": base64.b64encode(video_bytes).decode()}},
            {"text": text},
        ]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 8192, "responseMimeType": "application/json"},
        # One provider/model only; parallel_race avoids the fallback chain's
        # short per-attempt cap for a legitimate multimodal review.
        "x_router": {"strategy": "parallel_race", "providers": ["gemini"], "timeout_sec": 180, "max_attempts": 1},
    }
    env = dotenv_values(args.env_file)
    header = os.getenv("UAG_AUTH_HEADER_NAME") or env.get("UAG_AUTH_HEADER_NAME") or "x-api-token"
    token = os.getenv("UAG_AUTH_TOKEN") or env.get("UAG_AUTH_TOKEN") or ""
    provenance = {
        "created_at": datetime.now(timezone.utc).isoformat(), "model_requested": args.model,
        "video_path": str(args.video.resolve()), "video_sha256": hashlib.sha256(video_bytes).hexdigest(),
        "transcript_path": str(args.transcript.resolve()), "transcript_sha256": hashlib.sha256(args.transcript.read_bytes()).hexdigest(),
        "request_sha256": hashlib.sha256(text.encode()).hexdigest(), "status": "pending",
        "role": "supplementary machine video/audio review; independent frame inspection still required",
        "instructions_path": str(args.instructions.resolve()) if args.instructions else None,
        "intended_contract_supplied": not args.media_only,
        "actual_media_mime": args.media_mime,
    }
    try:
        with httpx.Client(trust_env=False, timeout=210) as client:
            response = client.post(args.base_url.rstrip("/") + "/v1/chat/completions", json=body, headers={header: token})
        with paths["response"].open("xb") as stream:
            stream.write(response.content)
        provenance.update(http_status=response.status_code, response_sha256=hashlib.sha256(response.content).hexdigest())
        if response.status_code != 200:
            provenance["status"] = "failed"
        else:
            found = genuine_review(response.json())
            if found:
                with paths["text"].open("x") as stream:
                    stream.write(found + "\n")
                provenance["status"] = "needs_review"
            else:
                provenance["status"] = "failed"
    except (httpx.HTTPError, ValueError):
        provenance["status"] = "failed"
    save_json(paths["provenance"], provenance)
    print(f"Actual-video machine review: {provenance['status']}; saved under {args.output_dir}")
    return int(provenance["status"] == "failed")


if __name__ == "__main__":
    raise SystemExit(main())
