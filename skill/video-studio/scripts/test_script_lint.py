"""Tests for script_lint.py. Run: python3 -m unittest test_script_lint (from scripts/)."""
import unittest

import script_lint as sl

JARGON = ["epoll", "kv cache", "kv", "p99"]

GOOD = ("Python's lstrip just ate half your filename. "
        "Run lstrip on report_2024.csv with the prefix 'report_' and you get '2024.csv'. "
        "But try 'rep.csv' and you get '.csv'. "
        "Because lstrip treats its argument as a set of characters, not a prefix. "
        "Since Python 3.9, use removeprefix instead. "
        "Send this to whoever still uses lstrip for this.")


class Lint(unittest.TestCase):
    def test_developer_script_passes(self):
        r = sl.lint(GOOD, 30, JARGON, {"lstrip", "removeprefix"})
        self.assertTrue(r["ok"], r["errors"])
        self.assertIn("removeprefix", [s.lower() for s in r["specifics"]])

    def test_known_terms_need_no_definition(self):
        r = sl.lint("Redis keeps the cache in memory, so the API call skips the database.", 10, JARGON)
        self.assertEqual(r["undefined_terms"], [])

    def test_term_beyond_a_student_needs_a_gloss(self):
        r = sl.lint("Redis uses epoll to stay fast.", 10, JARGON)
        self.assertEqual([j["term"] for j in r["undefined_terms"]], ["epoll"])
        r = sl.lint("Redis uses epoll, one thread watching every socket.", 10, JARGON)
        self.assertEqual(r["undefined_terms"], [])

    def test_overlapping_terms_reported_once(self):
        r = sl.lint("Ollama fills the kv cache first.", 10, JARGON)
        self.assertEqual([j["term"] for j in r["undefined_terms"]], ["kv cache"])

    def test_hook_too_long(self):
        hook = "Python " + " ".join(["word"] * 14) + "."
        r = sl.lint(hook, 10, JARGON)
        self.assertTrue(any("hook is" in e for e in r["errors"]))

    def test_hook_banned_opener_and_no_subject(self):
        r = sl.lint("Have you ever wondered why things break?", 10, JARGON)
        self.assertTrue(any("opens with" in e for e in r["errors"]))
        self.assertTrue(any("no concrete subject" in e for e in r["errors"]))

    def test_vague_script_fails_specifics(self):
        text = ("Postgres has a secret. It makes things faster. It is very clever. "
                "You should use it more often. It helps a lot.")
        r = sl.lint(text, 30, JARGON)
        self.assertTrue(any("specifics" in e for e in r["errors"]), r)

    def test_specifics_heuristic(self):
        got = {s.lower() for s in sl.specifics("Use os.path or getLogger in GitHub CI on 3.13 with max_int.", set())}
        self.assertEqual(got, {"os.path", "getlogger", "github", "ci", "3.13", "max_int"})
        self.assertEqual(sl.specifics("Can an AI call the API?", set()), [])

    def test_idioms_and_long_sentences(self):
        long = "Python " + " ".join(["word"] * 21) + "."
        r = sl.lint("Python 3.13 broke it. " + long + " In a nutshell, ship it.", 30, JARGON)
        self.assertTrue(r["long_sentences"])
        self.assertIn("in a nutshell", r["idioms"])

    def test_spoken_lines_and_screen_terms(self):
        md = "# SCRIPT\n**Screen:** `str.removeprefix()`\n\n## Line 1\n\n    Hello there.\n\n## Line 2\n    Bye.\n"
        self.assertEqual(sl.spoken_lines(md), ["Hello there.", "Bye."])
        self.assertIn("str.removeprefix", sl.screen_terms(md))


if __name__ == "__main__":
    unittest.main()
