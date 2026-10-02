#!/usr/bin/env python3
"""Stage-aware static validation for a ChronoStick long-form episode."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
POLICY = "NO BACKGROUND MUSIC. Natural diegetic sound effects only."
STAGE_FILES = {
    "00": ["source/intake.json"],
    "01": ["source/claims.json", "source/research-notes.md"],
    "02": ["script/story-architecture.md", "script/narration-es.md", "script/fidelity-ledger.json"],
    "02a": ["script/voiceover-google-vids-es.md", "script/voice-direction-notes.md"],
    "03": ["timestamps/word-timestamps-source.csv", "timestamps/timing-map.json"],
    "04": ["plan/visual-direction.md"],
    "05": ["plan/shot-plan.md", "plan/story-state-ledger.json", "plan/reference-manifest.json", "plan/map-manifest.json", "plan/text-events.json"],
    "06": ["plan/reference-manifest.json"],
    "07": ["plan/animatic-review.md", "plan/pilot-review.md"],
    "09": ["automation/job-plan.json", "automation/batch-settings.json", "automation/preflight.json"],
    "10": ["renders/selection-manifest.json"],
    "11": ["final/distribution-review.md"],
    "12": ["delivery/youtube/metadata.json", "delivery/youtube/metadata.md"],
}
PROMPT_RE = re.compile(r"^clip-(\d{3})\.md$")
JOB_RE = re.compile(r"^clip-(\d{3})\.json$")
SELECTED_RE = re.compile(r"^clip-(\d{3})-.*-r\d{3}\.(?:mp4|mkv|webm)$")


class Audit:
    def __init__(self, episode: Path):
        self.episode = episode
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def json(self, path: Path) -> dict | list | None:
        if not path.is_file():
            self.error(f"missing JSON: {path}")
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            self.error(f"invalid JSON {path}: {exc}")
            return None

    def required_file(self, relative: str) -> None:
        path = self.episode / relative
        if not path.is_file() or path.stat().st_size == 0:
            self.error(f"approved-stage artifact is absent or empty: {relative}")

    def within_repo(self, value: str, label: str) -> Path | None:
        path = (REPO / value).resolve()
        if not path.is_relative_to(REPO):
            self.error(f"{label} escapes repository: {value}")
            return None
        return path


def numbered_files(audit: Audit, directory: Path, pattern: re.Pattern[str]) -> dict[int, Path]:
    found: dict[int, Path] = {}
    if not directory.exists():
        return found
    for path in sorted(directory.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        match = pattern.fullmatch(path.name)
        if not match:
            audit.error(f"unexpected numbered artifact: {path}")
            continue
        number = int(match.group(1))
        if number < 1 or number in found:
            audit.error(f"duplicate or invalid slot number: {path}")
        found[number] = path
    return found


def check_reference_video(audit: Audit, intake: dict, intake_approved: bool, direction_approved: bool) -> set[str]:
    record = intake.get("reference_video")
    if record is None:
        return set()
    if not isinstance(record, dict):
        audit.error("intake reference_video must be an object")
        return set()
    status = record.get("status")
    if status not in {"not_supplied", "supplied"}:
        audit.error("intake reference_video status must be not_supplied or supplied")
        return set()
    if status == "not_supplied":
        if (audit.episode / "source/reference-video/manifest.json").exists():
            audit.error("reference-video manifest exists but intake still says not_supplied")
        return set()
    relative = record.get("manifest")
    if relative != "source/reference-video/manifest.json":
        audit.error("supplied reference video needs source/reference-video/manifest.json")
        return set()
    manifest = audit.json(audit.episode / relative)
    if not isinstance(manifest, dict):
        return set()
    if manifest.get("schema_version") != "1.0" or not isinstance(manifest.get("items"), list) or not manifest["items"]:
        audit.error("reference-video manifest needs schema_version 1.0 and nonempty items")
        return set()
    if not isinstance(manifest.get("influence_goal"), str) or not manifest["influence_goal"].strip():
        audit.error("reference-video manifest needs the user's influence goal")
    elif record.get("influence_goal") != manifest["influence_goal"]:
        audit.error("reference-video influence goal differs between intake and manifest")
    ids: set[str] = set()
    kinds: set[str] = set()
    for item in manifest["items"]:
        if not isinstance(item, dict):
            audit.error("reference-video item must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id or item_id in ids:
            audit.error("reference-video item IDs must be nonempty and unique")
        else:
            ids.add(item_id)
        if item.get("kind") not in {"video", "transcript", "frame", "screenshot"}:
            audit.error(f"reference-video item {item_id} has invalid kind")
        else:
            kinds.add(item["kind"])
        local, url = item.get("path"), item.get("url")
        if bool(local) == bool(url):
            audit.error(f"reference-video item {item_id} needs exactly one path or URL")
        elif local:
            if not isinstance(local, str):
                audit.error(f"reference-video item {item_id} path must be a string")
                continue
            target = (audit.episode / local).resolve()
            if not target.is_relative_to((audit.episode / "source/reference-video").resolve()) or not target.is_file():
                audit.error(f"reference-video item {item_id} path is absent or outside source/reference-video")
            elif hashlib.sha256(target.read_bytes()).hexdigest() != item.get("sha256"):
                audit.error(f"reference-video item {item_id} SHA-256 does not match")
        elif not isinstance(url, str) or not url.startswith("https://"):
            audit.error(f"reference-video item {item_id} needs an https URL")
    if intake_approved and {"video", "transcript"}.issubset(kinds):
        audit.required_file("source/reference-video/intake-review.md")
    if direction_approved:
        audit.required_file("plan/reference-video-analysis.md")
    return kinds


def check_voice_direction(audit: Audit) -> None:
    spoken = audit.episode / "script/narration-es.md"
    tagged = audit.episode / "script/voiceover-google-vids-es.md"
    if not tagged.is_file():
        return
    if not spoken.is_file():
        audit.error("Google Vids tagged script exists without clean spoken narration")
        return
    clean = re.sub(r"\s+", " ", spoken.read_text(encoding="utf-8")).strip()
    tagged_text = tagged.read_text(encoding="utf-8")
    directed = re.sub(r"\s+", " ", re.sub(r"\[[^\[\]\n]+\]", " ", tagged_text)).strip()
    if directed != clean:
        audit.error("Google Vids tagged script changes the clean spoken narration")
    scene_dir = audit.episode / "script/voiceover-google-vids-scenes"
    scenes = sorted(scene_dir.glob("scene-*.txt")) if scene_dir.is_dir() else []
    if len(tagged_text) > 2500 and not scenes:
        audit.error("Google Vids tagged script exceeds 2,500 characters without paste-ready scene files")
    if scenes:
        expected = [f"scene-{number:02d}.txt" for number in range(1, len(scenes) + 1)]
        if [path.name for path in scenes] != expected:
            audit.error("Google Vids scene files must be consecutively numbered from scene-01.txt")
        pieces: list[str] = []
        for scene in scenes:
            body = scene.read_text(encoding="utf-8")
            if not body.strip() or len(body) > 2500:
                audit.error(f"Google Vids scene is empty or exceeds 2,500 characters: {scene.name}")
            pieces.append(body.strip())
        if "\n\n".join(pieces) != tagged_text.strip():
            audit.error("Google Vids scene files do not reconstruct the tagged master")


def check_timing(audit: Audit) -> int | None:
    path = audit.episode / "timestamps/timing-map.json"
    if not path.exists():
        return None
    data = audit.json(path)
    if not isinstance(data, dict):
        return None
    try:
        end = float(data["narration_end"])
        seconds = float(data["clip_seconds"])
        count = int(data["slot_count"])
        slots = data["slots"]
    except (KeyError, TypeError, ValueError) as exc:
        audit.error(f"timing map needs narration_end, clip_seconds, slot_count, slots: {exc}")
        return None
    if not 600 <= end <= 900:
        audit.error(f"accepted long-form narration must be 600–900 seconds: {end}")
    if seconds != 5 or count != math.ceil(end / 5):
        audit.error("timing map must cover accepted narration in exact five-second slots")
    if not isinstance(slots, list) or len(slots) != count:
        audit.error("timing map slot list does not match slot_count")
        return None
    for index, slot in enumerate(slots, 1):
        if not isinstance(slot, dict) or slot.get("number") != index or slot.get("start") != (index - 1) * 5 or slot.get("end") != index * 5:
            audit.error(f"non-contiguous or malformed timing slot {index}")
    return count


def check_words(audit: Audit) -> None:
    path = audit.episode / "timestamps/word-timestamps-source.csv"
    if not path.exists():
        return
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            rows = csv.DictReader(handle)
            if not {"word", "start", "end"}.issubset(rows.fieldnames or []):
                audit.error("word timestamps need word,start,end columns")
                return
            last_start = -1.0
            seen = 0
            for seen, row in enumerate(rows, 1):
                try:
                    start, end = float(row["start"]), float(row["end"])
                except (TypeError, ValueError):
                    audit.error(f"word timestamp row {seen} has invalid time")
                    continue
                if not row["word"].strip() or start < 0 or end <= start or start < last_start:
                    audit.error(f"word timestamp row {seen} has empty word or invalid ordering")
                last_start = start
            if seen == 0:
                audit.error("word timestamp file is empty")
    except (OSError, UnicodeError) as exc:
        audit.error(f"cannot read word timestamps: {exc}")


def check_claims_and_fidelity(audit: Audit, research_approved: bool, script_approved: bool) -> None:
    claim_path = audit.episode / "source/claims.json"
    if not claim_path.exists():
        return
    claims_data = audit.json(claim_path)
    claims = claims_data.get("claims") if isinstance(claims_data, dict) else None
    if not isinstance(claims, list) or (research_approved and not claims):
        audit.error("claims ledger needs a nonempty claims array")
        return
    ids: set[str] = set()
    for index, claim in enumerate(claims, 1):
        if not isinstance(claim, dict) or not isinstance(claim.get("id"), str) or not claim["id"] or claim["id"] in ids:
            audit.error(f"claim {index} lacks a unique ID")
            continue
        ids.add(claim["id"])
        status = claim.get("status")
        if not claim.get("source_span") or not claim.get("claim") or not isinstance(status, str) or status not in {"supported", "qualified", "contested", "unverified"}:
            audit.error(f"claim {claim['id']} lacks source span, content or valid status")
        if isinstance(status, str) and status in {"supported", "qualified", "contested"} and not claim.get("citations"):
            audit.error(f"claim {claim['id']} needs supporting source citations")
    fidelity_path = audit.episode / "script/fidelity-ledger.json"
    if not fidelity_path.exists():
        return
    fidelity_data = audit.json(fidelity_path)
    mappings = fidelity_data.get("mappings") if isinstance(fidelity_data, dict) else None
    if not isinstance(mappings, list):
        audit.error("fidelity ledger needs mappings array")
        return
    covered: set[str] = set()
    for index, mapping in enumerate(mappings, 1):
        if not isinstance(mapping, dict) or not isinstance(mapping.get("claim_id"), str):
            audit.error(f"fidelity mapping {index} lacks claim ID")
            continue
        claim_id = mapping["claim_id"]
        if claim_id not in ids and mapping.get("treatment") != "sourced_addition":
            audit.error(f"fidelity mapping {index} names unknown source claim {claim_id}")
        treatment = mapping.get("treatment")
        if not isinstance(treatment, str) or treatment not in {"retained", "qualified", "omitted", "sourced_addition"}:
            audit.error(f"fidelity mapping {index} has invalid treatment")
        if treatment == "omitted" and not mapping.get("reason"):
            audit.error(f"fidelity mapping {index} needs an omission reason")
        if claim_id in ids:
            covered.add(claim_id)
    if script_approved and ids != covered:
        audit.error(f"approved script has {len(ids - covered)} unmapped source claims")


def check_text_events(audit: Audit, slot_count: int | None) -> None:
    path = audit.episode / "plan/text-events.json"
    if not path.exists():
        return
    data = audit.json(path)
    events = data.get("events") if isinstance(data, dict) else None
    if not isinstance(events, list):
        audit.error("text-events.json needs an events array")
        return
    for index, event in enumerate(events, 1):
        if not isinstance(event, dict):
            audit.error(f"text event {index} is not an object")
            continue
        clip, exact = event.get("clip"), event.get("exact_text")
        if not isinstance(clip, int) or clip < 1 or (slot_count and clip > slot_count):
            audit.error(f"text event {index} has invalid clip")
        if not isinstance(exact, str) or not exact.strip():
            audit.error(f"text event {index} lacks exact_text")
        if not event.get("claim_id") or not event.get("source"):
            audit.error(f"text event {index} lacks claim/source")
        try:
            onset = float(event["onset_seconds"])
            hold = float(event["hold_until_seconds"])
            exit_time = float(event["exit_seconds"])
            if not 0 <= onset < hold <= exit_time <= 5:
                audit.error(f"text event {index} has invalid five-second timing")
        except (KeyError, TypeError, ValueError):
            audit.error(f"text event {index} needs numeric onset/hold/exit times")
        if not event.get("placement") or not event.get("reference_asset"):
            audit.error(f"text event {index} lacks placement/reference anchor")
        if event.get("status") == "approved" and not event.get("approved_by"):
            audit.error(f"text event {index} claims approval without reviewer")


def check_references(audit: Audit, required: bool) -> None:
    path = audit.episode / "plan/reference-manifest.json"
    if not path.exists():
        return
    data = audit.json(path)
    if not isinstance(data, dict) or not isinstance(data.get("assets"), list) or not isinstance(data.get("coverage"), list):
        audit.error("reference manifest needs assets and coverage arrays")
        return
    assets: dict[str, dict] = {}
    for item in data["assets"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or item["id"] in assets:
            audit.error("reference asset has missing or repeated ID")
            continue
        assets[item["id"]] = item
        value = item.get("path")
        image = audit.within_repo(value, f"reference {item['id']}") if isinstance(value, str) else None
        if required:
            if not image or not image.is_file() or not image.stat().st_size:
                audit.error(f"reference {item['id']} is absent")
            elif hashlib.sha256(image.read_bytes()).hexdigest() != item.get("sha256"):
                audit.error(f"reference {item['id']} hash mismatch")
            if item.get("status") != "approved" or not item.get("approved_by"):
                audit.error(f"reference {item['id']} lacks review approval")
    if required and not data["coverage"]:
        audit.error("approved references need shot coverage entries")
    for item in data["coverage"]:
        if not isinstance(item, dict) or not item.get("shot_id"):
            audit.error("reference coverage entry lacks shot_id")
            continue
        ids = item.get("asset_ids")
        if not isinstance(ids, list) or not ids or any(not isinstance(value, str) or value not in assets for value in ids):
            audit.error(f"shot {item['shot_id']} has missing reference asset IDs")
        if required and item.get("unsupported_elements"):
            audit.error(f"shot {item['shot_id']} still has unsupported visual elements")


def check_job_plan(audit: Audit, slot_count: int | None, required: bool) -> None:
    path = audit.episode / "automation/job-plan.json"
    if not path.exists():
        return
    data = audit.json(path)
    if not isinstance(data, dict) or data.get("schema_version") != "1.0":
        audit.error("job plan needs schema_version 1.0")
        return
    if not isinstance(data.get("project_seed"), int) or not 0 <= data["project_seed"] <= 2**64 - 1:
        audit.error("job plan needs a nonnegative 64-bit project seed")
    slots = data.get("slots")
    if not isinstance(slots, list) or (required and (slot_count is None or len(slots) != slot_count)):
        audit.error("job plan must cover every timing slot")
        return
    for number, item in enumerate(slots, 1):
        if not isinstance(item, dict) or item.get("number") != number or not isinstance(item.get("references"), list) or not 1 <= len(item["references"]) <= 2:
            audit.error(f"job-plan slot {number:03d} has invalid number/references")
            continue
        if not isinstance(item.get("revision"), int) or not 1 <= item["revision"] <= 999:
            audit.error(f"job-plan slot {number:03d} has invalid revision")
        for value in item["references"]:
            image = audit.within_repo(value, f"job-plan slot {number:03d} reference") if isinstance(value, str) else None
            if not image or not image.is_file():
                audit.error(f"job-plan slot {number:03d} has a missing reference")


def expected_h3_slots(audit: Audit, slot_count: int | None) -> set[int]:
    episode = audit.json(audit.episode / "episode.json")
    exceptions = episode.get("picture_method_exceptions", []) if isinstance(episode, dict) else []
    controlled = {item.get("number") for item in exceptions if isinstance(item, dict)}
    if exceptions:
        if episode.get("id") != "006-shortest-war-ever" or controlled != {14, 118} or len(exceptions) != 2:
            audit.error("controlled geography exception must be exactly Episode006 slots014/118")
        for item in exceptions:
            if not isinstance(item, dict) or item.get("method") != "controlled_geography" or not item.get("authority"):
                audit.error("controlled geography needs an explicit method and recorded user authority")
                continue
            for field in ("decision_record", "source_reference", "artifact"):
                value = item.get(field)
                path = audit.within_repo(value, f"controlled geography {field}") if isinstance(value, str) else None
                if not path or not path.is_file():
                    audit.error(f"controlled geography {field} is missing")
                elif field in {"source_reference", "artifact"} and hashlib.sha256(path.read_bytes()).hexdigest() != item.get(field + "_sha256"):
                    audit.error(f"controlled geography {field} hash mismatch")
            if item.get("people") != 0 or item.get("review_status") != "approved" or not item.get("approved_by"):
                audit.error("controlled geography needs reviewed zero-person inputs and actual output review")
    return set(range(1, (slot_count or 0) + 1)) - controlled


def check_prompts(audit: Audit, slot_count: int | None, required: bool) -> dict[int, Path]:
    prompts = numbered_files(audit, audit.episode / "prompts", PROMPT_RE)
    expected = expected_h3_slots(audit, slot_count)
    if set(prompts) - expected:
        audit.error("active H3 prompt exists for a controlled/non-H3 slot")
    if required and (slot_count is None or set(prompts) != expected):
        audit.error("approved prompt set must cover every numbered timing slot")
    for number, path in prompts.items():
        text = path.read_text(encoding="utf-8")
        if not text.strip() or text.startswith("---") or re.search(r"(?m)^status:|^# (?:Approval|Review)", text):
            audit.error(f"clip {number:03d} is empty or contains internal metadata")
        if text.count(POLICY) != 1:
            audit.error(f"clip {number:03d} needs exact audio sentence once")
        if "16:9" not in text or not re.search(r"5\.0+", text):
            audit.error(f"clip {number:03d} lacks landscape/five-second declaration")
    return prompts


def check_jobs(audit: Audit, prompts: dict[int, Path], slot_count: int | None, required: bool, steps: int = 14) -> None:
    jobs = numbered_files(audit, audit.episode / "automation/jobs", JOB_RE)
    expected_slots = expected_h3_slots(audit, slot_count)
    if set(jobs) - expected_slots:
        audit.error("active H3 job exists for a controlled/non-H3 slot")
    if required and (slot_count is None or set(jobs) != expected_slots):
        audit.error("approved job set must cover every numbered timing slot")
    seeds: set[int] = set()
    outputs: set[str] = set()
    for number, path in jobs.items():
        data = audit.json(path)
        if not isinstance(data, dict):
            continue
        if data.get("schema_version") != "1.0" or data.get("template") != "h3_ref2va" or data.get("profile") != "youtube_shorts_hq":
            audit.error(f"job {number:03d} has unsupported service schema/template/profile")
        prompt_data = data.get("prompt")
        prompt_value = prompt_data.get("file") if isinstance(prompt_data, dict) else None
        prompt_path = audit.within_repo(prompt_value, f"job {number:03d} prompt") if isinstance(prompt_value, str) else None
        if prompt_path != prompts.get(number, Path("/missing")):
            audit.error(f"job {number:03d} prompt path does not match its slot")
        refs = data.get("references")
        if not isinstance(refs, list) or not 1 <= len(refs) <= 2:
            audit.error(f"job {number:03d} needs one or two ordered references")
            continue
        prompt_text = prompts[number].read_text(encoding="utf-8") if number in prompts else ""
        tags = {int(n) for n in re.findall(r"<Picture\s+(\d+)>", prompt_text, flags=re.I)}
        if tags != set(range(1, len(refs) + 1)):
            audit.error(f"job {number:03d} Picture tags do not map exactly to references")
        for position, ref in enumerate(refs, 1):
            value = ref.get("path") if isinstance(ref, dict) else ref
            image = audit.within_repo(value, f"job {number:03d} Picture {position}") if isinstance(value, str) else None
            if not image or not image.is_file():
                audit.error(f"job {number:03d} Picture {position} asset is missing")
        generation = data.get("generation")
        generation = generation if isinstance(generation, dict) else {}
        expected = {"aspect_ratio": "16:9", "megapixel": 0.6, "width": 1024, "height": 576,
                    "duration_seconds": 5, "fps": 24, "steps": steps, "sampler": "res_multistep",
                    "scheduler": "beta", "lightning": False, "ref_image_size": "match", "seed_mode": "fixed"}
        for key, value in expected.items():
            if generation.get(key) != value:
                audit.error(f"job {number:03d} generation.{key} must be {value!r}")
        seed = generation.get("seed")
        if not isinstance(seed, int) or not 0 <= seed <= 2**63 - 1 or seed in seeds:
            audit.error(f"job {number:03d} needs a unique fixed integer seed")
        seeds.add(seed)
        audio = data.get("audio")
        audio = audio if isinstance(audio, dict) else {}
        for key, value in {"enabled": True, "mode": "sfx_only", "dialogue": False,
                           "narration": False, "music": False, "require_audio_stream": True}.items():
            if audio.get(key) != value:
                audit.error(f"job {number:03d} audio.{key} must be {value!r}")
        output = data.get("output")
        output = output if isinstance(output, dict) else {}
        if output.get("overwrite") is not False or output.get("editorial_duration_seconds") != 5:
            audit.error(f"job {number:03d} output must be immutable with five-second normalization")
        prefix = output.get("prefix")
        if not isinstance(prefix, str) or not re.search(r"-r\d{3}$", prefix) or prefix in outputs:
            audit.error(f"job {number:03d} needs a unique revisioned output prefix")
        outputs.add(prefix)
        for key, suffix in (("directory", "renders/raw"), ("editorial_directory", "renders/editorial")):
            value = output.get(key)
            expected_path = str(audit.episode.relative_to(REPO) / suffix) if audit.episode.is_relative_to(REPO) else None
            if expected_path is not None and value != expected_path:
                audit.error(f"job {number:03d} output.{key} must be {expected_path}")
        post = data.get("postprocess")
        post = post if isinstance(post, dict) else {}
        if post.get("concat") is not False or post.get("upscale") is not False:
            audit.error(f"job {number:03d} must not auto-concat or auto-upscale")


def check_selection(audit: Audit, slot_count: int | None) -> None:
    selected = numbered_files(audit, audit.episode / "renders/final-selected", SELECTED_RE)
    if slot_count is None or set(selected) != set(range(1, slot_count + 1)):
        audit.error("approved picture selection must contain one render per slot")
    data = audit.json(audit.episode / "renders/selection-manifest.json")
    records = data.get("selections") if isinstance(data, dict) else None
    if not isinstance(records, list) or slot_count is None or len(records) != slot_count:
        audit.error("selection manifest must name exactly one approved clip per slot")
        return
    for number, record in enumerate(records, 1):
        if not isinstance(record, dict) or record.get("number") != number:
            audit.error(f"selection record {number:03d} is missing or out of order")
            continue
        value = record.get("path")
        file = audit.within_repo(value, f"selection {number:03d}") if isinstance(value, str) else None
        if not file or file != selected.get(number) or not file.is_file():
            audit.error(f"selection {number:03d} file does not match selected directory")
            continue
        if hashlib.sha256(file.read_bytes()).hexdigest() != record.get("sha256"):
            audit.error(f"selection {number:03d} hash mismatch")
        if record.get("decision") != "approved" or not record.get("approved_by"):
            audit.error(f"selection {number:03d} lacks actual approval")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path)
    args = parser.parse_args()
    audit = Audit(args.episode.resolve())
    if not audit.episode.is_dir():
        parser.error(f"episode directory does not exist: {audit.episode}")
    episode = audit.json(audit.episode / "episode.json")
    state = audit.json(audit.episode / "pipeline-state.json")
    if not isinstance(episode, dict) or not isinstance(state, dict):
        return 1
    profile = episode.get("production_profile")
    steps = episode.get("generation_steps", 14)
    if episode.get("id") != audit.episode.name or episode.get("format") != "longform" or profile not in {"h3-long-5s-14step-16x9", "h3-long-5s-12step-16x9"} or steps != (12 if profile == "h3-long-5s-12step-16x9" else 14):
        audit.error("episode identity, format or long-form production profile is invalid")
    if state.get("episode_id") != episode.get("id"):
        audit.error("pipeline state episode_id does not match manifest")
    if episode.get("target_language") != "es" or episode.get("duration_seconds") != {"minimum": 600, "maximum": 900}:
        audit.error("long-form target must be Spanish and 600–900 seconds")
    style = episode.get("style_authority")
    style_path = audit.within_repo(style, "style authority") if isinstance(style, str) else None
    if not style_path or not style_path.is_file():
        audit.error("style authority asset is missing")
    source = episode.get("source")
    source = source if isinstance(source, dict) else {}
    if source.get("status") not in {"missing", "reference_transcript_only"}:
        source_path = audit.episode / str(source.get("path", ""))
        if not source_path.is_file() or not source_path.stat().st_size:
            audit.error("supplied source is missing or empty")
        elif hashlib.sha256(source_path.read_bytes()).hexdigest() != source.get("sha256"):
            audit.error("supplied source hash changed")
    stages = state.get("stages")
    expected_stages = ["00", "01", "02", "02a", *[f"{n:02d}" for n in range(3, 13)]]
    if not isinstance(stages, list) or [item.get("id") for item in stages if isinstance(item, dict)] != expected_stages:
        audit.error("pipeline must have ordered stages 00–02, optional 02a, and 03–12")
        stages = []
    allowed = {"missing", "draft", "needs_review", "validated", "approved", "rejected", "skipped"}
    approved: set[str] = set()
    for stage in stages:
        if not isinstance(stage, dict):
            audit.error("pipeline stage is not an object")
            continue
        identifier, status = stage.get("id"), stage.get("status")
        if status not in allowed:
            audit.error(f"stage {identifier} has invalid status {status!r}")
        if status == "skipped" and identifier not in {"01", "02a"}:
            audit.error(f"only user-waived research or optional stage 02a may be skipped: {identifier}")
        if status == "approved":
            if not stage.get("approved_by") or not stage.get("decision_notes"):
                audit.error(f"stage {identifier} claims approval without reviewer/decision")
            for relative in STAGE_FILES.get(identifier, []):
                audit.required_file(relative)
            approved.add(identifier)
    research_stage = next((stage for stage in stages if isinstance(stage, dict) and stage.get("id") == "01"), {})
    research_waived = research_stage.get("status") == "skipped"
    waiver_path = audit.episode / "source/research-waiver.json"
    if research_waived:
        waiver = audit.json(waiver_path)
        if not isinstance(waiver, dict) or waiver.get("stage") != "01" or waiver.get("authorized_by") != "user" or waiver.get("decision") != "skip_independent_fact_verification" or not isinstance(waiver.get("basis"), list) or not waiver["basis"]:
            audit.error("skipped Stage 01 requires an explicit user-authorized research waiver with source basis")
        else:
            for relative in waiver["basis"]:
                if not isinstance(relative, str) or not relative.startswith("source/") or not (audit.episode / relative).is_file():
                    audit.error(f"research waiver source basis is absent or invalid: {relative}")
    elif waiver_path.exists():
        audit.error("research-waiver.json exists but Stage 01 is not skipped")
    for identifier in approved:
        if identifier == "02a":
            if not {"00", "02"}.issubset(approved) or not ("01" in approved or research_waived):
                audit.error("stage 02a is approved before the reviewed story")
        elif identifier != "00" and not all(f"{number:02d}" in approved or (number == 1 and research_waived) for number in range(int(identifier))):
            audit.error(f"stage {identifier} is approved before an earlier stage")
    voice_direction = next((stage for stage in stages if isinstance(stage, dict) and stage.get("id") == "02a"), {})
    if "03" in approved and voice_direction.get("status") not in {"skipped", "approved"}:
        audit.error("approved voice/timing requires stage 02a to be skipped or approved")
    check_voice_direction(audit)
    if "00" in approved and source.get("status") == "missing":
        audit.error("intake cannot be approved without supplied source")
    intake = audit.json(audit.episode / "source/intake.json")
    if isinstance(intake, dict):
        reference_kinds = check_reference_video(audit, intake, "00" in approved, "04" in approved)
        reference_record = intake.get("reference_video")
        if source.get("status") == "reference_transcript_only" and (
            not isinstance(reference_record, dict)
            or reference_record.get("status") != "supplied"
            or not {"video", "transcript"}.issubset(reference_kinds)
        ):
            audit.error("reference_transcript_only requires a supplied video and transcript in the reference manifest")
    slot_count = check_timing(audit)
    check_words(audit)
    check_claims_and_fidelity(audit, "01" in approved, "02" in approved)
    check_text_events(audit, slot_count)
    check_references(audit, "06" in approved)
    check_job_plan(audit, slot_count, "09" in approved)
    prompts = check_prompts(audit, slot_count, "08" in approved)
    check_jobs(audit, prompts, slot_count, "09" in approved, steps)
    if "03" in approved and (not episode.get("accepted_voice") or not episode.get("accepted_timing_map")):
        audit.error("approved timing needs recorded accepted voice and timing map")
    if "09" in approved:
        preflight = audit.json(audit.episode / "automation/preflight.json")
        if not isinstance(preflight, dict) or preflight.get("passed") is not True or preflight.get("live_dry_run_passed") is not True or preflight.get("job_count") != slot_count or preflight.get("expected_slot_count") != slot_count or preflight.get("output_collision_count") != 0:
            audit.error("approved job stage needs a passing live-service preflight record")
    if "10" in approved:
        check_selection(audit, slot_count)
    if "11" in approved:
        for key in ("picture_master", "distribution_master"):
            value = episode.get(key)
            if not isinstance(value, str) or not (audit.episode / value).is_file():
                audit.error(f"approved finish needs existing {key}")
    for warning in audit.warnings:
        print(f"WARN {warning}")
    for error in audit.errors:
        print(f"FAIL {error}")
    if audit.errors:
        print(f"Long-form validation failed: {len(audit.errors)} error(s)")
        return 1
    print(f"Long-form validation passed: {audit.episode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
