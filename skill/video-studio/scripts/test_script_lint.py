"""Tests for script_lint.py. Run: python3 -m unittest test_script_lint (from scripts/)."""
import unittest

import script_lint as sl

JARGON = ["temperature", "token", "gpt-2", "gpt", "divide", "divides"]


class Lint(unittest.TestCase):
    def test_beginner_script_passes(self):
        text = ("When ChatGPT writes, it picks one word at a time. Picture a jar of paper chits. "
                "Tea has the most chits, so tea usually comes out. That knob has a name: temperature. "
                "Turn it down and tea wins almost every time.")
        r = sl.lint(text, 30, JARGON)
        self.assertTrue(r["ok"], r["errors"])

    def test_term_before_definition_fails(self):
        r = sl.lint("It divides every score by the temperature.", 10, JARGON)
        self.assertEqual({j["term"] for j in r["undefined_terms"]}, {"divides", "temperature"})

    def test_definition_in_same_sentence_is_fine(self):
        r = sl.lint("GPT-2, which is an older cousin of ChatGPT, finishes the sentence.", 10, JARGON)
        self.assertEqual(r["undefined_terms"], [])

    def test_overlapping_terms_reported_once(self):
        r = sl.lint("Ask GPT-2 to finish this.", 10, JARGON)
        self.assertEqual([j["term"] for j in r["undefined_terms"]], ["gpt-2"])

    def test_too_many_numbers(self):
        r = sl.lint("Tea: fifty-four percent. Coffee: twenty-two. Milk: 9%. Soup: 3%.", 10, JARGON)
        self.assertFalse(r["ok"])
        self.assertTrue(any("numbers" in e for e in r["errors"]))

    def test_idioms_and_long_sentences(self):
        long = " ".join(["word"] * 20) + "."
        r = sl.lint(long + " The long shots get flatter odds.", 30, JARGON)
        self.assertTrue(r["long_sentences"])
        self.assertIn("long shots", r["idioms"])

    def test_spoken_lines_only_reads_indented_blocks(self):
        md = "# SCRIPT\n**Voice:** x\n\n## Line 1\n\n    Hello there.\n\n## Line 2\n    Bye.\n"
        self.assertEqual(sl.spoken_lines(md), ["Hello there.", "Bye."])


if __name__ == "__main__":
    unittest.main()
