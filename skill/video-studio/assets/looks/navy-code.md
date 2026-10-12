---
version: alpha
name: Look — navy-code (the studio's first look; one of references/looks.md)
description: >
  The studio's first look, and a safe default. Copy it into the project as `frame.md`
  (spec resolution reads frame.md first), then pick ONE pillar variant below and delete the
  others. Atoms are sacred: a tinted navy-black canvas (never #000), off-white text (never #fff),
  ONE voltage accent — the brand accent from brand-core.md — used scarcely, Plus Jakarta Sans
  for display and UI, JetBrains Mono for code and kickers. Navy #00304f, accent #00D890.
unit: 1080×1920 primary (Shorts / Reels); 1920×1080 for long-form
principle: atoms are sacred · composition is free · every number comes from the research dossier

colors:
  # Key names matter: HyperFrames maps roles by name (canvas → ground, text → ink role,
  # status names like error/caution are never picked as the accent). Keep `canvas` first.
  # — dark ground (default: teaching, product, build story) —
  canvas: "#0A1B29"         # the ground. Navy-tinted near-black; banding-safe flat fill
  canvas-raised: "#0F2638"  # cards, code panels
  canvas-elev: "#15324A"    # active panel, table header
  text: "#EAF1F7"           # primary text on canvas (never pure white)
  navy: "#00304F"           # brand navy — large shapes, end card
  mist: "#9DB3C6"           # secondary text, axis labels, indices
  hairline: "#EAF1F7@14%"
  voltage: "#00D890"        # THE accent: the answer, the insight, the CTA. ≤ 10% of any frame
  voltage-deep: "#00784F"   # accent as text on the light ground
  # — semantic, for teaching only (correctness, never decoration) —
  error: "#FF7A66"          # the naive/incorrect path, O(n²), a failing case
  caution: "#FFC566"        # pointer / "being read" outline / strings in code
  # — light ground (service videos for businesses) —
  light-ground: "#F4F7FB"
  light-text: "#0E2233"
  light-tile: "#E3EBF5"

typography:
  # Plus Jakarta Sans (variable 200–800) — display + UI. JetBrains Mono (100–800) — code, kickers, numbers in code.
  # Files: assets/fonts/ (vendored; link fonts.css). Never Inter (house brand on the web, but on HyperFrames' banned list).
  display-cover: { fontFamily: "Plus Jakarta Sans", px: 128, weight: 800, lineHeight: 0.98, tracking: "-0.03em" }
  display:       { fontFamily: "Plus Jakarta Sans", px: 96,  weight: 800, lineHeight: 1.02, tracking: "-0.025em" }
  headline:      { fontFamily: "Plus Jakarta Sans", px: 72,  weight: 700, lineHeight: 1.08, tracking: "-0.02em" }
  lead:          { fontFamily: "Plus Jakarta Sans", px: 44,  weight: 500, lineHeight: 1.3 }
  body:          { fontFamily: "Plus Jakarta Sans", px: 36,  weight: 400, lineHeight: 1.4 }
  kicker:        { fontFamily: "JetBrains Mono", px: 30, weight: 500, tracking: "0.14em", upper: true }
  code:          { fontFamily: "JetBrains Mono", px: 34, weight: 400, lineHeight: 1.55 }   # 9:16; ≤ 22 chars/line visible width
  code-16x9:     { fontFamily: "JetBrains Mono", px: 30, weight: 400, lineHeight: 1.6 }
  number-hero:   { fontFamily: "Plus Jakarta Sans", px: 220, weight: 800, lineHeight: 0.9, tracking: "-0.04em" }
  caption:       { fontFamily: "Plus Jakarta Sans", px: 54, weight: 800, lineHeight: 1.1 }  # word-synced captions, y 1440–1600
  # Weight contrast is the hierarchy: 800 display against 400 body. Never two sans families.

spacing:
  # 9:16 safe zones (references/craft/platform-specs.md): the strictest of YouTube's measured
  # overlay and Meta's guidance. Meaning lives in the core; captions in their band.
  core-zone: "y 200–1440; x 64–1016 above y 1150, x 64–850 below"   # organic layout, platform-specs §1
  caption-band: "y 1440–1600, x 64–850"   # word-synced captions; the scene continues below (B18)
  safe-top: "200px"
  safe-bottom: "320px"   # y 1600–1920: the scene continues, no text (B18)
  safe-right: "64px"     # above y 1150; 230px below it (the like/comment/share rail)
  safe-left: "64px"
  # 16:9 (long-form): content x 96–1824, y 96–860; captions y 880–1000.
  safe-16x9: "x 96–1824, y 96–860"
  # Usable width is 952 px (x 64–1016; keep the lower part inside x ≤ 850). Centre a shared
  # stage with left = 64 + (952 − stage_width) / 2.
  pad-16x9: "96px"
  radius-sm: "10px"
  radius-md: "16px"
  radius-lg: "28px"

components:
  code-panel:
    backgroundColor: "{colors.canvas-raised}"
    border: "1px solid {colors.hairline}"
    rounded: "{spacing.radius-md}"
    lineHighlight: "{colors.voltage}@16% full-width bar behind the active line; the line number turns voltage"
    syntax: "keywords text 700 · names text 400 · strings caution · numbers voltage · comments mist italic-free"
  state-panel:
    note: "variables/array cells as mono tiles; the cell being read gets a caution outline, a written cell flashes voltage"
  kicker-tag:
    note: "mono, uppercase, voltage text on canvas-elev pill — the series mark (e.g. SYSTEM DESIGN, AI, EXPLAINED)"
  end-card:
    note: "navy ground, logo (brand/logo.png) ≤ 120px, one line of CTA in headline, the handle from brand-core.md in kicker. 2.5 s, loops back visually to frame 1 where possible"

pillars:
  # Kicker = the series mark (JetBrains Mono, uppercase, voltage on a canvas-elev pill,
  # top-left of the safe area, first beats only). Signature = the visual identity.
  ai-term:
    ground: canvas
    kicker: "AI, EXPLAINED"
    signature: "one everyday object carries the whole explanation; the term appears only after the example has done the work"
  python:
    ground: canvas
    kicker: "PYTHON {version}"
    signature: "a code panel plus a terminal strip; the surprising output first, then the why; the version is always on screen"
  build:
    ground: canvas
    kicker: "BUILD IT"
    signature: "the finished thing running first; then a step counter (1/4 …) with only the changed lines lit"
  longform-ai:
    ground: canvas
    kicker: "AI, EXPLAINED"
    signature: "a chapter map (3–5 stations on a path) that returns at each break with the done station ticked in voltage"
  longform-sd:
    ground: canvas
    kicker: "SYSTEM DESIGN"
    signature: "ByteByteGo rule: a fixed boxes-and-arrows structure (≤ 7 boxes) with one moving flow; numbered steps; the chapter map as above"
  product:
    ground: canvas (or the product's own palette for the middle beats — real screenshots dominate)
    kicker: "BUILT BY US"
    signature: "real screen recordings / store screenshots in a device frame; no fake UI"
  service:
    ground: light-ground
    kicker: "FOR BUSINESSES"
    signature: "the business owner's problem in their words, then the before/after; one plain CTA"
  build-story:
    ground: canvas
    kicker: "BUILD LOG"
    signature: "git-log / terminal texture, real numbers from the repo or lab post"
avoid:
  - gradient text, neon cyan or purple glows, glassmorphism stacks
  - full-frame linear gradients on dark (they band under H.264) — use flat canvas + one soft radial ≤ 20% opacity
  - centred-everything; anchor to a left edge or a 2-column split
  - identical card grids; bullet lists read aloud verbatim
  - stock-photo people, fake app UI, invented metrics
---

# Notes

Video defaults to the dark ground because phones are watched in dark mode and code reads
better on it. The service pillar uses the light ground because it speaks to business
owners, and a light page reads as "for business" rather than "for developers".

`voltage` is scarce on purpose. If more than one element in a frame is green, the frame has
no focus. The answer, the insight and the CTA get it. Nothing else does.
