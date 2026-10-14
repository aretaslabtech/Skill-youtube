# Teaching formats — how to teach with motion

Our teaching videos win on one thing: the viewer *sees* the mechanism change state, in
sync with one calm sentence at a time. This file turns the research into build rules.

## Evidence we build on

- **Mayer's multimedia principles** (Dartmouth summary of the 12): words + pictures beat
  words alone; cut the extraneous; cue what matters; narration + graphics beats narration +
  graphics + the same text; labels go next to what they label; show it *while* you say it;
  segment; pre-train key terms; a friendly conversational voice.
- **3Blue1Brown's own rules** (FAQ): concrete before abstract; open with the key exercise,
  not the definition; "never start with definitions"; the pedagogical order is not the
  logical order; every animation needs an identifiable purpose; visuals and narration make
  the same point; good audio matters more than polish.
- **Guo, Kim & Rubin 2014** (edX, 6.9 M sessions): shorter videos, informal delivery, and
  Khan-style *drawing as you explain* engage more than slides or polished lecture cuts.
- **A 2025 field study (829 students, intro Python)**: text-only worked examples cost more
  immediate mental effort than visual ones; a step-by-step memory trace alone (Python Tutor
  style) helps less than trace **plus** one abstract/metaphor view; novices get lost in
  unlabelled trace detail.
- **ByteByteGo's animated diagrams** (third-party frame measurement): loops of 2.1–2.75 s
  where only **1.2–3.6 % of the canvas changes** — the structure stays still and one flow moves.

## Mayer, applied (each line is a Gate check)

| Principle | Rule in our videos |
|---|---|
| Coherence | No decorative particles, stock B-roll, or ambient drifting shapes. If removing an element loses no meaning, remove it |
| Signalling | Exactly one highlight colour for "look here" (`caution` outline = being read; `voltage` = the answer). The highlight arrives ≤ 200 ms before the VO says the thing |
| Redundancy | On-screen text ≤ 6 words per beat: labels, numbers, the key term. **Never put the narration sentence on screen as a paragraph.** Word-synced captions are the one exception (they serve sound-off viewers, 2–4 words at a time, small, in their own band) |
| Spatial contiguity | Labels sit on/next to the thing (≤ 40 px away), not in a legend. Variable names float above their tile |
| Temporal contiguity | The visual change and the spoken word happen within ±150 ms. Timeline beats are keyed to word timestamps |
| Segmenting | One idea per beat; a 0.3–0.7 s breath at each beat boundary (B16: ≤ 0.7 s of dead air); long-form uses chapter cards |
| Pre-training | If a term is needed later (e.g. "hash map"), show it once early as a 1-word label on a simple picture |
| Modality | Explain with VO + picture; text is for things the eye must compare (numbers, code) |
| Personalisation / voice | "you" and "we", contractions, the same cloned human voice every day |

## Format A — worked-example walkthrough (python, build, system-design chapters)

> The default rotation has no interview questions. This arc is for
> showing a mechanism on a worked example: a naive way, the insight, the better way, the
> cost. Two Sum below is only the reference for the visual vocabulary (it was the studio's
> first video).

**Arc:** problem → naive → insight → optimal → complexity → takeaway.

| Beat | Short (45 s) | Long-form (4 min) | Visual |
|---|---|---|---|
| Problem | 0–6 s | 0:00–0:30 | Problem types on in mono (≤ 2 lines), example input drawn as tiles |
| Naive | 6–14 s | 0:30–1:15 | Naive code (≤ 6 lines) + the pointer pair moving, a **comparison counter** climbing in `error` |
| Insight | 14–20 s | 1:15–1:50 | One sentence; the reframe drawn ("instead of searching, *remember*") |
| Optimal | 20–34 s | 1:50–3:10 | Code (≤ 8 lines) on the left/top, **state panel** (dict, stack, window) beside it, the active line highlighted as the state changes |
| Complexity | 34–40 s | 3:10–3:40 | Counters side by side, then O(n²) → O(n) morph; for long-form a quick n=10/1,000/1,000,000 table from `run.txt` |
| Takeaway | 40–45 s | 3:40–4:00 | One reusable pattern sentence: "When you need a pair, store what you've seen." |

Rules: the code on screen is the code in `research/solution.py`; every printed value comes
from `run.txt`. Show the edge case (empty input, duplicates) in long-form only.

## Format B — a hard idea through one simple example

> **Not for Shorts scripts** (Oct 2026). `script-voice.md` now puts real output first and
> allows an analogy of one sentence at most; developers found an analogy-led Short
> childish. Use this format only inside a long-form chapter that needs an intuition, and
> keep the section for its visual ideas.

1. **Ask** a question the viewer can't answer (gap).
2. **One everyday example** — concrete, specific, culturally neutral or local-everyday for
   your audience (a coffee order, a train ticket, a library shelf). No jargon yet.
3. **Let the example do the mechanism**: every step of the real algorithm happens to the
   example on screen.
4. **Name the term** only now (3Blue1Brown: definitions are where you arrive).
5. **One real use** ("this is how Spotify's 'similar songs' works" only if sourced).
6. **Where the analogy breaks**, one line. This is what makes it trustworthy.
7. **Takeaway** sentence.

Banned examples (overused to the point of slop): king − man + woman = queen; "imagine a
library" for databases unless the library *does* the mechanism; robots/brains for AI.

## Animated code — rules

- **Size**: 9:16 code at 34 px JetBrains Mono, ≤ 22 visible characters per line, ≤ 9 lines
  visible. 16:9: 30 px, ≤ 60 chars, ≤ 16 lines. Rewrite code to fit; never shrink it.
- **Reveal**: type-on only for the first ≤ 1 line (it reads as "live"). Otherwise reveal by
  line, keyed to the VO, 150–250 ms per line.
- **Active line**: full-width bar `voltage@16 %` behind it; line number turns `voltage`. One
  active line at a time.
- **Stepping**: each execution step = (1) highlight the line, (2) 200 ms later update the state
  panel, (3) hold ≥ 0.6 s. Never change code and state at the same instant.
- **State panel**: variables as mono tiles with the name above; the cell being read gets a
  `caution` outline; a written cell flashes `voltage` for 300 ms then settles to text colour.
- **Diffs**: when code changes (naive → optimal), morph only the changed tokens; removed
  tokens fade in `error` and collapse; unchanged lines don't move.
- **Output**: printed output appears in a terminal strip under the code, values copied from
  `run.txt`.
- **No scrolling code** faster than 1 line per 0.4 s; prefer cutting to the relevant 6 lines.
- **Syntax colours** (navy-code; other looks map the same roles): keywords text 700, names text 400, strings `caution`,
  numbers `voltage`. Don't use a rainbow theme.

## Data-structure visual vocabulary

| Structure / pattern | Draw it as | Motion that explains |
|---|---|---|
| Array | Row of square mono tiles, index above in `mist` | Pointer chevrons slide between tiles; read = `caution` outline |
| Two pointers | Two labelled chevrons (`L`, `R`) | They converge; the comparison appears between them |
| Sliding window | Rounded bracket over a tile range | Bracket stretches/shrinks; the running sum ticks |
| Hash map / set | Two-column table (key │ value) growing downward | Lookup = a ray from the current tile to the matching row, row flashes; miss = row ghost fades |
| Stack | Vertical tile tower, open top | Push drops in from above; pop lifts out and fades |
| Queue / BFS | Horizontal lane, enqueue right, dequeue left | Frontier nodes in `caution`, visited dim to `mist` |
| Linked list | Boxes + arrows | Re-pointing arrows animate their endpoint, not the box |
| Tree | Top-down, 3 levels max on 9:16 | Recursion path lights root→leaf; return values float up |
| DP table | Grid; row/col headers | Cell fills from the two cells it depends on (draw the dependency arrows briefly) |
| Recursion | Call-stack column beside the code | Frames push/pop with their local variables |
| Complexity | Two step counters or a race bar | Counters run in real proportion from `run.txt`; then the O-notation morphs |
| Vectors / embeddings | 2-D scatter with labelled points | Points slide to positions; similarity = an arc/angle that shrinks |

Rule from ByteByteGo: the layout is fixed; **only the thing being explained moves**. If more
than ~20 % of the frame is moving at once, the viewer doesn't know where to look.

## What the reference channels do, and what to steal

| Channel | What they do visually | Why it works | Steal / avoid |
|---|---|---|---|
| **3Blue1Brown** | One persistent canvas; objects transform into one another instead of cutting; colour carries identity (a variable keeps its colour across scenes) | Continuity lets the viewer track identity — transformation *is* the explanation | Steal: colour-as-identity, morph rather than cut. Avoid: 20-s slow builds in a Short |
| **Fireship** | Deadpan, dense script; a visual every 1–2 s (code, logos, memes, sound effects on the beat); 100-second format | Entertainment as the delivery mechanism; nothing that doesn't teach, joke or transition survives | Steal: density, ruthless cutting, timed visual punches. Avoid: borrowed meme footage (copyright, and it is not our identity) |
| **ByteByteGo** | Clean boxes-and-arrows diagrams, numbered steps, small coloured flows moving along arrows on a static structure | The structure is learnable at a glance; motion only shows flow/order | Steal: numbered steps, static structure + moving flow. Avoid: more than 7 boxes on a 9:16 frame |

## Worked beat sheet — "Two Sum" (45 s Short)

Input `nums = [3, 8, 1, 6, 4]`, `target = 10`. Verified: naive finds (3, 4) on comparison 10;
the hash-map pass finds it on lookup 5 (index 4 needs 6, stored at index 3) → `[3, 4]`.

| t (s) | VO (words) | Visual (state change) | Text |
|---|---|---|---|
| 0–2 | "Ten comparisons, or five lookups. Same answer." (7) | Two counters (0) above the 5 tiles; both start ticking | 10 vs 5 |
| 2–6 | "Two Sum: find two numbers that add to ten." (9) | Problem types on; `target = 10` badge | PYTHON |
| 6–13 | "The obvious way checks every pair." (6) | L/R chevrons sweep all pairs; counter climbs to 10 in `error`; pair (6,4) finally flashes | 10 checks |
| 13–15 | "That's n-squared. It falls over at a million." (8) | Counter label morphs to O(n²) | O(n²) |
| 15–20 | "Flip the question: for each number, what do I *need*?" (10) | Above tile 3: "need 7" bubble appears | need = 10 − x |
| 20–31 | "Need seven? Not seen. Store three. Need two? Not seen. Store eight…" (12) | Pointer walks tiles 0→3; each step: active code line → need bubble → lookup ray into the table (miss) → row written | — |
| 31–35 | "Four needs six. Six is already here." (7) | Lookup ray hits row `6 → 3`; row flashes `voltage`; answer [3, 4] lands big | [3, 4] |
| 35–40 | "One pass. Five lookups. O of n." (7) | Lookup counter stops at 5 beside the naive 10; O(n²) → O(n) | O(n) |
| 40–43 | "When you need a pair, remember what you've seen." (9) | Takeaway in headline type | remember what you've seen |
| 43–45 | "Next: Valid Parentheses—" (3) | Board resets to the first frame layout (loop) | #02 next |

Total ≈ 78 words, inside the 105-word budget, leaving silence on 31–35 s.

## Worked beat sheet — "What is a vector embedding?" (50 s Short)

Example: a search for **"cheap flights"** matching a page titled **"budget airfare"** — zero
shared words. Real dimension counts (e.g. 384 for all-MiniLM-L6-v2, 1,536 for OpenAI
text-embedding-3-small) must be verified in `research/` before they go on screen.

| t (s) | VO | Visual | Text |
|---|---|---|---|
| 0–3 | "'Cheap flights' and 'budget airfare' share zero words. Search still matches them." | Two phrases, shared-word counter reads 0 | 0 shared words |
| 3–9 | "Keyword search can't. It only sees letters." | Letter-matching lines fail to connect | — |
| 9–18 | "So give every phrase a position instead — numbers for what it *means*." | Phrase 1 dissolves into a column `[0.82, 0.11, …]`; a dot drops onto a 2-D plane | — |
| 18–28 | "Phrases about cheap travel land close together. 'Flight delay' lands nearby. 'Chocolate cake' lands far away." | Three more dots slide into place; clusters form | — |
| 28–36 | "Matching is now geometry: how close are the arrows?" | Arrows from origin; angle between the two travel phrases shrinks to a small arc; cosine value from `run.txt` | cos = 0.8x |
| 36–41 | "That list of numbers is an embedding." | The term appears *now*, attached to the column | embedding |
| 41–46 | "Real ones have hundreds of dimensions, not two — we drew two so you can see it." | 2-D plane fans into many faint axes | where it breaks |
| 46–50 | "Meaning becomes distance. That's how RAG finds your docs—" | Back to the two phrases (loop) | meaning = distance |

The cosine value shown comes from actually embedding the phrases in `research/solution.py`.

## Sources

- https://services.dartmouth.edu/TDClient/1806/Portal/KB/PrintArticle?ID=171655
- https://www.3blue1brown.com/faq/
- https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.txt
- https://arxiv.org/html/2509.26466v1
- https://raw.githubusercontent.com/yizhiyanhua-ai/fireworks-tech-graph/main/references/motion-effects.md
- https://skills.sh/jarmen423/skills/fireship-video-style
