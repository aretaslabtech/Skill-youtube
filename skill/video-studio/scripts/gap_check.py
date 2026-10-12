#!/usr/bin/env python3
"""
gap_check.py — rubric B16, "no dead air".

  python3 gap_check.py <hf-project-dir> [--max 0.7] [--payoff 1.2] [--json]

Measures the real silence between consecutive voice lines in the assembled timeline:

  gap = (next line's start + its first word's start) − (this line's start + its last word's end)

Line starts come from `index.html` (`<audio src="assets/voice/NN.wav" data-start=…>`), and word
timings from `audio_meta.json`. Exits 1 if any gap is over --max (default 0.7 s), except a
single gap up to --payoff (default 1.2 s), the one deliberate beat a video may keep.

Why: padded frames left 2–5 s gaps between sentences, and even 2 s felt about 1 s too long. Run it after `audio.mjs sync-durations`, after any hold padding, and after assembly.
"""
import json
import re
import sys
from pathlib import Path

AUDIO_RE = re.compile(r"<audio\b([^>]*)>", re.S)
ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')


def voice_starts(index_html: str) -> dict[str, float]:
    """assets/voice/NN.wav → its data-start in the assembled timeline."""
    out = {}
    for m in AUDIO_RE.finditer(index_html):
        attrs = dict(ATTR_RE.findall(m.group(1)))
        src = attrs.get("src", "")
        if "/voice/" in src and "data-start" in attrs:
            out[src] = float(attrs["data-start"])
    return out


def gaps(meta: dict, starts: dict[str, float]) -> list[dict]:
    lines = []
    for v in meta.get("voices", []):
        words = v.get("words") or []
        start = starts.get(v.get("path"))
        if start is None or not words:
            continue
        lines.append({"frame": v.get("frame"), "speech_start": start + float(words[0]["start"]),
                      "speech_end": start + float(words[-1]["end"]),
                      "first": words[0]["text"], "last": words[-1]["text"]})
    lines.sort(key=lambda l: l["speech_start"])
    out = []
    for a, b in zip(lines, lines[1:]):
        out.append({"after_frame": a["frame"], "before_frame": b["frame"],
                    "gap": round(b["speech_start"] - a["speech_end"], 2),
                    "between": f"…{a['last']}  ⟶  {b['first']}…"})
    return out


def judge(gs: list[dict], max_gap: float = 0.7, payoff: float = 1.2) -> dict:
    over = [g for g in gs if g["gap"] > max_gap]
    # One deliberate beat (the payoff) may run up to `payoff`; everything else must be ≤ max.
    allowed = [g for g in over if g["gap"] <= payoff][:1]
    bad = [g for g in over if g not in allowed]
    return {"ok": not bad, "violations": bad, "payoff_beat": allowed[0] if allowed else None,
            "longest": max((g["gap"] for g in gs), default=0.0), "count": len(gs)}


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    hf = Path(argv[0])
    max_gap = float(argv[argv.index("--max") + 1]) if "--max" in argv else 0.7
    payoff = float(argv[argv.index("--payoff") + 1]) if "--payoff" in argv else 1.2
    try:
        meta = json.loads((hf / "audio_meta.json").read_text())
        index = (hf / "index.html").read_text()
    except OSError as e:
        print(f"Failed: {e}")
        return 1
    gs = gaps(meta, voice_starts(index))
    r = judge(gs, max_gap, payoff)
    if "--json" in argv:
        print(json.dumps({**r, "gaps": gs}, indent=1, ensure_ascii=False))
    else:
        print(("PASS" if r["ok"] else "FAIL") + f": {r['count']} gaps, longest {r['longest']}s "
              f"(max {max_gap}s, one payoff beat ≤ {payoff}s)")
        for g in r["violations"]:
            print(f"  - {g['gap']}s after frame {g['after_frame']}: {g['between']}")
        if r["payoff_beat"]:
            g = r["payoff_beat"]
            print(f"  · payoff beat {g['gap']}s after frame {g['after_frame']}: {g['between']}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
