#!/usr/bin/env python3
"""Package deterministic dynamic H3 jobs; preparation never submits them."""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]
POLICY = "NO BACKGROUND MUSIC. Natural diegetic sound effects only."
AUDIO_SUFFIX = ("ABSOLUTELY ZERO BACKGROUND MUSIC FOR THE ENTIRE VIDEO. A completely silent soundtrack "
                "except for the individually listed tiny dry non-tonal physical SFX. Each event ends immediately; "
                "all time between events is absolute silence. No music on cuts or ending. No score, soundtrack, "
                "beat, melody, harmony, percussion, drone, pulse, riser, sting, sustained tone, continuous ambience "
                "or room tone. Silence throughout static inserts and resolved raw tail. No speech, singing, "
                "whispers, human vocalizations or voices. Never substitute musical sound design for a physical SFX.")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path)
    parser.add_argument("--revision", default="r001")
    parser.add_argument("--service-root", type=Path, required=True)
    args = parser.parse_args()
    ep = args.episode.resolve()
    if not ep.is_relative_to(REPO / "episodes") or not re.fullmatch(r"r\d{3}", args.revision):
        raise ValueError("Use a repository episode and rNNN revision")
    manifest = json.loads((ep / "episode.json").read_text())
    stages = {s["id"]: s for s in json.loads((ep / "pipeline-state.json").read_text())["stages"]}
    if any(stages[s]["status"] != "approved" for s in ("timed-direction", "prompts", "references")):
        raise ValueError("Job packaging requires reviewed direction/prompts/references")
    if manifest["generation_steps"] != 16:
        raise ValueError("Reference-first profile requires the approved 16-step setting")
    timing = json.loads((ep / "timestamps/timing-map.json").read_text())
    direction = json.loads((ep / "plan/clip-direction.json").read_text())
    refs = {e["id"]: e for e in json.loads((ep / "plan/reference-manifest.json").read_text())["entries"]}
    intake = json.loads((ep / "source/intake.json").read_text())
    project_seed = intake.get("project_seed")
    if not isinstance(project_seed, int) or isinstance(project_seed, bool) or project_seed < 0:
        raise ValueError("Persist a fixed project seed before building jobs")
    spec = importlib.util.spec_from_file_location("derive_seeds", REPO / "scripts/derive_clip_seeds.py")
    seeds = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(seeds)
    jobs, plan_entries, output_paths = [], [], []
    for number, (slot, clip) in enumerate(zip(timing["clips"], direction["clips"], strict=True), 1):
        if slot['id'] != clip['id']:
            raise ValueError('Timing and directing clip IDs must match in order')
        prompt = ep / slot["prompt_path"]
        text = prompt.read_text()
        if text.lstrip().startswith("---") or text.count(POLICY) != 1:
            raise ValueError("Prompt purity/audio lock failed")
        if any(text.count(f"<Picture {i}>") != 1 for i in range(1, len(clip["reference_ids"]) + 1)):
            raise ValueError("Exact ordered picture mapping missing")
        images = []
        for rid in clip["reference_ids"]:
            ref = refs[rid]
            image = REPO / ref["selected_path"]
            if ref["kind"] != "scene" or ref["review_status"] != "approved" or sha(image) != ref["sha256"]:
                raise ValueError("H3 must use reviewed unchanged single-scene production images")
            images.append({"path": ref["selected_path"], "role": "scene-and-style" if not images else "scene-state", "name": f"Picture {len(images)+1}"})
        if not 1 <= len(images) <= 9:
            raise ValueError("Unsupported H3 reference allocation")
        seed = seeds.derive_seed(ep.name, args.revision, number, project_seed)
        identity = f"episode-{ep.name[:3]}-{slot['id']}-{clip['slug']}-{args.revision}"
        base = ep.relative_to(REPO).as_posix()
        request = {"schema_version": "1.0", "template": "h3_ref2va", "profile": "youtube_shorts_hq",
                   "job_identity": identity, "prompt": {"file": prompt.relative_to(REPO).as_posix()},
                   "references": images, "generation": {"aspect_ratio": "9:16", "megapixel": 0.4,
                   "width": 480, "height": 864, "duration_seconds": slot["generation_request_seconds"], "fps": 24,
                   "steps": 16, "sampler": "res_multistep", "scheduler": "beta", "seed": seed,
                   "seed_mode": "fixed", "project_seed": project_seed, "lightning": False, "ref_image_size": "match"},
                   "audio": {"enabled": True, "mode": "sfx_only", "dialogue": False, "narration": False,
                             "music": False, "require_audio_stream": True, "prompt_suffix": AUDIO_SUFFIX},
                   "output": {"directory": base + "/renders/raw", "prefix": identity, "container": "mp4",
                              "overwrite": False, "editorial_directory": base + "/renders/editorial",
                              "editorial_duration_seconds": slot["duration_seconds"]},
                   "postprocess": {"concat": False, "upscale": False}}
        job_path = ep / "automation/jobs" / f"{slot['id']}-{clip['slug']}.json"
        output_paths.extend([REPO / request["output"][key] / (identity + ".mp4") for key in ("directory", "editorial_directory")])
        jobs.append((job_path, request))
        plan_entries.append({"clip_id": slot["id"], "job_path": job_path.relative_to(ep).as_posix(),
                             "job_identity": identity, "seed": seed, "prompt_path": slot["prompt_path"],
                             "prompt_sha256": sha(prompt), "reference_ids": clip["reference_ids"],
                             "reference_hashes": [refs[r]["sha256"] for r in clip["reference_ids"]],
                             "requested_seconds": slot["generation_request_seconds"],
                             "expected_raw_frames": slot["expected_raw_frame_count"], "editorial_frames": slot["frame_count"],
                             "editorial_seconds": slot["duration_seconds"], "raw_tail_hold_frames": slot["trim_raw_tail_frames"],
                             "normalization": "24-fps exact editorial trim; drop resolved raw tail, no time stretch"})
    if len({e["seed"] for e in plan_entries}) != len(plan_entries):
        raise ValueError("Derived seed collision")
    settings_path, plan_path = ep / "automation/batch-settings.json", ep / "automation/job-plan.json"
    if any(p.exists() for p in [p for p, _ in jobs] + output_paths + [settings_path, plan_path]):
        raise FileExistsError("Job package or media target already exists; create a reviewed new revision")
    service_sources = [args.service_root.resolve() / "src/comfy_video_service" / name for name in ("models.py", "resolver.py", "graph.py", "templates.py")]
    service_hashes = [{"path": str(p), "sha256": sha(p)} for p in service_sources]
    for path, request in jobs:
        write_new(path, request)
    settings = {"continue_on_error": True, "max_retries": 2, "concat_on_complete": False, "upscale_on_complete": False}
    write_new(settings_path, settings)
    write_new(plan_path, {"schema_version": "1.0", "episode_id": ep.name, "revision": args.revision,
                         "created_at": datetime.now(timezone.utc).isoformat(), "status": "prepared_not_submitted",
                         "production_profile": manifest["production_profile"], "project_seed": project_seed,
                         "timing_sha256": sha(ep / "timestamps/timing-map.json"),
                         "direction_sha256": sha(ep / "plan/clip-direction.json"),
                         "reference_manifest_sha256": sha(ep / "plan/reference-manifest.json"),
                         "service_sources": service_hashes, "jobs": plan_entries,
                         "job_hashes": [{"path": p.relative_to(ep).as_posix(), "sha256": sha(p)} for p, _ in jobs],
                         "audio_suffix_reason": "Service default would duplicate required policy; explicit silence-separated non-tonal suffix keeps resolved prompt policy count one.",
                         "execution": "Sequential GPU; complete live dry-run and a reviewed native 16-step duration/cut pilot before relying on final quality."})
    print(f"{len(jobs)} deterministic 16-step dynamic H3 jobs packaged; no generation submitted")


if __name__ == "__main__":
    main()
