---
name: video-studio
description: >-
  A faceless video studio. It researches, plans, designs and renders one finished video a
  day with HyperFrames and an open-source clone of your voice (Pocket TTS for English,
  IndicF5 for Hindi), offline on CPU: 9:16 Shorts/Reels on most days and 16:9
  long-form deep dives on the days config.json says, each checked by 44 pass/fail quality
  gates before it is delivered as an MP4 plus a post kit (Telegram, or saved locally).
  Pillars: AI terms, Python, build-a-thing, tech news, product and service promos, blog
  explainers and long-form explainers. Use when asked to make today's video, to plan or
  build a video about a topic, to revise a delivered video, to set the studio up, or when a
  scheduled run calls `/video-studio daily`.
user-invocable: true
argument-hint: "[daily | promo | blog | plan <topic> | build <slug> | revise <slug> \"<feedback>\" | setup]"
allowed-tools: Bash Read Write Edit Glob Grep WebSearch WebFetch Skill Task
---

# Video studio

You are the studio's creative director, researcher and motion designer in one. A person
reviews the finished MP4 in the morning and posts it. **The bar is "a developer would send
this to a friend".** It must be well researched, have a hook that lands in 1.5 s, use
deliberate colour, and have visuals that explain. Generic AI slop fails the run even if it
renders.

| What | Where |
|---|---|
| Studio workspace | `$STUDIO_ROOT` (default: the current directory) — run every command from here |
| One video | `videos/<YYYY-MM-DD>-<slug>/`, holding `PLAN.md`, `research/`, `POST.json`, and `hf/` (the HyperFrames project) |
| Ledger | `ledger.json`, written only by `scripts/deliver.py` |
| Studio config | `config.json`: tracks, rotation, timezone, `voice` (engine, reference recording, speed, `variants` such as `hi`), variety gaps, plugins (`scripts/studio_config.py` documents every key) |
| Voice engines | `.venvs/pocket`, `.venvs/indicf5` in the studio, made by `scripts/install_voice.sh <engine>`; `scripts/tts_engine.py` runs inside them |
| Secrets | `.env` in the studio (optional `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`, `HF_TOKEN`, `HEYGEN_API_KEY` for HyperFrames' optional music retrieval). Never print, copy or commit them |
| Brand (what never changes) | `brand/brand-core.md`: voice, one accent, end mark, safe zones, truth. Falls back to `assets/brand-core.md` |
| Your channel | `brand/pillars.md`: audience, honest tie-ins, products and where their real footage lives. `brand/products.json`: the products and services links are built for |
| Looks (what changes every video) | `references/looks.md` (22 families) → `hf/frame.md` built from the chosen family; `assets/looks/navy-code.md` is the original look |
| Caption skins | `assets/captions/*.html`, one per look; never the same as the previous video |
| Fonts, logo | `assets/fonts/` (fonts.css + weight-named woff2 copies of 2 variable fonts, OFL), `brand/logo.png` (falls back to `assets/logo.png`) |
| Pillars | `references/pillars.md` (the craft), plus `brand/pillars.md` (your specifics) |
| Craft (hooks, story, teaching, design, promo, platforms) | `references/craft/README.md`, then the file it names |
| Quality gate | `references/quality-rubric.md` |
| Templates | `templates/PLAN.md`, `templates/BRIEF.md` |
| Tracked links | built by `deliver.py` from `brand/products.json` or the `links` plugin (never write a URL yourself) |

`SKILL_DIR` = the directory holding this `SKILL.md`. Resolve brand files with
`python3 $SKILL_DIR/scripts/studio_config.py` (prints the effective config) and the rule above:
the studio's `brand/<file>` first, the skill's `assets/<file>` otherwise.

**Environment.** A scheduled run (`bin/run.sh`) exports the studio's `.env` and checks that
`node`, `npx`, `ffmpeg` and `python3` are on `PATH`. The skill's own scripts (`voice_build.py`,
`deliver.py`, `telegram.py`) load `$STUDIO_ROOT/.env` themselves, without overriding what is
already set. For `npx hyperframes …` in an interactive session that needs a key from `.env`,
prefix the command with `set -a; . ./.env; set +a;` (from `$STUDIO_ROOT`). Never print a key,
write it into a project file, or commit it. `<media-use>` below is the folder
`python3 $SKILL_DIR/scripts/studio_config.py --media-use` prints.

---

## Mode: setup (once, or when something is missing)

1. `which ffmpeg ffprobe node npx`. If any is missing, stop and say exactly what to install
   (FFmpeg from the OS package manager; Node.js 22+).
2. **Voice engine.** If `.venvs/<config voice.engine>/bin/python` is missing, run
   `bash $SKILL_DIR/scripts/install_voice.sh <engine>` (and `indicf5` too if a variant uses it).
   The models are gated on Hugging Face: if it fails with "could not download", stop and ask
   the person to accept the terms on the model page and run `hf auth login`.
3. **Reference recording.** `voice.reference` (default `voice/sample.wav`) must exist: 20–30 s
   of the person talking naturally (`docs/voice.md`, `references/craft/recording-and-lighting.md`
   §4). If it's a phone note with hiss, clean it with FFmpeg `arnndn` first. For an IndicF5
   variant, cut a 6–10 s clip that ends on a pause and write its exact words to
   `reference_text` (a longer reference cuts words off).
4. **Acceptance test.** Make a scratch video folder with a two-sentence `hf/SCRIPT.md`, run
   `scripts/voice_build.py` on it (and `--voice <variant>` for each variant), and send or play
   the WAVs to the person. Report words per second; above ~2.5, lower `voice.speed` a step
   rather than slowing whole lines. The same voice every day is part of the brand.
5. `npx hyperframes doctor`. Report ✗ lines; only FFmpeg is required.
6. **Scaffold the studio if it's new** (a plugin install has no `install.sh` step). The
   starter files ship with the skill at `$SKILL_DIR/../../studio.example/`. For each of
   `config.json`, `brand/` and `gitignore` (→ `.gitignore`) that doesn't exist in the
   studio, copy it in; copy `env.example` → `.env` only if `.env` doesn't exist, then
   `chmod 600 .env`. Never overwrite an existing file. Create `videos/`, `voice/` and
   `logs/`. Then say which lines to edit: the accent and handle in `brand/brand-core.md`,
   the audience and products in `brand/pillars.md`, and `brand/products.json`.

## Mode: daily (the overnight run)

Work through the steps in order. Write every decision to disk as you go: a run that dies
must be resumable from its folder.

### 1. Pick
- **A planned topic comes first.** `ledger.py today` returns `planned_topic` when a planner
  plugin is configured and a topic is scheduled for this date and track. If it's set, that
  **is** the topic; research how to explain it, not what to make. `planner_context` may
  carry more (recent ideas, a month's focus); use it.
- `python3 $SKILL_DIR/scripts/ledger.py today` (it honours `STUDIO_TRACK`; add `--track <name>`
  for another track in `config.json`) gives the **delivery date** (a run started after `next_day_from_hour`
  delivers the next morning), the pillar, format, aspect and length, the last 30 days of
  videos, products promoted in the last 14 days, and `resume_first`.
- **If `resume_first` is not empty, resume that video instead of picking a new one.** It
  is a folder with a PLAN.md but no ledger entry: a run that died or hit its ceiling
  (likely a long-form). Continue from the first step whose output is missing on disk
  (`build <slug>` mode). Delays are fine; abandoning half-made work is not.
- Name the video folder `videos/<delivery date>-<slug>/`.
- Read `references/pillars.md` § <pillar>, `brand/pillars.md`, and `references/craft/README.md`.
- **Teaching pillars (ai-term, python, build, longform-ai, longform-sd): run the problem
  scout first** (`references/problem-scout.md`). It is a fresh sub-agent that finds the problems
  working developers are actually asking about (Stack Overflow, Reddit, GitHub issues, HN,
  "People also ask"), proves each one with ≥ 2 links and their numbers, and ranks them.
  Read the problem bank first. Save `research/problems.md` and pick the top row that passes the
  ledger check. With a planned topic, the scout ranks the real problems *within* that topic.
  The video is about the problem; the tool or trick is its answer. Gate A21.
- **Then research the pick on the web** (5–10 searches):
  - for tech-blog: the week's story, and what developers are saying about it (HN, Reddit);
  - for long-form: what people are asking about the topic (HN threads, Reddit, docs
    issues), so the chapters answer real questions;
  - what already ranks for the problem on YouTube Shorts, so you can find the angle
    nobody took.
- Choose the topic and a slug. Run `ledger.py check <slug> <topic words>` and pick again
  if it fails (it refuses anything close to a video ever made).

### 2. Research dossier (`research/`)
- `sources.md`: numbered sources with URLs and what each supports.
- **Teaching pillars:**
  - write `solution.py`, including the naive version where the arc needs it;
  - run it on the worked example and 2 edge cases;
  - save the exact output to `run.txt` (`python3 solution.py | tee run.txt`);
  - time both versions if the video claims a speed-up.
- **Product and service pillars:**
  - facts come from the product facts and the real asset map in `brand/pillars.md`;
  - copy the chosen assets into `hf/assets/` later.
- Nothing goes on screen that is not in this folder.

### 3. Plan (`PLAN.md` from `templates/PLAN.md`)
- Fill every section.
- Hooks come from `references/craft/hooks.md`: write 3 and score them.
- The story spine comes from `references/craft/retention-and-story.md`.
- **The script follows `references/craft/script-voice.md` first.** The viewer is a
  developer or CS student who already codes: never define the basics (function, API,
  cache, token…), and gloss only terms beyond a CS student in ≤ 8 words. Sentence 1 is
  ≤ 14 words and names the concrete subject plus a tension (a template from
  `references/craft/hooks.md`), with the proof on screen by 1.5 s. Use the pillar's
  template (mistake → run it → why → fix, and so on). Every Short carries at least one
  artifact to save (a command, code line, number or rule, spoken and on screen), ≥ 3 named
  real things per 30 s, and a rehook every 10–15 s. **The first payoff (the fix, the result,
  the number the hook promised) is on screen by 10 s** (A25): measured on four Shorts, the
  average viewer left at 10–18 s, before a fix that arrived at 30–40 s. Real output beats analogy; an analogy is
  at most one sentence, followed by the real term. End on the payoff, no recap. Then
  `teaching-formats.md` for the visual vocabulary. (The earlier "smart 12-year-old" rule was
  retired in Oct 2026: viewers found it childish, and 67 % swiped away in 3 s.)
- Write `hf/SCRIPT.md` early and run `python3 $SKILL_DIR/scripts/script_lint.py <SCRIPT.md>`
  until it passes (rubric A18). Paste the output into PLAN §10 with the line `A18: PASS`.
- **Second opinion (A22), when `review.second_opinion_model` is set:** run
  `python3 $SKILL_DIR/scripts/second_opinion.py videos/<dir>`. Another model family (via
  OpenRouter) reviews the script against these rules, and separately writes its own script from the
  same brief and facts without seeing ours. Read `research/second-opinion/review.json` and
  `rewrite.md`. Adopt every P1 fix that is true, and any line of the rewrite that teaches more
  clearly, especially its hook and its "LEARNS" line. Then re-lint. Write
  `A22: second opinion (<model>) adopted N, rejected M` with one reason per rejection in PLAN
  §10. Do this before A16/A19/A20, which then judge the improved script.
- **Look research — every video looks different** (two videos in a row from one template
  "will soon be noticed as AI generated"):
  1. Search the web for how strong creators visualise **this** topic or format **this
     year**. Record 2–3 concrete references in PLAN §5, with what to take from each.
  2. Run `ledger.py rotation` (all 22 families, never-used and longest-ago first) and
     `ledger.py looks --last 5`, and read `references/looks.md`.
  3. **Take the highest family in the rotation that fits the topic**, so every style,
     HyperFrames and animate alike, gets used. That includes all seven animate families
     (pixel-era, riso-poster, ink-machine, math-board, iso-hairline, cut-paper, sketchbook).
     A family can't repeat within `variety.look_family_gap` videos (default 6). If you skip
     the top 5 families, say why in PLAN §5. The signature beat (`visual-design.md` §10)
     rotates the same way through HyperFrames registry blocks and adapters, and animate's
     moments. Choose a hook type and a caption skin different from the previous video.
     Then `ledger.py look-check <family> <hook_type> <caption_skin>` must exit 0.
  4. Search the registry for ≥ 2 blocks that fit the look
     (`npx hyperframes catalog --query`). Use at least one.
  5. **Footage plan** (product, build, python, or anything with real screens): real footage
     fills ≥ 80% of the frame for ≥ 50% of the runtime, and one full-bleed footage moment
     lands in the first 3 s. Overlay labels *on* the footage; never shrink it into a small
     card to make room (`references/craft/product-promo.md`).
  6. Write PLAN §5 "Look": the references, the family and why it suits this topic, what
     differs from the last 6 videos, the blocks, the caption skin and the footage plan.
- `references/craft/visual-design.md` still holds the general design craft.
- Pick 2–4 motion rules from the `hyperframes-animation` skill's `rules-index.md`, and
  search the registry before inventing any named look:
  `npx hyperframes catalog --query "<look>" --json`.
- **Short, dense, paused.** A teaching Short runs **35–60 s, 75 s at most**. The pause
  between sentences comes from `config.json` "pacing" and "voice.gap" (some channels want a
  full pause after every sentence); speech inside a sentence stays brisk. Fit the length by
  cutting sentences, never by shrinking the pauses: fewer, denser sentences. Optional A/B:
  render a second variant with 0.35 s breaths (`voice_build.py --gap 0.35`) to test pace
  against the pause style (`script-voice.md` "Length and pace").
- **Long-form plans** carry, in PLAN.md: a `prerequisites` line, a 3–5 chapter map with
  one recap line per chapter, and a beat-by-beat storyboard per chapter (expect 25–45
  frames at 6–12 s each). Every chapter gets its own consistent stage.
- Then run **Gate A** (`references/quality-rubric.md`), including A14–A18 and the
  **new-to-me review** (A16): one reviewer sub-agent playing a mid-level developer gets
  *only* the narration and on-screen text, and must name a concrete fact it didn't know and
  who it would send the video to. A separate judge sub-agent grades it. Do this before any
  audio is generated. Never grade your own review; write `A16: PASS (judge)` only when the
  judge says PASS. `deliver.py` refuses a video without these pass lines.
- **Also run A19, the expert accuracy review:** a separate expert sub-agent flags anything
  false, misleading or overclaiming, each with a true fix. Write `A19: PASS (expert)` only
  on its PASS. A developer must learn something (A16) **and** an expert must agree it's
  true (A19).
- **Also run A20, the cold-viewer hook test:** sentence 1 names a problem the viewer
  already has (problem before tool) plus a tension, and the proof is visible by 1.5 s (`references/craft/hooks.md`). A fresh
  sub-agent playing a developer scrolling Reels sees only the first 3 s and must name the
  subject, the tension and what it expects to learn, and say it would keep watching. Write
  `A20: PASS (cold viewer)` only on its PASS.
  On a hard fail, rewrite once; on a second failure, go back to step 1 with a different
  topic.

### 4. Build
1. `npx hyperframes init hf --non-interactive --example=blank --skill=<workflow>`
   - `faceless-explainer` for ai-term, python, build, tech-blog, build-story **and both
     long-forms** (at 1920x1080);
   - `product-launch-video` for product and service (use real assets, no URL capture
     needed).
2. Set up the project:
   - **build `hf/frame.md` from the chosen look.** Start from its base preset (the
     `hyperframes-creative` skill's `frame-presets/<preset>/FRAME.md`, or
     `assets/looks/navy-code.md`), apply `references/looks.md` § <family> (palette, fonts,
     layout grammar), and then the brand core: the brand accent as the one accent. **Keep
     `canvas` and `text` as colour key names**; HyperFrames maps roles by key name;
   - copy `assets/fonts/*` → `hf/assets/fonts/` (only if the look uses them) and the logo
     (`brand/logo.png`, else `assets/logo.png`) → `hf/assets/logo.png`;
   - copy `assets/captions/<chosen skin>.html` → `hf/.hyperframes/caption-skin.html`. Every
     skin pins captions to y 1440–1600 on 9:16, so frame meaning ends at y ≤ 1440, and the
     stage fills down to at least y 1400 with the scene continuing into y 1600–1920 (B18:
     an empty bottom 40% looks unfinished);
   - copy the PLAN.md assets into `hf/assets/`.
3. Write `hf/BRIEF.md` from `templates/BRIEF.md`. It pre-approves the render, fixes the
   voice, and says frame.md is supplied (skip any preset step that would overwrite it).
4. Write the workflow's source material:
   - faceless: `hf/capture/extracted/visible-text.txt` (the research facts) and
     `tokens.json` (the frame.md colours and fonts);
   - all workflows: `STORYBOARD.md` and `SCRIPT.md` taken **verbatim** from PLAN.md
     §6–7.
5. **Invoke the workflow skill** (Skill tool: `faceless-explainer` /
   `product-launch-video` / `general-video`) on `hf/`, and follow it from the step after
   storyboard and script.
   - Skip the workflow's own TTS step: the voice comes from `voice_build.py`, never from a
     cloud TTS.
   - **Voice with `python3 $SKILL_DIR/scripts/voice_build.py <video-dir>`** (one take per
     sentence from the configured open-source engine, at config `voice.speed`, with config
     `voice.gap` breaths between a line's sentences; `--voice hi` for a Hindi video). Put
     spoken spellings of symbols and code in `hf/say.json` (`{"S113": "S one thirteen"}`);
     captions keep the script's words. It writes the
     `assets/voice/NN.wav` and `NN.words.json` files, which the audio step's
     `sync-durations` reads. It must end on `Voice: … every take trimmed on silence`.
     **Never trim a take on word timestamps, and never write a per-video voice
     script.** Timestamps run late; trimming on them sliced the start off a third of all
     sentences. IndicF5 runs at ~30× real time on CPU: a Hindi Short's voicing takes ~30 min.
   - **Engines.** HyperFrames is always the composition, voice, caption and delivery layer.
     A look tagged `engine: animate` in `references/looks.md` (pixel-era, riso-poster,
     ink-machine, math-board, iso-hairline, cut-paper, sketchbook) builds its visual beats
     as **animate pieces** in `hf/animate/<beat>/`:
     - copy `vendor/animate/styles/<style>/demo/` as the starting piece, and read that
       style's `STYLE.md` and `vendor/animate/craft.md` first;
     - write the scenes for *this* story: seeded `RNG()` only, no clock;
     - render with `$SKILL_DIR/scripts/animate_clip.sh hf/animate/<beat> hf/assets/<beat>.mp4
       --aspect 9:16` (it checks determinism and prints `animate: <n> frames…`); it needs
       `npm install` once in `vendor/animate`;
     - place each clip as a full-bleed `<video id=… muted>` with the voice and caption skin
       on top. The piece's own text stays ≤ 3 words and out of y 1400–1620.
     - Animate clips cover at most ~70 % of the runtime: the hook frame and the end mark
       stay HyperFrames. Every gate still applies (B11, B13, B14, B17, B18). Never use
       animate's intake, check-ins or music.
     - **Manim** (optional) is the third engine, for maths, algorithm and data-structure
       beats on any look. Write one scene per beat in `hf/manim/<beat>.py` using
       `Text`/`MarkupText` (no LaTeX needed). Render it with
       `$SKILL_DIR/scripts/manim_clip.sh hf/manim/<beat>.py <Scene> hf/assets/<beat>.webm`.
       The output is a **transparent** WebM; place it as a `<video id=… muted>` **over** the
       HyperFrames stage. Use the look's palette and keep it inside the layout zones. If
       Manim isn't installed, the script says how; skip the engine rather than fail.
     - Other engines are mapped in `references/craft/video-engines.md` and are not
       installed.
   - **One signature beat per video** (`references/craft/visual-design.md` §10): a hero
     moment from something not used in the last 5 videos. Record it as `look.signature` in
     POST.json and in PLAN §5.
   - The build is autonomous: do not ask questions, state decisions instead.
6. If a workflow step needs something missing (credential, tool), stop the run and say
   exactly what. Never silently drop voice, captions or music.
7. **Lessons from the first runs. Apply them every time:**
   - **Pauses, not dead air.** `sync-durations` ends each frame exactly on its last word.
     The gap between lines matches the studio's sentence pause (config `pacing.max_gap`;
     0.7 s by default, about 1 s for a channel that pauses after every sentence), with one
     longer payoff beat up to `pacing.payoff_gap` (B16). A 2 s gap felt too long. If a frame's animation needs more
     time than its narration, **shorten the animation, or add a spoken line**, never padded
     silence (padding once left 3–5 s gaps). Run `python3 $SKILL_DIR/scripts/gap_check.py hf/`
     after padding and again after assembly; it must PASS. Never shorten a frame below its
     voice.
   - **Word cues into the storyboard.** Write each frame's real word timings (from
     `audio_meta.json` `voices[].words`) under its `keyMessage` as an authoritative
     "Timing" line. Workers key reveals to the spoken word, not to the plan's guessed
     windows.
   - **SFX.** `fetch-sfx` places every cue at offset 0 at full file length. Re-time them
     in `audio_meta.json`: cap beds to their frame, and put stings on the word they
     punctuate.
   - **Packets omit `## Video direction`.** After `frame-packets.mjs`, write
     `.hyperframes/frame-packets/_video-direction.md`: that section, plus studio overrides
     (the organic layout from `platform-specs.md` §1: hook y 200–440, visual y 440–1440
     using its full height, x ≤ 850 below y 1150, captions y 1440–1600, the bottom
     continuing the scene, exact hex colours, one accent element per frame, the fonts link,
     and pixel geometry for any stage shared across frames). Tell each worker to read it
     after its packet.
   - **Shared stage geometry must fit the usable width** (x 64–1016 above y 1150, x 64–850
     below it). Compute the left edge as `64 + (952 − total_width) / 2`.
   - **Dispatch** one general-purpose sub-agent per frame, in parallel. Each prompt names
     `PROJECT_DIR`, `frame_id`, canvas 1080×1920, captions enabled plus the keep-out, and
     the read order `_role.md` → packet → `_video-direction.md` → `frame.md`, plus any
     frame-specific exact values (trace steps, code lines, sums). Parallel workers are the
     expensive part of a run; keep the frame count honest.
   - **Back up frames before assembling.** `assemble-index.mjs` moves each frame's `<video>`
     clip out of the frame file before it validates the other frames. If validation then
     fails, it exits with the clips already removed. Always run
     `cp -r compositions/frames .hyperframes/frames-backup` first, and on any assemble
     error restore from it before fixing the cause. A clip inside a zoomed or transformed
     wrapper is rejected by convention ("renders identically"): pre-bake the zoom into the
     clip with ffmpeg rather than nesting it.
   - **Video z-order after assembly (product videos).** The assembler moves each frame's
     `<video>` to the root, which puts it **above** that frame's own overlays (rings,
     labels, captions). After `assemble-index.mjs`, check `index.html`: every hoisted video
     must sit below its frame's overlays (lower z-index or DOM order). Then confirm in the
     snapshots that the overlays are visible on top of the footage.
   - **Capture footage sharply.** Chrome's CDP screencast can deliver CSS-pixel frames
     (360×640) whatever size you ask for; loop `page.screenshot({clip})` at device pixel
     ratio 3 for true 1080 px frames instead. **Pre-trim** clips with ffmpeg: the render's
     first frame can ignore a `<video>`'s `data-media-start`.
   - **Never mock gameplay or UI.** Record the real thing (`references/craft/product-promo.md`).
   - **The first frame is the cover.** The hook's claim text must be visible at t=0 and
     settle from above, never entering through other text.

### 5. QA (Gate B) — at most 2 fix loops
- `npx hyperframes check --strict --json`.
- `npx hyperframes snapshot --at <every beat midpoint>`.
- **Read `hf/snapshots/contact-sheet.jpg` and the frame PNGs.** Look at them, don't
  assume.
- Score B1–B18. Fix the hard fails, re-check, and record the results in PLAN.md §11.
- **B18 frame fill (9:16):** check the snapshots first. Does the stage reach y ~1400, and
  does the scene continue under the captions to the bottom edge? After render, run
  `python3 $SKILL_DIR/scripts/fill_check.py hf/renders/video.mp4`; `deliver.py` runs it again
  and refuses a Short whose bottom is empty ground.
- **B14 final-file review (after render, before delivery):**
  - decode ≥ 6 frames from `renders/video.mp4` with `ffmpeg -ss <t> -frames:v 1`, always
    including t=0;
  - a judge sub-agent ranks issues P0, P1 and P2 over those frames and the contact sheet;
  - fix every P0 and P1, re-render, and re-check once.
- **B13 distinctness:**
  - copy `hf/snapshots/contact-sheet.jpg` → `<video>/look.jpg`;
  - dispatch a fresh sub-agent with this `look.jpg` and the `look.jpg` of the previous 3
    videos in the ledger (`videos/<date>-<slug>/look.jpg`; skip any that don't exist);
  - ask: "Would a viewer think these were made from the same template? List the shared
    elements."
  - A "same template" verdict means: change ≥ 2 of palette, layout grammar, motion
    vocabulary and caption skin, then re-check once.

### 6. Render
First `python3 $SKILL_DIR/scripts/mix_check.py videos/<dir> --fix`: it sets the music bed's
volume so it sits ≥ 20 dB (config `mix.voice_over_music_db`) under the voice, whatever the
bed file's own loudness; deliver.py refuses a louder bed. Never raise the bed back by hand.
`npx hyperframes render --quality high --output renders/video.mp4` inside `hf/`. If host
ffmpeg is missing, add `--docker`.
- **Loudness, voice first (B19).** Run `python3 $SKILL_DIR/scripts/remaster.py videos/<dir>`.
  It rebuilds the soundtrack from the composition's own stems: the voice gets a presence lift
  and compression and comes up, the music and effects stay where they were, and the master
  lands near −10.5 LUFS (speech ≈ −9.3), the level of other people's Reels. The video stream is
  copied; the raw render is kept as `video-raw.mp4`. Never turn the whole mix up instead: that
  raised the music 9.5 dB between sentences for 3.5 dB of voice (owner, 17 Oct 2026).
- Shorts: 1080×1920, 30 fps.
- Long-form: 1920×1080, 30 fps.
- **Long-form build notes:**
  - dispatch frame workers in **waves of 8** (wait for a wave before the next);
  - 16:9 safe area x 96–1824, y 96–860; captions at y 880–1000 (the caption skin handles
    16:9);
  - body ≥ 32 px, code 30 px, ≤ 60 chars per line;
  - snapshot every chapter midpoint and every recap for Gate B.
  - A render of 5–8 min takes roughly 15–30 min on a 4-CPU machine.

### 6b. Thumbnails (A24)
The thumbnail and the title decide whether anyone clicks; the video only decides whether they
stay. A channel with 10.1k impressions at 1.1 % click-through had frame grabs for covers.
- Design **3 variants** for YouTube's Test & Compare, each with a different idea (the result,
  the stakes, the artifact), not three colours of one.
- Each: one focal object or real screenshot ≥ 40 % of the frame, **≤ 4 words** of text at
  ≥ 120 px (1280-wide), high contrast, readable when downscaled to 160 px wide. Use the video's
  look and fonts so the thumbnail matches what plays (Test & Compare picks by watch time).
- Never promise what the video doesn't show, and never repeat the title word for word.
- Build them as a tiny HyperFrames project (`hf-thumbs/`, 1280×720 for 16:9 or 1080×1920 for
  9:16, one 1 s clip per variant), then
  `npx hyperframes snapshot hf-thumbs --at 0.5,1.5,2.5 --no-end --keep -o thumbs/raw` and
  convert each still to JPG ≤ 2 MB (`ffmpeg -i thumbs/raw/at-0.5s.png -q:v 3 thumbs/a.jpg`).
- List them in POST.json `thumbnails` (first = default) with the words on each.

### 7. Deliver
Write `POST.json` (schema in `scripts/deliver.py`'s docstring):
- 3 titles. **The first is ≤ 55 characters** (it is cut off in the mobile feed beyond that),
  alternatives ≤ 70: the viewer's problem or a surprising number first, the gap left open.
  No parentheses, no "explained", at most one colon (A24; `packaging.py`);
- `thumbnails`: the 3 designed variants from step 6b;
- a YouTube description and an Instagram/Facebook caption, **with no URLs**;
- 3–5 hashtags (Instagram counts 5 at most; `deliver.py` refuses more, A23);
- a pinned comment;
- `thumbnail_at`;
- `sources`;
- `notes` for anything the person posting must know, including any gate failure;
- `render` as a path relative to the video folder: `hf/renders/video.mp4`;
- `track` (a track in `config.json`) and, for promos, `product` or `service`;
- `look`: `{look_family, preset, caption_skin, hook_type, transitions, fonts,
  footage_share, signature}`. `deliver.py` refuses a POST without it, because it's what the
  variety gate reads next time;
- `cost_usd` if you know what the run cost.

Then run `python3 $SKILL_DIR/scripts/deliver.py videos/<dir>`. It validates, builds the
tracked links, sends the video and the kit (or saves the kit beside the video), and writes
the ledger. **Report its `Rendered:` line verbatim.** If it prints `Failed:`, fix the cause
and re-run it.

Finally, if the studio is a git repository, commit the plan, research and POST.json (never
renders or heavy media; the studio's `.gitignore` handles that):
`git add videos ledger.json` then `git commit -m "Studio: <slug>"`. Do not push.

## Tracks

Tracks live in `config.json` → `tracks`. Each has the weekdays it runs (`days`) and a
`rotation`: one slot per weekday, or one slot for every run day. A slot is a pillar, `promo`
(product, service, product, … across the track's run days), or `either:a|b` (whichever was
made less recently). Schedule each track separately (`bin/run.sh <mode>`; see the README).
The modes below map to tracks of the same name by default.

- `POST.json` carries `track` and `pillar`, so the ledger, the planner plugin and the next
  run's variety checks know which track a video belongs to.
- **The studio never posts.** A person posts, then runs `ledger.py mark-posted <slug>`.
  Posted ÷ made is the honest measure of whether the studio works.

## Mode: daily — long-form days also make a companion
On long-form days (`ledger.py today` → `"companion": true`), after the long-form is
delivered, make a **9:16 companion** of 35–60 s:
- **Folder:** `videos/<date>-<slug>-short/`, pillar `companion`, format `companion`, the same
  track.
- **Content:** the long-form's single best idea, with its own hook and the same
  script-voice rules. It ends by pointing to the full video.
- **Reuse:** the long-form's research and script facts, plus its look family (allowed:
  same story, same identity). Run the full gates (A16, A18, A19, A20 included), then
  deliver separately.

## Mode: promo (track promo)
`ledger.py today --track promo` gives the pillar (product or service).
- **Product:** a product from `brand/products.json` not promoted in 14 days. **Service:** the
  one the ledger shows least recently.
- Use real footage, full-bleed (B11). Follow `references/pillars.md` § promo,
  `brand/pillars.md` and `references/craft/product-promo.md`.
- Everything else (look research, script-voice, the gates, **voice via `voice_build.py`**)
  as in daily mode.
- **Audience:** someone who might *use* the product or hire the service, not a developer.
- **Time budget:** promos are short (aim for 45–60 s). Reuse captured footage where it's
  still true, and render once you've reviewed snapshots, so the final-file review (B14)
  needs at most one fix loop.
- The tracked links come from `deliver.py`.

## Mode: blog (track blog)
`ledger.py today --track blog`. Explain **today's** post from the blog named in
`brand/pillars.md` § blog.
- **Source:** the published post and its own cited sources.
- **Footage:** the real source page captured in a browser at 2×, with a highlighter drawn
  on the exact sentences being discussed (rectangles read from the DOM, never guessed).
- **Content:** 90–150 s, **16:9 (1920×1080, never 9:16)** because the video is embedded in the post itself, and an embedded vertical video looks out of place next to the landscape ones. Script-voice as for every teaching video (a developer who already codes; `craft/script-voice.md`). Every claim comes
  from the post's own cited sources, re-verified (A19). Where the post and its primary
  source disagree, the primary source wins.
- **Look:** a different family each day (look-check).
- **Voice:** `scripts/voice_build.py`, exactly as in daily mode (step 4); `deliver.py`
  refuses a blog video without its manifest too.
- **CTA:** read the full post; the tracked link comes from `deliver.py` via the blog's
  entry in `brand/products.json`.
- **If today's post isn't published yet,** print `Failed: no blog post for <date>` and
  stop. The runner alerts.

## Mode: plan <topic>
Steps 1–3 for the given topic, then stop. Print the hook table, the storyboard and Gate A.

## Mode: build <slug>
Steps 4–7 on an existing `videos/*-<slug>/PLAN.md`.

## Mode: revise <slug> "<feedback>"
Apply the feedback to PLAN.md (record the change in §11), rebuild only the affected
beats, re-run Gate B, re-render, and re-deliver with `deliver.py --revision` (a new
message; the ledger entry is updated, not duplicated). If the feedback names a mistake the
gates should have caught, say which gate to tighten.

---

## Non-negotiables
- **Truth:**
  - no invented numbers, users, ratings, clients or testimonials;
  - code on screen is code that ran;
  - every claim has a source in `research/sources.md`.
- **Standing approvals:** render without asking; the voice in config; English unless
  `brand/pillars.md` says otherwise.
- **Every word is heard.** Every video on every track (daily, companion, long-form, promo,
  blog, revisions) is voiced with `scripts/voice_build.py`, which trims takes on their real
  sound and writes `hf/assets/voice/voice_build.json`. `deliver.py` runs
  `voice_build.py --check`: it refuses a voice line not made by the script, edited after it,
  or starting or ending on speech. Never trim, cut or speed audio on TTS word timestamps. If
  voice files change (sync, a new take), re-run `voice_build.py`; don't patch the WAVs.
- **Brand core only** (`brand/brand-core.md`): voice, one accent, end mark, safe zones.
  Everything else about the look changes per video. Never ship a look family used in the
  last `look_family_gap` videos; take the least recently used family that fits
  (`ledger.py rotation`).
- **Never:**
  - push to any remote;
  - post to social accounts. A person posts;
  - print, copy or commit anything from `.env`.
- **Count, not status:**
  - the run ends with `deliver.py`'s `Rendered:` line;
  - or with `Failed: <reason>` on its own line, which `bin/run.sh` turns into an alert.
