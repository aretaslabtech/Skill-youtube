#!/usr/bin/env python3
"""
script_lint.py — the mechanical half of "explain it to a smart 12-year-old".

  python3 script_lint.py <path/to/SCRIPT.md> [--seconds N] [--json]

Reads the spoken lines of a SCRIPT.md (the indented blocks the TTS step reads) and fails
(exit 1) on any of:
  - a sentence over 18 words;
  - an estimated reading grade over 7 (Flesch–Kincaid);
  - more than one spoken number per 10 s of audio;
  - a jargon term (references/jargon.txt) spoken before it is defined;
  - an idiom or slang phrase.

Audio length: --seconds, else the voices in a sibling audio_meta.json, else words ÷ 2.0.
The lint can't tell whether a script is *clear*; rubric A16 (the teach-back review) does
that. But a script that fails it is certainly not clear to a beginner.
See references/craft/script-voice.md.
"""
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
JARGON_FILE = SKILL / "references" / "jargon.txt"

MAX_SENTENCE_WORDS = 18
MAX_GRADE = 7.0
SECONDS_PER_NUMBER = 10.0
WORDS_PER_SECOND = 2.0

# Phrases that define the term in the same breath ("…temperature, which is just a number…").
DEFINITION_MARKERS = (
    "which means", "which is", "that means", "meaning", "think of", "is like", "are like",
    "is just", "are just", "that's called", "is called", "are called", "we call", "it's called",
    "has a name", "is a name for", "stands for", "in other words", "a kind of", "a type of",
    "imagine", "picture", "like a", "basically",
)
IDIOMS = (
    "long shot", "long shots", "flatter odds", "under the hood", "at the end of the day",
    "ballpark", "game-changer", "game changer", "no-brainer", "deep dive", "low-hanging fruit",
    "move the needle", "secret sauce", "boils down to", "the gist", "out of the box",
    "rule of thumb", "ballpark figure", "on the fly", "heavy lifting", "silver bullet",
    "bang for the buck", "nuts and bolts", "in a nutshell", "spin up", "bake in", "baked in",
)
NUMBER_WORDS = {
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
    "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
    "hundred", "thousand", "million", "billion", "half", "percent", "dozen",
}
# Number words that are almost always grammar, not quantities, in narration.
NUMBER_GRAMMAR = {"one"}


def spoken_lines(md: str) -> list[str]:
    """The TTS step reads the indented (4-space) blocks of SCRIPT.md."""
    out = []
    for line in md.splitlines():
        if line.startswith("    ") and line.strip():
            out.append(line.strip())
    return out


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.?!])\s+|\s+[—–]\s+", text)
    return [p.strip() for p in parts if re.search(r"[A-Za-z0-9]", p)]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", text)


def syllables(word: str) -> int:
    w = word.lower().strip("'’")
    if w.isdigit():
        return max(1, len(w))  # digits are read as words; roughly one syllable each
    w = re.sub(r"[^a-z]", "", w)
    if not w:
        return 1
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee", "ye")) and n > 1:
        n -= 1
    return max(1, n)


def grade(text: str) -> float:
    """Flesch–Kincaid grade level of the spoken text."""
    ss = sentences(text)
    ws = words(text)
    if not ss or not ws:
        return 0.0
    syl = sum(syllables(w) for w in ws)
    return 0.39 * (len(ws) / len(ss)) + 11.8 * (syl / len(ws)) - 15.59


def count_numbers(text: str) -> int:
    n = len(re.findall(r"\d+(?:[.,]\d+)?%?", text))
    for w in words(text.lower()):
        if w in NUMBER_WORDS and w not in NUMBER_GRAMMAR:
            n += 1
    return n


def load_jargon() -> list[str]:
    try:
        lines = JARGON_FILE.read_text().splitlines()
    except OSError:
        return []
    return [l.strip().lower() for l in lines if l.strip() and not l.startswith("#")]


def _has_term(sentence: str, term: str) -> bool:
    return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", sentence.lower()) is not None


def undefined_jargon(ss: list[str], jargon: list[str]) -> list[dict]:
    """A term is fine once a sentence containing it (or the sentence just before) carries a
    definition marker. Before that, every use is flagged once."""
    defined, flagged = set(), []
    for i, s in enumerate(ss):
        low = s.lower()
        prev = ss[i - 1].lower() if i else ""
        hits = [t for t in jargon if _has_term(s, t)]
        # "gpt" inside "gpt-2" is one term, not two: keep only the longest overlapping match.
        hits = [t for t in hits if not any(t != o and t in o for o in hits)]
        for term in hits:
            if term in defined:
                continue
            if any(m in low for m in DEFINITION_MARKERS) or any(m in prev for m in DEFINITION_MARKERS):
                defined.add(term)
            else:
                flagged.append({"term": term, "sentence": s})
                defined.add(term)  # report once
    return flagged


def audio_seconds(script_path: Path, n_words: int) -> float:
    meta = script_path.parent / "audio_meta.json"
    try:
        m = json.loads(meta.read_text())
        total = sum(float(v.get("duration") or v.get("duration_s") or 0) for v in m.get("voices", []))
        if total > 0:
            return total
    except (OSError, json.JSONDecodeError, AttributeError, TypeError, ValueError):
        pass
    return n_words / WORDS_PER_SECOND


def lint(text: str, seconds: float, jargon: list[str]) -> dict:
    ss = sentences(text)
    long_ones = [{"words": len(words(s)), "sentence": s} for s in ss if len(words(s)) > MAX_SENTENCE_WORDS]
    g = round(grade(text), 1)
    n_num = count_numbers(text)
    allowed = max(1, int(seconds // SECONDS_PER_NUMBER))
    idioms = sorted({i for i in IDIOMS if re.search(rf"(?<![a-z]){re.escape(i)}(?![a-z])", text.lower())})
    jarg = undefined_jargon(ss, jargon)
    errors = []
    if long_ones:
        errors.append(f"{len(long_ones)} sentence(s) over {MAX_SENTENCE_WORDS} words")
    if g > MAX_GRADE:
        errors.append(f"reading grade {g} > {MAX_GRADE}")
    if n_num > allowed:
        errors.append(f"{n_num} spoken numbers in {seconds:.0f}s (max {allowed}: one per {SECONDS_PER_NUMBER:.0f}s)")
    if jarg:
        errors.append(f"{len(jarg)} term(s) used before being defined: " + ", ".join(j["term"] for j in jarg))
    if idioms:
        errors.append("idioms: " + ", ".join(idioms))
    return {
        "ok": not errors, "errors": errors, "grade": g, "sentences": len(ss),
        "words": len(words(text)), "seconds": round(seconds, 1), "numbers": n_num,
        "long_sentences": long_ones, "undefined_terms": jarg, "idioms": idioms,
    }


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    path = Path(argv[0])
    text = " ".join(spoken_lines(path.read_text()))
    if not text:
        print("Failed: no spoken (4-space indented) lines in " + str(path))
        return 1
    secs = float(argv[argv.index("--seconds") + 1]) if "--seconds" in argv else audio_seconds(path, len(words(text)))
    r = lint(text, secs, load_jargon())
    if "--json" in argv:
        print(json.dumps(r, indent=1, ensure_ascii=False))
    else:
        print(("PASS" if r["ok"] else "FAIL") + f": grade {r['grade']}, {r['words']} words, "
              f"{r['sentences']} sentences, {r['numbers']} numbers in {r['seconds']}s")
        for e in r["errors"]:
            print("  - " + e)
        for j in r["undefined_terms"]:
            print(f"    · {j['term']!r} in: {j['sentence']}")
        for s in r["long_sentences"]:
            print(f"    · {s['words']} words: {s['sentence']}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
