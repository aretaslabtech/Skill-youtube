# Prompt library — what the best Opus 5.5 video prompts ask for

Source: [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)
(513 prompts, read 10 Oct 2026). Twelve entries chosen for the bar they set, not the topic.

**How to use this file**
1. During **Look research** (SKILL.md §3), read the 2–3 entries closest to today's topic or family.
2. Take a *rule* from each (a constraint, a check, a scene shape), never a whole style.
3. Write what you took into PLAN §5 next to the web references, credited by slug.
4. Never copy a palette, font list or storyboard wholesale; our brand core and `looks.md` win.
5. Some authors use things we ban (Syne, spring overshoot, neon). Their *process* is the lesson.
6. Quotes are verbatim excerpts (≤ ~120 words; `…` marks a cut, `·` a list line break).
7. Their numbers (fps, durations, BPM) are theirs; ours come from `craft/platform-specs.md`.
8. "What we take" bullets name the place in our pipeline where the idea lands.
9. When a prompt and `visual-design.md` disagree, `visual-design.md` wins.
10. Add an entry only after a video used the idea and it worked; cite the video slug.

---

## 1. astrothewizard-618782 — the journey of photons (explainer)
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/astrothewizard-618782.md>

> "Make it genuinely educational and accurate. Where you can, simulate the real thing: the
> random walk should be an actual random walk, not a drawing of one. Include real numbers (core
> temperature, distance, travel time, years inside the Sun) and be honest about uncertainty in the
> estimates. Use humor and visual gags to keep attention: onomatopoeia, little characters,
> callbacks. Put what was happening on Earth during those 100,000 years alongside the photon's
> timeline. … Burned-in captions, since most people watch on X with the sound off … Build
> verification loops: render stills of every scene and review them critically, check transitions
> frame by frame, measure the audio mix numerically, fix what's weak and re-render."

**What we take**
- **Simulate, don't depict**: if the concept is a process (sampling, hashing, a queue, attention),
  compute it in the composition with a seeded PRNG and draw the result. Gate it in PLAN §5.
- **Honest numbers with error bars**: every figure from `research/sources.md`, ranges spoken as
  ranges ("somewhere between 10,000 and 170,000 years").
- **Context-alongside-timeline** scene shape: a second lane shows what else was happening.
- One mascot + onomatopoeia + a callback in the last beat → the `mascot-led` family.

## 2. ik-builds-585923 — HyperFrames motion-graphics template
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/ik-builds-585923.md>

> "Style: paper-light canvas, marker notes that draw on, real physics, huge kinetic type,
> hard light/dark switches, a new idea every 1.5–2 s, a sound on every hit. …
> - No chrome (scrubber, timecode, fps, headers). No animator jargon on screen … 
> - No invented results: no %, multipliers, customer names or figures. …
> Fonts {{BRAND_FONTS}}; Anton for kinetic type; Caveat handwriting via stroke-dashoffset. …
> Check the HyperFrames registry first. Set every from-state at t=0 (seek-safe); never cover
> an exit. One primary move per transition; no generic push/slide/rotate-swing. …
> Master -14 LUFS, -2 dBTP, re-measured after AAC encode."

**What we take**
- The whole look is now the `marker-on-paper` family (Anton + Caveat embedded via `@font-face`).
- **Visual rhythm**: a new visual idea every 1.5–2 s *while narration keeps its paced sentences*.
- **A sound on every hit**: every slam, draw-on and landing gets an SFX in the cue sheet.
- **Loudness re-measured after the AAC encode**, not before (our §6 loudnorm step; verify with a
  second `ffmpeg -af ebur128` pass on `renders/video.mp4`).

## 3. daniel-haida-636937 — Taxtello product film
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/daniel-haida-636937.md>

> "I want transitions that make the viewer think: “Of course the next scene came from that.”
> Good: chart line → document edge · gold pill → invoice button · financial number → amount in
> invoice · card edge → next surface · camera push through interface element · shared geometry ·
> mask reveal using actual product shapes. Bad: crossfade · random wipe · spin transition ·
> glitch · whip-pan every two seconds · generic SaaS slide-left · zoom-blur spam. …
> Reject your own result if it feels like: a SaaS template · a PowerPoint animation … an
> AI-generated promo template … I would rather have: 3 extraordinary visual moments than
> 10 mediocre feature animations."

**What we take**
- **Object-driven transitions** as the main grammar (`visual-design.md` §9b); catalog transitions
  are punctuation, not the sentence.
- Its self-rejection list goes into Gate B as a judge prompt: "Does any frame read as a template?"
- "Elements should not all start and stop at exactly the same frame"; "overshoot below ~2%".
- Inspect **decoded frames from the final MP4**, not browser screenshots (our B14).

## 4. gdgtify-929495 — "BUILD THE FLOOR" kinetic speech
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/gdgtify-929495.md>

> "Words have assigned architectural roles. WAIT is a lintel. WAITING is a suspended load. VOICE
> is a support. ROOM is an opening. FLOOR is a platform. These roles must emerge from the actual
> letterforms, not from separate illustrations placed behind text. … Do not force the speech onto
> a dance beat. Use a cue sheet based on phrases, pauses, and emphasis. Phrase reveals should
> follow reading order. Allow at least one 400ms moment of absolute stillness. … Keep the
> currently spoken phrase readable before it becomes architecture."

**What we take**
- **Words as objects**: the key term *becomes* the diagram (the word TOKEN splits into tokens).
- **Phrase-based cue sheet** from the TTS word timings, not a BPM grid, for narrated videos.
- **One ≥ 400 ms absolute stillness** before the payoff, logged in the PLAN storyboard.
- Final scene stands on something earlier scenes built (a structural callback).

## 5. stokebuilder-356793 — 50 podcast animations
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/stokebuilder-356793.md>

> "Write a shared style bible and a component kit first, so every animation looks like the same
> show. … Copy must be verbatim or faithful to what's said. Never invent facts, numbers or
> quotes. Sync each animation's beats to the spoken words. … Opus 5.5 at medium effort builds
> each animation. Opus 5.5 at extra-high effort judges each one once on brand consistency with
> the others, visual interest, relevance to the narrative and creative judgment. Only cues the
> judge considers egregiously bad go back for a fix. No blanket redo loops."

**What we take**
- PLAN §5 doubles as a **style bible**; long-forms also list a component kit (3–6 reusable parts).
- On-screen copy is **faithful to the narration**: no extra slogans or numbers not spoken or sourced.
- **Builder/judge split**: the judge is a separate sub-agent; only P0/P1 go back (our 2-loop cap).

## 6. howdevelop-733090 — TanStack AI launch film
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/howdevelop-733090.md>

> "Every transition should visually demonstrate a feature, rather than simply replace one title
> card with another. Keep all on-screen wording brief and legible. Avoid generic stock footage,
> spinning logos, fake dashboards, excessive glitch effects, and tiny code nobody can read. …
> The story must also work muted. … Do not call it a stable v1 release. Do not present planned
> orchestration features as already shipped. … The goal is a memorable showreel, not a
> slideshow of feature bullets."

**What we take**
- **Transition = demonstration**: an interrupted stream that resumes *is* the cut to "resumable".
- **Works muted** check: watch the contact sheet with captions only; can you retell it?
- Accuracy guardrails per tool video: list what is RC / beta / planned in `research/` and on screen.

## 7. techhalla-498547 — kinetic identity bumper
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/techhalla-498547.md>

> "BANNED: Generic AI clichés (brains, robots, neural nets, sparkles), soft gradients, bouncy
> cartoon easing, particle explosions, stock “futuristic HUD”, long paragraphs, narrator essay
> energy, Canva-deck energy, extra slogans beyond the locked message, purple/blue neon,
> glassmorphism. … Pre-pass: before full render, export one still per major beat (8 frames).
> Fix cramped type, orphan words, low contrast — then render."

**What we take**
- The banned list is folded into `visual-design.md` §9g (our anti-slop list).
- "Narrator essay energy" is a script check too: no throat-clearing sentences in `SCRIPT.md`.
- Ignore its type choices (Syne is banned for us) and its spring overshoot.

## 8. emollick-019567 — recursion, every part a different style
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/emollick-019567.md>

> "A video explaining recursion, where every explanation about recursion has a radically different
> video style, make this self-referential & clever & fast moving."

**What we take**
- **Form mirrors content**: when the concept is self-similar (recursion, fractals, nested calls),
  the structure of the video can be too. One per quarter at most; it is a stunt.
- A per-chapter style change is allowed in long-form *if* each chapter keeps one consistent stage
  and the brand core holds (`looks.md`).

## 9. x4b47x-034026 — paper shadow theatre, 9:16
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/x4b47x-034026.md>

> "Create a pure javascript animation. 30-60s, vertical 9:16, paper cut-out shadow theatre style
> with gentle, fitting audio (made in code) on the topic: What makes a place feel like home?"

**What we take**
- A one-line prompt worked because the **medium is a strong formal idea** with built-in rules
  (silhouettes, one light, a screen) → the `paper-shadow-theatre` family.
- Gentle topics (what a small-business owner fears, why automation feels risky) suit a gentle medium.

## 10. brainextends-606193 — Spotify product film
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/brainextends-606193.md>

> "Do not add an outer caption, creator watermark, decorative footer, or progress counter … For
> most of the middle sequence, keep one narrow rounded player bar near the bottom of the inner
> stage … This recurring player connects the changing shots. It must remain visually secondary
> to the artwork … Outgoing titles must disappear before incoming titles occupy the same space.
> Avoid overlapping text, sudden camera resets, long blank intervals, and arbitrary full-frame
> crossfades."

**What we take**
- **Tagged shot list**: write the PLAN storyboard as sections (`<art_direction>`, `<timeline>`,
  `<persistent_element>`, `<motion_quality>`, `<validation>`) with second-accurate beats.
- **One persistent element** that rides through scenes and stitches them (a cursor, a token, a cup).
- Outgoing text clears **before** incoming text lands in the same space.

## 11. tetsu-tetsu333-576886 — KotoSearch launch, phrase-synced
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/tetsu-tetsu333-576886.md>

> "② Claudeがアプリを触って、機能仕様書を作成 機能・料金・言っちゃダメな表現まで整理 …
> ⑤ ClaudeがRemotionで動画を実装 書き出した静止画を自分で見て、文字切れや重なりまで直してくる …
> ⑦ Claudeが音声を32フレーズに分解 話した瞬間に画面とテロップが出るよう自動で同期 ⑧ BGMは
> Claudeがコードで作曲 声の下では自動で音量を下げてくれる"

(Translation: ② Claude used the app and wrote a spec: features, pricing, even *phrases we must not
say*. ⑤ It looked at its own exported stills and fixed clipped and overlapping text. ⑦ It split
the voice into 32 phrases so the screen and the caption appear the instant each is spoken.
⑧ It composed the BGM in code and ducked it under the voice.)

**What we take**
- **Phrase-synced captions and visuals**: split the TTS into phrases; each visual change keys to a
  phrase start, not to an arbitrary second (`captions.mjs` groups = phrases).
- A **"must not say" list** in `research/` for product and service videos (claims, prices).
- Duck BGM under the voice (`hyperframes-audio` voiceover carve).

## 12. doubleunplussed-181894 — AI-lore music video, character direction
<https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/doubleunplussed-181894.md>

> "Don't feel the need to represent everything in the lyrics literally - feel free to include
> relevant references to concepts, events, and lore in the video, even if obscure (especially if
> obscure). … A style change - don't make Dr. Null's mouth wobble with the lyrics as if he's
> singing, it doesn't actually look like he's singing, just that the curcle of his mouth is
> jittery. Best to just not make him be singing. Make him just have appropriate expressions for
> the scenes … Dr. Null's arms look a bit unnatural in many scenes"

**What we take**
- **No fake lip sync**. A mascot acts through expressions and poses held per beat (`mascot-led`).
- Check limbs and hands in every snapshot; an unnatural pose reads as a generation error.
- **Earned references** (a real paper, a real incident) reward the regulars; keep them sourced.
