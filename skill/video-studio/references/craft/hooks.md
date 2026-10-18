# Hooks — the first 1–3 seconds

The hook is not "the intro". It is **frame 0 to ~1.5 s**, and on Shorts/Reels it is the
whole decision. Everything below is checkable against a plan or a snapshot.

## The rule: name the thing and the tension, then show the proof

> Review data (Oct 2026): on a new Instagram page, **67 % of viewers swiped away in the first
> 3 s** and the average watch was **8 s**. The hooks were questions in the viewer's words
> ("Why does your coding agent…?"), so they were clear, but they named no concrete thing and
> carried no tension a developer couldn't guess.

An earlier version of this file said "open on the viewer's own question". That fixed riddle
hooks ("Ten comparisons, or five lookups") but produced soft, generic openers. Every one of
the 20 top tech Shorts we studied (the library below) **names the concrete subject in the
first sentence** and pairs it with a tension. None opens with an analogy, a definition or
"have you ever wondered". So every hook now has three parts:

1. **Sentence 1 (spoken at 0 s): the subject plus a tension, in ≤ 14 words.** The subject is a
   language, tool, company, number or line of code. The tension is a mistake, a surprise, a
   stake or a contradiction.
   - "Python's `lstrip` just deleted half your filename." (mistake)
   - "Redis runs on one thread and still does 100,000 requests a second." (contradiction)
   - "Claude Code rewrote my whole file to change one line. Here's the fix." (stake)
   - "I added 0.1 to 0.2 in JavaScript and got 0.30000000000000004." (surprise)

   A question is fine if it names the subject: "Why does Postgres need VACUUM at all?" Not
   "Why is your app slow?"

   **Spoken, not headline-ese.** The 14-word limit is a ceiling, not a target, and it never
   means dropping verbs, articles or "you". Say it the way a person would say it to a friend:
   "You built a new website, but nobody's visiting?" not "New website, no visitors?". A
   clipped headline belongs on the on-screen slab (≤ 14 characters a line); the voice speaks
   the full sentence. Test it by reading it aloud: if no one talks like that, rewrite it.
2. **The proof (on screen by 1.5 s, ideally from frame 0).** It's the code, the output, the
   number or the diagram, readable with the sound off. The viewer must be able to see that
   the claim is real before they decide to swipe.
3. **The open loop.** The hook withholds the answer: the fix, the reason, the number three of
   three. Then the video **rehooks every 10–15 s** ("but", "here's the catch", "the last one is
   the weird one").

The background (definitions, the mechanism, our product) comes after the proof, and only
as much as the payoff needs.

### Problem before tool (owner review, 15 Oct 2026)

"The concrete subject" must be **something the viewer already has**: a job, a business
problem, a tool they use. It must not be the solution's vocabulary. "My read-only Python MCP
server let Claude Code write a full database copy" was concrete, and it passed the gates,
but the owner rejected it: "No one knows what VACUUM is… nobody knows what a read-only MCP
server is and they don't have any reason to copy the database, so why will they ever
watch it." Curiosity needs a foothold. Loewenstein's information-gap theory, and Kang et
al. (2009), find curiosity peaks at *moderate* prior knowledge (an inverted U). Zero
knowledge of the subject gives no gap, only a swipe. The classic Dropbox explainer worked
because it showed a file saved on a laptop opening on a phone. It never mentioned sync
protocols.

So the hook runs in this order: **the situation → what goes wrong → the tool or trick that
fixes it.**

1. **Sentence 1 is the situation, in the viewer's words.** Name a job they have done or will
   be asked to do, with its stake: "Your boss wants an AI that answers questions from the
   sales database." Or name the failure from that situation: "I gave Claude our sales
   database, read-only. It walked off with a full copy." The tension sits in the situation:
   money, customer data, a broken build or a wasted day.
2. **The obvious fix, then why it fails.** This is the open loop: "So you make it read-only.
   That's not enough."
3. **The technical name arrives as the answer** (`VACUUM INTO`, `set_authorizer`, MCP),
   after the viewer knows why they need it. A term in the first 5 s must be one the median
   viewer has already typed (Python, SQL, Claude, a database, an API). A term they haven't
   (MCP server, VACUUM, an RFC, a flag) waits until the problem is planted.

The test is: *Could this viewer meet this problem at work in the next year, and would they
recognise it from sentence 1 alone?* If the honest answer is "only if they already know the
fix", the hook is built from the solution's side. Rewrite it.

**The cold-viewer test (rubric A20).** A fresh sub-agent, playing a developer scrolling
Reels, is shown only the first two spoken lines, the on-screen text and a description of the
frames in the first 3 s. With no title and no context, it must name the concrete subject, the
tension, and what it expects to learn, and say it would keep watching. If not, the hook fails,
whatever it scored on the table below.

## Hook library (20 templates from real Shorts, Oct 2026)

Use one of these for sentence 1. View counts were public YouTube counts in Oct 2026.

| # | Template | Real example |
|---|---|---|
| 1 | **Broken expectation you can reproduce**: "I tried [simple thing] and got [absurd result]" | Fireship, 0.1 + 0.2 (8.7M) |
| 2 | **N reasons + open loop**: "N reasons [X] is [fast]. The last one is unintuitive." | ByteByteGo, Redis (1.3M) |
| 3 | **Easy mistake**: "Here's a [lang] mistake that's very easy to make." | b001 (3.3M) |
| 4 | **Prohibition**: "You should never do this in [lang]." | Indently (1.0M) |
| 5 | **Beginner upgrade**: "If you write [X], learn this [trick]." | b001 (2.3M) |
| 6 | **Provocative equation or question with a real answer** | 3Blue1Brown, word vectors (3.4M) |
| 7 | **Live demo hits a wall**: "[Agent] is doing [task] right now, and it just hit [obstacle]." | Tech With Tim (5.7M) |
| 8 | **Irony + stake (news)**: "The most [X] company just [ironic event]." | NetworkChuck (817K) |
| 9 | **Tiny cause, huge effect**: "One [person/bug] [huge outcome], all because [tiny measurable detail]." | Varun Mayya, XZ (507K) |
| 10 | **Scenario + "easy to guess… but"**: "[Setup]. What happens when [edge]? Easy to guess, but…" | Arpit Bhayani, MAX_INT (110K) |
| 11 | **Dated incident**: "On [date], [company] [failed]. Here's the real root cause." | Gaurav Sen, AWS (230K) |
| 12 | **Challenge a convention**: "Why can't we [thing everyone forbids]?" | Theo, .env (477K) |
| 13 | **Direct utility**: "Here's how to make [tool] [measurably better]." | Matt Pocock (299K) |
| 14 | **Bait-and-switch cold open**: an unrelated life hack, then "but here are N [tech] tricks" | Fireship, Linux (1.7M) |
| 15 | **Stake + concept**: "If you want to [real goal], you need to know [concept]." | Fireship, Big O (1.5M) |
| 16 | **Identity call-out**: "As [JS] developers we [habit everyone hides]…" | Fireship, console.log (1.3M) |
| 17 | **Giant number**: "[1 trillion] messages" / "[2 TB] of RAM in one…" | ByteByteGo (2.4M) |
| 18 | **Big-brand teardown**: "[Netflix]'s tech stack" | ByteByteGo (1.7M) |
| 19 | **Everyday "why" with a technical answer**: "Why do computers use RGB, not RBY?" | Fireship (3.6M) |
| 20 | **Name-the-behaviour**: "There's a name for [annoying AI habit]." | Coding with Lewis (1.7M) |

"N % of grads can't solve this" also works, but it's interview content, and this studio
never makes interview content.

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
| **Verbal** (VO, first sentence) | Starts on frame 0 — no breath, no music-only lead-in. Names the subject plus a tension; first word is content ("Python's…", not "So,"/"Hey guys") | ≤ 14 words (lint-checked) |
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
   - "One missing index took this checkout page from 40 ms to 9 seconds." (only if sourced or measured)
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

- It names no concrete thing: "Why is your app slow?", "This changes everything", "a cool
  trick". A developer can't tell what they'd learn.
- It names the solution's world, not the viewer's: the subject is a term or setup the viewer
  doesn't have yet ("a read-only MCP server", "VACUUM INTO"), so there is no problem they
  recognise (see "Problem before tool").
- It carries no tension a developer couldn't guess ("Caches make apps faster").
- It only makes sense once you know the topic: a riddle, a bare number pair ("10 vs 5"),
  or a metaphor ("a photo on a diet").
- It opens with an analogy, a definition, "have you ever", "imagine" or a greeting.
- The proof comes after 1.5 s, or never.

- A logo, channel intro, title card, brand sting or "Welcome back" in the first 3 s.
- Music-only first second, or the VO starting after 0.5 s.
- Topic statements ("Today we're learning about hash maps") — a topic is not a gap.
- Throat-clearing words in the first five: so, okay, hey, guys, in this video, did you know.
- A promise the video doesn't pay off (YouTube's own A/B test tool ranks title/thumbnail
  variants by **watch-time share, not CTR** — a lie that wins the click loses the test).
- A static first frame (black, blank ink, a slow fade from nothing).
- The answer revealed in the hook ("Use a hash map for Two Sum") — over-concrete, no gap.
- Text in the top 200 px or below y 1600, where platform UI sits (see `platform-specs.md` §1).
- A term beyond a CS student as the first word, unglossed ("MVCC…"). Known terms are fine.
- Claims we can't source: "most companies ask this", "99 % of devs" — unless the dossier proves it.

## 12 worked hooks (verbal / on-screen text / visual)

Written before the Oct 2026 rule. #1 fails it as written ("Ten comparisons, or five
lookups" names no subject); #3–#9 mostly pass. Check each against the three-part rule
before borrowing it.

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
| **Audience fit** | defines basics, or needs an unglossed term beyond a CS student | fits devs generally | names the exact developer situation (a Python version, an agent tool, a production system) |

Rules: pick the highest score; tie → the one with the stronger *Visual proof*; anything
below **8** → write a fourth. Record the table and the reason in `PLAN.md`.

Three gates sit above the score. A hook that fails any is out, whatever it scored:

- **Three-part shape:** subject plus tension in ≤ 14 words, proof on screen by 1.5 s, the
  answer withheld.
- **Lint (A18):** `script_lint.py` checks the length, the banned openers and that a concrete
  subject is named.
- **Cold-viewer test (A20):** a developer scrolling past can name the subject and the
  tension, and would keep watching.

## Checklist before leaving the hook

- [ ] Line 1 names the concrete subject plus a tension in ≤ 14 words; the proof is visible by 1.5 s.
- [ ] A rehook lands every 10–15 s.
- [ ] `A20: PASS (cold viewer)` is in PLAN §10.
- [ ] First spoken word at ≤ 0.2 s; no silent or music-only lead.
- [ ] On-screen hook text ≤ 6 words, ≥ 96 px, within y 200–1440 on 9:16.
- [ ] Frame 0 snapshot works as a cover (readable claim + striking subject).
- [ ] The promise names a specific object; the answer is withheld until the last third.
- [ ] Every number in the hook appears in `research/sources.md` or `run.txt`.
- [ ] Nothing in the first 3 s is branding.

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
- https://nautil.us/curiosity-depends-on-what-you-already-know-235803 (curiosity needs prior knowledge; Kang et al. 2009 inverted U)
- https://commoncraft.com/curse-knowledge-and-how-defeat-it (curse of knowledge; the Dropbox explainer shows the problem, not the protocol)
