#!/usr/bin/env python3
"""Create a reference-first Short and optionally relocate its original video."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess


REPO = Path(__file__).resolve().parents[1]
STAGES = [
    ("intake", "chronostick-pipeline"),
    ("reference-transcription", "chronostick-transcribe"),
    ("reference-analysis", "chronostick-reference-video"),
    ("scenario-script", "chronostick-script"),
    ("storyboard", "chronostick-storyboard"),
    ("references", "chronostick-references"),
    ("voice", "chronostick-pipeline"),
    ("voice-transcription", "chronostick-transcribe"),
    ("timed-direction", "chronostick-shot-plan"),
    ("prompts", "chronostick-clip-prompts"),
    ("jobs-preflight", "chronostick-generation-jobs"),
    ("generation", "chronostick-batch"),
    ("review", "chronostick-review"),
    ("finish", "chronostick-finish"),
    ("youtube", "chronostick-youtube"),
]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode_id")
    parser.add_argument("--title", required=True)
    parser.add_argument("--reference-video", type=Path, required=True)
    parser.add_argument("--reference-url", required=True)
    parser.add_argument("--target-seconds", type=int, default=30, choices=range(20, 31))
    parser.add_argument("--move-reference", action="store_true")
    parser.add_argument("--episodes-root", type=Path, default=REPO / "episodes")
    args = parser.parse_args()
    if not re.fullmatch(r"\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*", args.episode_id):
        parser.error("Use NNN-lowercase-hyphenated-slug")
    if not args.title.strip() or not args.reference_video.is_file():
        parser.error("A nonempty title and existing reference video are required")
    root = args.episodes_root.resolve() / args.episode_id
    if root.exists():
        parser.error(f"Refusing to replace existing episode: {root}")
    video = args.reference_video.resolve()
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)
    ]))
    if not any(s.get("codec_type") == "video" for s in probe.get("streams", [])):
        parser.error("Reference has no video stream")
    original_hash = sha256(video)
    for directory in ("source/reference-video", "source/research", "script", "audio",
                      "timestamps", "plan/storyboard", "prompts", "automation/jobs",
                      "renders/raw", "renders/editorial", "renders/final-selected",
                      "final", "delivery/youtube"):
        (root / directory).mkdir(parents=True, exist_ok=False)
    destination = root / "source/reference-video" / f"reference-{args.episode_id[4:]}-r001{video.suffix.lower()}"
    # Copy and verify before unlinking the incoming file. Never transcode it.
    with video.open("rb") as source, destination.open("xb") as target:
        shutil.copyfileobj(source, target)
    if sha256(destination) != original_hash:
        raise RuntimeError("Reference copy hash mismatch; incoming original retained")
    now = datetime.now(timezone.utc).isoformat()
    reference = {
        "id": "reference-video", "kind": "video", "path": destination.relative_to(root).as_posix(),
        "url": args.reference_url, "title": args.title.strip(), "original_name": video.name,
        "sha256": original_hash, "bytes": destination.stat().st_size,
        "provenance": "User-supplied download; URL supplied by user; byte identity preserved",
    }
    write_json(root / "source/reference-video/manifest.json", {
        "schema_version": "1.0", "role": "creative-reference-and-unverified-story-input",
        "influence_goal": "Close story and directing adaptation in original Spanish and ChronoStick style",
        "items": [reference], "created_at": now,
    })
    write_json(root / "source/reference-video/probe.json", probe)
    write_json(root / "source/intake.json", {
        "title_supplied": args.title.strip(), "reference_url": args.reference_url,
        "reference_manifest": "source/reference-video/manifest.json", "target_language": "es",
        "target_seconds": args.target_seconds, "target_decision": f"{args.target_seconds}-second working target within user-requested 20–30-second range",
        "source_status": "reference_video_only_unverified", "project_seed": None,
    })
    write_json(root / "episode.json", {
        "schema_version": "1.0", "id": args.episode_id, "format": "short",
        "workflow": "reference-first-v1", "title": args.title.strip(),
        "production_profile": "h3-short-dynamic-16step-20-30s", "target_language": "es",
        "target_seconds": args.target_seconds, "generation_steps": 16,
        "clip_duration_seconds": {"minimum": 4, "maximum": 7},
        "voice_provider": "google_vids",
        "voice_direction": {"provider": "google_vids", "selection": "used", "status": "missing",
                            "skill": "chronostick-voice-direction", "script_path": None,
                            "notes_path": None, "validation_path": None},
        "accepted_voice": None, "accepted_timing_map": None,
        "picture_master": None, "distribution_master": None,
        "next_action": "Extract reference speech and word/segment timestamps through Ajil",
    })
    write_json(root / "pipeline-state.json", {
        "schema_version": "2.0", "workflow": "reference-first-v1", "episode_id": args.episode_id,
        "current_stage": "reference-transcription", "updated_at": now,
        "stages": [dict(id=name, skill=skill, status="validated" if name == "intake" else "missing",
                        inputs=[reference["path"]] if name == "intake" else [],
                        outputs=["source/intake.json", "source/reference-video/manifest.json", "source/reference-video/probe.json"] if name == "intake" else [],
                        validated_at=now if name == "intake" else None,
                        approved_at=None, approved_by=None, decision_notes=None, next_action=None)
                   for name, skill in STAGES],
    })
    (root / "README.md").write_text(
        f"# {args.episode_id} — {args.title.strip()}\n\n"
        "Reference-first Spanish Short; user-requested dynamic production route.\n\n"
        f"- Working target: {args.target_seconds} seconds; range 20–30 seconds.\n"
        "- Profile: `h3-short-dynamic-16step-20-30s`; editorial clips 4–7 seconds, 16 steps.\n"
        f"- Original reference: `{reference['path']}`; bytes preserved, provenance recorded.\n"
        "- Transcript, analysis, scenario, storyboard, production references, accepted voice, timings, renders and masters: missing.\n"
        "- Creative approvals: none.\n\n"
        "## Next action\n\nExtract the reference through Ajil, inspect its actual video beside the transcript, then prepare a scenario and neutral sketch storyboard for user review.\n",
        encoding="utf-8",
    )
    if args.move_reference:
        # All provenance exists and the verified copy is complete before moving.
        if sha256(video) != original_hash:
            raise RuntimeError("Incoming reference changed during intake; original retained")
        video.unlink()
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
