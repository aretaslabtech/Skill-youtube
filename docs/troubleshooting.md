# Troubleshooting

Every entry here cost us at least one failed run. Most are now handled by the skill; they are
listed so you recognise them.

## Setup

**`heygen-tts.mjs not found`** — the HyperFrames skills aren't installed, or are somewhere
unusual. Install them (`npx skills add heygen-com/hyperframes`) or set `HEYGEN_TTS_SCRIPT` to
the file's full path in `.env`.

**`no voice id`** — run `/video-studio setup`, or put your HeyGen voice id in `config.json` →
`voice.voice_id` (or `HEYGEN_VOICE_ID` in `.env`).

**`npx hyperframes auth status` doesn't report HeyGen** — the key isn't loaded in that shell.
`set -a; . ./.env; set +a` first.

**Fonts fail to load / a look needs a font you don't have** — some machines can't reach
Google Fonts. Pick a look whose fonts are vendored (`assets/fonts/`) or embedded by the
HyperFrames compiler (Montserrat, Oswald, League Gothic, Archivo Black, Space Mono, IBM Plex
Mono, JetBrains Mono, Source Code Pro).

## Voice

**Words cut off at the start of sentences** — something trimmed takes on TTS timestamps,
which run ~0.2 s late. Re-voice with `voice_build.py`; `deliver.py` refuses audio it didn't
build (B17).

**The narration is too fast** — measure words per second (setup reports it). Keep per-
sentence voicing at speed 0.75 and adjust `voice.speed`/`voice.gap`; don't slow whole lines.

**Lines refused, or missing, after a voicing step** — HeyGen allows 30 TTS requests a minute,
and parallel batches can fail quietly. `voice_build.py` retries with backoff; don't run more
than ~4 voice jobs at once.

**Gaps of several seconds between sentences** — frames were padded to fit their animation.
Shorten the animation or add a spoken line; `gap_check.py` enforces ≤ 0.7 s (B16).

## Building and rendering

**Footage clips disappeared from a frame after assembling** — HyperFrames' `assemble-index.mjs`
moves each frame's `<video>` out before validating the others, and if validation fails it
exits with the clips already gone. Back up `compositions/frames` before assembling (the skill
does) and restore from it on any error.

**Overlays hidden behind footage** — the assembler hoists videos to the root, above their
frame's labels. Check the z-order in `index.html` after assembling.

**Soft, upscaled screen recordings** — Chrome's CDP screencast can deliver 360×640 frames
whatever size you request. Capture with `page.screenshot({clip})` at device pixel ratio 3
instead (true 1080 px, about 7.5 fps), or take stills.

**The video's first frame shows the wrong part of a clip** — the render's frame 0 can ignore a
`<video>`'s `data-media-start`, even when every browser snapshot looks right. Pre-trim clips
with FFmpeg, and always decode frame 0 of the final MP4 (B14).

**The bottom of every Short is empty** — the layout used YouTube's *ads* safe zone. Organic
Shorts can fill the frame; see `references/craft/platform-specs.md` §1 and gate B18.

**Renders are slow** — that's normal on a laptop. Our 4-CPU machine took 144–188 s for a
~75 s Short and 790–1,168 s for a 7-minute long-form. Every fix after rendering costs a full
render again, so check snapshots before rendering.

**`animate: … is not deterministic`** — an animate piece used the clock or an unseeded
random. Use the kit's seeded `RNG()` only.

## Delivery and scheduling

**`Failed: PLAN.md is missing 'A16: PASS (judge)'`** — the review gates didn't run or didn't
pass. That's the gate working: run them; never write the line by hand.

**A video arrives on Telegram as a file path** — it was over the 50 MB bot limit even after
re-encoding. The full file is on disk for YouTube.

**Cron ran but no video, and no alert** — check `logs/`. If the log is empty, cron couldn't
start the script: set `PATH` in the crontab, and use absolute paths.

**No video and the alert says "logged out"** — run `claude` on the machine and `/login`.

**Every job ran at the wrong hour** — the machine's timezone changed. Cron uses local time;
convert the entries.
