#!/usr/bin/env python3
"""Freeze image-tool requests and archive candidates; never infer art approval."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

from PIL import Image

REPO = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def repo_file(repo, relative):
    if not isinstance(relative, str) or not relative:
        raise ValueError("Missing repository file path")
    path = (repo / relative).resolve()
    if not path.is_relative_to(repo.resolve()) or not path.is_file() or not path.stat().st_size:
        raise ValueError(f"Missing/empty/escaped repository file: {relative}")
    return path


def freeze(repo, episode, ids, revision, name, style):
    if not re.fullmatch(r"r\d{3}", revision) or not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError("Use rNNN revision and lowercase request-group name")
    state = json.loads((episode / "pipeline-state.json").read_text())
    stages = {s["id"]: s for s in state["stages"]}
    if any(stages[k]["status"] != "approved" for k in ("scenario-script", "storyboard")):
        raise ValueError("Production design requires actual scenario/storyboard acceptance")
    manifest = json.loads((episode / "plan/reference-manifest.json").read_text())
    entries = {e["id"]: e for e in manifest["entries"]}
    if not ids or len(set(ids)) != len(ids) or any(i not in entries for i in ids):
        raise ValueError("Choose unique known reference IDs")
    style_path = repo_file(repo, style)
    if "storyboard" in style_path.parts:
        raise ValueError("Neutral sketches cannot be production rendering inputs")
    output = episode / "plan/references" / f"{name}-requests-{revision}.json"
    if output.exists():
        raise FileExistsError(output)
    requests = []
    for ref_id in ids:
        entry = entries[ref_id]
        prompt_path = repo_file(repo, entry.get("prompt_repo_path"))
        allowed = (repo / "prompts/image/episodes" / episode.name).resolve()
        if not prompt_path.is_relative_to(allowed):
            raise ValueError("Image prompt must be in the episode's pure prompt directory")
        prompt = prompt_path.read_text()
        if prompt.lstrip().startswith("---"):
            raise ValueError("Prompt must not contain YAML frontmatter")
        destination = f"assets/episodes/{episode.name}/references/{ref_id}-{revision}.png"
        if (repo / destination).exists():
            raise FileExistsError(destination)
        inputs = [{"path": style, "sha256": sha(style_path), "role": "rendering authority only"}]
        for dependency in entry.get("dependencies", []):
            dep = entries[dependency]
            if dep.get("review_status") != "approved" or not dep.get("review_decision"):
                raise ValueError(f"Unreviewed image dependency: {dependency}")
            dep_path = repo_file(repo, dep.get("selected_path"))
            if sha(dep_path) != dep.get("sha256"):
                raise ValueError(f"Changed image dependency: {dependency}")
            inputs.append({"path": dep["selected_path"], "sha256": dep["sha256"], "role": dependency})
        for item in entry.get("content_images", []):
            path = repo_file(repo, item["path"])
            if "storyboard" in path.parts:
                raise ValueError("Sketches remain planning evidence, not image-generation inputs")
            inputs.append({"path": item["path"], "sha256": sha(path), "role": item["role"]})
        if len(inputs) > 5:
            raise ValueError(f"Image tool accepts at most five input images: {ref_id}. Inherit identities from reviewed scene anchors without losing shot coverage.")
        requests.append({"id": ref_id, "prompt_repo_path": entry["prompt_repo_path"],
                         "prompt": prompt, "prompt_sha256": sha(prompt_path), "input_images": inputs,
                         "referenced_image_repo_paths": [i["path"] for i in inputs],
                         "destination_repo_path": destination, "transparent_background": False,
                         "storyboard_panel_ids": entry["storyboard_panel_ids"]})
    save_new(output, {"created_at": datetime.now(timezone.utc).isoformat(), "revision": revision,
                      "tool": "image_gen.imagegen", "requests": requests})
    return output


def verify(repo, request_path):
    request = json.loads(request_path.read_text())
    for item in request["requests"]:
        if len(item["input_images"]) > 5:
            raise ValueError(f"Image tool accepts at most five input images: {item['id']}")
        if hashlib.sha256(item["prompt"].encode()).hexdigest() != item["prompt_sha256"]:
            raise ValueError(f"Changed frozen prompt: {item['id']}")
        if sha(repo_file(repo, item["prompt_repo_path"])) != item["prompt_sha256"]:
            raise ValueError(f"Current prompt differs from request snapshot: {item['id']}")
        for image in item["input_images"]:
            if sha(repo_file(repo, image["path"])) != image["sha256"]:
                raise ValueError(f"Changed generation input: {item['id']}/{image['role']}")
    return request


def ingest(repo, episode, request_path, ref_id, source):
    request = json.loads(request_path.read_text())
    matches = [i for i in request["requests"] if i["id"] == ref_id]
    if len(matches) != 1:
        raise ValueError("Generated result must match exactly one frozen request")
    item = matches[0]
    destination = (repo / item["destination_repo_path"]).resolve()
    allowed = (repo / "assets/episodes" / episode.name / "references").resolve()
    if not destination.is_relative_to(allowed):
        raise ValueError("Generated destination escapes the episode asset directory")
    result_path = request_path.with_name(request_path.stem.replace("-requests-", f"-{ref_id}-result-") + ".json")
    if destination.exists() or result_path.exists():
        raise FileExistsError(destination if destination.exists() else result_path)
    with Image.open(source) as image:
        image.verify()
    with Image.open(source) as image:
        width, height = image.size
        if abs(width / height - 9 / 16) > 0.03:
            raise ValueError("Candidate is not a portrait 9:16 composition")
    destination.parent.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    with destination.open("xb") as stream:
        stream.write(data)
    save_new(result_path, {"archived_at": datetime.now(timezone.utc).isoformat(), "id": ref_id,
                          "revision": request["revision"], "request_path": str(request_path.relative_to(episode)),
                          "request_sha256": sha(request_path), "source_path": str(source.resolve()),
                          "path": item["destination_repo_path"], "sha256": sha(destination),
                          "dimensions": [width, height], "review_status": "needs_review"})
    # No selected_path/review_status/approval update: an actual image review follows.
    return destination, result_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    frozen = sub.add_parser("freeze")
    frozen.add_argument("--episode", type=Path, required=True)
    frozen.add_argument("--ids", nargs="+", required=True)
    frozen.add_argument("--revision", required=True)
    frozen.add_argument("--name", required=True)
    frozen.add_argument("--style-reference", required=True)
    checked = sub.add_parser("verify")
    checked.add_argument("--request", type=Path, required=True)
    imported = sub.add_parser("ingest")
    imported.add_argument("--episode", type=Path, required=True)
    imported.add_argument("--request", type=Path, required=True)
    imported.add_argument("--id", required=True)
    imported.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "freeze":
        print(freeze(REPO, args.episode.resolve(), args.ids, args.revision, args.name, args.style_reference))
    elif args.command == "verify":
        verify(REPO, args.request.resolve())
        print("Frozen prompts and generation input hashes verified")
    else:
        for path in ingest(REPO, args.episode.resolve(), args.request.resolve(), args.id, args.source):
            print(path)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        sys.exit(1)
