#!/usr/bin/env python3
"""Validate paste-ready Vids tags against the registered account vocabulary."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


REPO = Path(__file__).resolve().parents[1]
TAG_DOC = REPO / "docs/google-vids-voice-direction.md"
MAX_CHARACTERS = 2500


def registered_tags():
    rows = "\n".join(line for line in TAG_DOC.read_text().splitlines() if line.startswith("|"))
    return set(re.findall(r"`(\[[a-z]+(?: [a-z]+)*\])`", rows))


def normalize(text):
    return " ".join(text.split())


def validate(clean, tagged, scenes=None):
    errors = []
    found = re.findall(r"\[[^\[\]\n]*\]", tagged)
    remaining = re.sub(r"\[[^\[\]\n]*\]", "", tagged)
    if not clean.strip() or not tagged.strip():
        errors.append("Clean narration and tagged script must be nonempty")
    if not found:
        errors.append("No registered delivery tags in the tagged script")
    if "[" in remaining or "]" in remaining:
        errors.append("Malformed or unmatched bracket syntax")
    for tag in sorted(set(found)):
        if tag not in registered_tags():
            errors.append(f"Unregistered tag: {tag}")
        if tag == "[whisper]":
            errors.append("Whisper is forbidden by the user's voice rule")
    if normalize(clean) != normalize(remaining):
        errors.append("Tagged script changes spoken words, punctuation or order")
    if scenes is None:
        if len(tagged) > MAX_CHARACTERS:
            errors.append("Master exceeds 2,500 characters without ordered scene inputs")
    else:
        if not scenes:
            errors.append("Scene list is empty")
        for index, scene in enumerate(scenes, 1):
            if not scene.strip() or len(scene) > MAX_CHARACTERS:
                errors.append(f"Scene {index} is empty or exceeds 2,500 characters")
        if normalize(" ".join(scenes)) != normalize(tagged):
            errors.append("Ordered scenes do not reconstruct the tagged master")
    return {
        "status": "passed" if not errors else "failed", "errors": errors,
        "clean_sha256": hashlib.sha256(clean.encode()).hexdigest(),
        "tagged_sha256": hashlib.sha256(tagged.encode()).hexdigest(),
        "characters": len(tagged), "tag_count": len(found),
        "tag_counts": dict(Counter(found)), "scene_count": len(scenes) if scenes is not None else 1,
        "spoken_text_identical_ignoring_whitespace": normalize(clean) == normalize(remaining),
        "catalog": "docs/google-vids-voice-direction.md", "actual_voice_accepted": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean", type=Path, required=True)
    parser.add_argument("--tagged", type=Path, required=True)
    parser.add_argument("--scenes-dir", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if not args.clean.is_file() or not args.tagged.is_file():
        parser.error("Missing clean or tagged script")
    scenes = None
    if args.scenes_dir:
        paths = sorted(args.scenes_dir.glob("scene-*.txt"))
        expected = [f"scene-{index:02}.txt" for index in range(1, len(paths) + 1)]
        if [p.name for p in paths] != expected:
            parser.error("Scenes must be consecutively numbered from scene-01.txt")
        scenes = [p.read_text() for p in paths]
    report = validate(args.clean.read_text(), args.tagged.read_text(), scenes)
    if args.report:
        with args.report.open("x", encoding="utf-8") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    print(f"Google Vids script: {report['status']}; {report['characters']} characters, {report['tag_count']} tags")
    for error in report["errors"]:
        print("FAIL", error)
    return int(bool(report["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
