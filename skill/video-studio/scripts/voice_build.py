#!/usr/bin/env python3
"""
voice_build.py — voice a script one sentence at a time, and never cut into a word.

  python3 voice_build.py <video-dir> [--speed 0.75] [--gap 0.35]
  python3 voice_build.py --check <video-dir>     # the delivery gate (deliver.py runs it)

Voices every sentence of `hf/SCRIPT.md` (indented lines) separately with your HeyGen voice
(config.json "voice.voice_id", or HEYGEN_VOICE_ID), trims each take to its **audible** speech, and joins a line's sentences with a `--gap`
breath. Writes `hf/assets/voice/NN.wav` + `NN.words.json`, one per script line (the shape
HyperFrames' `audio.mjs sync-durations` reads). Takes are cached in `research/voice-takes/`, so a rerun costs no TTS.

Why per sentence: a clone voiced a whole line at a time at speed 0.9 measured ~3 words/s;
per sentence at 0.75 with short breaths lands at ≤ 2.2 words/s with gaps ≤ 0.7 s (B16).

Why trim on the audio, not on the word timings: HeyGen's first-word timestamp runs ~0.2 s
late, and viewers reported words being cut off. Trimming
at `first_word.start − 0.08` sliced the start off a third of all sentences ("The" → "e",
"Step" → "tep"). Now each take is cut at its first and last audible 10 ms window, plus
padding, with 8 ms fades. The build fails if any trimmed take starts or ends on speech.

The gate: the build writes `hf/assets/voice/voice_build.json`, a manifest with every line's
sha1. `--check` (and `deliver.py`, for every track: daily, companion, promo, blog) refuses a
video whose voice files weren't made by this script, were changed after it, or start or end
on speech.

Needs HEYGEN_API_KEY in the environment, node on PATH, and the HyperFrames media-use skill
(its heygen-tts.mjs). Override the helper's location with HEYGEN_TTS_SCRIPT.
"""
import argparse
import hashlib
import json
import os
import random
import re
import struct
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import studio_config as sc  # noqa: E402

def tts_script() -> Path:
    """The HyperFrames media-use TTS helper: HEYGEN_TTS_SCRIPT, else wherever the skills are."""
    if os.environ.get("HEYGEN_TTS_SCRIPT"):
        return Path(os.environ["HEYGEN_TTS_SCRIPT"])
    d = sc.media_use_dir()
    if d:
        return d / "audio" / "scripts" / "heygen-tts.mjs"
    raise SystemExit("Failed: heygen-tts.mjs not found — install the HyperFrames skills "
                     "(npx skills add heygen-com/hyperframes) or set HEYGEN_TTS_SCRIPT")


def voice_id() -> str:
    v = sc.load()["voice"]["voice_id"]
    if not v:
        raise SystemExit("Failed: no voice id — set config.json voice.voice_id or HEYGEN_VOICE_ID "
                         "(run /video-studio setup)")
    return v
SR = 44100
LEAD, TAIL = 0.06, 0.12   # silence kept before the first and after the last audible sound
FADE = 0.008
WIN = 0.01                # energy window (s)
THRESH = 0.03             # audible = window peak above 3 % of the take's peak
SENT_RE = re.compile(r"[^.?!]+(?:[.?!]+|$)")


def sentences(line: str) -> list[str]:
    """Split a line into sentences without dropping text: a trailing fragment with no
    punctuation is kept, and a '.' between digits or letters ("2.5", "example.com") doesn't split."""
    guarded = re.sub(r"(?<=\w)\.(?=\w)", "․", line)
    out = [s.strip().replace("․", ".") for s in SENT_RE.findall(guarded)]
    out = [s for s in out if s]
    if re.sub(r"\s", "", "".join(out)) != re.sub(r"\s", "", line):
        raise SystemExit(f"Failed: sentence split lost text in {line!r}")
    return out


def envelope(path: Path, rate: int = 8000) -> list[int]:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(rate),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    s = struct.unpack(f"<{len(raw) // 2}h", raw)
    n = int(rate * WIN)
    return [max((abs(x) for x in s[k:k + n]), default=0) for k in range(0, len(s), n)]


def audible_span(env: list[int]) -> tuple[float, float]:
    """First and last audible moment of a take, in seconds."""
    thr = (max(env) or 1) * THRESH
    loud = [k for k, v in enumerate(env) if v > thr]
    if not loud:
        raise ValueError("silent take")
    return loud[0] * WIN, (loud[-1] + 1) * WIN


def cut_points(env: list[int], length: float) -> tuple[float, float]:
    on, off = audible_span(env)
    return max(0.0, on - LEAD), min(length, off + TAIL)


def edges_quiet(path: Path) -> bool:
    """True if the first and last 20 ms of a trimmed take are below the audible threshold."""
    env = envelope(path)
    thr = (max(env) or 1) * THRESH
    return all(v <= thr for v in env[:2] + env[-2:])


def take(sentence: str, stem: Path, speed: float) -> tuple[Path, list[dict]]:
    wav, wjs = Path(f"{stem}.wav"), Path(f"{stem}.json")
    tries = 0
    while not wjs.exists():   # HeyGen allows 30 calls/min: back off with jitter on a refusal
        r = subprocess.run(["node", str(tts_script()), sentence, "-o", str(wav), "--words", str(wjs),
                            "--voice", voice_id(), "--speed", str(speed)], capture_output=True, text=True)
        if r.returncode:
            tries += 1
            if tries > 6:
                raise SystemExit(f"Failed: TTS {sentence!r}: {r.stderr[-300:]}")
            time.sleep(random.uniform(0, 2 ** tries))
    w = json.loads(wjs.read_text())
    return wav, (w["words"] if isinstance(w, dict) else w)


def build(video: Path, speed: float, gap: float) -> int:
    hf = video / "hf"
    lines = [l[4:].strip() for l in (hf / "SCRIPT.md").read_text().splitlines() if l.startswith("    ")]
    takes = video / "research" / "voice-takes"
    takes.mkdir(parents=True, exist_ok=True)
    out = hf / "assets" / "voice"
    out.mkdir(parents=True, exist_ok=True)
    bad = []
    for i, line in enumerate(lines, 1):
        parts, words, t = [], [], 0.0
        for k, s in enumerate(sentences(line)):
            stem = takes / f"{i:02d}-{k}-{speed}-{re.sub(r'[^a-z]', '', s.lower())[:60]}"
            wav, ws = take(s, stem, speed)
            env = envelope(wav)
            t0, t1 = cut_points(env, len(env) * WIN)
            trimmed = takes / f"{stem.name}.trim.wav"
            fade_out = max(0.0, t1 - t0 - FADE)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-af",
                            f"atrim={t0:.3f}:{t1:.3f},asetpts=N/SR/TB,afade=t=in:d={FADE},"
                            f"afade=t=out:st={fade_out:.3f}:d={FADE}",
                            "-ar", str(SR), "-ac", "1", str(trimmed)], check=True)
            if not edges_quiet(trimmed):
                bad.append(f"{i:02d}.{k} {s[:40]!r}")
            if k:
                t += gap
                parts.append(f"anullsrc=r={SR}:cl=mono,atrim=0:{gap}")
            parts.append(str(trimmed))
            # HeyGen's timings run late by about the gap between its first-word timestamp and the
            # real onset; shift the sentence's words back by it so captions don't lag the voice.
            late = min(max(0.0, ws[0]["start"] - (t0 + LEAD)), 0.35)
            for w in ws:
                words.append({"id": f"w{len(words)}", "text": w["text"],
                              "start": round(max(0.0, t + w["start"] - late - t0), 4),
                              "end": round(max(0.0, t + w["end"] - late - t0), 4)})
            t += t1 - t0
        inputs, labels = [], []
        for n, p in enumerate(parts):
            inputs += ["-f", "lavfi", "-i", p] if p.startswith("anullsrc") else ["-i", p]
            labels.append(f"[{n}:a]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
                        f"{''.join(labels)}concat=n={len(parts)}:v=0:a=1",
                        "-ar", str(SR), "-ac", "1", str(out / f"{i:02d}.wav")], check=True)
        (out / f"{i:02d}.words.json").write_text(json.dumps(words, indent=1))
        print(f"{i:02d} {len(words)} words, {t:.2f}s voiced")
    if bad:
        print(f"Failed: {len(bad)} take(s) cut on speech: " + "; ".join(bad))
        return 1
    wavs = {f"{i:02d}.wav": sha1(out / f"{i:02d}.wav") for i in range(1, len(lines) + 1)}
    (out / MANIFEST).write_text(json.dumps({"tool": "voice_build", "speed": speed, "gap": gap,
                                            "files": wavs}, indent=1))
    print(f"Voice: {len(lines)} lines, every take trimmed on silence")
    return 0


MANIFEST = "voice_build.json"


def sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def check(video: Path) -> list[str]:
    """Problems that must stop delivery; [] means the voice is clean."""
    voice = video / "hf" / "assets" / "voice"
    try:
        files = json.loads((voice / MANIFEST).read_text())["files"]
    except (OSError, ValueError, KeyError):
        return [f"no {MANIFEST}: voice the script with scripts/voice_build.py "
                "(never trim takes on TTS timestamps: they run late and cut words)"]
    errs = []
    on_disk = {p.name for p in voice.glob("*.wav")}
    for extra in sorted(on_disk - set(files)):
        errs.append(f"{extra} wasn't made by voice_build.py")
    for name, digest in sorted(files.items()):
        p = voice / name
        if not p.is_file():
            errs.append(f"{name} is missing")
        elif sha1(p) != digest:
            errs.append(f"{name} changed after voice_build.py made it")
        elif not edges_quiet(p):
            errs.append(f"{name} starts or ends on speech")
    return errs


def main(argv: list[str]) -> int:
    if argv[:1] == ["--check"] and len(argv) == 2:
        sc.adopt_root_from(Path(argv[1]))
        sc.load_env()
        errs = check(Path(argv[1]).resolve())
        print("Voice check: PASS" if not errs else "Failed: voice check — " + "; ".join(errs))
        return 1 if errs else 0
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--speed", type=float, help="TTS speed (default: config voice.speed, 0.75)")
    ap.add_argument("--gap", type=float, help="breath between sentences, s (default: config voice.gap, 0.35)")
    a = ap.parse_args(argv)
    sc.adopt_root_from(a.video)
    sc.load_env()
    v = sc.load()["voice"]
    speed = a.speed if a.speed is not None else v.get("speed", 0.75)
    gap = a.gap if a.gap is not None else v.get("gap", 0.35)
    return build(a.video.resolve(), speed, gap)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
