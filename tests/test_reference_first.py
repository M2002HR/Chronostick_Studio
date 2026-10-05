"""Offline tests of preservation, real timing checks and creative stage gates."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), REPO / "scripts" / f"{name}.py")
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


TRANSCRIBE = module("ajil-transcribe")
VALIDATE = module("validate-reference-first")
REVIEW = module("ajil-review-reference")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReferenceFirstTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.incoming = self.base / "incoming.mp4"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "color=s=64x96:r=12:d=2",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=2", "-shortest",
            "-c:v", "libx264", "-c:a", "aac", str(self.incoming),
        ], check=True)
        self.original_hash = sha(self.incoming)
        self.root = self.base / "episodes" / "999-test-short"

    def cli(self, script, *args):
        return subprocess.run([sys.executable, str(REPO / "scripts" / script), *map(str, args)],
                              capture_output=True, text=True)

    def scaffold(self, *args):
        result = self.cli("new-short-episode.py", "999-test-short", "--title", "Test",
                          "--reference-video", self.incoming, "--reference-url", "https://example.org/video",
                          "--episodes-root", self.base / "episodes", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.root / "source/reference-video/reference-test-short-r001.mp4"

    def test_move_preserves_video_and_records_selected_target(self):
        video = self.scaffold("--move-reference", "--target-seconds", "24")
        self.assertFalse(self.incoming.exists())
        self.assertEqual(sha(video), self.original_hash)
        intake = json.loads((self.root / "source/intake.json").read_text())
        self.assertEqual(intake["target_seconds"], 24)
        self.assertIn("24-second", intake["target_decision"])
        self.assertEqual(VALIDATE.validate(self.root), [])

    def test_existing_episode_cannot_replace_original_or_artifacts(self):
        self.scaffold()
        before = (self.root / "episode.json").read_bytes()
        result = self.cli("new-short-episode.py", "999-test-short", "--title", "Other",
                          "--reference-video", self.incoming, "--reference-url", "https://example.org",
                          "--episodes-root", self.base / "episodes", "--move-reference")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.root / "episode.json").read_bytes(), before)
        self.assertEqual(sha(self.incoming), self.original_hash)

    def test_narration_ingest_preserves_audio_samples_and_refuses_overwrite(self):
        self.scaffold()
        args = ["--input", self.incoming, "--episode", self.root, "--revision", "r001"]
        result = self.cli("ingest-narration.py", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        wav = self.root / "audio/narration-es-r001.wav"
        archived = self.root / "audio/source/voice-export-es-r001.mp4"
        self.assertEqual(sha(archived), self.original_hash)
        self.assertEqual(sha(self.incoming), self.original_hash)
        def pcm(path):
            return subprocess.check_output(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path),
                                            "-map", "0:a:0", "-c:a", "pcm_s24le", "-f", "s24le", "pipe:1"])
        self.assertEqual(pcm(wav), pcm(self.incoming))
        manifest_path = self.root / "episode.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["voice_intake"] = {"provenance_path": "audio/narration-provenance-es-r001.json"}
        manifest_path.write_text(json.dumps(manifest))
        self.assertEqual(VALIDATE.validate(self.root), [])
        before = sha(wav)
        self.assertNotEqual(self.cli("ingest-narration.py", *args).returncode, 0)
        self.assertEqual(sha(wav), before)
        with wav.open("ab") as stream:
            stream.write(b"changed")
        self.assertTrue(any("Voice intake hash mismatch" in e for e in VALIDATE.validate(self.root)))

    def test_validator_rejects_changed_original(self):
        video = self.scaffold()
        with video.open("ab") as stream:
            stream.write(b"changed")
        self.assertTrue(any("hash mismatch" in e for e in VALIDATE.validate(self.root)))

    def test_reference_design_requires_actual_scenario_and_board_approval(self):
        self.scaffold()
        path = self.root / "pipeline-state.json"
        state = json.loads(path.read_text())
        next(s for s in state["stages"] if s["id"] == "references")["status"] = "draft"
        path.write_text(json.dumps(state))
        self.assertTrue(any("scenario/storyboard approval" in e for e in VALIDATE.validate(self.root)))

    def test_validator_rejects_escape_and_malformed_state_without_crashing(self):
        self.scaffold()
        path = self.root / "pipeline-state.json"
        state = json.loads(path.read_text())
        state["stages"][0]["outputs"].append("../../../incoming.mp4")
        path.write_text(json.dumps(state))
        self.assertTrue(any("escapes episode" in e for e in VALIDATE.validate(self.root)))
        state["stages"][1] = "not a stage object"
        path.write_text(json.dumps(state))
        self.assertTrue(VALIDATE.validate(self.root))
        path.write_text("[]")
        self.assertTrue(VALIDATE.validate(self.root))

    def test_declared_approval_requires_reviewer_and_decision(self):
        self.scaffold()
        path = self.root / "pipeline-state.json"
        state = json.loads(path.read_text())
        state["stages"][0]["status"] = "approved"
        path.write_text(json.dumps(state))
        self.assertTrue(any("reviewer/decision" in e for e in VALIDATE.validate(self.root)))

    def test_production_references_must_cover_known_storyboard_panels(self):
        self.scaffold()
        state_path = self.root / "pipeline-state.json"
        state = json.loads(state_path.read_text())
        ref = next(s for s in state["stages"] if s["id"] == "references")
        ref.update(status="draft", outputs=["plan/reference-manifest.json"])
        state_path.write_text(json.dumps(state))
        board = self.root / "plan/storyboard/shot-list.json"
        board.parent.mkdir(parents=True, exist_ok=True)
        board.write_text(json.dumps({"shots": [{"id": "S01"}, {"id": "S02"}]}))
        manifest_path = self.root / "plan/reference-manifest.json"
        manifest = {"entries": [{"id": "mask", "storyboard_panel_ids": ["S01", "S02"]}]}
        manifest_path.write_text(json.dumps(manifest))
        def mapping_errors():
            return [e for e in VALIDATE.validate(self.root) if "panel" in e.lower()]
        self.assertEqual(mapping_errors(), [])
        manifest["entries"][0]["storyboard_panel_ids"] = ["S01", "S99"]
        manifest_path.write_text(json.dumps(manifest))
        issues = mapping_errors()
        self.assertTrue(any("unknown storyboard panels" in e for e in issues))
        self.assertTrue(any("lack reference coverage" in e for e in issues))
        manifest["entries"][0].pop("storyboard_panel_ids")
        manifest_path.write_text(json.dumps(manifest))
        self.assertTrue(any("lacks storyboard panel mapping" in e for e in mapping_errors()))
        manifest["entries"][0]["storyboard_panel_ids"] = ["S01"]
        manifest["omitted_panels"] = [{"id": "S02", "reason": "Redundant insert omitted during timing reconciliation."}]
        manifest_path.write_text(json.dumps(manifest))
        self.assertEqual(mapping_errors(), [])

    def test_creative_acceptance_is_bound_to_reviewed_artifact_bytes(self):
        self.scaffold()
        artifact = self.root / "plan/scenario.md"
        artifact.write_text("Reviewed scenario")
        record = self.root / "plan/review-decisions.json"
        record.write_text(json.dumps({"decisions": [{"id": "decision-1", "reviewer": "test reviewer",
            "quote": "Proceed with this scenario", "artifacts": [{"path": "plan/scenario.md", "sha256": sha(artifact)}]}]}))
        path = self.root / "episode.json"
        manifest = json.loads(path.read_text())
        manifest["creative_approvals"] = [{"decision_id": "decision-1", "path": "plan/review-decisions.json"}]
        path.write_text(json.dumps(manifest))
        self.assertEqual(VALIDATE.validate(self.root), [])
        artifact.write_text("A materially different scenario")
        self.assertTrue(any("Creative approval artifact changed" in e for e in VALIDATE.validate(self.root)))

    def test_word_overlaps_are_reported_without_rewriting(self):
        raw = {"text": "uno dos", "words": [
            {"word": "uno", "start": 0.4, "end": 0.8},
            {"word": "dos", "start": 0.3, "end": 0.9}],
            "segments": [{"text": "uno dos", "start": 0.0, "end": 1.0}]}
        before = json.dumps(raw)
        report = TRANSCRIBE.validate_words(raw, 2, "uno tres")
        self.assertEqual(report["overlapping_word_rows"], [2])
        self.assertEqual(report["nonmonotonic_word_rows"], [2])
        self.assertTrue(report["expected_script_changes"])
        self.assertEqual(json.dumps(raw), before)

    def test_invalid_or_missing_provider_timing_is_not_estimated(self):
        base = {"text": "uno", "words": [{"word": "uno", "start": 0, "end": 1}],
                "segments": [{"text": "uno", "start": 0, "end": 1}]}
        for start, end in ((-1, 1), (1, 0), (float("nan"), 1), (0, 3), (False, 1)):
            raw = {**base, "words": [{"word": "uno", "start": start, "end": end}]}
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                TRANSCRIBE.validate_words(raw, 2)
        with self.assertRaises(ValueError):
            TRANSCRIBE.validate_words({**base, "words": []}, 2)

    def test_offline_derivation_preserves_exact_response_and_refuses_overwrite(self):
        video = self.scaffold()
        prior_dir = self.base / "prior"
        prior_dir.mkdir()
        audio = prior_dir / "audio.wav"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video),
                        "-vn", "-ac", "1", "-ar", "16000", str(audio)], check=True)
        raw = prior_dir / "response.json"
        raw.write_bytes(b'{ "ok": true, "payload": { "raw": {"text":"uno", "language":"es", '
                        b'"words":[{"word":"uno","start":0.1,"end":0.9}], '
                        b'"segments":[{"text":"uno","start":0,"end":1}] } } }\n')
        provenance = prior_dir / "provenance.json"
        provenance.write_text(json.dumps({"input_sha256": sha(video), "audio_sha256": sha(audio),
                                          "raw_response_sha256": sha(raw), "http_status": 200}))
        output = self.root / "source/reference-video/transcription"
        args = ["--input", video, "--output-dir", output, "--purpose", "reference", "--revision", "r001",
                "--from-response", raw, "--audio-derivative", audio, "--source-provenance", provenance,
                "--audio-format", "wav", "--base-url", "http://127.0.0.1:1"]
        result = self.cli("ajil-transcribe.py", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        copied = output / "reference-response-r001.json"
        self.assertEqual(copied.read_bytes(), raw.read_bytes())
        derived = json.loads((output / "reference-provenance-r001.json").read_text())
        self.assertFalse(derived["api_request_made"])
        self.assertNotEqual(self.cli("ajil-transcribe.py", *args).returncode, 0)
        self.assertEqual(copied.read_bytes(), raw.read_bytes())
        raw.write_bytes(raw.read_bytes() + b" ")
        args[args.index("r001")] = "r002"
        self.assertNotEqual(self.cli("ajil-transcribe.py", *args).returncode, 0)
        self.assertFalse((output / "reference-response-r002.json").exists())

    def test_local_fallback_cannot_pass_as_video_review(self):
        fake = {"model": "local/fallback", "choices": [{"message": {"content":
                '{"timecoded_sequences":[{"start":0,"end":1}]}'}}]}
        with self.assertRaises(ValueError):
            REVIEW.genuine_review(fake)


if __name__ == "__main__":
    unittest.main()
