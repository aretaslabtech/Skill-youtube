#!/usr/bin/env python3
"""
script_lint.py — the mechanical half of the script rules (references/craft/script-voice.md).

  python3 script_lint.py <path/to/SCRIPT.md> [--seconds N] [--json]

The viewer is a developer or CS student who already codes. The lint reads the spoken lines of
a SCRIPT.md (the indented blocks the TTS step reads) and fails (exit 1) on any of:
  - a hook (the first spoken sentence) over 14 words, one that opens on a banned opener
    ("have you ever", "imagine", "in this video"…), one that names no concrete subject, or a
    bare "-ing" question ("Copying every order by hand?" instead of "Are you still copying…?");
  - a sentence over 20 words (one TTS breath);
  - fewer than 3 named specifics per 30 s of audio (see SPECIFICS below);
  - a term from references/jargon.txt (terms beyond a final-year CS student) spoken before
    it is defined; the basics every developer knows (function, API, cache, token…) are
    never defined, so they aren't in that file;
  - an idiom or slang phrase.

SPECIFICS (a heuristic count of distinct named real things in the narration): a word with a
digit ("3.13", "MAX_INT", "2038"), a code-shaped word (snake_case, dotted.name, camelCase,
mixed-case like "GitHub"), an all-caps acronym of 2+ letters ("MCP", "UTF"; not generic ones like AI, API, GPU), a
capitalised word that isn't the first word of its sentence ("…in Python…", "…from Redis…")
or is a first word that isn't a common opener ("Python's sort…" yes, "Why…" no),
and any word that appears in `backticks` anywhere in SCRIPT.md (the on-screen code and
labels: put the artifact in backticks there, and saying it counts). Repeats count once.

Audio length: --seconds, else the voices in a sibling audio_meta.json, else words ÷ 2.5.
The lint can't tell whether a script is *useful*; rubric A16 (the new-to-me judge) does that.
But a script that fails it is certainly too vague or too slow to hold a developer.
"""
import json
import math
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
JARGON_FILE = SKILL / "references" / "jargon.txt"

MAX_SENTENCE_WORDS = 20
MAX_HOOK_WORDS = 14
SPECIFICS_PER_30S = 3
WORDS_PER_SECOND = 2.5

# Phrases that define the term in the same breath ("…epoll, which means one thread watches…").
DEFINITION_MARKERS = (
    "which means", "which is", "that means", "meaning", "think of", "is like", "are like",
    "is just", "are just", "that's called", "is called", "are called", "we call", "it's called",
    "has a name", "is a name for", "stands for", "in other words", "a kind of", "a type of",
    "basically", "short for", "aka",
)
# The hook names the thing and a tension; it never warms up, sets a scene or asks a riddle.
BANNED_OPENERS = (
    "have you ever", "imagine", "picture this", "picture a", "hey guys", "hi guys", "hello",
    "in this video", "today we", "today i", "let's talk about", "welcome", "so,", "ever wondered",
)
IDIOMS = (
    "long shot", "long shots", "flatter odds", "at the end of the day",
    "ballpark", "game-changer", "game changer", "no-brainer", "low-hanging fruit",
    "move the needle", "secret sauce", "the gist", "ballpark figure", "silver bullet",
    "bang for the buck", "nuts and bolts", "in a nutshell",
)
# Capitalised words that aren't names, even mid-sentence.
NOT_NAMES = {"i", "i'm", "i've", "i'll", "i'd", "ok", "okay", "a", "the",
             # generic acronyms: categories, not named things ("an AI", "the API")
             "ai", "llm", "llms", "api", "apis", "app", "cpu", "gpu", "ram", "url", "ui", "os",
             "sql", "http", "json", "id", "ids"}
# Common sentence openers: a capitalised first word counts as a name only if it isn't one.
COMMON = set("""
a an the this that these those it its it's there here your you you're we our my i if when
why what how who which where while once then now so but and or because since until after
before every each all most some any no not never don't doesn't didn't can can't could will
won't would should must may might do does did is are was were be been have has had having
stop start try run use make see look watch let let's just only even still also first next
last one two three four five ten nobody everyone someone something nothing everything most
many few more less than turn add change keep put take get give say tell ask send save
ever have wondered hey hi hello welcome today in on at for from with without by of to into
""".split())


def spoken_lines(md: str) -> list[str]:
    """The TTS step reads the indented (4-space) blocks of SCRIPT.md."""
    out = []
    for line in md.splitlines():
        if line.startswith("    ") and line.strip():
            out.append(line.strip())
    return out


def screen_terms(md: str) -> set[str]:
    """Words in `backticks` anywhere in SCRIPT.md: the on-screen artifacts."""
    out = set()
    for chunk in re.findall(r"`([^`\n]+)`", md):
        out.update(w.lower() for w in words(chunk))
    return out


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.?!])\s+|\s+[—–]\s+", text)
    return [p.strip() for p in parts if re.search(r"[A-Za-z0-9]", p)]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_][A-Za-z0-9_'’\-.]*[A-Za-z0-9_]|[A-Za-z0-9_]", text)


def _is_specific(w: str, first: bool, screen: set[str]) -> bool:
    if w.lower() in screen:
        return True
    if w.lower() in NOT_NAMES:
        return False
    if re.search(r"\d", w):
        return True
    if "_" in w or re.search(r"[a-z]\.[a-z]", w, re.I):
        return True
    if re.search(r"[a-z][A-Z]", w):  # camelCase, GitHub, SQLite
        return True
    if len(w) >= 2 and w.isupper() and w.isalpha():
        return True
    if not w[0].isupper() or w.lower() in NOT_NAMES:
        return False
    return not first or re.sub(r"['’]s$", "", w).lower() not in COMMON


def specifics(text: str, screen: set[str] = frozenset()) -> list[str]:
    seen, out = set(), []
    for s in sentences(text):
        for i, w in enumerate(words(s)):
            key = w.lower().strip("'’")
            if key in seen or not _is_specific(w, i == 0, screen):
                continue
            seen.add(key)
            out.append(w)
    return out


def load_jargon() -> list[str]:
    try:
        lines = JARGON_FILE.read_text().splitlines()
    except OSError:
        return []
    return [l.strip().lower() for l in lines if l.strip() and not l.startswith("#")]


def _has_term(sentence: str, term: str) -> bool:
    return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", sentence.lower()) is not None


def undefined_jargon(ss: list[str], jargon: list[str]) -> list[dict]:
    """A term is fine once a sentence containing it (or the sentence just before or after)
    carries a definition marker or a colon/dash gloss. Before that, it's flagged once."""
    defined, flagged = set(), []
    for i, s in enumerate(ss):
        near = " ".join(x.lower() for x in ss[max(0, i - 1):i + 2])
        hits = [t for t in jargon if _has_term(s, t)]
        hits = [t for t in hits if not any(t != o and t in o for o in hits)]
        for term in hits:
            if term in defined:
                continue
            if any(m in near for m in DEFINITION_MARKERS) or re.search(rf"{re.escape(term)}\s*[,:(]", s.lower()):
                defined.add(term)
            else:
                flagged.append({"term": term, "sentence": s})
                defined.add(term)  # report once
    return flagged


def hook_problems(ss: list[str], screen: set[str]) -> list[str]:
    if not ss:
        return ["no hook"]
    hook = ss[0]
    out = []
    n = len(words(hook))
    if n > MAX_HOOK_WORDS:
        out.append(f"hook is {n} words (max {MAX_HOOK_WORDS})")
    low = hook.lower()
    opener = next((b for b in BANNED_OPENERS if low.startswith(b)), None)
    if opener:
        out.append(f"hook opens with {opener!r}")
    first = (words(hook) or [""])[0]
    if hook.rstrip().endswith("?") and first.lower().endswith("ing") and first.lower() not in COMMON:
        out.append(f"hook is a bare {first!r} fragment; ask the viewer a full question "
                   f"(\"Are you still {first.lower()}…?\")")
    if not any(_is_specific(w, i == 0, screen) for i, w in enumerate(words(hook))):
        out.append("hook names no concrete subject (a tool, language, company, number or code)")
    return out


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


def lint(text: str, seconds: float, jargon: list[str], screen: set[str] = frozenset()) -> dict:
    ss = sentences(text)
    long_ones = [{"words": len(words(s)), "sentence": s} for s in ss if len(words(s)) > MAX_SENTENCE_WORDS]
    spec = specifics(text, screen)
    need = max(SPECIFICS_PER_30S, math.ceil(seconds / 30 * SPECIFICS_PER_30S))
    idioms = sorted({i for i in IDIOMS if re.search(rf"(?<![a-z]){re.escape(i)}(?![a-z])", text.lower())})
    jarg = undefined_jargon(ss, jargon)
    hook = hook_problems(ss, screen)
    errors = list(hook)
    if long_ones:
        errors.append(f"{len(long_ones)} sentence(s) over {MAX_SENTENCE_WORDS} words")
    if len(spec) < need:
        errors.append(f"{len(spec)} named specifics in {seconds:.0f}s (need {need}: {SPECIFICS_PER_30S} per 30s)")
    if jarg:
        errors.append(f"{len(jarg)} term(s) used before being defined: " + ", ".join(j["term"] for j in jarg))
    if idioms:
        errors.append("idioms: " + ", ".join(idioms))
    return {
        "ok": not errors, "errors": errors, "hook": ss[0] if ss else "", "sentences": len(ss),
        "words": len(words(text)), "seconds": round(seconds, 1), "specifics": spec,
        "specifics_needed": need, "long_sentences": long_ones, "undefined_terms": jarg,
        "idioms": idioms,
    }


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    path = Path(argv[0])
    md = path.read_text()
    text = " ".join(spoken_lines(md))
    if not text:
        print("Failed: no spoken (4-space indented) lines in " + str(path))
        return 1
    secs = float(argv[argv.index("--seconds") + 1]) if "--seconds" in argv else audio_seconds(path, len(words(text)))
    r = lint(text, secs, load_jargon(), screen_terms(md))
    if "--json" in argv:
        print(json.dumps(r, indent=1, ensure_ascii=False))
    else:
        print(("PASS" if r["ok"] else "FAIL") + f": {r['words']} words, {r['sentences']} sentences, "
              f"{len(r['specifics'])}/{r['specifics_needed']} specifics in {r['seconds']}s")
        print(f"  hook: {r['hook']}")
        print(f"  specifics: {', '.join(r['specifics'])}")
        for e in r["errors"]:
            print("  - " + e)
        for j in r["undefined_terms"]:
            print(f"    · {j['term']!r} in: {j['sentence']}")
        for s in r["long_sentences"]:
            print(f"    · {s['words']} words: {s['sentence']}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
