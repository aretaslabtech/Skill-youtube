# The 38 gates

Every video passes two gates. **Gate A** checks the plan, before any money is spent on voice.
**Gate B** checks the build, before and after rendering. Each line is pass or fail; there is
no partial credit. **Hard** gates block the video: a plan gets one rewrite, a build gets at
most two fix loops, and anything still failing is written into the post kit's notes —
never delivered silently.

The agent works from the full text in
[`skill/video-studio/references/quality-rubric.md`](../skill/video-studio/references/quality-rubric.md),
which has the exact thresholds and the reviewer prompts. This page is the map.

**Checked by `deliver.py`** (🔒): it refuses the video without them. For A16, A18, A19 and
A20 it requires the pass line in `PLAN.md` — which the skill says to write only on the
reviewer's or linter's PASS. B17 and B18 it measures itself, from the files.

## Gate A — the plan

| Gate | Checks | Hard |
|---|---|---|
| A1 | One idea: the message is one sentence, and every beat serves it | ✔ |
| A2 | Sentence 1 is ≤ 14 words and names the concrete subject plus a tension; proof on screen by 1.5 s; no branding before 3 s | ✔ |
| A3 | Three hooks of different types were written and scored out of 12; the best scores ≥ 8 | ✔ |
| A4 | Every fact and on-screen number has a source in `research/sources.md` | ✔ |
| A5 | Code was run; the output on screen is pasted from the real run | teaching videos |
| A6 | Every beat has a visual that explains (a state change, a comparison, a real screen) | ✔ |
| A7 | On-screen text ≤ 6 words per beat, never the sentence being spoken | ✔ |
| A8 | A teaching Short runs 35–60 s (75 s cap); the configured pause between sentences is kept, and length comes from cutting sentences | ✔ |
| A9 | Something new on screen every 3–4 s and a spoken rehook every 10–15 s on a Short; a re-hook every 45–75 s on long-form | Shorts |
| A10 | The payoff lands in the last third, not in the hook; it ends on the payoff, no recap | |
| A11 | One specific call to action | ✔ |
| A12 | Real assets first; nothing faked | ✔ |
| A13 | Not a repeat of any earlier video (`ledger.py check`) | ✔ |
| A14 | The viewer is fixed: a developer or CS student who already codes; known terms are never defined | ✔ |
| A15 | At least one artifact to save (spoken and on screen), ≥ 3 named real things per 30 s, terms beyond a CS student glossed in ≤ 8 words | ✔ |
| A16 🔒 | New to me: a fresh agent playing a mid-level developer must name a concrete thing it learned and who it would send the video to; a separate judge grades it | ✔ |
| A17 | Long-form chapters end on a one-line recap | long-form |
| A18 🔒 | `script_lint.py`: hook ≤ 14 words naming a concrete subject with no banned opener, no sentence over 20 words, ≥ 3 named specifics per 30 s, no hard term before its gloss, no idioms | ✔ |
| A19 🔒 | Expert review: a fresh agent flags anything false or misleading, each with a fix as short and true | ✔ |
| A20 🔒 | Cold viewer: a fresh agent playing a developer scrolling Reels sees only the first 3 s and must name the subject, the tension and what it expects to learn | ✔ |

## Gate B — the build

| Gate | Checks | Hard |
|---|---|---|
| B1 | `npx hyperframes check` passes: no contrast errors, overflow or overlap | ✔ |
| B2 | Safe zones on 9:16: meaning in y 200–1440, captions y 1440–1600 | ✔ |
| B3 | Readable on a phone: body ≥ 32 px, headlines ≥ 72 px, code ≥ 30 px | ✔ |
| B4 | One focal point per frame: the brand accent on at most one element | ✔ |
| B5 | No slop tells: gradient text, neon glows, banned fonts, stock people, emoji as decoration | ✔ |
| B6 | Frame 1 works as a thumbnail and cover | ✔ |
| B7 | Motion explains: something meaningful is mid-change at every beat midpoint | |
| B8 | Captions are word-synced, 2–4 words at a time, inside the caption band | ✔ |
| B9 | The voice is intelligible over the music (music about −20 dB, ducked) | ✔ |
| B10 | The end mark is ≤ 2 s, and the last frame rhymes with the first so a Short loops | |
| B11 | Real footage fills ≥ 80% of the frame for ≥ 50% of the runtime | ✔ |
| B12 | No beat midpoint shows more than ~40% empty canvas | ✔ |
| B13 | A fresh agent compares this video with the last three and doesn't call them one template | ✔ |
| B14 | A judge reviews ≥ 6 frames decoded from the **final MP4**, including frame 0 | ✔ |
| B15 | Sound follows motion: every reveal has a sound on its frame | |
| B16 | No silence over 0.7 s between voice lines (one ≤ 1.2 s payoff beat allowed) — `gap_check.py` | ✔ |
| B17 🔒 | Every word is heard: every voice line was made by `voice_build.py` and starts and ends on silence | ✔ |
| B18 🔒 | A 9:16 Short fills its frame down to the bottom edge — `fill_check.py` | ✔ |

**Totals:** 38 gates, 33 hard (A5 and A17 only for teaching and long-form videos), 6
checked by `deliver.py` (2 of them measured from the files).

## Where the gates came from

Almost none were in the first version. Each was added the day a video failed that way:

| Failure | Gates it produced |
|---|---|
| The first Short: 97 words in 44 seconds, "too fast, too much content" | A8 |
| A script that "considers the viewer as an expert"; a self-graded review that passed it | A14, A15, A16 (with a separate judge), A18 |
| Three simplifications that had become untrue | A19 |
| "The hook doesn't make sense… I am noticing this in all videos" | A2, A20 |
| Two videos so alike "it will soon be noticed as AI generated"; footage in tiny cards | B11, B13, the look rotation |
| A rendered first frame that differed from every browser snapshot | B14 on the final file |
| 3–5 s gaps from padded frames | B16 |
| A third of all sentences losing their first ~0.2 s | B17 |
| The bottom 40% of every Short left empty | B18 |

**The lesson:** gates written in prose get bent under pressure; gates checked in code
don't. When you catch a failure by eye, turn it into a line of code that refuses the next
one.
