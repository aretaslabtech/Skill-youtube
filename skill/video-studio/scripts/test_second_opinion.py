import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import second_opinion as so


def video(d: Path) -> Path:
    (d / "hf").mkdir(parents=True)
    (d / "research").mkdir()
    (d / "hf" / "SCRIPT.md").write_text("1. Your API crashes the moment a row contains a date.\n")
    (d / "research" / "run.txt").write_text("TypeError: Object of type date is not JSON serializable\n")
    (d / "PLAN.md").write_text("---\nslug: x\n---\n")
    return d


class SecondOpinion(unittest.TestCase):
    def test_skips_without_a_model(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": ""}), \
                mock.patch.object(so.sc, "load", return_value={"review": {"second_opinion_model": ""}}):
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(so.main([str(video(Path(t)))]), 0)
            self.assertIn("second-opinion: skipped", buf.getvalue())

    def test_writes_review_rewrite_and_count(self):
        replies = iter([
            (json.dumps({"verdict": "REVISE", "issues": [{"severity": "P1"}, {"severity": "P2"}]}), {}),
            ("1. One.\n   SCREEN: x\n2. Two.\n   SCREEN: y\nLEARNS: z", {}),
        ])
        with tempfile.TemporaryDirectory() as t, mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "k"}), \
                mock.patch.object(so, "ask", side_effect=lambda *a, **k: next(replies)):
            v = video(Path(t))
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(so.main([str(v), "--model", "m/x"]), 0)
            out = v / "research" / "second-opinion"
            self.assertTrue((out / "rewrite.md").is_file())
            self.assertEqual(json.loads((out / "meta.json").read_text())["p1"], 1)
            self.assertIn("issues=2 p1=1 rewrite_sentences=2", buf.getvalue())

    def test_request_names_no_one(self):
        captured = {}

        def fake_urlopen(req, timeout):
            captured.update(dict(req.header_items()))
            raise OSError("stop")
        with mock.patch.object(so.urllib.request, "urlopen", fake_urlopen):
            with self.assertRaises(OSError):
                so.ask("m/x", "k", "s", "u", as_json=False)
        self.assertEqual(sorted(h.lower() for h in captured), ["authorization", "content-type"])


if __name__ == "__main__":
    unittest.main()
