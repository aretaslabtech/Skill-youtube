# Retention and story

A video keeps people when it keeps a question open and keeps paying small debts on time.
This file gives the spines (with second-level timings), the pacing numbers, how to read
the two kinds of retention graph, and where a CTA can go without costing the curve.

## Word budget first

> **Override from review:** the first Short (97 words in 44 s) was "too fast, too
> much content". **Use ≤ 2.0 words/s and 60–90 s for teaching videos.** The 2.6 words/s
> figure below is the research ceiling, not our target.

Narration runs at **~2.6 words/s** (≈ 156 wpm — brisk-conversational; Guo et al.'s 6.9 M-session
edX study found fast, enthusiastic delivery more engaging than slow, formal delivery).
Budget the script before writing it, and leave 1–2 s of silence on the payoff.

| Length | Max words | Beats (one idea each) |
|---|---|---|
| 30 s | 70 | 7–9 |
| 45 s | 105 | 10–13 |
| 60 s | 140 | 13–17 |
| 4 min long-form | 600 | 5–7 chapters × 4–6 beats |

If the script is over budget, cut a beat. Never speed the voice up past 1.1×.

## Short spine (30–60 s) — "Promise · Proof-in-steps · Payoff · Loop"

| Window (45 s Short) | Job | Rules |
|---|---|---|
| 0–1.5 s **Hook** | Open the gap (see `hooks.md`) | VO from frame 0; subject moving; ≤ 6-word headline |
| 1.5–5 s **Frame** | Why it matters / the setup | State the constraint or stakes in one sentence. Show the input (the array, the sentence, the shop's inbox) |
| 5–30 s **Build** | 3–4 steps that each change visible state | One new thing on screen every 3–4 s; each step answers a small question and raises the next |
| 30–38 s **Payoff** | The insight / the answer / the result | Lands at **65–85 % of runtime**. Bigger type, `voltage` accent, 1 s of held silence or a sting |
| 38–43 s **Takeaway** | One sentence the viewer can repeat | ≤ 10 words on screen; this is the line people screenshot |
| 43–45 s **Loop/CTA** | End on a line that flows into frame 0 | End card ≤ 2.5 s; last frame visually rhymes with the first |

For 30 s: compress Build to 2 steps. For 60 s: 4 steps plus one "twist" (an edge case, the
wrong-answer path) at ~60 % to re-open the gap before the payoff.

**Length choice.** Third-party data clusters the best Short completion at 15–45 s (tutorials
25–40 s, story 30–45 s); but learners need more time: our default is 60–90 s for teaching (rubric A8, after a
44 s Short was judged "too fast") and 30–50 s for product. Shorts may run up to 3 min, but a Short over 1 min
with any Content ID claim is blocked globally — keep licensed music out of anything > 60 s.

## Long-form spine (3–6 min, 16:9)

| Time | Section | Rules |
|---|---|---|
| 0–20 s | **Cold open** | Result first: the finished visual, the measured number, or the broken thing. No logo, no "welcome back" |
| 20–35 s | **Promise** | Say exactly what they'll be able to do by the end (Schmoyer's hook→promise→payoff). YouTube's "Intro" metric = % still watching at 30 s; the promise must be complete before it |
| 35–60 s | **Map** | One frame showing the 3–4 chapters as a path; return to it at each chapter break (signalling) |
| 1–4:30 | **Chapters** | Each chapter is a mini Hook→Build→Payoff loop (Kitchen/Blackman): open one question, close it before opening the next |
| every 45–75 s | **Re-hook** | Change at least two of: visual mode (code → diagram → screen), question, scale, speaker energy. MrBeast's doc escalates stakes every 60–90 s |
| ~70 % | **Biggest payoff** | Put the most valuable point where attention is most fragile, not at the very end |
| last 20–30 s | **Synthesis + one CTA** | One-line takeaway, then the next video (end screen in the last 5–20 s) |

Chapter titles go in the description as timestamps (0:00 first) so YouTube builds chapters.

## Open loops

- **One open at a time on Shorts; at most two on long-form.** More than two and viewers stop
  trusting that you'll pay them off.
- Open with a specific question; close it explicitly ("So that's why it's O(n)").
- Loop types that suit teaching:
  - **The withheld answer**: "There's a one-line fix — but first, watch it fail."
  - **The counter**: a visible counter (comparisons made, ms elapsed) that the viewer wants to see stop.
  - **The wrong path**: show the naive solution running and slowing; the gap is "what's faster?".
  - **The forward pointer** (long-form only): "Remember this number — it comes back in chapter 3."
- Never open a loop in the last 20 % of a Short — there is no time to pay it.

## Pacing — how often something must change

| Format | Visual change | New information | Hold after a key change |
|---|---|---|---|
| Short / Reel | every **1.5–3 s** (a move, a highlight, a cut, a value updating) | every **3–4 s** | ≥ 0.8 s still before the next change |
| Long-form | every **4–8 s** | every 10–20 s | ≥ 1.2 s; hold diagrams 2–3 s after the last element lands |

"Change" means state changes: a pointer advances, a cell fills, a line highlights, a number
ticks. A slow drift or parallax on a static slide is **not** a change (Gate B7). Third-party
data puts high-performing Shorts at one cut every 2–4 s; for motion-graphics videos we hit
that with in-frame state changes rather than hard cuts.

Pacing comes from the script, not from speeding up the render: if the VO pauses, the
visual must be doing the work in that pause.

## Reading the graphs

### Shorts / Reels
- **Views** (since 31 Mar 2025) count every start and replay, with no minimum watch time.
  For comparisons with older Shorts, and for monetisation, use **engaged views** (Advanced
  Mode).
- **Viewed vs. Swiped Away** = the hook/topic test. Low → frame 0, the topic, or the cover
  frame are wrong. Rewrite the hook type, not the middle.
- **Average percentage viewed** can exceed **100 %** because replays count. A curve that ends
  above its 3-s value means the ending loops.
- Shape diagnosis:
  - steep drop in 0–3 s → hook; 
  - steady slide → beats too long or not changing state;
  - cliff at one timestamp → that beat (jargon, a static hold, a muddled visual);
  - drop in the last 3 s → the end card or a "subscribe" ask; cut it.

### Long-form
- **Intro** (% at 30 s), **top moments**, **spikes** (rewatch or confusion — check which), **dips**,
  **continuous decline** (normal to a point). A spike right after a code reveal usually means
  the code was too fast; a dip right after a tangent means cut the tangent.
- Our checks after every long-form: intro %, where the first dip is, whether the 70 % payoff
  has a top moment. Write the finding into the next PLAN.md.

## Loopable endings (Shorts)

The loop is a design decision, not luck.
1. **Sentence loop**: the last line is grammatically completed by the first.
   End: "…and that's why you never write—" → Start: "—nested loops for Two Sum."
2. **Visual rhyme**: last frame = first frame's layout (same array, same colours), now solved.
3. **Counter reset**: end on the counter going back to 0 as the hook frame starts it.
4. **No outro**: no "thanks for watching", no 5-s logo. End card ≤ 2.5 s and it shares the
   first frame's background so the cut back to frame 0 is invisible.
5. Keep the final second free of music swells that resolve — a resolved cadence signals "end".

## CTAs that don't cost retention

- **One CTA per video**, specific and earned: "That's how RAG finds the paragraph — next week:
  how it ranks them." Never "like, share and subscribe".
- **Shorts**: the CTA is the last spoken line (≤ 8 words) *after* the payoff, or it is the loop
  line itself. No mid-Short "follow for more" — it creates an exit point.
- **Product/service**: the CTA can be visual from the payoff onward (store badge, a "message us"
  button) while the VO finishes the proof.
- **YouTube Shorts**: use the **related video** link (YouTube Studio → the Short → related
  video) to point to the long-form; it shows under the channel handle, needs advanced features.
  It can't be set via the API — note it in `POST.json.notes` for whoever posts.
- **Long-form**: one soft mention after the first big payoff (~60–70 %), then the end screen in
  the final 5–20 s pointing to the next video, not to "subscribe".
- Pinned comment carries the link/keyword; the description has no URLs from us (deliver.py
  adds tracked links).

## Story spines by pillar

| Pillar | Spine |
|---|---|
| ai-term / python | Question the viewer can't answer → one concrete example (no jargon) → the example *is* the mechanism → name the term → one real use → where it breaks → takeaway |
| build | The finished thing running → 3–4 build steps (changed lines + visible effect) → it runs → the one idea that made it work |
| longform-ai / longform-sd | Cold open → promise → map → 3–5 chapters (hook → build → payoff → one-line recap) → biggest payoff at ~70% → full-map recap → one CTA |
| (one-example concept) | Question → concrete example (no jargon) → the example *is* the mechanism → name the term → where it's used → where the analogy breaks (1 line) |
| product | Moment of magic → the pain it removes → 2–3 real moments → one real number → store CTA |
| service | Owner's pain in their words → before/after split → how it works in 3 steps → proof (real work) → one CTA (e.g. message us) |
| build-story | The number (stake) → what we tried → what broke → what we learned (one sentence) → what's next |

## Sources

- https://support.google.com/youtube/answer/15424877 (3-min Shorts, Content ID > 1 min)
- https://techcrunch.com/2025/03/26/youtube-is-changing-how-youtube-shorts-views-are-counted
- https://support.google.com/youtube/answer/9314415 (key moments for audience retention)
- https://support.google.com/youtube/answer/14075157 (related video on Shorts)
- https://subscribr.ai/youtube-strategy/youtube-shorts-analytics-metrics-growth
- https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention
- https://outlierkit.com/resources/youtube-scriptwriting-methods-compared/
- https://passionfru.it/mrbeast-leaked-document-81151/
- https://www.netinfluencer.com/mrbeast-productions-leaked-internal-document-rosanna-pansino/
- https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.txt
- https://business.google.com/in/think/marketing-strategies/short-form-video-advertising-tips/
