#!/usr/bin/env python3
"""
voice_build.py — voice a script one sentence at a time, and never cut into a word.

  python3 voice_build.py <video-dir> [--voice hi] [--speed 0.82] [--gap 0.35]
  python3 voice_build.py --check <video-dir>     # the delivery gate (deliver.py runs it)

Voices every sentence of `hf/SCRIPT.md` (indented lines) separately with an open-source voice
clone of your reference recording (config.json "voice"; `--voice hi` picks voice.variants.hi),
trims each take to its **audible** speech, and joins a line's sentences with a `--gap` breath.
Each line is then compressed and set to one loudness (voice.lufs, default -16 LUFS), so the
voice sits clearly above the music bed (mix_check.py holds the bed under it).
Writes `hf/assets/voice/NN.wav` + `NN.words.json`, one per script line (the shape HyperFrames'
`audio.mjs sync-durations` reads). Takes are cached in `research/voice-takes/`, so a rerun
voices only sentences that changed.

Engines (scripts/tts_engine.py, each in its own virtualenv from scripts/install_voice.sh):
  pocket   Kyutai Pocket TTS: English. ~1x real time on 4 CPU cores.
  indicf5  AI4Bharat IndicF5: Hindi and 10 other Indian languages. ~30x real time on CPU.
Word timings come from faster-whisper on the final audio. `hf/say.json` ({"written": "spoken"})
changes what the engine is asked to say (S113 → "S one thirteen") while captions keep the script.

Why per sentence: one long take drifts in pace and can't be retried in part; per sentence, with
the configured breath (voice.gap) between sentences, keeps gaps inside B16's limit.

Why trim on the audio, not on the word timings: TTS and ASR timestamps both run late or early
by tenths of a second, and viewers reported words being cut off. Trimming at
`first_word.start − 0.08` sliced the start off a third of all sentences ("The" → "e",
"Step" → "tep"). Now each take is cut at its first and last audible 10 ms window, plus
padding, with 8 ms fades. The build fails if any trimmed take starts or ends on speech.

The gate: the build writes `hf/assets/voice/voice_build.json`, a manifest with every line's
sha1. `--check` (and `deliver.py`, for every track: daily, companion, promo, blog) refuses a
video whose voice files weren't made by this script, were changed after it, or start or end
on speech.
"""
import argparse
import hashlib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import studio_config as sc  # noqa: E402

def voice_settings(variant: str | None = None) -> dict:
    """config.json "voice", with voice.variants[variant] laid over it (e.g. "hi" for Hindi)."""
    v = dict(sc.load()["voice"])
    variants = v.pop("variants", {}) or {}
    if variant:
        if variant not in variants:
            raise SystemExit(f"Failed: no voice.variants.{variant} in config.json (have: {', '.join(variants) or 'none'})")
        v.update(variants[variant])
    if not v.get("reference"):
        raise SystemExit("Failed: no voice.reference — record a sample (docs/voice.md) and set config.json "
                         "voice.reference (run /video-studio setup)")
    ref = Path(v["reference"]).expanduser()
    v["reference"] = str(ref if ref.is_absolute() else sc.root() / ref)
    if not Path(v["reference"]).is_file():
        raise SystemExit(f"Failed: voice.reference {v['reference']} not found")
    return v


def engine_python(v: dict) -> str:
    """The engine's interpreter: voice.python, else $STUDIO_ROOT/.venvs/<engine>/bin/python."""
    py = v.get("python") or str(sc.root() / ".venvs" / v["engine"] / "bin" / "python")
    if not Path(py).expanduser().is_file():
        raise SystemExit(f"Failed: no {v['engine']} engine at {py} — run scripts/install_voice.sh {v['engine']}")
    return str(Path(py).expanduser())


SR = 44100
LEAD, TAIL = 0.06, 0.12   # silence kept before the first and after the last audible sound
FADE = 0.008
WIN = 0.01                # energy window (s)
THRESH = 0.03             # audible = window peak above 3 % of the take's peak
SENT_RE = re.compile(r"[^.?!।]+(?:[.?!।]+|$)")   # । is the Devanagari full stop


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


def lufs(path: Path) -> float:
    """Integrated loudness (EBU R128) of a file, in LUFS."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else -70.0


def level(src: Path, dst: Path, v: dict) -> None:
    """Make the voice present and even (owner, 16 Oct 2026: "the voiceover is still low"):
    a gentle compressor tames the peaks, then a static gain brings every line to the same
    loudness (voice.lufs, default -16), under a -1.5 dBFS limiter. Static gain, not loudnorm:
    loudnorm on a 5 s line pumps."""
    comp = "acompressor=threshold=-24dB:ratio=3:attack=5:release=120:knee=4"
    squeezed = src.with_suffix(".comp.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", comp, "-ar", str(SR), "-ac", "1",
                    str(squeezed)], check=True)
    gain = max(-12.0, min(18.0, float(v.get("lufs", -16)) - lufs(squeezed)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(squeezed), "-af",
                    f"volume={gain:.2f}dB,alimiter=limit=0.84:level=disabled",
                    "-ar", str(SR), "-ac", "1", str(dst)], check=True)


def stem_for(i: int, k: int, sentence: str, say: str, v: dict, speed: float) -> str:
    """Cache name of a take: position, a readable slug, and a hash of everything that shapes the
    audio, so an edited sentence or a new reference is voiced again and nothing else is."""
    key = json.dumps([say, v["engine"], v["reference"], v.get("reference_text", ""), v.get("language", ""), speed])
    slug = re.sub(r"[^a-z]", "", sentence.lower())[:40]
    return f"{i:02d}-{k}-{v['engine']}{speed}-{slug}-{hashlib.sha1(key.encode()).hexdigest()[:8]}"


def apply_say(sentence: str, say: dict) -> str:
    for written, spoken in sorted(say.items(), key=lambda kv: -len(kv[0])):
        sentence = sentence.replace(written, spoken)
    return sentence


def synthesize(items: list[dict], v: dict, speed: float, takes: Path) -> None:
    """Voice every missing take in one engine run (the model loads once)."""
    todo = [it for it in items if not Path(it["json"]).exists()]
    if not todo:
        return
    job = {"engine": v["engine"], "reference": v["reference"], "reference_text": v.get("reference_text", ""),
           "language": v.get("language", ""), "asr_language": v.get("asr_language", "en"), "speed": speed,
           "best_of": int(v.get("best_of", 1)), "max_pause": float(v.get("max_pause", 0.6)), "items": todo}
    job_file = takes / "job.json"
    job_file.write_text(json.dumps(job, ensure_ascii=False, indent=1))
    print(f"Voicing {len(todo)} sentence(s) with {v['engine']}…", flush=True)
    r = subprocess.run([engine_python(v), str(Path(__file__).resolve().parent / "tts_engine.py"), str(job_file)])
    missing = [it["text"][:40] for it in todo if not Path(it["json"]).exists()]
    if r.returncode or missing:
        raise SystemExit(f"Failed: {v['engine']} engine exited {r.returncode}; not voiced: {missing}")


def build(video: Path, v: dict, speed: float, gap: float) -> int:
    hf = video / "hf"
    lines = [l[4:].strip() for l in (hf / "SCRIPT.md").read_text().splitlines() if l.startswith("    ")]
    say = json.loads((hf / "say.json").read_text()) if (hf / "say.json").is_file() else {}
    takes = video / "research" / "voice-takes"
    takes.mkdir(parents=True, exist_ok=True)
    out = hf / "assets" / "voice"
    out.mkdir(parents=True, exist_ok=True)
    plan = []   # (line, sentence index, sentence, stem)
    for i, line in enumerate(lines, 1):
        for k, s in enumerate(sentences(line)):
            spoken = apply_say(s, say)
            plan.append((i, k, s, takes / stem_for(i, k, s, spoken, v, speed), spoken))
    synthesize([{"text": s, "say": spoken, "wav": f"{stem}.wav", "json": f"{stem}.json"}
                for _, _, s, stem, spoken in plan], v, speed, takes)
    bad = []
    for i, line in enumerate(lines, 1):
        parts, words, t = [], [], 0.0
        for _, k, s, stem, _ in [p for p in plan if p[0] == i]:
            wav = Path(f"{stem}.wav")
            ws = json.loads(Path(f"{stem}.json").read_text())["words"]
            env = envelope(wav)
            length = len(env) * WIN
            t0, t1 = cut_points(env, length)
            # The energy-threshold detector can read a quiet trailing consonant, or a
            # falling-pitch tail, as silence before the ASR's own transcription actually
            # finishes (a 25 Oct 2026 audit found 71/218 sentences on one script landed
            # within TAIL of, or before, the ASR's own last-word end — audible words were
            # getting clipped). Never trim tighter than where the ASR itself heard real
            # speech, plus the same lead/tail padding used elsewhere.
            if ws:
                t0 = min(t0, max(0.0, ws[0]["start"] - LEAD))
                t1 = max(t1, min(length, ws[-1]["end"] + TAIL))
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
            # If the first word's timestamp runs late against the real onset, shift the sentence's
            # words back by the difference so captions don't lag the voice.
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
                        "-ar", str(SR), "-ac", "1", str(takes / f"line{i:02d}.raw.wav")], check=True)
        level(takes / f"line{i:02d}.raw.wav", out / f"{i:02d}.wav", v)
        (out / f"{i:02d}.words.json").write_text(json.dumps(words, ensure_ascii=False, indent=1))
        print(f"{i:02d} {len(words)} words, {t:.2f}s voiced")
    if bad:
        print(f"Failed: {len(bad)} take(s) cut on speech: " + "; ".join(bad))
        return 1
    wavs = {f"{i:02d}.wav": sha1(out / f"{i:02d}.wav") for i in range(1, len(lines) + 1)}
    (out / MANIFEST).write_text(json.dumps({"tool": "voice_build", "engine": v["engine"], "speed": speed,
                                            "gap": gap, "files": wavs}, indent=1))
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
    ap.add_argument("--voice", help="a voice.variants key in config.json, e.g. hi")
    ap.add_argument("--speed", type=float, help="tempo after synthesis (default: config voice.speed)")
    ap.add_argument("--gap", type=float, help="breath between sentences, s (default: config voice.gap, 0.35)")
    a = ap.parse_args(argv)
    sc.adopt_root_from(a.video)
    sc.load_env()
    v = voice_settings(a.voice)
    speed = a.speed if a.speed is not None else v.get("speed", 1.0)
    gap = a.gap if a.gap is not None else v.get("gap", 0.35)
    return build(a.video.resolve(), v, speed, gap)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
