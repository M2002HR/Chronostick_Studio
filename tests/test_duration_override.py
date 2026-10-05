import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ref_validation", ROOT / "scripts/validate-reference-first.py")
VALIDATE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(VALIDATE)


class DurationOverrideTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.ep = Path(self.temp.name)
        self.voice = self.ep / "voice.wav"
        self.voice.write_bytes(b"immutable fixture voice")
        digest = hashlib.sha256(self.voice.read_bytes()).hexdigest()
        self.record = self.ep / "decision.json"
        self.evidence = {"reviewer": "user (contextual continuation)", "quote": "Continue with care",
                         "scope": ["voice", "episode-runtime"],
                         "artifacts": [{"path": "voice.wav", "sha256": digest}]}
        self.record.write_text(json.dumps(self.evidence))
        self.manifest = {"target_seconds": 33.375, "accepted_voice": "voice.wav",
                         "duration_override": {"scope": "episode_only", "initial_target_seconds": 30,
                                               "voice_duration_seconds": 33.365333, "voice_path": "voice.wav",
                                               "voice_sha256": digest, "decision_path": "decision.json"}}

    def test_default_stays_strict_and_reviewed_override_is_scoped(self):
        self.assertEqual(VALIDATE.duration_override_errors({"target_seconds": 30}, self.ep), [])
        self.assertTrue(VALIDATE.duration_override_errors({"target_seconds": 33.375}, self.ep))
        self.assertEqual(VALIDATE.duration_override_errors(self.manifest, self.ep), [])
        self.manifest["target_seconds"] = 33.25
        self.assertTrue(VALIDATE.duration_override_errors(self.manifest, self.ep))

    def test_absent_decision_or_changed_audio_cannot_authorize_override(self):
        self.evidence["quote"] = ""
        self.record.write_text(json.dumps(self.evidence))
        self.assertTrue(VALIDATE.duration_override_errors(self.manifest, self.ep))
        self.evidence["quote"] = "Continue"
        self.record.write_text(json.dumps(self.evidence))
        self.voice.write_bytes(b"changed voice")
        self.assertTrue(VALIDATE.duration_override_errors(self.manifest, self.ep))


if __name__ == "__main__":
    unittest.main()
