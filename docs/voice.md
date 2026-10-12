# Cloning your voice

The voice is what viewers notice first, and it is where our studio went wrong most often.
This page is the method that worked, with the measurements behind it.

## 1. Record one sample (about 20 minutes)

What HeyGen and the other cloning vendors agree on:

- **Length.** HeyGen's guide asks for 30–60 s of expressive speech; its developer docs say an
  instant clone uses only the first 3 minutes of a recording (MP3 or WAV, up to 100 MiB).
  ElevenLabs notes little gain beyond 2–3 minutes. **Record one continuous take of 90–120 s
  and keep the best 60–90 s.**
- **Room over mic.** The clone copies the room. Pick the quietest room with the least echo,
  and hold a phone about 15 cm (6 inches) from your mouth, as HeyGen's guide suggests.
- **Expressive, not flat.** Cloning flattens tone. Read with clear rises and falls and smile
  where it fits; a flat read makes a flat voice.
- **Read what the clone will say.** Your kind of script, your language, your natural accent,
  including the words where your accent shows.
- **Steady.** One sitting, same distance, same energy, no "umm"s (they get cloned).
- **Format.** WAV, 48 kHz, 24-bit, mono, peaks around −6 to −3 dBFS. No noise suppression,
  compression or EQ. On iPhone, set Voice Memos to Lossless.

Save it as `voice/sample.wav` in your studio.

### A script to read (about 230 words, ~95 s)

Replace the bracketed parts; the rest is chosen to exercise questions, exclamations, numbers
and technical words.

> Hi, I'm [your name], and this is [your channel]. Let's solve one problem today — properly.
>
> Here's the question: given a list of numbers and a target, find the two numbers that add up
> to it. The obvious way? Check every pair. That works… until your list has a million items.
> Then it's painfully slow.
>
> So flip the question. For each number, ask: what do I *need*? If I'm holding six and the
> target is ten, I need four. Have I seen four already? A dictionary answers that instantly.
> One pass. O of n. Done!
>
> Now, a harder one. What is an embedding, really? It's a list of numbers that captures what a
> sentence *means*. "Cheap flights" and "budget airfare" share zero words — but their embeddings
> sit right next to each other. Isn't that wild?
>
> We build things like this every day: [your products, in a sentence], and [one phrase in your
> audience's own words].
>
> Quick numbers: three hundred and twelve [your currency], ninety-nine point nine percent,
> twenty twenty-six, version two point two.
>
> If this helped, follow along — tomorrow's question is even better. Seriously, you'll like it.

## 2. Clone it

`/video-studio setup` clones `voice/sample.wav` through HeyGen's API and writes the voice id
to `config.json`. You can also clone it in HeyGen's web app and paste the id into
`voice.voice_id`. Creating an instant clone was free when we did it; check HeyGen's current
terms.

## 3. Fix the pace — per sentence, not per line

A clone speaks at the speed of the person who recorded it. Ours, voiced a whole line at a
time, measured **2.8–3.0 words per second at HeyGen speed 0.9** — far above the **2.0
words/s** a learner can follow. Slowing whole lines further made the voice drawl.

`scripts/voice_build.py` voices **each sentence separately at speed 0.75** and joins them
with a **0.35 s breath**. That lands at or under about 2.2 words/s, keeps the silence between
lines under 0.7 s (gate B16), and means fixing one sentence re-voices only that sentence.
Takes are cached, so a rerun costs nothing. Tune `voice.speed` and `voice.gap` in
`config.json` for your voice: setup reports your words per second.

## 4. Never trim on TTS timestamps

HeyGen returns word timestamps with every take. Its first-word timestamp runs about **0.2 s
late**. Our first trim cut each take at that timestamp, and sliced the start off a third of
all sentences — "The" became "e", "Step" became "tep" — on a promo, 12 of 44 sentences.

`voice_build.py` cuts each take at its first and last **audible** 10 ms window (above 3% of
the take's peak), keeps a little padding, adds 8 ms fades, and fails if a trimmed take still
starts or ends on speech. It writes `voice_build.json`, a hash of every voice file, and
`deliver.py` refuses any video whose voice wasn't made — or was changed after — by this
script (gate B17).

## 5. Mind the rate limit

HeyGen's documentation lists **30 requests per minute** for `POST /v3/voices/speech` on
pay-as-you-go and subscription accounts, and returns `429 Too Many Requests` beyond it. We
learned this when parallel voicing had 23 lines refused at once, silently, in a log.
`voice_build.py` voices sequentially and retries with exponential backoff and jitter, up to
six times. Don't run more than about four voice jobs in parallel.

## What it costs

Measured on our clone in October 2026 by checking the wallet before and after: 346
characters → 22.8 s of audio → $0.05; 967 characters → 58.9 s → $0.14. About **$0.14 per
minute** of narration. Twelve finished videos, with revisions and tests, used $8.20.
