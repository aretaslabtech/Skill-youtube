import unittest

from voice_build import WIN, LEAD, TAIL, cut_points, sentences


class SentenceSplit(unittest.TestCase):
    def test_keeps_every_sentence(self):
        self.assertEqual(sentences("Step three. A guard counts. Why?"), ["Step three.", "A guard counts.", "Why?"])

    def test_keeps_a_trailing_fragment(self):
        self.assertEqual(sentences("It works. Visit example.com"), ["It works.", "Visit example.com"])

    def test_does_not_split_decimals_or_domains(self):
        self.assertEqual(sentences("It took 2.5 seconds on example.org today."),
                         ["It took 2.5 seconds on example.org today."])


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
