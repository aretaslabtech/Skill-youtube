#!/usr/bin/env python3
"""
packaging.py: the packaging gate (rubric A24). It checks the title and thumbnails, the two things
that decide whether anyone clicks.

  python3 packaging.py <video-dir>     # check POST.json; exit 1 on a hard failure

Measured on a 9-day-old channel (17 Oct 2026): 10.1k impressions at a 1.1 % click-through rate.
YouTube was showing the videos; almost nobody clicked. The titles were article headlines that
were cut off on phones ("…Here's What It Means f…"), and the cover was a frame grabbed from the
video, not a designed thumbnail.

Hard failures (`deliver.py` refuses):
  - titles[0] over 55 characters (it gets cut off in the mobile feed), or an alternative over 70;
  - a title with a parenthetical, "explained", or more than one colon/pipe/dash clause;
  - fewer than 3 thumbnails in POST.json "thumbnails" ([{"file", "text"}]) for
    YouTube's Test & Compare;
  - a thumbnail that is missing, not JPG/PNG, over 2 MB, smaller than 1280x720 (16:9) or 1080x1920
    (9:16), or the wrong shape for the render;
  - thumbnail text over 4 words, or two thumbnails with the same text (a test needs real
    variants).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

TITLE_MAX = 55
ALT_MAX = 70
THUMBS_MIN = 3
THUMB_WORDS = 4
THUMB_BYTES = 2_000_000
BANNED = re.compile(r"\(|\)|\bexplained\b", re.I)
CLAUSE = re.compile(r"[:|]|\s[-–—]\s")


def _dims(path: Path) -> tuple[int, int] | None:
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height", "-of", "csv=p=0:s=x", str(path)],
                             capture_output=True, text=True, timeout=60).stdout.strip()
        w, h = out.split("x")[:2]
        return int(w), int(h)
    except (ValueError, OSError, subprocess.SubprocessError):
        return None


def title_errors(titles: list) -> list[str]:
    errs = []
    for i, t in enumerate(titles or []):
        t = str(t).strip()
        cap = TITLE_MAX if i == 0 else ALT_MAX
        which = "title" if i == 0 else f"alternative title {i}"
        if len(t) > cap:
            errs.append(f"{which} is {len(t)} chars (max {cap}): {t!r}")
        if BANNED.search(t):
            errs.append(f"{which} has a parenthetical or 'explained': {t!r}")
        if len(CLAUSE.findall(t)) > 1:
            errs.append(f"{which} chains clauses with colons, pipes or dashes: {t!r}")
    return errs


def thumb_errors(vdir: Path, post: dict) -> list[str]:
    thumbs = post.get("thumbnails")
    if not isinstance(thumbs, list) or len(thumbs) < THUMBS_MIN:
        return [f"POST.json needs {THUMBS_MIN} designed thumbnails in \"thumbnails\" "
                "([{\"file\", \"text\"}]); a frame grab is not a thumbnail (A24)"]
    errs, texts = [], set()
    render = _dims(vdir / post.get("render", "")) if post.get("render") else None
    vertical = bool(render and render[1] > render[0])
    min_w, min_h = (1080, 1920) if vertical else (1280, 720)
    for i, t in enumerate(thumbs, 1):
        f = vdir / str((t or {}).get("file", ""))
        text = str((t or {}).get("text", "")).strip()
        if not f.is_file():
            errs.append(f"thumbnail {i} not found: {f}")
            continue
        if f.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            errs.append(f"thumbnail {i} must be JPG or PNG: {f.name}")
        if f.stat().st_size > THUMB_BYTES:
            errs.append(f"thumbnail {i} is {f.stat().st_size / 1e6:.1f} MB (YouTube max 2 MB)")
        d = _dims(f)
        if not d:
            errs.append(f"thumbnail {i} unreadable: {f.name}")
        else:
            w, h = d
            if w < min_w or h < min_h:
                errs.append(f"thumbnail {i} is {w}x{h} (min {min_w}x{min_h})")
            if (h > w) != vertical:
                errs.append(f"thumbnail {i} is {'vertical' if h > w else 'landscape'} but the video is not")
        words = len(text.split())
        if not text:
            errs.append(f"thumbnail {i} has no \"text\" (the words on it, for the record)")
        elif words > THUMB_WORDS:
            errs.append(f"thumbnail {i} text has {words} words (max {THUMB_WORDS}): {text!r}")
        if text.lower() in texts:
            errs.append(f"thumbnails repeat the text {text!r}; Test & Compare needs real variants")
        texts.add(text.lower())
    return errs


def check_post(vdir: Path, post: dict) -> list[str]:
    return title_errors(post.get("titles", [])) + thumb_errors(vdir, post)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    d = Path(sys.argv[1]).resolve()
    errs = check_post(d, json.loads((d / "POST.json").read_text()))
    print("A24: PASS" if not errs else "A24: FAIL\n- " + "\n- ".join(errs))
    sys.exit(1 if errs else 0)
