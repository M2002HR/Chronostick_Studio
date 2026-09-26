#!/usr/bin/env python3

import argparse
import hashlib
import json


def derive_seed(episode: str, revision: str, clip: int, project_seed: int) -> int:
    value = f"{episode}:{revision}:{clip:02d}:{project_seed}".encode()
    return int.from_bytes(hashlib.sha256(value).digest()[:8], "big")


def main() -> None:
    parser = argparse.ArgumentParser(description="Derive stable, unique 64-bit seeds for ChronoStick clips")
    parser.add_argument("--episode", required=True)
    parser.add_argument("--revision", default="r001")
    parser.add_argument("--project-seed", required=True, type=int)
    parser.add_argument("--count", required=True, type=int)
    args = parser.parse_args()
    if args.project_seed < 0 or args.count < 1:
        parser.error("project-seed must be non-negative and count must be positive")
    items = [
        {"clip": clip, "seed": derive_seed(args.episode, args.revision, clip, args.project_seed)}
        for clip in range(1, args.count + 1)
    ]
    seeds = [item["seed"] for item in items]
    if len(seeds) != len(set(seeds)):
        raise SystemExit("derived seeds are not unique")
    print(json.dumps({"episode": args.episode, "revision": args.revision, "project_seed": args.project_seed, "clips": items}, indent=2))


if __name__ == "__main__":
    main()
