# Video engines — what else Claude makes videos with (researched 12 Oct 2026)

HyperFrames (HTML + GSAP → MP4) is our composition layer and stays the only delivery path.
Anything below is a **second engine** that renders a clip we lay in (full-bleed or, with alpha,
over our graphics). The question was how others use Claude to make videos, and how to get more dynamic videos
with less repetition.

Most sources are third-party write-ups. Before installing anything, read the repo's README.

## In use

| Engine | Status | Good for | Output |
|---|---|---|---|
| **animate** (cth9191, MIT, vendored at `vendor/animate/`, commit `7e5eb56`) | **Vendored.** Pilot: the pixel demo at 9:16 rendered in ~12 s, deterministic across two page loads, B18 PASS inside a HyperFrames comp | the seven animate families (`looks.md` 16–22); era morphs | Opaque H.264 via `scripts/animate_clip.sh` |
| **Manim** Community 0.22 (optional: a venv of ~480 MB plus system cairo/pango dev packages; **no LaTeX needed**) | **Optional.** Measured: 6.5 s at 1080×1920 rendered in 17 s, peak RAM 0.86 GB. The transparent WebM keeps its alpha through HyperFrames (checked over a gradient) | Maths, algorithms, data structures and equations morphing, on any look, layered **over** our stage | Alpha WebM via `scripts/manim_clip.sh` |
| **HyperFrames adapters** (already installed: Three.js, Lottie, TypeGPU, about 400 registry blocks) | Barely used. Use them for signature beats first, since they cost nothing to add | 3D hero shots, character loops, shader moments | Native, in the comp |

## Candidates (not installed)

| Engine | What it's good at | Clip we'd get | When to add it |
|---|---|---|---|
| **Remotion** ([transparent video](https://www.remotion.dev/docs/transparent-videos), [agent skills](https://www.tella.com/blog/how-to-use-remotion-agent-skills-with-claude-code.md)) | React motion graphics; strong caption, map and 3D (R3F) skills | Alpha WebM (VP8/VP9 `yuva420p`) or ProRes 4444 | Only if a React component library becomes worth reusing. Overlaps HyperFrames |
| **Motion Canvas / Revideo** ([pkgpulse comparison](https://www.pkgpulse.com/guides/remotion-vs-motion-canvas-vs-revideo-programmatic-video-2026), [Revideo](https://docs.re.video/)) | Precise canvas scene graphs, code animations | PNG sequence or MP4 | Low priority, because animate already covers canvas |
| **Blender via MCP** ([real-world test](https://www.mindstudio.ai/blog/claude-blender-mcp-real-world-performance)) | Grey-box 3D scenes and simple object animation. Claude's spatial sense is imprecise and rigging is unrealistic | PNG sequence with alpha | Maybe one 3D hero shot a week, if a topic needs it |
| **After Effects MCP** ([mcp-ae](https://glama.ai/mcp/servers/shibin0/mcp-ae)) | Keyframes, comps, expressions | ProRes 4444 | No: it needs After Effects open and can't run headless |

## Ideas we took (12 Oct)
1. **Style as a swappable kit, rotated:** the 22 look families with `look-check`
   ([animate](https://github.com/cth9191/animate)).
2. **One signature beat per video,** never repeated within 5 (`visual-design.md` §10), mined
   from [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) via
   `prompt-library.md`.
3. **A banned-defaults list** in `brand-core.md`
   ([SuperDesign](https://www.superdesign.dev/blog/how-to-make-claude-code-ui-look-good)).
4. **Review real frames, not assumptions:** B14 on the final MP4, now also checking for text
   collisions (the idea behind animate's `textcheck.mjs`).
5. **Refine, don't restart:** revisions apply one targeted fix at a time
   ([claudecodeformarketers](https://claudecodeformarketers.com/blog/motion-graphics-with-hyperframes/)).

## Rules for any new engine
- It must be **deterministic**: the same time gives the same pixels. Prove it with two renders
  and a frame hash before production.
- It renders a **clip**. Voice, captions, the hook frame and the end mark stay in HyperFrames.
- It prints a **count line** (frames, seconds, size), never just "done".
- Record it here the same day, with what it renders and how it was checked.
