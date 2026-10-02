#!/usr/bin/env python3
"""Build immutable long-form H3 requests from an explicit per-slot reference plan."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
POLICY = "NO BACKGROUND MUSIC. Natural diegetic sound effects only."


def repo_file(value: str) -> Path:
    path = (REPO / value).resolve()
    if not path.is_relative_to(REPO) or not path.is_file():
        raise ValueError(f"missing or out-of-repository file: {value}")
    return path


def load_object(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def derive_seed(project_seed: int, number: int) -> int:
    digest = hashlib.sha256(f"{project_seed}:{number}".encode("ascii")).digest()
    # The service persists seeds in signed SQLite INTEGER columns.
    return int.from_bytes(digest[:8], "big") & (2**63 - 1)


def build(episode: Path, plan: dict) -> list[tuple[Path, dict]]:
    if not episode.is_relative_to(REPO):
        raise ValueError("episode must be inside the repository")
    timing = load_object(episode / "timestamps/timing-map.json")
    episode_manifest = load_object(episode / "episode.json")
    if episode_manifest.get("picture_method_exceptions"):
        raise ValueError("Mixed-method Episode006 uses its frozen map-redirection package; do not rebuild controlled slots as H3 or resubmit retained candidates")
    steps = episode_manifest.get("generation_steps", 14)
    if steps not in (12, 14):
        raise ValueError("episode generation_steps must be 12 or 14")
    if steps == 12 and episode_manifest.get("production_profile") != "h3-long-5s-12step-16x9":
        raise ValueError("12-step jobs require the matching episode production profile")
    count = timing.get("slot_count")
    if not isinstance(count, int) or count < 120 or count > 180:
        raise ValueError("timing map must contain 120–180 five-second slots")
    project_seed = plan.get("project_seed")
    if not isinstance(project_seed, int) or not 0 <= project_seed <= 2**64 - 1:
        raise ValueError("job plan needs a nonnegative 64-bit project_seed")
    slots = plan.get("slots")
    if plan.get("schema_version") != "1.0" or not isinstance(slots, list):
        raise ValueError("job plan needs schema_version 1.0 and slots array")
    if len(slots) != count:
        raise ValueError(f"job plan has {len(slots)} entries; timing requires {count}")

    records: list[tuple[Path, dict]] = []
    seeds: set[int] = set()
    for number, slot in enumerate(slots, 1):
        if not isinstance(slot, dict) or slot.get("number") != number:
            raise ValueError(f"job plan requires ordered slot {number:03d}")
        refs = slot.get("references")
        revision = slot.get("revision")
        if not isinstance(refs, list) or not 1 <= len(refs) <= 2:
            raise ValueError(f"slot {number:03d} needs one or two references")
        if not isinstance(revision, int) or not 1 <= revision <= 999:
            raise ValueError(f"slot {number:03d} needs revision 1–999")
        prompt = episode / f"prompts/clip-{number:03d}.md"
        if not prompt.is_file():
            raise ValueError(f"missing prompt: {prompt}")
        prompt_text = prompt.read_text(encoding="utf-8")
        if prompt_text.count(POLICY) != 1 or "16:9" not in prompt_text:
            raise ValueError(f"slot {number:03d} prompt lacks format/audio contract")
        tags = {int(n) for n in re.findall(r"<Picture\s+(\d+)>", prompt_text, flags=re.I)}
        if tags != set(range(1, len(refs) + 1)):
            raise ValueError(f"slot {number:03d} Picture tags do not match reference order")
        references = []
        for position, value in enumerate(refs, 1):
            if not isinstance(value, str):
                raise ValueError(f"slot {number:03d} reference path must be a string")
            image = repo_file(value)
            references.append({"path": str(image.relative_to(REPO)), "role": "scene", "name": f"Picture {position}"})
        seed = slot.get("seed", derive_seed(project_seed, number))
        if not isinstance(seed, int) or not 0 <= seed <= 2**63 - 1 or seed in seeds:
            raise ValueError(f"slot {number:03d} seed is invalid or repeated")
        seeds.add(seed)
        prefix = f"clip-{number:03d}-shot-r{revision:03d}"
        for directory in ("renders/raw", "renders/editorial"):
            if (episode / directory / f"{prefix}.mp4").exists():
                raise ValueError(f"slot {number:03d} output already exists; increment revision")
        root_relative = episode.relative_to(REPO)
        job = {
            "schema_version": "1.0", "template": "h3_ref2va", "profile": "youtube_shorts_hq",
            "job_identity": f"{episode.name}:clip-{number:03d}:r{revision:03d}",
            "prompt": {"file": str(prompt.relative_to(REPO))},
            "references": references,
            "generation": {
                "aspect_ratio": "16:9", "megapixel": 0.6, "width": 1024, "height": 576,
                "duration_seconds": 5, "fps": 24, "steps": steps,
                "sampler": "res_multistep", "scheduler": "beta", "seed": seed,
                "seed_mode": "fixed", "lightning": False, "ref_image_size": "match",
            },
            "audio": {"enabled": True, "mode": "sfx_only", "dialogue": False,
                      "narration": False, "music": False, "require_audio_stream": True},
            "output": {"directory": str(root_relative / "renders/raw"), "prefix": prefix,
                       "container": "mp4", "overwrite": False,
                       "editorial_directory": str(root_relative / "renders/editorial"),
                       "editorial_duration_seconds": 5},
            "postprocess": {"concat": False, "upscale": False},
        }
        records.append((episode / f"automation/jobs/clip-{number:03d}.json", job))
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path)
    parser.add_argument("--plan", type=Path, help="defaults to EPISODE/automation/job-plan.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    episode = args.episode.resolve()
    try:
        plan = load_object(args.plan or episode / "automation/job-plan.json")
        records = build(episode, plan)
        occupied = [path for path, _ in records if path.exists()]
        if occupied:
            raise ValueError(f"refusing to overwrite {len(occupied)} existing job JSON files; revise in Git")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    if args.dry_run:
        print(f"Validated {len(records)} long-form jobs; no files written")
        return 0
    for path, job in records:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} long-form jobs to {episode / 'automation/jobs'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
