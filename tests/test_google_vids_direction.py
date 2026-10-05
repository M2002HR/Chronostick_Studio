"""Verify that delivery tags cannot silently change spoken narration."""

import importlib.util
from pathlib import Path
import unittest


REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vids", REPO / "scripts/validate-google-vids-script.py")
VIDS = importlib.util.module_from_spec(spec)
spec.loader.exec_module(VIDS)


class VoiceDirectionTests(unittest.TestCase):
    def test_dense_tags_preserve_words_accents_and_punctuation(self):
        report = VIDS.validate("¡Esta máscara sí!", "[rushed pace] [curiosity] ¡Esta [bold] máscara [excited] sí!")
        self.assertEqual(report["status"], "passed")
        self.assertFalse(report["actual_voice_accepted"])

    def test_changed_words_punctuation_or_order_are_rejected(self):
        for tagged in ("[bold] Esta cara.", "[bold] Esta máscara!", "[bold] Máscara esta."):
            with self.subTest(tagged=tagged):
                self.assertEqual(VIDS.validate("Esta máscara.", tagged)["status"], "failed")

    def test_unknown_malformed_and_forbidden_tags_are_rejected(self):
        for tagged in ("[fast] Hola.", "[rushed pace Hola.", "[Excited] Hola.", "[whisper] Hola."):
            with self.subTest(tagged=tagged):
                self.assertEqual(VIDS.validate("Hola.", tagged)["status"], "failed")

    def test_scene_split_must_cover_master_under_limit(self):
        clean = "Hola. " * 430
        tagged = "[rushed pace] " + clean
        self.assertEqual(VIDS.validate(clean, tagged)["status"], "failed")
        scenes = ["[rushed pace] " + "Hola. " * 215, "Hola. " * 215]
        self.assertEqual(VIDS.validate(clean, tagged, scenes)["status"], "passed")
        self.assertEqual(VIDS.validate(clean, tagged, scenes[:-1])["status"], "failed")

    def test_annotations_or_added_speech_are_not_paste_ready(self):
        self.assertEqual(VIDS.validate("Hola.", "# Voice direction\n[bold] Hola.")["status"], "failed")
        self.assertEqual(VIDS.validate("Hola.", "[bold] Hola.\nSay it quickly.")["status"], "failed")


if __name__ == "__main__":
    unittest.main()
