import unittest

from fill_check import H, W, frame_stats, judge

GROUND, INK = (20, 24, 40), (240, 240, 230)


def frame(paint):
    """A W×H rgb24 frame on GROUND; `paint` is a list of (y0, y1) ranges in 1920-px units filled with INK."""
    px = bytearray(bytes(GROUND) * (W * H))
    for y0, y1 in paint:
        for y in range(int(y0 / 1920 * H), int(y1 / 1920 * H)):
            px[y * W * 3:(y + 1) * W * 3] = bytes(INK) * W
    return bytes(px)


class FrameFill(unittest.TestCase):
    def test_top_60_percent_layout_is_not_filled(self):
        # the old layout: visual y 440–1100, captions 1150–1200, nothing below
        s = frame_stats(frame([(440, 1000), (1160, 1190)]))
        self.assertFalse(s["filled"])
        self.assertEqual(s["bottom"], 0.0)

    def test_full_frame_layout_is_filled(self):
        s = frame_stats(frame([(440, 1000), (1150, 1300), (1700, 1800)]))
        self.assertTrue(s["filled"])

    def test_judge_needs_three_quarters(self):
        good, bad = {"filled": True}, {"filled": False}
        self.assertTrue(judge([good] * 6 + [bad] * 2)["ok"])
        self.assertFalse(judge([good] * 5 + [bad] * 3)["ok"])


if __name__ == "__main__":
    unittest.main()
