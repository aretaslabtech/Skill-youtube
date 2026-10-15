# Troubleshooting

Every entry here cost us at least one failed run. Most are now handled by the skill; they are
listed so you recognise them.

## Setup

**`no pocket engine at …/.venvs/pocket/bin/python`** — run
`STUDIO_ROOT=<studio> skill/video-studio/scripts/install_voice.sh pocket` (or `indicf5`).

**`could not download kyutai/pocket-tts`** (or `ai4bharat/IndicF5`) — the models are gated.
Accept the terms on the model page with the account you logged in with (`hf auth whoami`).

**`no voice.reference`** — record a sample (docs/voice.md) and set `voice.reference` in
`config.json`.

**Fonts fail to load / a look needs a font you don't have** — some machines can't reach
Google Fonts. Pick a look whose fonts are vendored (`assets/fonts/`) or embedded by the
HyperFrames compiler (Montserrat, Oswald, League Gothic, Archivo Black, Space Mono, IBM Plex
Mono, JetBrains Mono, Source Code Pro).

## Voice

**Words cut off at the start of sentences** — something trimmed takes on timestamps, which run
late. Re-voice with `voice_build.py`; `deliver.py` refuses audio it didn't build (B17).

**Hindi words cut off at the end** — the IndicF5 reference is too long, or `reference_text`
doesn't match it word for word. Use a 6–10 s clip that ends on a pause, with exactly its words.

**IndicF5: `Tensor on device cpu is not on the expected device meta`** — transformers 5.x got
installed. Re-run `install_voice.sh indicf5` (it pins 4.49.0).

**The narration is too fast** — lower `voice.speed` a step (0.82 → 0.75); don't slow whole
lines, and don't go much below 0.7 or it drawls.

**A word goes missing in every take** — Pocket drops words after a quoted phrase; remove the
quotes from what is spoken (`hf/say.json`). Set `voice.best_of: 3` for stubborn sentences.

**Voicing is slow** — IndicF5 runs at ~30× real time on CPU, so a 60 s Hindi Short needs about
half an hour. Run it from the overnight cron, or on a GPU machine.

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
