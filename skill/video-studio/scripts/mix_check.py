#!/usr/bin/env python3
"""
mix_check.py — keep the voice on top: the music bed must sit well under the voice.

  python3 mix_check.py <video-dir>          # report; exit 1 if the bed is too loud
  python3 mix_check.py <video-dir> --fix    # rewrite the bed's data-volume to the loudest that passes

Reads the `<audio>` tags in `hf/index.html` and `hf/compositions/*.html`:
- voice = `assets/voice/*.wav`;
- music = anything under `assets/music/`, or id `bed`/`music`.

Effective loudness = the file's integrated LUFS + 20·log10(data-volume). The mean voice line
must beat the loudest bed by config `mix.voice_over_music_db` (default 20 dB).

Why: a bed's file loudness varies a lot (−14 to −30 LUFS), so a fixed data-volume can't be
right for all of them. The owner heard the voice as low on 16 Oct 2026: a 0.16 bed at −14
LUFS was only 13 dB under the voice. deliver.py runs this check; run --fix before the render.
"""
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import studio_config as sc  # noqa: E402
from voice_build import lufs  # noqa: E402

TAG = re.compile(r"<audio\b[^>]*>", re.I)
ATTR = re.compile(r'([\w-]+)="([^"]*)"')


def tracks(hf: Path) -> list[dict]:
    out = []
    for page in [hf / "index.html", *sorted((hf / "compositions").glob("*.html"))]:
        if not page.is_file():
            continue
        for m in TAG.finditer(page.read_text()):
            a = dict(ATTR.findall(m.group(0)))
            src = a.get("src", "")
            kind = ("voice" if "assets/voice/" in src else
                    "music" if "assets/music/" in src or a.get("id") in ("bed", "music") else None)
            if kind:
                out.append({"page": page, "tag": m.group(0), "src": src, "kind": kind,
                            "vol": float(a.get("data-volume") or 1)})
    return out


def db(vol: float) -> float:
    return 20 * math.log10(vol) if vol > 0 else -120.0


def measure(video: Path) -> tuple[float | None, list[dict], float]:
    hf = video / "hf"
    need = float(sc.load().get("mix", {}).get("voice_over_music_db", 20))
    t = tracks(hf)
    cache: dict[str, float] = {}

    def file_lufs(src: str) -> float:
        if src not in cache:
            p = (hf / src).resolve()
            cache[src] = lufs(p) if p.is_file() else -70.0
        return cache[src]

    voices = [file_lufs(x["src"]) + db(x["vol"]) for x in t if x["kind"] == "voice"]
    voice = sum(voices) / len(voices) if voices else None
    music = [dict(x, eff=file_lufs(x["src"]) + db(x["vol"]), file=file_lufs(x["src"])) for x in t if x["kind"] == "music"]
    return voice, music, need


def check(video: Path) -> list[str]:
    """Problems that must stop delivery; [] means the voice sits on top of the music."""
    voice, music, need = measure(video)
    if voice is None:
        return []
    return [f"mix: music {Path(m['src']).name} at volume {m['vol']:g} is {voice - m['eff']:.1f} dB under the voice; "
            f"needs ≥ {need:g} dB (run scripts/mix_check.py {video} --fix, then render again)"
            for m in music if voice - m["eff"] < need]


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    video = Path(argv[0]).resolve()
    sc.adopt_root_from(video)
    voice, music, need = measure(video)
    if voice is None:
        print("mix: no voice tracks found")
        return 0
    bad = 0
    for m in music:
        gap = voice - m["eff"]
        ok = gap >= need
        line = f"mix: voice {voice:.1f} LUFS, {Path(m['src']).name} {m['eff']:.1f} LUFS at volume {m['vol']:g} → {gap:.1f} dB"
        if not ok and "--fix" in argv:
            vol = round(10 ** ((voice - need - m["file"]) / 20) - 0.0005, 3)
            page = m["page"]
            new = re.sub(r'data-volume="[^"]*"', f'data-volume="{vol:g}"', m["tag"]) if "data-volume" in m["tag"] \
                else m["tag"].replace("<audio", f'<audio data-volume="{vol:g}"', 1)
            page.write_text(page.read_text().replace(m["tag"], new, 1))
            line += f" — fixed: volume {vol:g} ({voice - (m['file'] + db(vol)):.1f} dB)"
            ok = True
        bad += not ok
        print(line + ("" if ok else f" — FAIL, needs ≥ {need:g} dB"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
