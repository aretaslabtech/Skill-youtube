# Looks — the 22 look families

The rule: only the **brand core** stays constant. Everything else — palette, fonts,
layout grammar, motion vocabulary, transitions, caption style — changes from video to video.
One navy look every day reads as AI-generated.

**Brand core (every video, every family):**
- the voice (narration, script tone);
- the brand accent from `brand-core.md` (default green `#00D890`; every palette below uses
  it, so swap in yours) used **at least once as an accent**, never as a ground or body text
  colour. On light grounds green **text** is `#00784F`, and `#00D890` goes on fills, bars,
  boxes and strokes. A look may have **one** other accent hue besides green, never two;
- a **≤ 2 s end mark**: your handle from `brand-core.md` (plus `brand/logo.png` if it fits the look),
  set in the family's own type and ground, not a navy end card pasted onto a paper video.

Everything below is a starting point built from material that exists:
`~/.claude/skills/hyperframes-creative/frame-presets/<preset>/FRAME.md`, the motion rules in
`~/.claude/skills/hyperframes-animation/rules-index.md` (`rules/<name>.md`), the transitions
in `transitions/catalog.md`, and registry items (`npx hyperframes add <name>`).

## How to choose

1. **Recency first.** Run `python3 scripts/ledger.py looks --last 5`. Pick a family that is
   **not in the last 6 videos** (`look_check` refuses it otherwise); start from the top of `ledger.py rotation` (least recently used first, so every style gets used). The caption skin and the
   hook type must also differ from the previous video.
2. **Match the topic,** using the best-fit pillars on each family. If two families fit, take the
   one used longest ago. `navy-code` is no longer the default. It is one family among twenty-two. Families 16–22 run on
   the **animate engine** (`engine: animate`, SKILL.md § Engines).
3. **Footage rule.** In footage-based looks (`documentary`, `split-screen`, `collage-scrapbook`,
   and any `product` / `build-story` video), real footage and screen captures go **full-bleed:
   ≥ 80 % of the frame for ≥ 50 % of the runtime**. A device frame is allowed for one beat at
   most and never for the whole video. Graphics sit *on* the footage as lower thirds, callouts and
   annotations. Footage does not get boxed inside the graphics.
4. **Write the frame.** Copy the base preset's `FRAME.md` into the project as `frame.md`, apply
   the "change" line, put the palette under `colors:` (keep `canvas` first, and name the green
   `accent` or `voltage` so `--cap-accent` resolves to it), and then copy the family's caption
   skin from `assets/captions/` to `<project>/.hyperframes/caption-skin.html`.
5. **Record it.** The ledger entry gets `look_family`, `caption_skin` and `hook_type`.

**Fonts.** HyperFrames bundles 18 families. The ones that are bundled **and** not banned are
Montserrat, Oswald, League Gothic (400 only), Archivo Black (400 only), Space Mono, IBM Plex Mono,
JetBrains Mono and Source Code Pro. Plus Jakarta Sans is vendored in `assets/fonts/`. Any other
Google font (Newsreader, Instrument Serif, Barlow, Libre Baskerville, Shrikhand, Kalam …) must
be **embedded with `@font-face` (woff2 in the project)**. An implicit fetch lints and fails
closed in cloud renders. **Never** use Inter, Roboto, Open Sans, Lato, Nunito, Poppins, Outfit,
Sora, Syne, Playfair Display, EB Garamond, Bodoni Moda, Cormorant, Cinzel or Prata. Several
presets ship with them, and the swaps are given below.

**Caption skins** (`assets/captions/`; all four share one contract and the same safe bands):
| skin | look | needs |
|---|---|---|
| `glow-word` | no card, dim → **accent-lit** active word → ink | a dark ground (the accent is text) |
| `boxed-word` | League Gothic caps, active word in a **solid accent box** | a bright accent (green, red, orange) |
| `underline-bar` | `--font-display` sentence case, a thick **green bar wipes in** under the active word | any ground; set the accent token to green |
| `band-karaoke` | a full-width semi-opaque band, the active word **fills L→R** | a dark or mid band (footage, deep grounds) |

A preset's own `caption-skin.html` is a fifth option, but only after its 9:16 band has been
re-pinned to y 1440–1600. The engine's default band sits under the Shorts UI.

---

## 1. navy-code
**Essence:** the studio's original look. A tinted navy-black ground, a code panel, one green spark.
- **Pillars:** python, build, longform-sd. Use it sparingly, because viewers already know it.
- **Base:** none; use `assets/looks/navy-code.md` as it is (the pillar variants, kicker pills, code-panel spec).
- **Palette:** canvas `#0A1B29`, raised `#0F2638`, elev `#15324A`, text `#EAF1F7`, mist `#9DB3C6`;
  semantic `#FF7A66` (wrong path) and `#FFC566` (being read) in teaching only. **Green** marks the
  answer line, the written cell and the CTA, ≤ 10 % of any frame.
- **Type:** Plus Jakarta Sans 800/400 + JetBrains Mono 400/700 (both vendored).
- **Layout:** 9:16 has the code panel in x 64–1016, y 440–1150, a terminal strip under it down to y 1440, and a kicker
  pill at top-left. 16:9 uses a 2-column split, code on the left (≤ 60 %) and the state panel on the right.
- **Motion:** `discrete-text-sequence` (typing), `asr-keyword-glow`, `coordinate-target-zoom`,
  `stat-bars-and-fills`. **Transitions:** push slide, blur crossfade, zoom through.
- **Texture:** one soft green radial ≤ 20 % opacity; no gradients (they band under H.264).
- **Caption skin:** `glow-word`.
- **Registry:** `code-snippet-dark-modern`, `code-highlight`, `code-diff`, `terminal-simulator`.
- **Never:** two green elements in one frame; using it two videos in a row.
- **Signature moment:** the surprising output prints first, then the one line that caused it lights up green.

## 2. editorial-paper
**Essence:** a printed essay. Warm cream paper, a big serif, code set like a magazine pull-quote.
- **Pillars:** longform-ai, ai-term, python (concepts), longform-sd.
- **Base:** `code-editorial`. Swap EB Garamond → **Newsreader** (embed) and Inter → **IBM Plex Mono**
  for chrome and code. Keep the cream paper, the hairline elevation, the warm-navy code surface and the ✱ mark.
- **Palette:** cream `#FAF9F5`, tile `#EFE9DE`, ink `#141413`, code surface `#1F1E1B`, rule `#141413@12%`.
  Other accent: coral `#CC785C`, used only for the ✱ eyebrow mark. **Green** is the underline bar
  under the key term and the highlighted code line (`#00D890@22%` fill). As text it is `#00784F`.
- **Type:** Newsreader 400 (display, sentence case, tracking −0.03em) + IBM Plex Mono 400/700.
- **Layout:** 9:16 puts a left-aligned headline at y 300–700, one pull-quote and a code card under it, with
  45 % of the frame left empty. 16:9 uses a 12-col grid, text in cols 1–7 and the figure or code in cols 8–12, with a page number at bottom-right.
- **Motion:** `waterfall-entry` (headlines), `css-marker-patterns` (underline mode),
  `viewport-change` (slow pan down the "page"). **Transitions:** crossfade, vertical push, color dip (to cream).
- **Texture:** a faint paper grain (`grain-overlay` at 4–6 %) and 1px hairline rules.
- **Caption skin:** `underline-bar` (it follows Newsreader through `--font-display`).
- **Registry:** `code-scroll`, `ink-bleed-reveal`, `mk-line-graph`, `grain-overlay`.
- **Never:** dark grounds, heavy shadows, more than one coral mark per frame.
- **Signature moment:** a single serif sentence holds while the green bar draws under the one word that matters.

## 3. blueprint
**Essence:** a draftsman's sheet. Deep blueprint blue, a permanent grid, systems drawn line by line.
- **Pillars:** longform-sd, build, ai-term (architectures).
- **Base:** `cobalt-grid`. **Invert it** so the ground is deep cobalt and the ink is paper-white. Keep the
  permanent graph-paper grid, the top and bottom hairlines, and the "one element dominates 3–6×" squint rule.
- **Palette:** ground `#0D2B55`, grid minor `#DCE8FF@8%`, major `#DCE8FF@18%`, ink `#E6EEFF`, secondary
  `#8FA9D6`. Other accent: redline `#FF6B5B` (the naive path, the bottleneck). **Green** is the packet or
  request that flows through the drawing, plus the final "✓ scales" stamp.
- **Type:** Oswald 400/700 uppercase (draft lettering, tracking 0.06em) + Space Mono 400 (dimensions, labels).
- **Layout:** 9:16 stacks the system top to bottom (≤ 5 boxes) with dimension lines on the right edge. 16:9 lays
  boxes and arrows left to right (≤ 7 boxes, ByteByteGo rule) with a title block at bottom-right like a drawing sheet.
- **Motion:** `svg-path-draw` (every box and arrow draws itself), `svg-icon-enrichment` (dash-flow on live
  edges), `viewport-change` (zoom to a component). **Transitions:** zoom through, horizontal blinds (calm 4h), push slide.
- **Texture:** the grid, plus slow `sine-wave-loop` breathing on the drawing's crosshair marks.
- **Caption skin:** `band-karaoke` (the band in ground blue reads as the sheet's title strip).
- **Registry:** `dynamic-grid`, `svg-line-draw-loader`, `grid-card-assemble`, `outline-draw`.
- **Craft** *(adapted from lemo-opuscar's Blueprint style, MIT)*:
  - **Drafting order**, one layer per beat: centre lines → outlines → detail → hatching →
    dimensions → part balloons → labels. Each stroke draws by arc length with a small glowing nib at its head.
  - **Four line weights** (outline 3.2, detail 2.0, thin 1.25, hair 0.9 px at zoom 1). In a
    `viewport-change` zoom, scale stroke width by **zoom^0.65**, not zoom: close-ups don't turn into
    sausages and wides don't vanish.
  - **Real conventions:** centre lines long-short, hidden edges short dashes, 45° hatching (8–14 px
    apart) for anything cut open, numbered balloons on leader lines. Fill every box with ground blue
    before stroking its outline, so overlaps occlude cleanly.
  - **Live annotations:** a dimension line measures a moving part and its number changes (latency,
    queue depth, replicas). "FIG. 1" struck through and rewritten "FIG. 2 · WITH CACHE" is the transition between versions.
  - **The title block tells the story.** STATUS reads DRAFT, and the verdict stamp lands **once**:
    green `✓ SCALES`, or redline `REJECTED` for the naive design. Keep the title block clear of the caption band.
- **Sound:** a technical-pen scratch per stroke (length = stroke length), a soft paper slap on a
  cut, part clicks for the exploded view, one rubber-stamp thump on the verdict. Music is mechanical
  and contrapuntal (harpsichord, pizzicato, music box), ducked well under the voice. Leave the
  biggest reveal with no voice over it.
- **Pitfalls:** the main figure near the frame edge (keep ≥ 10 % margin at every zoom you'll use);
  explode parts **sideways**, never up into the header; line widths that don't scale with zoom.
- **Never:** filled cards, drop shadows, rounded "app" UI, more than one moving flow at a time,
  3D rendering (oblique and isometric projection are fine).
- **Signature moment:** the full system draws in white, then one green packet travels the whole path.

## 4. bold-poster
**Essence:** kinetic typography as a gig poster. Huge words slam in on the beat, and words do the whole job.
- **Pillars:** ai-term, python (what's new), service (the hook), product (launch beats).
- **Base:** `bold-poster`. Keep the four-colour palette, the 3px+1.5px double-border grid, the tilted display
  and the red em-dash bullets. Swap Shrikhand to **one hero word per video** (embedded) and use **Archivo Black**
  for every other slam.
- **Palette:** off-white `#F5F2EF`, white `#FFFFFF`, ink `#1C1410`. Other accent: red `#D8000F`.
  **Green** gets one slam per video: the answer or payoff word set in a solid `#00D890` block with ink type.
- **Type:** Archivo Black 400 (uppercase, tracking −0.03em, line-height 0.9) + Libre Baskerville italic
  (embedded) for the one-line setup.
- **Layout:** 9:16 has 1–3 words per frame at 180–260px, tilted ±4°, filling 70 % of the width. 16:9 uses
  poster columns, with the word block on the left and the double-rule grid on the right.
- **Motion:** `kinetic-beat-slam`, `3d-text-depth-layers` (stacked red extrusion), `counting-dynamic-scale`,
  `waterfall-entry`. **Transitions:** staggered blocks (full-frame), squeeze, zoom through.
- **Texture:** none (flat paper). The rhythm is the texture: optional metronome ticks from `kinetic-beat-slam`.
- **Caption skin:** `boxed-word`.
- **Registry:** `caption-kinetic-slam`, `kinetic-type-swap`, `variable-axis-type`, `weight-wave`.
- **Never:** more than 3 words on screen at once; red body text; a code panel.
- **Signature moment:** the setup line sits small in italic, then the answer slams in full-frame in a green block.

## 5. documentary
**Essence:** real footage carries the video. Full-bleed footage, slow push-ins, quiet lower thirds and a film grade.
- **Pillars:** build-story, product, service, longform-ai (on-location or screen-recorded).
- **Base:** `broadside`. Use only its **chrome**: the ink-black and cream lower-third plates, IBM Plex Mono
  uppercase labels, 1px hairlines, the flat plane. Replace fire-orange with green as the single accent.
- **Palette:** the footage is the palette. Chrome is ink `#111111@85%` and cream `#F0ECE5`, with muted text `#888880`.
  **Green** is the lower-third tab and drawn baseline, and the one annotation ring on the screen recording. There is no second accent.
- **Type:** Barlow 800 lowercase (embedded; fall back to Oswald) for names and claims, plus IBM Plex Mono 400 uppercase labels.
- **Layout:** footage is **full-bleed for ≥ 80 % of the runtime**. On 9:16, crop to the subject (`media-use` reframe), put the
  lower third at y 1000–1120 and keep it clear of the caption band. On 16:9, put the lower third at bottom-left inside x 96–860.
- **Motion:** `multi-phase-camera` (slow push-in plus micro-drift on every shot, scale 1.00 → 1.06),
  `depth-of-field-blur` (rack to the detail), `coordinate-target-zoom` (punch into a screen region).
  **Transitions:** blur crossfade, light leak, color dip (to black). Hard cuts on the beat are fine.
- **Texture:** `grain-overlay` 6–8 %, a soft vignette, a warm grade or LUT through `media-use`.
- **Caption skin:** `band-karaoke`.
- **Registry:** `lt-kicker-name`, `lt-mask-reveal`, `push-in`, `grain-overlay`, `organic-light-leak-overlay`.
- **Never:** footage in a device frame or a card; animated graphics competing with a moving shot; stock people.
- **Signature moment:** a slow push into the real screen while a single green ring draws around the number that changed.

## 6. terminal-crt
**Essence:** an old phosphor terminal. Amber glow, scanlines, a cursor that thinks, output that lands.
- **Pillars:** python, build, build-story, ai-term (agents and CLIs).
- **Base:** `broadside` (flat dark plane, mono chrome, one accent discipline). Replace the orange register with
  an amber phosphor screen, and set everything in mono.
- **Palette:** ground `#0B0D0A`, screen `#11140F`, phosphor amber `#FFB547` (body text, so it is the
  other "accent" hue), dim amber `#7A5A2A`. **Green** is the `$` prompt, the `✓ passed` line and the final answer line.
- **Type:** IBM Plex Mono 400/700 for everything. One League Gothic title card (the topic) is allowed.
- **Layout:** 9:16 runs the terminal **full-frame** (no window chrome) with 22 chars per line at 40px and the
  cursor kept near y 700. 16:9 shows a full-frame terminal with an oscilloscope or status column at the right edge.
- **Motion:** `discrete-text-sequence` (typos, backspaces, holds), `context-sensitive-cursor`,
  `camera-cursor-tracking`, `chromatic-glitch` (once, on the reveal). **Transitions:** glitch, VHS tape, shutter.
- **Texture:** scanlines plus barrel warp (`yt-screen-warp`) and a phosphor bloom on the text (≤ 0.45 glow).
- **Caption skin:** `glow-word` (dim amber words, green active word).
- **Registry:** `yt-screen-warp`, `terminal-simulator`, `code-terminal-run`, `oscilloscope-trace`.
- **Never:** a macOS window frame; cyan or purple neon; more than one glitch burst per scene.
- **Signature moment:** the command types, hesitates, backspaces a typo, runs, and the one green line prints.

## 7. isometric-3d
**Essence:** systems as toy blocks. An isometric world of extruded tiles that the camera flies over.
- **Pillars:** longform-sd, ai-term (pipelines, RAG, agents), product (how it works).
- **Base:** `creative-mode`. Keep the cream canvas, 4px ink borders and hard offset shadows (no blur). Swap its
  green `#1F8A4C` → `#00D890`, drop pink and yellow, and keep orange.
- **Palette:** canvas `#EFE9D9`, ink `#0F0F0F`, block faces top `#FFFFFF`, left `#E2DACB`, right `#CFC5B2`.
  Other accent: orange `#E85A1F` (the bottleneck or failing node). **Green** is the active node's top face and the packet.
- **Type:** Archivo Black 400 uppercase (labels standing on the tiles) + Space Mono 400 (port numbers, counts).
- **Layout:** the world is a `.world` wrapper at `rotateX(55deg) rotateZ(-45deg)`. 9:16 runs the stack vertically
  (3–4 levels); 16:9 runs it as a wide plain. Labels are billboarded (counter-rotated) and must not collide with the caption band.
  The registry has **no isometric block**, so build the tiles with CSS 3D (three faces per block).
- **Motion:** `3d-camera-flight` (dive, tilt to flatten), `depth-scatter-assemble` (blocks assemble),
  `spring-pop-entrance` (nodes pop up from the plane), `orbit-3d-entry`. **Transitions:** 3D card flip, zoom out, gravity drop.
- **Texture:** a dot grid on the ground plane; the hard offset shadow is the only depth cue.
- **Caption skin:** `boxed-word`.
- **Registry:** `ui-3d-reveal`, `camera-rig-depth-stack`, `perspective-marquee`, `transitions-3d`.
- **Never:** blurred shadows, gradients on faces, perspective that drifts off true isometric mid-shot.
- **Signature moment:** the camera tilts from flat diagram to isometric, and the whole system rises out of the page.

## 8. whiteboard
**Essence:** explained by hand. Marker strokes draw themselves on a clean board, and the camera pans along the board.
- **Pillars:** ai-term, python (concepts), longform-sd, service (explaining automation to a business owner).
- **Base:** `daisy-days`. Keep **only** its hand-drawn SVG ornament layer, charcoal outlines and dot bullets.
  Replace the pastel surfaces with whiteboard white, and swap Fredoka/Quicksand for a marker hand.
- **Palette:** board `#F7F6F1`, marker ink `#1E2329`, ghost erase `#1E2329@8%`. Other accent: blue marker
  `#2B59C3`. **Green** is the marker that circles or ticks the answer.
- **Type:** Kalam 700 or Patrick Hand (embedded; same hand throughout) + Space Mono 400 for code and numbers.
- **Layout:** one long board; each beat is a region and the camera pans to it. 9:16 runs the board vertically and
  pans down; 16:9 runs it horizontally and pans right. Content fills to y 1440 on 9:16 and the board continues below it.
- **Motion:** `svg-path-draw` (every stroke), `css-marker-patterns` (circle, scribble, highlight),
  `viewport-change` (pan between regions). **Transitions:** push slide (it *is* the pan), zoom out (show the whole board), crossfade.
- **Texture:** a faint ghost of earlier erased diagrams; `hw-boil` jitter on held drawings.
- **Caption skin:** `underline-bar`. Set `--font-display` to the hand, and the green bar reads as a marker swipe.
- **Registry:** `whiteboard-ink`, `hw-arrow`, `hw-pipeline`, `vox-annotate`, `hw-boil`.
- **Craft** *(adapted from lemo-opuscar's Whiteboard style, MIT)*:
  - **The board is a map.** Each idea gets its own region, and distance on the board is distance in
    the argument. Returning to an earlier region is a free callback. No cuts on the board; if a
    cut is unavoidable it is a whip pan.
  - **Real marker, not animated text:** ink at ~0.94 opacity with `mix-blend-mode: multiply`, so
    overlaps darken; a slight low-frequency wobble along each stroke; circles start at an angle and
    **overlap past closure**; boxes are four strokes with small corner overshoot.
  - **Every stroke eases slow-fast-slow** and is given a **deadline**, not a speed: a label takes
    0.3–0.8 s, a title about 3 s, and **a term finishes writing on the word** the voice says it.
  - **A glossy sheen:** one soft diagonal white band (10–16 %) drifting at ~0.35× the camera
    speed. That one detail sells "whiteboard" over "white page".
  - **Colour has a job for the whole video:** ink = things and structure, blue = signals and
    process, green = the one thing that matters. One green mark per region.
  - **No hands, no cursor.** If a pen shows at all it floats, with a soft shadow that grows as it lifts.
- **Moves to pick from:** writing a formula term by term as it's spoken; the pen draws the line the
  camera then rides to the next region; an eraser wipes a trail backwards to mean "undo"; two pens
  drawing two quantities at once for a comparison; a faint ghost of an earlier diagram turning out to matter.
- **Sound:** a felt-on-gloss hiss per stroke whose length follows the stroke, an occasional
  dry-erase squeak on a long stroke, a cap click when a section ends. Music is light: solo piano,
  brushed jazz trio, marimba and pizzicato. Foley sits about 11 dB under the voice.
- **Pitfalls:** labels half cut off by a push-in; full stops that vanish (draw sub-width marks as
  dots); erasing across a label you meant to keep; one pen with too many jobs drifting late
  (give overlapping drawings their own deadline).
- **Never:** typeset headlines, clean vector icons, drop shadows, more than 3 marker colours.
- **Signature moment:** the camera pulls out to show the whole board drawn, and green circles the one idea that ties it together.

## 9. split-screen
**Essence:** two halves argue. Old against new, naive against right, before against after, side by side.
- **Pillars:** python (old vs new syntax), service (before/after for a business), product, build.
- **Base:** `coral`. Keep the hard colour-region splits, zero radius, zero shadow and wallpaper numerals.
  Swap Bebas Neue → **League Gothic**, and Inter → **Source Code Pro**.
- **Palette:** left panel ink `#1A1A1A`, right panel cream `#F5F0E8`, gray `#6B6B6B`. Other accent: coral
  `#E85D5D` marks the wrong or old side. **Green** marks the right or new side and the winning number.
- **Type:** League Gothic 400 uppercase (side labels, numbers) + Source Code Pro 400/700 (code, body).
- **Layout:** 9:16 splits **top and bottom** (two halves of 960px) with labels at the inner edge. 16:9 splits left and right.
  Footage or captures fill **each half edge to edge**. The divider is a 4px ink bar that can wipe.
- **Motion:** `split-tilt-cards` (entrance), `reactive-displacement` (the winner pushes the loser),
  `control-target-sync` (the same input changes both sides together), `counting-dynamic-scale`.
  **Transitions:** diagonal split, squeeze, vertical push.
- **Texture:** coral's 45° hatch at 6 % on the losing half only.
- **Caption skin:** `band-karaoke` (the band sits across the seam).
- **Registry:** `comparison-split`, `before-after-wipe`, `grade-split-reveal`, `split-tilt-cards`.
- **Never:** three panels; symmetric neutrality (one side must win); a split that never resolves.
- **Signature moment:** both halves run the same input, and the green half finishes while the coral one is still loading.

## 10. collage-scrapbook
**Essence:** a maker's notebook. Real screenshots as taped prints, torn paper, stickers, hand notes.
- **Pillars:** build-story, product, service, ai-term (a tool roundup).
- **Base:** `capsule`. Keep the grain overlay, the 2px ink outline and the soft hard-offset shadows. Turn its pills into
  **torn paper scraps and taped prints**, and swap Bodoni Moda → **Archivo Black** cut-out letters.
- **Palette:** cream `#F5F5F0`, kraft `#D9C7A3`, ink `#1A1A1A`, shadow `#1A1A1A@8%`. Other accent: tape
  yellow `#F2D160@75%`. **Green** is the sticker dot or stamp on the winning screenshot and the "shipped" stamp.
- **Type:** Archivo Black 400 (ransom-cut headline words on scraps) + Space Mono 400 (scribbled labels);
  optionally one handwritten note in Kalam (embedded).
- **Layout:** each screenshot is a large print, **≥ 80 % of the frame width**, tilted ±3°, with tape at the corners.
  9:16 stacks one print per beat; 16:9 allows two overlapping prints and a note. Footage rule applies.
- **Motion:** `spring-pop-entrance` (prints slap down), `depth-scatter-assemble` (a pile assembles),
  `nudge-curve` (slide the pile to reveal the next), `css-marker-patterns`. **Transitions:** gravity drop, staggered blocks, page burn.
- **Texture:** paper grain, deckled edges (clip-path), and tape with 70 % opacity.
- **Caption skin:** `boxed-word` (ink type on a green "label-maker" box).
- **Registry:** `freeze-frame-dressing`, `hw-frame`, `texture-mask-text`, `grain-overlay`.
- **Never:** clip-art stickers, emoji confetti, fake screenshots, prints too small to read.
- **Signature moment:** the final print slaps down on the pile and a green "SHIPPED" stamp thunks onto it.

## 11. newsroom-dataviz
**Essence:** a data desk story. Parchment pages, a big serif headline, one chart that tells the whole story.
- **Pillars:** longform-ai (benchmarks, adoption), ai-term (cost, speed), service (ROI for small businesses), build-story (real metrics).
- **Base:** `biennale-yellow`. Keep the parchment ground, the single indigo ink, the 1px hairlines, the bottom-right
  page number and the "text is always ink" rule. Use the yellow sun bloom only as a chart underprint.
- **Palette:** paper `#E9E5DB`, paper-deep `#DCD6C4`, ink `#1B2566`. Other accent: sun `#F1EE2E` (highlight band
  behind the key period). **Green** is the series or bar that matters and the delta chip (`#00D890` fill; as text `#00784F`).
- **Type:** Instrument Serif 400 (embedded; headline, tracking −0.02em) + IBM Plex Mono 400/700 (axes, figures,
  `tabular-nums`).
- **Layout:** 9:16 has the headline at y 300–520, the chart in y 560–1120 (≤ 5 bars or 2 series) and the source line under it.
  16:9 puts the chart in cols 1–8 and a big number with its explanation in cols 9–12. Every number comes from the dossier, with its source shown.
- **Motion:** `stat-bars-and-fills`, `chart-scrub-readout`, `counting-dynamic-scale`, `vertical-spring-ticker`.
  **Transitions:** vertical push, shutter, crossfade.
- **Texture:** a faint newsprint grain and a hairline column grid; a slow ticker crawl in the bottom chrome (y 1600–1700, below the captions).
- **Caption skin:** `underline-bar`.
- **Registry:** `data-chart`, `news-ticker`, `mk-line-graph`, `bar-chart-race`, `number-wheel`.
- **Never:** invented figures; 3D charts; pie charts with more than 3 slices; dual axes.
- **Signature moment:** the scrub head stops on one point, the bar turns green and the delta counts up.

## 12. glass-diorama
**Essence:** layered glass in depth. Frosted panes float over a warm aurora, and the camera racks focus through them.
- **Pillars:** product (games, apps), ai-term, longform-ai.
- **Base:** `blue-professional`, for its discipline: tinted cards with no shadow, a single accent, pill chrome and the progress bar.
  Rebuild the cards as **frosted glass** on a dark ground, and swap Space Grotesk + Inter → **Montserrat + Source Code Pro**.
- **Palette:** ground `#0B0F14`, aurora blobs saffron `#F2A33A@25%` (the other accent) and green `#00D890@18%`,
  glass `#FFFFFF@8%` + 1px `#FFFFFF@18%` border + `backdrop-filter: blur(24px)`, text `#F2F4F7`, secondary `#A7B0BD`.
  **Green** is the focused pane's edge light and the one live stat.
- **Type:** Montserrat 900 (display, tracking −0.03em) and 400 (body) + Source Code Pro 400 (data chips).
- **Layout:** 3–4 planes at different depths. 9:16 stacks the panes vertically with the focused pane centred at y 500–1000.
  16:9 uses a diorama: a big pane on the left, satellites receding to the right. Real app captures sit **inside** the
  glass panes at full pane size.
- **Motion:** `depth-of-field-blur` (rack between panes), `ambient-glow-bloom`, `3d-camera-flight` (slow drift
  between planes), `card-morph-anchor`. **Transitions:** blur through, focus pull, zoom through.
- **Texture:** the aurora blobs drift with `sine-wave-loop`; an optional thin jali/rangoli line pattern at 5 % on the ground.
- **Caption skin:** `glow-word`.
- **Registry:** `liquid-glass-widgets`, `liquid-glass-notification`, `glass-shard-title`, `camera-rig-depth-stack`, `mk-background`.
- **Never:** purple-blue gradients, neon glow, gradient text, more than 4 panes, glass over glass over glass without a focus rack.
- **Signature moment:** focus racks from a blurred foreground pane to the real app screen behind it, and its edge lights up green.

## 13. paper-shadow-theatre
**Essence:** a backlit screen and cut-paper puppets. One warm lamp, flat silhouettes, gentle pace. From
x4b47x-034026 (`references/prompt-library.md` #9); it also echoes Andhra's *tholu bommalata* leather shadow puppets.
- **Pillars:** service (what an owner fears, why automation feels risky), ai-term (a story-shaped concept),
  longform-ai (one quiet chapter), build-story (the origin of a product).
- **Base:** `editorial-forest`, for its flat paper depth (no shadows), 2px hairlines and the cream/ink pairing.
  **Drop its topbar, footline and monogram** (no corner chrome). Turn the cream into the lit screen and the
  ink into silhouettes. Swap Source Serif 4 → **Fraunces** (embed) and keep JetBrains Mono for code only.
- **Palette:** house dark `#14100C` (outside the screen), lit screen `#EBD3A3` with one soft radial hot-spot
  `#F6E4BE@20%` (the lamp), silhouette `#1A140E`, screen edge falloff `#B8925A`. Other accent: lamp amber
  `#F2A33A` (the flame, the one warm gel). **Green** is a single translucent *coloured gel* cut-out
  (`#00D890@65%`, like the dyed leather in tholu bommalata) on the object that is the answer.
- **Type:** Fraunces 300 / 700 (embedded; soft optical size, sentence case) set *as cut paper*: words are
  silhouettes on the screen, or ink on the house dark. Space Mono 400 for any code, which lives on a paper slip.
- **Layout:** the screen is a rounded-rect stage, ~88 % of the frame. 9:16: stage y 160–1600, a horizon/ground
  strip at y 1300–1600 that puppets stand on, the lamp's hot-spot at upper-left. 16:9: stage inset 96px, puppets on a
  shared ground line at 78 % height. **Depth = distance from the screen**: near puppets are crisp, far ones are
  larger and soft (`depth-of-field-blur`).
- **Motion:** `sine-wave-loop` (puppets sway on their rods, ≤ 2°; the lamp flickers ≤ 3 % luminance),
  `nudge-curve` (set pieces slide in on rails, slow-fast-slow), `depth-of-field-blur` (a puppet moves toward the
  lamp and grows soft), `multi-phase-camera` (one slow push per scene, ≤ 1.04). Puppets step on held poses
  (stop-motion cadence ~12 fps), never smooth-tweened limbs. **Transitions:** mostly object-driven (a silhouette
  becomes the next set piece; a hand covers the lamp). Catalog: circle iris (the lamp closing), color dip
  (to house dark), vertical blinds (as a curtain, once).
- **Texture:** paper fibre grain 5 %, slightly ragged cut edges (clip-path with a few jitter points), visible rods
  on the puppets.
- **Caption skin:** `band-karaoke`. The band is the stage apron, in silhouette ink at 85 %.
- **Registry:** `stop-motion-cadence` (stepped puppet time), `light-sweep-pass` (the lamp moving across the screen),
  `grain-overlay`.
- **Never:** smooth vector characters, gradients on silhouettes, glow, more than one lamp, puppets with faces
  that lip-sync, more than 3 puppets on the screen at once.
- **Signature moment:** a hand silhouette covers the lamp, the screen dips dark, and when the light returns the
  green gel piece sits where the problem was.

## 14. marker-on-paper
**Essence:** a designer's notebook that moves fast. Paper-light canvas, huge kinetic type, marker notes that
draw themselves, real physics, hard light↔dark switches. From ik-builds-585923 (`prompt-library.md` #2).
- **Pillars:** ai-term (fast definitions), python (what's new), product (launch beats), service (the hook), build.
- **Base:** `cartesian`, for its warm paper ground, 1px hairline as the only structure and zero shadow / zero fill.
  Swap Playfair Display → **Anton** (embed) for kinetic type and Inter → **Caveat** (embed) for the notes and
  JetBrains Mono for code. Drop the compass rings.
- **Palette:** paper `#F3EFE6`, ink `#161513`, hairline `#161513@14%`; dark switch = charcoal `#1D1C19` with paper
  text. Other accent: marker red-orange `#FF5A36` (the wrong answer, the crossed-out word). **Green** is the marker
  that writes or circles the answer and the one filled block (`#00D890` fills and strokes; as text on paper
  `#00784F`, on charcoal `#00D890`).
- **Type:** Anton 400 (embedded; uppercase, tracking −0.02em, 160–280px on 9:16) + Caveat 700 (embedded; notes,
  44–64px) + JetBrains Mono 400 for code. **Caveat and Anton are Google fonts, not bundled: embed both as woff2 via
  `@font-face`.** Caveat notes "write on" through `stroke-dashoffset`, so convert the note strings to SVG
  outlines at build time (or use SVG `<text>` with a stroke, then fill in after the stroke lands).
- **Layout:** 9:16: one huge word block y 300–800, the marker note annotating it from the side (x 600–1000),
  the physical object (ball, card, token) in y 900–1440. 16:9: type cols 1–7, note and object cols 8–12. A new
  visual idea every 1.5–2 s, while narration keeps its paced sentences.
- **Motion:** `kinetic-beat-slam` (type lands on phrase cues), `svg-path-draw` (Caveat notes and arrows),
  `css-marker-patterns` (circle, underline, scribble-out), `reactive-displacement` (an object knocks a word
  aside: real collisions), `motion-blur-streak` (smear on the fastest throw). Squash/stretch on landings ≤ 8 %,
  overshoot ≤ 2 %. **Transitions:** a hard cut on the hit that **inverts paper ↔ charcoal**; catalog: shutter,
  gravity drop, morph circle; registry `hw-scribble-transition` once per video. No generic push or slide.
- **Texture:** paper grain 3 %, the faint ghost of an erased note; no other texture.
- **Caption skin:** `boxed-word` (League Gothic in a green box sits with Anton on both grounds).
- **Registry:** `hw-path-text` (handwriting along a path), `hw-scribble-transition`, `marker-highlight`.
- **Never:** corner chrome, animator jargon on screen, invented %/multipliers, more than 4 words of Anton at once,
  two marker notes drawing at the same time.
- **Signature moment:** the screen snaps from paper to charcoal on a hit, a ball drops through the giant word,
  and a green Caveat note writes the answer beside the dent it left.

## 15. mascot-led
**Essence:** one simple character carries the concept. It reacts, gets confused, gets it, and calls back at the
end. From astrothewizard-618782 and doubleunplussed-181894 (`prompt-library.md` #1, #12).
- **Pillars:** ai-term (a token, an embedding, a prompt as the character), python (a variable, a generator),
  longform-sd (a request travelling the system), service (an invoice or chat message on its way).
- **Base:** `blockframe`, for its 4px black outlines, hard 8px offset shadows (no blur), square corners and
  label pills. Drop the five-pastel spread to cream plus **one** pastel field, and drop the star bursts. Swap Inter →
  **Bricolage Grotesque** (embed) and Space Grotesk → **Space Mono**.
- **Palette:** cream `#FFFDF5`, white `#FFFFFF` (mascot body), ink `#111111` (outlines, text), one scene field
  butter `#F7CB46` (the other accent: the mascot's world, never its body). **Green** is the thing the mascot is
  after or becomes (the answer object, the "got it" state of its eyes, the end-mark tag), ≤ 10 % of the frame.
  Green text on cream is `#00784F`.
- **Type:** Bricolage Grotesque 800 (embedded; labels, onomatopoeia at 120–200px, tilted ±6°) and 400 (rare body)
  + Space Mono 400 (numbers, code).
- **The mascot:** **the concept itself** (a token tile, a photon, a packet), never a robot, brain or
  assistant. ≤ 6 shapes, two dot eyes, eyebrows optional, no mouth or a static one. Personality comes from
  **expressions and poses only**: design 4–6 held poses (curious, startled, squashed, proud, tired) and cut
  between them on phrase cues. **No fake lip-sync**, no mouth flapping to the VO. Check limbs and hands in every
  snapshot.
- **Layout:** the mascot is the focal element, 25–40 % of the frame height. 9:16: mascot in y 600–1100, the
  world/diagram it moves through in y 300–700, onomatopoeia beside the impact point. 16:9: mascot travels
  left → right through a horizontal world; the context lane (a timeline of what else was happening) runs across
  the top.
- **Motion:** `spring-pop-entrance` (pose changes pop, overshoot ≤ 2 %), `press-release-spring` (squash on
  landings and bumps), `sine-wave-loop` (idle breathing, ≤ 1.5 % scale), `coordinate-target-zoom` (punch in on
  the face for the "oh!" beat). Simulate the world the mascot moves through (a real random walk, a real queue).
  **Transitions:** zoom through (into the mascot's eye or pocket), morph circle (the mascot curls into the next
  object), gravity drop (it falls into the next scene).
- **Texture:** none; the hard offset shadow is the only depth cue. A dot grid on the field at 6 % is allowed.
- **Caption skin:** `underline-bar` (set `--font-display` to Bricolage; the green bar reads as a sticker strip).
- **Registry:** `lottie-character-walk` (planted-feet walk cycles, read its README for the rig), `hw-text-cloud`
  (the mascot's thought bubble).
- **Never:** lip-sync, a robot or brain mascot, more than one character with a face, emoji, bouncy/elastic
  easing, a mascot that talks over captions, a callback that was never set up.
- **Signature moment:** the opening gag repeats in the last beat, but this time the mascot knows the answer:
  same pose, green eyes, one onomatopoeia.

---

## 16. pixel-era  · engine: animate
**Essence:** the idea told as a little video game. True low-res pixel art (no blur, no gradients), and
**resolution tells time**: an early era is chunky, a later one sharper.
- **Pillars:** build (games, Python games), any game-design topic, "history of X", build-story,
  ai-term when the metaphor is a game (agents, rewards, levels).
- **Engine:** `vendor/animate/styles/pixel/` (`STYLE.md`, `kit.js`, `sample.png`). Start a piece from
  `styles/pixel/demo/`, render with `scripts/animate_clip.sh`, lay it in full-bleed.
- **Palette:** the kit's `PAL16` (16 colours) or `HANDHELD` (4 greens); one palette per era. Our accent:
  `#00D890` as the one "power-up" / active element (coin, cursor, selected tile), never the ground.
- **Type:** in-scene text uses the kit's 5x7 bitmap font (`pixText`), ≤ 3 words, never in y 1400–1620.
  Captions stay ours (Plus Jakarta Sans via the caption skin) — the contrast is the point.
- **Layout:** the scene fills 1080x1920; the ground/platform line sits around y 1250–1350 so the
  world (bricks, water, grass) runs to the bottom edge under the captions (B18).
- **Motion:** on 2s (12 fps feel) for sprites; scrolls and parallax; the era morph (shrink window →
  shape morph → grow window, `kit/morph.js`) for "then → now" turns. HUD counters (SCORE, LV) carry
  the numbers.
- **Caption skin:** `boxed-word` (a solid box reads over busy pixels).
- **Never:** smoothing or bilinear scaling, gradients, more than one palette per era, fake CRT
  curvature on a handheld era.
- **Signature moment:** the world re-renders at a higher resolution as the idea "levels up".

## 17. riso-poster  · engine: animate
**Essence:** a three-ink risograph print that moves: halftone dots, overprints, plates slightly off register.
- **Pillars:** product, service (bold claims, before/after), ai-term with a single strong image.
- **Engine:** `vendor/animate/styles/riso/` (start from its `demo/`).
- **Palette:** paper `#f2ece3`; inks teal `rgb(54,137,171)`, fluorescent pink `rgb(220,68,160)`,
  yellow `rgb(238,222,30)`; mixes by overprint only. **No black, no white ink.** Our green appears as
  teal + yellow overprint on the one accent element.
- **Type:** big condensed display set in the print (Archivo Black / League Gothic), ≤ 4 words.
- **Motion:** on 2s; plates slide into register on the reveal; misregistration shimmer as texture.
- **Caption skin:** `underline-bar` with ink `#2a2a35` on the paper.
- **Never:** pure black, smooth gradients, more than three inks.
- **Signature moment:** the three plates slide in separately and lock into register on the key claim.

## 18. ink-machine  · engine: animate
**Essence:** boiling crosshatch ink. Warm cream paper outside, a navy "inside the computer" world
inside, reached through an iris.
- **Pillars:** ai-term (what happens inside the model), longform-ai beats, python concepts with a
  physical metaphor.
- **Engine:** `vendor/animate/styles/crosshatch/` (sketchbook is its lighter cousin:
  `styles/sketchbook/`).
- **Palette:** day ink `#3a2417` on paper `#f4ecd9`; night navy `#0c0d1c` with periwinkle `#c8d0f0`
  lines; hero terracotta `#d97757`. Our `#00D890` replaces the kit's glow green as the one live signal.
- **Type:** hand-lettered labels written on (`frac`), ≤ 3 words.
- **Motion:** lines boil every 2 frames even in holds; write-ons; iris in/out between worlds.
- **Caption skin:** `glow-word` in the navy world, `underline-bar` on paper.
- **Never:** flat fills (every shape gets hatch, cross, pencil or stipple), vector-clean lines.
- **Signature moment:** the iris opens from the paper desk into the glowing machine.

## 19. math-board  · engine: animate
**Essence:** a manim-style board: coloured math on a near-black stage, written on, transformed.
- **Pillars:** python (algorithms, complexity, numbers), ai-term with real maths (temperature,
  softmax, embeddings, gradient), longform-sd capacity maths.
- **Engine:** `vendor/animate/styles/math/` (smooth, on 1s; no texture).
- **Palette:** stage `#0E0E10`; one colour per quantity, kept everywhere (formula, figure, caption):
  red `#FC6255`, yellow `#F7D96F`, blue `#58C4DD`, and **our `#00D890` for the result**.
- **Type:** the kit's serif math; ≤ 1 formula on screen at a time.
- **Motion:** Write, ShowCreation sweeps, Transform between equations, a tracking dot with a live readout.
- **Caption skin:** `glow-word`.
- **Never:** maths that isn't true (A19 applies to every formula), more than 4 quantity colours.
- **Signature moment:** one equation transforms into the picture it describes.

## 20. iso-hairline  · engine: animate
**Essence:** calm, precise product illustration. Objects in 2:1 isometric on white, drawn only with
constant grey hairlines, faces filled white, one tiny dark accent per frame. It is **not**
`isometric-3d`, which uses chunky CSS toy blocks with hard shadows on cream. This one is quiet,
technical and Apple-manual-like.
- **Pillars:** product (how an app or device works inside), longform-sd (servers, queues and caches
  as stacked slabs), service (a calm "how we build it" explainer).
- **Engine:** `vendor/animate/styles/isometric/` (start from its `demo/`).
- **Palette:** ground `#ffffff`, edges `#a4a4ac`, inner lines `#e0e0e4`, accent `#232327`. Our
  `#00D890` replaces the dark accent on the one live element (the active port, packet or key).
- **Type:** small sans labels on leader lines (Space Mono / IBM Plex Mono), ≤ 3 words.
- **9:16 layout (B18 — the vendored demo FAILS it, 0/8: the object floats mid-frame over empty
  white):** compose **tall**. Stack the slabs into a tower, or zoom in so the object spans
  y 440–1440. Then run an isometric floor plate filled `#e4e4e8` (a light grid of `#d6d6dc`
  hairlines) from under the object **to the bottom edge**, so the scene continues beneath the
  captions. Check with `scripts/fill_check.py` on the exported clip before laying it in.
- **Motion:** on 1s with spring settles. Layers lift apart (exploded view), grids of parts light up
  in order, and everything else stays still.
- **Caption skin:** `underline-bar` with ink `#232327` (a white ground needs dark captions).
- **Never:** thick strokes, colour fills, drop shadows, more than one accent at a time.
- **Signature moment:** the exploded view, where the slabs lift apart to show the layer that matters.

## 21. cut-paper  · engine: animate
**Essence:** a warm collage world. Torn-edge paper shapes with soft shadows, crayon and pattern
fills (stripes, dots, gingham), and simple characters with faces. Playful and busy with small life.
It differs from `collage-scrapbook` (real photos and footage taped on kraft) and
`paper-shadow-theatre` (backlit silhouettes). Here everything is drawn paper, in full colour.
- **Pillars:** ai-term told as a story with a character, mascot-style explainers, build-story,
  service stories for shop owners (a little shop, customers, a phone), festival or seasonal posts.
- **Engine:** `vendor/animate/styles/cut-paper/` (and `examples/history-of-ai/`, a 60 s cut-paper
  chronology with 13 morphs).
- **Palette:** paper `#fbf6ea`, ink `#2a1d18`, navy `#26315f`, mustard `#d9a441`, teal `#3f9f9a`,
  pink `#f3a3bf`. The kit's hero orange `#ec7a4f` becomes **our `#00D890`** as the one hero element.
- **Type:** hand lettering written on (`handText` with `frac`), ≤ 4 words.
- **Motion:** on 2s. Pops for arrivals, the hero idles (bob, blink), and torn-hole morphs join scenes.
- **Caption skin:** `boxed-word` (solid boxes read over patterns).
- **Never:** vector-clean edges, flat fills without grain, the hero colour used as decoration.
- **Signature moment:** a torn-paper hole opens and the next world morphs through it.

## 22. sketchbook  · engine: animate
**Essence:** graphite and one accent on a warm sketchbook page. Ideas get pencilled, then inked,
then coloured with a quick scribble, and the camera moves across the page instead of cutting.
This is the hand-drawn "thinking it through" look; `whiteboard` and `marker-on-paper` are bolder
and flatter.
- **Pillars:** python concepts worked out step by step, ai-term "how would you design this",
  longform-sd sketches, build (planning a feature).
- **Engine:** `vendor/animate/styles/sketchbook/` (start from its `demo/`).
- **Palette:** paper `#f2ead8`, ink `#2a2420`, graphite `#6f6a63`, highlighter `#f7d64a` (the one
  word to read). The kit's terracotta hero `#d97757` becomes **our `#00D890`**.
- **Type:** hand lettering on the page narrates (≤ 4 words); captions stay ours.
- **Motion:** lines boil on 2s. Pencil → ink → colour scribble, plus camera pans across the page.
- **Caption skin:** `underline-bar`.
- **Never:** cuts away from the page, clean vector lines, more than one accent.
- **Signature moment:** a rough pencil sketch is inked over and "snaps" into the decided answer.

## Quick map

| family | ground | base preset | caption skin | key registry |
|---|---|---|---|---|
| navy-code | dark navy | none (`assets/looks/navy-code.md`) | glow-word | code-snippet-dark-modern, code-highlight |
| editorial-paper | cream | code-editorial | underline-bar | code-scroll, ink-bleed-reveal |
| blueprint | deep blue | cobalt-grid (inverted) | band-karaoke | dynamic-grid, svg-line-draw-loader |
| bold-poster | off-white | bold-poster | boxed-word | caption-kinetic-slam, kinetic-type-swap |
| documentary | footage | broadside (chrome only) | band-karaoke | lt-kicker-name, push-in |
| terminal-crt | phosphor black | broadside | glow-word | yt-screen-warp, terminal-simulator |
| isometric-3d | cream | creative-mode | boxed-word | ui-3d-reveal, camera-rig-depth-stack |
| whiteboard | board white | daisy-days (ornaments only) | underline-bar | whiteboard-ink, hw-arrow |
| split-screen | ink / cream | coral | band-karaoke | comparison-split, before-after-wipe |
| collage-scrapbook | cream / kraft | capsule | boxed-word | freeze-frame-dressing, hw-frame |
| newsroom-dataviz | parchment | biennale-yellow | underline-bar | data-chart, news-ticker |
| glass-diorama | graphite + aurora | blue-professional | glow-word | liquid-glass-widgets, glass-shard-title |
| paper-shadow-theatre | lit warm screen / house dark | editorial-forest (atoms only) | band-karaoke | stop-motion-cadence, light-sweep-pass |
| marker-on-paper | paper ↔ charcoal | cartesian | boxed-word | hw-path-text, hw-scribble-transition |
| mascot-led | cream + one pastel field | blockframe | underline-bar | lottie-character-walk, hw-text-cloud |
| pixel-era · animate | era palette (PAL16 / HANDHELD) | `vendor/animate/styles/pixel` | boxed-word | — (animate kit) |
| riso-poster · animate | riso paper | `vendor/animate/styles/riso` | underline-bar | — (animate kit) |
| ink-machine · animate | cream paper ↔ navy | `vendor/animate/styles/crosshatch` | glow-word / underline-bar | — (animate kit) |
| math-board · animate | near-black | `vendor/animate/styles/math` | glow-word | — (animate kit) |
| iso-hairline · animate | white | `vendor/animate/styles/isometric` | underline-bar | — (animate kit) |
| cut-paper · animate | warm paper, full colour | `vendor/animate/styles/cut-paper` | boxed-word | — (animate kit) |
| sketchbook · animate | sketchbook page | `vendor/animate/styles/sketchbook` | underline-bar | — (animate kit) |

Pillar lookup (animate families 16–22: **game design / retro / history-of** → pixel-era · **product, service** → riso-poster · **ai-term, longform-ai** → ink-machine · **python, maths** → math-board · **product internals, system design** → iso-hairline · **stories with a character, shop owners** → cut-paper · **working an idea out** → sketchbook): **ai-term** → bold-poster, whiteboard, isometric-3d, glass-diorama, editorial-paper,
marker-on-paper, mascot-led, paper-shadow-theatre · **python** → terminal-crt, split-screen, editorial-paper,
navy-code, bold-poster, marker-on-paper, mascot-led · **build** → terminal-crt, blueprint, split-screen, navy-code,
marker-on-paper · **product** → documentary, glass-diorama, collage-scrapbook, split-screen, marker-on-paper ·
**service** → documentary, split-screen, newsroom-dataviz, bold-poster, whiteboard, paper-shadow-theatre,
marker-on-paper, mascot-led · **longform-ai** → editorial-paper, newsroom-dataviz, glass-diorama, documentary,
paper-shadow-theatre · **longform-sd** → blueprint, isometric-3d, whiteboard, navy-code, mascot-led ·
**build-story** → documentary, collage-scrapbook, terminal-crt, newsroom-dataviz, paper-shadow-theatre.

Item names were checked against `npx hyperframes catalog --query …` (registry of 392 items) on 9 Oct 2026;
the items for families 13–15 were checked the same way on 10 Oct 2026. Ideas behind 13–15 and the rules they
carry are in `references/prompt-library.md`.
Install with `npx hyperframes add <name>` and read its README before wiring it in.
