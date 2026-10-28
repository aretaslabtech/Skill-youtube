# The 45 gates

Every video passes two gates. **Gate A** checks the plan, before any money is spent on voice.
**Gate B** checks the build, before and after rendering. Each line is pass or fail; there is
no partial credit. **Hard** gates block the video: a plan gets one rewrite, a build gets at
most two fix loops, and anything still failing is written into the post kit's notes —
never delivered silently.

The agent works from the full text in
[`skill/video-studio/references/quality-rubric.md`](../skill/video-studio/references/quality-rubric.md),
which has the exact thresholds and the reviewer prompts. This page is the map.

**Checked by `deliver.py`** (🔒): it refuses the video without them. For A16, A18, A19,
A20 and A21 it requires the pass line in `PLAN.md` — which the skill says to write only on the
reviewer's, linter's or scout's PASS — and for A22 the second opinion's `meta.json`. For C1
(documentary/crime pillars only) it requires the pass line plus `research/evidence-ledger.yaml`.
A23, A24, B17, B18 and B19 it measures itself, from the files, and so is the music level
(`mix_check.py`).

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
| A20 🔒 | Cold viewer: a fresh agent playing a developer scrolling Reels sees only the first 3 s and must name the subject, the tension and what it expects to learn, list every term it would look up (must be none) and name the problem from its own work | ✔ |
| A21 🔒 | Real problem (teaching pillars): a fresh scout agent ranks problems developers are asking about, each backed by ≥ 2 public links; the video's problem scores ≥ 9/15 (`references/problem-scout.md`) | ✔ |
| A22 🔒 | Second opinion (when `review.second_opinion_model` is set): a model from a different family reviews the script via OpenRouter and writes its own version from the same facts; true P1 fixes are adopted and the outcome is recorded as `A22: second opinion (<model>) adopted N, rejected M` (`scripts/second_opinion.py`) | ✔ |
| A23 🔒 | The published text is clean (`scripts/post_text.py`): ≤ 5 hashtags, none generic, a caption that opens on a sentence; invisible characters, em dashes and curly quotes are fixed automatically; the human score is advice in the kit | ✔ |
| A24 🔒 | Packaging (`scripts/packaging.py`): the first title ≤ 55 characters with no parenthetical, "explained" or chained clauses; 3 designed thumbnails (≤ 4 words each, the render's shape, ≤ 2 MB) for YouTube's Test & Compare | ✔ |
| A25 | The first payoff (the fix, result or promised number) is on screen by 10 s | ✔ |

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
| B19 🔒 | Voice first, at Reels level: the soundtrack is rebuilt from the stems so the voice comes up and the music doesn't; the file is −12 LUFS or louder — `remaster.py` | ✔ |

## Gate C — documentary / crime pillars (`crime-case`, `case-files`)

A separate, additive numbering so it never collides with the teaching-pillar gates above —
`crime-case` and `case-files` don't run A21 (problem scout) at all.

| Gate | Checks | Hard |
|---|---|---|
| C1 🔒 | Case scout: every claim used in the script traces to `research/evidence-ledger.yaml` with `script_safe: true` (`references/case-scout.md`); the plan carries `C1: PASS (case scout)` | ✔ |

**Totals:** 45 gates, 40 hard (A5, A17 and A21 only for teaching and long-form videos; A22
only when a second-opinion model is set; C1 only for `crime-case`/`case-files`), 12 checked
by `deliver.py` (5 of them measured from the files), plus the music-level check
(`mix_check.py`: voice levelled to −16 LUFS, music ≥ 20 dB under it), which `deliver.py`
also enforces.

## Where the gates came from

Almost none were in the first version. Each was added the day a video failed that way:

| Failure | Gates it produced |
|---|---|
| The first Short: 97 words in 44 seconds, "too fast, too much content" | A8 |
| A script that "considers the viewer as an expert"; a self-graded review that passed it | A14, A15, A16 (with a separate judge), A18 |
| Three simplifications that had become untrue | A19 |
| "The hook doesn't make sense… I am noticing this in all videos" | A2, A20 |
| "No one knows what VACUUM is… start with a business problem"; "no point making a video on a problem which no one is facing" | A20 (problem before tool), A21 |
| Two videos so alike "it will soon be noticed as AI generated"; footage in tiny cards | B11, B13, the look rotation |
| A rendered first frame that differed from every browser snapshot | B14 on the final file |
| 3–5 s gaps from padded frames | B16 |
| A third of all sentences losing their first ~0.2 s | B17 |
| Scripts that passed every Claude-judged gate and still taught nothing | A22 (a second model) |
| Twelve kits in a row with 6–8 hashtags, over Instagram's cap of 5 | A23 |
| 10.1k impressions at a 1.1 % click-through rate: headline titles cut off on phones, frame grabs for covers | A24 |
| Viewers leaving at 10–18 s, before a fix that arrived at 30–40 s | A25 |
| "The voiceover is still low": a music bed only 13 dB under the voice | `mix_check.py`, voice levelling |
| The bottom 40% of every Short left empty | B18 |
| "The voice is low compared to other people's posts": every render at −14 LUFS, Reels at −9 to −11 | B19 |

**The lesson:** gates written in prose get bent under pressure; gates checked in code
don't. When you catch a failure by eye, turn it into a line of code that refuses the next
one.
