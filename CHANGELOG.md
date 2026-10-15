# Changelog

## Unreleased

- **Open-source voices; HeyGen voice cloning removed.** The voice is now a clone of your own
  recording made offline on CPU: [Pocket TTS](https://github.com/kyutai-labs/pocket-tts) for
  English, [IndicF5](https://github.com/AI4Bharat/IndicF5) for Hindi and 10 other Indian
  languages. `scripts/tts_engine.py` runs each engine in its own virtualenv
  (`scripts/install_voice.sh pocket|indicf5`); `voice_build.py` voices every missing sentence in
  one engine run, times words with faster-whisper, and keeps the trim-on-real-sound logic and
  the B17 manifest. New config: `voice.engine`, `reference`, `reference_text`, `language`,
  `asr_language`, `best_of`, `max_pause`, and `variants` (`voice_build.py --voice hi`).
  `hf/say.json` holds spoken spellings. Sentences also split on the Devanagari `।`.
  `HEYGEN_API_KEY` is no longer required (`bin/run.sh` checks the voice engine instead);
  `voice.voice_id`, `HEYGEN_VOICE_ID` and `HEYGEN_TTS_SCRIPT` are gone. Take caches from
  earlier versions aren't reused.
- **Script rules rewritten for developers.** The "smart 12-year-old who never coded" viewer
  overcorrected: viewers called the scripts childish, and 67 % swiped away in the first 3 s.
  Based on research into top tech Shorts, the viewer is now a developer or CS student who
  already codes, and known terms are never defined. Every Short carries at least one artifact
  worth saving and ≥ 3 named specifics per 30 s, and runs 35–60 s (75 s cap).
  `craft/script-voice.md` has per-pillar templates.
- **Hooks:** sentence 1 is ≤ 14 words and names the concrete subject plus a tension, with the
  proof on screen by 1.5 s and a rehook every 10–15 s. `craft/hooks.md` gains a 20-template
  library from real Shorts. A20's cold viewer plays a developer scrolling Reels.
- **A16** is now a new-to-me review: a mid-level developer must name a concrete thing it
  learned and who it would send the video to.
- **`script_lint.py` (A18):** a hook check (length, banned openers, a concrete subject), 20-word
  sentences, ≥ 3 specifics per 30 s (a documented heuristic; `backticked` screen terms count),
  and `jargon.txt` narrowed to terms beyond a CS student. The reading-grade and
  number-density caps are dropped.
- **Pacing is configurable:** `config.json` "pacing" (`max_gap`, `payoff_gap`) sets the B16
  limits that `gap_check.py` reads, for channels that want a pause after every sentence.

- Looks: `blueprint` and `whiteboard` gain craft, sound and pitfall notes adapted from
  [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) (MIT): drafting order and zoom-scaled
  line weights for blueprint; the board as a map, multiply ink, deadline-timed strokes and the sheen for whiteboard.

## 1.0.1 — 2026-10-12

- Installable as a Claude Code plugin: `claude plugin marketplace add cybiqon-ai/faceless-video-studio`,
  then `claude plugin install faceless-video-studio@faceless-video-studio`. `/video-studio setup`
  now scaffolds a new studio itself; `install.sh --studio-only` and `STUDIO_SKILL` support plugin installs.
- Blog explainers are 16:9 (1920×1080, 90–150 s): they are embedded in the post itself.
- README: a demo GIF; the full demo video and a social preview image are on the v1.0.1 release.

## 1.0.0 — 2026-10-12

First public release, extracted from the studio Cybiqon has run daily since 8 October 2026.

- `video-studio` skill: seven modes (`daily`, `promo`, `blog`, `plan`, `build`, `revise`,
  `setup`); pillars for AI terms, Python, builds, tech news, promos and blog explainers, plus
  long-form deep dives and their companion Shorts.
- 38 pass/fail gates (33 hard), six of them checked by `deliver.py` before delivery.
- Per-sentence HeyGen voicing trimmed on real sound, with a hash manifest (B17).
- 22 look families, a look rotation and a variety gate; four caption skins.
- Engines: HyperFrames, the vendored animate (7 styles), optional Manim.
- Everything machine-specific moved to the studio folder: `config.json` tracks and rotation,
  `brand/`, `.env`, and optional `links`, `notify` and `planner` plugins.
- Telegram delivery built in (`telegram.py`), or the post kit saved locally.
- `bin/run.sh` for unattended runs: lock, ceilings, budget cap, count-not-status alerts.
- `install.sh`, `studio.example/`, `examples/cybiqon/`, docs, CI with a leak check.
