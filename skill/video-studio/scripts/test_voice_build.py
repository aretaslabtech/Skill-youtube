import json
import os
import tempfile
import unittest
from pathlib import Path

from voice_build import WIN, LEAD, TAIL, apply_say, cut_points, sentences, stem_for, voice_settings


class SentenceSplit(unittest.TestCase):
    def test_keeps_every_sentence(self):
        self.assertEqual(sentences("Step three. A guard counts. Why?"), ["Step three.", "A guard counts.", "Why?"])

    def test_keeps_a_trailing_fragment(self):
        self.assertEqual(sentences("It works. Visit example.com"), ["It works.", "Visit example.com"])

    def test_does_not_split_decimals_or_domains(self):
        self.assertEqual(sentences("It took 2.5 seconds on example.org today."),
                         ["It took 2.5 seconds on example.org today."])

    def test_splits_hindi_on_the_danda(self):
        self.assertEqual(sentences("वजह बहुत सीधी थी। टाइमआउट लगाइए!"), ["वजह बहुत सीधी थी।", "टाइमआउट लगाइए!"])


class Say(unittest.TestCase):
    def test_longest_spelling_wins(self):
        say = {"timeout=10": "timeout equals ten", "timeout=(3.05, 10)": "timeout equals three point oh five, ten"}
        self.assertEqual(apply_say("Pass timeout=(3.05, 10) now.", say), "Pass timeout equals three point oh five, ten now.")

    def test_take_is_revoiced_only_when_what_shapes_it_changes(self):
        v = {"engine": "pocket", "reference": "/r.wav", "reference_text": "", "language": "english_2026-04"}
        a = stem_for(1, 0, "Hello there.", "Hello there.", v, 0.82)
        self.assertEqual(a, stem_for(1, 0, "Hello there.", "Hello there.", dict(v), 0.82))
        self.assertNotEqual(a, stem_for(1, 0, "Hello there.", "Hello their.", v, 0.82))
        self.assertNotEqual(a, stem_for(1, 0, "Hello there.", "Hello there.", {**v, "reference": "/b.wav"}, 0.82))
        self.assertNotEqual(a, stem_for(1, 0, "Hello there.", "Hello there.", v, 1.0))


class Settings(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "voice").mkdir()
        (root / "voice" / "sample.wav").write_bytes(b"")
        (root / "voice" / "hindi.wav").write_bytes(b"")
        (root / "config.json").write_text(json.dumps({"voice": {"variants": {
            "hi": {"engine": "indicf5", "reference": "voice/hindi.wav", "reference_text": "नमस्ते", "speed": 1.0,
                   "asr_language": "hi"}}}}))
        self.old = os.environ.get("STUDIO_ROOT")
        os.environ["STUDIO_ROOT"] = str(root)

    def tearDown(self):
        if self.old is None:
            os.environ.pop("STUDIO_ROOT", None)
        else:
            os.environ["STUDIO_ROOT"] = self.old
        self.tmp.cleanup()

    def test_default_voice_is_english_pocket_with_an_absolute_reference(self):
        v = voice_settings()
        self.assertEqual((v["engine"], v["speed"]), ("pocket", 0.82))
        self.assertTrue(v["reference"].endswith("voice/sample.wav") and Path(v["reference"]).is_absolute())

    def test_variant_lays_over_the_default(self):
        v = voice_settings("hi")
        self.assertEqual((v["engine"], v["speed"], v["asr_language"], v["gap"]), ("indicf5", 1.0, "hi", 0.35))
        self.assertTrue(v["reference"].endswith("voice/hindi.wav"))

    def test_unknown_variant_fails(self):
        with self.assertRaises(SystemExit):
            voice_settings("ta")


class CutPoints(unittest.TestCase):
    def test_cuts_on_silence_around_the_audible_span(self):
        # 30 windows silent, 50 loud, 20 silent: speech from 0.30 s to 0.80 s
        env = [0] * 30 + [1000] * 50 + [0] * 20
        t0, t1 = cut_points(env, len(env) * WIN)
        self.assertAlmostEqual(t0, 0.30 - LEAD)
        self.assertAlmostEqual(t1, 0.80 + TAIL)

    def test_never_cuts_before_zero_or_past_the_end(self):
        env = [1000] * 10
        self.assertEqual(cut_points(env, 0.1), (0.0, 0.1))


if __name__ == "__main__":
    unittest.main()
