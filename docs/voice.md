# Cloning your voice

The voice is what viewers notice first, and it is where our studio went wrong most often.
This page is the method that worked, with the measurements behind it.

Since 15 Oct 2026 the studio clones your voice with **open-source models that run on your own
CPU**: no voice subscription, no per-minute bill, nothing uploaded. (It started on a paid
HeyGen clone; the numbers from that period are at the end.)

| Engine | Languages | Speed on 4 CPU cores | Reference it needs | Licence |
|---|---|---|---|---|
| `pocket`: [Pocket TTS](https://github.com/kyutai-labs/pocket-tts) (Kyutai) | English (also French, German, Spanish, Italian, Portuguese, Dutch) | ~1× real time | 20–30 s of you talking | code MIT, model CC-BY-4.0 |
| `indicf5`: [IndicF5](https://github.com/AI4Bharat/IndicF5) (AI4Bharat) | Hindi, Bengali, Gujarati, Marathi, Punjabi, Odia, Assamese, Tamil, Telugu, Kannada, Malayalam | ~30× real time (a 60 s Short ≈ 30 min) | a **6–10 s** clip plus its exact words | MIT |

Word timings for captions come from [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
(MIT), run on each finished take.

We tried others first. XTTS-v2 speaks Hindi and clones well, but its licence (CPML) forbids
commercial use and its Hindi sounded flat; Chatterbox and NeuTTS were 3–6× slower than Pocket
on CPU and add an inaudible watermark.

## 1. Install the engines

Both models are gated on Hugging Face. Accept the terms on
[kyutai/pocket-tts](https://huggingface.co/kyutai/pocket-tts) and
[ai4bharat/IndicF5](https://huggingface.co/ai4bharat/IndicF5), then:

```bash
pip install -U huggingface_hub && hf auth login
STUDIO_ROOT=~/my-studio skill/video-studio/scripts/install_voice.sh pocket
STUDIO_ROOT=~/my-studio skill/video-studio/scripts/install_voice.sh indicf5   # only for Hindi etc.
```

Each engine gets its own virtualenv in `~/my-studio/.venvs/<engine>` (CPU builds of PyTorch),
because their dependencies conflict. IndicF5 is pinned on purpose: with transformers 5.x it
fails to load ("Tensor on device cpu is not on the expected device meta"), and datasets 4
pulls a pyarrow that needs NumPy 2.

## 2. Record your reference (about 10 minutes)

- **Room over mic.** The clone copies the room. Pick the quietest room with the least echo,
  and hold a phone about 15 cm (6 inches) from your mouth. A phone voice note is enough.
- **Expressive, not flat.** Cloning keeps your rhythm and energy. Read with clear rises and
  falls, a little surprise, a little annoyance; a flat read makes a flat voice.
- **Talk like you would to a friend**, in the language the clone will speak. A Hindi voice
  cloned from an English recording sounds like an English speaker reading Hindi.
- **Steady.** One sitting, same distance, no "umm"s (they get cloned).
- **Clean the hiss.** Background hiss gets cloned too. RNNoise in FFmpeg removes it
  ([model files](https://github.com/GregorR/rnnoise-models)):
  `ffmpeg -i note.ogg -af arnndn=m=sh.rnnn -ac 1 -ar 24000 voice/sample.wav`

**English (Pocket):** 20–30 s is enough. Save it as `voice/sample.wav`.

**Hindi (IndicF5):** record 20–30 s, then keep **a 6–10 s clip that ends on a pause** and
write down exactly the words in it:

```bash
ffmpeg -i voice/hindi-note.wav -t 6.7 -af "afade=t=out:st=6.5:d=0.2" voice/hindi.wav
```

**Short sentences need more room too.** F5 fills the length it plans exactly, so a short
sentence came out rushed with its last word cut ("ना कोई एरर, ना कुछ।": 1.07 s, still voiced at
the end, and gate B17 refused it). `tts_engine.py` plans sentences under ~30 characters
proportionally slower and re-plans any take that still ends on speech.

**Why the clip must be short:** F5 cuts a reference longer than ~15 s, but keeps *all* of
`reference_text`, so it believes you speak faster than you do, plans every sentence too short,
and **chops the end off words**. Our first Hindi takes had exactly this bug; the 6.7 s clip
fixed it, and the same lines came out 21.7 s long instead of 15.7 s. `tts_engine.py` refuses a
reference over 12 s.

### Scripts to read

English (replace the bracketed parts; it exercises questions, exclamations, numbers and
technical words):

> Hi, I'm [your name], and this is [your channel]. Let's solve one problem today — properly.
> Here's the question: given a list of numbers and a target, find the two numbers that add up
> to it. The obvious way? Check every pair. That works… until your list has a million items.
> So flip the question. If I'm holding six and the target is ten, I need four. Have I seen four
> already? A dictionary answers that instantly. One pass. Done! Quick numbers: three hundred and
> twelve, ninety-nine point nine percent, version two point two.

Hindi (conversational, the way the videos will sound):

> यार, आज एक मज़ेदार चीज़ हुई। मेरी पाइथन स्क्रिप्ट पूरे चार घंटे चलती रही, और एक भी एरर नहीं
> आया! मुझे लगा सब ठीक है… पर नहीं भाई। वो तो एक ही यू-आर-एल पर अटकी पड़ी थी। पता है क्यों?
> क्योंकि रिक्वेस्ट्स लाइब्रेरी में डिफ़ॉल्ट टाइमआउट होता ही नहीं है। अब सोचो, कितना टाइम बर्बाद
> हुआ! तो सीधी सी बात है, हर रिक्वेस्ट पर टाइमआउट लगाओ। बस।

## 3. Configure it

```json
"voice": {
  "engine": "pocket",
  "reference": "voice/sample.wav",
  "language": "english_2026-04",
  "speed": 0.82,
  "gap": 0.35,
  "variants": {
    "hi": {
      "engine": "indicf5",
      "reference": "voice/hindi.wav",
      "reference_text": "यार, आज एक मज़ेदार चीज़ हुई। मेरी पाइथन स्क्रिप्ट पूरे चार घंटे चलती रही, और एक भी एरर नहीं आया!",
      "asr_language": "hi",
      "speed": 1.0
    }
  }
}
```

`python3 voice_build.py <video>` uses the default voice; `--voice hi` lays the `hi` variant over
it. Pocket's `language` picks a model version: `english_2026-04` kept an Indian-English
accent better than the default. Every key is in
[configuration.md](configuration.md).

## 4. Fix the pace — per sentence, not per line

A clone speaks at the speed of the person who recorded it, which is usually too fast for a
learner to follow. On our voice, Pocket slowed to 0.64× sounded slow and drawn out;
**`speed: 0.82`** (FFmpeg `atempo` after synthesis, pitch kept) was the setting that stuck.
IndicF5 already speaks at a comfortable pace in Hindi, so its variant uses **1.0**.

`voice_build.py` voices **each sentence separately** and joins them with a **`gap`** breath,
so fixing one sentence re-voices only that sentence. Takes are cached by a hash of the text,
engine, reference and speed. The engine runs once per build, so the model loads once.

## 5. Spell it for the voice, not the captions

Engines read symbols badly: `timeout=(3.05, 10)`, `S113`, `s.get`. Put spoken spellings in
`hf/say.json`; the engine says them, the captions keep the script's words:

```json
{"timeout=(3.05, 10)": "timeout equals three point oh five, ten", "S113": "S one thirteen", "s.get": "s dot get"}
```

What we learned voicing our videos with Pocket:

- **Quoted phrases lose words.** `sees "Error executing tool query".` lost "tool query" in 5 of
  5 takes. Drop the quotes from what is spoken.
- **Whisper mishears some words**, which skews the timings and the best-of score: "Strip" →
  "Script", "each brace" → "each place". Swapping a synonym in the script is cheaper than
  re-rolling takes. `voice.best_of: 3` voices each sentence three times and keeps the one
  Whisper hears closest to the script.
- **Long pauses mid-sentence.** Pocket sometimes stalls; `max_pause` (0.6 s) shortens any
  silence inside a sentence.
- **Pocket takes were 2–3 dB quieter** than our HeyGen takes had been. If the voice sounds buried, lower
  the music bed (about 0.035) rather than raising the voice.

For Hindi, **write the way people talk**: Hinglish, "तो हुआ ये कि…", "अब सोचो…". Textbook
Hindi, voiced correctly, still sounded flat to native listeners. Sentences end with `।`;
`voice_build.py` splits on it.

## 6. Never trim on timestamps

Every engine and ASR returns word timestamps, and they are off by tenths of a second. Our first
trim cut each take at the first word's timestamp, and sliced the start off a third of all
sentences — "The" became "e", "Step" became "tep" — on a promo, 12 of 44 sentences.

`voice_build.py` cuts each take at its first and last **audible** 10 ms window (above 3% of
the take's peak), keeps a little padding, adds 8 ms fades, and fails if a trimmed take still
starts or ends on speech. It writes `voice_build.json`, a hash of every voice file, and
`deliver.py` refuses any video whose voice wasn't made — or was changed after — by this
script (gate B17).

## What it costs

Nothing but CPU time: about real time for English, about 30× real time for Hindi on 4 cores
(an overnight cron hides both). Disk: ~1 GB for Pocket and Whisper, ~3 GB for IndicF5.

For comparison, the HeyGen clone the studio used until October 2026 cost about **$0.14 per
minute** of narration (346 characters → 22.8 s → $0.05; 967 characters → 58.9 s → $0.14),
allowed 30 requests a minute, and stopped the pipeline the day its prepaid credit ran out.
