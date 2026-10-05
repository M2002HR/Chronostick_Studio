#!/usr/bin/env python3
"""Copy one reviewed contiguous chapter's immutable H3 jobs into a batch folder."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path)
    parser.add_argument("chapter_id", help="lowercase letters, digits and hyphens")
    parser.add_argument("--first", type=int, required=True)
    parser.add_argument("--last", type=int, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.chapter_id):
        parser.error("invalid chapter_id")
    episode = args.episode.resolve()
    try:
        timing = json.loads((episode / "timestamps/timing-map.json").read_text(encoding="utf-8"))
        count = timing["slot_count"]
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        parser.error(f"invalid timing map: {exc}")
    if not 1 <= args.first <= args.last <= count:
        parser.error(f"slot range must be between 1 and {count}")
    target = episode / "automation/chapters" / args.chapter_id
    if target.exists():
        parser.error(f"refusing to replace staged chapter: {target}")
    originals = [episode / f"automation/jobs/clip-{number:03d}.json" for number in range(args.first, args.last + 1)]
    for path in originals:
        if not path.is_file() or not path.stat().st_size:
            parser.error(f"missing/empty approved job: {path}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            parser.error(f"invalid job {path}: {exc}")
        number = int(path.stem.split("-")[1])
        identity = data.get("job_identity")
        if not isinstance(identity, str) or identity.split(":clip-")[-1].split(":r")[0] != f"{number:03d}":
            parser.error(f"job identity does not match slot {number:03d}")
    jobs_dir = target / "jobs"
    jobs_dir.mkdir(parents=True)
    records = []
    for source in originals:
        raw = source.read_bytes()
        (jobs_dir / source.name).write_bytes(raw)
        records.append({"path": str(source.relative_to(episode)), "sha256": hashlib.sha256(raw).hexdigest()})
    (target / "manifest.json").write_text(json.dumps({
        "schema_version": "1.0", "chapter_id": args.chapter_id,
        "first_slot": args.first, "last_slot": args.last, "job_count": len(records),
        "source_jobs": records, "batch_id": None, "launch_status": "not_submitted",
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Staged {len(records)} jobs in {jobs_dir}; no generation submitted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
