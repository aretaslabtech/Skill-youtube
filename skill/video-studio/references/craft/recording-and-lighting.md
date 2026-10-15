# Recording and lighting — when you film or record yourself

Most videos are faceless (HyperFrames + cloned VO). This file covers the three times real
capture is needed: the one-time **voice-clone sample**, occasional **voice-over takes**, and
**face shots** for service and build-story videos (a human on screen is one of Meta's
"extra elements" that lift Reels performance; Google's Shorts-ads study favours talking
straight to camera, scrappy over polished). Budget assumes a phone, one inexpensive LED light, and a room.

## 1. Lighting

### Setup A — window only (free)
- Face the window with it **~45° to one side**, not behind you and not dead-on. Shoot mid-morning or
  mid-afternoon; avoid direct sun on the face (hard shadows, squinting). Hang a white bedsheet
  over the window if sun hits it — that's free diffusion.
- Bounce: white foam board, chart paper or a white bedsheet on the shadow side, 60–90 cm from the
  face. Move it closer until the shadow side is visibly lighter but still darker than the lit side.
- Turn **off** all room lights (warm tubes/LEDs mixed with daylight make one cheek orange).
- Weakness: changes with clouds; record the whole take in one 20-minute window.

### Setup B — one light + bounce (the default)
- **Key**: one LED panel/softbox, daylight **5000–5600 K, CRI ≥ 90**, diffused (softbox, shower
  curtain, or baking paper — keep paper ≥ 15 cm from hot bulbs).
- Position: **45° to the side, raised so it points down ~30–45°**, about **1–1.5 m** from the face
  (closer = softer; a big source close by is the cheapest soft light).
- Check: a small shadow of the nose falls toward the cheek, not down onto the lip (too high) and not
  straight back (too frontal). Catchlight visible in both eyes.
- **Fill** = the bounce board on the other side, giving a **~2:1 key:fill** (shadow side about half
  as bright). Brighter fill = flat/corporate; no fill = moody, too dark for a service video.
- Glasses: raise the key and move it further to the side until the reflection leaves the lens.

### Setup C — three-point (when the background is dark or cluttered)
- Add a **back/rim light** behind and to the side opposite the key, aimed at hair/shoulders, just
  bright enough to draw an outline. Or, if the wall is close behind, aim a small lamp at the wall
  instead (background separation).
- All sources the same colour temperature. A practical lamp in the background (warm, small, out of
  focus) is allowed as decoration — it's the one exception to "match everything".

### Background and room
- 1–2 m between you and the wall, so it falls darker and softer than you.
- Plain or deliberately composed: a bookshelf, a monitor showing real code/our product. No bed, no
  laundry, no bright window behind you (silhouette).
- Turn off the ceiling fan for audio, and for picture (it flickers some LED light and moves hair).

### Troubleshooting

| You see | Fix |
|---|---|
| Flat, "passport" face | Fill too strong — move the bounce away |
| Dark eye sockets / hard shadow under nose and chin | Key too high or too hard — lower it, diffuse it |
| You blend into the background | Add rim light or move away from the wall |
| Orange one side, blue the other | Mixed colour temperatures — kill room lights or match Kelvin |
| Flicker/rolling bands | LED/tube flicker vs shutter — 1/50 s shutter under 50 Hz mains (India, Europe; 1/60 under 60 Hz) |

## 2. Phone camera

| Setting | Value | Why |
|---|---|---|
| Lens | **Rear main camera** (1×), not the selfie camera | Much better sensor; use a mirror app or a cheap monitor/second phone to frame |
| Resolution | 4K if storage allows, else 1080p | 4K lets us punch in 1.5× without visible loss for a 1080 output |
| Frame rate | **25 or 30 fps, fixed** | Our timeline is 30 fps; never let the editor guess the rate from a variable-frame-rate clip |
| Shutter (pro mode / Blackmagic Camera / FiLMiC) | 180° rule: **1/50 at 25 fps, 1/60 at 30 fps** | Natural motion blur. Under 50 Hz mains lighting prefer 25 fps + 1/50 if you see flicker |
| Focus/exposure | Long-press on the eye → **AE/AF lock**, then drag exposure down ~⅓ stop | Stops pumping as you move; protects skin highlights |
| HDR video | **Off** | HDR exports badly to social and mismatches our SDR BT.709 graphics |
| White balance | Lock to the light (5000–5600 K) | Stops colour drift mid-take |
| Stabilisation | On if handheld; off on a tripod | — |
| Mount | Tripod or a stack of books; lens at **eye level** | Lens above eye = looking down at the viewer; below = up the nose |

**Framing**
- 9:16 talking head: eyes on the upper-third line — **y ≈ 600–700 of 1920** — which keeps the
  face below the 288 px top UI zone. Head-to-chest framing, ~10 % headroom.
- Leave the bottom 35 % free of anything important (captions + platform UI).
- 16:9: subject on one third, the other third holds the graphic we'll add; eyes on the top third.
- Look into the lens, not at the screen. Put a sticky note with a face next to the lens if it helps.

## 3. Voice recording (VO takes and the clone sample)

### Room
- Smallest soft room you have; a **wardrobe full of clothes** is the best free booth. Otherwise
  hang duvets/blankets behind and to the sides of the mic covering ~60 % of the nearby walls (a
  fully dead room also sounds wrong).
- Kill: ceiling fan, AC, fridge (if in the room), phone notifications (flight mode), laptop fans.
  Record late night or early morning to miss horns, pressure-cooker whistles and construction.
- If a noise can't be removed, put it **behind** a cardioid mic (its dead side).

### Mic and placement
- Best → acceptable: USB/XLR dynamic or condenser mic → lav mic into the phone → phone held close.
- Distance: **15–20 cm** (two fists) for a mic; **~15 cm (6 in)** for a phone. Keep it constant —
  don't lean in or turn your head.
- Angle the mic **~30–45° off-axis**, aimed at the corner of the mouth, to keep P/B plosives off it.
  Pop filter if you have one. Test line: "Peter Piper picked a peck of pickled peppers."
- Mount on a stand/boom, not on the desk you're typing on.

### Levels and format
- Speaking average around **−18 dBFS** (ElevenLabs' clone guidance: RMS **−23 to −18 dB**), peaks
  **−6 to −3 dBFS**, never touching 0. Set gain with your loudest line first.
- Record **10 s of room tone** (silence, same position) before the take.
- Format: **WAV, 48 kHz, 24-bit, mono** (lossless, and 48 kHz matches the video timeline); iPhone Voice Memos → set
  audio quality to **Lossless**. Never record to a compressed voice-note format.
- No processing on the raw take: no noise suppression, no compression, no EQ, no music.
- Headphones on playback; listen for hum, fan, echo, mouth clicks, before re-recording.

## 4. The voice-clone reference (one-time, ~10 min of work)

The studio clones locally (Pocket TTS for English, IndicF5 for Hindi; `docs/voice.md`), and
both learn from a short reference. What cloning guides (HeyGen's, ElevenLabs') and our own runs
agree on:
- **Length**: **20–30 s of natural, expressive speech** for Pocket. For IndicF5, keep a **6–10 s
  clip that ends on a pause** and write down its exact words: a reference over ~15 s gets
  clipped while its text doesn't, and the clone cuts words off.
- **Clean**: one voice, no music, no background noise; the clone copies the room, so the room
  matters more than the mic.
- **Expressive, not flat**: cloning flattens tone — read with clear rises and falls, smile where it
  fits. A flat read produces a flat voice (the "TTS plateau" slop tell).
- **Match the use**: read the kind of script the clone will speak (our teaching VO), in the
  language you'll use, in your natural accent — don't put on an accent; include words where
  your accent shows.
- **Steady**: same distance, same energy, one sitting. No long pauses, no "umm"s (they get
  cloned), but natural breaths are fine. Leave ~1 s between paragraphs.

### Script to read (≈ 230 words, ~95 s at a natural pace)

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
> We build things like this every day: puzzle games, browser extensions, and chat bots that
> let a small shop answer "how much is this?" at eleven at night — so the owner can finally
> sleep. [Swap in your own products, and a phrase in your audience's own words.]
>
> Quick numbers: three hundred and twelve dollars, ninety-nine point nine percent, twenty
> twenty-six, version two point two. [Use your currency.]
>
> If this helped, follow along — tomorrow's question is even better. Seriously, you'll like it.

Why this script: questions, exclamations, a whisper of humour, numbers read the way we'll need
them, Python/AI terms (dictionary, O of n, embedding), your product names, and a phrase in
your audience's own words — the clone learns from what you read.

### After recording
1. Trim head/tail silence. Remove steady hiss with FFmpeg `arnndn` (it gets cloned otherwise);
   don't normalise beyond peak −3 dBFS.
2. Save as `voice/sample.wav` in your studio and set `voice.reference` in `config.json` (for
   Hindi: the 6–10 s clip and `reference_text` under `voice.variants.hi`).
3. Run the setup mode in `SKILL.md`; it installs the engine and voices a test.
4. Acceptance test: generate the Two Sum beat sheet VO (`teaching-formats.md`) and listen for:
   pitch movement on questions, natural pauses at full stops, correct "O of n", no metallic room
   echo. If it's flat, re-record more expressively — don't tweak settings first.

## Sources

- https://subscribr.ai/youtube-strategy/3-point-lighting-youtube-guide
- https://markus-hagner-photography.com/how-to-shoot-a-talking-head-video-with-professional-lighting-on-a-budget/
- https://www.provideocoalition.com/get-180-shutter-speed-smartphone-videos/amp/
- https://www.redsharknews.com/8-tips-for-better-vocal-recordings
- https://www.heygen.com/blog/how-to-perfect-your-ai-voice-clone
- https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning
- https://elevenlabs.io/blog/7-tips-for-creating-a-professional-grade-voice-clone-in-elevenlabs
- https://business.google.com/in/think/marketing-strategies/short-form-video-advertising-tips/
- https://blog.adobe.com/en/publish/2024/11/04/unlock-potential-reels-best-practices-for-creative-success-using-adobe-creative-cloud
- https://www.opus.pro/blog/ai-slop-aesthetic-12-tells
