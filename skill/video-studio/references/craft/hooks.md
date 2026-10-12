# Hooks — the first 1–3 seconds

The hook is not "the intro". It is **frame 0 to ~1.5 s**, and on Shorts/Reels it is the
whole decision. Everything below is checkable against a plan or a snapshot.

## The rule: ask their question, then show the proof

> Review feedback: "If the video started like *why your shop's website loads slowly* and then showed the
> comparison of heavy images and lighter images, it would have been a better hook. I am
> noticing this in all videos — the hook doesn't make sense."

Our hooks scored well on craft (a specific gap, fast, the subject on screen) and still
failed, because they were **clever instead of clear**: "Ten comparisons, or five lookups.
Same answer." means nothing to someone who doesn't already know the video is about Two
Sum. A stranger scrolling past has no context. So every hook now has two parts, in this
order:

1. **The question (spoken at 0 s, on screen as the text hook).** It's the viewer's own
   problem, in the words *they* would type into Google or say to a friend. It's not ours.
   - "Why does your shop's website load so slowly?"
   - "Why does ChatGPT give a different answer every time?"
   - "How does Google Maps know there's traffic?"
   - "Why is my Python loop so slow?"

   Name **who** it is for (your shop, your app, ChatGPT) and **the symptom they feel**
   (slow, wrong, different, costly). Not the mechanism, not our term for it.
2. **The proof (on screen by 3 s, ideally from frame 0).** It's the thing that answers
   "is that real?": the slow side vs the fast side, the two different ChatGPT answers
   side by side, the loop's timer crawling. It must be a visible comparison or a
   before/after that a viewer reads with the sound off. The second spoken line names it
   plainly: "This side has heavy photos. This side has light ones."

The cause (the term, the mechanism, our product) comes **after** the proof, in the setup.
Never in the hook.

**The cold-viewer test (rubric A20).** A fresh sub-agent is shown only the first two
spoken lines, the on-screen text and a description of the frames in the first 3 s. With
no title and no context, it must say: who this is for, what problem it's about, and why
it would keep watching. If its answer doesn't match the PLAN's `message` and `audience`,
the hook fails, whatever it scored on the table below.

## What the numbers say (and how much to trust them)

| Fact | Source quality | What it means for us |
|---|---|---|
| Shorts analytics show **Viewed vs. Swiped Away**; guides put a healthy Short at **70–80 % viewed** | Third-party benchmarks (subscribr, Galloway summaries); YouTube publishes no threshold | Compare against our own last 10 Shorts, not a universal number. A low ratio is a frame-0/topic problem, not a pacing problem |
| A retention curve at **≥ 80 % at 3 s** means the hook did its job | Practitioner rule of thumb | Our Gate-B proxy: something on frame 0 already states the promise |
| **63 %** of TikTok's highest-CTR ads state the key message in the first 3 s (TikTok's auction-ads creative guide; a secondary guide quotes 67 %) | Platform-published correlation, not causation | Say the claim in second 1, not second 5 |
| Meta: 9:16 + sound on + safe zones + **one extra element (an early hook, a human, voice-over, text overlay, lo-fi)** → 56 % higher CTR, 30 % higher 3-s play rate | Meta analysis as reported by Adobe | Hooks are one of five levers; stacking two (voice + on-screen claim) is the default |
| Google's study of 2,000+ Shorts ads: the winners are "Shorts-first", open with a **question**, low-key tone, talk like a friend, avoid ad aesthetics | Google Creative Works via Think with Google | No title cards, no logo stings, no "In this video…" |
| Headline experiments (meta-analysis of 8,977 A/B tests, Le Quéré & Matias 2025, PMC11704130 — abstract only, full text not read): click-through is **curvilinear in concreteness** — too vague loses, too concrete loses | Peer-reviewed registered report | The hook names the specific thing *and* withholds the answer. "This Python trick" is too vague; "Use `dict.get` instead of `if key in d`" is too complete |

Curiosity, per Loewenstein's information-gap theory, is the itch to answer a *specific*
question you now know you can't answer. Vague teases don't open a gap; they open a shrug.

## The three channels must say one thing

Every hook is written as a triple. If any line contradicts or dilutes the others, rewrite.

| Channel | Rule | Limit |
|---|---|---|
| **Verbal** (VO, first sentence) | Starts on frame 0 — no breath, no music-only lead-in. First word is content ("Nested loops…", not "So,"/"Hey guys") | ≤ 12 words, ≤ 4 s spoken |
| **Text** (on-screen, not the caption) | States the claim or the question as a headline. Never repeats the VO verbatim (Mayer redundancy) — it compresses it | ≤ 6 words, display ≥ 96 px, inside the core safe zone |
| **Visual** | Already moving at t=0 and *is* the subject: the bug, the result, the race, the before/after. Not a background | Readable as a still: it is also the cover frame |

Caption track (word-synced) runs underneath from word one; it is not the text hook.

## Hook taxonomy for tech and teaching content

Each type: when to use it, the template, and the visual that must accompany it.

1. **Result-first** — show the end state, then rewind. Best for products and builds.
   - "This took 4 lines instead of 40." / Visual: the 40-line block collapsing into 4.
2. **Contradiction / myth-bust** — state the common belief, then deny it.
   - "`is` and `==` are not the same — and it'll bite you at 257." / Visual: `256 is 256 → True`, `257 is 257 → False` typed live.
3. **"You're doing X wrong"** (the correction) — only when we can prove the better way.
   - "Stop using `+=` to build strings in a loop." / Visual: a timer race, `+=` vs `''.join`.
4. **Stakes** — name what getting it wrong costs the viewer (money, time, a broken build).
   - "This is the question that ends most Amazon phone screens in minute 5." (only if sourced)
5. **Specific question** (Google's top-performing Shorts-ad opener) — a question the viewer can't answer yet.
   - "What does a computer actually store when it 'understands' a word?" / Visual: the word "cat" dissolving into a column of numbers.
6. **Challenge / pause-test** — gives the viewer a task in second 1.
   - "Find the bug in 5 seconds." / Visual: 6 lines of code with a visible countdown ring.
7. **Visual pattern interrupt** — something moves that shouldn't (a list reversing itself, a graph that redraws). Pair with a one-line VO; the interrupt alone is decoration.
8. **Number claim** — a measured, surprising number from `research/run.txt`.
   - "38× faster. Same answer. One line changed." (only a number we measured)
9. **Before/after split** — left half pain, right half fix, same frame. Default for service videos: "Your customers wait 6 hours for a reply. Here they wait 6 seconds."
10. **Build-story stake** — a real number from the repo or ledger.
    - "200 days. Three paying users. Here's the one thing I'd change." (only your own real numbers)

Types that suit each pillar: ai-term → 2, 5, 7; python → 2, 3, 8; build → 1, 6; longform → 1, 5, 8; product → 1, 9;
service → 9, 4; build-story → 10, 1.

## What kills a hook (any one = rewrite)

- It only makes sense once you know the topic: a riddle, a bare number pair ("10 vs 5"),
  a metaphor ("a photo on a diet"), or our product's name before the viewer's problem.
- The first line is a statement about other people ("many shoppers leave…") instead of
  the viewer's own question ("why does *your* site…").
- The comparison that proves it comes after 3 s, or never.

- A logo, channel intro, title card, or "Welcome back" in the first 2 s.
- Music-only first second, or the VO starting after 0.5 s.
- Topic statements ("Today we're learning about hash maps") — a topic is not a gap.
- Throat-clearing words in the first five: so, okay, hey, guys, in this video, did you know.
- A promise the video doesn't pay off (YouTube's own A/B test tool ranks title/thumbnail
  variants by **watch-time share, not CTR** — a lie that wins the click loses the test).
- A static first frame (black, blank ink, a slow fade from nothing).
- The answer revealed in the hook ("Use a hash map for Two Sum") — over-concrete, no gap.
- Text in the top 200 px or below y 1600, where platform UI sits (see `platform-specs.md` §1).
- Jargon the target viewer hasn't met yet as the first word ("Cosine similarity…").
- Claims we can't source: "most companies ask this", "99 % of devs" — unless the dossier proves it.

## 12 worked hooks (verbal / on-screen text / visual)

Written before the 10 Oct rule. #1 fails the cold-viewer test as written ("Ten
comparisons, or five lookups" has no question a stranger owns); its rule-compliant form is
"How do you find two numbers that add up to a target, fast?" over the two counters racing.
Check each against the two-part rule before borrowing it.

| # | Pillar | Verbal (frame 0) | Text | Visual at t=0 |
|---|---|---|---|---|
| 1 | python (Two Sum, the studio's first video) | "Ten comparisons, or five lookups. Same answer." | 10 vs 5 | Two counters racing over the array [3, 8, 1, 6, 4] |
| 2 | build (a CLI in 20 lines) | "This is a whole command-line tool. It's twenty lines." | 20 lines | The tool running in a terminal, then the file scrolling to show it's short |
| 3 | longform-sd (rate limiting) | "Your API just got 10,000 requests in one second. Which ones do you drop?" | 10,000 req/s | A flood of request dots hitting one server box |
| 4 | python (3.13 free-threading) | "Python just let four threads use four cores. Here's what that changes." | 4 threads → 4 cores | Four bars lighting together where before only one lit |
| 5 | ai-term (embeddings) | "'Cheap flights' and 'budget airfare' share zero words. Search still matches them." | 0 shared words | Two phrases sliding toward the same point |
| 6 | ai-term (attention) | "In 'the animal didn't cross the street because it was tired' — how does a model know what 'it' is?" | What is "it"? | The word "it" pulsing, faint lines reaching out |
| 7 | python (GIL) | "Four threads. Four cores. Python still uses one. Here's why." | 4 threads → 1 core | Four bars where only one ever lights |
| 8 | python (generators) | "This list of a billion numbers uses 200 bytes." (measured) | 1,000,000,000 items | Memory meter that refuses to rise |
| 9 | Python gotcha | "This default argument remembers every call. That's a bug." | It remembers | `def add(x, items=[])` printing a growing list |
| 10 | product (a Maps lead extractor) | "Every business on this map, in a spreadsheet, in one click." | 1 click → CSV | Real screen recording: pins → rows filling |
| 11 | service (a chat bot for a shop) | "Your shop gets 40 'price kya hai?' messages a day. This answers all of them." (40 only if sourced; else drop the number) | Price kya hai? ×40 | Phone with a stack of unread WhatsApp chats, then replies landing |
| 12 | build-story | "I spent 3 weeks on a feature 4 people used." (real number) | 3 weeks · 4 users | Analytics chart with a flat line |

## Writing three, scoring three (Gate A3)

Write three hooks of **different types** (e.g. one question, one result-first, one stakes).
Score each 0–2 on six criteria. Max 12.

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| **Gap specificity** | topic/vague ("a cool trick") | names the domain | names the exact object and withholds the answer |
| **Speed** | claim lands after 3 s | 1.5–3 s | claim spoken *and* on screen by 1.5 s |
| **Visual proof** | background/decor at t=0 | relevant but static | the subject itself, already in motion, readable as a still |
| **Channel alignment** | VO, text, visual say different things | two agree | all three state one idea; text compresses VO, doesn't copy it |
| **Truth / payoff** | unsourced or unpaid claim | sourced but payoff weaker than promised | sourced (`research/`) and the payoff exceeds it |
| **Audience fit** | needs a term the viewer lacks | fits devs generally | names the exact viewer's situation (learning Python, shipping an AI feature, running a shop) |

Rules: pick the highest score; tie → the one with the stronger *Visual proof*; anything
below **8** → write a fourth. Record the table and the reason in `PLAN.md`.

Two gates sit above the score. A hook that fails either is out, whatever it scored:

- **Two-part shape:** the viewer's question first, then a visible comparison by 3 s.
- **Cold-viewer test (A20):** a stranger can say who it's for and what problem it's about.

Whatever the taxonomy type (stakes, number claim, myth-bust), it is phrased as the
viewer's question and backed by the proof.

## Checklist before leaving the hook

- [ ] Line 1 is the viewer's own question in their words; the comparison is visible by 3 s.
- [ ] `A20: PASS (cold viewer)` is in PLAN §10.
- [ ] First spoken word at ≤ 0.2 s; no silent or music-only lead.
- [ ] On-screen hook text ≤ 6 words, ≥ 96 px, within y 200–1440 on 9:16.
- [ ] Frame 0 snapshot works as a cover (readable claim + striking subject).
- [ ] The promise names a specific object; the answer is withheld until the last third.
- [ ] Every number in the hook appears in `research/sources.md` or `run.txt`.
- [ ] Nothing in the first 2 s is branding.

## Sources

- https://subscribr.ai/youtube-strategy/youtube-shorts-analytics-metrics-growth
- https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention
- https://megadigital.ai/en/blog/tiktok-ad-creative/
- https://ads.tiktok.com/business/library/Auction_Ads_Creative_Tips.pdf (63 % figure via the guide; PDF text not machine-readable here)
- https://blog.adobe.com/en/publish/2024/11/04/unlock-potential-reels-best-practices-for-creative-success-using-adobe-creative-cloud
- https://business.google.com/in/think/marketing-strategies/short-form-video-advertising-tips/
- https://business.google.com/us/think/future-of-marketing/creative-best-practices-youtube-ads/
- https://support.google.com/youtube/answer/13861714 (Test & Compare optimises watch-time share)
- https://outlierkit.com/resources/youtube-scriptwriting-methods-compared/
- https://www.somake.ai/blog/youtube-shorts-aspect-ratio
