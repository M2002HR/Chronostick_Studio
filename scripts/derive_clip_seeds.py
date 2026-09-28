#!/usr/bin/env python3

import argparse
import hashlib
import json


def derive_seed(episode_id: str, revision: str, clip_number: int, project_seed: int) -> int:
    material = f"{episode_id}|{revision}|{clip_number:02d}|{project_seed}".encode("utf-8")
    return int(hashlib.sha256(material).hexdigest()[:16], 16) & ((1 << 63) - 1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Derive deterministic unique clip seeds.")
    parser.add_argument("--episode-id", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--clip-count", required=True, type=int)
    parser.add_argument("--project-seed", required=True, type=int)
    args = parser.parse_args()

    if args.clip_count < 1:
        parser.error("--clip-count must be positive")
    if args.project_seed < 0:
        parser.error("--project-seed must be non-negative")

    seeds = {
        f"clip-{clip_number:02d}": derive_seed(
            args.episode_id, args.revision, clip_number, args.project_seed
        )
        for clip_number in range(1, args.clip_count + 1)
    }
    if len(set(seeds.values())) != len(seeds):
        raise SystemExit("derived seed collision")
    print(json.dumps(seeds, indent=2))


if __name__ == "__main__":
    main()
