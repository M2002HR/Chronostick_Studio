import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("short_plan", ROOT / "scripts/validate-short-plan.py")
PLAN = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PLAN)


class ShortPlanTests(unittest.TestCase):
    def setUp(self):
        self.timing = {"fps": 24, "word_count": 2, "picture_frame_count": 120,
                       "clips": [{"id": "clip-01", "start_frame": 0, "end_frame": 120,
                                  "duration_seconds": 5, "expected_raw_frame_count": 124,
                                  "owned_word_indexes": [1, 2]}]}
        self.direction = {"clips": [{"id": "clip-01", "reference_ids": ["scene"],
                                    "raw_tail_hold": {"start_frame_local": 120, "end_frame_local": 124},
                                    "shots": [{"id": "a", "start_frame_local": 0, "end_frame_local": 60,
                                               "storyboard_panel_ids": ["S01"], "reference_ids": ["scene"],
                                               "primary_action": "one step", "inventory": "one figure", "resolved_end_state": "planted"},
                                              {"id": "b", "start_frame_local": 60, "end_frame_local": 120,
                                               "storyboard_panel_ids": ["S02"], "reference_ids": ["scene"],
                                               "primary_action": "hold", "inventory": "one figure", "resolved_end_state": "still"}]}]}
        self.refs = {"scene": {"storyboard_panel_ids": ["S01", "S02"]}}

    def errors(self):
        return PLAN.interval_errors(self.timing, self.direction, {"S01", "S02"}, self.refs)

    def test_contiguous_covered_plan_and_bound_raw_tail_pass(self):
        self.assertEqual(self.errors(), [])

    def test_gaps_missing_coverage_and_sfx_boundary_fail(self):
        self.direction["clips"][0]["shots"][1]["start_frame_local"] = 61
        self.assertTrue(any("gap/overlap" in e for e in self.errors()))
        self.direction["clips"][0]["shots"][1]["start_frame_local"] = 60
        self.refs["scene"]["storyboard_panel_ids"] = ["S01"]
        self.assertTrue(any("does not cover" in e for e in self.errors()))
        self.direction["clips"][0]["shots"][0]["sfx"] = {"onset_frame_local": 59, "end_frame_local": 65}
        self.assertTrue(any("SFX crosses" in e for e in self.errors()))

    def test_duplicate_words_and_missing_tail_fail(self):
        self.timing["clips"][0]["owned_word_indexes"] = [1, 1, 2]
        self.direction["clips"][0]["raw_tail_hold"]["end_frame_local"] = 120
        self.assertTrue(any("one clip owner" in e for e in self.errors()))
        self.assertTrue(any("raw-tail hold" in e for e in self.errors()))


if __name__ == "__main__":
    unittest.main()
