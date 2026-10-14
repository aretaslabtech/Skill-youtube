# Visual design — moodboard, colour, type, layout, motion

`assets/brand-core.md` holds what never changes, and `references/looks.md` holds the look families (one per video). `assets/looks/navy-code.md` is the original look. This file is *how* to
use them so a frame reads as designed rather than generated. Numbers here are checkable
in a snapshot.

## 1. Moodboard in words (write it into PLAN.md before any HTML)

A moodboard sets tone before style frames, and style frames before animation (standard
motion-design order: direction → references → style frames → motion). We can't paste images
into a cron run, so we write the board as six fixed lines:

```
Feeling:   3 adjectives + 1 anti-adjective   e.g. "precise, calm, quietly witty — not hype"
Palette:   ground / text / accent / semantic, with the % of frame each may occupy
Type:      display face+weight+size, body, mono; case rules
Texture:   grain %, any pattern (dot grid, blueprint lines), or "none"
Motion:    easing family, typical durations, what moves vs what stays still
References: 2–3 named, specific things and what to take from each
           e.g. "ByteByteGo flow arrows (static boxes, moving packets)",
                "a railway timetable board (mono numbers flipping)",
                "hand-painted shop signage (service days: flat, bold, two colours)"
```

Rules: references must be specific objects or works, never "modern, clean, sleek, futuristic".
One reference per video should come from outside tech (signage, print, transit, packaging) —
it is what makes the frame ours. Each pillar keeps the same Feeling/Palette/Type for the
series; only Texture/References vary per episode.

## 2. Colour for video

**Proportions per frame** (navy-code tokens shown; other looks map the same roles):

| Role | Token | Share of frame |
|---|---|---|
| Ground | `canvas #0A1B29` (service: `light-ground #F4F7FB`) | 60–75 % |
| Structure | `canvas-raised`, `canvas-elev`, hairlines | 15–30 % |
| Text | `text #EAF1F7`, `mist #9DB3C6` | as needed |
| Accent | `voltage #00D890` | **≤ 10 %, one element** |
| Semantic | `wrong #FF7A66`, `caution #FFC566` | only where they mean wrong/watch |

- **One accent, one meaning.** Voltage = the answer, the insight, the CTA. If two things are
  green, neither is the focus (Gate B4).
- **Colour = identity.** A variable, a product or a concept keeps its colour across every
  scene (3Blue1Brown's habit). Write the colour map in PLAN.md.
- **Contrast**: body text ≥ 4.5:1, large text (≥ 48 px bold) ≥ 3:1 (WCAG 2). `text` on `canvas` ≈ 15:1,
  `mist` on `canvas` ≈ 8:1 — fine. Saturated blues and reds on dark grounds *look* lower-contrast
  than their ratio (NN/g); never put body text in `error` or a pure blue.
- **Never #000 / #fff.** Pure black crushes in H.264 and looks like a dead frame; pure white
  halates on phones in dark rooms. Use `canvas` / `text`.
- **Dark vs light ground.** Dark is default: tech-site reader polls put "dark mode always on"
  around 73–82 % (self-selected, but our audience is that audience), and code reads better on
  it. Light ground for the service pillar (business owners, matches cybiqon.in) — then use
  `voltage-deep #00784F` for accent text; bright voltage fails on light.
- **Light text looks bolder on dark**: drop body weight one step on dark (500 → 400), and don't
  use weights < 400 for anything below 48 px.

**Banding (H.264 is 8-bit).** A smooth gradient spanning few code values becomes visible
stair-steps, and the encoder's quantisation makes it worse; YouTube's re-encode won't fix it.
- No full-frame linear gradients on dark. Flat `canvas` + at most **one soft radial ≤ 20 % opacity**.
- If a gradient is unavoidable, add **2–4 % monochrome grain** across the frame *in the
  composition* and export at ≥ 12 Mbps; check the darkest 10 % of the frame in the snapshot at
  200 % zoom.
- Glows: one, small, on the focal element; large soft glows band.

## 3. Typography for vertical video

Two families per video, chosen by the look (`references/looks.md`); the vendored pair is **Plus
Jakarta Sans** (display/UI) and **JetBrains Mono** (code, kickers, numbers-as-data). Hierarchy
comes from weight (800 vs 400) and size, not from a third font.

| Role (9:16, 1080 wide) | Size | Weight | Line length | Lines |
|---|---|---|---|---|
| Cover / hook headline | 112–128 px | 800, tracking −0.03em | ≤ 14 chars/line | ≤ 3 |
| Display | 96 px | 800 | ≤ 16 chars | ≤ 3 |
| Headline | 72 px | 700 | ≤ 22 chars | ≤ 3 |
| Lead / label | 44 px | 500 | ≤ 32 chars | ≤ 2 |
| Body (rare) | 36 px | 400 | ≤ 38 chars | ≤ 3 |
| Code | 34 px mono | 400 | ≤ 22 chars | ≤ 9 |
| Captions | 54–70 px | 800 | ≤ 3 words | 1–2 |
| Kicker / series tag | 30 px mono, caps, +0.14em | 500 | ≤ 24 chars | 1 |

- Floor: nothing essential below **32 px** on 9:16 (it's ~1.7 % of frame height; phones show
  ~1/3 scale). Caption guides converge on 55–70 px; ours is 54 px/800 because it's bold.
- 16:9: display 88–110 px, headline 64 px, body 36 px, code 30 px (≤ 60 chars, ≤ 16 lines).
- Sentence case everywhere except the kicker. No all-caps sentences. No centred paragraphs.
- Numbers that change (counters, timers) use `font-variant-numeric: tabular-nums` so they
  don't jitter.
- Text appears on a word or line boundary with the VO; it never fades in letter-by-letter
  unless it is a one-line code type-on.

## 4. Layout grids and safe zones

**9:16 (1080×1920)** — see `platform-specs.md` for where the numbers come from.

```
y    0 ─────────────── platform top UI: ground / texture / footage only
y  200 ─── hook band: hook, kicker, chapter title (x 64–1016)
y  440 ─── main visual starts (full width x 64–1016)
        │  the visual uses the WHOLE height: diagram, code, phone frame, footage
y 1150 ─── below here keep meaning in x 64–850 (the right action rail)
        │  labels, result line, the lower half of the stage
y 1440 ─── caption band y 1440–1600 (captions only, x 64–850, no full-width box)
y 1600–1920  bottom: the stage/footage/ground CONTINUES here (bleeds off-frame); no text
            (an empty bottom 40 % looks unfinished — rubric B18)
```

- Columns: 6 columns inside x 64–1016 (24 px gutters) for organic; anything carrying meaning
  stays left of x 850 below y 1150, because the like/comment/share rail sits there from mid-height down.
- Anchor to a left edge (x 64 or x 96) or a 2-column split; centre only single short lines.
- One focal element per frame, occupying 30–55 % of the core zone.

**16:9 (1920×1080)**: 96 px padding all round (title-safe ≈ 90 %), 12-column grid with 24 px
gutters; code on columns 1–7, state/diagram on 8–12. Keep the bottom-right 400×160 px clear
in the final 20 s (end screen elements).

## 5. Motion that explains vs motion that decorates

Test for every animated property: *if this didn't move, would the viewer understand less?*
If no, it doesn't move.

| Explains (keep) | Decorates (cut) |
|---|---|
| A pointer moving to the element being read | Background shapes drifting/parallax |
| A value morphing from old to new | Every element "fading up" on entry |
| An arrow drawing in the order data flows | Continuous looping glows/pulses on idle elements |
| A camera push to the line under discussion | Camera floating with no target |
| Layout change that shows grouping (items sliding into a set) | Random rotation/scale "energy" |

Timing (Material motion, adapted for video where the viewer can't pause):
- Easing: entering `cubic-bezier(0, 0, 0.2, 1)`; exiting `cubic-bezier(0.4, 0, 1, 1)`; moving
  on-screen `cubic-bezier(0.4, 0, 0.2, 1)`. Never linear, except counters and flows.
- Durations: small UI-scale moves 250–400 ms; elements crossing > 1/3 of the frame 450–700 ms;
  camera pushes 600–900 ms. Material warns > 400 ms feels slow in UI; video gets slightly more
  because the change *is* the content — but hold the result ≥ 0.6 s.
- Stagger groups at 40–80 ms per item, max 6 items; beyond that reveal as one block.
- ≤ 2 things animating at once (ByteByteGo: 1–4 % of canvas changes per loop).

## 6. Series identity

- Same kicker tag per pillar, top-left in band A (`AI, EXPLAINED`, `PYTHON 3.13`, `BUILD IT`,
  `SYSTEM DESIGN`, `BUILT BY US`, `BUILD LOG`, `FOR BUSINESSES`).
- Within one video: the same ground, the same two fonts, the same caption style and the same
  voice; the end mark follows `brand-core.md` (logo ≤ 120 px, ≤ 2 s). Across videos the look
  changes; only the brand core stays.
- A signature move per pillar, used once per video (the look's `signature moment` in references/looks.md), e.g. longform-sd:
  one moving flow on a fixed boxes-and-arrows structure.
- No logo on frame 0. The kicker is the brand in the first second.

## 7. Thumbnail and cover frame

- **Frame 0 is the cover** (Gate B6) and the Reels cover: headline ≤ 6 words at ≥ 112 px +
  the subject, inside y 300–1250 so it survives the Instagram 3:4 grid crop (removes 240 px
  top and bottom) and the platform UI.
- One idea, one focal object, ≥ 40 % of the frame; readable at 160 px wide (test by
  downscaling the snapshot).
- The cover shows the *question or result*, never the answer to the hook's gap.
- Long-form thumbnails: 1280×720 min (YouTube recommends up to 3840×2160, ≤ 2 MB from mobile);
  3–5 words max, face or object on one third, text on the other; YouTube Test & Compare picks
  by watch-time share, so the thumbnail must match the video.

## 8. Anti-slop checklist (Gate B5 detail)

Fail if any is true:
- [ ] Purple-to-blue or cyan-magenta gradients; gradient-filled text; neon text glow.
- [ ] Glassmorphism on more than one panel; glow on every card; heavy drop shadows on flat UI.
- [ ] Inter/Roboto/Poppins/Montserrat display; three or more fonts; uniform weights.
- [ ] Centred everything; three identical cards in a row; 2×2 icon grids.
- [ ] Emoji as icons or decoration; mixed icon styles.
- [ ] Stock people, generated faces, generated "hands on keyboard", glowing brains, robots,
      circuit-board backgrounds, floating particles, lens flares.
- [ ] AI-video tells: floaty camera with no target, too-smooth motion, morphing backgrounds,
      gibberish in-scene text, every shot lit/coloured the same, oversaturated colour.
- [ ] Voice tells: TTS plateau (every sentence same contour), no breaths, no pauses — fix
      with punctuation and pause marks in the script.
- [ ] Copy tells: "unlock", "leverage", "supercharge", "game-changer", round invented stats,
      "In today's fast-paced world".
- [ ] Default chart colours; fake UI; invented metrics; a fake code editor that couldn't run.
- [ ] A frame where nothing is changing for > 2 s on a Short, other than the deliberate payoff hold.

## 9. Lessons from awesome-opus5-5-videos (10 Oct 2026)

The bar: nobody can tell the video was AI-generated. These rules come from the strongest prompts in
[yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos); excerpts and
attributions are in `references/prompt-library.md`. Each rule is checkable in PLAN.md or a snapshot.

**(a) Simulate, don't depict** (astrothewizard-618782). If the concept is a process (a random walk,
temperature sampling, a hash, a queue, attention weights), the composition **computes** it from a seeded
PRNG or real data and draws the result: sampled bars come from a real softmax, a queue drains at the stated
rate. A hand-placed drawing of the process fails. Real numbers come from `research/sources.md` and uncertain
ones are shown as ranges. *Check:* PLAN §5 names the one thing that is simulated and the code that does it.

**(b) Object-driven transitions** (daniel-haida-636937, howdevelop-733090). The next scene grows out of an
object in the current one, and the transition itself demonstrates the idea. daniel-haida's lists, verbatim:
- Good: "chart line → document edge", "gold pill → invoice button", "financial number → amount in invoice",
  "card edge → next surface", "camera push through interface element", "shared geometry", "mask reveal using
  actual product shapes".
- Bad: "crossfade", "random wipe", "spin transition", "glitch", "whip-pan every two seconds", "generic SaaS
  slide-left", "zoom-blur spam".
Crossfades and generic catalog wipes may not be the **main** grammar. *Check:* ≥ 60 % of scene changes in the
storyboard name the carrying object ("the token tile becomes the next row"); a catalog transition is
allowed for ≤ 1 in 3 cuts.

**(c) Scene shapes worth reusing.**
- **Continuous scale zoom** with an on-screen **scale ruler** (a tick bar that relabels 1 m → 1 km → 1 AU as the
  camera moves) so the viewer always knows where they are (astrothewizard-618782 cites the infinite-zoom genre).
- **Take-apart / exploded view**: the object separates along one axis into labelled parts, then reassembles
  (daniel-haida-636937: "the UI compresses or folds into one beautiful … product object").
- **Context alongside the timeline**: a second lane shows what else was happening during the same span
  (astrothewizard-618782: "what was happening on Earth during those 100,000 years").
- **Words as architecture**: the key word *becomes* the structure (gdgtify-929495).

**(d) Works muted** (howdevelop-733090, astrothewizard-618782). The story reads from visuals + captions alone.
*Check:* give a fresh sub-agent the contact sheet and the caption text only; it must retell the takeaway.

**(e) Visual rhythm** (ik-builds-585923, gdgtify-929495). A **new visual idea every 1.5–2 s** (a draw-on, a
state change, a camera move) while narration keeps its paced sentences: the eye gets fed, the ear doesn't get
rushed. At least **one deliberate ~400 ms absolute stillness** (nothing moves, captions hold) just before the
payoff. Cues key to **phrase starts** from the TTS timings, not to a beat grid (tetsu-tetsu333-576886).
*Check:* the storyboard lists idea timestamps (no gap > 2.5 s outside the payoff hold) and marks the stillness.

**(f) Restraint** (daniel-haida-636937). "3 extraordinary visual moments" beat "10 mediocre" ones: name the
three in PLAN §5 and spend the build time there. Elements in a group **never all start and stop on the same
frame** (offset arrivals by 40–120 ms). **Overshoot ≤ 2 %**; squash ≤ 8 % only on physical landings. One
primary move per transition (ik-builds-585923). Outgoing text clears before incoming text takes the same
space (brainextends-606193).

**(g) Anti-slop banned list** (techhalla-498547, ik-builds-585923, howdevelop-733090, brainextends-606193).
Fail Gate B5 if any appears:
- [ ] Corner text, frames or UI chrome: timecode, scrubbers, fps counters, progress counters, headers,
      watermarks, decorative footers (the kicker tag and the end mark are the only exceptions).
- [ ] AI clichés: brains, robots, neural-net node meshes, sparkles, glowing circuits, stock "futuristic HUD".
- [ ] Particle bursts or confetti, glows on anything but the one focal element, lens flares.
- [ ] Glassmorphism outside the `glass-diorama` family; purple/blue neon anywhere.
- [ ] Bouncy or elastic easing (`elastic`, `back.out` with overshoot > 2 %), spinning logos, 3D spinning cards.
- [ ] Tiny unreadable code (below the §3 floors), fake dashboards, invented %/multipliers/customer names.
- [ ] "Narrator essay energy": throat-clearing lines, slogans that aren't in the script, a paragraph on screen.
- [ ] Animator jargon on screen ("easing", "stagger", "squash").

**(h) Self-critique on the final file** (daniel-haida-636937, astrothewizard-618782, stokebuilder-356793).
Inspect frames **decoded from the final `renders/video.mp4`** (`ffmpeg -ss <t> -frames:v 1`), not browser
snapshots, and have a **separate judge sub-agent** rank issues **P0/P1/P2**. Give the judge daniel-haida's
rejection list: does any frame read as "a SaaS template", "a PowerPoint animation", "an AI-generated promo
template", or "excessive marketing copy"? Only P0/P1 go back for a fix; no blanket redo loops
(stokebuilder-356793). Re-measure loudness after the AAC encode (ik-builds-585923). This is Gate B14.

## 10. One signature beat, and the engines

The goal: more dynamic videos with less repetition. The research (animate, the
awesome-opus5-5 prompt library, Remotion/Manim creators) agrees: rotate the style as a
swappable kit, and give every video **one signature beat**, a hero moment that only this
video has. Pick it from something **not used in the last 5 videos** (`ledger.py looks --last 5`
shows `signature`):

- a HyperFrames registry block (`npx hyperframes catalog --query …`);
- a runtime adapter we rarely use: Three.js, Lottie or TypeGPU (`hyperframes-animation`);
- an animate style moment: the era morph, riso plates locking into register, the ink iris,
  a Manim Transform (`scripts/manim_clip.sh`);
- a technique adapted from `references/prompt-library.md`.

Write it in PLAN §5 as `Signature: <name> — <the beat it lands on>` and in POST.json as
`look.signature`. `ledger.py look-check … <signature>` refuses a repeat within 5 videos.

Further reading from animate (MIT): `vendor/animate/craft.md` (hard-won frame rules) and
`vendor/animate/grammar/FORMATS.md` (story formats: the morph chain, beat-cut). Three rules
worth keeping on every video:
- a shape morph carries the eye across "then → now" turns better than a cut;
- leave silence before the payoff (our one ≤ 1.2 s B16 beat);
- end on a changed version of the opening frame.

## Sources

- https://milanote.com/guide/motion-design-moodboard
- https://nngroup.com/articles/dark-mode-users-issues
- https://www.forasoft.com/learn/video-quality/articles-vqm/banding-gradient-steps
- https://m1.material.io/motion/duration-easing.html
- https://www.opus.pro/blog/ai-slop-aesthetic-12-tells
- https://github.com/Laith0003/ux-skill/wiki/Anti-AI-slop-ban-list
- https://www.3blue1brown.com/faq/
- https://raw.githubusercontent.com/yizhiyanhua-ai/fireworks-tech-graph/main/references/motion-effects.md
- https://support.google.com/youtube/answer/72431 (thumbnail specs)
- https://support.google.com/youtube/answer/13861714 (Test & Compare)
- https://www.hopperhq.com/blog/instagram-reel-size/ (3:4 grid crop)
- https://www.somake.ai/blog/youtube-shorts-aspect-ratio (Shorts safe-zone pixels)
- https://github.com/yihui-dev/awesome-opus5-5-videos (prompts cited in §9; excerpts in `references/prompt-library.md`)
