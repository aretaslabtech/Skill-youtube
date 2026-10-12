#!/usr/bin/env python3
"""
fill_check.py — rubric B18, "the Short fills the frame".

  python3 fill_check.py <video.mp4> [--samples 8] [--json]

Why: Shorts built inside YouTube's *ads* safe zone (nothing below y 1248) ended their visual
near y 1130, so the bottom 40% of every frame was empty space, which looks unfinished.

For `--samples` frames (spread over 8–92 % of the runtime) it finds the frame's dominant
ground colour, then measures how much of two bands differs from it:

- **lower visual** y 1150–1440 — the stage must reach down here;
- **bottom** y 1600–1920 — the scene must continue under the captions.

A frame is *filled* when both bands are at least `MIN_INK` non-ground. PASS when ≥ 75 % of the
samples are filled (the end card and one hold may be plain). 9:16 only; a 16:9 video prints
`B18: n/a (not 9:16)` and passes.
"""
import json
import subprocess
import sys
from collections import Counter

W, H = 270, 480            # analysis size (1080×1920 / 4)
SCALE = 1920 / H
BANDS = {"lower_visual": (1150, 1440), "bottom": (1600, 1920)}
MIN_INK = 0.10             # share of a band that must differ from the ground (captions alone ≈ 4–8 %)
DIFF = 24                  # per-channel difference that counts as "not ground"
PASS_SHARE = 0.75


def dominant(px: bytes) -> tuple[int, int, int]:
    c = Counter((px[i] >> 4, px[i + 1] >> 4, px[i + 2] >> 4) for i in range(0, len(px), 3 * 7))
    q = c.most_common(1)[0][0]
    # average the real pixels in that bucket, so a flat ground matches exactly
    tot, n = [0, 0, 0], 0
    for i in range(0, len(px), 3 * 7):
        if (px[i] >> 4, px[i + 1] >> 4, px[i + 2] >> 4) == q:
            tot[0] += px[i]; tot[1] += px[i + 1]; tot[2] += px[i + 2]; n += 1
    return tuple(round(t / n) for t in tot)


def band_ink(px: bytes, ground, y0: int, y1: int, w: int = W, h: int = H) -> float:
    r0, r1 = int(y0 / 1920 * h), min(h, int(y1 / 1920 * h))
    ink = total = 0
    for y in range(r0, r1):
        row = y * w * 3
        for x in range(0, w * 3, 3):
            i = row + x
            total += 1
            if (abs(px[i] - ground[0]) > DIFF or abs(px[i + 1] - ground[1]) > DIFF
                    or abs(px[i + 2] - ground[2]) > DIFF):
                ink += 1
    return ink / total if total else 0.0


def frame_stats(px: bytes, w: int = W, h: int = H) -> dict:
    g = dominant(px)
    out = {k: round(band_ink(px, g, a, b, w, h), 3) for k, (a, b) in BANDS.items()}
    out["filled"] = all(v >= MIN_INK for k, v in out.items())
    return out


def judge(frames: list[dict]) -> dict:
    filled = sum(f["filled"] for f in frames)
    share = filled / len(frames) if frames else 0.0
    return {"ok": share >= PASS_SHARE, "filled": filled, "samples": len(frames), "share": round(share, 2)}


def probe(video: str) -> tuple[float, int, int]:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:format=duration", "-of", "json", video],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    s = j["streams"][0]
    return float(j["format"]["duration"]), int(s["width"]), int(s["height"])


def grab(video: str, t: float) -> bytes:
    return subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                           "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          capture_output=True, check=True).stdout


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    video = argv[0]
    n = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else 8
    dur, w, h = probe(video)
    if h <= w:
        print("B18: n/a (not 9:16)")
        return 0
    ts = [dur * (0.08 + 0.84 * k / max(1, n - 1)) for k in range(n)]
    frames = []
    for t in ts:
        px = grab(video, t)
        if len(px) == W * H * 3:
            frames.append({"t": round(t, 1), **frame_stats(px)})
    r = judge(frames)
    if "--json" in argv:
        print(json.dumps({**r, "frames": frames}, indent=1))
    print(("B18: PASS" if r["ok"] else "B18: FAIL") +
          f" — {r['filled']}/{r['samples']} sampled frames fill the lower visual (y 1150–1440) "
          f"and the bottom (y 1600–1920); need {int(PASS_SHARE * 100)} %")
    for f in frames:
        if not f["filled"]:
            print(f"  - {f['t']}s: lower visual {f['lower_visual']:.0%}, bottom {f['bottom']:.0%} non-ground")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
