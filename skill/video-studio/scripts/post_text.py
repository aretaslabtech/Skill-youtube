#!/usr/bin/env python3
"""
post_text.py — the text gate (rubric A23): clean and lint the words that get published.

  python3 post_text.py <video-dir>        # check POST.json; exit 1 on a hard failure
  python3 post_text.py --text "…"         # clean and score one text (an X post, say)

The video gets forty gates; the caption under it got none. This uses the vendored caption
linter and humanizer (vendor/igtext, MIT, from Jakeschincariol/instagram-agent-skill).

Fixed in place, because these are machine fingerprints with no legitimate use in a caption:
  - invisible format characters (zero-width spaces, joiners, soft hyphens, BOMs…), except in
    Indic-script text, where ZWJ/ZWNJ shape conjuncts;
  - em dashes (→ comma) and curly quotes (→ straight).
Arrows, en-dash ranges and ellipses are left alone: we use them on purpose.

Hard failures (`deliver.py` refuses):
  - more than 5 hashtags (Instagram's cap since 18 Dec 2025; platform-specs.md §2);
  - a generic tag (#fyp, #viral, #reels…), which describes nothing;
  - a caption that opens on a blank line, a hashtag or a mention;
  - a caption plus tags over 2200 characters.

Advisory only, reported in the kit: the five-check human score (detect.py), stock words
(slop.json) and structural tells. Measured on 12 delivered kits (17 Oct 2026), the score
flagged good, concrete captions because 4–5 sentences are too few to judge rhythm, and the
stock-word list hit "the authors' harness". So they inform the rewrite; they don't block it.
"""
import json
import re
import sys
from pathlib import Path

VENDOR = Path(__file__).resolve().parent.parent / "vendor" / "igtext"
sys.path.insert(0, str(VENDOR))

import caption as ig_caption  # noqa: E402
import detect as ig_detect  # noqa: E402
import humanize as ig_humanize  # noqa: E402

LEX = json.loads((VENDOR / "slop.json").read_text())
FIXED_TYPOGRAPHY = {"EM DASH", "LEFT SINGLE QUOTE", "RIGHT SINGLE QUOTE",
                    "LEFT DOUBLE QUOTE", "RIGHT DOUBLE QUOTE"}
_TYPO_LEX = {"typographic": [e for e in LEX["typographic"] if e["name"] in FIXED_TYPOGRAPHY]}
INDIC = re.compile(r"[ऀ-෿]")
TEXT_FIELDS = ("caption", "youtube_description", "pinned_comment")


def clean(text: str) -> tuple[str, list[str]]:
    """Strip invisible characters and fix em dashes and curly quotes. Returns (text, fixes)."""
    fixes = []
    if not INDIC.search(text):
        text, inv = ig_humanize.pass_invisible(text, LEX)
        fixes += [f"{h['count']}× {h['name']}" for h in inv]
    urls_text, urls = ig_humanize.protect_urls(text)
    urls_text, typo = ig_humanize.pass_typographic(urls_text, _TYPO_LEX)
    fixes += [f"{h['count']}× {h['name']}" for h in typo]
    return ig_humanize.restore_urls(urls_text, urls), fixes


def advice(text: str) -> str:
    """One line: the human score, plus stock words and structural tells worth a rewrite."""
    _, overall, verdict = ig_detect.run(text, LEX)
    _, rep = ig_humanize.humanize(text, LEX)
    bits = [f"{overall:.0f}/100 {verdict}"]
    if rep["lexical"]:
        bits.append("stock words: " + ", ".join(h["find"] for h in rep["lexical"][:4]))
    if rep["structures"]:
        bits.append("tells: " + ", ".join(s["name"].split(" (")[0] for s in rep["structures"][:3]))
    return "; ".join(bits)


def check_post(post: dict) -> tuple[list[str], list[str]]:
    """Clean POST.json's texts in place. Returns (hard errors, advisory notes)."""
    errs, notes = [], []
    for k in TEXT_FIELDS:
        if post.get(k):
            post[k], fixes = clean(post[k])
            if fixes:
                notes.append(f"{k}: fixed {', '.join(fixes)}")
    tags = [f"#{h.lstrip('#')}" for h in post.get("hashtags") or []]
    a = ig_caption.analyse((post.get("caption") or "") + "\n\n" + " ".join(tags))
    if len(tags) > ig_caption.HASHTAG_LIMIT:
        errs.append(f"A23: {len(tags)} hashtags; Instagram counts {ig_caption.HASHTAG_LIMIT} at most")
    filler = [t for t in tags if t.lower() in ig_caption.FILLER_TAGS]
    if filler:
        errs.append(f"A23: generic hashtag(s) {' '.join(filler)}; spend the tags on topics")
    for c in a["checks"]:
        if c["status"] == "FAIL" and c["check"] in ("FIRST LINE", "LENGTH"):
            errs.append(f"A23: caption {c['check'].lower()}: {c['detail']}")
        elif c["status"] == "WARN" and c["check"] in ("FIRST LINE", "ONE ASK"):
            notes.append(f"caption {c['check'].lower()}: {c['detail']}")
    if post.get("caption"):
        notes.append(f"caption reads {advice(post['caption'])}")
    return errs, notes


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[0] == "--text":
        text, fixes = clean(argv[1])
        print(text)
        print(f"fixed: {', '.join(fixes) or 'nothing'} · {advice(text)}", file=sys.stderr)
        return 0
    if len(argv) != 1:
        print(__doc__)
        return 1
    post = json.loads((Path(argv[0]) / "POST.json").read_text())
    errs, notes = check_post(post)
    for line in errs + notes:
        print(("✗ " if line in errs else "· ") + line)
    print(f"A23: {'FAIL' if errs else 'PASS'} errors={len(errs)} notes={len(notes)}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
