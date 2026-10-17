"""Tests for packaging.py (A24). Run: python3 -m unittest test_packaging (from scripts/)."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import packaging as pk


def image(path: Path, w: int, h: int) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=navy:s={w}x{h}",
                    "-frames:v", "1", str(path)], check=True)


class Titles(unittest.TestCase):
    def test_short_title_passes(self):
        self.assertEqual(pk.title_errors(["My scraper froze for 4 hours"]), [])

    def test_long_title_fails(self):
        errs = pk.title_errors(["Anthropic Ran an AI Model on 15 Cheap TV Boxes. Here's What It Means for You"])
        self.assertTrue(any("max 55" in e for e in errs))

    def test_alternatives_get_more_room(self):
        self.assertEqual(pk.title_errors(["Short one", "x" * 70]), [])
        self.assertTrue(pk.title_errors(["Short one", "x" * 71]))

    def test_parenthetical_and_explained_fail(self):
        self.assertTrue(pk.title_errors(["R-Zero (and its catches)"]))
        self.assertTrue(pk.title_errors(["Coconut, Explained"]))

    def test_one_colon_ok_two_clauses_fail(self):
        self.assertEqual(pk.title_errors(["Gemini 4: one million tokens"]), [])
        self.assertTrue(pk.title_errors(["Gemini 4: 1M tokens | where it wins"]))


class Thumbs(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        (self.d / "thumbs").mkdir()
        self.addCleanup(shutil.rmtree, self.d)

    def post(self, *specs):
        out = []
        for i, (w, h, text) in enumerate(specs):
            f = self.d / "thumbs" / f"{i}.png"
            image(f, w, h)
            out.append({"file": f"thumbs/{i}.png", "text": text})
        return {"thumbnails": out}

    def test_three_good_landscape_pass(self):
        p = self.post((1280, 720, "FROZE 4 HOURS"), (1280, 720, "NO TIMEOUT"), (1920, 1080, "requests hangs"))
        self.assertEqual(pk.thumb_errors(self.d, p), [])

    def test_missing_block_fails(self):
        self.assertTrue(pk.thumb_errors(self.d, {}))
        p = self.post((1280, 720, "A"), (1280, 720, "B"))
        self.assertTrue(any("needs 3" in e for e in pk.thumb_errors(self.d, p)))

    def test_too_small_too_wordy_and_repeated(self):
        p = self.post((640, 360, "ONE"), (1280, 720, "one"), (1280, 720, "far too many words on this"))
        errs = " ".join(pk.thumb_errors(self.d, p))
        self.assertIn("min 1280x720", errs)
        self.assertIn("repeat", errs)
        self.assertIn("max 4", errs)

    def test_shape_must_match_vertical_render(self):
        image(self.d / "video.mp4", 1080, 1920)
        p = self.post((1280, 720, "A"), (1280, 720, "B"), (1280, 720, "C"))
        p["render"] = "video.mp4"
        self.assertTrue(any("landscape" in e for e in pk.thumb_errors(self.d, p)))


if __name__ == "__main__":
    unittest.main()
