#!/usr/bin/env python3
"""Validate the non-media contract of ChronoStick localization branches."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any


REVISIONED_MEDIA = re.compile(r"-r\d{3}\.(?:wav|flac|m4a|mp3|mp4|mov)$", re.IGNORECASE)
LANGUAGE_TAG = re.compile(r"^[a-z]{2,3}(?:-[a-z0-9]{2,8})*$")
APPROVED_STATUSES = {"needs_review", "approved"}
REQUIRED_ARTIFACTS = (
    "visual_timing_map",
    "segment_plan",
    "raw_timestamps",
    "word_timestamps",
    "timing_map",
    "narration_audio",
    "captions",
    "distribution_master",
)


def error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path}: {message}")


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        error(errors, path, f"invalid JSON: {exc}")
        return None
    if not isinstance(data, dict):
        error(errors, path, "JSON root must be an object")
        return None
    return data


def resolve(root: Path, branch: Path, value: Any) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    # Manifest source paths are repository-relative; branch artifacts are local.
    root_candidate = root / candidate
    return root_candidate if root_candidate.exists() else branch / candidate


def normalize_words(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text).replace("ي", "ی").replace("ك", "ک")
    return re.findall(r"[^\s\W_]+(?:[\u200c][^\s\W_]+)*|\d+(?:[.,٫٬]\d+)*", text, flags=re.UNICODE)


def probe_duration(path: Path) -> float | None:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def validate_branch(root: Path, manifest_path: Path, errors: list[str]) -> None:
    branch = manifest_path.parent
    manifest = load_json(manifest_path, errors)
    if manifest is None:
        return

    if manifest.get("schema_version") != "1.0":
        error(errors, manifest_path, "schema_version must be '1.0'")
    status = manifest.get("status")
    if status not in {"draft", "needs_review", "approved", "rejected", "blocked", "superseded"}:
        error(errors, manifest_path, "status is missing or invalid")
    language = manifest.get("language")
    if not isinstance(language, str) or not LANGUAGE_TAG.fullmatch(language):
        error(errors, manifest_path, "language must be a lowercase BCP-47-style tag")
    elif branch.name != language:
        error(errors, manifest_path, "language must match its localizations/<language> directory")

    picture = manifest.get("source_picture")
    if not isinstance(picture, dict):
        error(errors, manifest_path, "source_picture must be an object")
        return
    picture_path = resolve(root, branch, picture.get("path"))
    if picture_path is None or not picture_path.is_file():
        error(errors, manifest_path, "source_picture.path does not identify an existing master")
        return
    declared_hash = picture.get("sha256")
    if status in APPROVED_STATUSES and not isinstance(declared_hash, str):
        error(errors, manifest_path, "reviewable localization requires source_picture.sha256")
    elif isinstance(declared_hash, str):
        actual_hash = hashlib.sha256(picture_path.read_bytes()).hexdigest()
        if declared_hash != actual_hash:
            error(errors, manifest_path, "source_picture.sha256 does not match the master")
    actual_picture_duration = probe_duration(picture_path)
    declared_picture_duration = picture.get("duration_seconds")
    if status in APPROVED_STATUSES:
        if not isinstance(declared_picture_duration, (int, float)):
            error(errors, manifest_path, "reviewable localization requires source_picture.duration_seconds")
        elif actual_picture_duration is None:
            error(errors, picture_path, "ffprobe could not read source picture duration")
        elif not math.isclose(float(declared_picture_duration), actual_picture_duration, abs_tol=0.12):
            error(errors, manifest_path, "declared source picture duration differs from ffprobe by more than 0.12s")
    if picture.get("audio_contract") not in {"picture_sfx_only", "approved_sfx_stem"}:
        error(errors, manifest_path, "source picture must declare picture_sfx_only or approved_sfx_stem")

    source_timing = manifest.get("source_timing_authority")
    if not isinstance(source_timing, dict):
        error(errors, manifest_path, "source_timing_authority must be an object")
    elif status in APPROVED_STATUSES:
        source_timing_path = resolve(root, branch, source_timing.get("path"))
        if source_timing_path is None or not source_timing_path.is_file():
            error(errors, manifest_path, "reviewable localization requires source_timing_authority.path")
        elif not isinstance(source_timing.get("sha256"), str):
            error(errors, manifest_path, "reviewable localization requires source_timing_authority.sha256")
        elif hashlib.sha256(source_timing_path.read_bytes()).hexdigest() != source_timing["sha256"]:
            error(errors, manifest_path, "source_timing_authority.sha256 does not match")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        error(errors, manifest_path, "artifacts must be an object")
        return
    if status not in APPROVED_STATUSES:
        return
    for key in REQUIRED_ARTIFACTS:
        artifact_path = resolve(root, branch, artifacts.get(key))
        if artifact_path is None or not artifact_path.is_file():
            error(errors, manifest_path, f"reviewable localization requires artifacts.{key}")
    for key in ("narration_audio", "distribution_master"):
        value = artifacts.get(key)
        if isinstance(value, str) and not REVISIONED_MEDIA.search(value):
            error(errors, manifest_path, f"artifacts.{key} must have immutable -rNNN media naming")

    script_path = resolve(root, branch, manifest.get("narration", {}).get("approved_script") if isinstance(manifest.get("narration"), dict) else None)
    if script_path is None or not script_path.is_file() or not script_path.read_text(encoding="utf-8").strip():
        error(errors, manifest_path, "narration.approved_script must be a non-empty canonical script")

    validate_segments(root, branch, artifacts, declared_picture_duration, errors)
    validate_timing(root, branch, artifacts, script_path, declared_picture_duration, errors)
    validate_media_durations(root, branch, artifacts, declared_picture_duration, errors)
    validate_review(manifest_path, manifest, errors)


def validate_segments(root: Path, branch: Path, artifacts: dict[str, Any], picture_duration: Any, errors: list[str]) -> None:
    path = resolve(root, branch, artifacts.get("segment_plan"))
    if path is None or not path.is_file():
        return
    data = load_json(path, errors)
    if data is None:
        return
    segments = data.get("segments")
    if not isinstance(segments, list) or not segments:
        error(errors, path, "segments must be a non-empty array")
        return
    previous_end = -1.0
    for item in segments:
        if not isinstance(item, dict):
            error(errors, path, "each segment must be an object")
            continue
        start, end = item.get("start"), item.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or not end > start:
            error(errors, path, f"segment {item.get('id', '?')} needs numeric start < end")
            continue
        if start < previous_end - 1e-6:
            error(errors, path, f"segment {item.get('id', '?')} overlaps the preceding segment")
        previous_end = float(end)
        if isinstance(picture_duration, (int, float)) and end > float(picture_duration) + 0.12:
            error(errors, path, f"segment {item.get('id', '?')} ends beyond the picture duration")
        if not isinstance(item.get("localized_text"), str) or not item["localized_text"].strip():
            error(errors, path, f"segment {item.get('id', '?')} lacks localized_text")
        tolerance = item.get("anchor_tolerance_seconds")
        if not isinstance(tolerance, (int, float)) or tolerance < 0 or tolerance > 1:
            error(errors, path, f"segment {item.get('id', '?')} has invalid anchor_tolerance_seconds")


def validate_timing(root: Path, branch: Path, artifacts: dict[str, Any], script_path: Path | None, picture_duration: Any, errors: list[str]) -> None:
    raw = resolve(root, branch, artifacts.get("raw_timestamps"))
    csv_path = resolve(root, branch, artifacts.get("word_timestamps"))
    timing_path = resolve(root, branch, artifacts.get("timing_map"))
    for path in (raw, csv_path, timing_path):
        if path is None or not path.is_file():
            return
    try:
        with csv_path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, csv.Error) as exc:
        error(errors, csv_path, f"unreadable timestamp CSV: {exc}")
        return
    if not rows or not {"word", "start", "end"}.issubset(rows[0]):
        error(errors, csv_path, "timestamp CSV must contain word,start,end and at least one row")
        return
    words: list[str] = []
    previous_start = -1.0
    last_end = -1.0
    for row_number, row in enumerate(rows, start=2):
        try:
            start, end = float(row["start"]), float(row["end"])
        except (TypeError, ValueError):
            error(errors, csv_path, f"row {row_number} has non-numeric start/end")
            continue
        if not end >= start >= 0:
            error(errors, csv_path, f"row {row_number} has invalid interval")
        if start < previous_start:
            error(errors, csv_path, f"row {row_number} starts before the preceding word")
        previous_start, last_end = start, max(last_end, end)
        if not row.get("word", "").strip():
            error(errors, csv_path, f"row {row_number} has an empty word")
        words.append(row.get("word", ""))
    if isinstance(picture_duration, (int, float)) and last_end > float(picture_duration) + 0.12:
        error(errors, csv_path, "localized narration extends beyond the picture duration")
    if script_path is not None and script_path.is_file():
        script_words = normalize_words(script_path.read_text(encoding="utf-8"))
        timed_words = normalize_words(" ".join(words))
        if script_words != timed_words:
            error(errors, csv_path, "timed words do not match the canonical localized script")
    timing = load_json(timing_path, errors)
    if timing is None:
        return
    source = timing.get("source")
    if not isinstance(source, dict) or source.get("path") != artifacts.get("raw_timestamps"):
        error(errors, timing_path, "timing map must identify artifacts.raw_timestamps as its source")
    if isinstance(source, dict) and isinstance(source.get("sha256"), str):
        actual_hash = hashlib.sha256(raw.read_bytes()).hexdigest()
        if source["sha256"] != actual_hash:
            error(errors, timing_path, "raw timestamp source hash mismatch")
    else:
        error(errors, timing_path, "timing map requires source.sha256 for the raw timestamp response")
    narration = timing.get("narration")
    if not isinstance(narration, dict) or not isinstance(narration.get("spoken_end"), (int, float)):
        error(errors, timing_path, "timing map requires narration.spoken_end")
    elif not math.isclose(float(narration["spoken_end"]), last_end, abs_tol=0.12):
        error(errors, timing_path, "narration.spoken_end must match the final timed word")


def validate_review(manifest_path: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    review = manifest.get("review")
    if not isinstance(review, dict):
        error(errors, manifest_path, "review must be an object")
        return
    if manifest.get("status") == "approved":
        required = ("audio_status", "timing_status", "caption_status", "mix_status", "distribution_status")
        if any(review.get(key) != "approved" for key in required):
            error(errors, manifest_path, "approved localization requires every review status to be approved")
        if not isinstance(review.get("approved_at"), str) or not isinstance(review.get("approved_by"), str):
            error(errors, manifest_path, "approved localization requires approved_at and approved_by")


def validate_media_durations(root: Path, branch: Path, artifacts: dict[str, Any], picture_duration: Any, errors: list[str]) -> None:
    if not isinstance(picture_duration, (int, float)):
        return
    narration_path = resolve(root, branch, artifacts.get("narration_audio"))
    master_path = resolve(root, branch, artifacts.get("distribution_master"))
    for label, path in (("narration_audio", narration_path), ("distribution_master", master_path)):
        if path is None or not path.is_file():
            continue
        duration = probe_duration(path)
        if duration is None:
            error(errors, path, f"ffprobe could not read artifacts.{label}")
        elif label == "narration_audio" and duration > float(picture_duration) + 0.12:
            error(errors, path, "localized narration audio exceeds the fixed picture duration")
        elif label == "distribution_master" and not math.isclose(duration, float(picture_duration), abs_tol=0.12):
            error(errors, path, "localized distribution master duration differs from source picture by more than 0.12s")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) == 2 else ".").resolve()
    errors: list[str] = []
    for manifest in sorted(root.glob("episodes/*/localizations/*/localization-manifest.json")):
        validate_branch(root, manifest, errors)
    for item in errors:
        print(f"FAIL localization: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
