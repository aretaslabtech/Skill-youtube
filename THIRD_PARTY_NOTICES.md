# Third-party notices

This repository's own code and docs are MIT-licensed ([LICENSE](LICENSE)). It also bundles,
or depends on, the following. Each keeps its own licence.

## Bundled

| Component | Where | Licence | Notes |
|---|---|---|---|
| [animate](https://github.com/cth9191/animate) by cth9191 | `skill/video-studio/vendor/animate/` | MIT — [`LICENSE`](skill/video-studio/vendor/animate/LICENSE) | Vendored unmodified from commit `7e5eb56` (v0.4.0); see `VENDORED.md`. Only `package.json`, `package-lock.json`, `.gitignore` and `VENDORED.md` there are ours |
| [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) by Jakeschincariol | `skill/video-studio/vendor/igtext/` | MIT — [`LICENSE`](skill/video-studio/vendor/igtext/LICENSE) | `caption.py`, `humanize.py`, `detect.py` and `slop.json` vendored unmodified from commit `d03c56b`; see `VENDORED.md`, which is ours |
| [Plus Jakarta Sans](https://github.com/tokotype/PlusJakartaSans) | `skill/video-studio/assets/fonts/` | SIL Open Font License 1.1 — [`OFL-plusjakartasans.txt`](skill/video-studio/assets/fonts/OFL-plusjakartasans.txt) | Latin subset from Google Fonts |
| [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono) | `skill/video-studio/assets/fonts/` | SIL Open Font License 1.1 — [`OFL-jetbrainsmono.txt`](skill/video-studio/assets/fonts/OFL-jetbrainsmono.txt) | Latin subset from Google Fonts |
| Prompt excerpts from [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) | `skill/video-studio/references/prompt-library.md` | The list is MIT; each excerpt is short, quoted for commentary, and linked to its source | Credit belongs to the original creators named in each entry |
| Style rules adapted from [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) by Lemomo | `skill/video-studio/references/looks.md` (the **Craft**, **Moves**, **Sound** and **Pitfalls** notes in `blueprint` and `whiteboard`) | MIT | Paraphrased and adapted to HyperFrames from its `styles/blueprint/STYLE.md` and `styles/whiteboard/STYLE.md`; no code copied |
| [GSAP](https://gsap.com) (loaded from a CDN, not bundled) | `skill/video-studio/assets/captions/*.html` | GSAP's standard licence | Fetched at render time |

## Required at runtime, not bundled

| Component | Licence |
|---|---|
| [HyperFrames](https://github.com/heygen-com/hyperframes) and its agent skills | Apache 2.0 |
| [Pocket TTS](https://github.com/kyutai-labs/pocket-tts) (Kyutai), installed by `install_voice.sh pocket` | code MIT; model weights CC-BY-4.0 (credit Kyutai) |
| [IndicF5](https://github.com/AI4Bharat/IndicF5) (AI4Bharat), installed by `install_voice.sh indicf5` | MIT |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) and Whisper models, for word timings | MIT |
| [HeyGen API](https://developers.heygen.com), only if you enable HyperFrames' music retrieval | Commercial service; your account and its terms |
| [Claude Code](https://code.claude.com) | Anthropic's terms |
| [FFmpeg](https://ffmpeg.org) | LGPL/GPL, depending on your build |
| [Playwright](https://playwright.dev) (for animate) | Apache 2.0 |
| [Manim Community](https://www.manim.community/) (optional) | MIT |
