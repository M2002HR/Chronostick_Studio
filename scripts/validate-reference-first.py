#!/usr/bin/env python3
"""Check reference-first Shorts artifacts without inferring creative approval."""

import argparse
import hashlib
import json
import importlib.util
import math
import re
from pathlib import Path
import sys

from jsonschema import Draft202012Validator


REPO = Path(__file__).resolve().parents[1]
STAGES = ("intake", "reference-transcription", "reference-analysis", "scenario-script",
          "storyboard", "references", "voice", "voice-transcription", "timed-direction",
          "prompts", "jobs-preflight", "generation", "review", "finish", "youtube")
REQUIRED = {
    "intake": ["source/intake.json", "source/reference-video/manifest.json", "source/reference-video/probe.json"],
    "reference-analysis": ["source/reference-video/intake-review.md", "plan/reference-video-analysis.md"],
    "scenario-script": ["script/narration-es.md", "plan/scenario.md", "script/script-analysis.json"],
    "storyboard": ["plan/storyboard/shot-list.json", "plan/storyboard/review.md"],
    "references": ["plan/reference-manifest.json"],
    "timed-direction": ["plan/shot-plan.md", "plan/story-state-ledger.json", "timestamps/timing-map.json"],
    "jobs-preflight": ["automation/job-plan.json", "automation/preflight.json"],
    "review": ["renders/selection-manifest.json"],
}


def file_hash(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def duration_override_errors(manifest, root):
    """Keep the default duration strict; allow a hash-bound episode voice choice."""
    target = manifest.get("target_seconds")
    if isinstance(target, bool) or not isinstance(target, (int, float)) or not math.isfinite(target) or target <= 0:
        return ["Target must be a finite positive number"]
    override = manifest.get("duration_override")
    if override is None:
        return [] if 20 <= target <= 30 else ["Target must be 20–30 seconds or have a reviewed episode-only voice override"]
    if not isinstance(override, dict) or override.get("scope") != "episode_only":
        return ["Duration override must be explicitly episode-only"]
    initial, duration = override.get("initial_target_seconds"), override.get("voice_duration_seconds")
    if (isinstance(initial, bool) or not isinstance(initial, (int, float)) or not 20 <= initial <= 30
            or isinstance(duration, bool) or not isinstance(duration, (int, float))
            or not math.isfinite(duration) or duration <= 0):
        return ["Duration override lacks original target and actual accepted voice duration"]
    if not math.isclose(target, math.ceil(duration * 24 - 1e-8) / 24, abs_tol=1e-6):
        return ["Voice-led target must cover complete audio on the next 24-fps frame"]
    voice, decision = override.get("voice_path"), override.get("decision_path")
    if not isinstance(voice, str) or not isinstance(decision, str) or manifest.get("accepted_voice") != voice:
        return ["Duration override must point to the accepted voice and review decision"]
    audio, record = (root / voice).resolve(), (root / decision).resolve()
    if (not audio.is_relative_to(root.resolve()) or not record.is_relative_to(root.resolve())
            or not audio.is_file() or not record.is_file()):
        return ["Duration override audio/decision missing or outside episode"]
    try:
        evidence = json.loads(record.read_text())
    except (OSError, ValueError):
        return ["Duration override decision is unreadable"]
    if (not isinstance(evidence, dict) or not evidence.get("quote")
            or not str(evidence.get("reviewer", "")).startswith("user")
            or "episode-runtime" not in evidence.get("scope", [])):
        return ["Duration override lacks actual user decision evidence"]
    digest = file_hash(audio)
    if override.get("voice_sha256") != digest or not any(
            isinstance(a, dict) and a.get("path") == voice and a.get("sha256") == digest
            for a in evidence.get("artifacts", [])):
        return ["Duration override accepted voice hash changed or unbound"]
    return []


def validate(root):
    root = root.resolve()
    errors = []

    def load(relative):
        try:
            value = json.loads((root / relative).read_text())
            if not isinstance(value, dict):
                raise ValueError("Expected a JSON object")
            return value
        except (OSError, ValueError) as exc:
            errors.append(f"{relative}: {type(exc).__name__}")
            return {}

    def path(relative):
        if not isinstance(relative, str) or not relative:
            errors.append("Missing artifact path")
            return None
        p = (root / relative).resolve()
        if not p.is_relative_to(root):
            errors.append(f"Artifact escapes episode: {relative}")
            return None
        if not p.is_file() or not p.stat().st_size:
            errors.append(f"Artifact absent/empty: {relative}")
            return None
        return p

    manifest = load("episode.json")
    state = load("pipeline-state.json")
    if (manifest.get("id") != root.name or manifest.get("format") != "short"
            or manifest.get("workflow") != "reference-first-v1"
            or manifest.get("production_profile") != "h3-short-dynamic-16step-20-30s"):
        errors.append("Episode identity/format/workflow/profile mismatch")
    errors.extend(duration_override_errors(manifest, root))
    if manifest.get("generation_steps") != 16 or manifest.get("target_language") != "es":
        errors.append("Profile requires 16 steps and Spanish")
    if manifest.get("clip_duration_seconds") != {"minimum": 4, "maximum": 7}:
        errors.append("Dynamic editorial clip range must be 4–7 seconds")
    if state.get("schema_version") != "2.0" or state.get("workflow") != "reference-first-v1" or state.get("episode_id") != root.name:
        errors.append("Wrong pipeline state version/workflow/episode")
    schema = json.loads((REPO / "docs/pipeline/pipeline-state-v2.schema.json").read_text())
    for issue in Draft202012Validator(schema).iter_errors(state):
        errors.append(f"State schema {list(issue.path)}: {issue.message}")
    stages = state.get("stages")
    if not isinstance(stages, list) or [s.get("id") if isinstance(s, dict) else None for s in stages] != list(STAGES):
        errors.append("Missing, duplicated or reordered semantic stages")
        return errors
    if any(not isinstance(s.get("inputs"), list) or not isinstance(s.get("outputs"), list) for s in stages):
        return errors
    if state.get("current_stage") not in STAGES:
        errors.append("Unknown current stage")
    by_id = {s["id"]: s for s in stages}
    present = {"draft", "validated", "needs_review", "approved"}
    complete = {"validated", "needs_review", "approved"}
    for stage in stages:
        status = stage.get("status")
        if status not in {"missing", "draft", "validated", "needs_review", "approved", "rejected", "blocked", "superseded", "skipped"}:
            errors.append(f"Unknown status: {stage['id']}")
        if status == "approved" and not all(stage.get(k) for k in ("approved_by", "approved_at", "decision_notes")):
            errors.append(f"Approval lacks real reviewer/decision: {stage['id']}")
        if status == "validated" and not stage.get("validated_at"):
            errors.append(f"Validation lacks timestamp: {stage['id']}")
        if status in present:
            for artifact in stage.get("outputs", []):
                path(artifact)
        if status in complete:
            if not stage.get("outputs"):
                errors.append(f"Completed stage has no outputs: {stage['id']}")
            for artifact in REQUIRED.get(stage["id"], []):
                path(artifact)
    # Creative reference production is gated by the user's actual storyboard/scenario review.
    if by_id["references"]["status"] in present and any(by_id[k]["status"] != "approved" for k in ("scenario-script", "storyboard")):
        errors.append("Production references precede scenario/storyboard approval")
    if by_id["voice-transcription"]["status"] in complete and by_id["voice"]["status"] != "approved":
        errors.append("Accepted voice timing precedes voice acceptance")
    if by_id["timed-direction"]["status"] in complete and any(by_id[k]["status"] != "approved" for k in ("references", "voice", "voice-transcription")):
        errors.append("Final timed direction lacks accepted voice, timings or references")
    if by_id["timed-direction"]["status"] in complete:
        spec = importlib.util.spec_from_file_location("short_plan_validation", REPO / "scripts/validate-short-plan.py")
        plan_validation = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plan_validation)
        errors.extend(plan_validation.validate(root, REPO))

    for downstream, upstream in (("prompts", "timed-direction"), ("jobs-preflight", "prompts"),
                                 ("generation", "jobs-preflight"), ("finish", "review"), ("youtube", "finish")):
        if by_id[downstream]["status"] in complete and by_id[upstream]["status"] != "approved":
            errors.append(f"{downstream} precedes reviewed {upstream}")

    reference = load("source/reference-video/manifest.json")
    items = reference.get("items", [])
    if not isinstance(items, list) or any(not isinstance(i, dict) for i in items):
        errors.append("Malformed reference manifest items")
        return errors
    videos = [i for i in items if i.get("kind") == "video"]
    if len(videos) != 1:
        errors.append("Reference manifest must identify exactly one original video")
    for item in items:
        p = path(item.get("path"))
        if p and item.get("sha256") != file_hash(p):
            errors.append(f"Reference hash mismatch: {item.get('id')}")

    voice_intake = manifest.get("voice_intake")
    if voice_intake is not None:
        if not isinstance(voice_intake, dict):
            errors.append("Malformed voice_intake record")
        elif path(voice_intake.get("provenance_path")):
            voice_provenance = load(voice_intake["provenance_path"])
            artifacts = voice_provenance.get("artifacts")
            if not isinstance(artifacts, dict) or not artifacts:
                errors.append("Voice intake provenance has no archived artifacts")
            else:
                for role, artifact in artifacts.items():
                    if not isinstance(artifact, dict):
                        errors.append(f"Malformed voice artifact: {role}")
                        continue
                    p = path(artifact.get("path"))
                    if p and file_hash(p) != artifact.get("sha256"):
                        errors.append(f"Voice intake hash mismatch: {role}")

    direction = manifest.get("voice_direction", {})
    if not isinstance(direction, dict):
        errors.append("Malformed voice_direction record")
        direction = {}
    tagged_exists = (root / "script/voiceover-google-vids-es.md").exists()
    if tagged_exists or direction.get("status") in complete:
        if direction.get("provider") != "google_vids" or direction.get("selection") != "used":
            errors.append("Google Vids paste input lacks provider/selection record")
        clean = path("script/narration-es.md")
        tagged = path(direction.get("script_path"))
        path(direction.get("notes_path"))
        report_path = path(direction.get("validation_path"))
        if clean and tagged:
            spec = importlib.util.spec_from_file_location("vids_validation", REPO / "scripts/validate-google-vids-script.py")
            vids = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(vids)
            report = vids.validate(clean.read_text(), tagged.read_text())
            errors.extend(f"Voice direction: {e}" for e in report["errors"])
            for key, expected in (("clean_script_sha256", file_hash(clean)), ("tagged_script_sha256", file_hash(tagged))):
                if direction.get(key) != expected:
                    errors.append(f"Voice direction stale {key}")
            if report_path:
                saved = load(direction["validation_path"])
                if saved.get("status") != "passed" or saved.get("clean_sha256") != report["clean_sha256"] or saved.get("tagged_sha256") != report["tagged_sha256"]:
                    errors.append("Voice direction validation report is stale/failed")
    if manifest.get("voice_provider") == "google_vids" and by_id["voice"]["status"] in complete and direction.get("status") not in complete:
        errors.append("Google Vids voice lacks prepared/validated tagged handoff")

    for name in ("reference-transcription", "voice-transcription"):
        if by_id[name]["status"] not in complete:
            continue
        provenance_path = by_id[name].get("provenance")
        if not path(provenance_path):
            continue
        provenance = load(provenance_path)
        directory = (root / provenance_path).parent
        for key, hash_key in (("audio_path", "audio_sha256"), ("raw_response_path", "raw_response_sha256")):
            value = provenance.get(key)
            if not isinstance(value, str):
                errors.append(f"Missing {key}: {name}")
                continue
            p = path(str(directory.relative_to(root) / value))
            if p and file_hash(p) != provenance.get(hash_key):
                errors.append(f"Transcription provenance hash mismatch: {name}/{key}")
        input_path = provenance.get("input_path")
        if not isinstance(input_path, str) or not Path(input_path).resolve().is_relative_to(root) or not Path(input_path).is_file() or file_hash(Path(input_path)) != provenance.get("input_sha256"):
            errors.append(f"Original transcription input missing/changed: {name}")
        if provenance.get("status") != "needs_review":
            errors.append(f"Completed transcription points to failed extraction: {name}")

    if by_id["storyboard"]["status"] in complete:
        shots = load("plan/storyboard/shot-list.json").get("shots", [])
        if not isinstance(shots, list) or any(not isinstance(s, dict) for s in shots):
            errors.append("Malformed storyboard shots")
            return errors
        if not shots or len({s.get("id") for s in shots}) != len(shots):
            errors.append("Storyboard requires nonempty unique shot IDs")
        for shot in shots:
            path(shot.get("sketch_path"))
            if not shot.get("scenario_beat") or not shot.get("action"):
                errors.append(f"Storyboard shot lacks beat/action: {shot.get('id')}")

    # Production art must remain traceable to the actual reviewed storyboard.
    if by_id["references"]["status"] in present:
        references = load("plan/reference-manifest.json")
        entries = references.get("entries")
        panels = load("plan/storyboard/shot-list.json").get("shots", [])
        if not isinstance(panels, list):
            errors.append("Malformed reference storyboard panel list")
            panels = []
        panel_ids = {s["id"] for s in panels if isinstance(s, dict) and isinstance(s.get("id"), str)}
        covered = set()
        if not isinstance(entries, list) or not entries or any(not isinstance(e, dict) for e in entries):
            errors.append("Reference manifest requires nonempty entries")
            entries = []
        entry_ids = [e.get("id") for e in entries]
        if any(not isinstance(i, str) or not i for i in entry_ids):
            errors.append("Production reference IDs must be nonempty strings")
        if len({i for i in entry_ids if isinstance(i, str)}) != len(entries):
            errors.append("Duplicate production reference IDs")
        for entry in entries:
            ids = entry.get("storyboard_panel_ids")
            if not isinstance(ids, list) or not ids or any(not isinstance(i, str) for i in ids):
                errors.append(f"Reference lacks storyboard panel mapping: {entry.get('id')}")
                continue
            unknown = set(ids) - panel_ids
            if unknown:
                errors.append(f"Reference cites unknown storyboard panels: {entry.get('id')}/{sorted(unknown)}")
            if len(ids) != len(set(ids)):
                errors.append(f"Reference repeats storyboard panel IDs: {entry.get('id')}")
            covered.update(set(ids) & panel_ids)
            selected = entry.get("selected_path")
            if selected:
                image = (REPO / selected).resolve() if isinstance(selected, str) else None
                allowed = (REPO / "assets/episodes" / root.name / "references").resolve()
                if not image or not image.is_relative_to(allowed):
                    errors.append(f"Reference image outside episode asset directory: {entry.get('id')}")
                elif not image.is_file() or not image.stat().st_size:
                    errors.append(f"Selected reference image absent/empty: {entry.get('id')}")
                else:
                    if not re.search(r"-r\d{3}\.(?:png|jpe?g|webp)$", image.name, re.I):
                        errors.append(f"Reference image lacks immutable revision: {entry.get('id')}")
                    if entry.get("sha256") != file_hash(image):
                        errors.append(f"Selected reference image hash mismatch: {entry.get('id')}")
            if by_id["references"]["status"] == "approved" and (
                    not selected or entry.get("review_status") != "approved" or not entry.get("review_decision")):
                errors.append(f"Approved references lack selected/reviewed image: {entry.get('id')}")
        omitted = references.get("omitted_panels", [])
        if not isinstance(omitted, list) or any(not isinstance(i, dict) or not i.get("reason")
                                               or not isinstance(i.get("id"), str)
                                               or i.get("id") not in panel_ids for i in omitted):
            errors.append("Omitted storyboard panels require known ID and reason")
            omitted = []
        uncovered = panel_ids - covered - {i["id"] for i in omitted}
        if uncovered:
            errors.append(f"Storyboard panels lack reference coverage or recorded omission: {sorted(uncovered)}")

    approvals = manifest.get("creative_approvals", [])
    if not isinstance(approvals, list):
        errors.append("Creative approvals must be a list")
        approvals = []
    for approval in approvals:
        if not isinstance(approval, dict) or not path(approval.get("path")):
            errors.append("Creative approval lacks a decision record")
            continue
        decisions = load(approval["path"]).get("decisions", [])
        if not isinstance(decisions, list):
            errors.append("Creative decision record must contain a decisions list")
            decisions = []
        decision = next((d for d in decisions if isinstance(d, dict)
                         and d.get("id") == approval.get("decision_id")), None)
        if not decision or not decision.get("quote") or not decision.get("reviewer"):
            errors.append("Creative approval lacks reviewer and actual decision evidence")
            continue
        artifacts = decision.get("artifacts", [])
        if not isinstance(artifacts, list) or not artifacts:
            errors.append("Creative approval lacks reviewed artifact hashes")
            artifacts = []
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                errors.append("Malformed creative approval artifact")
                continue
            p = path(artifact.get("path"))
            if p and file_hash(p) != artifact.get("sha256"):
                errors.append(f"Creative approval artifact changed: {artifact.get('path')}")

    if by_id["prompts"]["status"] in complete:
        timing = load("timestamps/timing-map.json")
        clips = timing.get("clips", [])
        if not clips:
            errors.append("Final prompts require variable-duration clips in timing map")
        for clip in clips:
            if not isinstance(clip, dict):
                errors.append("Malformed timing clip")
                continue
            duration = clip.get("duration_seconds")
            if not isinstance(duration, (int, float)) or isinstance(duration, bool) or not 4 <= duration <= 7:
                errors.append(f"Clip duration outside 4–7 seconds: {clip.get('id')}")
            p = path(clip.get("prompt_path"))
            if p and p.read_text().count("NO BACKGROUND MUSIC. Natural diegetic sound effects only.") != 1:
                errors.append(f"Missing/duplicated exact audio policy: {p.name}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path)
    args = parser.parse_args()
    errors = validate(args.episode)
    for error in errors:
        print("FAIL", error)
    if not errors:
        print(f"Reference-first validation passed: {args.episode}")
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
