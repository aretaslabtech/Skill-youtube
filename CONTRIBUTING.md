# Contributing

Thanks for wanting to make it better. The bar for a change is the same as the bar for a
video: does it make what a viewer sees or hears better, and can it be checked?

## Good first contributions

- **A new look family** in `skill/video-studio/references/looks.md`: palette, fonts,
  layout grammar, motion and the pillars it suits, built from material that exists (a
  HyperFrames preset, registry blocks, an animate style).
- **A new caption skin** in `skill/video-studio/assets/captions/` that keeps captions inside
  y 1440–1600 on 9:16.
- **A new plugin example** (`notify` for Slack/Discord/email, `links` for another store).
- **A gate that turns a failure you saw into code.** Describe the video that failed, the rule,
  and how it is checked.

## Before you open a pull request

```bash
cd skill/video-studio/scripts
python3 -m unittest            # every test, against a throwaway studio
cd ../../.. && scripts/leak_check.sh
```

Both run in CI on every push.

- Keep the deterministic parts (`scripts/`) stdlib-only Python 3.10+.
- Every number in the docs needs a source: a measurement, a log, or a linked page.
- Never commit a real `.env`, voice id, API key, chat id, log or render.
- Don't edit `vendor/animate/`: re-vendor a newer upstream commit instead (see `VENDORED.md`).

## Reporting a bad video

Open an issue with the pillar, the look family, what was wrong (a frame grab helps), and the
gate you think should have caught it. That's how most of the 44 gates were born.
