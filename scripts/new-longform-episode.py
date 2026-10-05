#!/usr/bin/env python3
"""Create an honest, stage-aware long-form episode workspace without media generation."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
EPISODE_ID = re.compile(r"^[0-9]{3}-[a-z0-9]+(?:-[a-z0-9]+)*$")
STAGES = [
    ("00", "intake", "chronostick-longform-pipeline"),
    ("01", "research", "chronostick-longform-script"),
    ("02", "spanish-story", "chronostick-longform-script"),
    ("02a", "google-vids-voice-direction", "chronostick-longform-pipeline"),
    ("03", "voice-timing", "chronostick-longform-timing"),
    ("04", "visual-direction", "chronostick-longform-visual-direction"),
    ("05", "shot-plan", "chronostick-longform-shot-plan"),
    ("06", "references", "chronostick-longform-assets"),
    ("07", "animatic-pilot", "chronostick-longform-visual-direction"),
    ("08", "video-prompts", "chronostick-longform-prompts"),
    ("09", "jobs-preflight", "chronostick-longform-jobs"),
    ("10", "generation-review", "chronostick-longform-review"),
    ("11", "finish", "chronostick-longform-finish"),
    ("12", "youtube-closeout", "chronostick-longform-youtube"),
]
DIRS = [
    "source", "script", "audio", "timestamps", "plan", "prompts",
    "automation/jobs", "automation/retries", "renders/raw", "renders/editorial",
    "renders/final-selected", "final", "delivery/youtube",
]


def save_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode_id", help="NNN-lowercase-hyphenated-slug")
    parser.add_argument("--title", required=True)
    parser.add_argument("--source", type=Path, help="Original supplied source; copied byte-for-byte")
    parser.add_argument("--reference-video", type=Path, help="Example video; copied byte-for-byte into the episode")
    parser.add_argument("--reference-transcript", type=Path, help="Transcript of the example video; copied byte-for-byte")
    parser.add_argument("--reference-influence-goal", default="Use the supplied example as a creative baseline for rhythm, visual explanation and tone, while independently verifying historical claims")
    parser.add_argument("--episodes-root", type=Path, default=REPO / "episodes", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not EPISODE_ID.fullmatch(args.episode_id):
        parser.error("episode_id must be NNN-lowercase-hyphenated-slug")
    if not args.title.strip():
        parser.error("title must not be empty")
    if args.source and not args.source.is_file():
        parser.error(f"source file does not exist: {args.source}")
    if bool(args.reference_video) != bool(args.reference_transcript):
        parser.error("--reference-video and --reference-transcript must be supplied together")
    for supplied in (args.reference_video, args.reference_transcript):
        if supplied and not supplied.is_file():
            parser.error(f"reference file does not exist: {supplied}")
    root = args.episodes_root.resolve() / args.episode_id
    if root.exists():
        parser.error(f"refusing to replace an existing episode: {root}")

    root.mkdir(parents=True)
    for directory in DIRS:
        (root / directory).mkdir(parents=True, exist_ok=True)

    source_record: dict[str, str | None] = {
        "status": "reference_transcript_only" if args.reference_video and not args.source else "missing",
        "path": None, "sha256": None,
    }
    if args.source:
        raw = args.source.read_bytes()
        target = root / "source/source-en.md"
        target.write_bytes(raw)
        source_record = {"status": "supplied_unverified", "path": "source/source-en.md", "sha256": hashlib.sha256(raw).hexdigest()}

    reference_record = {"status": "not_supplied", "manifest": None, "influence_goal": None}
    if args.reference_video and args.reference_transcript:
        reference_dir = root / "source/reference-video"
        reference_dir.mkdir()
        video_target = reference_dir / f"reference-video{args.reference_video.suffix.lower()}"
        transcript_target = reference_dir / f"reference-transcript{args.reference_transcript.suffix.lower()}"
        for supplied, target in ((args.reference_video, video_target), (args.reference_transcript, transcript_target)):
            shutil.copyfile(supplied, target)
        items = []
        for identifier, kind, supplied, target in (
            ("reference-video", "video", args.reference_video, video_target),
            ("reference-transcript", "transcript", args.reference_transcript, transcript_target),
        ):
            items.append({
                "id": identifier, "kind": kind,
                "path": target.relative_to(root).as_posix(), "url": None,
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "timecode": None, "original_name": supplied.name,
            })
        save_json(reference_dir / "manifest.json", {
            "schema_version": "1.0", "influence_goal": args.reference_influence_goal,
            "items": items,
        })
        reference_record = {
            "status": "supplied", "manifest": "source/reference-video/manifest.json",
            "influence_goal": args.reference_influence_goal,
        }

    episode = {
        "schema_version": "1.0",
        "id": args.episode_id,
        "format": "longform",
        "title": args.title.strip(),
        "production_profile": "h3-long-5s-14step-16x9",
        "target_language": "es",
        "duration_seconds": {"minimum": 600, "maximum": 900},
        "source": source_record,
        "style_authority": "assets/styles/style-detailed-cinematic-stick-history-r001.png",
        "accepted_voice": None,
        "accepted_timing_map": None,
        "picture_master": None,
        "distribution_master": None,
        "next_action": (
            "Inspect the reference video beside its transcript and record source/reference-video/intake-review.md"
            if args.reference_video else
            "Verify source claims and write the Spanish story architecture"
            if args.source else "Supply a historical source or a reference video with transcript"
        ),
    }
    save_json(root / "episode.json", episode)
    save_json(root / "source/intake.json", {
        "schema_version": "1.0", "title_supplied": args.title.strip(),
        "source": source_record, "reference_video_role": "creative-example-and-story-outline-only",
        "reference_video": reference_record,
        "project_seed": None, "notes": [],
    })
    save_json(root / "pipeline-state.json", {
        "schema_version": "1.0", "episode_id": args.episode_id,
        "stages": [
            {"id": identifier, "name": name, "skill": skill,
             "status": "skipped" if identifier == "02a" else ("draft" if identifier == "00" and (args.source or args.reference_video) else "missing"),
             "inputs": [], "outputs": [], "approved_by": None,
             "decision_notes": None, "next_action": None}
            for identifier, name, skill in STAGES
        ],
    })
    (root / "README.md").write_text(
        f"# {args.episode_id} — {args.title.strip()}\n\n"
        "## Status\n\n"
        f"- format: long-form, 10–15 minutes, Spanish, landscape 16:9\n"
        f"- production profile: `h3-long-5s-14step-16x9`\n"
        f"- source: {source_record['status']}\n"
        f"- reference video and transcript: {reference_record['status']}\n"
        "- script, accepted voice, word timing, shot plan, references, prompts, renders, and masters: missing\n"
        "- review approvals: none\n\n"
        "## Next action\n\n"
        f"{episode['next_action']}.\n\n"
        "Follow `docs/longform/workflow.md`; record each real artifact and decision here and in `pipeline-state.json`.\n",
        encoding="utf-8",
    )
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
