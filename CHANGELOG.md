# Changelog

## Unreleased

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
