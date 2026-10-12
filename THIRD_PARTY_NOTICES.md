# Third-party notices

This repository's own code and docs are MIT-licensed ([LICENSE](LICENSE)). It also bundles,
or depends on, the following. Each keeps its own licence.

## Bundled

| Component | Where | Licence | Notes |
|---|---|---|---|
| [animate](https://github.com/cth9191/animate) by cth9191 | `skill/video-studio/vendor/animate/` | MIT — [`LICENSE`](skill/video-studio/vendor/animate/LICENSE) | Vendored unmodified from commit `7e5eb56` (v0.4.0); see `VENDORED.md`. Only `package.json`, `package-lock.json`, `.gitignore` and `VENDORED.md` there are ours |
| [Plus Jakarta Sans](https://github.com/tokotype/PlusJakartaSans) | `skill/video-studio/assets/fonts/` | SIL Open Font License 1.1 — [`OFL-plusjakartasans.txt`](skill/video-studio/assets/fonts/OFL-plusjakartasans.txt) | Latin subset from Google Fonts |
| [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono) | `skill/video-studio/assets/fonts/` | SIL Open Font License 1.1 — [`OFL-jetbrainsmono.txt`](skill/video-studio/assets/fonts/OFL-jetbrainsmono.txt) | Latin subset from Google Fonts |
| Prompt excerpts from [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) | `skill/video-studio/references/prompt-library.md` | The list is MIT; each excerpt is short, quoted for commentary, and linked to its source | Credit belongs to the original creators named in each entry |
| [GSAP](https://gsap.com) (loaded from a CDN, not bundled) | `skill/video-studio/assets/captions/*.html` | GSAP's standard licence | Fetched at render time |

## Required at runtime, not bundled

| Component | Licence |
|---|---|
| [HyperFrames](https://github.com/heygen-com/hyperframes) and its agent skills | Apache 2.0 |
| [HeyGen API](https://developers.heygen.com) | Commercial service; your account and its terms |
| [Claude Code](https://code.claude.com) | Anthropic's terms |
| [FFmpeg](https://ffmpeg.org) | LGPL/GPL, depending on your build |
| [Playwright](https://playwright.dev) (for animate) | Apache 2.0 |
| [Manim Community](https://www.manim.community/) (optional) | MIT |
