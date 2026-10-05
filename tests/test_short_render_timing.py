import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('render_timing', Path(__file__).parents[1] / 'scripts/audit-short-render-timing.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RenderTimingTests(unittest.TestCase):
    def setUp(self):
        self.stream = {'avg_frame_rate': '24/1', 'time_base': '1/12288', 'duration': '4.208008'}
        self.frames = [{'best_effort_timestamp': i * 512} for i in range(101)]

    def test_mux_endpoint_rounding_does_not_hide_correct_frame_timing(self):
        self.assertEqual(module.presentation_errors(self.stream, self.frames, 101, 24), [])

    def test_missing_frame_fails_despite_nominal_correct_duration(self):
        self.assertTrue(module.presentation_errors(self.stream, self.frames[:-1], 101, 24))

    def test_shifted_or_stretched_pts_fail_despite_correct_count(self):
        self.frames[50]['best_effort_timestamp'] += 512
        self.assertTrue(module.presentation_errors(self.stream, self.frames, 101, 24))

    def test_wrong_endpoint_fails_despite_correct_count(self):
        self.stream['duration'] = '4.25'
        self.assertTrue(module.presentation_errors(self.stream, self.frames, 101, 24))


if __name__ == '__main__':
    unittest.main()
