"""Tests for gap_check.py. Run: python3 -m unittest test_gap_check (from scripts/)."""
import unittest

import gap_check as gc

INDEX = '''<audio id="a" src="assets/voice/01.wav" data-start="0" data-duration="3"></audio>
<audio id="b" src="assets/voice/02.wav" data-start="3.5" data-duration="3"></audio>
<audio id="c" src="assets/voice/03.wav" data-start="8" data-duration="3"></audio>
<audio id="m" src="assets/bgm/track.mp3" data-start="0"></audio>'''


def meta(*lines):
    return {"voices": [{"frame": i + 1, "path": f"assets/voice/0{i + 1}.wav",
                        "words": [{"text": "a", "start": s, "end": s + 0.2}, {"text": "b.", "start": e - 0.2, "end": e}]}
                       for i, (s, e) in enumerate(lines)]}


class Gap(unittest.TestCase):
    def test_starts_parsed_and_bgm_ignored(self):
        self.assertEqual(gc.voice_starts(INDEX), {"assets/voice/01.wav": 0.0, "assets/voice/02.wav": 3.5,
                                                 "assets/voice/03.wav": 8.0})

    def test_gap_is_speech_end_to_next_speech_start(self):
        gs = gc.gaps(meta((0.3, 2.8), (0.3, 2.8), (0.3, 2.8)), gc.voice_starts(INDEX))
        self.assertEqual([g["gap"] for g in gs], [1.0, 2.0])

    def test_one_payoff_beat_allowed_rest_fail(self):
        r = gc.judge([{"gap": 0.5}, {"gap": 1.1}, {"gap": 0.6}])
        self.assertTrue(r["ok"])
        r = gc.judge([{"gap": 1.1}, {"gap": 1.0}])
        self.assertFalse(r["ok"])
        self.assertFalse(gc.judge([{"gap": 2.0}])["ok"])


if __name__ == "__main__":
    unittest.main()
