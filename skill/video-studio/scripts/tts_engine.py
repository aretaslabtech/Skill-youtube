#!/usr/bin/env python3
"""
tts_engine.py — the open-source voice engines. Runs inside an engine's own virtualenv
(made by `scripts/install_voice.sh <engine>`); voice_build.py calls it once per build with a
job file, so each model loads once.

  <venv>/bin/python tts_engine.py job.json

Engines (both clone your voice from a short reference recording, offline, on CPU):
  pocket   Kyutai Pocket TTS — English (and a few European languages). ~1x real time on 4 cores.
  indicf5  AI4Bharat IndicF5 — Hindi and 10 other Indian languages. ~30x real time on 4 cores,
           so a 60 s Short needs ~30 min of voicing: fine overnight, slow interactively.

For every item it writes `<wav>` (mono, the engine's rate) and `<json>` = {"words": [...]}: the
script's own words with start/end times from faster-whisper, run on the final audio.

Job file:
  {"engine": "pocket"|"indicf5", "reference": "/abs/ref.wav", "reference_text": "...",
   "language": "english_2026-04", "asr_language": "en", "speed": 0.82, "best_of": 1,
   "max_pause": 0.6, "items": [{"text": "...", "say": "...", "wav": "...", "json": "..."}]}

  text   what the captions show (the script's words)
  say    what the engine is asked to speak (text with TTS spellings applied)
  speed  tempo applied after synthesis with ffmpeg atempo (1.0 = as spoken; pitch kept)
  best_of  candidates per sentence; the one Whisper hears closest to the text wins
  max_pause  longest silence kept inside a sentence, s (Pocket sometimes stalls mid-sentence)
"""
import os
import sys

# This folder also holds packaging.py (the A24 gate), which shadows the pip "packaging"
# module that transformers/torch import ("cannot import name 'version' from packaging",
# 26 Oct 2026, first IndicF5 run after packaging.py was added). Drop the script dir from
# sys.path: nothing here imports a sibling module.
_here = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != _here]

import difflib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

ASR_RATE = 16000
INDICF5_MAX_REF = 12.0   # F5 clips a longer reference but keeps all of reference_text → cut-off words


def to16k(a: np.ndarray, sr: int) -> np.ndarray:
    a = a if a.ndim == 1 else a.mean(1)
    idx = np.round(np.arange(0, len(a), sr / ASR_RATE)).astype(int)
    return a[idx[idx < len(a)]].astype(np.float32)


def norm(s: str) -> str:
    return re.sub(r"[^\w ]", "", s.lower())


def cap_pauses(a: np.ndarray, sr: int, max_pause: float) -> np.ndarray:
    """Shorten any silent run inside the speech (10 ms windows under -35 dBFS) to max_pause."""
    n, thr = int(0.01 * sr), 10 ** (-35 / 20)
    loud = np.array([np.abs(a[i:i + n]).max() > thr for i in range(0, len(a), n)])
    idx = np.flatnonzero(loud)
    if not len(idx):
        return a
    keep, pos, run = [], 0, None
    for k in range(idx[0], idx[-1] + 1):
        if not loud[k]:
            run = k if run is None else run
        elif run is not None:
            if (k - run) * 0.01 > max_pause:
                cut_at, cut_to = int((run * 0.01 + max_pause / 2) * sr), int((k * 0.01 - max_pause / 2) * sr)
                keep.append(a[pos:cut_at])
                pos = cut_to
            run = None
    keep.append(a[pos:])
    return np.concatenate(keep)


def tempo(a: np.ndarray, sr: int, speed: float) -> np.ndarray:
    if abs(speed - 1.0) < 1e-3:
        return a
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d) / "in.wav", Path(d) / "out.wav"
        sf.write(src, a, sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", f"atempo={speed}", str(dst)], check=True)
        out, _ = sf.read(dst, dtype="float32")
    return out


def word_times(asr, a16: np.ndarray, text: str, lang: str) -> list[dict]:
    """The script's words, timed by Whisper. Equal counts map one to one; otherwise (numbers,
    contractions, other scripts) the words are spread over the heard span by length."""
    segs, _ = asr.transcribe(a16, language=lang, word_timestamps=True, initial_prompt=text)
    heard = [w for s in segs for w in (s.words or [])]
    script = text.split()
    if len(heard) == len(script):
        return [{"text": t, "start": round(w.start, 3), "end": round(w.end, 3)} for t, w in zip(script, heard)]
    a, b = (heard[0].start, heard[-1].end) if heard else (0.0, len(a16) / ASR_RATE)
    total = sum(len(t) + 1 for t in script)
    out, t0 = [], a
    for t in script:
        d = (b - a) * (len(t) + 1) / total
        out.append({"text": t, "start": round(t0, 3), "end": round(t0 + d * 0.9, 3)})
        t0 += d
    return out


def heard_score(asr, a16: np.ndarray, text: str, lang: str) -> float:
    segs, _ = asr.transcribe(a16, language=lang)
    heard = " ".join(s.text.strip() for s in segs)
    return difflib.SequenceMatcher(None, norm(heard), norm(text)).ratio()


class Pocket:
    def __init__(self, job):
        from pocket_tts.models.tts_model import TTSModel
        self.tts = TTSModel.load_model(language=job.get("language") or "english_2026-04")
        self.state = self.tts.get_state_for_audio_prompt(job["reference"])
        self.sr = self.tts.sample_rate

    def say(self, text: str) -> np.ndarray:
        return self.tts.generate_audio(self.state, text).numpy().astype(np.float32)


class IndicF5:
    SR = 24000

    def __init__(self, job):
        from transformers import AutoModel
        ref = job["reference"]
        if sf.info(ref).duration > INDICF5_MAX_REF:
            raise SystemExit(f"Failed: IndicF5 reference is {sf.info(ref).duration:.1f} s; use a 6–10 s clip that ends "
                             f"on a pause (over {INDICF5_MAX_REF:.0f} s, F5 clips the audio but not the text, and words get cut off)")
        if not job.get("reference_text"):
            raise SystemExit("Failed: IndicF5 needs voice.reference_text: the exact words spoken in the reference")
        self.model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True)
        self.model.config.remove_sil = False   # its silence trim can eat word endings
        self.ref, self.ref_text, self.sr = ref, job["reference_text"], self.SR

    def say(self, text: str) -> np.ndarray:
        """F5 plans a take's length from the reference's chars-per-second and fills it exactly, so
        a short sentence comes out rushed and its last word cut off ("ना कोई एरर, ना कुछ।" got
        1.07 s, still voiced at the end). Plan short sentences slower (F5 itself does this for
        under 10 bytes), and if a take still ends on speech, plan it longer again."""
        speed = min(1.0, max(0.5, len(text) / 30))
        for _ in range(3):
            self.model.config.speed = speed
            a = np.asarray(self.model(text, ref_audio_path=self.ref, ref_text=self.ref_text))
            if a.dtype == np.int16 or np.abs(a).max() > 1.5:
                a = a.astype(np.float32) / 32768.0
            a = a.astype(np.float32)
            if np.abs(a[-int(0.02 * self.SR):]).max() <= 0.03 * (np.abs(a).max() or 1):
                break
            speed = max(0.4, speed - 0.15)
        return a


ENGINES = {"pocket": Pocket, "indicf5": IndicF5}


def main(job_path: str) -> int:
    job = json.loads(Path(job_path).read_text())
    if job["engine"] not in ENGINES:
        raise SystemExit(f"Failed: unknown voice engine {job['engine']!r} (pocket | indicf5)")
    from faster_whisper import WhisperModel
    lang = job.get("asr_language") or "en"
    engine = ENGINES[job["engine"]](job)
    asr = WhisperModel("small.en" if lang == "en" else "small", device="cpu", compute_type="int8")
    for it in job["items"]:
        best = None
        for _ in range(max(1, int(job.get("best_of", 1)))):
            a = engine.say(it["say"])
            a = cap_pauses(a, engine.sr, float(job.get("max_pause", 0.6)))
            a = tempo(a, engine.sr, float(job.get("speed", 1.0)))
            score = heard_score(asr, to16k(a, engine.sr), it["text"], lang) if job.get("best_of", 1) > 1 else 1.0
            if best is None or score > best[0]:
                best = (score, a)
        a = best[1]
        sf.write(it["wav"], a, engine.sr)
        words = word_times(asr, to16k(a, engine.sr), it["text"], lang)
        Path(it["json"]).write_text(json.dumps({"words": words}, ensure_ascii=False, indent=1))
        print(f"take {Path(it['wav']).name[:48]} {len(a) / engine.sr:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
