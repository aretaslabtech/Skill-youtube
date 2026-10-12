# Changelog

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
