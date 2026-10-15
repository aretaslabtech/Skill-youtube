---
workflow: <faceless-explainer | product-launch-video | general-video>
flow: automation
storyboard: no
message: "<PLAN.md message>"
destination: <youtube-shorts | youtube>
aspect: <1080x1920 | 1920x1080>
language: en
length: <e.g. 45s>
angle: <concept | tutorial | promo | story>
audience: "<PLAN.md audience>"
voice: <config voice engine + variant, e.g. pocket, or indicf5 (hi)>
---

## Intent

<Two or three lines from PLAN.md §1 and §4: what the video is, for whom, and the tone.>
Built by the video studio (`/video-studio`). PLAN.md in this folder is the
storyboard of record: follow its beats, narration and on-screen text exactly.

## Assets

- assets/fonts/fonts.css — Plus Jakarta Sans + JetBrains Mono, vendored; link it if the look uses them, otherwise use the look's fonts from frame.md
- assets/logo.png — the brand logo (brand/logo.png), end card only
- <each asset from PLAN.md §8: path — what it is — where it belongs>

## Customizations

- Design spec: frame.md, built from the look family <x> (references/looks.md) plus the brand core: #00D890 as the one accent. Follow the look's layout grammar and motion vocabulary; it must not look like the studio's previous videos.
- Caption skin: .hyperframes/caption-skin.html (assets/captions/<name>).
- Real footage, where there is any, fills the frame (≥ 80%) for at least half the runtime; labels sit on top of it, never beside a shrunken card.
- Layout (9:16, organic, `platform-specs.md` §1): hook y 200–440; the visual fills y 440–1440 (x ≤ 850 below y 1150) and continues into y 1600–1920 without text; word-synced captions of 2–4 words in y 1440–1600, x 64–850, with the key word in voltage. Never leave the bottom 40 % as empty ground (B18).
- <bespoke asks from the storyboard, e.g. "array cells fill as the pointer moves", "O(n²) morphs to O(n)">

## Notes

- **Render is pre-approved (standing instruction).** After
  `check` passes and the contact sheet is reviewed, render without asking. Do not start
  the Studio preview server.
- **Voice is fixed:** already made by `scripts/voice_build.py` into `assets/voice/`. Do not
  voice anything else, and do not call a cloud TTS or fall back to Kokoro. If voicing failed,
  stop and report the blocker.
- **Music:** the media-use BGM step (or a CC0 track from the studio's library), mood "<from PLAN.md>", ducked about 20 dB under the voice.
  None on the hook's first second.
- Avoid: everything in frame.md `avoid:` and references/quality-rubric.md B5.
