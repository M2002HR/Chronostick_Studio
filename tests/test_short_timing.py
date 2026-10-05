import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("short_timing", ROOT / "scripts/build-short-timing.py")
TIMING = importlib.util.module_from_spec(spec)
spec.loader.exec_module(TIMING)


class ShortTimingTests(unittest.TestCase):
    def test_provider_overlap_stays_traceable_and_each_word_has_one_owner(self):
        words = [{"word": "uno", "start": 0.1, "end": 0.5},
                 {"word": "dos", "start": 0.4, "end": 0.9},
                 {"word": "tres", "start": 4.9, "end": 5.2},
                 {"word": "fin", "start": 9.8, "end": 10.1}]
        original = [w.copy() for w in words]
        result = TIMING.derive(words, [0, 120, 243], 24, 10.12)
        self.assertEqual(words, original)
        self.assertEqual(result["normalized_words"][1]["start"], 0.5)
        self.assertEqual(result["normalized_words"][1]["provider_start"], 0.4)
        owners = [i for clip in result["clips"] for i in clip["owned_word_indexes"]]
        self.assertEqual(owners, [1, 2, 3, 4])
        self.assertIn(3, result["clips"][0]["overlapping_word_indexes"])
        self.assertIn(3, result["clips"][1]["overlapping_word_indexes"])
        self.assertGreaterEqual(result["picture_duration_seconds"], 10.12)
        self.assertLess(result["audio_tail_padding_seconds"], 1 / 24)

    def test_short_slot_requests_supported_raw_duration_without_stretch(self):
        r = TIMING.derive([{"word": "fin", "start": 4, "end": 4.1}], [0, 101], 24, 4.2)
        self.assertEqual(r["clips"][0]["generation_request_seconds"], 5)
        self.assertEqual(r["clips"][0]["expected_raw_frame_count"], 124)
        self.assertEqual(r["clips"][0]["trim_raw_tail_frames"], 23)

    def test_truncation_extra_padding_invalid_slots_and_nested_overlap_fail(self):
        words = [{"word": "fin", "start": 9.9, "end": 10.1}]
        for boundaries in ([0, 120, 240], [0, 120, 264], [0, 72, 243], [0, 120, 120, 243]):
            with self.subTest(boundaries=boundaries), self.assertRaises(ValueError):
                TIMING.derive(words, boundaries, 24, 10.12)
        with self.assertRaises(ValueError):
            TIMING.derive([{"word": "uno", "start": 0.1, "end": 0.9},
                           {"word": "dos", "start": 0.2, "end": 0.5}], [0, 120], 24, 5)


if __name__ == "__main__":
    unittest.main()
